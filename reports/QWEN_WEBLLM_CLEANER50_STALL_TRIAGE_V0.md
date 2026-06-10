# Qwen WebLLM Cleaner50 Stall Triage V0

Date: 2026-06-10

This note records a scale-run interruption during the cleaner50 attempt. It is
an experiment-pipeline finding, not a paper result.

## What Happened

- The first cleaner50 attempt was interrupted before any final output was
  saved.
- The panel was hardened with per-query checkpoint saves.
- The rerun successfully checkpointed through q020, producing 60 schema-valid
  records.
- During q021, `all_generation` completed, but `hybrid_without_refusal` stalled
  in the WebLLM streaming generation path for several minutes.
- The page was reloaded to stop the stalled batch.
- After the reload, WebGPU probing itself stalled in both the original tab and
  a fresh tab, suggesting the browser WebGPU runtime was not cleanly recoverable
  inside the same Codex app session.

## Saved Partial

```text
runs/qwen_webllm_cleaner50_v0/qwen_webllm_cleaner50_v0_records.jsonl
reports/QWEN_WEBLLM_CLEANER50_STALLED_PARTIAL_DIAGNOSTICS_V0.md
reports/qwen_webllm_cleaner50_stalled_partial_diagnostics_v0.json
```

The saved checkpoint contains:

- 60 records.
- 20 completed queries.
- 0 schema errors.
- 0 `tab_backgrounded_rows`.
- 1 `long_task_gc_row`.

## Interpretation

The cleaner20 result was reproducible for q001-q020 under the checkpointed
cleaner50 rerun. The scale blocker appears when entering the later generative
comparison lane, specifically at q021 under `hybrid_without_refusal`.

This suggests the next experiment should not be another blind full-50 rerun in
the same browser session. The next step should be a focused q021/q022 triage
run after a clean browser/WebGPU restart that tests whether the stall is:

- a random WebGPU/WebLLM runtime hang;
- caused by the q021 prompt/evidence payload;
- caused by repeated streaming calls after a long batch;
- sensitive to max token budget.
- recoverable with an explicit generation timeout and WebLLM interrupt path.

## Boundary

No conclusion should be drawn about condition-level superiority from this
partial run. It only supports a methodology conclusion: full-scale browser-local
WebLLM experiments need checkpointing and stall-aware execution before larger
claims are attempted.
