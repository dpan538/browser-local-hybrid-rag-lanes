#!/usr/bin/env python3
"""Compile source-audited manifests and query plans into fixture views."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

import jsonschema

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from evidence_aggregator import aggregate_evidence_state  # noqa: E402
from split_fixture_views import build_evaluation_view, build_runtime_view  # noqa: E402
from validate_fixture import load_schema, validate_fixture_line  # noqa: E402
from validate_source_audit_manifest import (  # noqa: E402
    load_source_family_ids,
    validate_consistency as validate_manifest_consistency,
)


PLACEHOLDER = "[not provided in source]"
FIELD_NAMES = [
    "title",
    "date_text",
    "source",
    "source_citation",
    "rights_label",
    "reuse_permission",
    "public_domain_status",
    "image_state_label",
]
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
    "source_citation",
]
RECORD_REQUIRED_FIELDS = {"source", "rights_label"}
STATUS_TO_FIXTURE_AUDIT = {
    "audited": "pass",
    "partial": "uncertain",
    "failed": "fail",
}
FIELD_STATE_TO_CHECKLIST = {
    "verified": "present_and_consistent",
    "missing": "absent",
    "conflicting": "present_but_conflicting",
    "not_applicable": "not_applicable",
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def validate_jsonl_schema(rows: Iterable[Dict[str, Any]], schema_path: Path) -> None:
    schema = load_json(schema_path)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema, format_checker=jsonschema.FormatChecker())
    errors: List[str] = []
    for index, row in enumerate(rows, start=1):
        try:
            validator.validate(row)
        except jsonschema.ValidationError as exc:
            dotted_path = ".".join(str(part) for part in exc.path)
            errors.append(f"line {index}: {exc.message} (path: {dotted_path})")
    if errors:
        raise ValueError("\n".join(errors))


def validate_unique_query_plan_ids(rows: List[Dict[str, Any]]) -> None:
    seen: set[str] = set()
    duplicates: List[str] = []
    for row in rows:
        query_id = row["query_id"]
        if query_id in seen:
            duplicates.append(query_id)
        seen.add(query_id)
    if duplicates:
        raise ValueError("duplicate query_id in query plan: " + ", ".join(sorted(duplicates)))


def validate_query_plan_semantics(rows: List[Dict[str, Any]]) -> None:
    errors: List[str] = []
    for row in rows:
        query_id = row["query_id"]
        lane_intent = set(row["lane_intent"])
        primary_lane = row["primary_lane"]
        refusal_policy = row["refusal_policy"]
        if primary_lane == "deterministic_refusal" and "refusal" not in lane_intent:
            errors.append(f"{query_id}: deterministic_refusal requires lane_intent 'refusal'")
        if primary_lane == "deterministic_exact" and not lane_intent.intersection({"source", "rights", "provenance"}):
            errors.append(
                f"{query_id}: deterministic_exact requires source/rights/provenance lane_intent"
            )
        if "refusal" in lane_intent and refusal_policy == "never":
            errors.append(f"{query_id}: lane_intent includes refusal but refusal_policy is never")
        if row.get("warmup") and row.get("role") != "warmup":
            errors.append(f"{query_id}: warmup=true requires role=warmup")
        if row.get("mixed_intent") and not row.get("secondary_lanes"):
            errors.append(f"{query_id}: mixed_intent=true requires secondary_lanes")
        if primary_lane == "compound" and "research_guidance" not in lane_intent:
            errors.append(f"{query_id}: compound lane requires research_guidance lane_intent")
    if errors:
        raise ValueError("Query plan semantic validation failed:\n" + "\n".join(errors))


def load_refusal_matrix(path: Path) -> Dict[str, Dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        return {row["evidence_state"]: row for row in csv.DictReader(handle)}


def group_manifest(rows: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    by_manifest_id: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        grouped[row["query_id"]].append(row)
        by_manifest_id[row["manifest_id"]] = row
    grouped["__by_manifest_id__"] = list(by_manifest_id.values())
    return grouped


def manifest_rows_for_plan(
    plan: Dict[str, Any],
    manifest_by_query: Dict[str, List[Dict[str, Any]]],
    manifest_by_id: Dict[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    if plan.get("manifest_ids"):
        missing = [item for item in plan["manifest_ids"] if item not in manifest_by_id]
        if missing:
            raise ValueError(f"{plan['query_id']}: manifest_ids not found: {missing}")
        return [manifest_by_id[item] for item in plan["manifest_ids"]]
    return manifest_by_query.get(plan["query_id"], [])


def aggregate_field_state(records: List[Dict[str, Any]], field_name: str) -> str:
    states = [row["fields"][field_name]["state"] for row in records if field_name in row["fields"]]
    if not states:
        return "absent"
    if "conflicting" in states:
        return "present_but_conflicting"
    if "verified" in states:
        return "present_and_consistent"
    if all(state == "not_applicable" for state in states):
        return "not_applicable"
    return "absent"


def field_checklist_for(plan: Dict[str, Any], manifest_rows: List[Dict[str, Any]]) -> Dict[str, str]:
    checklist = {field: "not_applicable" for field in BASE_CHECKLIST_FIELDS}
    for field in plan["decisive_fields"]:
        checklist[field] = aggregate_field_state(manifest_rows, field)
    return checklist


def value_for_record(manifest_row: Dict[str, Any], field_name: str) -> str:
    field = manifest_row["fields"][field_name]
    state = field["state"]
    if state in {"verified", "conflicting"}:
        return field["value"]
    return PLACEHOLDER if field_name in RECORD_REQUIRED_FIELDS else ""


def maybe_add(record: Dict[str, Any], key: str, value: str) -> None:
    if value != "":
        record[key] = value


def record_for(manifest_row: Dict[str, Any]) -> Dict[str, Any]:
    fields = manifest_row["fields"]
    record: Dict[str, Any] = {
        "record_id": manifest_row["record_id"],
        "source": value_for_record(manifest_row, "source"),
        "source_name": manifest_row["source_name"],
        "source_domain": manifest_row["source_domain"],
        "rights_label": value_for_record(manifest_row, "rights_label"),
        "record_origin": manifest_row["record_origin"],
        "rights_state": "metadata_rights_statement",
        "image_state_code": fields["image_state_label"]["value"] or "metadata_only_unknown",
        "source_audit_status": STATUS_TO_FIXTURE_AUDIT[manifest_row["source_audit_status"]],
        "source_audit_notes": manifest_row.get("auditor_notes", ""),
        "chronology_proof": fields["date_text"]["state"] == "verified",
    }
    for key in [
        "title",
        "date_text",
        "source_citation",
        "reuse_permission",
        "public_domain_status",
        "image_state_label",
    ]:
        maybe_add(record, key, value_for_record(manifest_row, key))
    return record


def deterministic_required_fields(checklist: Dict[str, str]) -> List[str]:
    return [
        field
        for field in ["source", "rights_label", "reuse_permission", "public_domain_status"]
        if checklist.get(field) != "not_applicable"
    ]


def refusal_expected_for(
    plan: Dict[str, Any],
    evidence_state: str,
    refusal_matrix: Dict[str, Dict[str, str]],
) -> bool:
    policy = plan["refusal_policy"]
    if policy == "always":
        return True
    if policy == "never":
        return False
    row = refusal_matrix.get(evidence_state, {})
    return row.get("refusal_label_if_system_refuses") == "correct_refusal"


def expected_behavior_for(
    plan: Dict[str, Any],
    deterministic_required: List[str],
    refusal_expected: bool,
    evidence_state: str,
) -> Dict[str, Any]:
    compound_parts = [
        {"part": "deterministic_fields", "mode": "deterministic"},
        {"part": "research_guidance", "mode": "generative"},
    ] if plan["primary_lane"] == "compound" else []

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
            "expect_no_evidence": evidence_state == "missing",
            "min_helpfulness_score": 3,
            "contract_compliance_required": True,
        },
        "condition_2_hybrid_no_refusal": {
            "should_refuse": False,
            "deterministic_fields_required": deterministic_required,
            "allowed_output_modes": c2_modes,
            "expect_no_evidence": evidence_state == "missing",
            "min_helpfulness_score": 3,
            "contract_compliance_required": True,
            **({"compound_parts": compound_parts} if compound_parts else {}),
        },
        "condition_3_full_hybrid": {
            "should_refuse": refusal_expected,
            "deterministic_fields_required": [] if refusal_expected else deterministic_required,
            "allowed_output_modes": c3_modes,
            "expect_no_evidence": evidence_state == "missing",
            "min_helpfulness_score": 4 if plan["primary_lane"] == "compound" else 3,
            "contract_compliance_required": True,
            **({"compound_parts": compound_parts} if compound_parts else {}),
        },
    }


def compile_row(
    plan: Dict[str, Any],
    manifest_rows: List[Dict[str, Any]],
    refusal_matrix: Dict[str, Dict[str, str]],
) -> Dict[str, Any]:
    if not manifest_rows and not plan.get("allow_no_records", False):
        raise ValueError(f"{plan['query_id']}: no manifest rows and allow_no_records=false")

    checklist = field_checklist_for(plan, manifest_rows)
    evidence_state = aggregate_evidence_state(
        checklist,
        plan["intent_label"],
        plan["decisive_fields"],
    )
    if plan.get("evidence_state_override"):
        evidence_state = plan["evidence_state_override"]
    refusal_expected = refusal_expected_for(plan, evidence_state, refusal_matrix)
    records = [record_for(row) for row in manifest_rows]
    deterministic_required = deterministic_required_fields(checklist)

    query: Dict[str, Any] = {
        "text": plan["question_text"],
        "intent_label": plan["intent_label"],
        "primary_lane": plan["primary_lane"],
        "mixed_intent": plan["mixed_intent"],
        "routing_ambiguity_notes": plan.get("authoring_notes", ""),
    }
    if plan.get("secondary_lanes"):
        query["secondary_lanes"] = plan["secondary_lanes"]

    return {
        "fixture_version": "1.0",
        "query_id": plan["query_id"],
        "applicable_conditions": [1, 2, 3],
        "fixture_meta": {
            "blueprint_version": plan["plan_version"],
            "stratum": plan["stratum"],
            "role": "warmup" if plan.get("warmup") else plan["role"],
            "target_evidence_state": evidence_state,
            "refusal_expected": refusal_expected,
            "conflict_expected": evidence_state == "contradictory",
            "audit_caveat": "metadata_only_no_image_download",
        },
        "query": query,
        "evidence_packet": {
            "records": records,
            "field_checklist": checklist,
            "decisive_fields": plan["decisive_fields"],
            "aggregated_evidence_state": evidence_state,
            "retrieved_snippets": [
                {
                    "snippet_id": f"snip_{plan['query_id']}_{index:03d}",
                    "record_id": record["record_id"],
                    "text": f"Metadata-only audited record from {record.get('source_name', 'source')}.",
                    "rank": index,
                }
                for index, record in enumerate(records, start=1)
            ],
        },
        "expected_behavior": expected_behavior_for(
            plan,
            deterministic_required,
            refusal_expected,
            evidence_state,
        ),
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
    warmups = [row for row in rows if row.get("fixture_meta", {}).get("role") == "warmup"]
    if len(warmups) >= count:
        return warmups[:count]
    fallback = [row for row in rows if row.get("fixture_meta", {}).get("role") == "eval"]
    selected = warmups + fallback[: max(0, count - len(warmups))]
    if len(selected) < count:
        raise ValueError(f"Only found {len(selected)} warmup candidates; expected {count}")
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="fixtures/source_audited_50/source_audit_manifest_v0.jsonl")
    parser.add_argument("--query-plan", default="fixtures/source_audited_50/query_plan_v0.jsonl")
    parser.add_argument("--manifest-schema", default="schemas/source_audit_manifest_schema.json")
    parser.add_argument("--query-plan-schema", default="schemas/source_audited_query_plan_schema.json")
    parser.add_argument("--source-families", default="config/source_families.yaml")
    parser.add_argument("--refusal-matrix", default="config/refusal_decision_matrix.csv")
    parser.add_argument("--output", default="fixtures/source_audited_50/experiment_fixture.jsonl")
    parser.add_argument("--runtime-output", default="fixtures/source_audited_50/runtime_view.jsonl")
    parser.add_argument("--evaluation-output", default="fixtures/source_audited_50/evaluation_view.jsonl")
    parser.add_argument("--warmup-output", default="fixtures/source_audited_50/warmup_queries.jsonl")
    parser.add_argument("--warmup-count", type=int, default=5)
    args = parser.parse_args()

    manifest_rows = load_jsonl(REPO_ROOT / args.manifest)
    query_plan_rows = load_jsonl(REPO_ROOT / args.query_plan)
    validate_jsonl_schema(manifest_rows, REPO_ROOT / args.manifest_schema)
    validate_jsonl_schema(query_plan_rows, REPO_ROOT / args.query_plan_schema)
    validate_unique_query_plan_ids(query_plan_rows)
    validate_query_plan_semantics(query_plan_rows)
    source_family_ids = load_source_family_ids(REPO_ROOT / args.source_families)
    manifest_errors = validate_manifest_consistency(
        manifest_rows,
        source_family_ids,
        require_pass=False,
        allow_partial=True,
    )
    if manifest_errors:
        raise ValueError(
            "Source-audit manifest consistency failed:\n" + "\n".join(manifest_errors)
        )
    failed_rows = [
        f"{row['manifest_id']}:{row['record_id']}"
        for row in manifest_rows
        if row.get("source_audit_status") == "failed"
    ]
    if failed_rows:
        raise ValueError(
            "Failed source-audit rows cannot be compiled: " + ", ".join(failed_rows[:20])
        )

    manifest_by_query: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    manifest_by_id: Dict[str, Dict[str, Any]] = {}
    for row in manifest_rows:
        manifest_by_query[row["query_id"]].append(row)
        manifest_by_id[row["manifest_id"]] = row

    refusal_matrix = load_refusal_matrix(REPO_ROOT / args.refusal_matrix)
    compiled_rows = [
        compile_row(
            plan,
            manifest_rows_for_plan(plan, manifest_by_query, manifest_by_id),
            refusal_matrix,
        )
        for plan in query_plan_rows
    ]
    validate_compiled(compiled_rows)

    write_jsonl(compiled_rows, REPO_ROOT / args.output)
    write_jsonl([build_runtime_view(row) for row in compiled_rows], REPO_ROOT / args.runtime_output)
    write_jsonl([build_evaluation_view(row) for row in compiled_rows], REPO_ROOT / args.evaluation_output)
    warmup_rows = select_warmup_rows(compiled_rows, args.warmup_count)
    write_jsonl([build_runtime_view(row) for row in warmup_rows], REPO_ROOT / args.warmup_output)
    print(f"Compiled {len(compiled_rows)} source-audited fixture rows.")
    print(f"Wrote {len(warmup_rows)} warmup runtime rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
