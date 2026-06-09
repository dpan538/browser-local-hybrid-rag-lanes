#!/usr/bin/env python3
"""Probe the configured local model backend before running an experiment."""

from __future__ import annotations

import argparse
import json
import time

from model_backend import ModelBackendError, backend_config, call_model


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        default="Return one short sentence confirming that the local backend is reachable.",
    )
    parser.add_argument("--max-tokens", type=int, default=64)
    args = parser.parse_args()

    started = time.perf_counter()
    result = {
        "ok": False,
        "backend": backend_config(),
        "prompt_chars": len(args.prompt),
    }
    try:
        text, meta = call_model(args.prompt, max_tokens=args.max_tokens)
        result.update({
            "ok": True,
            "text": text,
            "model_meta": meta,
            "elapsed_ms": (time.perf_counter() - started) * 1000.0,
        })
    except ModelBackendError as exc:
        result.update({
            "error": str(exc),
            "elapsed_ms": (time.perf_counter() - started) * 1000.0,
        })
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
