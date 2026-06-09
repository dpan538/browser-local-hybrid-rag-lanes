# Real Model Backend Smoke Plan V0

Date: 2026-06-10

This plan defines the first step beyond the `stub` backend. It does not download
model weights or mandate a specific local runtime. Instead, it adds a narrow
adapter contract so an already-running local model endpoint can be probed before
any browser pilot run.

## Supported Backends

### `stub`

Default deterministic timed backend for protocol and UI validation.

```bash
HYBRID_LANE_MODEL_BACKEND=stub
```

### `openai_compatible`

Adapter for a local OpenAI-compatible chat-completions endpoint, such as a
locally hosted model server. This repo does not start that server and does not
download model weights.

Required:

```bash
HYBRID_LANE_MODEL_BACKEND=openai_compatible
HYBRID_LANE_MODEL_BASE_URL=http://127.0.0.1:8000/v1
HYBRID_LANE_MODEL_NAME=<local-model-name>
```

Optional:

```bash
HYBRID_LANE_MODEL_API_KEY=<local-api-key-if-needed>
HYBRID_LANE_MODEL_TIMEOUT_SEC=60
HYBRID_LANE_MODEL_TEMPERATURE=0
```

## Probe Before Running

CLI probe:

```bash
.venv/bin/python scripts/probe_model_backend.py
```

Browser/API probe:

```bash
curl -s -X POST http://127.0.0.1:8787/api/model/probe \
  -H 'Content-Type: application/json' \
  -d '{"max_tokens":64}'
```

The experiment panel also exposes `Probe Model Backend`. A real model smoke run
should not begin until the probe returns:

```json
{ "ok": true }
```

## One-Query Smoke Acceptance Criteria

For the first non-stub run, use a single generative or compound query before
running the 10-query browser pilot. Suggested candidates:

- `q033`: bounded explanation, sufficient evidence;
- `q041`: mixed deterministic fields plus generated historical explanation.

Acceptance criteria:

- model probe succeeds;
- exactly one query x three conditions can run from the browser panel;
- the saved JSONL validates against `schemas/run_record_schema.json`;
- `qwen_generation_latency_ms` is populated for rows that invoke generation;
- deterministic-only rows keep `qwen_generation_latency_ms = 0.0`;
- failure messages are explicit if the local endpoint is unavailable.

## Interpretation Boundary

This smoke run can support:

- adapter reachability;
- run-record compatibility with a non-stub backend;
- cold/warm field population;
- whether generated text returns through the same contract-checking pipeline.

It cannot yet support:

- WebGPU dispatch-overhead claims;
- WebLLM-specific browser-cache or model-load claims;
- source/evidence correctness;
- statistical superiority;
- user-perceived helpfulness.

## Next Gate

Only after the one-query smoke succeeds should the 10-query browser pilot be
re-run with a non-stub backend and a new `run_id`, for example:

```text
browser_pilot_openai_compatible_v0
```

Do not reuse an existing run ID unless intentionally setting
`allow_overwrite=true` through a controlled script.
