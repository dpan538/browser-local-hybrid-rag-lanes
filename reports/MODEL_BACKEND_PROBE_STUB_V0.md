# Model Backend Probe Stub V0

Date: 2026-06-10

This memo records the first probe of the comparison-backend adapter. The probe
used the default `stub` backend, so it only verifies adapter plumbing and output
shape. It is not a Qwen/WebLLM run.

## Probe Command

```bash
.venv/bin/python scripts/probe_model_backend.py
```

## Result

The probe returned `ok: true` with:

- backend: `stub`;
- prompt length recorded;
- generated text returned;
- elapsed time recorded.

## Interpretation

This confirms that the adapter layer can be called from a script before the
Flask API or browser panel runs an experiment. It does not validate any real
local model, WebLLM runtime, WebGPU execution, or Qwen behavior.

The primary experiment model remains `Qwen/Qwen3.5-0.8B`. The inherited
research WebLLM runtime id is `Qwen3.5-0.8B-q4f16_1-MLC`. Primary Qwen results
must come from a Codex in-app browser WebLLM/WebGPU run, not from this
server-side adapter.

## Comparison-Only Probe

The OpenAI-compatible path is comparison-only and guarded. It requires an
explicit comparison flag:

```bash
HYBRID_LANE_ALLOW_COMPARISON_BACKEND=1
HYBRID_LANE_MODEL_BACKEND=openai_compatible
HYBRID_LANE_MODEL_BASE_URL=http://127.0.0.1:8000/v1
HYBRID_LANE_MODEL_NAME=<same-scale-comparison-model-name>
.venv/bin/python scripts/probe_model_backend.py
```

The model server must already be running. This repository should not download
weights or start a model runtime implicitly. Comparison results must be labeled
separately and cannot be used as primary Qwen/WebLLM evidence.
