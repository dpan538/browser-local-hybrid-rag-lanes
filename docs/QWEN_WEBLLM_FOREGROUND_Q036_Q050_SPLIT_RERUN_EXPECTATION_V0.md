# Qwen WebLLM Foreground Q036-Q050 Split Rerun Expectation V0

Date: 2026-06-10

This is a foreground-control rerun plan, not a paper result.

## Purpose

- Replace the latency-contaminated q036-q050 segment with shorter foreground
  runs.
- Preserve the existing raw q036-q050 attempt as a documented contaminated
  contract/stability artifact.
- Preserve the primary model boundary:
  `Qwen/Qwen3.5-0.8B` via `Qwen3.5-0.8B-q4f16_1-MLC`.

## Planned Runs

```text
run_id: qwen_webllm_foreground_q036_q042_split_v0
batch_start: 36
batch_limit: 7
conditions: all_generation, hybrid_without_refusal, full_hybrid
generation_timeout_ms: 120000
```

```text
run_id: qwen_webllm_foreground_q043_q050_split_v0
batch_start: 43
batch_limit: 8
conditions: all_generation, hybrid_without_refusal, full_hybrid
generation_timeout_ms: 120000
```

## Success Criteria

For each split segment:

- q036-q042: 21 records.
- q043-q050: 24 records.
- Schema errors: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 0.

If either segment is backgrounded, keep it as a contaminated stability artifact
and rerun only that segment with stronger foreground protection.
