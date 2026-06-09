# Qwen WebLLM 10-To-50 Experiment Expectation V0

Date: 2026-06-10

This is the pre-run backup note for the first primary-model experiment using
the Codex in-app browser. The primary model identity is `Qwen/Qwen3.5-0.8B`.
The browser research runtime id is `Qwen3.5-0.8B-q4f16_1-MLC`.

## Fixture Selection

Use the 50-row draft runtime/evaluation views:

```bash
HYBRID_LANE_RUNTIME_PATH=fixtures/drafts/runtime_view_v0.jsonl
HYBRID_LANE_EVAL_PATH=fixtures/drafts/evaluation_view_v0.jsonl
```

The committed one-row default fixture remains the smallest smoke fixture. This
experiment intentionally points Flask at the 50-row draft fixture via
environment variables.

## Run Sequence

1. Start Flask with the draft 50-row runtime/evaluation views.
2. Open `/tools/qwen_webllm_smoke/` in the Codex in-app browser.
3. Probe WebGPU.
4. Click `Load Qwen WebLLM`.
5. Run `Run First 10`.
6. If the 10-query batch saves valid JSONL and has no model/runtime blocker,
   immediately run `Run First 50`.

## Expected Outputs

The 10-query pilot should save:

```text
runs/qwen_webllm_pilot10_v0/qwen_webllm_pilot10_v0_records.jsonl
```

The 50-query scale run should save:

```text
runs/qwen_webllm_scale50_v0/qwen_webllm_scale50_v0_records.jsonl
```

These run outputs are experimental artifacts. They are not committed unless a
later curation step explicitly promotes summaries or reports.

## Success Criteria

- The WebGPU probe is available or its failure is explicit.
- The Qwen WebLLM engine loads or fails with a clear model/runtime error.
- Each completed generative or compound row records
  `qwen_generation_latency_ms`, `ttft_ms`, and `tokens_per_second`.
- Deterministic-only rows record `qwen_generation_latency_ms = 0.0`.
- Saved JSONL validates against `schemas/run_record_schema.json`.
- The producer metadata for generated rows is
  `webllm_qwen3_5_0_8b_research_runtime`.

## Stop Conditions

Stop before the 50-query run if the 10-query pilot shows:

- WebLLM cannot load the Qwen runtime;
- the browser tab crashes, hangs, or loses WebGPU;
- saved records fail schema validation;
- generated rows do not record Qwen latency fields;
- deterministic lanes unexpectedly invoke Qwen generation.

## Non-Claims

This run does not establish statistical superiority, source correctness, or
full usability. It tests whether the primary Qwen/WebLLM path can produce
schema-compatible hybrid-lane records at 10 and then 50 query scale.
