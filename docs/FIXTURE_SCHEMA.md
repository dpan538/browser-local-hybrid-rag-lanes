# Fixture Schema

Generated: 2026-06-09

This document defines the first public-safe fixture format for the hybrid
answer-lane experiments. The fixture is intentionally small and synthetic or
source-auditable; it must not depend on private archive product state.

## Files

Planned fixture files:

- `fixtures/records.jsonl`
- `fixtures/queries.jsonl`
- `fixtures/labels.jsonl`

Draft files:

- `fixtures/drafts/mixed_intent_query_drafts.jsonl`
- `review/golden_answers.json`

Schemas:

- `schemas/fixture_record_schema.json`
- `schemas/fixture_query_schema.json`
- `schemas/fixture_label_schema.json`

## Record Object

Each record represents archive-like evidence, not model output.

Required concepts:

- stable `record_id`;
- descriptive metadata such as title, date, region, object type;
- source/provenance fields;
- rights/reuse fields;
- image-state fields;
- field-state checklist;
- source-audit status.

Important distinction:

The record can be syntactically valid while evidence correctness remains
`not_audited` or `uncertain`. Valid fixture shape does not imply source truth.

## Query Object

Each query represents a user task.

Required concepts:

- stable `query_id`;
- natural-language query text;
- `intent_label`;
- `primary_lane`;
- optional secondary lanes for mixed-intent rows;
- referenced records;
- user task features such as `rights`, `history`, `comparison`, or
  `recommendation`.

Mixed-intent rows must include:

- `mixed_intent=true`;
- a manually assigned `primary_lane`;
- at least one `secondary_lane`;
- `routing_ambiguity_notes`.

## Label Object

Each label defines the expected execution and review state for one query.

Required concepts:

- `query_id`;
- expected `evidence_state`;
- `field_state_checklist`;
- expected execution mode under each condition:
  - `all_generation`;
  - `hybrid_without_refusal`;
  - `full_hybrid`;
- refusal expectation;
- deterministic required fields;
- review focus.

Labels are not answers. They define what should be checked.

## Field-State Checklist

Every contract-bearing field can be assigned one of:

- `present_and_consistent`;
- `present_but_conflicting`;
- `absent`;
- `not_applicable`.

The checklist supports refusal and fallback decisions. It also prevents a
single vague "evidence is partial" label from hiding which field is missing or
conflicting.

Initial contract-bearing fields:

- `source`;
- `rights_label`;
- `rights_state`;
- `reuse_permission`;
- `public_domain_status`;
- `image_state_code`;
- `date_text`;
- `chronology_proof`;
- `comparison_corpus`;
- `research_context`.

## Evidence-State Aggregation

Use the following first-version aggregation:

| Evidence State | Checklist Basis |
|---|---|
| `sufficient` | Required fields for the user task are `present_and_consistent`. |
| `partial` | At least one relevant field is present, but one or more required fields are absent or indirect. |
| `missing` | No relevant evidence fields are present for the requested claim. |
| `contradictory` | Any required field is `present_but_conflicting`. |
| `not_applicable` | The missing field is not relevant to the requested task. |

If multiple states apply, use this precedence:

1. `contradictory`;
2. `missing`;
3. `partial`;
4. `sufficient`;
5. `not_applicable`.

## Calibration Examples

The 5-example calibration set should cover:

1. deterministic exact field rendering;
2. correct refusal;
3. over-refusal;
4. qualified answer instead of refusal;
5. compound deterministic plus generative answer.

These examples are not experiment results. They are reviewer calibration tools.

## Mixed-Intent Drafts

The first 10 mixed-intent drafts are used to test routing ambiguity before
building the full 50-query fixture. They should not be used alone to claim
deterministic lane success.
