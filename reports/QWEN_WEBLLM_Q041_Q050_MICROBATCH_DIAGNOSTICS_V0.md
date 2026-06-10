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

## qwen_webllm_q041_q050_microbatch_v0_records

- Rows: 30
- Queries: 10
- Schema errors: 0
- Failure query ids: q043, q044, q047, q048

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 10 | 10 | 0 | 4 | 9888.65 | 12832.59 | 9888.65 | 12832.59 |
| hybrid_without_refusal | 10 | 10 | 0 | 4 | 10019.8 | 12724.56 | 10019.85 | 12724.6 |
| full_hybrid | 10 | 6 | 4 | 0 | 9941.35 | 11981.78 | 9341.15 | 11477.36 |

Environment:

{
  "cold_start_rows": 0,
  "warmup_rows": 0,
  "warm_rows": 30,
  "tab_backgrounded_rows": 30,
  "long_task_gc_rows": 0,
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
    "count": 4
  },
  {
    "condition": "hybrid_without_refusal",
    "fail_keys": [
      "refusal_expected_alignment"
    ],
    "count": 4
  }
]

