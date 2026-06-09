#!/usr/bin/env python3
"""Automatic contract checks for hybrid lane run records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


DETERMINISTIC_FIELDS = [
    "source",
    "rights_label",
    "reuse_permission",
    "public_domain_status",
]

PLACEHOLDER = "[not provided in source]"


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def runtime_index(path: Path) -> Dict[str, Dict[str, Any]]:
    return {row["query_id"]: row for row in load_jsonl(path)}


def first_record(runtime_query: Dict[str, Any]) -> Dict[str, Any]:
    records = runtime_query.get("evidence_packet", {}).get("records") or [{}]
    return records[0]


def field_state(runtime_query: Dict[str, Any], field: str) -> str:
    return runtime_query.get("evidence_packet", {}).get("field_checklist", {}).get(
        field,
        "not_applicable",
    )


def answer_text(answer: Dict[str, Any]) -> str:
    return json.dumps(answer, ensure_ascii=False).lower()


def load_blueprint_index(path: Path) -> Dict[str, Dict[str, Any]]:
    if not path.exists():
        return {}
    return {row["query_id"]: row for row in load_jsonl(path)}


def refusal_value(answer: Dict[str, Any]) -> str:
    return str(answer.get("refusal", "") or "").strip().lower()


def answer_refused(answer: Dict[str, Any]) -> bool:
    value = refusal_value(answer)
    return bool(value and value != "none")


def check_contract(
    record: Dict[str, Any],
    runtime_query: Dict[str, Any],
    blueprint_row: Dict[str, Any] | None = None,
) -> Dict[str, str]:
    answer = record.get("answer", {}) or {}
    condition = record.get("condition", "")
    source_record = first_record(runtime_query)
    results: Dict[str, str] = {}

    for field in DETERMINISTIC_FIELDS:
        value = str(answer.get(field, "") or "")
        expected = str(source_record.get(field, PLACEHOLDER))
        state = field_state(runtime_query, field)

        if state == "absent":
            results[f"{field}_rendered"] = "pass" if value == PLACEHOLDER else "warning"
        else:
            results[f"{field}_rendered"] = "pass" if value.strip() else "fail"

        if condition in {"hybrid_without_refusal", "full_hybrid"}:
            results[f"{field}_mutation"] = "pass" if value == expected else "fail"
        else:
            results[f"{field}_mutation"] = "n/a"

    source_value = str(answer.get("source", "") or "")
    expected_source = str(source_record.get("source", "") or "")
    results["source_pointer_preserved"] = (
        "pass" if expected_source and expected_source in source_value else "warning"
    )

    rights_mutated = results.get("rights_label_mutation") == "fail"
    status_mutated = results.get("public_domain_status_mutation") == "fail"
    results["rights_label_upgrade"] = "warning" if rights_mutated or status_mutated else "pass"

    checklist = runtime_query.get("evidence_packet", {}).get("field_checklist", {})
    has_conflict = any(value == "present_but_conflicting" for value in checklist.values())
    if has_conflict:
        text = answer_text(answer)
        conflict_terms = ["conflict", "contradict", "inconsistent", "冲突", "矛盾", "不一致"]
        results["conflict_surfaced"] = (
            "pass" if any(term in text for term in conflict_terms) else "fail"
        )
    else:
        results["conflict_surfaced"] = "n/a"

    if blueprint_row:
        if blueprint_row.get("conflict_expected") and results["conflict_surfaced"] == "n/a":
            results["conflict_surfaced"] = "fail"

        expected_refusal = bool(blueprint_row.get("refusal_expected"))
        did_refuse = answer_refused(answer)
        if expected_refusal:
            results["refusal_expected_alignment"] = "pass" if did_refuse else "fail"
        else:
            results["refusal_expected_alignment"] = "warning" if did_refuse else "pass"

    for field in DETERMINISTIC_FIELDS:
        if field_state(runtime_query, field) == "absent":
            results[f"{field}_placeholder_used"] = (
                "pass" if str(answer.get(field, "")) == PLACEHOLDER else "warning"
            )

    return results


def enrich_records(
    records_path: Path,
    runtime_path: Path,
    output_path: Path,
    blueprint_path: Path | None = None,
) -> None:
    runtimes = runtime_index(runtime_path)
    blueprints = load_blueprint_index(blueprint_path) if blueprint_path else {}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with records_path.open("r", encoding="utf-8") as source, output_path.open(
        "w",
        encoding="utf-8",
    ) as target:
        for raw_line in source:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            record = json.loads(raw_line)
            runtime_query = runtimes[record["query_id"]]
            record["auto_contract"] = check_contract(
                record,
                runtime_query,
                blueprints.get(record["query_id"]),
            )
            target.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
            target.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", default="runs/collected_records.jsonl")
    parser.add_argument("--runtime", default="fixtures/runtime_view/experiment_fixture.runtime.jsonl")
    parser.add_argument("--output", default="runs/auto_evaluated_records.jsonl")
    parser.add_argument(
        "--blueprint",
        default="",
        help="Optional blueprint file with refusal/conflict expectations.",
    )
    args = parser.parse_args()
    blueprint_path = Path(args.blueprint) if args.blueprint else None
    enrich_records(
        Path(args.records),
        Path(args.runtime),
        Path(args.output),
        blueprint_path if blueprint_path and blueprint_path.exists() else None,
    )
    print(f"Wrote auto-evaluated records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
