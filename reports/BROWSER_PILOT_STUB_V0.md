# Browser Pilot Stub V0

Date: 2026-06-10

This memo records the first Codex in-app browser execution of the hybrid
answer-lane experiment panel. It is a browser-mediated protocol check using the
`stub` backend, not a WebLLM/Qwen result.

## Purpose

The earlier 50-query dry run verified the API-only automation path. This pilot
checks whether the same protocol can be executed from the browser panel:

- load the 50-row draft runtime view;
- expose a 10-query browser pilot subset;
- run the 10 query x 3 condition grid from the panel;
- capture browser environment flags;
- save the generated JSONL to the local ignored `runs/` directory.

## Inputs

Server fixture paths:

- `fixtures/drafts/compiled_experiment_fixture_v0.jsonl`
- `fixtures/drafts/runtime_view_v0.jsonl`
- `fixtures/drafts/evaluation_view_v0.jsonl`
- `fixtures/drafts/warmup_queries_v0.jsonl`
- `fixtures/drafts/browser_pilot_subset_v0.jsonl`

Browser panel:

- `tools/experiment_panel/index.html`

## Procedure

The Flask app was started with draft fixture path overrides. The Codex in-app
browser opened:

```text
http://127.0.0.1:8787/
```

The panel reported:

- `50 rows`;
- `10 pilot`;
- `API stub`;
- `condition_prompt_pack_v1`.

The `Run ID` was set to:

```text
browser_pilot_stub_v0
```

The panel ran `Run Browser Pilot`, then automatically saved records through the
server-side `/api/runs/save` endpoint.

Generated ignored output:

- `runs/browser_pilot_stub_v0/browser_pilot_stub_v0_records.jsonl`
- `runs/browser_pilot_stub_v0/analysis_summary.md`

## Results

The saved browser-mediated JSONL contained 30 records:

| Item | Count |
| --- | ---: |
| unique queries | 10 |
| all-generation records | 10 |
| hybrid-without-refusal records | 10 |
| full-hybrid records | 10 |

Automatic contract failures:

| Condition | Failures |
| --- | ---: |
| all_generation | 4 |
| hybrid_without_refusal | 4 |
| full_hybrid | 0 |

All 8 failures were refusal false negatives. In this 10-query subset, four
queries were refusal-expected rows. The full-hybrid deterministic refusal lane
handled those rows without automatic contract failure.

Paired analysis:

| Contrast | Paired queries | Contract discordant pairs | Left fail / right pass | Exact paired binomial p |
| --- | ---: | ---: | ---: | ---: |
| all_generation vs hybrid_without_refusal | 10 | 0 | 0 | 1.0000 |
| hybrid_without_refusal vs full_hybrid | 10 | 4 | 4 | 0.1250 |

The p-values are descriptive only. With 10 queries and a timed stub backend,
they are useful as pipeline checks rather than statistical evidence.

## Environment Capture

The first measured browser call was marked:

- `warm_state`: `cold_start`;
- `visibility_state`: `visible`;
- `was_backgrounded`: `false`;
- `long_task_count`: observed as nonzero in the first browser run.

The long-task signal confirms that browser-side environment metadata is being
captured, but it should be interpreted cautiously until real model execution is
added.

## Implementation Notes

This pilot exposed two browser-specific issues:

- Codex in-app browser does not support ordinary download events for this
  workflow. The panel now saves pilot records through `/api/runs/save` instead
  of relying on file download.
- Button labels were present in the DOM but could appear off-center in wide
  browser screenshots. The panel now uses left-aligned button labels with a
  stable minimum height for clearer reproducibility screenshots.

## Limitations

This result does not support claims about:

- WebLLM/Qwen quality;
- WebGPU dispatch overhead;
- real browser-local model cold start;
- source/evidence correctness;
- perceived helpfulness.

The value of this step is narrower: the browser panel can execute and persist a
small preregistered subset, with evaluator-aware automatic contract metrics,
without manual answer pasting.

## Next Step

The next experimental step is to keep this browser path fixed and replace only
the backend layer for a 5-query real local-model smoke run. The acceptance
criterion should be operational, not substantive: records must save, schema
validation must pass, and cold/warm latency fields must be populated.
