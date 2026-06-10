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

## qwen_webllm_foreground_q001_q010_v0_records

- Rows: 30
- Queries: 10
- Schema errors: 0
- Failure query ids: q009, q010

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 10 | 10 | 0 | 2 | 8820.0 | 11509.14 | 8820.0 | 11509.28 |
| hybrid_without_refusal | 10 | 2 | 8 | 2 | 3839.85 | 3916.13 | 0.05 | 3848.37 |
| full_hybrid | 10 | 0 | 10 | 0 | None | None | 0.0 | 0.06 |

Environment:

{
  "cold_start_rows": 1,
  "warmup_rows": 0,
  "warm_rows": 30,
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
    "count": 2
  },
  {
    "condition": "hybrid_without_refusal",
    "fail_keys": [
      "refusal_expected_alignment"
    ],
    "count": 2
  }
]

