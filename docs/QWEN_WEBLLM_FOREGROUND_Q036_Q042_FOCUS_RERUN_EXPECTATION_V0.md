# Qwen WebLLM Foreground Q036-Q042 Focus Rerun Expectation V0

Date: 2026-06-10

This is a stronger foreground-control rerun plan, not a paper result.

## Purpose

- Rerun q036-q042 after `qwen_webllm_foreground_q036_q042_split_v0` was
  backgrounded.
- Use a foreground keeper that repeatedly brings Codex to the front during the
  run.
- Preserve the primary model boundary:
  `Qwen/Qwen3.5-0.8B` via `Qwen3.5-0.8B-q4f16_1-MLC`.

## Planned Run

```text
run_id: qwen_webllm_foreground_q036_q042_focus_v0
batch_start: 36
batch_limit: 7
conditions: all_generation, hybrid_without_refusal, full_hybrid
generation_timeout_ms: 120000
foreground_keeper: osascript frontmost Codex loop during run
```

## Success Criteria

- 21 records.
- Schema errors: 0.
- Generation timeouts: 0.
- Save errors: 0.
- `tab_backgrounded_rows`: 0.

If this run is also backgrounded, the issue is likely the Codex in-app browser
visibility lifecycle rather than segment length alone.
