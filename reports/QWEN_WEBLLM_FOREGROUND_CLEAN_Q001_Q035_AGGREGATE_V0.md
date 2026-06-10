# Qwen WebLLM Aggregated Run Diagnostics

This aggregate treats segmented run records as experimental
instrumentation data, not paper-ready findings.

## Coverage

- Rows: 105
- Queries: 35
- Schema errors: 0
- Duplicate query-condition pairs: 0
- Missing query-condition pairs: 0
- Failure query ids: q009, q010, q011, q012, q013, q014, q015, q016, q017, q018, q019

Inputs:

- `runs/qwen_webllm_foreground_q001_q010_v0/qwen_webllm_foreground_q001_q010_v0_records.jsonl`: 30 rows, 10 queries, range q001-q010
- `runs/qwen_webllm_foreground_q011_q020_v0/qwen_webllm_foreground_q011_q020_v0_records.jsonl`: 30 rows, 10 queries, range q011-q020
- `runs/qwen_webllm_foreground_q021_q035_v0/qwen_webllm_foreground_q021_q035_v0_records.jsonl`: 45 rows, 15 queries, range q021-q035

## Condition Summary

| Condition | Rows | Qwen rows | Skip rows | Failures | Generation errors | Timeouts | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 35 | 35 | 0 | 11 | 0 | 0 | 9941.8 | 12442.01 | 9941.9 | 12442.04 |
| hybrid_without_refusal | 35 | 27 | 8 | 11 | 0 | 0 | 10758.2 | 12680.7 | 9962.8 | 12540.7 |
| full_hybrid | 35 | 16 | 19 | 0 | 0 | 0 | 10956.8 | 12713.33 | 0.0 | 12409.09 |

## Environment

{
  "cold_start_rows": 3,
  "warmup_rows": 0,
  "warm_rows": 105,
  "tab_backgrounded_rows": 0,
  "long_task_gc_rows": 3,
  "network_variance_rows": 0,
  "manual_interruption_rows": 0
}

## Failure Groups

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

## Model

{
  "qwen_model_meta_rows": 78,
  "deterministic_meta_rows": 27,
  "model_ids": [
    "Qwen3.5-0.8B-q4f16_1-MLC"
  ],
  "primary_model_identities": [
    "Qwen/Qwen3.5-0.8B"
  ],
  "model_load_ms_values": [
    1938.2,
    2014.2,
    2122.6
  ]
}
