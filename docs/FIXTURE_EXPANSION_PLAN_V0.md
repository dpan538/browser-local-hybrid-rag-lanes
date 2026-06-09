# Fixture Expansion Plan V0

Generated: 2026-06-09

This plan expands the current one-row smoke fixture into a 50-query exploratory
fixture without changing the protocol. The next milestone is a blueprint, not a
paper-facing dataset: every row must still be reviewed before it becomes part of
`fixtures/experiment_fixture.jsonl`.

## Goal

Create a stratified query set that can test hybrid answer-lane allocation:

- deterministic evidence-field delivery;
- deterministic insufficient-evidence refusal;
- bounded generative research guidance;
- compound deterministic-plus-generative answers;
- routing ambiguity in mixed-intent questions.

The expanded fixture remains exploratory until the rule table, prompt pack,
runtime/evaluation views, and analysis plan are frozen with a no-missing
manifest.

## Strata And Quotas

| Stratum | Count | Primary purpose |
|---|---:|---|
| `source_rights` | 8 | Exact source, rights, reuse, public-domain, and image-state field delivery. |
| `no_evidence_refusal` | 6 | Missing evidence should trigger refusal or bounded non-answer. |
| `first_earliest_refusal` | 5 | First/earliest claims require chronology proof and comparison corpus evidence. |
| `comparison` | 6 | Bounded generative comparison over supplied records. |
| `recommendation` | 5 | Region/period or next-source research guidance. |
| `explanation` | 5 | Current-object explanation with evidence-bound interpretation. |
| `more_context` | 5 | More-context requests where source pointers and guidance interact. |
| `mixed_intent` | 10 | Compound deterministic fields plus generated guidance, or refusal plus guidance. |

Total: 50 measured queries.

Warmup rows are separate and must not be sampled from the measured 50.

## Blueprint Contract

The blueprint is a declarative authoring format. Each row must contain:

- `query_id`, `role`, `stratum`, and `query_text`;
- `intent_label`, `primary_lane`, and optional `secondary_lanes`;
- `evidence_state`, `decisive_fields`, `refusal_expected`, and
  `conflict_expected`;
- `source_audit_status`, `record_origin`, and `audit_caveat`;
- `deterministic_fields` used by the compiler to create synthetic records.

The schema is `schemas/fixture_blueprint_schema.json`.

Validate the blueprint:

```bash
.venv/bin/python scripts/validate_blueprint.py
```

## Development And Evaluation Split

Use a pre-declared, seeded split before authoring final records:

- 15 development rows for rule-table sanity checks and reviewer calibration
  examples;
- 35 evaluation rows for reported pilot results.

The split seed lives in `fixtures/drafts/query_strata_v0.json`. Apply it with:

```bash
.venv/bin/python scripts/finalize_blueprint_split.py
```

The development rows are allowed to inform rule/debug fixes. Evaluation rows
must not be used to tune the rule table after freeze.

The blueprint marks each row as `dev` or `eval`. When the fixture is compiled,
the split should remain visible in evaluation metadata but not used by the
runtime router.

## Evidence-State Targets

The 50-query blueprint should include:

- sufficient evidence rows for deterministic rendering and bounded generation;
- partial evidence rows for qualified answers;
- missing evidence rows for refusal tests;
- contradictory evidence rows for conflict surfacing;
- not-applicable fields where absence of irrelevant fields must not trigger
  refusal.

Do not let `mixed_intent` rows default to `sufficient`. Each mixed row must list
its decisive fields.

## Source-Audit Policy

Synthetic or fixture-authored source fields can test evidence-to-output
fidelity. They cannot establish evidence correctness. Each row must carry:

- `source_audit_status`;
- `record_origin`;
- any source-audit caveat needed for paper reporting.

Source-audit failures are reported separately from deterministic rendering
failures.

## Promotion Path

1. Generate or update `fixtures/drafts/fixture_expansion_blueprint_v0.jsonl`.
2. Validate the blueprint with `scripts/validate_blueprint.py`.
3. Compile draft fixtures with `scripts/compile_blueprint.py`.
4. Review the compiled draft fixture and warmup set.
5. Promote the compiled fixture only after review.
6. Validate the promoted master fixture.
7. Split runtime and evaluation views.
8. Validate the protocol bundle.
9. Freeze artifacts before any paper-facing run.

Compile the current draft:

```bash
.venv/bin/python scripts/compile_blueprint.py
```

Default draft outputs:

- `fixtures/drafts/compiled_experiment_fixture_v0.jsonl`
- `fixtures/drafts/runtime_view_v0.jsonl`
- `fixtures/drafts/evaluation_view_v0.jsonl`
- `fixtures/drafts/warmup_set_v0.json`
- `fixtures/drafts/warmup_queries_v0.jsonl`

These draft outputs do not replace the current smoke fixture.

## Non-Goals

This expansion does not introduce:

- real model weights;
- downloaded images;
- archive product runtime logic;
- learned routing;
- legal reuse determination.
