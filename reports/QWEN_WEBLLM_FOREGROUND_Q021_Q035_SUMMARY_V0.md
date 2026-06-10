# Qwen WebLLM Foreground Q021-Q035 Summary V0

Date: 2026-06-10

This is an instrumentation and foreground-control result, not a paper claim.

## Run Scope

```text
run_id: qwen_webllm_foreground_q021_q035_v0
query range: q021-q035
conditions: all_generation, hybrid_without_refusal, full_hybrid
records: 45
model_id: Qwen3.5-0.8B-q4f16_1-MLC
primary_model_identity: Qwen/Qwen3.5-0.8B
generation_timeout_ms: 120000
```

## Environment Result

- Schema errors: 0.
- Generation timeouts: 0.
- Save errors observed in panel log: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 1.
- `model_load_ms`: 1938.2.

This is the third consecutive foreground-controlled segment with
`tab_backgrounded_rows` equal to 0, and the first foreground segment dominated
by generative execution.

## Contract Result

| Condition | Rows | Qwen rows | Deterministic skip rows | Contract failures |
|---|---:|---:|---:|---:|
| all_generation | 15 | 15 | 0 | 0 |
| hybrid_without_refusal | 15 | 15 | 0 | 0 |
| full_hybrid | 15 | 15 | 0 | 0 |

Failure query ids:

- None.

Interpretation:

- q021-q035 covers comparison, recommendation, and explanation-style rows.
- These rows do not benefit from deterministic refusal or deterministic field
  rendering in the current rule table, so all three conditions invoke Qwen for
  all rows.
- This segment is useful as a generative-heavy latency and stability reference,
  not as evidence of deterministic lane speedup.

## Latency Snapshot

| Condition | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|
| all_generation | 10948.2 | 13006.47 | 10948.2 | 13006.54 |
| hybrid_without_refusal | 10888.2 | 13132.2 | 10888.2 | 13132.23 |
| full_hybrid | 10926.9 | 12715.49 | 10927.0 | 12715.56 |

Latency is expectedly similar across conditions because all rows are
generative in this segment.

## Next Step

Run the remaining q036-q050 foreground-controlled segment:

```text
run_id: qwen_webllm_foreground_q036_q050_v0
batch_start: 36
batch_limit: 15
```

That segment should restore mixed deterministic/generative behavior through
recommendation and mixed-intent rows.
