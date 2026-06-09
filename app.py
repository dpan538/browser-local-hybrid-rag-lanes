#!/usr/bin/env python3
"""Minimal Flask runner for the hybrid answer-lane pilot.

This app is intentionally small. It serves the experiment panel and exposes
`/api/run` so the browser UI and scripts can execute the same controlled
condition logic with server-side timing.

The default model backend is a deterministic stub. It does not download model
weights and does not claim real Qwen/WebLLM performance. Replace
`call_local_model` or set up a new backend when the protocol is ready for a
real local model run.
"""

from __future__ import annotations

import json
import os
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from flask import Flask, jsonify, request, send_from_directory

from scripts.auto_contract_check import check_contract


ROOT = Path(__file__).resolve().parent
RUNTIME_PATH = ROOT / "fixtures" / "runtime_view" / "experiment_fixture.runtime.jsonl"
EVAL_PATH = ROOT / "fixtures" / "evaluation_view" / "experiment_fixture.eval.jsonl"
WARMUP_PATH = ROOT / "fixtures" / "warmup_queries.jsonl"
PANEL_DIR = ROOT / "tools" / "experiment_panel"
MASTER_FIXTURE_PATH = ROOT / "fixtures" / "experiment_fixture.jsonl"
LANE_RULES_PATH = ROOT / "config" / "lane_rules_v1.yaml"
REFUSAL_MATRIX_PATH = ROOT / "config" / "refusal_decision_matrix.csv"
PROMPT_PACK_PATH = ROOT / "config" / "condition_prompt_pack_v1.json"
ANALYSIS_PLAN_PATH = ROOT / "docs" / "EXPERIMENT_EXECUTION_PLAN.md"

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


def prompt_pack() -> Dict[str, Any]:
    return load_json(PROMPT_PACK_PATH)


def runtime_rows() -> List[Dict[str, Any]]:
    return load_jsonl(RUNTIME_PATH)


def eval_rows() -> List[Dict[str, Any]]:
    return load_jsonl(EVAL_PATH)


def warmup_rows() -> List[Dict[str, Any]]:
    return load_jsonl(WARMUP_PATH)


def find_runtime_row(query_id: str) -> Dict[str, Any] | None:
    for row in runtime_rows() + warmup_rows():
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
    without downloading model weights.
    """
    backend = os.environ.get("HYBRID_LANE_MODEL_BACKEND", "stub")
    if backend != "stub":
        raise RuntimeError(
            f"model backend '{backend}' is not implemented in this reproducible scaffold"
        )

    delay_ms = float(os.environ.get("HYBRID_LANE_STUB_DELAY_MS", "80"))
    time.sleep(delay_ms / 1000.0)
    text = (
        "Generated research guidance: use the exact evidence fields for source "
        "and rights, then interpret the public-health context cautiously."
    )
    return text, {
        "backend": backend,
        "max_tokens": max_tokens,
        "stub_delay_ms": delay_ms,
        "prompt_chars": len(prompt),
        "prompt_pack_version": prompt_pack().get("version"),
    }


def deterministic_fields(row: Dict[str, Any]) -> Dict[str, str]:
    record = (row.get("evidence_packet", {}).get("records") or [{}])[0]
    output: Dict[str, str] = {}
    for field in DETERMINISTIC_FIELDS:
        output[field] = str(record.get(field, "[not provided in source]"))
    return output


def should_refuse(row: Dict[str, Any]) -> bool:
    evidence_state = row.get("routing_inputs", {}).get("evidence_state")
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
    return {
        "cold_start": SERVER_STATE["request_count"] == 1 or warm_state == "cold_start",
        "warmup": warm_state == "warmup",
        "warm": warm_state == "warm",
        "tab_backgrounded": client_env.get("visibility_state") == "hidden",
        "long_task_gc": bool(client_env.get("long_task_count", 0)),
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
    )
    contract_failure = any(value == "fail" for value in auto_contract.values())
    contract_warning = any(value == "warning" for value in auto_contract.values())
    unsupported_upgrade = auto_contract.get("rights_label_upgrade") in {"warning", "fail"}

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
        "contract_metrics": {
            "contract_failure": contract_failure,
            "contract_warning": contract_warning,
            "field_omission_count": sum(1 for value in auto_contract.values() if value == "fail"),
            "field_mutation_count": sum(
                1 for key, value in auto_contract.items()
                if key.endswith("_mutation") and value == "fail"
            ),
            "unsupported_upgrade_count": 1 if unsupported_upgrade else 0,
            "unsupported_claims": 0,
            "hallucination_count": 0,
            "hallucination_severity": None,
            "refusal_false_positive": False,
            "refusal_false_negative": False,
        },
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
    except RuntimeError as exc:
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


@app.get("/api/health")
def api_health() -> Any:
    return jsonify({
        "ok": True,
        "runtime_rows": len(runtime_rows()),
        "eval_rows": len(eval_rows()),
        "warmup_rows": len(warmup_rows()),
        "model_backend": os.environ.get("HYBRID_LANE_MODEL_BACKEND", "stub"),
        "prompt_pack_version": prompt_pack().get("version"),
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8787, debug=False)
