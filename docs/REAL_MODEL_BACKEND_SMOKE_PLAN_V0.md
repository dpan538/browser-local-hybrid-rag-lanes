# Qwen Primary Runtime And Comparison Backend Smoke Plan V0

Date: 2026-06-10

This plan corrects the model boundary for the first step beyond the `stub`
backend. The primary experiment model is `Qwen/Qwen3.5-0.8B`. The product
runtime artifact inherited from the archive research branch is
`onnx-community/Qwen3.5-0.8B-ONNX`; the browser research path may use the
custom WebLLM/MLC model id `Qwen3.5-0.8B-q4f16_1-MLC`.

Server-side OpenAI-compatible endpoints are not the primary experiment path.
They are comparison-only probes and must never be used for headline claims about
browser-local Qwen/WebLLM behavior.

This repository still does not commit model weights, browser cache, downloaded
images, raw HTML, cookies, sessions, or credentials.

## Primary Runtime Boundary

Primary model identity:

```text
Qwen/Qwen3.5-0.8B
```

Product runtime artifact reference:

```text
onnx-community/Qwen3.5-0.8B-ONNX
```

Research WebLLM model id used by the earlier browser-local RAG lab:

```text
Qwen3.5-0.8B-q4f16_1-MLC
```

The primary smoke run must be a Codex in-app browser run that records WebGPU,
WebLLM, model-load, TTFT, total generation latency, and cache state. Flask may
serve fixtures, save JSONL, and perform deterministic contract checks, but it
must not stand in for browser-local Qwen generation.

## Supported Backends

### `stub`

Default deterministic timed backend for protocol and UI validation. It is not a
model-quality or model-latency result.

```bash
HYBRID_LANE_MODEL_BACKEND=stub
```

### `openai_compatible` comparison-only

Adapter for a local OpenAI-compatible chat-completions endpoint. This backend is
disabled unless the run is explicitly marked as a comparison. It must not be
used for the main Qwen 3.5 0.8B experiment, and it must not be described as a
browser-local WebLLM/WebGPU result.

Required:

```bash
HYBRID_LANE_ALLOW_COMPARISON_BACKEND=1
HYBRID_LANE_MODEL_BACKEND=openai_compatible
HYBRID_LANE_MODEL_BASE_URL=http://127.0.0.1:8000/v1
HYBRID_LANE_MODEL_NAME=<same-scale-comparison-model-name>
```

Optional:

```bash
HYBRID_LANE_MODEL_API_KEY=<local-api-key-if-needed>
HYBRID_LANE_MODEL_TIMEOUT_SEC=60
HYBRID_LANE_MODEL_TEMPERATURE=0
```

If `HYBRID_LANE_ALLOW_COMPARISON_BACKEND=1` is absent, the adapter intentionally
fails so incidental local endpoints such as Ollama or LM Studio cannot become
the primary experiment path.

## Primary Probe Before Running

For the main experiment, the probe belongs in the browser panel:

1. load the Qwen/WebLLM page in the Codex in-app browser;
2. probe WebGPU;
3. load `Qwen3.5-0.8B-q4f16_1-MLC`;
4. run one generative or compound query;
5. save JSONL with model id, model URL, model-lib URL, cold/warm cache state,
   model-load latency, TTFT, total generation latency, output tokens, and
   WebGPU/device errors.

The server-side CLI probe remains useful only for stub or comparison plumbing:

```bash
.venv/bin/python scripts/probe_model_backend.py
```

Browser/API comparison probe:

```bash
curl -s -X POST http://127.0.0.1:8787/api/model/probe \
  -H 'Content-Type: application/json' \
  -d '{"max_tokens":64}'
```

The experiment panel exposes this as `Probe Comparison Backend`. A comparison
run should not begin until the probe returns:

```json
{ "ok": true }
```

## One-Query Primary Qwen Smoke Acceptance Criteria

For the first real Qwen/WebLLM run, use a single generative or compound query
before running the 10-query browser pilot. Suggested candidates:

- `q033`: bounded explanation, sufficient evidence;
- `q041`: mixed deterministic fields plus generated historical explanation.

Acceptance criteria:

- WebGPU probe succeeds in the Codex in-app browser;
- WebLLM loads `Qwen3.5-0.8B-q4f16_1-MLC`;
- exactly one query x three conditions can run from the browser panel, with
  Qwen invoked only on generative or compound lanes;
- the saved JSONL validates against `schemas/run_record_schema.json`;
- `qwen_generation_latency_ms` is populated for rows that invoke generation;
- deterministic-only rows keep `qwen_generation_latency_ms = 0.0`;
- cold/warm cache state and WebGPU/device errors are recorded;
- failure messages are explicit if WebGPU, WebLLM, or the model artifact is
  unavailable.

## Interpretation Boundary

This smoke run can support:

- primary Qwen/WebLLM run-record compatibility;
- cold/warm field population;
- whether generated text returns through the same contract-checking pipeline;
- whether deterministic lanes correctly skip Qwen generation.

It cannot yet support:

- statistical WebGPU dispatch-overhead claims;
- source/evidence correctness;
- statistical superiority;
- user-perceived helpfulness.

## Next Gate

Only after the one-query Qwen/WebLLM smoke succeeds should the 10-query browser
pilot be re-run with a new `run_id`, for example:

```text
browser_pilot_qwen_webllm_smoke_v0
```

Do not reuse an existing run ID unless intentionally setting
`allow_overwrite=true` through a controlled script.
