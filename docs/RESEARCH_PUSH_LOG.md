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

## 2026-06-10: Qwen WebLLM cleaner20 pre-run backup

Purpose:

- Back up a cleaner 20-query instrumentation rerun before starting it.
- Use the same primary Qwen/WebLLM path but keep the Codex in-app browser
  visible and foregrounded during execution.
- Test the corrected row-delta `long_task_gc` behavior.
- Allow custom batch runs to preserve the entered run id, so the run can be
  saved as `qwen_webllm_cleaner20_v0`.

Expected output:

```text
runs/qwen_webllm_cleaner20_v0/qwen_webllm_cleaner20_v0_records.jsonl
```

Validation target before push:

- Qwen smoke panel JavaScript passes `node --check`.
- Python diagnostics script compilation passes.
- Protocol bundle validation and `git diff --check` pass.

Known limitations:

- This backup does not include cleaner20 outputs.
- Cleaner20 is an instrumentation check, not a paper finding.

## 2026-06-10: Qwen WebLLM cleaner20 diagnostics and cleaner50 pre-run backup

Purpose:

- Record the completed cleaner20 run as a diagnostics artifact while keeping
  raw run records ignored under `runs/`.
- Confirm that the corrected row-delta `long_task_gc` instrumentation and
  foregrounded Codex browser path produced cleaner environment flags.
- Back up the cleaner50 expectation before starting the full 50-query rerun.

Cleaner20 diagnostic result:

- 60 run records: 20 queries across 3 conditions.
- Schema errors: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 3.
- Failure groups remain concentrated on `refusal_expected_alignment`, which is
  useful for ablation triage but not yet a paper finding.

Cleaner50 expected output:

```text
runs/qwen_webllm_cleaner50_v0/qwen_webllm_cleaner50_v0_records.jsonl
reports/QWEN_WEBLLM_CLEANER50_DIAGNOSTICS_V0.md
reports/qwen_webllm_cleaner50_diagnostics_v0.json
```

Known limitations:

- Cleaner20 and cleaner50 are still instrumentation and pipeline checks.
- Raw Qwen/WebLLM answers are not committed.
- No claim is made yet about user-facing usability or source-audited semantic
  correctness.

## 2026-06-10: Cleaner50 interruption recovery hardening

Purpose:

- Fix the long-batch failure mode observed when cleaner50 was interrupted
  before final save.
- Add per-query checkpoint saves during Qwen/WebLLM batch execution, preserving
  completed records if Codex, the browser, or WebGPU exits mid-run.
- Keep final output under the same run id by intentionally overwriting the
  latest checkpoint when the batch completes.
- Align Flask environment flags with the frontend by treating `long_task_gc` as
  a per-row delta signal only.

Expected effect:

- A restarted cleaner50 run should produce incremental files under
  `runs/qwen_webllm_cleaner50_v0/` before the final 150-row output.
- If a later query stalls, the partial checkpoint can be diagnosed rather than
  discarded.

Known limitations:

- Checkpointing does not solve an underlying WebGPU generation stall; it only
  prevents complete data loss.
- Raw run records remain ignored and are not committed.

## 2026-06-10: Cleaner50 stalled partial diagnostics

Purpose:

- Record the checkpointed cleaner50 rerun honestly as a stalled partial run.
- Preserve diagnostics for the 60 schema-valid rows saved through q020.
- Avoid claiming a completed 50-query scale result when q021
  `hybrid_without_refusal` stalled in WebLLM streaming generation.

Observed result:

- Saved checkpoint rows: 60.
- Completed queries: q001-q020.
- Schema errors: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 1.
- q021 `all_generation` completed in-page, but the batch stalled before q021
  `hybrid_without_refusal` produced a record.
- After reloading, WebGPU probe also stalled in both the original tab and a new
  tab, so the in-app browser session was treated as contaminated.

Next experimental step:

- Restart the browser/WebGPU session, then run a focused q021/q022 triage before
  attempting another full cleaner50.
- Treat this as a scale-blocker diagnosis, not as a condition-level finding.

