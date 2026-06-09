#!/usr/bin/env python3
"""Compile blueprint rows into draft master/runtime/evaluation fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from evidence_aggregator import aggregate_evidence_state  # noqa: E402
from split_fixture_views import build_evaluation_view, build_runtime_view  # noqa: E402
from validate_fixture import load_schema, validate_fixture_line  # noqa: E402


PLACEHOLDER = "[not provided in source]"
BASE_CHECKLIST_FIELDS = [
    "source",
    "rights_label",
    "reuse_permission",
    "public_domain_status",
    "image_state_label",
    "research_context",
    "chronology_proof",
    "comparison_corpus",
    "date_text",
    "title",
]
RECORD_REQUIRED_FIELDS = {"source", "rights_label"}
RECORD_FIELD_NAMES = {
    "source",
    "rights_label",
    "reuse_permission",
    "public_domain_status",
    "image_state_label",
    "source_citation",
    "title",
    "date_text",
    "chronology_proof",
}


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def write_jsonl(rows: Iterable[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")


def write_json(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def absent_field_for(decisive_fields: List[str]) -> str:
    for field in reversed(decisive_fields):
        if field not in RECORD_REQUIRED_FIELDS:
            return field
    return decisive_fields[-1]


def field_checklist_for(row: Dict[str, Any]) -> Dict[str, str]:
    decisive = list(row["decisive_fields"])
    target = row["evidence_state"]
    checklist = {field: "not_applicable" for field in BASE_CHECKLIST_FIELDS}

    if target == "sufficient":
        for field in decisive:
            checklist[field] = "present_and_consistent"
    elif target == "partial":
        missing_field = absent_field_for(decisive)
        for field in decisive:
            checklist[field] = (
                "absent" if field == missing_field else "present_and_consistent"
            )
    elif target == "missing":
        for field in decisive:
            checklist[field] = "absent"
    elif target == "contradictory":
        conflict_field = decisive[0]
        for field in decisive:
            checklist[field] = (
                "present_but_conflicting"
                if field == conflict_field
                else "present_and_consistent"
            )
    elif target == "not_applicable":
        for field in decisive:
            checklist[field] = "not_applicable"
    else:
        raise ValueError(f"unknown evidence_state: {target}")

    return checklist


def record_count_for(row: Dict[str, Any], checklist: Dict[str, str]) -> int:
    if all(checklist.get(field) == "absent" for field in row["decisive_fields"]):
        return 0
    return max(1, int(row.get("record_count_target", 1)))


def record_for(row: Dict[str, Any], checklist: Dict[str, str], index: int) -> Dict[str, Any]:
    deterministic = row["deterministic_fields"]
    record_id = f"syn_{row['query_id']}_{index:02d}"
    record: Dict[str, Any] = {
        "record_id": record_id,
        "title": f"Synthetic {row['stratum']} record {row['query_id']}",
        "date_text": "1936",
        "source": deterministic["source"],
        "source_citation": deterministic["source_citation"],
        "source_name": "Synthetic Public Health Archive",
        "source_domain": "example.org",
        "rights_label": deterministic["rights_label"],
        "rights_state": "fixture_metadata_only",
        "reuse_permission": deterministic["reuse_permission"],
        "public_domain_status": deterministic["public_domain_status"],
        "record_origin": row["record_origin"],
        "image_state_code": "IMG-META",
        "image_state_label": deterministic["image_state_label"],
        "chronology_proof": checklist.get("chronology_proof") == "present_and_consistent",
        "source_audit_status": row["source_audit_status"],
        "source_audit_notes": row.get("audit_caveat", ""),
    }

    for field, state in checklist.items():
        if state == "absent" and field in record and field not in RECORD_REQUIRED_FIELDS:
            del record[field]

    if row.get("conflict_expected") and index == 2:
        conflict_field = row["decisive_fields"][0]
        if conflict_field in RECORD_FIELD_NAMES:
            record[conflict_field] = f"{record.get(conflict_field, PLACEHOLDER)} [conflicting]"

    return record


def expected_behavior_for(row: Dict[str, Any], deterministic_required: List[str]) -> Dict[str, Any]:
    refusal_expected = bool(row["refusal_expected"])
    compound_parts = [
        {"part": "deterministic_fields", "mode": "deterministic"},
        {"part": "research_guidance", "mode": "generative"},
    ] if row["primary_lane"] == "compound" else []

    c1_modes = ["refusal", "qualified_answer"] if refusal_expected else ["generative", "qualified_answer"]
    c2_modes = ["refusal", "qualified_answer", "generative"] if refusal_expected else [
        "exact_render",
        "generative",
        "qualified_answer",
    ]
    c3_modes = ["refusal"] if refusal_expected else [
        "exact_render",
        "generative",
        "qualified_answer",
    ]

    return {
        "condition_1_all_generation": {
            "should_refuse": refusal_expected,
            "deterministic_fields_required": [],
            "allowed_output_modes": c1_modes,
            "expect_no_evidence": row["evidence_state"] == "missing",
            "min_helpfulness_score": 3,
            "contract_compliance_required": True,
        },
        "condition_2_hybrid_no_refusal": {
            "should_refuse": False,
            "deterministic_fields_required": deterministic_required,
            "allowed_output_modes": c2_modes,
            "expect_no_evidence": row["evidence_state"] == "missing",
            "min_helpfulness_score": 3,
            "contract_compliance_required": True,
            **({"compound_parts": compound_parts} if compound_parts else {}),
        },
        "condition_3_full_hybrid": {
            "should_refuse": refusal_expected,
            "deterministic_fields_required": [] if refusal_expected else deterministic_required,
            "allowed_output_modes": c3_modes,
            "expect_no_evidence": row["evidence_state"] == "missing",
            "min_helpfulness_score": 4 if row["primary_lane"] == "compound" else 3,
            "contract_compliance_required": True,
            **({"compound_parts": compound_parts} if compound_parts else {}),
        },
    }


def compile_row(row: Dict[str, Any]) -> Dict[str, Any]:
    checklist = field_checklist_for(row)
    records = [
        record_for(row, checklist, index)
        for index in range(1, record_count_for(row, checklist) + 1)
    ]
    aggregated = aggregate_evidence_state(
        checklist,
        row["intent_label"],
        row["decisive_fields"],
    )
    if aggregated != row["evidence_state"]:
        raise ValueError(
            f"{row['query_id']}: compiled evidence_state {aggregated} "
            f"does not match blueprint {row['evidence_state']}"
        )

    deterministic_required = [
        field
        for field in ["source", "rights_label", "reuse_permission", "public_domain_status"]
        if field in checklist and checklist[field] != "not_applicable"
    ]
    query: Dict[str, Any] = {
        "text": row["query_text"],
        "intent_label": row["intent_label"],
        "primary_lane": row["primary_lane"],
        "mixed_intent": row["mixed_intent"],
        "routing_ambiguity_notes": row.get("authoring_notes", ""),
    }
    if row.get("secondary_lanes"):
        query["secondary_lanes"] = row["secondary_lanes"]

    return {
        "fixture_version": "1.0",
        "query_id": row["query_id"],
        "applicable_conditions": [1, 2, 3],
        "fixture_meta": {
            "blueprint_version": row["blueprint_version"],
            "stratum": row["stratum"],
            "role": row["role"],
            "target_evidence_state": row["evidence_state"],
            "refusal_expected": row["refusal_expected"],
            "conflict_expected": row["conflict_expected"],
            "audit_caveat": row.get("audit_caveat", ""),
        },
        "query": query,
        "evidence_packet": {
            "records": records,
            "field_checklist": checklist,
            "decisive_fields": row["decisive_fields"],
            "aggregated_evidence_state": aggregated,
            "retrieved_snippets": [
                {
                    "snippet_id": f"snip_{row['query_id']}_001",
                    "record_id": records[0]["record_id"] if records else "no_record",
                    "text": f"Synthetic snippet for {row['stratum']} with {aggregated} evidence.",
                    "rank": 1,
                }
            ] if records else [],
        },
        "expected_behavior": expected_behavior_for(row, deterministic_required),
    }


def validate_compiled(rows: List[Dict[str, Any]]) -> None:
    schema = load_schema()
    errors: List[str] = []
    for row in rows:
        errors.extend(
            f"{row['query_id']}: {error}"
            for error in validate_fixture_line(row, schema)
        )
    if errors:
        raise ValueError("Compiled fixture validation failed:\n" + "\n".join(errors))


def select_warmup_rows(rows: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    seen_strata = set()
    for row in rows:
        meta = row.get("fixture_meta", {})
        if meta.get("role") != "dev":
            continue
        stratum = meta.get("stratum")
        if stratum in seen_strata:
            continue
        selected.append(row)
        seen_strata.add(stratum)
        if len(selected) == count:
            break
    if len(selected) < count:
        raise ValueError(f"Only found {len(selected)} warmup candidates; expected {count}")
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blueprint", default="fixtures/drafts/fixture_expansion_blueprint_v0.jsonl")
    parser.add_argument("--output", default="fixtures/drafts/compiled_experiment_fixture_v0.jsonl")
    parser.add_argument("--runtime-output", default="fixtures/drafts/runtime_view_v0.jsonl")
    parser.add_argument("--evaluation-output", default="fixtures/drafts/evaluation_view_v0.jsonl")
    parser.add_argument("--warmup-json", default="fixtures/drafts/warmup_set_v0.json")
    parser.add_argument("--warmup-runtime", default="fixtures/drafts/warmup_queries_v0.jsonl")
    parser.add_argument("--warmup-count", type=int, default=5)
    args = parser.parse_args()

    blueprint_rows = load_jsonl(REPO_ROOT / args.blueprint)
    compiled_rows = [compile_row(row) for row in blueprint_rows]
    validate_compiled(compiled_rows)

    write_jsonl(compiled_rows, REPO_ROOT / args.output)
    write_jsonl([build_runtime_view(row) for row in compiled_rows], REPO_ROOT / args.runtime_output)
    write_jsonl([build_evaluation_view(row) for row in compiled_rows], REPO_ROOT / args.evaluation_output)

    warmup_rows = select_warmup_rows(compiled_rows, args.warmup_count)
    write_json(warmup_rows, REPO_ROOT / args.warmup_json)
    write_jsonl([build_runtime_view(row) for row in warmup_rows], REPO_ROOT / args.warmup_runtime)

    print(f"Compiled {len(compiled_rows)} fixture rows to {args.output}")
    print(f"Wrote {len(warmup_rows)} warmup rows to {args.warmup_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
