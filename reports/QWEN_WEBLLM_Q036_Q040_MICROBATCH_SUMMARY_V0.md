# Qwen WebLLM Q036-Q040 Microbatch Summary V0

Date: 2026-06-10

This is a segmented execution triage run, not a paper result.

## Run

```text
run_id: qwen_webllm_q036_q040_microbatch_v0
batch_start: 36
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

The q036-q040 segment completed without WebLLM stall or save failure. Segmented
execution has now completed q021-q040 after the monolithic cleaner50 stall.

Latency should not be interpreted because all rows were marked backgrounded.

## Next Step

Run q041-q050 as the final mixed-intent segment, then aggregate segmented
diagnostics separately from the monolithic cleaner50 partial.
