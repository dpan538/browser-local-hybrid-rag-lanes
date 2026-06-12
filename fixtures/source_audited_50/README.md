# Source-Audited 50 Fixture

This directory is reserved for the Paper v1 source-audited 50-query gate.

Do not add synthetic fixture rows here.

Target files:

```text
source_audit_manifest_v0.jsonl
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
  --require-pass
```

The audit scope is metadata-only. Do not download or commit images, browser
caches, or model artifacts.
