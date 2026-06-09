#!/usr/bin/env python3
"""Merge blinded reviewer scores back to true query and condition labels."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def write_jsonl(rows: Iterable[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")


def run_record_index(path: Path) -> Dict[tuple[str, str, str], Dict[str, Any]]:
    index: Dict[tuple[str, str, str], Dict[str, Any]] = {}
    if not path.exists():
        return index
    for row in load_jsonl(path):
        key = (
            str(row.get("query_id")),
            str(row.get("condition")),
            str(row.get("run_id")),
        )
        index[key] = row
    return index


def merge_reviews(
    reviewed_pack_path: Path,
    mapping_path: Path,
    records_path: Path,
    output_path: Path,
) -> None:
    reviewed_items = load_json(reviewed_pack_path)
    mapping = load_json(mapping_path)
    records = run_record_index(records_path)

    merged = []
    for item in reviewed_items:
        blind_id = item["blind_id"]
        if blind_id not in mapping:
            raise KeyError(f"blind_id {blind_id} is missing from mapping")

        true_label = mapping[blind_id]
        key = (
            str(true_label.get("query_id")),
            str(true_label.get("condition")),
            str(true_label.get("run_id")),
        )
        source_record = records.get(key, {})
        merged.append({
            "blind_id": blind_id,
            "query_id": true_label.get("query_id"),
            "condition": true_label.get("condition"),
            "run_id": true_label.get("run_id"),
            "review_checklist": item.get("review_checklist", {}),
            "perception_scores": item.get("perception_scores", {}),
            "reviewer_notes": item.get("reviewer_notes", ""),
            "auto_contract": item.get("auto_contract") or source_record.get("auto_contract"),
            "contract_metrics": source_record.get("contract_metrics", {}),
            "latency": source_record.get("latency", {}),
        })

    write_jsonl(merged, output_path)
    print(f"Wrote {len(merged)} unblinded review rows to {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviewed-pack", default="review/blind_pack.json")
    parser.add_argument("--mapping", default="review/blind_mapping.json")
    parser.add_argument("--records", default="runs/collected_records.jsonl")
    parser.add_argument("--output", default="review/unblinded_review_records.jsonl")
    args = parser.parse_args()

    merge_reviews(
        reviewed_pack_path=Path(args.reviewed_pack),
        mapping_path=Path(args.mapping),
        records_path=Path(args.records),
        output_path=Path(args.output),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
