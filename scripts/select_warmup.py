#!/usr/bin/env python3
"""Prepare a warmup runtime-view set independent of measured rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from split_fixture_views import build_runtime_view


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", default="fixtures/experiment_fixture.jsonl")
    parser.add_argument("--output", default="fixtures/warmup_queries.jsonl")
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()

    rows = load_jsonl(Path(args.fixture))
    warmups = [row for row in rows if row.get("role") == "warmup"]
    if len(warmups) < args.count:
        raise SystemExit(
            f"Not enough warmup rows: need {args.count}, found {len(warmups)}. "
            "Add master fixture rows with top-level role='warmup' or maintain "
            "fixtures/warmup_queries.jsonl manually."
        )

    write_jsonl([build_runtime_view(row) for row in warmups[: args.count]], Path(args.output))
    print(f"Wrote {args.count} warmup rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
