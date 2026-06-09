# Research Push Log

This log records the purpose and validation state of main-branch pushes. It is
used as a human-readable backup description because research commits need more
context than a short subject line.

## 2026-06-09: `f491f81`

Subject:

`research: add protocol freeze experiment scaffold`

Purpose:

- Added the Flask experiment runner and Codex-browser panel.
- Added protocol-freeze documentation, prompt pack, run-record metadata, and
  automated pilot scripts.
- Split runtime-visible fixture data from evaluator-only labels.
- Added automatic contract checks, blinded review export, blinded review merge,
  freeze manifest generation, and paired exploratory analysis.

Validation reported at push time:

- protocol bundle validation passed;
- fixture validation passed;
- Python script compilation passed;
- Flask API smoke test passed;
- 3-condition smoke pilot passed;
- run-record schema validation passed;
- `git diff --check` passed.

Known limitations:

- The model backend was a timed stub, not real browser-local WebLLM/Qwen.
- The fixture remained a one-row smoke fixture.
- Generated smoke outputs were intentionally ignored rather than committed.

## 2026-06-10: `2b8a806`

Subject:

`research: add fixture blueprint compiler`

Purpose:

- Added a 50-query fixture expansion blueprint.
- Added seeded dev/eval split, blueprint schema, blueprint validator, compiler,
  draft runtime/evaluation views, and draft warmup set.
- Added rule-table label alignment for schema-level intent labels.
- Preserved the existing smoke fixture by writing the 50-row expansion under
  `fixtures/drafts/`.

Validation reported at push time:

- blueprint validation passed;
- compiled 50-row fixture passed `validate_fixture.py`;
- draft runtime and evaluation views each contained 50 rows;
- warmup set contained 5 rows;
- protocol bundle validation passed;
- `git diff --check` passed.

Known limitations:

- The draft fixture still used synthetic, not source-audited records.
- Query wording quality had not yet been audited at the time of push.

## 2026-06-10: query wording quality audit

Purpose:

- Add fixture quality audit tooling and report.
- Rewrite draft query templates so the 50-row compiled fixture has 50 unique
  user-facing query texts.
- Preserve synthetic/source-audit limitations as explicit promotion blockers.

Validation target before push:

- blueprint validation;
- compiled fixture validation;
- protocol bundle validation;
- Python script compilation;
- fixture quality audit regeneration;
- `git diff --check`.

## 2026-06-10: promotion gate candidate

Purpose:

- Add a scripted promotion gate that distinguishes exploratory synthetic-fixture
  promotion from paper-facing source-audited promotion.
- Keep the remaining synthetic/not-audited limitation explicit instead of
  hiding it in the quality audit.
- Document source-audit requirements for future evidence-correctness claims.

Expected validation before push:

- exploratory promotion gate passes;
- paper promotion gate fails for the expected source-audit reason;
- Python script compilation passes;
- `git diff --check` passes.

## 2026-06-10: exploratory 50-query stub dry run

Purpose:

- Run the first full 50-query x 3-condition dry run through the Flask
  experiment API.
- Confirm that the draft runtime view, pilot runner, automatic contract checker,
  analysis script, and blind-pack exporter work together without manual answer
  pasting.
- Preserve the result as an exploratory report while keeping raw run records
  ignored.

Validation target before push:

- 150 run records validate against `schemas/run_record_schema.json`;
- analysis reports 50 paired queries for each condition contrast;
- full-hybrid has zero automatic contract failures in the stub dry run;
- Python script compilation passes;
- blueprint, fixture, protocol-bundle, and promotion-gate checks pass;
- `git diff --check` passes.

Known limitations:

- The run used the timed `stub` backend, not WebLLM/Qwen.
- The 50-row draft fixture remains synthetic and not source-audited.
- The dry run is a pipeline validation result, not a paper-facing model result.
