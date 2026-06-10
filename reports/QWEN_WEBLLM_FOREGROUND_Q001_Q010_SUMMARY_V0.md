# Qwen WebLLM Foreground Q001-Q010 Summary V0

Date: 2026-06-10

This is an instrumentation and foreground-control result, not a paper claim.

## Run Scope

```text
run_id: qwen_webllm_foreground_q001_q010_v0
query range: q001-q010
conditions: all_generation, hybrid_without_refusal, full_hybrid
records: 30
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
- `model_load_ms`: 2122.6.

This satisfies the pre-run foreground-control criterion for a 30-record
segment. The single long-task flag means latency should still be treated as
diagnostic, but the prior backgrounding problem was not reproduced.

## Contract Result

| Condition | Rows | Qwen rows | Deterministic skip rows | Contract failures |
|---|---:|---:|---:|---:|
| all_generation | 10 | 10 | 0 | 2 |
| hybrid_without_refusal | 10 | 2 | 8 | 2 |
| full_hybrid | 10 | 0 | 10 | 0 |

Failure query ids:

- `q009`
- `q010`

Failure group:

- `refusal_expected_alignment`

Interpretation:

- `q009` and `q010` are refusal-required rows.
- Conditions without the deterministic refusal lane show the expected refusal
  alignment failures.
- Full hybrid handles the same rows through deterministic refusal and has 0
  contract failures in this segment.

## Latency Snapshot

| Condition | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|
| all_generation | 8820.0 | 11509.14 | 8820.0 | 11509.28 |
| hybrid_without_refusal | 3839.85 | 3916.13 | 0.05 | 3848.37 |
| full_hybrid | n/a | n/a | 0.0 | 0.06 |

These values are useful for pipeline triage. They should not be reported as
stable latency evidence until larger foreground-controlled segments are run.

## Next Step

Use the same foreground-controlled Codex in-app browser path for a larger
rerun. Recommended next segment:

```text
run_id: qwen_webllm_foreground_q001_q020_v0
batch_start: 1
batch_limit: 20
```

If `tab_backgrounded_rows` remains 0, proceed to a full q001-q050 foreground
rerun or two 25-query segments.
