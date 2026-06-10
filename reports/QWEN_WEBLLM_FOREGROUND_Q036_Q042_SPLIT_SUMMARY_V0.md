# Qwen WebLLM Foreground Q036-Q042 Split Summary V0

Date: 2026-06-10

This split segment is a contaminated foreground-control attempt, not clean
latency evidence.

## Run Scope

```text
run_id: qwen_webllm_foreground_q036_q042_split_v0
query range: q036-q042
records: 21
model_id: Qwen3.5-0.8B-q4f16_1-MLC
primary_model_identity: Qwen/Qwen3.5-0.8B
generation_timeout_ms: 120000
```

## Result

- Rows: 21.
- Schema errors: 0.
- Generation timeouts: 0.
- Contract failures: 0.
- `tab_backgrounded_rows`: 21.
- `long_task_gc_rows`: 3.

## Interpretation

The shorter segment did not solve the foreground problem by itself. The run is
valid for contract/stability diagnostics, but it must not be used as clean
latency evidence.

## Next Step

Rerun q036-q042 with an explicit foreground keeper:

```text
run_id: qwen_webllm_foreground_q036_q042_focus_v0
```
