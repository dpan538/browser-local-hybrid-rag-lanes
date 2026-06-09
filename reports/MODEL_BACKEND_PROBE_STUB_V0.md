# Model Backend Probe Stub V0

Date: 2026-06-10

This memo records the first probe of the new model-backend adapter. The probe
used the default `stub` backend, so it only verifies adapter plumbing and output
shape.

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

This confirms that the backend adapter layer can be called from a script before
the Flask API or browser panel runs an experiment. It does not validate any real
local model, WebLLM runtime, WebGPU execution, or Qwen behavior.

## Next Probe

The next meaningful probe should use:

```bash
HYBRID_LANE_MODEL_BACKEND=openai_compatible
HYBRID_LANE_MODEL_BASE_URL=http://127.0.0.1:8000/v1
HYBRID_LANE_MODEL_NAME=<local-model-name>
.venv/bin/python scripts/probe_model_backend.py
```

The model server must already be running. This repository should not download
weights or start a model runtime implicitly.
