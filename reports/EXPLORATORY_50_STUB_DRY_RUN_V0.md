# Exploratory 50-Query Stub Dry Run v0

Date: 2026-06-10

This memo records the first end-to-end dry run over the 50-query draft fixture.
It is an engineering and protocol-reproducibility check, not a paper-facing
model result. The run used the Flask experiment API with the `stub` local-model
backend, synthetic fixture records, and the draft runtime/evaluation views.

## Purpose

The dry run tested whether the current experimental pipeline can execute the
declared three-condition ablation without manual answer pasting:

- condition 1: all-generation;
- condition 2: hybrid without deterministic refusal;
- condition 3: full hybrid with deterministic field rendering and deterministic
  refusal.

The run also tested whether post-hoc automatic contract checking can distinguish
deterministic field failures from legitimate deterministic refusals.

## Inputs

Draft fixture inputs:

- `fixtures/drafts/compiled_experiment_fixture_v0.jsonl`
- `fixtures/drafts/runtime_view_v0.jsonl`
- `fixtures/drafts/evaluation_view_v0.jsonl`
- `fixtures/drafts/warmup_queries_v0.jsonl`

Protocol inputs:

- `config/lane_rules_v1.yaml`
- `config/refusal_decision_matrix.csv`
- `config/condition_prompt_pack_v1.json`
- `schemas/run_record_schema.json`

Generated run outputs were written under `runs/exploratory_50_stub_v0/`. That
directory is intentionally ignored because raw run records are exploratory
artifacts and should not be committed by default.

## Commands

Server paths were overridden so the Flask API used the 50-row draft fixture
rather than the one-row smoke fixture:

```bash
HYBRID_LANE_MASTER_FIXTURE_PATH=fixtures/drafts/compiled_experiment_fixture_v0.jsonl \
HYBRID_LANE_RUNTIME_PATH=fixtures/drafts/runtime_view_v0.jsonl \
HYBRID_LANE_EVAL_PATH=fixtures/drafts/evaluation_view_v0.jsonl \
HYBRID_LANE_WARMUP_PATH=fixtures/drafts/warmup_queries_v0.jsonl \
.venv/bin/python app.py
```

The measured run used five warmup queries followed by the 50 query x 3
condition grid:

```bash
.venv/bin/python scripts/run_full_pilot.py \
  --runtime fixtures/drafts/runtime_view_v0.jsonl \
  --warmup fixtures/drafts/warmup_queries_v0.jsonl \
  --output runs/exploratory_50_stub_v0/collected_records.jsonl \
  --run-id exploratory_50_stub_v0 \
  --sleep-ms 5
```

Post-processing:

```bash
.venv/bin/python scripts/auto_contract_check.py \
  --records runs/exploratory_50_stub_v0/collected_records.jsonl \
  --runtime fixtures/drafts/runtime_view_v0.jsonl \
  --output runs/exploratory_50_stub_v0/auto_evaluated_records.jsonl \
  --blueprint fixtures/drafts/fixture_expansion_blueprint_v0.jsonl

.venv/bin/python scripts/analysis.py \
  --records runs/exploratory_50_stub_v0/auto_evaluated_records.jsonl \
  --output runs/exploratory_50_stub_v0/analysis_summary.md

.venv/bin/python scripts/prepare_blind_review.py \
  --records runs/exploratory_50_stub_v0/auto_evaluated_records.jsonl \
  --output runs/exploratory_50_stub_v0/blind_pack.json \
  --mapping runs/exploratory_50_stub_v0/blind_mapping.json
```

## Pipeline Findings

The run produced 150 measured records:

| Item | Count |
| --- | ---: |
| unique queries | 50 |
| all-generation records | 50 |
| hybrid-without-refusal records | 50 |
| full-hybrid records | 50 |

Execution-mode distribution:

| Execution mode | Count |
| --- | ---: |
| generative_answer | 103 |
| compound_answer | 16 |
| deterministic_render | 16 |
| deterministic_refusal | 15 |

Contract-failure distribution after automatic post-hoc checking:

| Condition | Contract failures |
| --- | ---: |
| all_generation | 15 |
| hybrid_without_refusal | 15 |
| full_hybrid | 0 |

The 15 failures in conditions 1 and 2 correspond to refusal-expected rows that
did not produce a refusal. Condition 3 satisfied those rows through the
deterministic refusal lane.

## Paired Analysis

The descriptive paired analysis reported 50 paired queries for both contrasts.
These p-values are implementation smoke indicators only because the backend is a
timed stub and the fixture is synthetic.

| Contrast | Contract discordant pairs | Left fail / right pass | Left pass / right fail | Exact paired binomial p |
| --- | ---: | ---: | ---: | ---: |
| all_generation vs hybrid_without_refusal | 0 | 0 | 0 | 1.0000 |
| hybrid_without_refusal vs full_hybrid | 15 | 15 | 0 | 0.0001 |

Stub latency medians were close across conditions and are not interpretable as
WebLLM/Qwen latency:

| Condition | Median total latency |
| --- | ---: |
| all_generation | approximately 84 ms |
| hybrid_without_refusal | approximately 83 ms |
| full_hybrid | approximately 81 ms |

## Fixes Triggered By The Dry Run

The dry run exposed three protocol/runtime issues that were fixed before this
memo:

- The Flask app originally loaded only the default one-row fixture paths. It now
  accepts environment-variable path overrides and reports active fixture paths
  in `/api/health`.
- Automatic contract checking originally penalized deterministic refusals for
  not rendering source/rights fields. Refused answers now mark deterministic
  field-rendering and mutation checks as `n/a`.
- Full-hybrid refusal routing originally refused only `missing` and
  `contradictory` evidence states. It now refuses `partial` evidence when the
  fixture intent signal is `refusal_required`, which covers first/earliest
  claims without adequate chronology proof.

## Limitations

This run must not be cited as evidence that hybrid lanes improve real
browser-local model quality or latency.

Remaining blockers for paper-facing claims:

- The local generation backend was `stub`, not WebLLM/Qwen.
- Fixture records remain synthetic and not source-audited.
- No human or LLM-as-judge perception review was run.
- The dry run does not exercise browser WebGPU dispatch, cold-start model load,
  or real local retrieval.
- Raw run artifacts are exploratory and ignored rather than committed.

## Next Experimental Step

The next step is to preserve this automation pipeline while replacing only the
generation backend and evidence source:

- keep the same 50-query x 3-condition harness;
- run a small real-browser/local-model subset first, preferably 5 to 10 queries;
- record cold-start and warm-run states separately;
- keep automatic contract checking as the primary compliance signal;
- add source-audited records before making evidence-correctness claims;
- use the blind-review pack only for usability/perception dimensions.
