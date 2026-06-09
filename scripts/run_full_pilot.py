#!/usr/bin/env python3
"""Run all runtime queries across all primary conditions through the Flask API."""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path
from typing import Any, Dict, List
from urllib import request


CONDITIONS = [
    "all_generation",
    "hybrid_without_refusal",
    "full_hybrid",
]


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def run_api(base_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return post_json(f"{base_url.rstrip('/')}/api/run", payload)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8787")
    parser.add_argument("--runtime", default="fixtures/runtime_view/experiment_fixture.runtime.jsonl")
    parser.add_argument("--warmup", default="fixtures/warmup_queries.jsonl")
    parser.add_argument("--output", default="runs/collected_records.jsonl")
    parser.add_argument("--seed", type=int, default=538)
    parser.add_argument("--sleep-ms", type=int, default=100)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    runtime_rows = load_jsonl(Path(args.runtime))
    warmup_rows = load_jsonl(Path(args.warmup))

    for row in warmup_rows:
        for condition in CONDITIONS[:1]:
            run_api(args.base_url, {
                "query_id": row["query_id"],
                "condition": condition,
                "warm_state": "warmup",
                "run_id": "pilot_warmup",
            })

    planned = [
        (row["query_id"], condition)
        for row in runtime_rows
        for condition in CONDITIONS
    ]
    rng.shuffle(planned)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for query_id, condition in planned:
            record = run_api(args.base_url, {
                "query_id": query_id,
                "condition": condition,
                "warm_state": "warm",
                "run_id": "pilot_run_001",
            })
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")
            time.sleep(args.sleep_ms / 1000.0)

    print(f"Wrote {len(planned)} run records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