## 2026-06-10: Q021 triage timeout hardening pre-run backup

Purpose:

- Add a generation timeout control to the Qwen/WebLLM panel.
- Convert WebLLM streaming stalls into explicit run records with
  `generation_error` metadata, rather than freezing the whole batch.
- Back up the q021 focused triage expectation before rerunning after a clean
  browser/WebGPU restart.

Expected first run:

```text
run_id: qwen_webllm_q021_triage_v0
query: q021
condition: hybrid_without_refusal
generation_timeout_ms: 120000
```

Known limitations:

- A timeout record is pipeline evidence, not model-quality evidence.
- If WebGPU probe still hangs after restart, the q021 triage cannot proceed.

## 2026-06-10: Q021/Q022 focused triage result

Purpose:

- Test whether q021 `hybrid_without_refusal` is intrinsically prone to WebLLM
  stall.
- Run q021 and nearby q022 under a fresh Codex in-app browser/WebGPU session.

Observed result:

- q021 C2 completed without timeout: 6808.4 ms Qwen generation.
- q022 C2 completed without timeout: 16264.3 ms Qwen generation.
- Both records were schema-valid and used `Qwen3.5-0.8B-q4f16_1-MLC`.

Interpretation:

- q021 itself is not an inevitable stall case.
- The cleaner50 stall is more likely tied to long-batch/session-state
  accumulation after q001-q020.

Next experimental step:

- Run q021-q025 as a timeout-protected microbatch before attempting another
  full cleaner50.

## 2026-06-10: Q021-Q025 microbatch triage result

Purpose:

- Test whether the q021 cleaner50 stall reproduces in a smaller segmented
  batch with generation timeout enabled.

Observed result:

- Run id: `qwen_webllm_q021_q025_microbatch_v0`.
- Rows: 15.
- Schema errors: 0.
- Contract failures: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 2.
- `long_task_gc_rows`: 1.

Interpretation:

- q021-q025 can complete in a segmented run.
- The cleaner50 blocker is more likely monolithic-batch/session instability
  than an intrinsically failing q021 prompt.
- Latency remains diagnostic only because 2 rows were backgrounded.

Next experimental step:

- Continue segmented microbatches with q026-q030 before attempting another
  monolithic cleaner50.

## 2026-06-10: Q026-Q030 microbatch triage result

Purpose:

- Continue timeout-protected segmented execution after q021-q025 completed.

Observed result:

- Run id: `qwen_webllm_q026_q030_microbatch_v0`.
- Rows: 15.
- Schema errors: 0.
- Contract failures: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 15.
- `long_task_gc_rows`: 0.

Interpretation:

- q026-q030 completed without WebLLM stall.
- Latency should not be interpreted because all rows were backgrounded.
- The segmented strategy remains viable for execution stability.

Next experimental step:

- Run q031-q035 with the browser kept foregrounded if latency is part of the
  claim.

## 2026-06-10: Q031-Q035 microbatch triage result

Purpose:

- Continue timeout-protected segmented execution after q026-q030 completed.

Observed result:

- Run id: `qwen_webllm_q031_q035_microbatch_v0`.
- Rows: 15.
- Schema errors: 0.
- Contract failures: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 15.
- `long_task_gc_rows`: 0.

Interpretation:

- q031-q035 completed without WebLLM stall.
- Latency should not be interpreted because all rows were backgrounded.
- The segmented strategy has now completed q021-q035 after the cleaner50
  monolithic stall.

Next experimental step:

- Run q036-q040 and q041-q050 as remaining segments, then aggregate segment
  diagnostics.

## 2026-06-10: Q036-Q040 microbatch triage result

Purpose:

- Continue timeout-protected segmented execution after q031-q035 completed.

Observed result:

- Run id: `qwen_webllm_q036_q040_microbatch_v0`.
- Rows: 15.
- Schema errors: 0.
- Contract failures: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 15.
- `long_task_gc_rows`: 0.

Interpretation:

