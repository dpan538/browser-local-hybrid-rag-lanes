#!/usr/bin/env python3
"""Select a small runtime-view subset for Codex browser pilot runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_QUERY_IDS = [
    "q001",
    "q009",
    "q015",
    "q021",
    "q027",
    "q033",
    "q041",
    "q042",
    "q044",
    "q047",
]


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


def select_rows(rows: List[Dict[str, Any]], query_ids: List[str]) -> List[Dict[str, Any]]:
    by_id = {row["query_id"]: row for row in rows}
    missing = [query_id for query_id in query_ids if query_id not in by_id]
    if missing:
        raise ValueError(f"query IDs not found in runtime view: {', '.join(missing)}")
    return [by_id[query_id] for query_id in query_ids]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", default="fixtures/drafts/runtime_view_v0.jsonl")
    parser.add_argument("--output", default="fixtures/drafts/browser_pilot_subset_v0.jsonl")
    parser.add_argument("--query-ids", default=",".join(DEFAULT_QUERY_IDS))
    args = parser.parse_args()

    query_ids = [item.strip() for item in args.query_ids.split(",") if item.strip()]
    rows = load_jsonl(Path(args.runtime))
    selected = select_rows(rows, query_ids)
    write_jsonl(selected, Path(args.output))
    print(f"Wrote {len(selected)} browser pilot rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
