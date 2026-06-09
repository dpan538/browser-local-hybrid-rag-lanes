#!/usr/bin/env python3
"""Minimal Flask runner for the hybrid answer-lane pilot.

This app is intentionally small. It serves the experiment panel and exposes
`/api/run` so the browser UI and scripts can execute the same controlled
condition logic with server-side timing.

The default model backend is a deterministic stub. It does not download model
weights and does not claim real Qwen/WebLLM performance. The primary model
identity for real runs is `Qwen/Qwen3.5-0.8B`; real generation should be run in
the browser-local Qwen/WebLLM path, while server-side adapters are limited to
documented comparison probes.
"""

from __future__ import annotations

import json
import os
import re
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from flask import Flask, jsonify, request, send_from_directory
from jsonschema import Draft202012Validator

from scripts.auto_contract_check import check_contract, contract_metrics_from_auto
from scripts.model_backend import (
    ModelBackendError,
    backend_config,
    backend_name,
    call_model,
)


ROOT = Path(__file__).resolve().parent
PANEL_DIR = ROOT / "tools" / "experiment_panel"
LANE_RULES_PATH = ROOT / "config" / "lane_rules_v1.yaml"
REFUSAL_MATRIX_PATH = ROOT / "config" / "refusal_decision_matrix.csv"
PROMPT_PACK_PATH = ROOT / "config" / "condition_prompt_pack_v1.json"
ANALYSIS_PLAN_PATH = ROOT / "docs" / "EXPERIMENT_EXECUTION_PLAN.md"
RUN_RECORD_SCHEMA_PATH = ROOT / "schemas" / "run_record_schema.json"


def repo_path_from_env(env_name: str, default: str) -> Path:
    value = os.environ.get(env_name, default)
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


MASTER_FIXTURE_PATH = repo_path_from_env(
    "HYBRID_LANE_MASTER_FIXTURE_PATH",
    "fixtures/experiment_fixture.jsonl",
)
RUNTIME_PATH = repo_path_from_env(
    "HYBRID_LANE_RUNTIME_PATH",
    "fixtures/runtime_view/experiment_fixture.runtime.jsonl",
)
EVAL_PATH = repo_path_from_env(
    "HYBRID_LANE_EVAL_PATH",
    "fixtures/evaluation_view/experiment_fixture.eval.jsonl",
)
WARMUP_PATH = repo_path_from_env(
    "HYBRID_LANE_WARMUP_PATH",
    "fixtures/warmup_queries.jsonl",
)
BROWSER_PILOT_PATH = repo_path_from_env(
    "HYBRID_LANE_BROWSER_PILOT_PATH",
    "fixtures/drafts/browser_pilot_subset_v0.jsonl",
)
RUNS_DIR = repo_path_from_env("HYBRID_LANE_RUNS_DIR", "runs")

CONDITION_ALIASES = {
    "all-generation": "all_generation",
    "all_generation": "all_generation",
    "hybrid-without-refusal": "hybrid_without_refusal",
    "hybrid_without_refusal": "hybrid_without_refusal",
    "full-hybrid": "full_hybrid",
    "full_hybrid": "full_hybrid",
}

DETERMINISTIC_FIELDS = [
    "source",
    "rights_label",
    "reuse_permission",
    "public_domain_status",
]

app = Flask(__name__)
SERVER_STATE = {
    "request_count": 0,
    "started_at": time.perf_counter(),
}


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def run_record_validator() -> Draft202012Validator | None:
    schema = load_json(RUN_RECORD_SCHEMA_PATH)
    return Draft202012Validator(schema) if schema else None


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def protocol_artifact_hashes() -> Dict[str, str]:
    artifacts = {
        "fixture_hash": MASTER_FIXTURE_PATH,
        "runtime_view_hash": RUNTIME_PATH,
        "rule_table_hash": LANE_RULES_PATH,
        "refusal_matrix_hash": REFUSAL_MATRIX_PATH,
        "prompt_pack_hash": PROMPT_PACK_PATH,
        "analysis_plan_hash": ANALYSIS_PLAN_PATH,
    }
    hashes: Dict[str, str] = {}
    for key, path in artifacts.items():
        value = sha256_file(path)
        if value:
            hashes[key] = value
    return hashes