- q036-q040 completed without WebLLM stall.
- Latency should not be interpreted because all rows were backgrounded.
- Segmented execution has now completed q021-q040.

Next experimental step:

- Run q041-q050 as the final mixed-intent segment.

## 2026-06-10: Q041-Q050 microbatch and segmented 150 diagnostic

Purpose:

- Complete the remaining mixed-intent q041-q050 segment.
- Aggregate the stalled cleaner50 partial plus segmented reruns into a full
  150-row diagnostic coverage set.

Observed result:

- q041-q050 rows: 30.
- q041-q050 schema errors: 0.
- q041-q050 generation timeouts: 0.
- q041-q050 save errors: 0.
- q041-q050 contract failures: 4 in all-generation, 4 in
  hybrid-without-refusal, 0 in full-hybrid.
- Segmented coverage now represents 150 rows across q001-q050.

Interpretation:

- Segmented execution recovered the full fixture after the monolithic cleaner50
  stall.
- This is a methodology result about execution stability and checkpointing.
- Latency is not clean because most segmented rows were marked backgrounded.

Next experimental step:

- Repeat segmented execution with stronger foreground control if latency claims
  are needed.

## 2026-06-10: Segmented 150 aggregation script

Purpose:

- Add a reusable aggregation script for multi-file Qwen/WebLLM segmented runs.
- Replace hand-merged segment summaries with a single condition-level aggregate
  that checks row coverage, duplicate pairs, missing pairs, schema validity,
  contract failures, generation errors, timeouts, environment flags, and model
  identity.

Observed aggregate:

- Rows: 150.
- Queries: 50.
- Schema errors: 0.
- Duplicate query-condition pairs: 0.
- Missing query-condition pairs: 0.
- `all_generation` contract failures: 15.
- `hybrid_without_refusal` contract failures: 15.
- `full_hybrid` contract failures: 0.
- Generation errors/timeouts: 0.
- `tab_backgrounded_rows`: 77.

Interpretation:

- The segmented run set provides complete fixture coverage for pipeline and
  contract diagnostics.
- Latency remains diagnostic only because the aggregate includes backgrounded
  rows.

## 2026-06-10: Foreground q001-q010 clean-latency pre-run backup

Purpose:

- Back up the first foreground-controlled segmented rerun before starting it.
- Test whether Codex in-app browser execution can keep `tab_backgrounded_rows`
  at 0 for a small 30-row segment.

Expected output:

```text
runs/qwen_webllm_foreground_q001_q010_v0/qwen_webllm_foreground_q001_q010_v0_records.jsonl
```

Success criteria:

- 30 records.
- Schema errors: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 0.

Known limitation:

- If any row is backgrounded, the run is still useful for stability but not
  clean latency evidence.

## 2026-06-10: Foreground q001-q010 run and diagnostics

Purpose:

- Execute the predeclared foreground-controlled q001-q010 Qwen WebLLM segment.
- Verify whether Codex in-app browser can keep the panel visible throughout
  a 30-record run.

Run artifact:

```text
runs/qwen_webllm_foreground_q001_q010_v0/qwen_webllm_foreground_q001_q010_v0_records.jsonl
```

Reports:

```text
reports/QWEN_WEBLLM_FOREGROUND_Q001_Q010_DIAGNOSTICS_V0.md
reports/QWEN_WEBLLM_FOREGROUND_Q001_Q010_SUMMARY_V0.md
reports/qwen_webllm_foreground_q001_q010_diagnostics_v0.json
```

Result:

- Rows: 30.
- Schema errors: 0.
- Generation timeouts: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 1.
- Model id: `Qwen3.5-0.8B-q4f16_1-MLC`.
- Primary model identity: `Qwen/Qwen3.5-0.8B`.

Contract signal:

- `all_generation`: 2 contract failures.
- `hybrid_without_refusal`: 2 contract failures.
- `full_hybrid`: 0 contract failures.
- Failure ids: `q009`, `q010`.
- Failure group: `refusal_expected_alignment`.

Interpretation:

