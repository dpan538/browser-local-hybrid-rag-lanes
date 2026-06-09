# Qwen WebLLM Smoke Run Plan V0

Date: 2026-06-10

This plan defines the first primary-model smoke run for the hybrid-lanes repo.
It follows the archive research boundary:

- primary model identity: `Qwen/Qwen3.5-0.8B`;
- product runtime artifact reference: `onnx-community/Qwen3.5-0.8B-ONNX`;
- browser research runtime id: `Qwen3.5-0.8B-q4f16_1-MLC`.

The run must be performed in the Codex in-app browser. Flask may serve fixtures,
prompt packs, and save JSONL records, but Flask must not generate the Qwen
answer. Server-side OpenAI-compatible endpoints are comparison-only.

## Panel

Start the Flask app:

```bash
.venv/bin/python app.py
```

Open:

```text
http://127.0.0.1:8787/tools/qwen_webllm_smoke/
```

The panel pins:

```text
model_id: Qwen3.5-0.8B-q4f16_1-MLC
model_url: https://huggingface.co/mlc-ai/Qwen3.5-0.8B-q4f16_1-MLC
model_lib_url: https://raw.githubusercontent.com/akaashrp/mlc-binaries/main/Qwen3.5-0.8B-q4f16_1-webgpu-mlc.wasm
```

The browser may download and cache model artifacts locally. Those artifacts are
not committed.

## Smoke Sequence

1. Probe WebGPU.
2. Load Qwen WebLLM.
3. Select one mixed or generative query, preferably `q042`.
4. Run `C1 all-generation`.
5. Run `C2 hybrid without refusal`.
6. Run `C3 full hybrid`.
7. Save records with run id `qwen_webllm_smoke_v0`.

## Acceptance Criteria

- WebGPU probe reports `available`, or the failure is captured in the log.
- WebLLM load either succeeds with model-load latency or records an explicit
  failure.
- Generative and compound lanes invoke Qwen and populate
  `qwen_generation_latency_ms`, `ttft_ms`, and `tokens_per_second`.
- Deterministic-only and deterministic-refusal lanes keep
  `qwen_generation_latency_ms = 0.0`.
- Saved JSONL validates against `schemas/run_record_schema.json`.
- The run record identifies the producer as
  `webllm_qwen3_5_0_8b_research_runtime` for Qwen rows.

## Non-Claims

The smoke run does not support statistical superiority, full usability claims,
or source/evidence correctness. It only proves that the primary Qwen/WebLLM path
can feed the same hybrid-lane record schema used by the protocol.
