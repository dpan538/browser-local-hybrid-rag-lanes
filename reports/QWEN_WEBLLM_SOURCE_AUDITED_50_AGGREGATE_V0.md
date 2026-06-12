# Qwen WebLLM Aggregated Run Diagnostics

This aggregate treats segmented run records as experimental
instrumentation data, not paper-ready findings.

## Coverage

- Rows: 150
- Queries: 50
- Schema errors: 0
- Duplicate query-condition pairs: 0
- Missing query-condition pairs: 0
- Failure query ids: q016, q017, q018, q019, q020, q035, q036, q037, q038, q049

Inputs:

- `runs/qwen_webllm_source_audited_50_v0/qwen_webllm_source_audited_50_v0_records.jsonl`: 150 rows, 50 queries, range q001-q050

## Condition Summary

| Condition | Rows | Qwen rows | Skip rows | Failures | Generation errors | Timeouts | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all_generation | 50 | 50 | 0 | 10 | 0 | 0 | 13957.45 | 17645.81 | 13957.5 | 17645.81 |
| hybrid_without_refusal | 50 | 40 | 10 | 10 | 0 | 0 | 14505.45 | 19290.83 | 12691.45 | 18663.34 |
| full_hybrid | 50 | 30 | 20 | 0 | 0 | 0 | 14703.5 | 18471.53 | 11368.45 | 17519.05 |

## Environment

{
  "cold_start_rows": 1,
  "warmup_rows": 0,
  "warm_rows": 150,
  "tab_backgrounded_rows": 0,
  "long_task_gc_rows": 64,
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

## Model

{
  "qwen_model_meta_rows": 120,
  "deterministic_meta_rows": 30,
  "model_ids": [
    "Qwen3.5-0.8B-q4f16_1-MLC"
  ],
  "primary_model_identities": [
    "Qwen/Qwen3.5-0.8B"
  ],
  "model_load_ms_values": [
    2014.9
  ]
}
