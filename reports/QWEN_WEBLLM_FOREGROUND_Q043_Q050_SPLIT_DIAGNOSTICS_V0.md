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

## qwen_webllm_foreground_q043_q050_split_v0_records

- Rows: 24
- Queries: 8
- Schema errors: 0
- Failure query ids: q043, q044, q047, q048

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 8 | 8 | 0 | 4 | 9760.5 | 10489.49 | 9760.5 | 10489.49 |
| hybrid_without_refusal | 8 | 8 | 0 | 4 | 9581.6 | 10792.04 | 9581.6 | 10792.04 |
| full_hybrid | 8 | 4 | 4 | 0 | 9617.15 | 9956.15 | 4664.35 | 9909.62 |

Environment:

{
  "cold_start_rows": 1,
  "warmup_rows": 0,
  "warm_rows": 24,
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
      "conflict_surfaced",
      "refusal_expected_alignment"
    ],
    "count": 1
  },
  {
    "condition": "all_generation",
    "fail_keys": [
      "refusal_expected_alignment"
    ],
    "count": 3
  },
  {
    "condition": "hybrid_without_refusal",
    "fail_keys": [
      "refusal_expected_alignment"
    ],
    "count": 4
  }
]

