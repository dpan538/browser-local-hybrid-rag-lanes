#!/usr/bin/env python3
"""Lightweight paired analysis for exploratory hybrid lane pilot records."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import median
from typing import Any, Dict, List, Tuple


CONTRASTS = [
    ("all_generation", "hybrid_without_refusal"),
    ("hybrid_without_refusal", "full_hybrid"),
]


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def grouped_by_query(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Dict[str, Any]]]:
    grouped: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for record in records:
        grouped.setdefault(record["query_id"], {})[record["condition"]] = record
    return grouped


def contract_pass(record: Dict[str, Any]) -> bool:
    metrics = record.get("contract_metrics", {})
    return not bool(metrics.get("contract_failure"))


def total_latency(record: Dict[str, Any]) -> float:
    latency = record.get("latency", {})
    return float(latency.get("hybrid_system_latency_ms") or 0.0)


def binomial_two_sided(k: int, n: int, p: float = 0.5) -> float:
    if n == 0:
        return 1.0
    observed = math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
    total = 0.0
    for i in range(n + 1):
        prob = math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
        if prob <= observed + 1e-15:
            total += prob
    return min(1.0, total)


def mcnemar_like(a_records: List[Dict[str, Any]], b_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    b01 = 0
    b10 = 0
    for left, right in zip(a_records, b_records):
        left_pass = contract_pass(left)
        right_pass = contract_pass(right)
        if left_pass and not right_pass:
            b10 += 1
        if not left_pass and right_pass:
            b01 += 1
    discordant = b01 + b10
    return {
        "left_fail_right_pass": b01,
        "left_pass_right_fail": b10,
        "discordant_pairs": discordant,
        "exact_binomial_p": binomial_two_sided(min(b01, b10), discordant),
    }


def paired_records(
    grouped: Dict[str, Dict[str, Dict[str, Any]]],
    left: str,
    right: str,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    left_rows = []
    right_rows = []
    for query_id in sorted(grouped):
        by_condition = grouped[query_id]
        if left in by_condition and right in by_condition:
            left_rows.append(by_condition[left])
            right_rows.append(by_condition[right])
    return left_rows, right_rows


def contrast_summary(
    grouped: Dict[str, Dict[str, Dict[str, Any]]],
    left: str,
    right: str,
) -> Dict[str, Any]:
    left_rows, right_rows = paired_records(grouped, left, right)
    latency_diffs = [
        total_latency(right_record) - total_latency(left_record)
        for left_record, right_record in zip(left_rows, right_rows)
    ]
    sign_positive = sum(1 for diff in latency_diffs if diff > 0)
    sign_negative = sum(1 for diff in latency_diffs if diff < 0)
    nonzero = sign_positive + sign_negative
    return {
        "contrast": f"{left} vs {right}",
        "paired_queries": len(left_rows),
        "contract": mcnemar_like(left_rows, right_rows),
        "median_latency_diff_ms_right_minus_left": (
            median(latency_diffs) if latency_diffs else None
        ),
        "latency_sign_test_p": binomial_two_sided(min(sign_positive, sign_negative), nonzero),
        "latency_positive_diffs": sign_positive,
        "latency_negative_diffs": sign_negative,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", default="runs/collected_records.jsonl")
    parser.add_argument("--output", default="runs/analysis_summary.md")
    args = parser.parse_args()

    records = load_jsonl(Path(args.records))
    grouped = grouped_by_query(records)
    summaries = [contrast_summary(grouped, left, right) for left, right in CONTRASTS]

    lines = [
        "# Exploratory Paired Analysis Summary",
        "",
        "This report is descriptive for the first pilot. It does not claim statistical superiority.",
        "",
    ]
    for summary in summaries:
        lines.extend([
            f"## {summary['contrast']}",
            "",
            f"- Paired queries: {summary['paired_queries']}",
            f"- Contract discordant pairs: {summary['contract']['discordant_pairs']}",
            f"- Left fail / right pass: {summary['contract']['left_fail_right_pass']}",
            f"- Left pass / right fail: {summary['contract']['left_pass_right_fail']}",
            f"- Exact paired binomial p: {summary['contract']['exact_binomial_p']:.4f}",
            f"- Median latency diff, right minus left: {summary['median_latency_diff_ms_right_minus_left']}",
            f"- Latency sign-test p: {summary['latency_sign_test_p']:.4f}",
            "",
        ])

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote analysis summary to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
