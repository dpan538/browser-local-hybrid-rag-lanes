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

## qwen_webllm_q021_q025_microbatch_v0_records

- Rows: 15
- Queries: 5
- Schema errors: 0
- Failure query ids: none

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 5 | 5 | 0 | 0 | 11574.7 | 20896.94 | 11574.7 | 20897.04 |
| hybrid_without_refusal | 5 | 5 | 0 | 0 | 11318.8 | 17102.52 | 11318.8 | 17102.64 |
| full_hybrid | 5 | 5 | 0 | 0 | 9677.2 | 14557.46 | 9677.2 | 14557.54 |

Environment:

{
  "cold_start_rows": 0,
  "warmup_rows": 0,
  "warm_rows": 15,
  "tab_backgrounded_rows": 2,
  "long_task_gc_rows": 1,
  "network_variance_rows": 0,
  "manual_interruption_rows": 0
}

Failure groups:

[]

## qwen_webllm_q026_q030_microbatch_v0_records

- Rows: 15
- Queries: 5
- Schema errors: 0
- Failure query ids: none

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 5 | 5 | 0 | 0 | 10878.4 | 11204.04 | 10878.5 | 11204.04 |
| hybrid_without_refusal | 5 | 5 | 0 | 0 | 11036.4 | 11918.58 | 11036.4 | 11918.58 |
| full_hybrid | 5 | 5 | 0 | 0 | 11265.7 | 11908.42 | 11265.8 | 11908.44 |

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

## qwen_webllm_q031_q035_microbatch_v0_records

- Rows: 15
- Queries: 5
- Schema errors: 0
- Failure query ids: none

| Condition | Rows | Qwen rows | Skip rows | Failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 5 | 5 | 0 | 0 | 14682.9 | 17202.18 | 14683.0 | 17202.18 |
| hybrid_without_refusal | 5 | 5 | 0 | 0 | 8681.4 | 17083.18 | 8681.4 | 17083.18 |
| full_hybrid | 5 | 5 | 0 | 0 | 16675.5 | 19158.8 | 16675.5 | 19158.88 |

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

