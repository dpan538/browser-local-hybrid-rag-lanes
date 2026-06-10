# Qwen WebLLM Q021/Q022 Triage Summary V0

Date: 2026-06-10

This is a focused scale-blocker triage, not a paper result.

## Runs

```text
qwen_webllm_q021_triage_v0
query: q021
condition: hybrid_without_refusal
generation_timeout_ms: 120000

qwen_webllm_q022_triage_v0
query: q022
condition: hybrid_without_refusal
generation_timeout_ms: 120000
```

## Result

Both focused runs completed without generation timeout:

| Run | Rows | Schema errors | Qwen generation ms | Timeout |
|---|---:|---:|---:|---|
| q021 C2 | 1 | 0 | 6808.4 | no |
| q022 C2 | 1 | 0 | 16264.3 | no |

The same primary model boundary was preserved:

```text
Qwen/Qwen3.5-0.8B
Qwen3.5-0.8B-q4f16_1-MLC
```

## Interpretation

The cleaner50 stall at q021 `hybrid_without_refusal` does not appear to be
caused by q021 being inherently non-runnable. Under a fresh WebGPU/WebLLM
session, q021 C2 and nearby q022 C2 both completed.

The likely scale blocker is session-state or long-batch accumulation:

- repeated streaming calls before q021;
- WebGPU/WebLLM state after q001-q020;
- local app/browser process instability during long runs;
- absence of a per-generation timeout in the original cleaner50 attempt.

## Next Experiment

Run a small microbatch before another full cleaner50:

```text
run_id: qwen_webllm_q021_q025_microbatch_v0
batch_start: 21
batch_limit: 5
conditions: all_generation, hybrid_without_refusal, full_hybrid
generation_timeout_ms: 120000
```

If the microbatch completes, try a segmented cleaner50 strategy rather than one
monolithic browser run.
