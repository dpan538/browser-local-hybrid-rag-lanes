# Qwen WebLLM Foreground Q036-Q050 Expectation V0

Date: 2026-06-10

This is the final foreground-controlled segment for q001-q050 coverage, not a
paper result.

## Purpose

- Complete foreground-controlled Qwen WebLLM coverage for q001-q050 by running
  q036-q050.
- Stress recommendation and mixed-intent rows, including compound answer lanes.
- Preserve the primary model boundary:
  `Qwen/Qwen3.5-0.8B` via `Qwen3.5-0.8B-q4f16_1-MLC`.

## Planned Run

```text
run_id: qwen_webllm_foreground_q036_q050_v0
batch_start: 36
batch_limit: 15
conditions: all_generation, hybrid_without_refusal, full_hybrid
generation_timeout_ms: 120000
```

## Success Criteria

- 45 records.
- Schema errors: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 0.

If any row is backgrounded, this run remains useful for stability diagnostics
but cannot be used as clean latency evidence.
