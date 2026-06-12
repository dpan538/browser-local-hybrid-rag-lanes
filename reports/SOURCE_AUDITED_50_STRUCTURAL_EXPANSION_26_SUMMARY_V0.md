# Source-Audited 50 Structural Expansion 26 Summary V0

Generated: 2026-06-12

This report records the post-run state after expanding
`fixtures/source_audited_50/` from the 15-row LOC-only batch to a 26-query
structural batch. The purpose of this step is fixture/provenance construction,
not a Qwen/WebLLM model run.

## Scope

The expansion adds structural coverage that was missing from the 15-row batch:

- no-evidence deterministic refusal rows;
- first/earliest deterministic refusal rows;
- multi-record comparison rows;
- a second source family using Wikimedia Commons file metadata;
- continued metadata-only audit with no image downloads.

## Artifact Counts

| Artifact | Count |
|---|---:|
| Source-audit manifest rows | 18 |
| Query-plan rows | 26 |
| Experiment fixture rows | 26 |
| Runtime-view rows | 26 |
| Evaluation-view rows | 26 |
| Warmup rows | 1 |

## Source Families

| Source family | Manifest rows | Notes |
|---|---:|---|
| `loc_metadata` | 15 | Library of Congress item-level metadata |
| `wikimedia_commons_metadata` | 3 | Wikimedia Commons file metadata via official API/file pages |

The Wikimedia Commons rows were authored from metadata fields only. No media
files were downloaded.

## Query Distribution

| Stratum | Query count |
|---|---:|
| `source_rights` | 5 |
| `mixed_intent` | 7 |
| `explanation` | 4 |
| `more_context` | 1 |
| `recommendation` | 1 |
| `no_evidence_refusal` | 3 |
| `first_earliest_refusal` | 2 |
| `comparison` | 3 |

| Primary lane | Query count |
|---|---:|
| `deterministic_exact` | 5 |
| `compound` | 7 |
| `generative` | 9 |
| `deterministic_refusal` | 5 |

| Evidence state | Query count |
|---|---:|
| `sufficient` | 21 |
| `missing` | 5 |

| Records per query | Query count |
|---|---:|
| 0 records | 3 |
| 1 record | 20 |
| 2 records | 3 |

## Added Rows

| Query range | Purpose |
|---|---|
| `q016`-`q018` | No-evidence refusal rows with `allow_no_records=true` |
| `q019`-`q020` | First/earliest refusal rows using a record but missing comparison corpus |
| `q021`-`q023` | Two-record comparison rows using existing LOC manifest records |
| `q024`-`q026` | Wikimedia Commons metadata rows for source/rights, mixed, and explanation lanes |

## Validation

The following checks passed before this summary was written:

```text
.venv/bin/python scripts/validate_source_audit_manifest.py fixtures/source_audited_50/source_audit_manifest_v0.jsonl --min-rows 18 --allow-partial
.venv/bin/python scripts/validate_source_audited_query_plan.py fixtures/source_audited_50/query_plan_v0.jsonl --min-rows 26
.venv/bin/python scripts/sync_query_manifest.py --manifest fixtures/source_audited_50/source_audit_manifest_v0.jsonl --query-plan fixtures/source_audited_50/query_plan_v0.jsonl
.venv/bin/python scripts/compile_source_audited_fixture.py --warmup-count 1
.venv/bin/python scripts/check_source_audited_consistency.py --expected-rows 26 --require-explicit-warmup
.venv/bin/python scripts/validate_fixture.py fixtures/source_audited_50/experiment_fixture.jsonl
```

Observed validation state:

- manifest validation: passed, 18 rows;
- query-plan validation: passed, 26 rows;
- manifest/query sync: passed;
- source-audited consistency: passed, 26 rows;
- experiment fixture validation: passed, 26 rows.

## Current Boundary

This is still an intermediate Paper v1 fixture-building milestone:

- it does not run Qwen/WebLLM;
- it does not support model-quality claims;
- it does not complete the 50-query source-audited gate;
- it does not claim legal rights correctness beyond metadata-level source audit;
- it does not download images, model weights, or browser cache.

The next expansion should continue from 26 toward 50 rows by adding additional
source families, partial/conflicting evidence states, and more mixed-intent
compound rows before any Paper v1 model run is promoted.
