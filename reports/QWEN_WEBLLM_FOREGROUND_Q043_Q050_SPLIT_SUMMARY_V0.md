# Qwen WebLLM Foreground Q043-Q050 Split Summary V0

Date: 2026-06-12

This is a clean foreground-control rerun for q043-q050, not a paper result.

## Run Scope

```text
run_id: qwen_webllm_foreground_q043_q050_split_v0
query range: q043-q050
records: 24
model_id: Qwen3.5-0.8B-q4f16_1-MLC
primary_model_identity: Qwen/Qwen3.5-0.8B
generation_timeout_ms: 120000
```

## Result

- Rows: 24.
- Schema errors: 0.
- Generation timeouts: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 1.
- `model_load_ms`: 2162.9.

## Contract Signal

- `all_generation`: 4 contract failures.
- `hybrid_without_refusal`: 4 contract failures.
- `full_hybrid`: 0 contract failures.
- Failure ids: `q043`, `q044`, `q047`, `q048`.
- `q043` in all-generation also failed `conflict_surfaced`.

## Interpretation

This clean split replaces the contaminated q043-q050 portion of the earlier
q036-q050 run for latency diagnostics. The refusal-lane signal is preserved:
conditions without deterministic refusal fail on the refusal-required mixed
rows, while full hybrid has 0 contract failures.
