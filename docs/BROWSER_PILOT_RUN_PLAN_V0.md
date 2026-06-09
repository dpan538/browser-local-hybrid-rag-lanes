# Browser Pilot Run Plan V0

This plan defines the first Codex in-app browser run for the hybrid answer-lane
experiment. It is smaller than the 50-query dry run and is intended to validate
browser-mediated execution, environment logging, and JSONL export before any
real WebLLM/Qwen claims.

## Scope

The browser pilot uses 10 queries selected from the 50-row draft runtime view:

| Query | Stratum | Intent | Evidence state | Refusal expected |
| --- | --- | --- | --- | --- |
| q001 | source_rights | source/rights | sufficient | false |
| q009 | no_evidence_refusal | refusal_required | missing | true |
| q015 | first_earliest_refusal | refusal_required | missing | true |
| q021 | comparison | comparison | partial | false |
| q027 | recommendation | recommendation | partial | false |
| q033 | explanation | explanation | sufficient | false |
| q041 | mixed_intent | mixed | sufficient | false |
| q042 | mixed_intent | mixed | partial | false |
| q044 | mixed_intent | mixed | contradictory | true |
| q047 | mixed_intent | mixed | missing | true |

The subset is stored as:

- `fixtures/drafts/browser_pilot_subset_v0.jsonl`

Regenerate it with:

```bash
.venv/bin/python scripts/select_browser_pilot_subset.py
```

## Server Setup

Use the 50-row draft views and explicit browser pilot subset:

```bash
HYBRID_LANE_MASTER_FIXTURE_PATH=fixtures/drafts/compiled_experiment_fixture_v0.jsonl \
HYBRID_LANE_RUNTIME_PATH=fixtures/drafts/runtime_view_v0.jsonl \
HYBRID_LANE_EVAL_PATH=fixtures/drafts/evaluation_view_v0.jsonl \
HYBRID_LANE_WARMUP_PATH=fixtures/drafts/warmup_queries_v0.jsonl \
HYBRID_LANE_BROWSER_PILOT_PATH=fixtures/drafts/browser_pilot_subset_v0.jsonl \
.venv/bin/python app.py
```

Then open:

```text
http://127.0.0.1:8787/tools/experiment_panel/
```

## Browser Panel Procedure

1. Confirm the header shows `10 pilot`.
2. Set `Run ID` to `browser_pilot_stub_v0` for the stub backend.
3. Click `Run Browser Pilot`.
4. The panel runs 10 queries x 3 conditions in sequence.
5. The panel automatically saves JSONL records through `/api/runs/save`.
6. The first measured browser call is marked `cold_start`; the remaining calls
   are marked `warm`.
7. The saved file path is reported in the `Run Record` panel.

Each run record includes:

- `env_flags.client_environment.visibility_state`;
- `env_flags.client_environment.was_backgrounded`;
- `env_flags.client_environment.long_task_count`;
- `env_flags.client_environment.user_agent`;
- `env_flags.client_environment.browser_pilot_sequence_index`;
- API-side contract metrics using evaluator-only refusal/conflict labels.

## Analysis

After the panel saves the JSONL under `runs/browser_pilot_stub_v0/`, run:

```bash
.venv/bin/python scripts/analysis.py \
  --records runs/browser_pilot_stub_v0/browser_pilot_stub_v0_records.jsonl \
  --output runs/browser_pilot_stub_v0/analysis_summary.md
```

The browser pilot can be compared with the earlier API-only dry run to identify
browser-mediated timing or environment differences. It should not be used for
paper-facing latency claims while the backend remains `stub`.

## Interpretation Boundary

This pilot can support claims about:

- browser panel usability for executing the protocol;
- run-record export shape;
- environment flag capture;
- automatic contract-check plumbing with evaluator labels;
- whether browser-mediated runs preserve the expected condition behavior.

It cannot support claims about:

- WebLLM/Qwen quality;
- WebGPU dispatch overhead;
- model cold-start behavior;
- evidence correctness;
- user-facing helpfulness without review.
