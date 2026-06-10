# Qwen WebLLM Cleaner50 Expectation V0

Date: 2026-06-10

This is a pre-run backup note for the next browser-local Qwen/WebLLM scale
check. It is not a paper-claim document.

## Purpose

- Expand the cleaner instrumentation path from 20 queries to the full 50-query
  fixture.
- Keep the primary model boundary fixed to `Qwen/Qwen3.5-0.8B` through the
  WebLLM runtime id `Qwen3.5-0.8B-q4f16_1-MLC`.
- Use the Codex in-app browser, kept visible and foregrounded, to avoid the
  background-tab contamination seen in the earlier scale50 run.
- Re-check that `long_task_gc` is row-delta based rather than cumulative.

## Expected Output

```text
runs/qwen_webllm_cleaner50_v0/qwen_webllm_cleaner50_v0_records.jsonl
reports/QWEN_WEBLLM_CLEANER50_DIAGNOSTICS_V0.md
reports/qwen_webllm_cleaner50_diagnostics_v0.json
```

## Expected Diagnostic Pattern

- 150 run records: 50 queries across 3 conditions.
- Schema errors should remain 0.
- `tab_backgrounded_rows` should remain 0 if the browser stays foregrounded.
- `long_task_gc_rows` should be lower than the old 10-to-50 run because the
  panel and Flask API now record per-row long-task deltas.
- Failure groups are expected to remain concentrated around
  `refusal_expected_alignment`; this is an ablation signal to inspect, not a
  standalone finding.

## Recovery Behavior

The browser panel saves a checkpoint after each query's three conditions using
the same run id. If Codex, the browser, or WebGPU exits before the final row,
the partial JSONL file should preserve completed records instead of losing the
entire batch.

## Interpretation Boundary

Cleaner50 may justify larger repeated runs or fixture refinement. It should not
be treated as a paper result until repeated clean runs, source-audit checks, and
reviewer-facing usability evaluation are added.
