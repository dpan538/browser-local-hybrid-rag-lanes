#!/usr/bin/env python3
"""Check consistency across source-audited fixture artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set


ALLOWED_ORIGINS = {"source_audited", "derived_from_public_source"}
ALLOWED_FIXTURE_AUDITS = {"pass", "uncertain"}
REQUIRED_FREEZE_FILES = [
    "fixtures/source_audited_50/source_audit_manifest_v0.jsonl",
    "fixtures/source_audited_50/query_plan_v0.jsonl",
    "fixtures/source_audited_50/experiment_fixture.jsonl",
    "fixtures/source_audited_50/runtime_view.jsonl",
    "fixtures/source_audited_50/evaluation_view.jsonl",
    "fixtures/source_audited_50/warmup_queries.jsonl",
]


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


def record_ids_from_fixture(rows: List[Dict[str, Any]]) -> Set[str]:
    ids: Set[str] = set()
    for row in rows:
        for record in row["evidence_packet"].get("records", []):
            ids.add(record["record_id"])
    return ids


def check_consistency(
    manifest_path: Path,
    query_plan_path: Path,
    fixture_path: Path,
    runtime_path: Path,
    eval_path: Path,
    warmup_path: Path,
    freeze_manifest_path: Path | None,
) -> List[str]:
    errors: List[str] = []
    manifest_rows = load_jsonl(manifest_path)
    query_plan_rows = load_jsonl(query_plan_path)
    fixture_rows = load_jsonl(fixture_path)
    runtime_rows = load_jsonl(runtime_path)
    eval_rows = load_jsonl(eval_path)
    warmup_rows = load_jsonl(warmup_path)

    manifest_record_ids = {row["record_id"] for row in manifest_rows}
    fixture_record_ids = record_ids_from_fixture(fixture_rows)
    missing_manifest_records = sorted(fixture_record_ids - manifest_record_ids)
    if missing_manifest_records:
        errors.append(
            "fixture records missing from source audit manifest: "
            + ", ".join(missing_manifest_records[:20])
        )

    plan_query_ids = {row["query_id"] for row in query_plan_rows}
    fixture_query_ids = {row["query_id"] for row in fixture_rows}
    if fixture_query_ids != plan_query_ids:
        errors.append(
            "fixture/query-plan query ids differ: "
            f"missing={sorted(plan_query_ids - fixture_query_ids)} "
            f"extra={sorted(fixture_query_ids - plan_query_ids)}"
        )

    if len(runtime_rows) != len(fixture_rows):
        errors.append(f"runtime row count {len(runtime_rows)} != fixture {len(fixture_rows)}")
    if len(eval_rows) != len(fixture_rows):
        errors.append(f"evaluation row count {len(eval_rows)} != fixture {len(fixture_rows)}")

    runtime_query_ids = {row["query_id"] for row in runtime_rows}
    eval_query_ids = {row["query_id"] for row in eval_rows}
    if runtime_query_ids != fixture_query_ids:
        errors.append("runtime query ids do not match fixture query ids")
    if eval_query_ids != fixture_query_ids:
        errors.append("evaluation query ids do not match fixture query ids")

    for row in fixture_rows:
        for record in row["evidence_packet"].get("records", []):
            origin = record.get("record_origin")
            audit = record.get("source_audit_status")
            if origin not in ALLOWED_ORIGINS:
                errors.append(f"{row['query_id']}:{record['record_id']} invalid origin {origin}")
            if audit not in ALLOWED_FIXTURE_AUDITS:
                errors.append(f"{row['query_id']}:{record['record_id']} invalid audit {audit}")

    fixture_runtime_ids = {row["query_id"] for row in fixture_rows}
    for row in warmup_rows:
        if row["query_id"] not in fixture_runtime_ids:
            errors.append(f"warmup query {row['query_id']} not present in fixture")

    if freeze_manifest_path:
        manifest = load_json(freeze_manifest_path)
        hashed_files = set(manifest.get("files", {}).keys())
        missing_freeze_files = [
            file_name
            for file_name in REQUIRED_FREEZE_FILES
            if file_name not in hashed_files
        ]
        if missing_freeze_files:
            errors.append(
                "freeze manifest missing source-audited files: "
                + ", ".join(missing_freeze_files)
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="fixtures/source_audited_50/source_audit_manifest_v0.jsonl")
    parser.add_argument("--query-plan", default="fixtures/source_audited_50/query_plan_v0.jsonl")
    parser.add_argument("--fixture", default="fixtures/source_audited_50/experiment_fixture.jsonl")
    parser.add_argument("--runtime", default="fixtures/source_audited_50/runtime_view.jsonl")
    parser.add_argument("--evaluation", default="fixtures/source_audited_50/evaluation_view.jsonl")
    parser.add_argument("--warmup", default="fixtures/source_audited_50/warmup_queries.jsonl")
    parser.add_argument("--freeze-manifest")
    args = parser.parse_args()

    required_paths = [
        Path(args.manifest),
        Path(args.query_plan),
        Path(args.fixture),
        Path(args.runtime),
        Path(args.evaluation),
        Path(args.warmup),
    ]
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        print("Source-audited consistency check failed:")
        for path in missing:
            print(f"  - missing file: {path}")
        return 1

    errors = check_consistency(
        Path(args.manifest),
        Path(args.query_plan),
        Path(args.fixture),
        Path(args.runtime),
        Path(args.evaluation),
        Path(args.warmup),
        Path(args.freeze_manifest) if args.freeze_manifest else None,
    )
    if errors:
        print("Source-audited consistency check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Source-audited consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