def safe_run_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return normalized or "browser_pilot_run"


def prompt_pack() -> Dict[str, Any]:
    return load_json(PROMPT_PACK_PATH)


def runtime_rows() -> List[Dict[str, Any]]:
    return load_jsonl(RUNTIME_PATH)


def eval_rows() -> List[Dict[str, Any]]:
    return load_jsonl(EVAL_PATH)


def find_eval_row(query_id: str) -> Dict[str, Any] | None:
    for row in eval_rows():
        if row.get("query_id") == query_id:
            return row
    return None


def evaluator_contract_labels(query_id: str) -> Dict[str, Any] | None:
    row = find_eval_row(query_id)
    if not row:
        return None
    meta = row.get("evaluation_labels", {}).get("fixture_meta", {})
    return {
        "refusal_expected": bool(meta.get("refusal_expected")),
        "conflict_expected": bool(meta.get("conflict_expected")),
    }


def warmup_rows() -> List[Dict[str, Any]]:
    return load_jsonl(WARMUP_PATH)


def browser_pilot_rows() -> List[Dict[str, Any]]:
    return load_jsonl(BROWSER_PILOT_PATH)


def find_runtime_row(query_id: str) -> Dict[str, Any] | None:
    for row in runtime_rows() + warmup_rows() + browser_pilot_rows():
        if row.get("query_id") == query_id:
            return row
    return None


def normalize_condition(condition: str) -> str:
    try:
        return CONDITION_ALIASES[condition]
    except KeyError as exc:
        allowed = ", ".join(sorted(CONDITION_ALIASES))
        raise ValueError(f"unknown condition '{condition}', expected one of {allowed}") from exc


def ms_since(start: float) -> float:
    return (time.perf_counter() - start) * 1000.0


def call_local_model(prompt: str, max_tokens: int = 512) -> Tuple[str, Dict[str, Any]]:
    """Call the configured local model backend.

    The default backend is a timed stub so protocol code can be validated
    without downloading model weights. This server-side hook is not the primary
    Qwen/WebLLM experiment path.
    """
    text, meta = call_model(prompt, max_tokens=max_tokens)
    meta["prompt_pack_version"] = prompt_pack().get("version")
    return text, meta


def deterministic_fields(row: Dict[str, Any]) -> Dict[str, str]:
    record = (row.get("evidence_packet", {}).get("records") or [{}])[0]
    output: Dict[str, str] = {}
    for field in DETERMINISTIC_FIELDS:
        output[field] = str(record.get(field, "[not provided in source]"))
    return output


def should_refuse(row: Dict[str, Any]) -> bool:
    evidence_state = row.get("routing_inputs", {}).get("evidence_state")
    intent_signal = row.get("routing_inputs", {}).get("intent_signal")
    if intent_signal == "refusal_required" and evidence_state in {"partial", "missing", "contradictory"}:
        return True
    return evidence_state in {"missing", "contradictory"}


def execution_mode_for(row: Dict[str, Any], condition: str) -> str:
    intent_signal = row.get("routing_inputs", {}).get("intent_signal")
    if condition == "all_generation":
        return "generative_answer"
    if condition == "full_hybrid" and should_refuse(row):
        return "deterministic_refusal"
    if intent_signal == "mixed":
        return "compound_answer"
    if intent_signal in {"source/rights", "source_rights", "rights_only"}:
        return "deterministic_render"
    return "generative_answer"


