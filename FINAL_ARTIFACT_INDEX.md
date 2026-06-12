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
| Source-audited fixture | `fixtures/source_audited_50/` | 50-query gate generated from 23 metadata records |
| Runtime view for Paper v1 | `fixtures/source_audited_50/runtime_view.jsonl` | Source-audited gate generated, 50 rows |
| Evaluation view for Paper v1 | `fixtures/source_audited_50/evaluation_view.jsonl` | Source-audited gate generated, 50 rows |
| Warmup queries for Paper v1 | `fixtures/source_audited_50/warmup_queries.jsonl` | First batch generated, 1 warmup row |
| Freeze manifest | `manifests/protocol_v1_freeze_manifest.json` | Missing |
| Paper v1 raw run records | `runs/paper_v1_qwen_webllm_50_clean/` | Missing |
| Source-audited 50 Qwen/WebLLM pre-run expectation | `docs/QWEN_WEBLLM_SOURCE_AUDITED_50_EXPECTATION_V0.md` | Added as pre-run backup |
| Paper v1 aggregate report | `reports/PAPER_V1_QWEN_WEBLLM_50_AGGREGATE.md` | Missing |
| Blind review pack | `review/paper_v1_blind_pack.json` | Missing |
| Reviewer A scores | `review/paper_v1_reviewer_A.jsonl` | Missing |
| Reviewer B scores | `review/paper_v1_reviewer_B.jsonl` | Missing |
| Human review summary | `reports/HUMAN_REVIEW_SUMMARY_PAPER_V1.md` | Missing |
| Final claim ledger | `reports/PAPER_V1_CLAIM_LEDGER.md` | Missing |
| Information Research target plan | `docs/INFORMATION_RESEARCH_TARGET_PLAN.md` | Superseded historical target |
| Source-audited expansion roadmap | `docs/SOURCE_AUDITED_EXPANSION_ROADMAP.md` | Added as methods roadmap |
| Journal target strategy | `docs/JOURNAL_TARGET_STRATEGY.md` | Active venue ladder |
| Paper v1 fixture provenance plan | `docs/PAPER_V1_FIXTURE_PROVENANCE_PLAN.md` | Added as provenance gate |
| Source family selection v0 | `docs/SOURCE_FAMILY_SELECTION_V0.md` | Added as first-batch source selection rationale |
| Source-audited 26-to-50 expansion expectation | `docs/SOURCE_AUDITED_50_26_TO_50_EXPANSION_EXPECTATION_V0.md` | Added as next expansion pre-run backup |
| Source-audited 15-row expansion summary | `reports/SOURCE_AUDITED_50_EXPANSION_15_SUMMARY_V0.md` | Added as post-run expansion summary |
| Source-audited 26-row structural expansion summary | `reports/SOURCE_AUDITED_50_STRUCTURAL_EXPANSION_26_SUMMARY_V0.md` | Added as structural expansion summary |
| Source-audited 50-query gate summary | `reports/SOURCE_AUDITED_50_GATE_50_SUMMARY_V0.md` | Added as first complete source-audited 50-query gate summary |
| Source audit manifest schema | `schemas/source_audit_manifest_schema.json` | Added as provenance validation schema |
| Source-audited query plan schema | `schemas/source_audited_query_plan_schema.json` | Added as query authoring schema |
| Source audit manifest validator | `scripts/validate_source_audit_manifest.py` | Added as provenance validation script |
| Source-audited query plan validator | `scripts/validate_source_audited_query_plan.py` | Added as query-plan validation script |
| Manifest/query sync checker | `scripts/sync_query_manifest.py` | Added as manifest/query alignment gate |
| Source-audited fixture compiler | `scripts/compile_source_audited_fixture.py` | Added as source-audit to fixture compiler |
| Source-audited consistency checker | `scripts/check_source_audited_consistency.py` | Added as cross-artifact validation |
| Source family registry | `config/source_families.yaml` | Added as source-family configuration |
| Freeze profile registry | `config/freeze_profiles.yaml` | Added as profile-driven freeze configuration |
| Paper v1 blind-pack generator | `scripts/generate_blind_pack.py` | Added as condition-hidden review export |
| Source-audited compiler smoke test | `scripts/smoke_source_audited_compile.py` | Added as end-to-end source-audit compile rehearsal |

## Artifact Rule

A result is paper-facing only if every input artifact has a freeze-manifest
hash and every output artifact is listed here with its exact run identity.
