# Source-Audited 50 Fixture

This directory is reserved for the Paper v1 source-audited 50-query gate.

Do not add synthetic fixture rows here.

Target files:

```text
source_audit_manifest_v0.jsonl
query_plan_v0.jsonl
experiment_fixture.jsonl
runtime_view.jsonl
evaluation_view.jsonl
warmup_queries.jsonl
```

The source-audit manifest must validate with:

```bash
.venv/bin/python scripts/validate_source_audit_manifest.py \
  fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --min-rows 50 \
  --allow-partial
```

Use `--require-pass` only for a strict all-audited bundle. Paper v1 may include
`partial` rows when they are deliberate partial/missing/contradictory evidence
cases.

The query plan and manifest must align before compilation:

```bash
.venv/bin/python scripts/validate_source_audited_query_plan.py \
  fixtures/source_audited_50/query_plan_v0.jsonl \
  --min-rows 50

.venv/bin/python scripts/sync_query_manifest.py \
  --manifest fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --query-plan fixtures/source_audited_50/query_plan_v0.jsonl
```

Compile after the manifest and query plan are ready:

```bash
.venv/bin/python scripts/compile_source_audited_fixture.py
.venv/bin/python scripts/check_source_audited_consistency.py \
  --expected-rows 50 \
  --require-explicit-warmup
```

Freeze the full source-audited bundle with:

```bash
.venv/bin/python scripts/freeze_manifest.py \
  --profile paper-v1-source-audited \
  --output manifests/protocol_v1_freeze_manifest.json
```

The audit scope is metadata-only. Do not download or commit images, browser
caches, or model artifacts.
