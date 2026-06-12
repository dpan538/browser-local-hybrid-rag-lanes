# Experiment Status

Updated: 2026-06-12

This file is the paper-facing status ledger for the hybrid answer-lane
allocation study. It separates current diagnostic evidence from claims that
would require a larger Paper v1 freeze and blinded human review.

## Current State

The repository now has two complete 50-query WebLLM/Qwen instrumentation
aggregates:

1. a clean synthetic exploratory aggregate;
2. a source-audited 50-query diagnostic aggregate.

Current source-audited diagnostic aggregate:

- 50 queries x 3 conditions = 150 rows.
- Primary model identity: `Qwen/Qwen3.5-0.8B`.
- WebLLM runtime id: `Qwen3.5-0.8B-q4f16_1-MLC`.
- Schema errors: 0.
- Duplicate query-condition pairs: 0.
- Missing query-condition pairs: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 64.
- Contract failures:
  - `all_generation`: 10.
  - `hybrid_without_refusal`: 10.
  - `full_hybrid`: 0.

Evidence:

- `reports/QWEN_WEBLLM_SOURCE_AUDITED_50_AGGREGATE_V0.md`
- `reports/qwen_webllm_source_audited_50_aggregate_v0.json`
- `reports/QWEN_WEBLLM_SOURCE_AUDITED_50_SUMMARY_V0.md`

The earlier synthetic clean aggregate remains useful for protocol comparison:

- `reports/QWEN_WEBLLM_FOREGROUND_CLEAN_Q001_Q050_AGGREGATE_V0.md`
- `reports/qwen_webllm_foreground_clean_q001_q050_aggregate_v0.json`

## Publication Target State

The active publication route is:

```text
Journal of Information Science -> The Electronic Library ->
Open Information Science / Digital Library Perspectives
```

Online Information Review and Aslib Journal of Information Management remain
stretch targets only.

The minimum JIS candidate requires 200 source-audited queries, 600 condition
outputs, a frozen protocol manifest, all-output automatic contract metrics,
paired analysis by query, and two-rater blinded semantic review on 180 sampled
outputs. A 300-query run remains the preferred stronger version if time allows.

## Readiness Ledger

| Item | Current Status | Paper v1 Requirement |
|---|---|---|
| Research question | Ready | Keep framed as answer execution policy, not general RAG quality. |
| Three-condition ablation | Ready for exploratory use | Freeze condition prompt pack before paper run. |
| Qwen/WebLLM browser run | Source-audited 50-query diagnostic aggregate complete | Scale to 200-query JIS candidate or freeze as calibration-only. |
| Fixture | Source-audited 50-query gate complete | Expand to 200 source-audited queries before JIS claim level. |
| Automatic contract checks | Ready for exploratory contract analysis | Freeze checker version and include in manifest. |
| Latency evidence | Source-audited run has 0 tab-background rows but 64 long-task rows | Report cold/warm, long-task flags, and avoid strong latency claims. |
| Human review | Not complete | Add two-rater blinded review with simple rubric. |
| Usability claim | Blocked | Requires blinded human review. |
| Rights/source correctness claim | Blocked | Requires source audit; deterministic rendering only preserves supplied evidence. |
| Journal-ready package | Not ready | Needs source-audited fixture, freeze manifest, clean run, human review, and final claim ledger. |

## Current Best-Supported Statement

In a controlled source-audited 50-query diagnostic fixture, full hybrid lane
allocation eliminated the observed automatic refusal-alignment contract
failures, while all-generation and hybrid-without-refusal each retained 10
automatic refusal-alignment failures.

Boundary:

- no blinded human usability review;
- 50-query diagnostic scale, not the 200-query JIS candidate scale;
- metadata-level source audit only, not legal rights determination;
- no general browser-local RAG quality claim;
- latency is foreground-clean but long-task-diagnostic.

## Next Gate

The next methodological step is source-audited review preparation, not
immediate paper drafting.

The next gate should define:

- blind review pack from the source-audited run;
- small calibration review;
- adjudication rubric for partial-evidence and mixed-intent rows;
- decision on whether this 50-query run remains calibration-only or becomes a
  frozen pilot artifact;
- blinded human review pack and reviewer instructions;
- final artifact index;
- claim and non-claim ledger.
