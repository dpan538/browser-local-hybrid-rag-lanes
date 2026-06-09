#!/usr/bin/env python3
"""Apply the seeded dev/eval split from query_strata_v0.json to a blueprint."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from generate_fixture_blueprint import split_assignments  # noqa: E402


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


def write_jsonl(rows: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")


def expected_role_by_query(config: Dict[str, Any]) -> Dict[str, str]:
    slots = []
    global_index = 0
    for stratum in config["strata"]:
        for local_index in range(1, int(stratum["count"]) + 1):
            global_index += 1
            query_id = f"q{global_index:03d}"
            slots.append((query_id, f"{stratum['name']}:{local_index}"))

    roles = split_assignments(
        [slot_key for _, slot_key in slots],
        int(config["dev_count"]),
        str(config.get("split_seed", "fixture-blueprint-v0")),
    )
    return {query_id: roles[slot_key] for query_id, slot_key in slots}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blueprint", default="fixtures/drafts/fixture_expansion_blueprint_v0.jsonl")
    parser.add_argument("--config", default="fixtures/drafts/query_strata_v0.json")
    args = parser.parse_args()

    blueprint_path = REPO_ROOT / args.blueprint
    config = load_json(REPO_ROOT / args.config)
    roles = expected_role_by_query(config)
    rows = load_jsonl(blueprint_path)

    for row in rows:
        row["role"] = roles[row["query_id"]]

    write_jsonl(rows, blueprint_path)
    print(
        f"Applied seeded split {config.get('split_seed')} "
        f"to {len(rows)} blueprint rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