- The foreground-control path succeeded for this small segment.
- The refusal alignment failures are concentrated in the conditions that do
  not enforce the deterministic refusal lane.
- This is still instrumentation evidence, not a paper-ready finding.

Next step:

- Repeat with a larger foreground-controlled segment, preferably q001-q020,
  before rerunning all q001-q050 foregrounded.

## 2026-06-10: Foreground q011-q020 expansion pre-run backup

Purpose:

- Back up the next foreground-controlled Qwen WebLLM segment before execution.
- Extend q001-q010 coverage to q011-q020 without duplicating rows.
- Preserve the model boundary as `Qwen/Qwen3.5-0.8B` via
  `Qwen3.5-0.8B-q4f16_1-MLC`.

Expected output:

```text
runs/qwen_webllm_foreground_q011_q020_v0/qwen_webllm_foreground_q011_q020_v0_records.jsonl
```

Success criteria:

- 30 records.
- Schema errors: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 0.

Known limitation:

- If any row is backgrounded, this segment remains useful for stability
  diagnostics but not clean latency evidence.

## 2026-06-10: Foreground q011-q020 run and diagnostics

Purpose:

- Execute the predeclared q011-q020 foreground-controlled Qwen WebLLM segment.
- Extend foreground coverage to q001-q020 without duplicating q001-q010.

Run artifact:

```text
runs/qwen_webllm_foreground_q011_q020_v0/qwen_webllm_foreground_q011_q020_v0_records.jsonl
```

Reports:

```text
reports/QWEN_WEBLLM_FOREGROUND_Q011_Q020_DIAGNOSTICS_V0.md
reports/QWEN_WEBLLM_FOREGROUND_Q011_Q020_SUMMARY_V0.md
reports/qwen_webllm_foreground_q011_q020_diagnostics_v0.json
```

Result:

- Rows: 30.
- Schema errors: 0.
- Generation timeouts: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 1.
- Model id: `Qwen3.5-0.8B-q4f16_1-MLC`.
- Primary model identity: `Qwen/Qwen3.5-0.8B`.

Contract signal:

- `all_generation`: 9 contract failures.
- `hybrid_without_refusal`: 9 contract failures.
- `full_hybrid`: 0 contract failures.
- Failure ids: `q011`-`q019`.
- Failure group: `refusal_expected_alignment`.

Interpretation:

- The second foreground-controlled segment also avoided tab backgrounding.
- The refusal-lane ablation signal is stronger here because q011-q019 are
  refusal-required rows.
- This remains instrumentation evidence until larger foreground-controlled
  segments confirm stability.

Next step:

- Run q021-q035 as a foreground-controlled generative-heavy segment.

## 2026-06-10: Foreground q021-q035 generative-heavy pre-run backup

Purpose:

- Back up the next foreground-controlled Qwen WebLLM segment before execution.
- Stress comparison, recommendation, and explanation lanes where Qwen
  generation is expected to dominate.
- Preserve the model boundary as `Qwen/Qwen3.5-0.8B` via
  `Qwen3.5-0.8B-q4f16_1-MLC`.

Expected output:

```text
runs/qwen_webllm_foreground_q021_q035_v0/qwen_webllm_foreground_q021_q035_v0_records.jsonl
```

Success criteria:

- 45 records.
- Schema errors: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 0.

Known limitation:

- This segment is expected to contain much more generation than q001-q020, so
  latency remains diagnostic until repeated foreground-controlled runs confirm
  stability.

## 2026-06-10: Foreground q021-q035 run and diagnostics

Purpose:

- Execute the predeclared q021-q035 foreground-controlled Qwen WebLLM segment.
- Stress a generative-heavy section covering comparison, recommendation, and
  explanation rows.

Run artifact:

```text
runs/qwen_webllm_foreground_q021_q035_v0/qwen_webllm_foreground_q021_q035_v0_records.jsonl
```

Reports:

