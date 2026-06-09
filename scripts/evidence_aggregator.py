#!/usr/bin/env python3
"""Evidence-state aggregation helpers for hybrid lane fixtures."""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional


class FieldState(str, Enum):
    PRESENT_CONSISTENT = "present_and_consistent"
    PRESENT_CONFLICTING = "present_but_conflicting"
    ABSENT = "absent"
    NOT_APPLICABLE = "not_applicable"


class EvidenceState(str, Enum):
    SUFFICIENT = "sufficient"
    PARTIAL = "partial"
    MISSING = "missing"
    CONTRADICTORY = "contradictory"
    NOT_APPLICABLE = "not_applicable"


INTENT_REQUIRED_FIELDS: Dict[str, List[str]] = {
    "source/rights": ["source", "rights_label", "reuse_permission"],
    "refusal_required": ["chronology_proof", "comparison_corpus"],
    "comparison": ["date_text", "title"],
    "recommendation": ["research_context"],
    "explanation": ["image_state_label"],
    # Mixed rows are validated through primary_lane and compound_parts. The
    # fixture author must provide row-level decisive_fields; mixed should not
    # silently default to sufficient.
    "mixed": [],
}


def aggregate_evidence_state(
    field_checklist: Dict[str, str],
    intent_label: str,
    decisive_fields: Optional[List[str]] = None,
) -> str:
    """Compute an aggregate evidence state from a field checklist and intent.

    Precedence:
    contradictory > missing > partial > sufficient.

    Row-level decisive_fields override the intent-level default mapping. This
    is required for mixed-intent rows so that they do not default to sufficient
    without an explicit evidence basis.
    """
    required = (
        list(decisive_fields)
        if decisive_fields is not None
        else INTENT_REQUIRED_FIELDS.get(intent_label, [])
    )
    if not required:
        return EvidenceState.NOT_APPLICABLE.value

    states = [
        field_checklist.get(field, FieldState.ABSENT.value)
        for field in required
    ]
    applicable_states = [
        state for state in states if state != FieldState.NOT_APPLICABLE.value
    ]

    if not applicable_states:
        return EvidenceState.NOT_APPLICABLE.value

    if FieldState.PRESENT_CONFLICTING.value in applicable_states:
        return EvidenceState.CONTRADICTORY.value
    if all(state == FieldState.ABSENT.value for state in applicable_states):
        return EvidenceState.MISSING.value
    if any(state == FieldState.ABSENT.value for state in applicable_states):
        return EvidenceState.PARTIAL.value
    if all(
        state == FieldState.PRESENT_CONSISTENT.value
        for state in applicable_states
    ):
        return EvidenceState.SUFFICIENT.value
    return EvidenceState.PARTIAL.value


if __name__ == "__main__":
    example = {
        "source": "present_and_consistent",
        "rights_label": "present_and_consistent",
        "reuse_permission": "absent",
    }
    print(aggregate_evidence_state(example, "source/rights"))
