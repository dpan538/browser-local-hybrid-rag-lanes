# Qwen WebLLM Run Diagnostics

This diagnostic treats run records as experimental instrumentation data,
not as paper-ready findings.

## Diagnostic Consequence

The 10-to-50 run is useful for pipeline and ablation triage, but it should
not be expanded into strong paper claims yet. The next run should first
improve environment instrumentation: `long_task_gc` must be row-delta
based, the tab should remain foregrounded, and latency summaries should be
treated as diagnostic until those flags are clean.

The most useful current signal is not "we have a finding"; it is that the
pipeline can now expose exactly where the candidate finding would need
stronger evidence: refusal-boundary handling, Qwen invocation accounting,
and clean browser latency measurement.

## qwen_webllm_pilot10_v0_records

- Rows: 30
- Queries: 10
- Schema errors: 0
- Failure query ids: q009, q010

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 10 | 10 | 0 | 2 | 17136.05 | 20177.98 | 17136.1 | 20178.03 |
| hybrid_without_refusal | 10 | 2 | 8 | 2 | 3608.05 | 3620.33 | 0.0 | 3609.41 |
| full_hybrid | 10 | 0 | 10 | 0 | None | None | 0.0 | 0.06 |

Environment:

{
  "cold_start_rows": 1,
  "warmup_rows": 0,
  "warm_rows": 30,
  "tab_backgrounded_rows": 0,
  "long_task_gc_rows": 30,
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

## qwen_webllm_scale50_v0_records

- Rows: 150
- Queries: 50
- Schema errors: 0
- Failure query ids: q009, q010, q011, q012, q013, q014, q015, q016, q017, q018, q019, q043, q044, q047, q048

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 50 | 50 | 0 | 15 | 12557.05 | 21813.27 | 12557.1 | 21813.27 |
| hybrid_without_refusal | 50 | 42 | 8 | 15 | 12467.8 | 21462.23 | 12359.2 | 21438.53 |
| full_hybrid | 50 | 27 | 23 | 0 | 13660.3 | 21766.76 | 10910.45 | 20669.22 |

Environment:

{
  "cold_start_rows": 0,
  "warmup_rows": 0,
  "warm_rows": 150,
  "tab_backgrounded_rows": 71,
  "long_task_gc_rows": 150,
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
    "count": 15
  },
  {
    "condition": "hybrid_without_refusal",
    "fail_keys": [
      "refusal_expected_alignment"
    ],
    "count": 15
  }
]

