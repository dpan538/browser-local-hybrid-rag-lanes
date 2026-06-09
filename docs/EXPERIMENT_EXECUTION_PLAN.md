# Experiment Execution Plan

Generated: 2026-06-09

This plan describes the first reproducible browser-local hybrid lane pilot.
It assumes the experiment is operated in the Codex in-app browser against a
local Flask API and panel, not in Chrome and not against archive product
runtime.

## Goal

Run a controlled pilot for hybrid answer-lane methodology:

- compare all-generation, hybrid-without-refusal, and full-hybrid conditions;
- preserve identical evidence packets across conditions;
- capture latency, output, contract metrics, and reviewer checklist fields;
- keep runtime-visible fixture data separate from evaluator-only labels.

The pilot is exploratory unless the fixture, rule table, prompt packs, and
analysis plan are frozen before the run.

## Local Environment Setup

Create and use the repo-local virtual environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Validate the master fixture:

```bash
.venv/bin/python scripts/validate_fixture.py fixtures/experiment_fixture.jsonl
```

Validate the protocol bundle:

```bash
.venv/bin/python scripts/validate_protocol_bundle.py
```

Export runtime and evaluation views:

```bash
.venv/bin/python scripts/split_fixture_views.py \
  fixtures/experiment_fixture.jsonl \
  fixtures/runtime_view/experiment_fixture.runtime.jsonl \
  fixtures/evaluation_view/experiment_fixture.eval.jsonl
```

## API Runner And Experiment Panel

Start the local Flask runner:

```bash
.venv/bin/python app.py
```

Open this URL in the Codex in-app browser:

```text
http://127.0.0.1:8787/tools/experiment_panel/
```

If Codex browser blocks local URLs in the current session, treat that as an
environment setup blocker rather than switching to Chrome. The panel remains a
static local artifact; the intended browser surface is Codex browser once local
URL access is available.

The panel calls:

- `GET /api/health`
- `GET /api/fixtures/runtime`
- `GET /api/fixtures/evaluation`
- `POST /api/run`

Runtime mode uses only runtime view fields. Reviewer/evaluation fields are
separate and should remain hidden until output collection is complete.

The default model backend is a timed stub. It is for protocol and UI
verification only; it does not download model weights and does not represent
real Qwen/WebLLM latency. A real local model backend can replace the stub when
the protocol is ready.

## Pre-Run Freeze Checklist

Before a paper-facing run, record content hashes for:

- master fixture;
- runtime fixture view;
- evaluation fixture view;
- `config/lane_rules_v1.yaml`;
- `config/refusal_decision_matrix.csv`;
- condition prompt pack;
- analysis plan;
- environment-stability schema.

For the exploratory sample panel run, this checklist is used as a rehearsal.

Generate the manifest:

```bash
.venv/bin/python scripts/freeze_manifest.py
```

See `docs/PROTOCOL_FREEZE_V0.md` for the paper-facing freeze gate. A run is
only paper-facing if the freeze manifest has no missing files and all
condition, fixture, rule, refusal, prompt, and analysis artifacts are frozen
before output collection.

## Condition Definitions

Condition 1: all-generation

- Same visible answer sections as hybrid conditions.
- The local model generates all field values and caveats.
- No deterministic parser rescue or post-hoc field repair.

Condition 2: hybrid without refusal

- Exact source/rights/provenance fields are deterministic.
- Research guidance remains generative.
- Refusal remains a model responsibility.

Condition 3: full hybrid

- Exact source/rights/provenance fields are deterministic.
- Mandatory insufficient-evidence refusal is deterministic.
- Research guidance and mixed-intent synthesis remain generative or compound.

Optional diagnostic:

- deterministic-only subset for exact-field and refusal-eligible rows.
- not a primary baseline.

## Manual Panel Run Sequence

1. Validate fixture and regenerate runtime/eval views.
2. Start the Flask runner with `.venv/bin/python app.py`.
3. Open the panel in Codex browser.
4. Confirm fixture row count and runtime/eval separation.
5. Select a query and condition.
6. Click `Run Condition`.
7. The API returns answer, timings, environment flags, and auto-contract
   checks.
8. Export the run record JSON if doing a panel demonstration.
9. Repeat for each condition with randomized or counterbalanced order.
10. After output collection, switch to evaluator labels for review.

Manual paste is no longer part of measured runs. If a human pastes output for
demonstration, mark the row as non-measured.

## Full Automated Pilot Sequence

Start the Flask runner, then from another shell:

```bash
.venv/bin/python scripts/run_full_pilot.py
.venv/bin/python scripts/auto_contract_check.py
.venv/bin/python scripts/prepare_blind_review.py
.venv/bin/python scripts/merge_blind_review.py
.venv/bin/python scripts/analysis.py
```

Outputs:

- `runs/collected_records.jsonl`
- `runs/auto_evaluated_records.jsonl`
- `review/blind_pack.json`
- `review/blind_mapping.json`
- `review/unblinded_review_records.jsonl`
- `runs/analysis_summary.md`

The full pilot script uses `POST /api/run` for every query x condition pair,
so timing and condition logic are controlled by the same runner as the panel.

## Warmup And Latency Policy

For a measured run:

- run one cold-start trial separately;
- run five warmup queries from `fixtures/warmup_queries.jsonl` before the warm
  block;
- keep the first measured warm query marked separately if residual warmup is
  visible;
- keep anomaly-flagged rows in primary results;
- use anomaly exclusions only in a labeled sensitivity analysis.

Report:

- median;
- IQR;
- P90;
- maximum;
- anomaly counts;
- raw P95 only as descriptive, not as a success claim.

## Review Policy

Use automatic contract checks before human review:

- source/rights/status fields rendered;
- hybrid deterministic fields equal the runtime evidence values;
- source pointer preserved;
- conflict surfaced when present;
- placeholders used when required.

Human review should focus on residual perception-oriented dimensions.

Use checklist-first review:

- contract pass/warning/failure;
- all required fields rendered;
- placeholders used when required;
- no field mutation;
- no unsupported rights/status/provenance upgrade;
- source pointer preserved;
- conflict surfaced when present.

Use 1-5 scores only for perception-oriented dimensions:

- helpfulness;
- refusal clarity;
- source clarity;
- rights clarity;
- research usefulness;
- format consistency.

Reviewer labels should be blinded to condition names where feasible.
Use `scripts/prepare_blind_review.py` after collecting run records.

## Analysis Plan

Primary planned contrasts:

1. Condition 1 vs Condition 2: deterministic evidence-field delivery.
2. Condition 2 vs Condition 3: deterministic refusal.

Use paired-by-query analysis:

- McNemar-style exact paired tests for binary contract/refusal outcomes;
- Wilcoxon signed-rank or paired permutation for latency and ordinal scores;
- paired effect sizes and confidence intervals before p-value rhetoric.

The first 50-query run is exploratory unless a sealed evaluation fixture and
pre-registered rule table are in place.

## Claims Allowed After Pilot

Allowed:

- field-fidelity differences on the controlled fixture;
- under-refusal and over-refusal tradeoffs on the controlled fixture;
- warm end-to-end latency differences on the pinned local setup;
- mixed-intent failure modes as descriptive evidence.

Forbidden:

- semantic correctness of deterministic answers;
- legal rights determination;
- universal browser-local speed claims;
- statistical superiority from 50 rows;
- claims that Qwen generation is faster when generation was skipped.
