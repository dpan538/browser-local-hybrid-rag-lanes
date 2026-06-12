# Qwen WebLLM Source-Audited 50 Expectation V0

Generated: 2026-06-12

This note backs up the run expectation before executing the first browser-local
Qwen/WebLLM experiment over the completed `source_audited_50` fixture gate.

## Purpose

Run the primary browser-local model path over the metadata-audited 50-query
fixture:

- primary model identity: `Qwen/Qwen3.5-0.8B`;
- WebLLM runtime id: `Qwen3.5-0.8B-q4f16_1-MLC`;
- fixture: `fixtures/source_audited_50/runtime_view.jsonl`;
- evaluation labels: `fixtures/source_audited_50/evaluation_view.jsonl`;
- design: 50 queries x 3 conditions = 150 run records.

This is the first source-audited Qwen/WebLLM run. It should not be described as
a paper-facing final result until diagnostics, aggregation, and a post-run gate
confirm schema validity, condition coverage, environment flags, and contract
metrics.

## Server Configuration

Start the Flask server with source-audited paths:

```bash
HYBRID_LANE_MASTER_FIXTURE_PATH=fixtures/source_audited_50/experiment_fixture.jsonl \
HYBRID_LANE_RUNTIME_PATH=fixtures/source_audited_50/runtime_view.jsonl \
HYBRID_LANE_EVAL_PATH=fixtures/source_audited_50/evaluation_view.jsonl \
HYBRID_LANE_WARMUP_PATH=fixtures/source_audited_50/warmup_queries.jsonl \
.venv/bin/python app.py
```

The `/api/health` response must report:

```text
runtime_rows: 50
eval_rows: 50
warmup_rows: 1
paths.runtime: fixtures/source_audited_50/runtime_view.jsonl
paths.evaluation: fixtures/source_audited_50/evaluation_view.jsonl
```

## Browser Run

Use the Codex in-app browser Qwen smoke panel:

```text
http://127.0.0.1:8787/tools/qwen_webllm_smoke/?run_id=qwen_webllm_source_audited_50_v0&batch_start=1&batch_limit=50&max_tokens=160&generation_timeout_ms=120000&temperature=0.2
```

Run the custom batch, not the hard-coded `Run First 50` shortcut, so the run id
remains:

```text
qwen_webllm_source_audited_50_v0
```

Expected output path:

```text
runs/qwen_webllm_source_audited_50_v0/qwen_webllm_source_audited_50_v0_records.jsonl
```

Raw run records remain ignored under `runs/` unless a later artifact packaging
step explicitly includes them.

## Success Criteria

The run is considered complete if:

- 150 records are saved;
- all 50 query ids have exactly 3 condition rows;
- schema errors are 0;
- duplicate query-condition pairs are 0;
- missing query-condition pairs are 0;
- generation timeouts are 0, or any timeout row is explicitly diagnosed;
- model id is `Qwen3.5-0.8B-q4f16_1-MLC`;
- primary model identity is `Qwen/Qwen3.5-0.8B`;
- `tab_backgrounded_rows` is 0 for clean latency use, or the run is marked
  contract-diagnostic only.

## Expected Signals

Because this fixture includes source-audited partial and missing evidence rows,
expected signals may differ from the synthetic 50-query exploratory fixture.
The expected high-level pattern is:

- C1 all-generation may produce refusal-alignment or field-mutation failures;
- C2 hybrid-without-refusal should preserve deterministic fields but may still
  under-refuse on missing/contradictory evidence;
- C3 full-hybrid should reduce under-refusal by using deterministic refusal;
- deterministic skip rows should reduce Qwen invocation count in C3 relative
  to C1;
- latency claims require foreground-clean environment flags and should remain
  diagnostic if backgrounding or long-task anomalies appear.

## Stop Conditions

Stop and diagnose before continuing if:

- `/api/health` reports the old draft runtime or fewer than 50 rows;
- WebGPU probe is unavailable;
- WebLLM fails to load the Qwen runtime;
- batch execution stalls without checkpointed saved rows;
- saved rows fail `schemas/run_record_schema.json`;
- `run_id` is not `qwen_webllm_source_audited_50_v0`;
- generated records do not point to the source-audited fixture artifact hashes.

## Boundary

This pre-run backup does not download or commit model weights. The browser may
cache WebLLM model artifacts locally during execution, but those artifacts must
not be committed. The run should not download image files.
