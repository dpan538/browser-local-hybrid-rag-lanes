# Qwen WebLLM Foreground Q001-Q010 Expectation V0

Date: 2026-06-10

This is a clean-latency instrumentation probe, not a paper result.

## Purpose

- Test whether the Codex in-app browser can keep a segmented run foregrounded.
- Re-run q001-q010 with checkpointing and generation timeout enabled.
- Preserve the primary model boundary:
  `Qwen/Qwen3.5-0.8B` via `Qwen3.5-0.8B-q4f16_1-MLC`.

## Planned Run

```text
run_id: qwen_webllm_foreground_q001_q010_v0
batch_start: 1
batch_limit: 10
conditions: all_generation, hybrid_without_refusal, full_hybrid
generation_timeout_ms: 120000
```

## Success Criteria

- 30 records.
- Schema errors: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 0.

If any row is backgrounded, this run remains useful for stability diagnostics
but cannot be used as clean latency evidence.