```text
reports/QWEN_WEBLLM_FOREGROUND_Q021_Q035_DIAGNOSTICS_V0.md
reports/QWEN_WEBLLM_FOREGROUND_Q021_Q035_SUMMARY_V0.md
reports/qwen_webllm_foreground_q021_q035_diagnostics_v0.json
```

Result:

- Rows: 45.
- Schema errors: 0.
- Generation timeouts: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 1.
- Model id: `Qwen3.5-0.8B-q4f16_1-MLC`.
- Primary model identity: `Qwen/Qwen3.5-0.8B`.

Contract signal:

- `all_generation`: 0 contract failures.
- `hybrid_without_refusal`: 0 contract failures.
- `full_hybrid`: 0 contract failures.
- Failure ids: none.

Interpretation:

- This segment behaved as a generative-heavy reference: all 45 rows invoked
  Qwen and no deterministic skip rows were observed.
- Latency is therefore similar across the three conditions in this segment.
- The foreground-control path remains stable across a longer Qwen-heavy run.

Next step:

- Run q036-q050 as the remaining foreground-controlled segment.

## 2026-06-10: Foreground q036-q050 final segment pre-run backup

Purpose:

- Back up the final foreground-controlled Qwen WebLLM segment before execution.
- Complete q001-q050 foreground coverage by running q036-q050.
- Stress recommendation and mixed-intent rows, including compound answer lanes.
- Preserve the model boundary as `Qwen/Qwen3.5-0.8B` via
  `Qwen3.5-0.8B-q4f16_1-MLC`.

Expected output:

```text
runs/qwen_webllm_foreground_q036_q050_v0/qwen_webllm_foreground_q036_q050_v0_records.jsonl
```

Success criteria:

- 45 records.
- Schema errors: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 0.

Known limitation:

- This segment may mix all-generation, generative guidance, and compound
  answer lanes; latency should remain diagnostic until aggregate analysis is
  complete.

## 2026-06-10: Foreground q036-q050 run and contaminated diagnostics

Purpose:

- Execute the predeclared q036-q050 Qwen WebLLM segment.
- Complete q001-q050 foreground-attempt coverage.
- Capture recommendation and mixed-intent behavior, including compound answers
  and deterministic refusals.

Run artifact:

```text
runs/qwen_webllm_foreground_q036_q050_v0/qwen_webllm_foreground_q036_q050_v0_records.jsonl
```

Reports:

```text
reports/QWEN_WEBLLM_FOREGROUND_Q036_Q050_DIAGNOSTICS_V0.md
reports/QWEN_WEBLLM_FOREGROUND_Q036_Q050_SUMMARY_V0.md
reports/qwen_webllm_foreground_q036_q050_diagnostics_v0.json
```

Result:

- Rows: 45.
- Schema errors: 0.
- Generation timeouts: 0.
- `tab_backgrounded_rows`: 18.
- `long_task_gc_rows`: 2.
- Model id: `Qwen3.5-0.8B-q4f16_1-MLC`.
- Primary model identity: `Qwen/Qwen3.5-0.8B`.

Contract signal:

- `all_generation`: 4 contract failures.
- `hybrid_without_refusal`: 4 contract failures.
- `full_hybrid`: 0 contract failures.
- Failure ids: `q043`, `q044`, `q047`, `q048`.
- Failure group: `refusal_expected_alignment`.

Interpretation:

- The run is valid for contract/stability diagnostics.
- The run is not clean latency evidence because it was backgrounded mid-run.
- The full-hybrid deterministic refusal lane again removes refusal-alignment
  failures observed in conditions without deterministic refusal.

Next step:

- Rerun q036-q050 with stronger foreground protection before using it in a
  clean latency aggregate.

## 2026-06-10: Foreground aggregate split

Purpose:

- Aggregate the foreground-controlled segments without hiding the q036-q050
  backgrounding event.
- Preserve a clean latency boundary for q001-q035 and a separate q001-q050
  foreground-attempt aggregate.

Reports:

