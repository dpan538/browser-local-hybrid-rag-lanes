# Fixture Schema

Generated: 2026-06-09

This document defines the first public-safe fixture format for the hybrid
answer-lane experiments. The fixture is intentionally small and synthetic or
source-auditable; it must not depend on private archive product state.

## Canonical V1 Format

The canonical v1 fixture is a single self-contained JSONL file:

- `fixtures/experiment_fixture.jsonl`

Each line is one complete test case containing:

- `query`;
- `evidence_packet`;
- `expected_behavior`.

This avoids cross-file join errors between records, queries, and labels. It
also makes each row independently reproducible.

## Supporting Files

Draft and calibration files:

- `fixtures/drafts/mixed_intent_query_drafts.jsonl`
- `review/golden_answers.json`

Schemas:

- `schemas/experiment_fixture_schema.json`
- `schemas/golden_answers_schema.json`
- `schemas/fixture_record_schema.json`
- `schemas/fixture_query_schema.json`
- `schemas/fixture_label_schema.json`

The three separated fixture schemas are retained as normalized-reference
schemas. The first runnable experiment should use
`schemas/experiment_fixture_schema.json`.

## Experiment Fixture Row

Required top-level fields:

- `fixture_version`;
- `query_id`;
- `applicable_conditions`;
- `query`;
- `evidence_packet`;
- `expected_behavior`.

The current version is `1.0`.

## Query Object

Each query represents a user task.

Required concepts:

- natural-language text;
- `intent_label`;
- `primary_lane`;
- optional `secondary_lanes`;
- `mixed_intent`;
- `routing_ambiguity_notes`.

Mixed-intent rows must include:

- `mixed_intent=true`;
- `primary_lane="compound"` when the expected behavior is a compound answer;
- at least one `secondary_lane`;
- notes explaining why the router may be ambiguous.

## Evidence Packet

The evidence packet contains records and task-level evidence state.

Required concepts:

- `records`: the record subset for this query;
- `field_checklist`: the field-state checklist aggregated for the user task;
- `aggregated_evidence_state`: the result of applying the evidence aggregation
  rules;
- optional `retrieved_snippets`, for analyzing retrieval-stage evidence.

Record fields may include:

- `record_id`;
- `title`;
- `date_text`;
- `source`;
- `source_citation`;
- `source_name`;
- `source_domain`;
- `rights_label`;
- `rights_state`;
- `reuse_permission`;
- `public_domain_status`;
- `image_state_code`;
- `image_state_label`;
- `chronology_proof`;
- `source_audit_status`;
- `source_audit_notes`.

Important distinction:

The record can be syntactically valid while evidence correctness remains
`not_audited` or `uncertain`. Valid fixture shape does not imply source truth.

## Expected Behavior

Expected behavior is condition-specific:

- `condition_1_all_generation`;
- `condition_2_hybrid_no_refusal`;
- `condition_3_full_hybrid`.

Each condition can specify:

- `should_refuse`;
- `deterministic_fields_required`;
- `allowed_output_modes`;
- `compound_parts`;
- `expect_no_evidence`;
- `min_helpfulness_score`;
- `contract_compliance_required`.

For compound answers, use:

```json
"compound_parts": [
  { "part": "rights_and_permissions", "mode": "deterministic" },
  { "part": "historical_importance", "mode": "generative" }
]
```

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

Evidence-state aggregation depends on the intent-to-required-fields mapping in
`scripts/evidence_aggregator.py`.

Current mapping:

| Intent | Required Fields |
|---|---|
| `source/rights` | `source`, `rights_label`, `reuse_permission` |
| `refusal_required` | `chronology_proof`, `comparison_corpus` |
| `comparison` | `date_text`, `title` |
| `recommendation` | `research_context` |
| `explanation` | `image_state_label` |
| `mixed` | v1 defaults to sufficient; compound parts and review labels carry the ambiguity |

First-version aggregation:

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

The validation script checks whether `aggregated_evidence_state` matches the
computed state from the checklist and intent.

## Calibration Examples

The 5-example calibration set should cover:

1. deterministic exact field rendering;
2. correct refusal;
3. over-refusal;
4. qualified answer instead of refusal;
5. compound deterministic plus generative answer.

These examples are not experiment results. They are reviewer calibration tools.

`review/golden_answers.json` stores task-level ideal answers. They are not
condition-specific outputs.

## Mixed-Intent Drafts

The first 10 mixed-intent drafts are used to test routing ambiguity before
building the full 50-query fixture. They should not be used alone to claim
deterministic lane success.

## Validation

Install dependencies:

```bash
pip install -r requirements.txt
```

Validate the sample fixture:

```bash
python scripts/validate_fixture.py fixtures/experiment_fixture.jsonl
```

The validator checks:

- JSON Schema validity;
- evidence-state aggregation consistency;
- mixed-intent `secondary_lanes`;
- deterministic-refusal/intent compatibility;
- compound answer `compound_parts`;
- deterministic required fields against the field checklist.
