# Source-Audited 50 26-To-50 Expansion Expectation V0

Generated: 2026-06-12

This note backs up the clean 26-query source-audited structural state before
continuing toward the 50-query Paper v1 fixture gate.

## Starting State

The current `fixtures/source_audited_50/` bundle contains:

- 26 query-plan rows;
- 18 source-audit manifest rows;
- 2 source families: `loc_metadata` and `wikimedia_commons_metadata`;
- 5 deterministic-refusal rows;
- 3 multi-record comparison rows;
- 1 explicit warmup row.

The 26-row bundle has passed manifest validation, query-plan validation,
manifest/query sync, source-audited compilation, source-audited consistency,
fixture validation, protocol-bundle validation, and freeze-profile generation.

## Next Expansion Target

The next expansion should move toward 50 rows while prioritizing structural
coverage over easy source/rights success cases:

- add at least one additional source family if reliable metadata is available;
- add partial-evidence rows with missing contract-bearing fields;
- add contradictory-evidence rows if public metadata supports a clear conflict;
- add more mixed-intent/compound rows combining deterministic fields with
  bounded generation;
- add more comparison and recommendation rows using multi-record evidence
  packets;
- keep all rows metadata-only and avoid image downloads.

## Stop Conditions

Stop and patch the toolchain before continuing if any of the following appear:

- a source family cannot be represented in `config/source_families.yaml`;
- a manifest row needs a field state not accepted by the schema;
- no-record or multi-record rows bypass source/manifest alignment checks;
- runtime views expose evaluator-only fields;
- a compiled row cannot pass `scripts/validate_fixture.py`;
- freeze-profile generation misses any source-audited bundle file.

## Expected Validation Before Next Post-Run Backup

```text
.venv/bin/python scripts/validate_source_audit_manifest.py fixtures/source_audited_50/source_audit_manifest_v0.jsonl --min-rows <N> --allow-partial
.venv/bin/python scripts/validate_source_audited_query_plan.py fixtures/source_audited_50/query_plan_v0.jsonl --min-rows <M>
.venv/bin/python scripts/sync_query_manifest.py --manifest fixtures/source_audited_50/source_audit_manifest_v0.jsonl --query-plan fixtures/source_audited_50/query_plan_v0.jsonl
.venv/bin/python scripts/compile_source_audited_fixture.py --warmup-count 1
.venv/bin/python scripts/check_source_audited_consistency.py --expected-rows <M> --require-explicit-warmup
.venv/bin/python scripts/validate_fixture.py fixtures/source_audited_50/experiment_fixture.jsonl
.venv/bin/python scripts/validate_protocol_bundle.py
.venv/bin/python scripts/freeze_manifest.py --profile paper-v1-source-audited --output /private/tmp/hybrid_lane_paper_v1_source_audited_freeze_manifest.json
git diff --check
```

## Boundary

This expansion is fixture/provenance work only. It should not run WebLLM/Qwen,
commit model weights, download image assets, or commit browser cache.
