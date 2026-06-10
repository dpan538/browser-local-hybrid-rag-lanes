# Qwen WebLLM Foreground Q021-Q035 Expectation V0

Date: 2026-06-10

This is a foreground-controlled generative-heavy expansion segment, not a
paper result.

## Purpose

- Extend foreground-controlled Qwen WebLLM coverage to q021-q035.
- Stress comparison, recommendation, and explanation lanes, where all or most
  conditions require Qwen generation rather than deterministic rendering.
- Preserve the primary model boundary:
  `Qwen/Qwen3.5-0.8B` via `Qwen3.5-0.8B-q4f16_1-MLC`.

## Planned Run

```text
run_id: qwen_webllm_foreground_q021_q035_v0
batch_start: 21
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
