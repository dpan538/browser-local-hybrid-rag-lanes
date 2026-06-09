#!/usr/bin/env python3
"""Create a SHA-256 freeze manifest for paper-facing pilot artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


DEFAULT_FILES = [
    "fixtures/experiment_fixture.jsonl",
    "fixtures/runtime_view/experiment_fixture.runtime.jsonl",
    "fixtures/evaluation_view/experiment_fixture.eval.jsonl",
    "fixtures/warmup_queries.jsonl",
    "config/lane_rules_v1.yaml",
    "config/refusal_decision_matrix.csv",
    "config/condition_prompt_pack_v1.json",
    "docs/EXPERIMENT_EXECUTION_PLAN.md",
    "docs/PROTOCOL_FREEZE_V0.md",
    "schemas/run_record_schema.json",
    "schemas/environment_stability_log_schema.json",
    "schemas/condition_prompt_pack_schema.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(files: List[str]) -> Dict[str, object]:
    manifest: Dict[str, object] = {
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "files": {},
        "missing": [],
    }
    file_hashes: Dict[str, str] = {}
    missing: List[str] = []
    for file_name in files:
        path = Path(file_name)
        if path.exists():
            file_hashes[file_name] = sha256(path)
        else:
            missing.append(file_name)
    manifest["files"] = file_hashes
    manifest["missing"] = missing
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="runs/freeze_manifest.json",
        help="Path to write the freeze manifest.",
    )
    parser.add_argument(
        "--file",
        action="append",
        dest="files",
        help="Additional file to include. Can be repeated.",
    )
    args = parser.parse_args()

    files = DEFAULT_FILES + (args.files or [])
    manifest = build_manifest(files)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest written to {output_path}")
    if manifest["missing"]:
        print("Missing files:")
        for file_name in manifest["missing"]:
            print(f"  - {file_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
