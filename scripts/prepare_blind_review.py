#!/usr/bin/env python3
"""Create a condition-blinded review pack from collected run records."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def write_json(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", default="runs/collected_records.jsonl")
    parser.add_argument("--output", default="review/blind_pack.json")
    parser.add_argument("--mapping", default="review/blind_mapping.json")
    parser.add_argument("--seed", type=int, default=538)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    records = load_jsonl(Path(args.records))
    rng.shuffle(records)

    blind_pack = []
    mapping: Dict[str, Dict[str, Any]] = {}
    for index, record in enumerate(records):
        blind_id = f"BLIND-{index + 1:04d}"
        mapping[blind_id] = {
            "query_id": record.get("query_id"),
            "condition": record.get("condition"),
            "run_id": record.get("run_id"),
        }
        blind_pack.append({
            "blind_id": blind_id,
            "query_id": record.get("query_id"),
            "answer": record.get("answer"),
            "auto_contract": record.get("auto_contract"),
            "review_checklist": {},
            "perception_scores": {
                "helpfulness": None,
                "refusal_clarity": None,
                "source_clarity": None,
                "rights_clarity": None,
                "research_usefulness": None,
                "format_consistency": None,
            },
        })

    write_json(blind_pack, Path(args.output))
    write_json(mapping, Path(args.mapping))
    print(f"Wrote {len(blind_pack)} blinded records to {args.output}")
    print(f"Wrote blind mapping to {args.mapping}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
