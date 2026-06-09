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

## 2026-06-10: Codex browser pilot scaffold

Purpose:

- Add a preregistered 10-query browser pilot subset drawn from the 50-query
  draft runtime view.
- Extend the experiment panel so Codex in-app browser can run the subset across
  all three conditions and persist JSONL records through the local Flask API.
- Record the first browser-mediated stub run and its limitations.

Validation target before push:

- browser pilot subset validates against the runtime fixture view schema;
- Codex in-app browser panel reports 50 runtime rows and 10 pilot rows;
- browser pilot produces and saves 30 run records;
- saved run records validate against `schemas/run_record_schema.json`;
- paired analysis reports 10 paired queries for both contrasts;
- Python script compilation, blueprint validation, fixture validation, protocol
  bundle validation, and `git diff --check` pass.

Known limitations:

- The backend remains `stub`, so this is not a WebLLM/Qwen result.
- Raw browser pilot outputs remain ignored under `runs/`.
- The current browser pilot still uses synthetic, not source-audited records.

## 2026-06-10: preflight script hardening

Purpose:

- Patch script and panel loopholes before starting a real local-model smoke run.
- Prevent browser pilot saves from silently overwriting an existing run output.
- Validate saved run records at save time and fail analysis on duplicate
  `query_id + condition` rows.
- Improve browser environment flags so long-task data includes a per-request
  delta and backgrounding is not missed.

Validation target before push:

- Python script compilation passes;
- Flask save endpoint returns HTTP 200 for the first save and HTTP 409 for a
  duplicate run ID;
- existing browser pilot run records still validate against
  `schemas/run_record_schema.json`;
- analysis still works on the existing browser pilot record file;
- duplicate analysis records intentionally raise an error;
- protocol bundle validation and `git diff --check` pass.

Known limitations:

- This hardening does not implement the real WebLLM/Qwen backend.
- It improves pipeline integrity but does not change the synthetic fixture or
  source-audit limitation.

## 2026-06-10: model backend adapter probe

Purpose:

- Add a model-backend adapter layer so the experiment can move beyond `stub`
  without hard-coding model downloads or a specific runtime.
- Support an OpenAI-compatible local endpoint via environment variables.
- Add CLI and browser/API probe paths that must pass before a non-stub smoke
  run begins.
- Document the one-query smoke gate and the limits of adapter-level evidence.
- Superseded note: the following Qwen boundary correction reclassifies this
  endpoint path as comparison-only, not primary experiment infrastructure.

Validation target before push:

- Python script compilation passes;
- `scripts/probe_model_backend.py` succeeds with the default `stub` backend;
- `openai_compatible` without `HYBRID_LANE_MODEL_NAME` fails fast with an
  explicit configuration error;
- Flask test client `/api/model/probe` succeeds under `stub`;
- protocol bundle validation and `git diff --check` pass.

Known limitations:

- This does not start WebLLM, Ollama, LM Studio, or any model server.
- The adapter proves reachability and run-record compatibility only after an
  external local endpoint is already running.

## 2026-06-10: Qwen primary model boundary correction

Purpose:

- Correct the backend plan after confirming the archive research branch names
  `Qwen/Qwen3.5-0.8B` as the primary model identity.
- Preserve `onnx-community/Qwen3.5-0.8B-ONNX` as the product runtime artifact
  reference and `Qwen3.5-0.8B-q4f16_1-MLC` as the research WebLLM runtime id.
- Reclassify OpenAI-compatible server endpoints as comparison-only, not primary
  experiment infrastructure.
- Prevent accidental use of incidental local endpoints by requiring
  `HYBRID_LANE_ALLOW_COMPARISON_BACKEND=1` before the comparison adapter can
  run.

Validation target before push:

- Default stub probe still succeeds.
- OpenAI-compatible backend without the comparison flag fails fast with an
  explicit "comparison-only" error.
- Python script compilation passes.
- Protocol bundle validation and `git diff --check` pass.

Known limitations:

- This correction does not yet implement the browser WebLLM Qwen runner in the
  hybrid-lanes panel.
