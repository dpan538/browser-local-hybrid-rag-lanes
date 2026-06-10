# Qwen WebLLM Segmented 150 Summary V0

Date: 2026-06-10

This summary aggregates diagnostics from the stalled cleaner50 partial and the
subsequent segmented reruns. It is a methodology result, not a paper result.

## Inputs

```text
q001-q020: qwen_webllm_cleaner50_v0 checkpoint partial
q021-q025: qwen_webllm_q021_q025_microbatch_v0
q026-q030: qwen_webllm_q026_q030_microbatch_v0
q031-q035: qwen_webllm_q031_q035_microbatch_v0
q036-q040: qwen_webllm_q036_q040_microbatch_v0
q041-q050: qwen_webllm_q041_q050_microbatch_v0
```

## Coverage

- Total rows represented: 150.
- Total queries represented: 50.
- Schema errors across all segments: 0.
- Generation timeouts in completed segments: 0.
- Segment save errors after checkpoint hardening: 0.
- Primary model: `Qwen/Qwen3.5-0.8B`.
- WebLLM runtime id: `Qwen3.5-0.8B-q4f16_1-MLC`.

## Contract Pattern

The refusal-alignment pattern from earlier runs reappears:

- Full hybrid avoids the refusal-alignment failures in the deterministic
  refusal lanes.
- All-generation and hybrid-without-refusal still fail on expected refusal
  cases.

This is still a diagnostic pattern, not a usability or semantic-correctness
claim.

## Execution Finding

The monolithic cleaner50 run stalled around q021, while segmented execution
completed q021-q050 after timeout hardening. This supports a methodology
finding:

> Browser-local WebLLM experiments should use checkpointed, timeout-protected,
> segmented execution before relying on full-fixture scale runs.

## Latency Boundary

Latency should not be used as a clean result from the segmented aggregate:

- q001-q020 had clean foreground flags.
- q021-q025 had 2 backgrounded rows.
- q026-q050 segments were marked backgrounded.

The next clean-latency run should repeat segmented execution with stronger
foreground control or a browser automation mode that keeps visibility state
stable.
