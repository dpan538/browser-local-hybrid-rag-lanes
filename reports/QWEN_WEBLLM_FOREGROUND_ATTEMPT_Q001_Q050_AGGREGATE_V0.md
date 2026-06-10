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

- `runs/qwen_webllm_foreground_q001_q010_v0/qwen_webllm_foreground_q001_q010_v0_records.jsonl`: 30 rows, 10 queries, range q001-q010
- `runs/qwen_webllm_foreground_q011_q020_v0/qwen_webllm_foreground_q011_q020_v0_records.jsonl`: 30 rows, 10 queries, range q011-q020
- `runs/qwen_webllm_foreground_q021_q035_v0/qwen_webllm_foreground_q021_q035_v0_records.jsonl`: 45 rows, 15 queries, range q021-q035
- `runs/qwen_webllm_foreground_q036_q050_v0/qwen_webllm_foreground_q036_q050_v0_records.jsonl`: 45 rows, 15 queries, range q036-q050

## Condition Summary

| Condition | Rows | Qwen rows | Skip rows | Failures | Generation errors | Timeouts | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 50 | 50 | 0 | 15 | 0 | 0 | 9939.65 | 12284.34 | 9939.7 | 12284.39 |
| hybrid_without_refusal | 50 | 42 | 8 | 15 | 0 | 0 | 10346.25 | 12415.41 | 9878.4 | 12253.05 |
| full_hybrid | 50 | 27 | 23 | 0 | 0 | 0 | 10860.1 | 12576.74 | 6036.1 | 12113.65 |

## Environment

{
  "cold_start_rows": 4,
  "warmup_rows": 0,
  "warm_rows": 150,
  "tab_backgrounded_rows": 18,
  "long_task_gc_rows": 5,
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
    1938.2,
    2014.2,
    2122.6,
    2127.7
  ]
}