def assemble_answer(row: Dict[str, Any], condition: str) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    t0 = time.perf_counter()
    timings: Dict[str, Any] = {
        "retrieval_latency_ms": 0.0,
        "deterministic_assembly_latency_ms": None,
        "qwen_generation_latency_ms": None,
        "hybrid_system_latency_ms": None,
        "ttft_ms": None,
        "tokens_per_second": None,
        "latency_saved_by_deterministic_ms": None,
    }

    execution_mode = execution_mode_for(row, condition)
    record = (row.get("evidence_packet", {}).get("records") or [{}])[0]
    question = row.get("query", {}).get("text", "")

    answer: Dict[str, Any] = {
        "output_mode": execution_mode,
        "source": "",
        "rights_label": "",
        "reuse_permission": "",
        "public_domain_status": "",
        "research_guidance": "",
        "refusal": None,
        "caveats": [],
    }

    if execution_mode == "deterministic_refusal":
        det_start = time.perf_counter()
        answer["refusal"] = "I cannot answer this from the provided evidence."
        answer["caveats"].append("deterministic_refusal_missing_or_contradictory_evidence")
        timings["deterministic_assembly_latency_ms"] = ms_since(det_start)
        timings["qwen_generation_latency_ms"] = 0.0
        timings["hybrid_system_latency_ms"] = ms_since(t0)
        return answer, timings, execution_mode

    if condition in {"hybrid_without_refusal", "full_hybrid"}:
        det_start = time.perf_counter()
        answer.update(deterministic_fields(row))
        timings["deterministic_assembly_latency_ms"] = ms_since(det_start)
    else:
        timings["deterministic_assembly_latency_ms"] = 0.0

    needs_generation = execution_mode in {"generative_answer", "compound_answer"} or condition == "all_generation"
    if needs_generation:
        prompts = prompt_pack()
        condition_prompt = prompts.get("conditions", {}).get(condition, {})
        prompt = json.dumps(
            {
                "prompt_pack_version": prompts.get("version"),
                "global_constraints": prompts.get("global_constraints", []),
                "condition_prompt": condition_prompt,
                "condition": condition,
                "question": question,
                "evidence_packet": row.get("evidence_packet", {}),
            },
            ensure_ascii=False,
        )
        gen_start = time.perf_counter()
        generated_text, model_meta = call_local_model(prompt)
        timings["qwen_generation_latency_ms"] = ms_since(gen_start)
        answer["research_guidance"] = generated_text
        answer["model_meta"] = model_meta

    if condition == "all_generation":
        answer["source"] = f"Generated source summary for {record.get('source', 'unknown source')}"
        answer["rights_label"] = f"Generated rights summary: {record.get('rights_label', 'unknown')}"
        answer["reuse_permission"] = (
            f"Generated reuse note: {record.get('reuse_permission', 'unknown')}"
        )
        answer["public_domain_status"] = (
            f"Generated status note: {record.get('public_domain_status', 'unknown')}"
        )

    if condition == "full_hybrid":
        answer["refusal"] = "none"

    answer["caveats"].append("evidence_correctness_requires_source_audit")
    timings["hybrid_system_latency_ms"] = ms_since(t0)
    return answer, timings, execution_mode


def environment_flags(payload: Dict[str, Any]) -> Dict[str, Any]:
    SERVER_STATE["request_count"] += 1
    client_env = payload.get("client_environment", {}) or {}
    warm_state = payload.get("warm_state", "warm")
    long_task_delta = int(client_env.get("long_task_count_delta", 0) or 0)
    long_task_total = int(client_env.get("long_task_count", 0) or 0)
    return {
        "cold_start": SERVER_STATE["request_count"] == 1 or warm_state == "cold_start",
        "warmup": warm_state == "warmup",
        "warm": warm_state == "warm",
        "tab_backgrounded": (
            client_env.get("visibility_state") == "hidden"
            or bool(client_env.get("was_backgrounded", False))
        ),
        "long_task_gc": bool(long_task_delta or long_task_total),
        "network_variance": False,
        "manual_interruption": False,
        "client_environment": client_env,
    }


