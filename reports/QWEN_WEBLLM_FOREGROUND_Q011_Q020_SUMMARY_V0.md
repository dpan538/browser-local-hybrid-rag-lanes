# Qwen WebLLM Foreground Q011-Q020 Summary V0

Date: 2026-06-10

This is an instrumentation and foreground-control result, not a paper claim.

## Run Scope

```text
run_id: qwen_webllm_foreground_q011_q020_v0
query range: q011-q020
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
- `model_load_ms`: 2014.2.

This is the second consecutive foreground-controlled 30-record segment with
`tab_backgrounded_rows` equal to 0.

## Contract Result

| Condition | Rows | Qwen rows | Deterministic skip rows | Contract failures |
|---|---:|---:|---:|---:|
| all_generation | 10 | 10 | 0 | 9 |
| hybrid_without_refusal | 10 | 10 | 0 | 9 |
| full_hybrid | 10 | 1 | 9 | 0 |

Failure query ids:

- `q011`
- `q012`
- `q013`
- `q014`
- `q015`
- `q016`
- `q017`
- `q018`
- `q019`

Failure group:

- `refusal_expected_alignment`

Interpretation:

- `q011`-`q019` are refusal-required rows.
- Conditions without deterministic refusal show refusal-alignment failures.
- Full hybrid routes those rows through deterministic refusal and has 0
  contract failures in this segment.
- `q020` is a comparison row and remains generative under full hybrid.

## Latency Snapshot

| Condition | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|
| all_generation | 7597.45 | 11968.08 | 7597.55 | 11968.08 |
| hybrid_without_refusal | 5465.45 | 11763.39 | 5465.55 | 11763.39 |
| full_hybrid | 12283.3 | 12283.3 | 0.0 | 6755.82 |

These values are diagnostic. The full-hybrid P95 is shaped by one generative
comparison row plus nine deterministic refusal rows.

## Next Step

The foreground path has now succeeded for q001-q020. Recommended next segment:

```text
run_id: qwen_webllm_foreground_q021_q035_v0
batch_start: 21
batch_limit: 15
```

This would stress the comparison, recommendation, and explanation lanes with
more generative work while continuing to avoid duplicate rows.
