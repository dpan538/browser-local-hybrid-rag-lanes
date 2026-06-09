#!/usr/bin/env python3
"""Check whether a compiled draft fixture can be promoted."""

from __future__ import annotations

import argparse
import json
from collections import Counter
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


def duplicate_query_ids(rows: List[Dict[str, Any]]) -> List[str]:
    counts = Counter(row["query_id"] for row in rows)
    return sorted(query_id for query_id, count in counts.items() if count > 1)


def duplicate_query_texts(rows: List[Dict[str, Any]]) -> List[str]:
    counts = Counter(row["query"]["text"] for row in rows)
    return sorted(text for text, count in counts.items() if count > 1)


def no_record_rows(rows: List[Dict[str, Any]]) -> List[str]:
    return [
        row["query_id"]
        for row in rows
        if not row["evidence_packet"].get("records")
    ]


def unjustified_no_record_rows(rows: List[Dict[str, Any]]) -> List[str]:
    bad = []
    for row in rows:
        if row["evidence_packet"].get("records"):
            continue
        meta = row.get("fixture_meta", {})
        if not (
            meta.get("refusal_expected")
            and row["evidence_packet"].get("aggregated_evidence_state") == "missing"
        ):
            bad.append(row["query_id"])
    return bad


def record_counts(rows: List[Dict[str, Any]], field: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        records = row["evidence_packet"].get("records", [])
        if not records:
            counts["no_records"] += 1
        for record in records:
            counts[str(record.get(field, "missing"))] += 1
    return counts


def gate_findings(rows: List[Dict[str, Any]], mode: str) -> tuple[List[str], List[str]]:
    failures: List[str] = []
    warnings: List[str] = []

    if len(rows) != 50:
        failures.append(f"Expected 50 measured rows; found {len(rows)}.")

    duplicate_ids = duplicate_query_ids(rows)
    if duplicate_ids:
        failures.append(f"Duplicate query_id values: {', '.join(duplicate_ids)}.")

    duplicate_texts = duplicate_query_texts(rows)
    if duplicate_texts:
        failures.append(f"{len(duplicate_texts)} duplicate query texts remain.")

    unjustified_missing = unjustified_no_record_rows(rows)
    if unjustified_missing:
        failures.append(
            "No-record rows not justified as missing-evidence refusal tests: "
            + ", ".join(unjustified_missing)
        )

    origin_counts = record_counts(rows, "record_origin")
    audit_counts = record_counts(rows, "source_audit_status")

    synthetic_records = origin_counts.get("synthetic", 0)
    not_audited_records = audit_counts.get("not_audited", 0)

    if mode == "paper":
        if synthetic_records:
            failures.append(
                f"{synthetic_records} synthetic records remain; paper mode "
                "requires source-audited or derived-public-source records."
            )
        if not_audited_records:
            failures.append(
                f"{not_audited_records} records are not source-audited; "
                "paper mode blocks evidence-correctness claims."
            )
    else:
        if synthetic_records:
            warnings.append(
                f"{synthetic_records} synthetic records: exploratory promotion "
                "must frame the fixture as synthetic."
            )
        if not_audited_records:
            warnings.append(
                f"{not_audited_records} records are not source-audited: "
                "evidence correctness claims remain blocked."
            )

    missing_rows = no_record_rows(rows)
    if missing_rows:
        warnings.append(
            f"{len(missing_rows)} no-record rows are present and treated as "
            "missing-evidence refusal tests."
        )

    return failures, warnings


def markdown_report(rows: List[Dict[str, Any]], mode: str) -> str:
    failures, warnings = gate_findings(rows, mode)
    decision = "PASS" if not failures else "FAIL"
    lines = [
        "# Promotion Gate V0",
        "",
        f"- Mode: `{mode}`",
        f"- Decision: `{decision}`",
        f"- Rows: {len(rows)}",
        f"- Unique query IDs: {len(set(row['query_id'] for row in rows))}",
        f"- Unique query texts: {len(set(row['query']['text'] for row in rows))}",
        "",
        "## Failures",
        "",
    ]
    if failures:
        lines.extend(f"- {item}" for item in failures)
    else:
        lines.append("- None.")

    lines.extend(["", "## Warnings", ""])
    if warnings:
        lines.extend(f"- {item}" for item in warnings)
    else:
        lines.append("- None.")

    sections = [
        ("Record Origin Counts", record_counts(rows, "record_origin")),
        ("Source Audit Counts", record_counts(rows, "source_audit_status")),
    ]
    for title, counts in sections:
        lines.extend(["", f"## {title}", "", "| Value | Count |", "|---|---:|"])
        for key, value in sorted(counts.items()):
            lines.append(f"| `{key}` | {value} |")

    lines.extend([
        "",
        "## Interpretation",
        "",
        "Exploratory mode may pass with synthetic records if the study claims are",
        "limited to evidence-to-output fidelity, refusal behavior, latency plumbing,",
        "and usability workflow rehearsal. Paper mode requires source-audited or",
        "derived-public-source evidence before making evidence-correctness claims.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fixture",
        default="fixtures/drafts/compiled_experiment_fixture_v0.jsonl",
    )
    parser.add_argument(
        "--mode",
        choices=["exploratory", "paper"],
        default="exploratory",
    )
    parser.add_argument("--output", default="reports/PROMOTION_GATE_V0.md")
    args = parser.parse_args()

    rows = load_jsonl(Path(args.fixture))
    report = markdown_report(rows, args.mode)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")

    failures, _warnings = gate_findings(rows, args.mode)
    print(f"Wrote promotion gate report to {output}")
    print("Decision:", "PASS" if not failures else "FAIL")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
