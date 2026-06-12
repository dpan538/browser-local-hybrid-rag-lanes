#!/usr/bin/env python3
"""Validate Paper v1 source-audit manifest JSONL files."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema is required. Run: pip install -r requirements.txt")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "source_audit_manifest_schema.json"


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


def validate_rows(rows: List[Dict[str, Any]], schema: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    seen_record_ids: set[str] = set()

    for index, row in enumerate(rows, start=1):
        try:
            validator.validate(row)
        except jsonschema.ValidationError as exc:
            dotted_path = ".".join(str(part) for part in exc.path)
            errors.append(f"line {index}: {exc.message} (path: {dotted_path})")
            continue

        record_id = row["record_id"]
        if record_id in seen_record_ids:
            errors.append(f"line {index}: duplicate record_id '{record_id}'")
        seen_record_ids.add(record_id)

        if row["source_audit_status"] == "pass":
            for field, state in row["field_audit"].items():
                value = row["fields"].get(field, "")
                if state == "verified" and not value.strip():
                    errors.append(
                        f"line {index}: field '{field}' is verified but empty"
                    )
                if state == "missing" and value.strip():
                    errors.append(
                        f"line {index}: field '{field}' is missing but has a value"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="Source-audit manifest JSONL file.")
    parser.add_argument("--schema", default=str(SCHEMA_PATH))
    parser.add_argument("--min-rows", type=int, default=0)
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="Require every row to have source_audit_status=pass.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Source-audit manifest not found: {manifest_path}")
        return 1

    rows = load_jsonl(manifest_path)
    schema = load_json(Path(args.schema))
    errors = validate_rows(rows, schema)

    if len(rows) < args.min_rows:
        errors.append(f"row count {len(rows)} is below required minimum {args.min_rows}")

    if args.require_pass:
        failing = [
            row["record_id"]
            for row in rows
            if row.get("source_audit_status") != "pass"
        ]
        if failing:
            errors.append(
                "require-pass set but non-pass rows exist: " + ", ".join(failing[:20])
            )

    if errors:
        print("Source-audit manifest validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    status_counts = Counter(row["source_audit_status"] for row in rows)
    origin_counts = Counter(row["record_origin"] for row in rows)
    print("Source-audit manifest validation passed.")
    print(f"Rows: {len(rows)}")
    print(f"Audit status counts: {dict(sorted(status_counts.items()))}")
    print(f"Record origin counts: {dict(sorted(origin_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
