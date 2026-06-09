#!/usr/bin/env python3
"""Export runtime and evaluation fixture views from a master JSONL fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict


DEFAULT_RULE_VERSION = "lane_rules_v1"


def build_runtime_view(row: Dict[str, Any]) -> Dict[str, Any]:
    evidence_packet = row["evidence_packet"]
    return {
        "fixture_version": row["fixture_version"],
        "query_id": row["query_id"],
        "applicable_conditions": row.get("applicable_conditions", [1, 2, 3]),
        "query": {
            "text": row["query"]["text"],
        },
        "routing_inputs": {
            "rule_version": DEFAULT_RULE_VERSION,
            "intent_signal": row["query"]["intent_label"],
            "evidence_state": evidence_packet["aggregated_evidence_state"],
            "decisive_fields": evidence_packet["decisive_fields"],
        },
        "evidence_packet": evidence_packet,
    }


def build_evaluation_view(row: Dict[str, Any]) -> Dict[str, Any]:
    evidence_packet = row["evidence_packet"]
    query = row["query"]
    source_audit_statuses = [
        record.get("source_audit_status", "not_audited")
        for record in evidence_packet.get("records", [])
    ]
    return {
        "fixture_version": row["fixture_version"],
        "query_id": row["query_id"],
        "evaluation_labels": {
            "intent_label": query["intent_label"],
            "primary_lane": query["primary_lane"],
            "secondary_lanes": query.get("secondary_lanes", []),
            "mixed_intent": query.get("mixed_intent", False),
            "routing_ambiguity_notes": query.get("routing_ambiguity_notes", ""),
            "aggregated_evidence_state": evidence_packet["aggregated_evidence_state"],
            "decisive_fields": evidence_packet["decisive_fields"],
            "source_audit_statuses": source_audit_statuses,
        },
        "expected_behavior": row["expected_behavior"],
    }


def write_jsonl(rows: list[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")


def split_fixture(master_path: Path, runtime_path: Path, eval_path: Path) -> None:
    runtime_rows = []
    eval_rows = []
    with master_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            row = json.loads(raw_line)
            runtime_rows.append(build_runtime_view(row))
            eval_rows.append(build_evaluation_view(row))

    write_jsonl(runtime_rows, runtime_path)
    write_jsonl(eval_rows, eval_path)


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "Usage: python scripts/split_fixture_views.py "
            "<master.jsonl> <runtime.jsonl> <evaluation.jsonl>"
        )
        return 1

    split_fixture(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
