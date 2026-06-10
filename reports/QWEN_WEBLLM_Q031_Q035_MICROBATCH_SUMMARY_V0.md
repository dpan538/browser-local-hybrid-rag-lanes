# Qwen WebLLM Q031-Q035 Microbatch Summary V0

Date: 2026-06-10

This is a segmented execution triage run, not a paper result.

## Run

```text
run_id: qwen_webllm_q031_q035_microbatch_v0
batch_start: 31
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

The q031-q035 segment completed without WebLLM stall or save failure. Together
with q021-q025 and q026-q030, this strengthens the segmented-run strategy for
execution stability.

Latency should not be interpreted because all rows were marked backgrounded.

## Next Step

Run q036-q040 and q041-q050 as remaining segmented microbatches, then aggregate
the completed segment diagnostics separately from the stalled monolithic
cleaner50 attempt.
