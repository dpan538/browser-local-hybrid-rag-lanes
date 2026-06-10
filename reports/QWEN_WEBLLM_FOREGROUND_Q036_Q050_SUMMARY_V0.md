# Qwen WebLLM Foreground Q036-Q050 Summary V0

Date: 2026-06-10

This is an instrumentation and contract/stability result. It is not clean
latency evidence because the run was backgrounded mid-segment.

## Run Scope

```text
run_id: qwen_webllm_foreground_q036_q050_v0
query range: q036-q050
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
- `tab_backgrounded_rows`: 18.
- `long_task_gc_rows`: 2.
- `model_load_ms`: 2127.7.

This segment failed the clean foreground-latency criterion. It remains useful
for contract behavior and execution-mode coverage.

## Contract Result

| Condition | Rows | Qwen rows | Deterministic skip rows | Contract failures |
|---|---:|---:|---:|---:|
| all_generation | 15 | 15 | 0 | 4 |
| hybrid_without_refusal | 15 | 15 | 0 | 4 |
| full_hybrid | 15 | 11 | 4 | 0 |

Failure query ids:

- `q043`
- `q044`
- `q047`
- `q048`

Failure group:

- `refusal_expected_alignment`

Interpretation:

- q036-q040 are recommendation rows.
- q041-q050 are mixed-intent rows, including compound answers and deterministic
  refusals.
- Full hybrid routes four rows through deterministic refusal and has 0
  contract failures in this segment.
- Conditions without deterministic refusal show refusal-alignment failures on
  the same four query ids.

## Latency Snapshot

| Condition | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|
| all_generation | 9937.5 | 11801.24 | 9937.5 | 11801.24 |
| hybrid_without_refusal | 9873.6 | 11824.98 | 9873.7 | 11825.05 |
| full_hybrid | 9733.1 | 11797.5 | 9385.8 | 11785.61 |

These latency values should be treated as contaminated by tab backgrounding.

## Next Step

Rerun q036-q050 with stronger foreground protection before using it in a clean
latency aggregate. The current artifact can remain in the repository as a
documented contaminated segment for contract/stability comparison.
