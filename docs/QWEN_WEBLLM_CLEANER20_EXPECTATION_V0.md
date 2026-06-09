# Qwen WebLLM Cleaner20 Expectation V0

Date: 2026-06-10

This is a pre-run expectation for a cleaner instrumentation rerun. It is not a
paper-claim run. The goal is to test whether the measurement pipeline is now
cleaner after changing `long_task_gc` from cumulative long-task presence to
per-row long-task delta.

## Model And Runtime

- Primary model identity: `Qwen/Qwen3.5-0.8B`
- Browser research runtime id: `Qwen3.5-0.8B-q4f16_1-MLC`
- Runtime surface: Codex in-app browser
- Server role: Flask serves fixtures, prompt pack, and save endpoint only
- Comparison/server model backends: not used

## Fixture

Use the same 50-row draft fixture as the first run:

```bash
HYBRID_LANE_RUNTIME_PATH=fixtures/drafts/runtime_view_v0.jsonl
HYBRID_LANE_EVAL_PATH=fixtures/drafts/evaluation_view_v0.jsonl
```

Run only the first 20 queries:

```text
q001 through q020
```

Expected rows:

```text
20 queries x 3 conditions = 60 records
```

## Run ID

```text
qwen_webllm_cleaner20_v0
```

Expected local output:

```text
runs/qwen_webllm_cleaner20_v0/qwen_webllm_cleaner20_v0_records.jsonl
```

The raw JSONL remains ignored by git.

## Procedure

1. Start Flask with the 50-row draft fixture paths.
2. Open `/tools/qwen_webllm_smoke/` in the Codex in-app browser.
3. Keep the browser visible while the run executes.
4. Probe WebGPU.
5. Load Qwen WebLLM.
6. Set:
   - run id: `qwen_webllm_cleaner20_v0`
   - batch start: `1`
   - batch limit: `20`
7. Click `Run Batch`.
8. Save is automatic after batch completion.
9. Run `scripts/diagnose_qwen_webllm_run.py` on the saved JSONL.

## Success Criteria

- 60 records saved.
- 0 schema errors.
- Qwen rows record `qwen_generation_latency_ms`, `ttft_ms`, and
  `tokens_per_second`.
- Deterministic rows keep `qwen_generation_latency_ms = 0.0`.
- `tab_backgrounded_rows = 0`.
- `long_task_gc_rows` is no longer trivially equal to all rows.

## Stop Conditions

Stop and do not scale if:

- WebLLM cannot load;
- the tab crashes or loses WebGPU;
- schema validation fails;
- foreground tab cannot be maintained;
- `long_task_gc_rows` still equals all rows.

## Interpretation Boundary

Cleaner20 answers only whether instrumentation is better. It does not establish
latency stability, usability, or a paper-level claim.
