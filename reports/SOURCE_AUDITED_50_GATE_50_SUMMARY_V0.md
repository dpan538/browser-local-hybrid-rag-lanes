# Source-Audited 50 Gate Summary V0

Generated: 2026-06-12

This report records the first mechanically complete 50-query
`fixtures/source_audited_50/` gate. It is a fixture/provenance milestone, not a
Qwen/WebLLM model run.

## Scope

The gate now contains 50 query rows compiled from 23 metadata-audited source
records across three source families. Some source records are reused across
comparison, recommendation, and mixed-intent rows so the unit of the gate is the
query, not a one-record-per-query manifest.

No images, model weights, or browser cache artifacts were downloaded or
committed.

## Artifact Counts

| Artifact | Count |
|---|---:|
| Source-audit manifest rows | 23 |
| Query-plan rows | 50 |
| Experiment fixture rows | 50 |
| Runtime-view rows | 50 |
| Evaluation-view rows | 50 |
| Warmup rows | 1 |

## Source Families

| Source family | Manifest rows | Audit status |
|---|---:|---|
| `loc_metadata` | 15 | audited |
| `wikimedia_commons_metadata` | 3 | audited |
| `museum_metadata` | 5 | partial |

The `museum_metadata` rows use official Metropolitan Museum of Art Collection
API metadata. They are deliberately marked `partial` because the API records
used here expose title/date/source/object URL fields but do not provide a
license label or reuse permission.

## Query Distribution

| Stratum | Query count |
|---|---:|
| `source_rights` | 10 |
| `mixed_intent` | 11 |
| `explanation` | 6 |
| `more_context` | 2 |
| `recommendation` | 4 |
| `no_evidence_refusal` | 6 |
| `first_earliest_refusal` | 4 |
| `comparison` | 7 |

| Primary lane | Query count |
|---|---:|
| `deterministic_exact` | 10 |
| `compound` | 11 |
| `generative` | 19 |
| `deterministic_refusal` | 10 |

| Evidence state | Query count |
|---|---:|
| `sufficient` | 32 |
| `missing` | 10 |
| `partial` | 8 |

| Records per query | Query count |
|---|---:|
| 0 records | 6 |
| 1 record | 36 |
| 2 records | 8 |

The 10 `missing` evidence rows are deterministic-refusal rows. The 8 `partial`
evidence rows are primarily rights/reuse queries over Met metadata where source
and citation are present but reuse fields are absent.

## Toolchain Correction

During this expansion, the consistency checker was tightened from a
record-level rule to a field-level rule:

- before: any `partial` source-audit record could not produce a query-level
  `sufficient` evidence state;
- after: a `partial` source-audit record is allowed to support a query-level
  `sufficient` state when the missing/conflicting fields are not decisive for
  that query.

This matters because the Met records are partial for rights/reuse, but still
provide sufficient title/date/source-citation evidence for some explanation and
comparison rows.

## Validation

The following checks passed:

```text
.venv/bin/python scripts/validate_source_audit_manifest.py fixtures/source_audited_50/source_audit_manifest_v0.jsonl --min-rows 23 --allow-partial
.venv/bin/python scripts/validate_source_audited_query_plan.py fixtures/source_audited_50/query_plan_v0.jsonl --min-rows 50
.venv/bin/python scripts/sync_query_manifest.py --manifest fixtures/source_audited_50/source_audit_manifest_v0.jsonl --query-plan fixtures/source_audited_50/query_plan_v0.jsonl
.venv/bin/python scripts/compile_source_audited_fixture.py --warmup-count 1
.venv/bin/python scripts/check_source_audited_consistency.py --expected-rows 50 --require-explicit-warmup
.venv/bin/python scripts/validate_fixture.py fixtures/source_audited_50/experiment_fixture.jsonl
```

## Current Boundary

This gate is mechanically ready for the next Paper v1 preparation step, but it
is not yet a paper-facing model result:

- no Qwen/WebLLM run has been executed on this source-audited fixture;
- no formal freeze manifest has been committed for this exact run bundle;
- no automatic contract metrics or blinded semantic review exist for this
  source-audited gate;
- rights statements remain metadata-level source claims, not legal advice.

The next step is to run the full protocol-bundle/freeze checks, then perform a
clean browser-local Qwen/WebLLM run against this 50-query source-audited
runtime view.
