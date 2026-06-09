#!/usr/bin/env python3
"""Validate the protocol bundle before a pilot or paper-facing run."""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path
from typing import Any, Dict, Iterable, List

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema is required. Run: pip install -r requirements.txt")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from validate_fixture import load_schema, validate_fixture_line  # noqa: E402


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


def validate_json_schema(instance_path: Path, schema_path: Path) -> List[str]:
    errors: List[str] = []
    schema = load_json(schema_path)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema, resolver=local_ref_resolver(schema))
    try:
        validator.validate(load_json(instance_path))
    except jsonschema.ValidationError as exc:
        dotted_path = ".".join(str(part) for part in exc.path)
        errors.append(f"{instance_path}: {exc.message} (path: {dotted_path})")
    return errors


def validate_jsonl_schema(instance_path: Path, schema_path: Path) -> List[str]:
    errors: List[str] = []
    schema = load_json(schema_path)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema, resolver=local_ref_resolver(schema))
    for index, row in enumerate(load_jsonl(instance_path), start=1):
        try:
            validator.validate(row)
        except jsonschema.ValidationError as exc:
            dotted_path = ".".join(str(part) for part in exc.path)
            errors.append(
                f"{instance_path} line {index}: {exc.message} (path: {dotted_path})"
            )
    return errors


def local_ref_resolver(schema: Dict[str, Any]) -> jsonschema.RefResolver:
    experiment_schema = load_json(REPO_ROOT / "schemas" / "experiment_fixture_schema.json")
    store = {
        "experiment_fixture_schema.json": experiment_schema,
        "https://github.com/dpan538/browser-local-hybrid-rag-lanes/schemas/experiment_fixture_schema.json": experiment_schema,
    }
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return jsonschema.RefResolver.from_schema(schema, store=store)


def validate_master_fixture(path: Path) -> List[str]:
    errors: List[str] = []
    fixture_schema = load_schema()
    for index, row in enumerate(load_jsonl(path), start=1):
        for error in validate_fixture_line(row, fixture_schema):
            errors.append(f"{path} line {index}: {error}")
    return errors


def validate_calibration(path: Path, min_examples: int) -> List[str]:
    data = load_json(path)
    calibration = data.get("calibration_set", [])
    errors: List[str] = []
    if len(calibration) < min_examples:
        errors.append(
            f"{path}: calibration_set has {len(calibration)} examples; "
            f"expected at least {min_examples}"
        )

    required_topics = {
        "conflicting": False,
        "placeholder": False,
        "format": False,
        "compound": False,
        "refusal": False,
    }
    for item in calibration:
        text = " ".join(
            str(item.get(field, ""))
            for field in ("task_description", "ideal_answer", "review_notes")
        ).lower()
        if "conflict" in text or "contradict" in text:
            required_topics["conflicting"] = True
        if "placeholder" in text:
            required_topics["placeholder"] = True
        if "format" in text:
            required_topics["format"] = True
        if "compound" in text:
            required_topics["compound"] = True
        if item.get("refusal_expected"):
            required_topics["refusal"] = True

    for topic, present in required_topics.items():
        if not present:
            errors.append(f"{path}: calibration_set missing topic '{topic}'")
    return errors


def validate_prompt_pack(path: Path) -> List[str]:
    data = load_json(path)
    conditions = data.get("conditions", {})
    errors: List[str] = []
    if conditions.get("all_generation", {}).get("deterministic_postprocessing_allowed"):
        errors.append(f"{path}: all_generation must not allow deterministic postprocessing")
    if conditions.get("hybrid_without_refusal", {}).get("deterministic_refusal_allowed"):
        errors.append(f"{path}: hybrid_without_refusal must not allow deterministic refusal")
    if not conditions.get("full_hybrid", {}).get("deterministic_refusal_allowed"):
        errors.append(f"{path}: full_hybrid must allow deterministic refusal")
    return errors


def missing_files(paths: Iterable[Path]) -> List[str]:
    return [str(path) for path in paths if not path.exists()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-calibration", type=int, default=8)
    args = parser.parse_args()

    required_paths = [
        REPO_ROOT / "fixtures" / "experiment_fixture.jsonl",
        REPO_ROOT / "fixtures" / "runtime_view" / "experiment_fixture.runtime.jsonl",
        REPO_ROOT / "fixtures" / "evaluation_view" / "experiment_fixture.eval.jsonl",
        REPO_ROOT / "config" / "condition_prompt_pack_v1.json",
        REPO_ROOT / "review" / "golden_answers.json",
        REPO_ROOT / "schemas" / "condition_prompt_pack_schema.json",
        REPO_ROOT / "schemas" / "golden_answers_schema.json",
        REPO_ROOT / "schemas" / "runtime_fixture_view_schema.json",
        REPO_ROOT / "schemas" / "evaluation_fixture_view_schema.json",
    ]
    errors = [f"Missing required file: {path}" for path in missing_files(required_paths)]
    if errors:
        for error in errors:
            print(error)
        return 1

    errors.extend(validate_master_fixture(REPO_ROOT / "fixtures" / "experiment_fixture.jsonl"))
    errors.extend(validate_jsonl_schema(
        REPO_ROOT / "fixtures" / "runtime_view" / "experiment_fixture.runtime.jsonl",
        REPO_ROOT / "schemas" / "runtime_fixture_view_schema.json",
    ))
    errors.extend(validate_jsonl_schema(
        REPO_ROOT / "fixtures" / "evaluation_view" / "experiment_fixture.eval.jsonl",
        REPO_ROOT / "schemas" / "evaluation_fixture_view_schema.json",
    ))
    errors.extend(validate_json_schema(
        REPO_ROOT / "config" / "condition_prompt_pack_v1.json",
        REPO_ROOT / "schemas" / "condition_prompt_pack_schema.json",
    ))
    errors.extend(validate_prompt_pack(REPO_ROOT / "config" / "condition_prompt_pack_v1.json"))
    errors.extend(validate_json_schema(
        REPO_ROOT / "review" / "golden_answers.json",
        REPO_ROOT / "schemas" / "golden_answers_schema.json",
    ))
    errors.extend(validate_calibration(
        REPO_ROOT / "review" / "golden_answers.json",
        args.min_calibration,
    ))

    if errors:
        print("Protocol bundle validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Protocol bundle validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
