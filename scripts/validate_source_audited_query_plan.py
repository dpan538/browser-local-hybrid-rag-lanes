#!/usr/bin/env python3
"""Validate source-audited query plan JSONL files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

import jsonschema


SCHEMA_PATH = Path("schemas/source_audited_query_plan_schema.json")


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


def validate_schema(rows: Iterable[Dict[str, Any]], schema: Dict[str, Any]) -> List[str]:
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    errors: List[str] = []
    for index, row in enumerate(rows, start=1):
        try:
            validator.validate(row)
        except jsonschema.ValidationError as exc:
            dotted_path = ".".join(str(part) for part in exc.path)
            errors.append(f"line {index}: {exc.message} (path: {dotted_path})")
    return errors


def validate_semantics(rows: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    seen: Set[str] = set()
    for row in rows:
        query_id = row["query_id"]
        if query_id in seen:
            errors.append(f"{query_id}: duplicate query_id")
        seen.add(query_id)

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
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query_plan", help="Source-audited query plan JSONL.")
    parser.add_argument("--schema", default=str(SCHEMA_PATH))
    parser.add_argument("--min-rows", type=int, default=0)
    args = parser.parse_args()

    path = Path(args.query_plan)
    if not path.exists():
        print(f"Source-audited query plan not found: {path}")
        return 1

    rows = load_jsonl(path)
    errors = []
    errors.extend(validate_schema(rows, load_json(Path(args.schema))))
    if not errors:
        errors.extend(validate_semantics(rows))
    if len(rows) < args.min_rows:
        errors.append(f"row count {len(rows)} is below required minimum {args.min_rows}")

    if errors:
        print("Source-audited query plan validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Source-audited query plan validation passed.")
    print(f"Rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
