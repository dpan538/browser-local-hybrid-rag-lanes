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

## qwen_webllm_foreground_q036_q042_focus_v0_records

- Rows: 21
- Queries: 7
- Schema errors: 0
- Failure query ids: none

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 7 | 7 | 0 | 0 | 9782.0 | 11351.37 | 9782.0 | 11351.37 |
| hybrid_without_refusal | 7 | 7 | 0 | 0 | 9817.0 | 11422.92 | 9817.0 | 11423.05 |
| full_hybrid | 7 | 7 | 0 | 0 | 9792.6 | 11289.05 | 9792.6 | 11289.05 |

Environment:

{
  "cold_start_rows": 1,
  "warmup_rows": 0,
  "warm_rows": 21,
  "tab_backgrounded_rows": 0,
  "long_task_gc_rows": 1,
  "network_variance_rows": 0,
  "manual_interruption_rows": 0
}

Failure groups:

[]

