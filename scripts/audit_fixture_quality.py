#!/usr/bin/env python3
"""Audit draft fixture quality before promotion."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def table(counter: Counter[Any]) -> List[str]:
    return [f"| `{key}` | {value} |" for key, value in sorted(counter.items())]


def duplicate_queries(rows: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    buckets: Dict[str, List[str]] = defaultdict(list)
    for row in rows:
        buckets[row["query"]["text"]].append(row["query_id"])
    return {text: ids for text, ids in buckets.items() if len(ids) > 1}


def record_origin_counts(rows: List[Dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        for record in row["evidence_packet"].get("records", []):
            counts[record.get("record_origin", "missing")] += 1
    return counts


def source_audit_counts(rows: List[Dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        records = row["evidence_packet"].get("records", [])
        if not records:
            counts["no_records"] += 1
        for record in records:
            counts[record.get("source_audit_status", "missing")] += 1
    return counts


def promotion_blockers(rows: List[Dict[str, Any]]) -> List[str]:
    blockers: List[str] = []
    duplicates = duplicate_queries(rows)
    if duplicates:
        blockers.append(
            f"{sum(len(ids) for ids in duplicates.values())} rows share repeated query text."
        )

    synthetic_records = record_origin_counts(rows).get("synthetic", 0)
    if synthetic_records:
        blockers.append(
            f"{synthetic_records} records are synthetic; promotion needs explicit reporting language."
        )

    not_audited = source_audit_counts(rows).get("not_audited", 0)
    if not_audited:
        blockers.append(
            f"{not_audited} records are not source-audited; evidence correctness claims are blocked."
        )

    no_record_rows = [
        row["query_id"]
        for row in rows
        if not row["evidence_packet"].get("records")
    ]
    if no_record_rows:
        blockers.append(
            f"{len(no_record_rows)} rows have no records: {', '.join(no_record_rows[:12])}."
        )

    return blockers


def markdown_report(rows: List[Dict[str, Any]]) -> str:
    role_counts = Counter(row.get("fixture_meta", {}).get("role", "missing") for row in rows)
    stratum_counts = Counter(row.get("fixture_meta", {}).get("stratum", "missing") for row in rows)
    state_counts = Counter(row["evidence_packet"]["aggregated_evidence_state"] for row in rows)
    refusal_counts = Counter(str(row.get("fixture_meta", {}).get("refusal_expected")) for row in rows)
    conflict_counts = Counter(str(row.get("fixture_meta", {}).get("conflict_expected")) for row in rows)
    duplicates = duplicate_queries(rows)
    blockers = promotion_blockers(rows)

    lines = [
        "# Fixture Quality Audit V0",
        "",
        "This report audits the compiled draft fixture before promotion. It is",
        "descriptive and intentionally conservative: findings here do not mean the",
        "fixture is invalid, only that it is not yet ready for paper-facing use.",
        "",
        "## Summary",
        "",
        f"- Rows: {len(rows)}",
        f"- Unique query texts: {len(set(row['query']['text'] for row in rows))}",
        f"- Duplicate query text groups: {len(duplicates)}",
        "",
        "## Promotion Blockers",
        "",
    ]
    if blockers:
        lines.extend(f"- {item}" for item in blockers)
    else:
        lines.append("- No automatic promotion blockers detected.")

    sections = [
        ("Role Counts", role_counts),
        ("Stratum Counts", stratum_counts),
        ("Evidence State Counts", state_counts),
        ("Refusal Expected Counts", refusal_counts),
        ("Conflict Expected Counts", conflict_counts),
        ("Record Origin Counts", record_origin_counts(rows)),
        ("Source Audit Counts", source_audit_counts(rows)),
    ]
    for title, counter in sections:
        lines.extend(["", f"## {title}", "", "| Value | Count |", "|---|---:|"])
        lines.extend(table(counter))

    lines.extend(["", "## Duplicate Query Text", ""])
    if duplicates:
        for text, ids in sorted(duplicates.items(), key=lambda item: (-len(item[1]), item[0])):
            lines.append(f"- `{', '.join(ids)}`: {text}")
    else:
        lines.append("- No repeated query text.")

    recommendations = []
    if duplicates:
        recommendations.append(
            "Rewrite repeated query templates so each eval row has a distinct user wording."
        )
    recommendations.extend([
        "Keep synthetic/source-audit limitations explicit in the paper and evaluation metadata.",
        "Review no-record refusal rows to ensure they are intentional missing-evidence tests.",
        "Do not promote the draft fixture until source-audit and no-record limitations are accepted or revised.",
    ])
    lines.extend(["", "## Recommended Next Edits", ""])
    for index, recommendation in enumerate(recommendations, start=1):
        lines.append(f"{index}. {recommendation}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fixture",
        default="fixtures/drafts/compiled_experiment_fixture_v0.jsonl",
    )
    parser.add_argument(
        "--output",
        default="reports/FIXTURE_QUALITY_AUDIT_V0.md",
    )
    args = parser.parse_args()

    rows = load_jsonl(Path(args.fixture))
    report = markdown_report(rows)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote fixture quality audit to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
