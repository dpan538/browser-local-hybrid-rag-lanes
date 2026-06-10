#!/usr/bin/env python3
"""Diagnose browser-side Qwen/WebLLM hybrid-lane run records.

This script treats run outputs as experimental diagnostics, not paper claims.
It summarizes schema validity, Qwen invocation, deterministic skips, contract
failures, latency distributions, and environment flags.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parent.parent
CONDITIONS = ["all_generation", "hybrid_without_refusal", "full_hybrid"]


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def percentile(values: Iterable[float], percent: float) -> float | None:
    ordered = sorted(float(value) for value in values)
    if not ordered:
        return None
    position = (len(ordered) - 1) * percent / 100.0
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return ordered[int(position)]
    return ordered[low] * (high - position) + ordered[high] * (position - low)


def rounded(value: float | None) -> float | None:
    return None if value is None else round(value, 2)


def latency_summary(values: List[float]) -> Dict[str, float | None]:
    return {
        "p50": rounded(percentile(values, 50)),
        "p90": rounded(percentile(values, 90)),
        "p95": rounded(percentile(values, 95)),
        "max": rounded(max(values) if values else None),
    }


def schema_errors(rows: List[Dict[str, Any]], schema_path: Path) -> List[Dict[str, Any]]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors: List[Dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        for error in validator.iter_errors(row):
            errors.append({
                "row_index": index,
                "query_id": row.get("query_id"),
                "condition": row.get("condition"),
                "message": error.message,
                "path": list(error.path),
            })
    return errors


def failure_groups(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    counter: Counter[tuple[str, tuple[str, ...]]] = Counter()
    for row in rows:
        if not row.get("contract_metrics", {}).get("contract_failure"):
            continue
        keys = tuple(
            sorted(
                key
                for key, value in row.get("auto_contract", {}).items()
                if value == "fail"
            )
        )
        counter[(row.get("condition", ""), keys)] += 1
    return [
        {
            "condition": condition,
            "fail_keys": list(keys),
            "count": count,
        }
        for (condition, keys), count in sorted(counter.items())
    ]


def condition_summary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    output: Dict[str, Any] = {}
    for condition in CONDITIONS:
        subset = [row for row in rows if row.get("condition") == condition]
        qwen_rows = [
            row for row in subset
            if float(row.get("latency", {}).get("qwen_generation_latency_ms") or 0) > 0
        ]
        deterministic_rows = [row for row in subset if row not in qwen_rows]
        qwen_latency = [
            float(row["latency"]["qwen_generation_latency_ms"])
            for row in qwen_rows
        ]
        hybrid_latency = [
            float(row["latency"]["hybrid_system_latency_ms"])
            for row in subset
        ]
        output[condition] = {
            "rows": len(subset),
            "qwen_rows": len(qwen_rows),
            "deterministic_skip_rows": len(deterministic_rows),
            "contract_failures": sum(
                bool(row.get("contract_metrics", {}).get("contract_failure"))
                for row in subset
            ),
            "execution_modes": dict(Counter(row.get("execution_mode", "") for row in subset)),
            "qwen_generation_ms": latency_summary(qwen_latency),
            "hybrid_system_ms": latency_summary(hybrid_latency),
        }
    return output


def environment_summary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "cold_start_rows": sum(bool(row.get("env_flags", {}).get("cold_start")) for row in rows),
        "warmup_rows": sum(bool(row.get("env_flags", {}).get("warmup")) for row in rows),
        "warm_rows": sum(bool(row.get("env_flags", {}).get("warm")) for row in rows),
        "tab_backgrounded_rows": sum(bool(row.get("env_flags", {}).get("tab_backgrounded")) for row in rows),
        "long_task_gc_rows": sum(bool(row.get("env_flags", {}).get("long_task_gc")) for row in rows),
        "network_variance_rows": sum(bool(row.get("env_flags", {}).get("network_variance")) for row in rows),
        "manual_interruption_rows": sum(bool(row.get("env_flags", {}).get("manual_interruption")) for row in rows),
    }


def model_summary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    model_rows = [
        row for row in rows
        if row.get("answer", {}).get("model_meta", {}).get("producer")
        == "webllm_qwen3_5_0_8b_research_runtime"
    ]
    deterministic_rows = [
        row for row in rows
        if row.get("answer", {}).get("model_meta", {}).get("producer")
        == "deterministic_hybrid_system_v1"
    ]
    return {
        "qwen_model_meta_rows": len(model_rows),
        "deterministic_meta_rows": len(deterministic_rows),
        "model_ids": sorted({
            str(row.get("answer", {}).get("model_meta", {}).get("model_id"))
            for row in model_rows
            if row.get("answer", {}).get("model_meta", {}).get("model_id")
        }),
        "primary_model_identities": sorted({
            str(row.get("answer", {}).get("model_meta", {}).get("primary_model_identity"))
            for row in rows
            if row.get("answer", {}).get("model_meta", {}).get("primary_model_identity")
        }),
        "model_load_ms_values": sorted({
            round(float(row.get("answer", {}).get("model_meta", {}).get("model_load_ms")), 2)
            for row in model_rows
            if row.get("answer", {}).get("model_meta", {}).get("model_load_ms") is not None
        }),
    }


def diagnose_run(path: Path, schema_path: Path) -> Dict[str, Any]:
    rows = load_jsonl(path)
    failures = [
        row for row in rows
        if row.get("contract_metrics", {}).get("contract_failure")
    ]
    return {
        "path": str(path),
        "rows": len(rows),
        "queries": len({row.get("query_id") for row in rows}),
        "schema_errors": schema_errors(rows, schema_path),
        "by_condition": condition_summary(rows),
        "failure_groups": failure_groups(rows),
        "failure_query_ids": sorted({row.get("query_id") for row in failures}),
        "environment": environment_summary(rows),
        "model": model_summary(rows),
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# Qwen WebLLM Run Diagnostics",
        "",
        "This diagnostic treats run records as experimental instrumentation data,",
        "not as paper-ready findings.",
        "",
        "## Diagnostic Consequence",
        "",
        "This run is useful for pipeline and ablation triage, but it should",
        "not be expanded into strong paper claims yet. Environment flags such",
        "as `long_task_gc`, tab foregrounding, and browser visibility should be",
        "checked before treating latency summaries as more than diagnostics.",
        "",
        "The most useful current signal is not \"we have a finding\"; it is that the",
        "pipeline can now expose exactly where the candidate finding would need",
        "stronger evidence: refusal-boundary handling, Qwen invocation accounting,",
        "and clean browser latency measurement.",
        "",
    ]
    for run in report["runs"]:
        lines.extend([
            f"## {Path(run['path']).stem}",
            "",
            f"- Rows: {run['rows']}",
            f"- Queries: {run['queries']}",
            f"- Schema errors: {len(run['schema_errors'])}",
            f"- Failure query ids: {', '.join(run['failure_query_ids']) or 'none'}",
            "",
            "| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for condition in CONDITIONS:
            item = run["by_condition"][condition]
            lines.append(
                "| {condition} | {rows} | {qwen} | {skip} | {fail} | {qp50} | {qp95} | {hp50} | {hp95} |".format(
                    condition=condition,
                    rows=item["rows"],
                    qwen=item["qwen_rows"],
                    skip=item["deterministic_skip_rows"],
                    fail=item["contract_failures"],
                    qp50=item["qwen_generation_ms"]["p50"],
                    qp95=item["qwen_generation_ms"]["p95"],
                    hp50=item["hybrid_system_ms"]["p50"],
                    hp95=item["hybrid_system_ms"]["p95"],
                )
            )
        lines.extend([
            "",
            "Environment:",
            "",
            json.dumps(run["environment"], indent=2),
            "",
            "Failure groups:",
            "",
            json.dumps(run["failure_groups"], indent=2),
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", nargs="+", help="Run JSONL files to diagnose.")
    parser.add_argument(
        "--schema",
        default="schemas/run_record_schema.json",
        help="Run record JSON schema path.",
    )
    parser.add_argument("--json-out", default="", help="Optional JSON report path.")
    parser.add_argument("--md-out", default="", help="Optional Markdown report path.")
    args = parser.parse_args()

    schema_path = Path(args.schema)
    if not schema_path.is_absolute():
        schema_path = REPO_ROOT / schema_path

    report = {
        "schema": str(schema_path),
        "runs": [
            diagnose_run(Path(path), schema_path)
            for path in args.runs
        ],
    }

    if args.json_out:
        json_path = Path(args.json_out)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.md_out:
        md_path = Path(args.md_out)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_markdown(report) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if any(run["schema_errors"] for run in report["runs"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
