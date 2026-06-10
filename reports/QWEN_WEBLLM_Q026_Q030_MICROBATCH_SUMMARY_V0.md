# Qwen WebLLM Q026-Q030 Microbatch Summary V0

Date: 2026-06-10

This is a segmented execution triage run, not a paper result.

## Run

```text
run_id: qwen_webllm_q026_q030_microbatch_v0
batch_start: 26
batch_limit: 5
conditions: all_generation, hybrid_without_refusal, full_hybrid
generation_timeout_ms: 120000
```

## Result

- Rows: 15.
- Queries: 5.
- Schema errors: 0.
- Contract failures: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 15.
- `long_task_gc_rows`: 0.

## Interpretation

The q026-q030 segment completed without WebLLM stall or save failure. This
continues to support segmented execution as a practical workaround for the
cleaner50 monolithic-run stall.

Latency from this segment should not be used as clean latency evidence because
all rows were marked backgrounded.

## Next Step

Continue with q031-q035 using the same timeout-protected segmented strategy,
while keeping the Codex browser foregrounded if latency is being evaluated.
