#!/usr/bin/env python3
"""Local model backend adapters for hybrid lane smoke runs.

The primary experiment model is Qwen/Qwen3.5-0.8B. Browser-local Qwen/WebLLM
execution is expected to happen in the browser, not through this server-side
adapter. The OpenAI-compatible adapter is comparison-only and is guarded so an
incidental Ollama/LM Studio endpoint cannot become the primary experiment path.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Tuple
from urllib import error, request

PRIMARY_MODEL_IDENTITY = "Qwen/Qwen3.5-0.8B"
PRIMARY_PRODUCT_RUNTIME_ARTIFACT = "onnx-community/Qwen3.5-0.8B-ONNX"
PRIMARY_RESEARCH_WEBLLM_MODEL_ID = "Qwen3.5-0.8B-q4f16_1-MLC"
COMPARISON_BACKENDS = {"openai_compatible", "openai-compatible"}


class ModelBackendError(RuntimeError):
    """Raised when a configured local model backend cannot complete a call."""


def backend_name() -> str:
    return os.environ.get("HYBRID_LANE_MODEL_BACKEND", "stub").strip() or "stub"


def backend_config() -> Dict[str, Any]:
    backend = backend_name()
    config: Dict[str, Any] = {
        "backend": backend,
        "implemented": backend in {"stub", *COMPARISON_BACKENDS},
        "primary_model_identity": PRIMARY_MODEL_IDENTITY,
        "primary_product_runtime_artifact": PRIMARY_PRODUCT_RUNTIME_ARTIFACT,
        "primary_research_webllm_model_id": PRIMARY_RESEARCH_WEBLLM_MODEL_ID,
        "primary_backend_note": (
            "Primary Qwen 3.5 0.8B runs must use the browser-local "
            "Qwen/WebLLM path. Server-side adapters are not primary evidence."
        ),
    }
    if backend == "stub":
        config.update({
            "stub_delay_ms": float(os.environ.get("HYBRID_LANE_STUB_DELAY_MS", "80")),
        })
    if backend in COMPARISON_BACKENDS:
        config.update({
            "base_url": os.environ.get("HYBRID_LANE_MODEL_BASE_URL", "http://127.0.0.1:8000/v1"),
            "model": os.environ.get("HYBRID_LANE_MODEL_NAME", ""),
            "timeout_sec": float(os.environ.get("HYBRID_LANE_MODEL_TIMEOUT_SEC", "60")),
            "api_key_set": bool(os.environ.get("HYBRID_LANE_MODEL_API_KEY")),
            "comparison_only": True,
            "comparison_backend_enabled": comparison_backend_enabled(),
        })
    return config


def comparison_backend_enabled() -> bool:
    return os.environ.get("HYBRID_LANE_ALLOW_COMPARISON_BACKEND", "").strip() == "1"


def call_model(prompt: str, max_tokens: int = 512) -> Tuple[str, Dict[str, Any]]:
    backend = backend_name()
    if backend == "stub":
        return call_stub(prompt, max_tokens)
    if backend in COMPARISON_BACKENDS:
        if not comparison_backend_enabled():
            raise ModelBackendError(
                "openai_compatible is comparison-only. Primary experiments must use "
                "browser-local Qwen/Qwen3.5-0.8B. Set "
                "HYBRID_LANE_ALLOW_COMPARISON_BACKEND=1 only for a documented "
                "same-scale comparison run."
            )
        return call_openai_compatible(prompt, max_tokens)
    raise ModelBackendError(
        f"model backend '{backend}' is not implemented; expected stub or comparison-only openai_compatible"
    )


def call_stub(prompt: str, max_tokens: int = 512) -> Tuple[str, Dict[str, Any]]:
    delay_ms = float(os.environ.get("HYBRID_LANE_STUB_DELAY_MS", "80"))
    time.sleep(delay_ms / 1000.0)
    text = (
        "Generated research guidance: use the exact evidence fields for source "
        "and rights, then interpret the public-health context cautiously."
    )
    return text, {
        "backend": "stub",
        "max_tokens": max_tokens,
        "stub_delay_ms": delay_ms,
        "prompt_chars": len(prompt),
    }


def call_openai_compatible(prompt: str, max_tokens: int = 512) -> Tuple[str, Dict[str, Any]]:
    base_url = os.environ.get("HYBRID_LANE_MODEL_BASE_URL", "http://127.0.0.1:8000/v1").rstrip("/")
    model = os.environ.get("HYBRID_LANE_MODEL_NAME", "").strip()
    if not model:
        raise ModelBackendError(
            "HYBRID_LANE_MODEL_NAME is required for openai_compatible backend"
        )

    timeout_sec = float(os.environ.get("HYBRID_LANE_MODEL_TIMEOUT_SEC", "60"))
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are running a local-model smoke test. Answer briefly, "
                    "preserve evidence caveats, and do not invent source fields."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": float(os.environ.get("HYBRID_LANE_MODEL_TEMPERATURE", "0")),
        "max_tokens": max_tokens,
        "stream": False,
    }
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("HYBRID_LANE_MODEL_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    endpoint = f"{base_url}/chat/completions"
    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    started = time.perf_counter()
    try:
        with request.urlopen(req, timeout=timeout_sec) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ModelBackendError(
            f"openai_compatible backend returned HTTP {exc.code}: {body[:500]}"
        ) from exc
    except error.URLError as exc:
        raise ModelBackendError(
            f"openai_compatible backend could not connect to {endpoint}: {exc.reason}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise ModelBackendError("openai_compatible backend returned invalid JSON") from exc

    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ModelBackendError(
            "openai_compatible backend response did not contain choices[0].message.content"
        ) from exc

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    usage = data.get("usage", {}) if isinstance(data, dict) else {}
    return str(text), {
        "backend": "openai_compatible",
        "base_url": base_url,
        "model": model,
        "max_tokens": max_tokens,
        "prompt_chars": len(prompt),
        "elapsed_ms": elapsed_ms,
        "usage": usage,
    }
