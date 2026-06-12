# Final Artifact Index

Updated: 2026-06-12

This file tracks the artifact set needed for a paper-facing run. Items marked
exploratory are useful evidence but are not, by themselves, journal-ready.

## Current Exploratory Artifacts

| Artifact | Path | Status |
|---|---|---|
| Clean q001-q050 Qwen aggregate report | `reports/QWEN_WEBLLM_FOREGROUND_CLEAN_Q001_Q050_AGGREGATE_V0.md` | Exploratory clean aggregate |
| Clean q001-q050 Qwen aggregate JSON | `reports/qwen_webllm_foreground_clean_q001_q050_aggregate_v0.json` | Exploratory clean aggregate |
| q001-q010 raw run | `runs/qwen_webllm_foreground_q001_q010_v0/qwen_webllm_foreground_q001_q010_v0_records.jsonl` | Exploratory raw evidence |
| q011-q020 raw run | `runs/qwen_webllm_foreground_q011_q020_v0/qwen_webllm_foreground_q011_q020_v0_records.jsonl` | Exploratory raw evidence |
| q021-q035 raw run | `runs/qwen_webllm_foreground_q021_q035_v0/qwen_webllm_foreground_q021_q035_v0_records.jsonl` | Exploratory raw evidence |
| q036-q042 focus raw run | `runs/qwen_webllm_foreground_q036_q042_focus_v0/qwen_webllm_foreground_q036_q042_focus_v0_records.jsonl` | Exploratory raw evidence |
| q043-q050 split raw run | `runs/qwen_webllm_foreground_q043_q050_split_v0/qwen_webllm_foreground_q043_q050_split_v0_records.jsonl` | Exploratory raw evidence |
| Fixture quality audit | `reports/FIXTURE_QUALITY_AUDIT_V0.md` | Documents paper blockers |
| Promotion gate | `reports/PROMOTION_GATE_V0.md` | Exploratory pass, paper blocked |
| Protocol freeze v0 | `docs/PROTOCOL_FREEZE_V0.md` | Existing gate, needs Paper v1 refresh |

## Required Paper v1 Artifacts

| Artifact | Target Path | Status |
|---|---|---|
| Source-audited fixture | `fixtures/source_audited_50/` | Missing |
| Runtime view for Paper v1 | `fixtures/source_audited_50/runtime_view.jsonl` | Missing |
| Evaluation view for Paper v1 | `fixtures/source_audited_50/evaluation_view.jsonl` | Missing |
| Warmup queries for Paper v1 | `fixtures/source_audited_50/warmup_queries.jsonl` | Missing |
| Freeze manifest | `manifests/protocol_v1_freeze_manifest.json` | Missing |
| Paper v1 raw run records | `runs/paper_v1_qwen_webllm_50_clean/` | Missing |
| Paper v1 aggregate report | `reports/PAPER_V1_QWEN_WEBLLM_50_AGGREGATE.md` | Missing |
| Blind review pack | `review/paper_v1_blind_pack.json` | Missing |
| Reviewer A scores | `review/paper_v1_reviewer_A.jsonl` | Missing |
| Reviewer B scores | `review/paper_v1_reviewer_B.jsonl` | Missing |
| Human review summary | `reports/HUMAN_REVIEW_SUMMARY_PAPER_V1.md` | Missing |
| Final claim ledger | `reports/PAPER_V1_CLAIM_LEDGER.md` | Missing |

## Artifact Rule

A result is paper-facing only if every input artifact has a freeze-manifest
hash and every output artifact is listed here with its exact run identity.
