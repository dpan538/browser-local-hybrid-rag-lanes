# Qwen WebLLM Q021-Q025 Microbatch Summary V0

Date: 2026-06-10

This is a scale-blocker triage run, not a paper result.

## Run

```text
run_id: qwen_webllm_q021_q025_microbatch_v0
batch_start: 21
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
- `tab_backgrounded_rows`: 2.
- `long_task_gc_rows`: 1.

## Latency Snapshot

| Condition | Rows | Qwen rows | Qwen P50 ms | Qwen P95 ms |
|---|---:|---:|---:|---:|
| all_generation | 5 | 5 | 11574.7 | 20896.94 |
| hybrid_without_refusal | 5 | 5 | 11318.8 | 17102.52 |
| full_hybrid | 5 | 5 | 9677.2 | 14557.46 |

Latency remains diagnostic because this triage run has 2 backgrounded rows.

## Interpretation

q021-q025 completed as a focused microbatch with no timeout. This supports the
working diagnosis that the cleaner50 stall was caused by long-session or
monolithic-batch instability rather than q021 being intrinsically unrunnable.

The next scale strategy should be segmented batches, not another immediate
monolithic cleaner50.

## Next Step

Run the next segment:

```text
run_id: qwen_webllm_q026_q030_microbatch_v0
batch_start: 26
batch_limit: 5
generation_timeout_ms: 120000
```

If q026-q030 also completes, continue segmenting q031-q035, q036-q040, and
q041-q050 before re-aggregating diagnostics.
