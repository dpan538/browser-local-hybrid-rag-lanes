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

Each audited field uses the same object shape:

```json
{
  "state": "verified",
  "value": "Public Domain Mark 1.0",
  "evidence_note": "Stated in the public metadata rights field."
}
```

`source_audit_status` has three values:

- `audited`: all applicable fields are verified or not applicable;
- `partial`: at least one applicable field is missing or uncertain, but the
  row may still support a partial-evidence fixture case;
- `failed`: the row must not be promoted into a paper-facing fixture.

The validator is:

```text
scripts/validate_source_audit_manifest.py
```

Run a strict all-audited gate when every row is expected to have complete
metadata:

```bash
.venv/bin/python scripts/validate_source_audit_manifest.py \
  fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --min-rows 50 \
  --require-pass
```

Run a partial-evidence gate when rows intentionally test missing or incomplete
metadata:

```bash
.venv/bin/python scripts/validate_source_audit_manifest.py \
  fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --min-rows 50 \
  --allow-partial
```

Rows marked `source_audit_status=failed` are always rejected by validation and
compilation. They may remain in scratch files only, not in a Paper v1 manifest.

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

`image_state_label` is metadata-only. It means the source metadata describes
the image as one of:

- `image_public_domain`;
- `image_restricted`;
- `image_copyrighted`;
- `image_rights_unknown`;
- `no_image_available`;
- `metadata_only_not_applicable`.

It does not mean the image file was downloaded or visually inspected.

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

The source family registry is:

```text
config/source_families.yaml
```

The manifest validator checks that each `source_family_id` exists in that
registry.

## Query Plan And Compilation

The source audit manifest records public metadata. Query wording and lane
intent belong in a separate query plan:

```text
fixtures/source_audited_50/query_plan_v0.jsonl
schemas/source_audited_query_plan_schema.json
```

Each query-plan row binds source metadata to an executable test case. Required
fields include:

- `query_id`: joined to manifest rows by `query_id`, unless explicit
  `manifest_ids` are listed;
- `question_text`: the user-visible query;
- `stratum`: the sampling stratum;
- `intent_label`, `primary_lane`, and optional `secondary_lanes`;
- `lane_intent`: one or more of `source`, `rights`, `provenance`,
  `research_guidance`, or `refusal`;
- `decisive_fields`: the fields used to aggregate evidence state;
- `refusal_policy`: `matrix`, `always`, or `never`;
- `warmup`: true only for rows deliberately excluded from measurement;
- optional `evidence_state_override` for mixed-intent rows where the task-level
  evidence state differs from simple field aggregation.

Validate the query plan and manifest/query alignment before compilation:

```bash
.venv/bin/python scripts/validate_source_audited_query_plan.py \
  fixtures/source_audited_50/query_plan_v0.jsonl \
  --min-rows 50

.venv/bin/python scripts/sync_query_manifest.py \
  --manifest fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --query-plan fixtures/source_audited_50/query_plan_v0.jsonl
```

Compile source-audited artifacts with:

```bash
.venv/bin/python scripts/compile_source_audited_fixture.py \
  --manifest fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --query-plan fixtures/source_audited_50/query_plan_v0.jsonl \
  --output fixtures/source_audited_50/experiment_fixture.jsonl \
  --runtime-output fixtures/source_audited_50/runtime_view.jsonl \
  --evaluation-output fixtures/source_audited_50/evaluation_view.jsonl \
  --warmup-output fixtures/source_audited_50/warmup_queries.jsonl
```

The compiler maps field states as follows:

| Source audit state | Fixture field checklist state | Runtime behavior |
|---|---|---|
| `verified` | `present_and_consistent` | render value if lane requires it |
| `missing` | `absent` | omit optional field; deterministic renderer falls back to placeholder |
| `conflicting` | `present_but_conflicting` | mark aggregate evidence as contradictory |
| `not_applicable` | `not_applicable` | ignore for task evidence state |

`refusal_expected` is derived from `refusal_policy` in the query plan and
`config/refusal_decision_matrix.csv`, rather than typed manually into the
source audit manifest.

After compilation, run:

```bash
.venv/bin/python scripts/check_source_audited_consistency.py \
  --expected-rows 50 \
  --require-explicit-warmup
```

For a Paper v1 freeze, generate:

```bash
.venv/bin/python scripts/freeze_manifest.py \
  --profile paper-v1-source-audited \
  --output manifests/protocol_v1_freeze_manifest.json
```

The `paper-v1-source-audited` profile is defined in:

```text
config/freeze_profiles.yaml
```

The profile must include the source audit manifest, query plan, compiled
fixture, runtime/evaluation views, warmup rows, source-family registry, schemas,
rules, prompt pack, review instructions, and analysis scripts.

For blind semantic review after a run, generate a condition-hidden pack with:

```bash
.venv/bin/python scripts/generate_blind_pack.py \
  --records runs/paper_v1_qwen_webllm_50_clean/records.jsonl \
  --output review/paper_v1_blind_pack.json \
  --mapping review/paper_v1_blind_mapping.json
```

A one-row smoke exercise of the source-audited compiler is available at:

```bash
.venv/bin/python scripts/smoke_source_audited_compile.py
```

## Promotion Gate

The source-audited 50 gate can pass only when:

- every manifest row validates against the schema;
- every measured fixture record maps to a manifest row;
- no paper-facing record has `record_origin=synthetic`;
- no paper-facing record has `source_audit_status=not_audited` or
  `source_audit_status=failed`;
- `partial` rows are allowed only when the row's aggregated evidence state is
  `partial`, `missing`, or `contradictory`;
- missing or conflicting fields are surfaced as partial/missing/contradictory
  evidence rather than inferred;
- the freeze manifest hashes the source audit manifest, fixture, rule table,
  prompt pack, schemas, and analysis scripts.
