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

## qwen_webllm_q036_q040_microbatch_v0_records

- Rows: 15
- Queries: 5
- Schema errors: 0
- Failure query ids: none

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 5 | 5 | 0 | 0 | 8523.2 | 8553.26 | 8523.3 | 8553.28 |
| hybrid_without_refusal | 5 | 5 | 0 | 0 | 8534.1 | 8723.08 | 8534.1 | 8723.18 |
| full_hybrid | 5 | 5 | 0 | 0 | 8538.8 | 8701.94 | 8538.8 | 8701.94 |

Environment:

{
  "cold_start_rows": 0,
  "warmup_rows": 0,
  "warm_rows": 15,
  "tab_backgrounded_rows": 15,
  "long_task_gc_rows": 0,
  "network_variance_rows": 0,
  "manual_interruption_rows": 0
}

Failure groups:

[]

