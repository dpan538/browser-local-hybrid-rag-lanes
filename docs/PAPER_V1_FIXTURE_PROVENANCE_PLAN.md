# Paper V1 Fixture Provenance Plan

Generated: 2026-06-12

This document defines the provenance layer for the Paper v1 source-audited
fixture. It starts the fixture/provenance phase without adding fake audited
records, downloading images, or changing the browser runtime.

## Goal

Build a source-audited fixture that can support Journal of Information Science
submission claims:

- source, rights, provenance, and image-state fields are traceable to public
  metadata;
- deterministic lanes preserve supplied evidence fields;
- evidence-to-output fidelity remains separate from evidence correctness;
- all audit decisions are reproducible from committed metadata references.

## Non-Goals

Do not:

- download model weights;
- download images;
- commit browser cache;
- touch archive product runtime logic;
- claim legal rights truth beyond source metadata;
- treat synthetic rows as source-audited evidence.

## Fixture Phases

### Phase 1: Source-Audited 50 Gate

Purpose:

- prove the source-audit workflow;
- produce a clean 50-query fixture with public-derived metadata;
- freeze rules and prompt pack before running Qwen/WebLLM.

Required target files:

```text
fixtures/source_audited_50/source_audit_manifest_v0.jsonl
fixtures/source_audited_50/experiment_fixture.jsonl
fixtures/source_audited_50/runtime_view.jsonl
fixtures/source_audited_50/evaluation_view.jsonl
fixtures/source_audited_50/warmup_queries.jsonl
```

### Phase 2: 100-Query Calibration

Purpose:

- test expansion authoring;
- calibrate the blind review form;
- avoid final claims.

### Phase 3: 200-Query JIS Candidate

Purpose:

- produce the first paper-facing Journal of Information Science package.

Target evidence:

```text
200 source-audited queries
600 condition outputs
automatic metrics on all outputs
human review on 180 blinded sampled outputs
```

### Phase 4: 300-Query Stronger Version

Purpose:

- produce a stronger JIS/revision package or OIR/AJIM stretch package.

## Source Audit Manifest

Every audited source record must have one row in:

```text
fixtures/source_audited_50/source_audit_manifest_v0.jsonl
```

The row schema is:

```text
schemas/source_audit_manifest_schema.json
```

The validator is:

```text
scripts/validate_source_audit_manifest.py
```

Run:

```bash
.venv/bin/python scripts/validate_source_audit_manifest.py \
  fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --min-rows 50 \
  --require-pass
```

## Audit Scope

The default audit scope is:

```text
metadata_only_no_image_download
```

This means:

- public metadata pages or APIs may be used;
- stable source URLs and metadata URLs must be recorded;
- fields copied into the fixture must be traceable to public metadata;
- images are not downloaded or committed;
- source correctness is limited to whether the metadata supports the fixture
  fields.

## Field-Level Audit

Each manifest row records field states for:

- `title`;
- `date_text`;
- `source`;
- `source_citation`;
- `rights_label`;
- `reuse_permission`;
- `public_domain_status`;
- `image_state_label`.

Allowed field states:

- `verified`;
- `missing`;
- `conflicting`;
- `not_applicable`.

The fixture compiler must not invent a value for a missing audited field. If a
field is required by a deterministic lane but absent in the public metadata,
the fixture should either use a placeholder or mark the row as partial/missing
evidence.

## Accepted Record Origins

Paper-facing source records may use:

- `source_audited`: manually checked against public metadata;
- `derived_from_public_source`: generated from public metadata with a
  reproducible transformation and then checked.

The Paper v1 fixture must not use:

- `synthetic`;
- `not_audited`.

Synthetic rows can remain in development fixtures only.

## Candidate Source Criteria

Candidate sources should provide:

- stable public record pages;
- machine-readable or clearly structured metadata;
- explicit source/provenance fields;
- explicit rights or reuse metadata where relevant;
- no requirement to download images for the audit.

Candidate source families should be recorded before row authoring begins.

## Promotion Gate

The source-audited 50 gate can pass only when:

- every manifest row validates against the schema;
- every measured fixture record maps to a manifest row;
- no paper-facing record has `record_origin=synthetic`;
- no paper-facing record has `source_audit_status=not_audited`;
- missing or conflicting fields are surfaced as partial/missing/contradictory
  evidence rather than inferred;
- the freeze manifest hashes the source audit manifest, fixture, rule table,
  prompt pack, schemas, and analysis scripts.
