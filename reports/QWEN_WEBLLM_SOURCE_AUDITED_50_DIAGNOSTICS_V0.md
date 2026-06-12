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

## qwen_webllm_source_audited_50_v0_records

- Rows: 150
- Queries: 50
- Schema errors: 0
- Failure query ids: q016, q017, q018, q019, q020, q035, q036, q037, q038, q049

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 50 | 50 | 0 | 10 | 13957.45 | 17645.81 | 13957.5 | 17645.81 |
| hybrid_without_refusal | 50 | 40 | 10 | 10 | 14505.45 | 19290.83 | 12691.45 | 18663.34 |
| full_hybrid | 50 | 30 | 20 | 0 | 14703.5 | 18471.53 | 11368.45 | 17519.05 |

Environment:

{
  "cold_start_rows": 1,
  "warmup_rows": 0,
  "warm_rows": 150,
  "tab_backgrounded_rows": 0,
  "long_task_gc_rows": 64,
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
    "count": 10
  },
  {
    "condition": "hybrid_without_refusal",
    "fail_keys": [
      "refusal_expected_alignment"
    ],
    "count": 10
  }
]

