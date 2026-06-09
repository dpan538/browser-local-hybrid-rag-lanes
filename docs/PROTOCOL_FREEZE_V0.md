# Protocol Freeze V0

Generated: 2026-06-09

This document defines the minimum artifact bundle that must be frozen before a
paper-facing hybrid answer-lane run. It is stricter than the smoke-test runner:
smoke runs verify plumbing, while paper-facing runs support claims.

## Freeze Bundle

The following files are part of the v0 protocol bundle:

- `fixtures/experiment_fixture.jsonl`
- `fixtures/runtime_view/experiment_fixture.runtime.jsonl`
- `fixtures/evaluation_view/experiment_fixture.eval.jsonl`
- `fixtures/warmup_queries.jsonl`
- `config/lane_rules_v1.yaml`
- `config/refusal_decision_matrix.csv`
- `config/condition_prompt_pack_v1.json`
- `docs/EXPERIMENT_EXECUTION_PLAN.md`
- `docs/PROTOCOL_FREEZE_V0.md`
- `schemas/run_record_schema.json`
- `schemas/environment_stability_log_schema.json`
- `schemas/condition_prompt_pack_schema.json`

The freeze manifest is generated with:

```bash
.venv/bin/python scripts/freeze_manifest.py
```

Any change to a freeze-bundle file after manifest generation creates a new
protocol version or a new exploratory run.

## Condition-Locked Prompt Pack

`config/condition_prompt_pack_v1.json` defines the visible answer sections and
condition-specific prompt constraints. It is not meant to make the stub backend
realistic. It exists so all later model backends use the same condition
contract.

The prompt pack enforces:

- same visible answer sections across all conditions;
- no deterministic field rescue in the all-generation baseline;
- deterministic field rendering in both hybrid conditions;
- deterministic refusal only in the full-hybrid condition.

## Run Eligibility

A run can be treated as paper-facing only if:

- the freeze manifest has no missing files;
- runtime and evaluation fixture views were regenerated from the same master
  fixture before the manifest was created;
- the Codex in-app browser is the browser surface for panel-mediated runs;
- the model backend is declared in run metadata;
- warmup rows are separate from measured rows;
- anomaly flags remain in the primary record;
- generated run outputs are preserved under an explicitly named run directory.

Smoke runs are useful for development but cannot support empirical claims.

## Reviewer Flow

1. Generate run records with `scripts/run_full_pilot.py`.
2. Run automatic contract checks with `scripts/auto_contract_check.py`.
3. Generate blinded review items with `scripts/prepare_blind_review.py`.
4. Reviewers score only blinded items.
5. Merge blinded scores back to true conditions with
   `scripts/merge_blind_review.py`.
6. Run paired analysis after the review merge.

Reviewers must not see condition names, rule traces, or latency fields during
primary perception scoring.

## Calibration Gate

Before scoring a full set, reviewers independently score the calibration items
in `review/golden_answers.json`. The calibration set must contain at least
eight examples covering:

- exact source/rights rendering;
- missing evidence refusal;
- partial evidence qualified answers;
- compound deterministic-plus-generative answers;
- contradictory evidence;
- missing deterministic fields and placeholders;
- format-matched all-generation baseline review.

If reviewer disagreement exceeds one point on any 1-5 perception dimension, the
rubric examples should be revised before the full review begins.

## Output Hygiene

The repository ignores default generated outputs under `runs/` and the default
blind review files. Paper-facing outputs should be copied into a named
subdirectory and added intentionally only after the run is declared frozen.

Do not commit:

- model weights;
- browser caches;
- downloaded images;
- product-specific archive runtime state;
- local cookies, credentials, or session files.
