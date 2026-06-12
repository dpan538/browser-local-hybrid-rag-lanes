#!/usr/bin/env python3
"""Validate Paper v1 source-audit manifest JSONL files."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema is required. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Run: pip install -r requirements.txt")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "source_audit_manifest_schema.json"
SOURCE_FAMILIES_PATH = REPO_ROOT / "config" / "source_families.yaml"

COMPLETE_STATUSES = {"audited"}
INCOMPLETE_FIELD_STATES = {"missing", "conflicting"}
ALLOWED_ORIGINS = {"source_audited", "derived_from_public_source"}


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


def load_source_family_ids(path: Path) -> Set[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {
        str(item["id"])
        for item in data.get("source_families", [])
        if "id" in item
    }


def validate_schema(rows: Iterable[Dict[str, Any]], schema: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema, format_checker=jsonschema.FormatChecker())

    for index, row in enumerate(rows, start=1):
        try:
            validator.validate(row)
        except jsonschema.ValidationError as exc:
            dotted_path = ".".join(str(part) for part in exc.path)
            errors.append(f"line {index}: {exc.message} (path: {dotted_path})")
    return errors


def validate_consistency(
    rows: List[Dict[str, Any]],
    source_family_ids: Set[str],
    require_pass: bool,
) -> List[str]:
    errors: List[str] = []
    seen_manifest_ids: Set[str] = set()
    seen_record_ids: Set[str] = set()

    for index, row in enumerate(rows, start=1):
        manifest_id = row.get("manifest_id", f"line_{index}")
        record_id = row.get("record_id", "")

        if manifest_id in seen_manifest_ids:
            errors.append(f"{manifest_id}: duplicate manifest_id")
        seen_manifest_ids.add(manifest_id)

        if record_id in seen_record_ids:
            errors.append(f"{manifest_id}: duplicate record_id '{record_id}'")
        seen_record_ids.add(record_id)

        origin = row.get("record_origin")
        if origin not in ALLOWED_ORIGINS:
            errors.append(f"{manifest_id}: invalid record_origin '{origin}'")

        family_id = row.get("source_family_id")
        if source_family_ids and family_id not in source_family_ids:
            errors.append(f"{manifest_id}: source_family_id '{family_id}' not in config")

        status = row.get("source_audit_status")
        field_states = {
            field_name: field.get("state")
            for field_name, field in row.get("fields", {}).items()
        }
        incomplete_fields = [
            field_name
            for field_name, state in field_states.items()
            if state in INCOMPLETE_FIELD_STATES
        ]
        if status in COMPLETE_STATUSES and incomplete_fields:
            errors.append(
                f"{manifest_id}: status '{status}' cannot contain incomplete fields: "
                + ", ".join(sorted(incomplete_fields))
            )

        for field_name, field in row.get("fields", {}).items():
            state = field.get("state")
            value = str(field.get("value", ""))
            note = str(field.get("evidence_note", ""))
            if state == "verified" and not value.strip():
                errors.append(f"{manifest_id}: field '{field_name}' is verified but empty")
            if state == "missing" and value.strip():
                errors.append(f"{manifest_id}: field '{field_name}' is missing but has a value")
            if state in {"verified", "conflicting"} and not note.strip():
                errors.append(
                    f"{manifest_id}: field '{field_name}' is {state} but has no evidence_note"
                )

        if require_pass and status != "audited":
            errors.append(
                f"{manifest_id}: require-pass set but source_audit_status is '{status}'"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="Source-audit manifest JSONL file.")
    parser.add_argument("--schema", default=str(SCHEMA_PATH))
    parser.add_argument("--source-families", default=str(SOURCE_FAMILIES_PATH))
    parser.add_argument("--min-rows", type=int, default=0)
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="Require every row to have source_audit_status=audited.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Source-audit manifest not found: {manifest_path}")
        return 1

    rows = load_jsonl(manifest_path)
    schema = load_json(Path(args.schema))
    source_family_ids = (
        load_source_family_ids(Path(args.source_families))
        if Path(args.source_families).exists()
        else set()
    )

    errors: List[str] = []
    errors.extend(validate_schema(rows, schema))
    if not errors:
        errors.extend(validate_consistency(rows, source_family_ids, args.require_pass))

    if len(rows) < args.min_rows:
        errors.append(f"row count {len(rows)} is below required minimum {args.min_rows}")

    if errors:
        print("Source-audit manifest validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    status_counts = Counter(row["source_audit_status"] for row in rows)
    origin_counts = Counter(row["record_origin"] for row in rows)
    family_counts = Counter(row["source_family_id"] for row in rows)
    print("Source-audit manifest validation passed.")
    print(f"Rows: {len(rows)}")
    print(f"Audit status counts: {dict(sorted(status_counts.items()))}")
    print(f"Record origin counts: {dict(sorted(origin_counts.items()))}")
    print(f"Source family counts: {dict(sorted(family_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
