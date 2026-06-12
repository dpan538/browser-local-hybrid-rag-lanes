# Experiment Status

Updated: 2026-06-12

This file is the paper-facing status ledger for the hybrid answer-lane
allocation study. It separates current exploratory evidence from claims that
would require a Paper v1 freeze, source-audited evidence, and blinded human
review.

## Current State

The repository has a clean exploratory 50-query WebLLM/Qwen instrumentation
aggregate:

- 50 queries x 3 conditions = 150 rows.
- Primary model identity: `Qwen/Qwen3.5-0.8B`.
- WebLLM runtime id: `Qwen3.5-0.8B-q4f16_1-MLC`.
- Schema errors: 0.
- Duplicate query-condition pairs: 0.
- Missing query-condition pairs: 0.
- `tab_backgrounded_rows`: 0.
- `long_task_gc_rows`: 5.
- Contract failures:
  - `all_generation`: 15.
  - `hybrid_without_refusal`: 15.
  - `full_hybrid`: 0.

Evidence:

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
| Qwen/WebLLM browser run | Exploratory clean 50-query aggregate complete | Repeat or preserve under a Paper v1 freeze manifest. |
| Fixture | Synthetic, not source-audited | Build source-audited or public-derived fixture before evidence-correctness claims. |
| Automatic contract checks | Ready for exploratory contract analysis | Freeze checker version and include in manifest. |
| Latency evidence | Exploratory, clean of tab-background rows | Report cold/warm, long-task flags, and segmented-run provenance. |
| Human review | Not complete | Add two-rater blinded review with simple rubric. |
| Usability claim | Blocked | Requires blinded human review. |
| Rights/source correctness claim | Blocked | Requires source audit; deterministic rendering only preserves supplied evidence. |
| Journal-ready package | Not ready | Needs source-audited fixture, freeze manifest, clean run, human review, and final claim ledger. |

## Current Best-Supported Statement

In a controlled synthetic 50-query exploratory fixture, full hybrid lane
allocation eliminated the observed automatic refusal-alignment contract
failures, while all-generation and hybrid-without-refusal each retained 15
automatic contract failures.

Boundary:

- synthetic fixture;
- no source audit;
- no blinded human usability review;
- no general browser-local RAG quality claim;
- no legal rights correctness claim.

## Next Gate

The next methodological step is Paper v1 Freeze, not more scattered diagnostic
runs.

Paper v1 must define:

- frozen fixture and fixture provenance;
- frozen rule table and prompt pack;
- frozen browser/model/hardware configuration;
- frozen automatic analysis scripts;
- blinded human review pack and reviewer instructions;
- final artifact index;
- claim and non-claim ledger.