- The next experiment step must be a Codex in-app browser Qwen/WebLLM smoke run,
  not a server-side local endpoint run.

## 2026-06-10: Qwen WebLLM smoke panel scaffold

Purpose:

- Add a minimal Codex in-app browser panel for the primary Qwen/WebLLM smoke
  path.
- Pin the panel to `Qwen3.5-0.8B-q4f16_1-MLC`, matching the inherited
  browser-local RAG lab runtime id.
- Keep Flask in a serving/saving role only: fixture loading, prompt-pack
  delivery, and JSONL save.
- Build schema-compatible run records in the browser after Qwen/WebLLM
  generation or deterministic lane assembly.

Validation target before push:

- Python script compilation passes.
- Qwen smoke panel JavaScript passes `node --check`.
- Protocol bundle validation and `git diff --check` pass.
- Flask serves `/tools/qwen_webllm_smoke/`, `/api/prompt-pack`, runtime
  fixtures, and evaluation fixtures.
- Codex in-app browser loads the panel and WebGPU probe reports `available`.

Known limitations:

- The panel was verified without clicking `Load Qwen WebLLM`, so no model
  artifacts were downloaded during this scaffold validation.
- The first real smoke run still requires an intentional browser-side Qwen load
  and generated JSONL save.

## 2026-06-10: Qwen WebLLM 10-to-50 pre-run backup

Purpose:

- Back up the exact expectation before the first primary-model experiment.
- Declare that the experiment points Flask at
  `fixtures/drafts/runtime_view_v0.jsonl` and
  `fixtures/drafts/evaluation_view_v0.jsonl`, each with 50 rows.
- Add browser-panel batch controls for `Run First 10` and `Run First 50`.
- Define save paths, success criteria, and stop conditions before loading the
  Qwen WebLLM runtime.

Expected run IDs:

- `qwen_webllm_pilot10_v0`
- `qwen_webllm_scale50_v0`

Validation target before push:

- Python script compilation passes.
- Qwen smoke panel JavaScript passes `node --check`.
- Protocol bundle validation and `git diff --check` pass.

Known limitations:

- This backup does not include run outputs.
- Browser model artifacts may be downloaded/cached locally during the actual
  run, but they must not be committed.

## 2026-06-10: Qwen WebLLM 10-to-50 run summary and gate

Purpose:

- Summarize the completed primary Qwen/WebLLM pilot10 and scale50 runs without
  committing raw JSONL outputs.
- Record schema validation, Qwen invocation counts, deterministic skip counts,
  refusal-alignment failures, and latency distributions.
- Gate the result as method-analysis ready while blocking hard latency claims.

Key result:

- Scale50 saved 150 schema-valid rows.
- C1 had 15 contract failures, all `refusal_expected_alignment`.
- C2 had 15 contract failures, all `refusal_expected_alignment`.
- C3 had 0 contract failures.
- C3 reduced Qwen invocation from 50/50 rows in C1 to 27/50 rows.

Known limitations:

- Raw run outputs remain local under ignored `runs/`.
- Latency is exploratory because browser environment flags recorded long tasks
  and backgrounded rows.

## 2026-06-10: Qwen WebLLM diagnostics and instrumentation correction

Purpose:

- Slow the interpretation down after the first 10-to-50 run.
- Add a reusable diagnostics script for schema validity, Qwen invocation counts,
  deterministic skips, failure groups, latency summaries, and environment flags.
- Generate machine-readable and Markdown diagnostics from the ignored local run
  outputs without committing raw answers.
- Fix the browser panel's `long_task_gc` flag so future rows use per-row
  long-task delta instead of cumulative long-task presence.

Validation target before push:

- Qwen diagnostics script runs on pilot10 and scale50 outputs.
- Python script compilation passes.
- Qwen smoke panel JavaScript passes `node --check`.
- Protocol bundle validation and `git diff --check` pass.

Known limitations:

- Existing pilot10/scale50 records still carry the old cumulative
  `long_task_gc` behavior; this correction affects future runs only.
- The diagnostics report is for experiment triage, not a paper claim.
