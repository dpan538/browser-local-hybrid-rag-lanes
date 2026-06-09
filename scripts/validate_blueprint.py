#!/usr/bin/env python3
"""Validate fixture expansion blueprint rows before compilation."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

import jsonschema
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from generate_fixture_blueprint import split_assignments  # noqa: E402


LANE_FOR_ACTION = {
    "deterministic_exact": {"deterministic_render"},
    "deterministic_refusal": {"deterministic_refusal"},
    "generative": {"generative_answer"},
    "compound": {"compound_answer"},
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if raw_line:
                rows.append(json.loads(raw_line))
    return rows


def validate_schema(rows: Iterable[Dict[str, Any]], schema_path: Path) -> List[str]:
    schema = load_json(schema_path)
    errors: List[str] = []
    for index, row in enumerate(rows, start=1):
        try:
            jsonschema.validate(row, schema)
        except jsonschema.ValidationError as exc:
            dotted_path = ".".join(str(part) for part in exc.path)
            errors.append(f"line {index} {row.get('query_id', '?')}: {exc.message} ({dotted_path})")
    return errors


def load_rules(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def rule_coverage(rules: Dict[str, Any]) -> Dict[str, Set[str]]:
    coverage: Dict[str, Set[str]] = {
        "deterministic_render": set(),
        "deterministic_refusal": set(),
        "generative_answer": set(),
        "compound_answer": set(),
    }
    for rule in rules.get("rules", []):
        action = rule.get("action")
        labels = rule.get("condition", {}).get("intent_label", [])
        if isinstance(labels, str):
            labels = [labels]
        if action in coverage:
            coverage[action].update(labels)
    return coverage


def refusal_states(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as handle:
        return {row["evidence_state"] for row in csv.DictReader(handle)}


def expected_slots(config: Dict[str, Any]) -> List[tuple[str, str, int]]:
    slots: List[tuple[str, str, int]] = []
    global_index = 0
    for stratum in config["strata"]:
        for local_index in range(1, int(stratum["count"]) + 1):
            global_index += 1
            slots.append((f"q{global_index:03d}", stratum["name"], local_index))
    return slots


def validate_split(rows: List[Dict[str, Any]], config: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    slots = expected_slots(config)
    slot_keys = [f"{stratum}:{local_index}" for _, stratum, local_index in slots]
    expected_roles = split_assignments(
        slot_keys,
        int(config["dev_count"]),
        str(config.get("split_seed", "fixture-blueprint-v0")),
    )
    by_id = {row["query_id"]: row for row in rows}

    for query_id, stratum, local_index in slots:
        row = by_id.get(query_id)
        if row is None:
            errors.append(f"{query_id}: missing expected blueprint row")
            continue
        expected_role = expected_roles[f"{stratum}:{local_index}"]
        if row.get("role") != expected_role:
            errors.append(
                f"{query_id}: role {row.get('role')} does not match seeded role {expected_role}"
            )

    role_counts = Counter(row["role"] for row in rows)
    if role_counts["dev"] != int(config["dev_count"]):
        errors.append(f"dev count {role_counts['dev']} != {config['dev_count']}")
    if role_counts["eval"] != int(config["eval_count"]):
        errors.append(f"eval count {role_counts['eval']} != {config['eval_count']}")
    return errors


def validate_quotas(rows: List[Dict[str, Any]], config: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if len(rows) != int(config["total_measured_queries"]):
        errors.append(f"row count {len(rows)} != {config['total_measured_queries']}")

    expected = {item["name"]: int(item["count"]) for item in config["strata"]}
    observed = Counter(row["stratum"] for row in rows)
    for stratum, count in expected.items():
        if observed[stratum] != count:
            errors.append(f"stratum {stratum}: observed {observed[stratum]} != expected {count}")
    return errors


def validate_rule_alignment(
    rows: List[Dict[str, Any]],
    rules: Dict[str, Any],
    refusal_state_set: Set[str],
) -> List[str]:
    errors: List[str] = []
    coverage = rule_coverage(rules)
    all_rule_labels = set().union(*coverage.values())

    for row in rows:
        query_id = row["query_id"]
        lane = row["primary_lane"]
        intent = row["intent_label"]
        actions = LANE_FOR_ACTION[lane]
        supported = any(intent in coverage[action] for action in actions)
        if not supported:
            errors.append(
                f"{query_id}: intent_label '{intent}' is not covered by lane '{lane}' in lane_rules_v1"
            )
        if intent not in all_rule_labels:
            errors.append(f"{query_id}: intent_label '{intent}' not present in any lane rule")

        evidence_state = row["evidence_state"]
        if row["conflict_expected"] != (evidence_state == "contradictory"):
            errors.append(f"{query_id}: conflict_expected inconsistent with evidence_state")
        if row["refusal_expected"] and evidence_state not in refusal_state_set:
            if row["primary_lane"] != "deterministic_refusal":
                errors.append(
                    f"{query_id}: refusal_expected but evidence_state '{evidence_state}' "
                    "has no refusal matrix entry"
                )
        if row["primary_lane"] == "deterministic_refusal" and not row["refusal_expected"]:
            errors.append(f"{query_id}: deterministic_refusal lane requires refusal_expected=true")
        if row["mixed_intent"] and row["primary_lane"] != "compound":
            errors.append(f"{query_id}: mixed_intent rows must use compound primary_lane in v0")

        deterministic_fields = row.get("deterministic_fields", {})
        for field in row["decisive_fields"]:
            if field in {"source", "rights_label", "reuse_permission", "public_domain_status", "image_state_label"}:
                if field not in deterministic_fields:
                    errors.append(f"{query_id}: decisive deterministic field '{field}' missing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blueprint", default="fixtures/drafts/fixture_expansion_blueprint_v0.jsonl")
    parser.add_argument("--config", default="fixtures/drafts/query_strata_v0.json")
    parser.add_argument("--schema", default="schemas/fixture_blueprint_schema.json")
    parser.add_argument("--rules", default="config/lane_rules_v1.yaml")
    parser.add_argument("--refusal-matrix", default="config/refusal_decision_matrix.csv")
    args = parser.parse_args()

    rows = load_jsonl(REPO_ROOT / args.blueprint)
    config = load_json(REPO_ROOT / args.config)
    rules = load_rules(REPO_ROOT / args.rules)
    refusal_state_set = refusal_states(REPO_ROOT / args.refusal_matrix)

    errors: List[str] = []
    errors.extend(validate_schema(rows, REPO_ROOT / args.schema))
    errors.extend(validate_quotas(rows, config))
    errors.extend(validate_split(rows, config))
    errors.extend(validate_rule_alignment(rows, rules, refusal_state_set))

    if errors:
        print("Blueprint validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Blueprint validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