```text
reports/QWEN_WEBLLM_FOREGROUND_CLEAN_Q001_Q035_AGGREGATE_V0.md
reports/qwen_webllm_foreground_clean_q001_q035_aggregate_v0.json
reports/QWEN_WEBLLM_FOREGROUND_ATTEMPT_Q001_Q050_AGGREGATE_V0.md
reports/qwen_webllm_foreground_attempt_q001_q050_aggregate_v0.json
```

Clean q001-q035 aggregate:

- Rows: 105.
- Queries: 35.
- Schema errors: 0.
- Duplicate query-condition pairs: 0.
- Missing query-condition pairs: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 3.
- Contract failures:
  - `all_generation`: 11.
  - `hybrid_without_refusal`: 11.
  - `full_hybrid`: 0.
- Failure group: `refusal_expected_alignment`.
- Failure ids: `q009`-`q019`.

Foreground-attempt q001-q050 aggregate:

- Rows: 150.
- Queries: 50.
- Schema errors: 0.
- Duplicate query-condition pairs: 0.
- Missing query-condition pairs: 0.
- `tab_backgrounded_rows`: 18.
- `long_task_gc_rows`: 5.
- Contract failures:
  - `all_generation`: 15.
  - `hybrid_without_refusal`: 15.
  - `full_hybrid`: 0.
- Failure ids: `q009`-`q019`, `q043`, `q044`, `q047`, `q048`.

Interpretation:

- q001-q035 is the current clean foreground set for latency diagnostics.
- q001-q050 is complete for contract coverage but contaminated for clean
  latency because q036-q050 was backgrounded mid-run.
- The main ablation signal remains refusal-lane related: conditions without
  deterministic refusal show refusal alignment failures; full hybrid has 0
  contract failures across both aggregates.

Next step:

- Rerun q036-q050 with stricter foreground protection, then regenerate a clean
  q001-q050 aggregate.

## 2026-06-10: Foreground q036-q050 split rerun pre-run backup

Purpose:

- Back up the rerun plan for replacing the latency-contaminated q036-q050
  segment.
- Split q036-q050 into shorter foreground-controlled runs:
  `q036-q042` and `q043-q050`.
- Preserve the model boundary as `Qwen/Qwen3.5-0.8B` via
  `Qwen3.5-0.8B-q4f16_1-MLC`.

Expected outputs:

```text
runs/qwen_webllm_foreground_q036_q042_split_v0/qwen_webllm_foreground_q036_q042_split_v0_records.jsonl
runs/qwen_webllm_foreground_q043_q050_split_v0/qwen_webllm_foreground_q043_q050_split_v0_records.jsonl
```

Success criteria:

- q036-q042: 21 records.
- q043-q050: 24 records.
- Schema errors: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 0 for each split segment.

Known limitation:

- If either shorter segment is backgrounded, keep that segment as contaminated
  and rerun only the affected range.

## 2026-06-10: q036-q042 split contaminated run and focus rerun plan

Purpose:

- Record the first split rerun of q036-q042.
- Preserve it as contaminated foreground-control evidence because it was
  backgrounded during generation.
- Predeclare a stronger focus-keeper rerun for q036-q042.

Run artifact:

```text
runs/qwen_webllm_foreground_q036_q042_split_v0/qwen_webllm_foreground_q036_q042_split_v0_records.jsonl
```

Reports:

```text
reports/QWEN_WEBLLM_FOREGROUND_Q036_Q042_SPLIT_DIAGNOSTICS_V0.md
reports/QWEN_WEBLLM_FOREGROUND_Q036_Q042_SPLIT_SUMMARY_V0.md
reports/qwen_webllm_foreground_q036_q042_split_diagnostics_v0.json
```

Result:

- Rows: 21.
- Schema errors: 0.
- Generation timeouts: 0.
- Contract failures: 0.
- `tab_backgrounded_rows`: 21.
- `long_task_gc_rows`: 3.

Interpretation:

- Segment length alone did not solve the Codex in-app browser backgrounding
  issue.
- This artifact is retained for contract/stability diagnostics but must not
  be used as clean latency evidence.

Next step:

