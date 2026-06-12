#!/usr/bin/env python3
"""Check alignment between source-audit manifest rows and query plan rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="fixtures/source_audited_50/source_audit_manifest_v0.jsonl")
    parser.add_argument("--query-plan", default="fixtures/source_audited_50/query_plan_v0.jsonl")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    query_plan_path = Path(args.query_plan)
    missing = [str(path) for path in (manifest_path, query_plan_path) if not path.exists()]
    if missing:
        print("Manifest/query-plan sync failed:")
        for path in missing:
            print(f"  - missing file: {path}")
        return 1

    manifest_rows = load_jsonl(manifest_path)
    plan_rows = load_jsonl(query_plan_path)
    manifest_by_id = {row["manifest_id"]: row for row in manifest_rows}
    manifest_query_ids = {row["query_id"] for row in manifest_rows}
    plan_query_ids = {row["query_id"] for row in plan_rows}

    errors: List[str] = []
    for row in plan_rows:
        query_id = row["query_id"]
        if row.get("allow_no_records", False):
            continue
        manifest_ids = row.get("manifest_ids") or []
        if manifest_ids:
            missing_ids = [item for item in manifest_ids if item not in manifest_by_id]
            if missing_ids:
                errors.append(f"{query_id}: manifest_ids not found: {missing_ids}")
        elif query_id not in manifest_query_ids:
            errors.append(f"{query_id}: no manifest row and allow_no_records=false")

    covered_manifest_ids: Set[str] = set()
    for row in plan_rows:
        manifest_ids = row.get("manifest_ids") or []
        if manifest_ids:
            covered_manifest_ids.update(manifest_ids)
        elif not row.get("allow_no_records", False):
            covered_manifest_ids.update(
                manifest["manifest_id"]
                for manifest in manifest_rows
                if manifest["query_id"] == row["query_id"]
            )
    orphan_manifest_ids = sorted(set(manifest_by_id) - covered_manifest_ids)
    if orphan_manifest_ids:
        errors.append(
            "manifest rows not referenced by query plan: "
            + ", ".join(orphan_manifest_ids[:20])
        )

    if errors:
        print("Manifest/query-plan sync failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Manifest/query-plan sync passed.")
    print(f"Manifest rows: {len(manifest_rows)}")
    print(f"Query plan rows: {len(plan_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
