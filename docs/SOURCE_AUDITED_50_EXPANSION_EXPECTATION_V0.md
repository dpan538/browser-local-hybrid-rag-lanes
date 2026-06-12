# Source-Audited 50 Expansion Expectation V0

Generated: 2026-06-12

This is the pre-run backup note for the next `source_audited_50` expansion
cycle. It records the intended experiment direction before adding more audited
rows.

## Starting State

The repository currently has:

- 5 source-audited LOC metadata rows;
- 5 matching query-plan rows;
- compiled experiment, runtime, and evaluation views;
- 1 explicit warmup row;
- passing manifest, query-plan, sync, compiler, consistency, protocol-bundle,
  and freeze-profile checks.

## Expansion Goal

The next cycle should expand toward 15 source-audited rows if validation stays
clean. The near-term target is not a paper-facing run yet; it is a controlled
authoring and validation exercise for the source-audited fixture pipeline.

Expected additions:

- additional LOC item-level metadata records, preferably single-item public
  health or WPA poster records with stable JSON metadata;
- at least one new lane stratum beyond source/rights exact delivery;
- more mixed/compound rows where deterministic rights/provenance are paired
  with bounded generative guidance;
- no downloaded images, no model weights, and no browser cache.

## Self-Audit Checks Before Expansion

Before adding rows, check the scripts for:

- deterministic-field coverage for source citations and provenance fields;
- query-plan semantics for mixed and compound rows;
- consistency checks for runtime/evaluation separation;
- freeze-profile coverage for any new executable artifact;
- validation behavior for partial, failed, and missing-record rows.

If a script loophole is found, patch and validate it before continuing row
authoring.

## Gate For Each Batch

Every batch must pass:

```bash
.venv/bin/python scripts/validate_source_audit_manifest.py \
  fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --min-rows <N> \
  --allow-partial

.venv/bin/python scripts/validate_source_audited_query_plan.py \
  fixtures/source_audited_50/query_plan_v0.jsonl \
  --min-rows <N>

.venv/bin/python scripts/sync_query_manifest.py \
  --manifest fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --query-plan fixtures/source_audited_50/query_plan_v0.jsonl

.venv/bin/python scripts/compile_source_audited_fixture.py --warmup-count 1

.venv/bin/python scripts/check_source_audited_consistency.py \
  --expected-rows <N> \
  --require-explicit-warmup
```

Use `--require-pass` when the batch intentionally contains only audited rows.
Use `--allow-partial` when the batch deliberately adds partial-evidence rows.

## Stop Conditions

Pause row expansion if:

- a source record lacks stable public metadata;
- rights or reuse fields require inference beyond source wording;
- the compiler changes rights/source/provenance wording unexpectedly;
- runtime views expose evaluator-only labels;
- validation can pass despite a known inconsistent manifest/query relation.

