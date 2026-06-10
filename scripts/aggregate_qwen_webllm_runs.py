#!/usr/bin/env python3
"""Aggregate multiple browser-side Qwen/WebLLM run JSONL files.

This script is for segmented-run diagnostics. It treats raw records as
instrumentation data, not paper-ready findings.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

from diagnose_qwen_webllm_run import (
    CONDITIONS,
    condition_summary,
    environment_summary,
    failure_groups,
    load_jsonl,
    model_summary,
    schema_errors,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def row_key(row: Dict[str, Any]) -> Tuple[str, str]:
    return str(row.get("query_id", "")), str(row.get("condition", ""))


def duplicate_pairs(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    counts = Counter(row_key(row) for row in rows)
    return [
        {"query_id": query_id, "condition": condition, "count": count}
        for (query_id, condition), count in sorted(counts.items())
        if count > 1
    ]


def missing_pairs(rows: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    query_ids = sorted({str(row.get("query_id", "")) for row in rows if row.get("query_id")})
    seen = {row_key(row) for row in rows}
    missing: List[Dict[str, str]] = []
    for query_id in query_ids:
        for condition in CONDITIONS:
            if (query_id, condition) not in seen:
                missing.append({"query_id": query_id, "condition": condition})
    return missing


def run_inputs(paths: List[Path]) -> List[Dict[str, Any]]:
    output: List[Dict[str, Any]] = []
    for path in paths:
        rows = load_jsonl(path)
        output.append({
            "path": str(path),
            "rows": len(rows),
            "queries": len({row.get("query_id") for row in rows}),
            "query_range": [
                min((str(row.get("query_id")) for row in rows if row.get("query_id")), default=""),
                max((str(row.get("query_id")) for row in rows if row.get("query_id")), default=""),
            ],
        })
    return output


def aggregate(paths: List[Path], schema_path: Path) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for path in paths:
        rows.extend(load_jsonl(path))

    failures = [
        row for row in rows
        if row.get("contract_metrics", {}).get("contract_failure")
    ]
    generation_error_rows = [
        row for row in rows
        if row.get("answer", {}).get("model_meta", {}).get("generation_error")
    ]
    timeout_rows = [
        row for row in generation_error_rows
        if "timeout" in str(row.get("answer", {}).get("model_meta", {}).get("generation_error", "")).lower()
    ]
    by_condition = condition_summary(rows)
    by_condition_generation_errors = {
        condition: sum(
            row.get("condition") == condition
            for row in generation_error_rows
        )
        for condition in CONDITIONS
    }
    by_condition_timeouts = {
        condition: sum(row.get("condition") == condition for row in timeout_rows)
        for condition in CONDITIONS
    }

    return {
        "schema": str(schema_path),
        "inputs": run_inputs(paths),
        "rows": len(rows),
        "queries": len({row.get("query_id") for row in rows}),
        "schema_errors": schema_errors(rows, schema_path),
        "duplicate_pairs": duplicate_pairs(rows),
        "missing_pairs": missing_pairs(rows),
        "by_condition": by_condition,
        "by_condition_generation_errors": by_condition_generation_errors,
        "by_condition_timeouts": by_condition_timeouts,
        "failure_groups": failure_groups(rows),
        "failure_query_ids": sorted({row.get("query_id") for row in failures}),
        "environment": environment_summary(rows),
        "model": model_summary(rows),
    }


def render_markdown(report: Dict[str, Any]) -> str:
    environment = report["environment"]
    lines = [
        "# Qwen WebLLM Aggregated Run Diagnostics",
        "",
        "This aggregate treats segmented run records as experimental",
        "instrumentation data, not paper-ready findings.",
        "",
        "## Coverage",
        "",
        f"- Rows: {report['rows']}",
        f"- Queries: {report['queries']}",
        f"- Schema errors: {len(report['schema_errors'])}",
        f"- Duplicate query-condition pairs: {len(report['duplicate_pairs'])}",
        f"- Missing query-condition pairs: {len(report['missing_pairs'])}",
        f"- Failure query ids: {', '.join(report['failure_query_ids']) or 'none'}",
        "",
        "Inputs:",
        "",
    ]
    for item in report["inputs"]:
        lines.append(
            f"- `{item['path']}`: {item['rows']} rows, {item['queries']} queries, range {item['query_range'][0]}-{item['query_range'][1]}"
        )
    lines.extend([
        "",
        "## Condition Summary",
        "",
        "| Condition | Rows | Qwen rows | Skip rows | Failures | Generation errors | Timeouts | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for condition in CONDITIONS:
        item = report["by_condition"][condition]
        lines.append(
            "| {condition} | {rows} | {qwen} | {skip} | {fail} | {generr} | {timeouts} | {qp50} | {qp95} | {hp50} | {hp95} |".format(
                condition=condition,
                rows=item["rows"],
                qwen=item["qwen_rows"],
                skip=item["deterministic_skip_rows"],
                fail=item["contract_failures"],
                generr=report["by_condition_generation_errors"][condition],
                timeouts=report["by_condition_timeouts"][condition],
                qp50=item["qwen_generation_ms"]["p50"],
                qp95=item["qwen_generation_ms"]["p95"],
                hp50=item["hybrid_system_ms"]["p50"],
                hp95=item["hybrid_system_ms"]["p95"],
            )
        )

    lines.extend([
        "",
        "## Environment",
        "",
        json.dumps(environment, indent=2),
        "",
    ])
    if environment.get("tab_backgrounded_rows"):
        lines.extend([
            "Latency boundary: this aggregate contains backgrounded rows, so",
            "latency values are diagnostic only and should not be used as clean",
            "latency evidence.",
            "",
        ])
    lines.extend([
        "## Failure Groups",
        "",
        json.dumps(report["failure_groups"], indent=2),
        "",
        "## Model",
        "",
        json.dumps(report["model"], indent=2),
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", nargs="+", help="Run JSONL files to aggregate.")
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
    paths = [Path(path) for path in args.runs]
    report = aggregate(paths, schema_path)

    if args.json_out:
        json_path = Path(args.json_out)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if args.md_out:
        md_path = Path(args.md_out)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_markdown(report), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 1 if report["schema_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
