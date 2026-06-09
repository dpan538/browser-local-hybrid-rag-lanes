#!/usr/bin/env python3
"""Validate a hybrid lane experiment fixture JSONL file.

Usage:
    python scripts/validate_fixture.py fixtures/experiment_fixture.jsonl

Requires:
    pip install -r requirements.txt
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import jsonschema
    from jsonschema import validate as jsonschema_validate
except ImportError:
    print("Error: jsonschema is required. Run: pip install -r requirements.txt")
    sys.exit(1)

from evidence_aggregator import aggregate_evidence_state


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SCHEMA_PATH = REPO_ROOT / "schemas" / "experiment_fixture_schema.json"


def load_schema() -> Dict[str, Any]:
    return json.loads(FIXTURE_SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_fixture_line(
    line_obj: Dict[str, Any],
    fixture_schema: Dict[str, Any],
) -> List[str]:
    """Return validation errors for one fixture row."""
    errors: List[str] = []

    try:
        jsonschema_validate(instance=line_obj, schema=fixture_schema)
    except jsonschema.ValidationError as exc:
        path = ".".join(str(part) for part in exc.path)
        errors.append(f"Schema violation: {exc.message} (path: {path})")
        return errors

    intent = line_obj["query"]["intent_label"]
    checklist = line_obj["evidence_packet"]["field_checklist"]
    declared_state = line_obj["evidence_packet"]["aggregated_evidence_state"]
    computed_state = aggregate_evidence_state(checklist, intent)
    if declared_state != computed_state:
        errors.append(
            "Evidence state mismatch: "
            f"declared '{declared_state}', computed '{computed_state}' "
            f"from field_checklist and intent '{intent}'"
        )

    query = line_obj["query"]
    if query.get("mixed_intent", False):
        if not query.get("secondary_lanes"):
            errors.append("mixed_intent=true but secondary_lanes is missing or empty")
        if query["primary_lane"] in query.get("secondary_lanes", []):
            errors.append(
                f"Warning: primary_lane '{query['primary_lane']}' appears in "
                "secondary_lanes; review routing labels"
            )

    if query["primary_lane"] == "deterministic_refusal":
        if query["intent_label"] != "refusal_required":
            errors.append(
                "deterministic_refusal lane used with intent "
                f"'{query['intent_label']}', expected 'refusal_required'"
            )

    if query["primary_lane"] == "compound":
        cond3 = line_obj["expected_behavior"].get("condition_3_full_hybrid")
        if cond3 is None or not cond3.get("compound_parts"):
            errors.append(
                "primary_lane='compound' but "
                "condition_3_full_hybrid.compound_parts is missing or empty"
            )

    for condition_name, expectation in line_obj["expected_behavior"].items():
        for field in expectation.get("deterministic_fields_required", []):
            if field not in checklist:
                errors.append(
                    f"Field '{field}' required in "
                    f"{condition_name}.deterministic_fields_required "
                    "but not present in field_checklist"
                )

    return errors


def validate_fixture_file(file_path: Path) -> bool:
    if not file_path.exists():
        print(f"Error: file does not exist: {file_path}")
        return False

    fixture_schema = load_schema()
    total_errors = 0
    line_count = 0

    with file_path.open("r", encoding="utf-8") as handle:
        for line_count, raw_line in enumerate(handle, start=1):
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                data = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                print(f"Line {line_count}: JSON parse error: {exc}")
                total_errors += 1
                continue

            errors = validate_fixture_line(data, fixture_schema)
            if errors:
                print(f"\nLine {line_count} (query_id: {data.get('query_id', 'unknown')}):")
                for error in errors:
                    print(f"  - {error}")
                total_errors += len(errors)
            else:
                print(f"ok line {line_count} query_id={data.get('query_id', 'unknown')}")

    if total_errors == 0:
        print(f"\nValidation complete: {line_count} lines, no errors.")
        return True

    print(f"\nValidation complete: {total_errors} errors.")
    return False


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_fixture.py <fixture_file.jsonl>")
        return 1
    return 0 if validate_fixture_file(Path(sys.argv[1])) else 1


if __name__ == "__main__":
    raise SystemExit(main())