def build_run_record(
    row: Dict[str, Any],
    condition: str,
    answer: Dict[str, Any],
    timings: Dict[str, Any],
    env_flags: Dict[str, Any],
    execution_mode: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    auto_contract = check_contract(
        {
            "query_id": row["query_id"],
            "condition": condition,
            "answer": answer,
        },
        row,
        evaluator_contract_labels(row["query_id"]),
    )
    contract_metrics = contract_metrics_from_auto(auto_contract)

    return {
        "run_id": payload.get("run_id") or "pilot_run_001",
        "query_id": row["query_id"],
        "condition": condition,
        "intent_label": row.get("routing_inputs", {}).get("intent_signal", ""),
        "execution_mode": execution_mode,
        "rule_match": {
            "rule_version": row.get("routing_inputs", {}).get("rule_version"),
            "rule_name": None,
            "routing_undefined": False,
            "routing_notes": "api_runner_scaffold",
        },
        "evidence_state": row.get("routing_inputs", {}).get("evidence_state"),
        "field_state_checklist": row.get("evidence_packet", {}).get("field_checklist", {}),
        "latency": {
            **timings,
            "warm_state": payload.get("warm_state", "warm"),
        },
        "contract_metrics": contract_metrics,
        "format": {
            "output_format": (
                "structured_fields_plus_natural_language"
                if execution_mode == "compound_answer"
                else "bounded_natural_language"
                if execution_mode == "generative_answer"
                else "refusal_template"
                if execution_mode == "deterministic_refusal"
                else "structured_fields"
            ),
            "format_consistency_score": None,
            "compound_answer": execution_mode == "compound_answer",
        },
        "protocol_artifacts": protocol_artifact_hashes(),
        "answer": answer,
        "auto_contract": auto_contract,
        "env_flags": env_flags,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def root() -> Any:
    return send_from_directory(PANEL_DIR, "index.html")


@app.get("/tools/experiment_panel/")
def panel_index() -> Any:
    return send_from_directory(PANEL_DIR, "index.html")


@app.get("/tools/experiment_panel/<path:path>")
def panel_asset(path: str) -> Any:
    return send_from_directory(PANEL_DIR, path)


@app.get("/api/fixtures/runtime")
def api_runtime() -> Any:
    return jsonify(runtime_rows())


@app.get("/api/fixtures/evaluation")
def api_evaluation() -> Any:
    return jsonify(eval_rows())


@app.get("/api/fixtures/browser-pilot")
def api_browser_pilot() -> Any:
    return jsonify(browser_pilot_rows())


@app.post("/api/run")
def api_run() -> Any:
    payload = request.get_json(force=True) or {}
    query_id = payload.get("query_id")
    condition_raw = payload.get("condition", "")
    if not query_id:
        return jsonify({"error": "query_id is required"}), 400

    try:
        condition = normalize_condition(condition_raw)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    row = find_runtime_row(query_id)
    if row is None:
        return jsonify({"error": f"query_id '{query_id}' not found"}), 404

    try:
        answer, timings, execution_mode = assemble_answer(row, condition)
    except ModelBackendError as exc:
        return jsonify({"error": str(exc)}), 501

    env_flags = environment_flags(payload)
    run_record = build_run_record(
        row=row,
        condition=condition,
        answer=answer,
        timings=timings,
        env_flags=env_flags,
        execution_mode=execution_mode,
        payload=payload,
    )
    return jsonify(run_record)


@app.get("/api/model/config")
def api_model_config() -> Any:
    return jsonify(backend_config())


@app.post("/api/model/probe")
def api_model_probe() -> Any:
    payload = request.get_json(force=True) or {}
    prompt = payload.get(
        "prompt",
        "Return one short sentence confirming that the configured comparison backend is reachable.",
    )
    max_tokens = int(payload.get("max_tokens", 64))
    started = time.perf_counter()
    try:
        text, meta = call_local_model(str(prompt), max_tokens=max_tokens)
    except ModelBackendError as exc:
        return jsonify({
            "ok": False,
            "backend": backend_config(),
            "error": str(exc),
            "elapsed_ms": ms_since(started),
        }), 501
    return jsonify({
        "ok": True,
        "backend": backend_config(),
        "text": text,
        "model_meta": meta,
        "elapsed_ms": ms_since(started),
    })


@app.post("/api/runs/save")
def api_save_runs() -> Any:
    payload = request.get_json(force=True) or {}
    records = payload.get("records") or []
    if not isinstance(records, list) or not records:
        return jsonify({"error": "records must be a non-empty list"}), 400

    requested_run_id = str(payload.get("run_id") or records[0].get("run_id") or "browser_pilot_run")
    run_id = safe_run_id(requested_run_id)
    validator = run_record_validator()
    if validator:
        for index, record in enumerate(records):
            errors = sorted(validator.iter_errors(record), key=lambda item: list(item.path))
            if errors:
                return jsonify({
                    "error": "run record schema validation failed",
                    "record_index": index,
                    "record_query_id": record.get("query_id"),
                    "message": errors[0].message,
                    "path": list(errors[0].path),
                }), 400

    record_run_ids = {str(record.get("run_id", "")) for record in records}
    if len(record_run_ids) != 1:
        return jsonify({
            "error": "records must share one run_id",
            "run_ids": sorted(record_run_ids),
        }), 400
    if safe_run_id(next(iter(record_run_ids))) != run_id:
        return jsonify({
            "error": "payload run_id does not match record run_id",
            "payload_run_id": run_id,
            "record_run_id": next(iter(record_run_ids)),
        }), 400

    output_dir = RUNS_DIR / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{run_id}_records.jsonl"
    allow_overwrite = bool(payload.get("allow_overwrite", False))
    if output_path.exists() and not allow_overwrite:
        return jsonify({
            "error": "run output already exists",
            "path": str(output_path.relative_to(ROOT) if output_path.is_relative_to(ROOT) else output_path),
            "hint": "set allow_overwrite=true only for an intentional rerun",
        }), 409

    temp_path = output_path.with_suffix(".jsonl.tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")
    temp_path.replace(output_path)

    return jsonify({
        "ok": True,
        "run_id": run_id,
        "records": len(records),
        "path": str(output_path.relative_to(ROOT) if output_path.is_relative_to(ROOT) else output_path),
    })


@app.get("/api/health")
def api_health() -> Any:
    return jsonify({
        "ok": True,
        "runtime_rows": len(runtime_rows()),
        "eval_rows": len(eval_rows()),
        "warmup_rows": len(warmup_rows()),
        "browser_pilot_rows": len(browser_pilot_rows()),
        "model_backend": backend_name(),
        "model_backend_config": backend_config(),
        "prompt_pack_version": prompt_pack().get("version"),
        "paths": {
            "master_fixture": str(MASTER_FIXTURE_PATH.relative_to(ROOT) if MASTER_FIXTURE_PATH.is_relative_to(ROOT) else MASTER_FIXTURE_PATH),
            "runtime": str(RUNTIME_PATH.relative_to(ROOT) if RUNTIME_PATH.is_relative_to(ROOT) else RUNTIME_PATH),
            "evaluation": str(EVAL_PATH.relative_to(ROOT) if EVAL_PATH.is_relative_to(ROOT) else EVAL_PATH),
            "warmup": str(WARMUP_PATH.relative_to(ROOT) if WARMUP_PATH.is_relative_to(ROOT) else WARMUP_PATH),
            "browser_pilot": str(BROWSER_PILOT_PATH.relative_to(ROOT) if BROWSER_PILOT_PATH.is_relative_to(ROOT) else BROWSER_PILOT_PATH),
            "runs_dir": str(RUNS_DIR.relative_to(ROOT) if RUNS_DIR.is_relative_to(ROOT) else RUNS_DIR),
        },
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8787, debug=False)
