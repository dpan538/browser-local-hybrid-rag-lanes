#!/usr/bin/env python3
"""Generate Paper v1 condition-hidden semantic review packs."""

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
    parser.add_argument("--records", default="runs/paper_v1_qwen_webllm_50_clean/records.jsonl")
    parser.add_argument("--output", default="review/paper_v1_blind_pack.json")
    parser.add_argument("--mapping", default="review/paper_v1_blind_mapping.json")
    parser.add_argument("--seed", type=int, default=538)
    args = parser.parse_args()

    records = load_jsonl(Path(args.records))
    rng = random.Random(args.seed)
    rng.shuffle(records)

    blind_pack = []
    mapping: Dict[str, Dict[str, Any]] = {}
    for index, record in enumerate(records, start=1):
        blind_id = f"PAPER-V1-BLIND-{index:04d}"
        mapping[blind_id] = {
            "query_id": record.get("query_id"),
            "condition": record.get("condition"),
            "run_id": record.get("run_id"),
        }
        blind_pack.append({
            "blind_id": blind_id,
            "query_id": record.get("query_id"),
            "query": record.get("query_text") or record.get("query", {}).get("text", ""),
            "answer": record.get("answer", {}),
            "review": {
                "decision": None,
                "faithfulness": None,
                "usefulness": None,
                "refusal_appropriateness": None,
                "notes": ""
            }
        })

    write_json(blind_pack, Path(args.output))
    write_json(mapping, Path(args.mapping))
    print(f"Wrote {len(blind_pack)} blinded review items to {args.output}")
    print(f"Wrote blind mapping to {args.mapping}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
