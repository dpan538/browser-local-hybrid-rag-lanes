# Qwen WebLLM Q021 Triage Expectation V0

Date: 2026-06-10

This is a focused scale-blocker triage, not a paper result.

## Purpose

- Test whether the cleaner50 stall at q021 `hybrid_without_refusal` is
  reproducible after a clean browser/WebGPU restart.
- Keep the primary model fixed to `Qwen/Qwen3.5-0.8B` via
  `Qwen3.5-0.8B-q4f16_1-MLC`.
- Preserve the cleaner50 prompt, temperature, and default max token budget.
- Add a generation timeout so WebLLM streaming stalls become explicit records
  instead of freezing the whole run.

## Planned Runs

Initial focused run:

```text
run_id: qwen_webllm_q021_triage_v0
query: q021
condition: hybrid_without_refusal
generation_timeout_ms: 120000
```

If q021 succeeds, run q022 under the same condition as a nearby comparison.
If q021 times out, stop and diagnose the timeout record before attempting more
queries.

## Expected Output

```text
runs/qwen_webllm_q021_triage_v0/qwen_webllm_q021_triage_v0_records.jsonl
```

## Interpretation Boundary

This triage can show whether q021 is a reproducible WebLLM stall point. It
cannot support condition-level claims about hybrid answer lanes.