- Rerun q036-q042 as
  `qwen_webllm_foreground_q036_q042_focus_v0` while a foreground keeper
  repeatedly sets Codex as the frontmost app.

## 2026-06-12: q036-q042 focus rerun

Purpose:

- Rerun q036-q042 after the first split attempt was fully backgrounded.
- Use the Codex in-app browser manually in the foreground.
- Preserve the model boundary as `Qwen/Qwen3.5-0.8B` via
  `Qwen3.5-0.8B-q4f16_1-MLC`.

Run artifact:

```text
runs/qwen_webllm_foreground_q036_q042_focus_v0/qwen_webllm_foreground_q036_q042_focus_v0_records.jsonl
```

Reports:

```text
reports/QWEN_WEBLLM_FOREGROUND_Q036_Q042_FOCUS_DIAGNOSTICS_V0.md
reports/QWEN_WEBLLM_FOREGROUND_Q036_Q042_FOCUS_SUMMARY_V0.md
reports/qwen_webllm_foreground_q036_q042_focus_diagnostics_v0.json
```

Result:

- Rows: 21.
- Schema errors: 0.
- Generation timeouts: 0.
- Contract failures: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 1.

Interpretation:

- This run replaces the contaminated q036-q042 split attempt for clean latency
  diagnostics.
- The manual Codex browser foreground path worked for this segment.

Next step:

- Run q043-q050 using the same manual Codex browser foreground path.

## 2026-06-12: q043-q050 clean split and q001-q050 clean aggregate

Purpose:

- Complete the remaining q043-q050 foreground-controlled split after the
  q036-q042 focus rerun succeeded.
- Regenerate the full clean q001-q050 aggregate using q036-q042 focus and
  q043-q050 split in place of the background-contaminated q036-q050 attempt.
- Preserve the model boundary as `Qwen/Qwen3.5-0.8B` via
  `Qwen3.5-0.8B-q4f16_1-MLC`.

Run artifact:

```text
runs/qwen_webllm_foreground_q043_q050_split_v0/qwen_webllm_foreground_q043_q050_split_v0_records.jsonl
```

Reports:

```text
reports/QWEN_WEBLLM_FOREGROUND_Q043_Q050_SPLIT_DIAGNOSTICS_V0.md
reports/QWEN_WEBLLM_FOREGROUND_Q043_Q050_SPLIT_SUMMARY_V0.md
reports/qwen_webllm_foreground_q043_q050_split_diagnostics_v0.json
reports/QWEN_WEBLLM_FOREGROUND_CLEAN_Q001_Q050_AGGREGATE_V0.md
reports/qwen_webllm_foreground_clean_q001_q050_aggregate_v0.json
```

q043-q050 split result:

- Rows: 24.
- Schema errors: 0.
- Generation timeouts: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 1.
- Contract failures:
  - `all_generation`: 4.
  - `hybrid_without_refusal`: 4.
  - `full_hybrid`: 0.
- Failure ids: `q043`, `q044`, `q047`, `q048`.

Clean q001-q050 aggregate:

- Rows: 150.
- Queries: 50.
- Schema errors: 0.
- Duplicate query-condition pairs: 0.
- Missing query-condition pairs: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 5.
- Contract failures:
  - `all_generation`: 15.
  - `hybrid_without_refusal`: 15.
  - `full_hybrid`: 0.
- Failure ids: `q009`-`q019`, `q043`, `q044`, `q047`, `q048`.

Interpretation:

- The full 50-query foreground-controlled Qwen/WebLLM instrumentation set is
  now complete without tab-background contamination.
- This is still exploratory instrumentation, not a paper-facing finding.
- The current contract signal remains refusal-lane related: conditions without
  deterministic refusal show refusal alignment failures, while full hybrid has
  0 automatic contract failures on this synthetic fixture.

Next step:

- Analyze the clean aggregate before expanding or making stronger claims.

## 2026-06-12: Paper v1 freeze scaffold

Purpose:

