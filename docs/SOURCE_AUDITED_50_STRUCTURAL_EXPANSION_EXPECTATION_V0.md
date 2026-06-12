# Source-Audited 50 Structural Expansion Expectation V0

Generated: 2026-06-12

This is the pre-run backup note for the next expansion cycle after the 15-row
LOC metadata milestone. The goal is structural coverage, not simply adding more
successful source/rights rows.

## Starting State

The fixture currently has:

- 15 source-audited LOC manifest rows;
- 15 query-plan rows;
- 15 compiled fixture/runtime/evaluation rows;
- 1 explicit warmup row;
- source citation and image-state fields treated as contract-bearing
  deterministic fields.

## Expansion Goal

The next cycle should move toward 25-30 rows if validation stays clean.

Priority additions:

- no-evidence refusal rows with `allow_no_records=true`;
- first/earliest refusal rows where the available metadata cannot prove a
  superlative claim;
- comparison rows with multiple audited records;
- at least one second source family, preferably Wikimedia Commons or DPLA;
- continued metadata-only audit with no image downloads.

## Expected Script/Gate Work

Before and during row authoring, inspect and patch:

- compiler handling for no-record refusal rows;
- consistency checks for query-plan rows that deliberately have no manifest
  rows;
- comparison rows with multiple manifest IDs;
- deterministic-field expectations for comparison and compound rows;
- source-family diversity reporting.

## Batch Gate

Each expansion batch must pass:

```bash
.venv/bin/python scripts/validate_source_audit_manifest.py \
  fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --min-rows <manifest_N> \
  --allow-partial

.venv/bin/python scripts/validate_source_audited_query_plan.py \
  fixtures/source_audited_50/query_plan_v0.jsonl \
  --min-rows <query_N>

.venv/bin/python scripts/sync_query_manifest.py \
  --manifest fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --query-plan fixtures/source_audited_50/query_plan_v0.jsonl

.venv/bin/python scripts/compile_source_audited_fixture.py --warmup-count 1

.venv/bin/python scripts/check_source_audited_consistency.py \
  --expected-rows <query_N> \
  --require-explicit-warmup
```

This cycle may intentionally have more query-plan rows than manifest rows
because no-evidence refusal cases can have `allow_no_records=true`.

## Stop Conditions

Pause expansion if:

- no-record rows compile into accidental sufficient evidence;
- comparison rows silently drop one of their manifest records;
- a second source family requires image download to support key fields;
- rights statements require stronger legal interpretation than the source
  wording supports;
- runtime views expose evaluator-only fields.

