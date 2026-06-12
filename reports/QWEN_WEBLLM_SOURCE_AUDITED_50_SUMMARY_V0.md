# Qwen WebLLM Source-Audited 50 Summary V0

Generated: 2026-06-12

This report summarizes the first complete browser-local
`Qwen3.5-0.8B-q4f16_1-MLC` run over the completed
`fixtures/source_audited_50/` gate. It is a source-audited experimental
diagnostic, not yet a paper-facing final result.

## Run Identity

| Field | Value |
|---|---|
| Run id | `qwen_webllm_source_audited_50_v0` |
| Runtime fixture | `fixtures/source_audited_50/runtime_view.jsonl` |
| Evaluation fixture | `fixtures/source_audited_50/evaluation_view.jsonl` |
| Query-condition rows | 150 |
| Query count | 50 |
| Conditions | `all_generation`, `hybrid_without_refusal`, `full_hybrid` |
| Primary model identity | `Qwen/Qwen3.5-0.8B` |
| WebLLM runtime id | `Qwen3.5-0.8B-q4f16_1-MLC` |

Raw run records remain local under ignored `runs/`.

## Coverage And Environment

| Metric | Value |
|---|---:|
| Rows saved | 150 |
| Queries covered | 50 |
| Schema errors | 0 |
| Duplicate query-condition pairs | 0 |
| Missing query-condition pairs | 0 |
| Generation errors | 0 |
| Timeouts | 0 |
| Tab-backgrounded rows | 0 |
| Long-task rows | 64 |

The run is clean for coverage and tab foregrounding. Latency should still be
treated cautiously because 64 rows recorded long-task events.

## Condition Summary

| Condition | Rows | Qwen rows | Skip rows | Contract failures | Qwen P50 ms | Qwen P95 ms | Hybrid P50 ms | Hybrid P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `all_generation` | 50 | 50 | 0 | 10 | 13957.45 | 17645.81 | 13957.50 | 17645.81 |
| `hybrid_without_refusal` | 50 | 40 | 10 | 10 | 14505.45 | 19290.83 | 12691.45 | 18663.34 |
| `full_hybrid` | 50 | 30 | 20 | 0 | 14703.50 | 18471.53 | 11368.45 | 17519.05 |

## Failure Pattern

Automatic contract failures occur only in the two conditions that do not enforce
the deterministic refusal lane:

| Condition | Failure group | Count |
|---|---|---:|
| `all_generation` | `refusal_expected_alignment` | 10 |
| `hybrid_without_refusal` | `refusal_expected_alignment` | 10 |
| `full_hybrid` | none | 0 |

Failure query ids:

```text
q016, q017, q018, q019, q020, q035, q036, q037, q038, q049
```

These are the missing-evidence and earliest/superlative refusal rows.

## Immediate Interpretation

The main replicated diagnostic signal is:

- `full_hybrid` removes observed refusal-alignment contract failures on the
  source-audited 50-query gate;
- `hybrid_without_refusal` preserves deterministic field rendering but still
  fails on missing-evidence refusal rows;
- `full_hybrid` reduces Qwen invocations from 50/50 in `all_generation` to
  30/50 by skipping deterministic exact and refusal rows.

This supports continued investigation of answer-lane allocation. It does not
yet establish human-perceived usefulness, semantic correctness of upstream
metadata, or journal-ready generalization.

## Next Checks

Before treating this as Paper v1 evidence, the next steps are:

1. Inspect representative failure and non-failure records for obvious checker
   artifacts.
2. Generate a source-audited blind review pack from this run.
3. Run a small calibration review before any formal two-rater review.
4. Decide whether to rerun for latency with long-task mitigation or keep
   latency as diagnostic only.
