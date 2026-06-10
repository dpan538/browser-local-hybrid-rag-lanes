# Qwen WebLLM Run Diagnostics

This diagnostic treats run records as experimental instrumentation data,
not as paper-ready findings.

## Diagnostic Consequence

This run is useful for pipeline and ablation triage, but it should
not be expanded into strong paper claims yet. Environment flags such
as `long_task_gc`, tab foregrounding, and browser visibility should be
checked before treating latency summaries as more than diagnostics.

The most useful current signal is not "we have a finding"; it is that the
pipeline can now expose exactly where the candidate finding would need
stronger evidence: refusal-boundary handling, Qwen invocation accounting,
and clean browser latency measurement.

## qwen_webllm_cleaner50_v0_records

- Rows: 60
- Queries: 20
- Schema errors: 0
- Failure query ids: q009, q010, q011, q012, q013, q014, q015, q016, q017, q018, q019

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 20 | 20 | 0 | 11 | 14079.75 | 24041.78 | 14079.8 | 24041.87 |
| hybrid_without_refusal | 20 | 12 | 8 | 11 | 6822.55 | 18349.13 | 6223.95 | 14613.82 |
| full_hybrid | 20 | 1 | 19 | 0 | 18804.3 | 18804.3 | 0.0 | 940.31 |

Environment:

{
  "cold_start_rows": 1,
  "warmup_rows": 0,
  "warm_rows": 60,
  "tab_backgrounded_rows": 0,
  "long_task_gc_rows": 1,
  "network_variance_rows": 0,
  "manual_interruption_rows": 0
}

Failure groups:

[
  {
    "condition": "all_generation",
    "fail_keys": [
      "refusal_expected_alignment"
    ],
    "count": 11
  },
  {
    "condition": "hybrid_without_refusal",
    "fail_keys": [
      "refusal_expected_alignment"
    ],
    "count": 11
  }
]

