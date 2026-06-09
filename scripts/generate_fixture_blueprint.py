#!/usr/bin/env python3
"""Generate a 50-query fixture expansion blueprint from stratum quotas."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


QUESTION_TEMPLATES = {
    "source_rights": [
        "What source and rights fields are available for this record?",
        "Can you show the reuse and public-domain status for this item?",
        "What does the evidence say about rights and image-state caveats?",
        "List the exact source URL, rights label, and reuse caveat for this record.",
        "Which metadata fields tell me whether this item can be reused?",
        "Show the rights statement without rephrasing it into permission advice.",
        "What source pointer and public-domain status are supplied for this object?",
        "Separate the archive source field from the rights and image-state fields.",
    ],
    "no_evidence_refusal": [
        "What can you conclude about this claim from the available evidence?",
        "Can you answer this unsupported historical claim?",
        "Is there enough evidence here to make the requested assertion?",
        "Does the evidence packet support this interpretation, or should you decline it?",
        "Can you make a substantive claim if the relevant fields are absent?",
        "What should the system say when no source evidence is available for the question?",
    ],
    "first_earliest_refusal": [
        "Is this the first or earliest example in the archive?",
        "Can we say this is the earliest known record for the topic?",
        "Does this record prove a first occurrence claim?",
        "Is one dated record enough to call this the earliest campaign example?",
        "Can you verify a first-known claim without a comparison corpus?",
    ],
    "comparison": [
        "How do these records compare based on the supplied evidence?",
        "What differences are visible between the two campaign records?",
        "Compare these items without adding unsupported context.",
        "Which similarities and differences are supported by the metadata for these records?",
        "Can you contrast the two records while keeping uncertain fields caveated?",
        "What comparison is justified by the titles, dates, and context fields alone?",
    ],
    "recommendation": [
        "Which source should I inspect next for this region and period?",
        "What would be a useful next research step from these records?",
        "Which evidence-backed direction should I follow next?",
        "What archive lead should I pursue next, given only these fields?",
        "Which next source would help me narrow the regional context?",
    ],
    "explanation": [
        "Explain what is known about this object from the supplied evidence.",
        "What can this record tell me about the public-health campaign context?",
        "Give a bounded explanation of this item using only the evidence.",
        "Summarize this object while keeping interpretation separate from metadata.",
        "What cautious explanation can be made from the title, date, and image-state fields?",
    ],
    "more_context": [
        "What additional context should I seek for this object?",
        "Which related source or field would help me understand this record better?",
        "What context is missing, and what can still be said from the evidence?",
        "What follow-up evidence would make this record easier to interpret?",
        "Which missing context should be named before making a stronger claim?",
    ],
    "mixed_intent": [
        "What are the rights for this record, and why might it matter historically?",
        "Can I reuse this image, and what related records should I compare?",
        "Separate the exact source and rights fields from your interpretation.",
        "Give me the source and reuse caveat, then suggest how to discuss the item in a caption.",
        "Does the rights label prove public-domain reuse, and what research context is still useful?",
        "Show the deterministic metadata first, then explain what can be cautiously inferred.",
        "If the evidence is incomplete, what should be refused and what guidance can still help?",
        "Which fields should be copied exactly, and which parts need generated research guidance?",
        "Can you provide citation details while also explaining why this record belongs in a comparison?",
        "What are the image-state caveats, and how should I frame the object in a study note?",
    ],
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def state_for(stratum: Dict[str, Any], index: int) -> str:
    states = stratum["target_evidence_states"]
    return states[index % len(states)]


def split_for(global_index: int, dev_count: int) -> str:
    return "dev" if global_index <= dev_count else "eval"


def split_assignments(slot_keys: List[str], dev_count: int, seed: str) -> Dict[str, str]:
    ranked = sorted(
        slot_keys,
        key=lambda key: hashlib.sha256(f"{seed}:{key}".encode("utf-8")).hexdigest(),
    )
    dev_keys = set(ranked[:dev_count])
    return {key: "dev" if key in dev_keys else "eval" for key in slot_keys}


def templates_for(stratum_name: str) -> List[str]:
    return QUESTION_TEMPLATES.get(stratum_name, ["Draft query placeholder."])


def iter_blueprint_rows(config: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    global_index = 0
    dev_count = int(config["dev_count"])
    slot_keys = [
        f"{stratum['name']}:{local_index}"
        for stratum in config["strata"]
        for local_index in range(1, int(stratum["count"]) + 1)
    ]
    role_by_slot = split_assignments(
        slot_keys,
        dev_count,
        str(config.get("split_seed", "fixture-blueprint-v0")),
    )
    for stratum in config["strata"]:
        templates = templates_for(stratum["name"])
        for local_index in range(1, int(stratum["count"]) + 1):
            global_index += 1
            slot_key = f"{stratum['name']}:{local_index}"
            query_id = f"q{global_index:03d}"
            template = templates[(local_index - 1) % len(templates)]
            evidence_state = state_for(stratum, local_index - 1)
            refusal_expected = (
                stratum["primary_lane"] == "deterministic_refusal"
                or evidence_state in {"missing", "contradictory"}
            )
            row = {
                "blueprint_version": config["version"],
                "status": "draft_slot_not_fixture_row",
                "query_id": query_id,
                "role": role_by_slot[slot_key],
                "stratum": stratum["name"],
                "query_text": template,
                "intent_label": stratum["intent_label"],
                "primary_lane": stratum["primary_lane"],
                "mixed_intent": stratum["name"] == "mixed_intent",
                "evidence_state": evidence_state,
                "decisive_fields": stratum["decisive_fields"],
                "record_count_target": 2 if stratum["name"] in {"comparison", "mixed_intent"} else 1,
                "refusal_expected": refusal_expected,
                "conflict_expected": evidence_state == "contradictory",
                "source_audit_status": "not_audited",
                "record_origin": "synthetic",
                "audit_caveat": "Synthetic blueprint row; not source-audited.",
                "deterministic_fields": {
                    "source": f"https://example.org/archive/{query_id}",
                    "rights_label": "Fixture rights label; source audit required",
                    "reuse_permission": "source verification required before reuse",
                    "public_domain_status": "not independently determined",
                    "image_state_label": "metadata-only; image not downloaded",
                    "source_citation": f"Synthetic fixture source, record {query_id}",
                },
                "authoring_notes": "Fill evidence_packet, field_checklist, source_audit_status, and expected_behavior before promotion.",
            }
            if row["mixed_intent"]:
                row["secondary_lanes"] = ["deterministic_exact", "generative"]
            yield row


def write_jsonl(rows: Iterable[Dict[str, Any]], path: Path) -> int:
    count = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="fixtures/drafts/query_strata_v0.json")
    parser.add_argument(
        "--output",
        default="fixtures/drafts/fixture_expansion_blueprint_v0.jsonl",
    )
    args = parser.parse_args()

    config = load_json(Path(args.config))
    rows = list(iter_blueprint_rows(config))
    expected = int(config["total_measured_queries"])
    if len(rows) != expected:
        raise ValueError(f"generated {len(rows)} rows; expected {expected}")
    count = write_jsonl(rows, Path(args.output))
    print(f"Wrote {count} blueprint rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
