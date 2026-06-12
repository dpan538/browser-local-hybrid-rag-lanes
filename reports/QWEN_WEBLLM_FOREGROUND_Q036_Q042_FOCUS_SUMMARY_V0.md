# Qwen WebLLM Foreground Q036-Q042 Focus Summary V0

Date: 2026-06-12

This is a clean foreground-control rerun for q036-q042, not a paper result.

## Run Scope

```text
run_id: qwen_webllm_foreground_q036_q042_focus_v0
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
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 1.
- `model_load_ms`: 2010.6.

## Interpretation

This focus rerun replaces the contaminated q036-q042 split attempt for clean
latency diagnostics. The successful foreground state suggests the earlier
failure was caused by browser visibility/focus rather than model instability.

## Next Step

Run q043-q050 using the same manual Codex browser foreground path:

```text
run_id: qwen_webllm_foreground_q043_q050_split_v0
batch_start: 43
batch_limit: 8
```
