# Qwen WebLLM Aggregated Run Diagnostics

This aggregate treats segmented run records as experimental
instrumentation data, not paper-ready findings.

## Coverage

- Rows: 150
- Queries: 50
- Schema errors: 0
- Duplicate query-condition pairs: 0
- Missing query-condition pairs: 0
- Failure query ids: q009, q010, q011, q012, q013, q014, q015, q016, q017, q018, q019, q043, q044, q047, q048

Inputs:

- `runs/qwen_webllm_cleaner50_v0/qwen_webllm_cleaner50_v0_records.jsonl`: 60 rows, 20 queries, range q001-q020
- `runs/qwen_webllm_q021_q025_microbatch_v0/qwen_webllm_q021_q025_microbatch_v0_records.jsonl`: 15 rows, 5 queries, range q021-q025
- `runs/qwen_webllm_q026_q030_microbatch_v0/qwen_webllm_q026_q030_microbatch_v0_records.jsonl`: 15 rows, 5 queries, range q026-q030
- `runs/qwen_webllm_q031_q035_microbatch_v0/qwen_webllm_q031_q035_microbatch_v0_records.jsonl`: 15 rows, 5 queries, range q031-q035
- `runs/qwen_webllm_q036_q040_microbatch_v0/qwen_webllm_q036_q040_microbatch_v0_records.jsonl`: 15 rows, 5 queries, range q036-q040
- `runs/qwen_webllm_q041_q050_microbatch_v0/qwen_webllm_q041_q050_microbatch_v0_records.jsonl`: 30 rows, 10 queries, range q041-q050

## Condition Summary

| Condition | Rows | Qwen rows | Skip rows | Failures | Generation errors | Timeouts | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 50 | 50 | 0 | 15 | 0 | 0 | 10880.7 | 21242.6 | 10880.75 | 21242.7 |
| hybrid_without_refusal | 50 | 42 | 8 | 15 | 0 | 0 | 9803.8 | 17390.17 | 8619.75 | 16571.53 |
| full_hybrid | 50 | 27 | 23 | 0 | 0 | 0 | 9896.5 | 18954.45 | 6627.05 | 17846.34 |

## Environment

{
  "cold_start_rows": 1,
  "warmup_rows": 0,
  "warm_rows": 150,
  "tab_backgrounded_rows": 77,
  "long_task_gc_rows": 2,
  "network_variance_rows": 0,
  "manual_interruption_rows": 0
}

Latency boundary: this aggregate contains backgrounded rows, so
latency values are diagnostic only and should not be used as clean
latency evidence.

## Failure Groups

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

## Model

{
  "qwen_model_meta_rows": 119,
  "deterministic_meta_rows": 31,
  "model_ids": [
    "Qwen3.5-0.8B-q4f16_1-MLC"
  ],
  "primary_model_identities": [
    "Qwen/Qwen3.5-0.8B"
  ],
  "model_load_ms_values": [
    2036.0,
    2621.8
  ]
}
