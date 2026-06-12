#!/usr/bin/env python3
"""Smoke test the source-audit manifest -> fixture compilation path."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")


def smoke_rows() -> tuple[dict, dict]:
    fields = {
        "title": {
            "state": "verified",
            "value": "Smoke Poster",
            "evidence_note": "Smoke metadata title field."
        },
        "date_text": {
            "state": "verified",
            "value": "1936",
            "evidence_note": "Smoke metadata date field."
        },
        "source": {
            "state": "verified",
            "value": "Library of Congress",
            "evidence_note": "Smoke metadata source field."
        },
        "source_citation": {
            "state": "verified",
            "value": "loc-smoke-001",
            "evidence_note": "Smoke metadata identifier field."
        },
        "rights_label": {
            "state": "verified",
            "value": "Public Domain",
            "evidence_note": "Smoke metadata rights field."
        },
        "reuse_permission": {
            "state": "verified",
            "value": "unrestricted",
            "evidence_note": "Smoke metadata reuse field."
        },
        "public_domain_status": {
            "state": "verified",
            "value": "yes",
            "evidence_note": "Smoke metadata public domain field."
        },
        "image_state_label": {
            "state": "verified",
            "value": "image_public_domain",
            "evidence_note": "Smoke rights metadata; image not downloaded."
        }
    }
    manifest = {
        "audit_version": "paper_v1_source_audit_v0",
        "manifest_id": "sa_smoke_q001_001",
        "fixture_target": "source_audited_50",
        "query_id": "q001",
        "record_id": "src_q001_001",
        "source_family_id": "loc_metadata",
        "source_name": "Library of Congress",
        "source_domain": "loc.gov",
        "source_url": "https://www.loc.gov/item/smoke/",
        "metadata_url": "https://www.loc.gov/item/smoke/?fo=json",
        "source_record_id": "smoke",
        "record_origin": "source_audited",
        "source_audit_status": "audited",
        "audit_scope": "metadata_only_no_image_download",
        "fields": fields,
        "auditor_notes": "Smoke test only.",
        "checked_at": "2026-06-12T00:00:00+00:00",
        "checked_by": "codex"
    }
    plan = {
        "plan_version": "paper_v1_query_plan_v0",
        "query_id": "q001",
        "role": "warmup",
        "stratum": "source_rights",
        "question_text": "What rights and reuse information does this source record provide?",
        "intent_label": "source/rights",
        "primary_lane": "deterministic_exact",
        "mixed_intent": False,
        "decisive_fields": ["source", "rights_label", "reuse_permission"],
        "lane_intent": ["source", "rights", "provenance"],
        "manifest_ids": ["sa_smoke_q001_001"],
        "warmup": True,
        "refusal_policy": "matrix",
        "authoring_notes": "Smoke query plan."
    }
    return manifest, plan


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", default="/private/tmp/hybrid_lane_source_audit_smoke")
    args = parser.parse_args()
    base = Path(args.workdir)
    base.mkdir(parents=True, exist_ok=True)
    manifest, plan = smoke_rows()
    manifest_path = base / "manifest.jsonl"
    plan_path = base / "query_plan.jsonl"
    fixture_path = base / "experiment_fixture.jsonl"
    runtime_path = base / "runtime_view.jsonl"
    eval_path = base / "evaluation_view.jsonl"
    warmup_path = base / "warmup_queries.jsonl"

    write_jsonl(manifest_path, [manifest])
    write_jsonl(plan_path, [plan])

    run([
        sys.executable,
        "scripts/validate_source_audit_manifest.py",
        str(manifest_path),
        "--min-rows",
        "1",
        "--require-pass",
    ])
    run([
        sys.executable,
        "scripts/validate_source_audited_query_plan.py",
        str(plan_path),
        "--min-rows",
        "1",
    ])
    run([
        sys.executable,
        "scripts/sync_query_manifest.py",
        "--manifest",
        str(manifest_path),
        "--query-plan",
        str(plan_path),
    ])
    run([
        sys.executable,
        "scripts/compile_source_audited_fixture.py",
        "--manifest",
        str(manifest_path),
        "--query-plan",
        str(plan_path),
        "--output",
        str(fixture_path),
        "--runtime-output",
        str(runtime_path),
        "--evaluation-output",
        str(eval_path),
        "--warmup-output",
        str(warmup_path),
        "--warmup-count",
        "1",
    ])
    run([
        sys.executable,
        "scripts/check_source_audited_consistency.py",
        "--manifest",
        str(manifest_path),
        "--query-plan",
        str(plan_path),
        "--fixture",
        str(fixture_path),
        "--runtime",
        str(runtime_path),
        "--evaluation",
        str(eval_path),
        "--warmup",
        str(warmup_path),
        "--expected-rows",
        "1",
        "--require-explicit-warmup",
    ])
    print(f"Source-audited compile smoke passed in {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