- Convert the external assessment into repository-level paper-facing controls.
- Add status, claim, non-claim, and artifact ledgers so exploratory diagnostics
  do not silently become overclaimed paper evidence.
- Define the next phase as Paper v1 Freeze rather than additional loose
  diagnostic runs.
- Add simple blinded reviewer instructions that separate human semantic review
  from automatic/mechanical contract checks.

Added files:

```text
EXPERIMENT_STATUS.md
CLAIMS_AND_NON_CLAIMS.md
FINAL_ARTIFACT_INDEX.md
docs/PAPER_V1_FREEZE_PLAN.md
docs/BLIND_REVIEWER_INSTRUCTIONS_SIMPLE.md
manifests/README.md
```

Current stance:

- The clean q001-q050 Qwen/WebLLM aggregate remains exploratory.
- The current strongest automatic signal is refusal-lane related:
  `full_hybrid` has 0 automatic contract failures while `all_generation` and
  `hybrid_without_refusal` each have 15 on the synthetic fixture.
- Journal-level claims remain blocked until a source-audited or public-derived
  fixture, freeze manifest, paper-facing run, and blinded human review exist.

Next step:

- Build the Paper v1 fixture and freeze manifest before running another
  paper-facing experiment.

## 2026-06-12: Information Research target and expansion roadmap

Purpose:

- Record Information Research as the first writing and style target while
  noting that the official submissions page currently says the journal is not
  accepting submissions.
- Reframe the paper for an information-system and information-user audience
  rather than as a RAG algorithm benchmark.
- Replace a simple 50-to-100-to-300 scaling story with a staged plan:
  synthetic 50, source-audited 50, source-audited 100, then held-out 200/300
  robustness.
- Define the formal human-review entry gate and keep current review work at
  calibration-only until source audit and freeze requirements are met.

Added files:

```text
docs/INFORMATION_RESEARCH_TARGET_PLAN.md
docs/SOURCE_AUDITED_EXPANSION_ROADMAP.md
```

Updated files:

```text
docs/PAPER_V1_FREEZE_PLAN.md
CLAIMS_AND_NON_CLAIMS.md
FINAL_ARTIFACT_INDEX.md
scripts/freeze_manifest.py
README.md
```

Current stance:

- Information Research is the preferred target style and audience, but not an
  immediate submission endpoint unless submissions reopen.
- A source-audited 100-query Paper v1 package is the minimum target for that
  venue framing.
- Human review should start formally after source audit, rule/prompt freeze,
  clean three-condition run, automatic contract checks, and blind-pack export.

## 2026-06-12: OIR/AJIM stretch-target strategy

Purpose:

- Supersede Information Research as the active first target because its
  submissions page is closed and the current OJS archive state is uncertain.
- Define Online Information Review as the first stretch target and Aslib
  Journal of Information Management as the second stretch target.
- Preserve Journal of Information Science, The Electronic Library, Open
  Information Science, and Digital Library Perspectives as backup tiers.
- Raise the OIR/AJIM evidence standard to a 300-query source-audited final run
  with automatic metrics on all 900 condition outputs and two-rater blinded
  semantic review on 240-300 sampled outputs.

Added files:

```text
docs/JOURNAL_TARGET_STRATEGY.md
```

Updated files:

```text
docs/INFORMATION_RESEARCH_TARGET_PLAN.md
docs/SOURCE_AUDITED_EXPANSION_ROADMAP.md
docs/PAPER_V1_FREEZE_PLAN.md
CLAIMS_AND_NON_CLAIMS.md
FINAL_ARTIFACT_INDEX.md
scripts/freeze_manifest.py
README.md
```

Current stance:

- OIR/AJIM are high-risk stretch targets, not safe Q2/Q3 fallbacks.
- The final OIR/AJIM candidate needs 300 source-audited queries, 900 outputs,
  a frozen manifest, clean Qwen/WebLLM browser-local runs, all-output automatic
  contract metrics, and sampled blinded semantic review.
- The 100-query stage is now calibration, and the 200-query stage is a formal
  review/workflow pilot rather than the final paper-facing run.
