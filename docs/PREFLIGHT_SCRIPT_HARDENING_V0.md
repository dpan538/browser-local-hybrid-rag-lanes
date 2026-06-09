# Preflight Script Hardening V0

Date: 2026-06-10

This note records script and panel fixes made before starting a real
browser-local model smoke run. The goal is to prevent avoidable pipeline errors
from being mistaken for model behavior.

## Issues Fixed

### Silent Run Overwrite

The `/api/runs/save` endpoint previously wrote `runs/<run_id>/<run_id>_records.jsonl`
without checking whether that file already existed. A repeated browser run with
the same `run_id` could silently replace earlier records.

Fix:

- validate run records before saving;
- require all records in a saved batch to share one `run_id`;
- reject mismatched payload and record run IDs;
- reject existing output paths with HTTP 409 unless `allow_overwrite=true` is
  explicitly provided;
- write through a temporary file and then replace atomically.

### Save-Time Record Shape

The browser panel could POST arbitrary record-shaped objects to `/api/runs/save`.
If a malformed record was saved, analysis could fail later or, worse, consume a
partial record.

Fix:

- `/api/runs/save` now validates every saved record against
  `schemas/run_record_schema.json`.

### Browser Environment Flags

The browser panel reported a cumulative `long_task_count`. That made it hard to
distinguish a long task that happened during the current run record from one
that happened earlier in the same browser session.

Fix:

- the panel now reports `long_task_count_delta` per request;
- the API still preserves the cumulative count in `client_environment`;
- `tab_backgrounded` now considers both current `visibility_state` and the
  panel's historical `was_backgrounded` flag.

### Duplicate Analysis Rows

`scripts/analysis.py` previously grouped records by `query_id` and `condition`
using assignment. Duplicate records for the same pair would be silently
overwritten.

Fix:

- analysis now raises an error when duplicate `query_id + condition` pairs are
  found.

## Remaining Risks Before Real Backend Smoke

- The real model backend is not implemented yet; `HYBRID_LANE_MODEL_BACKEND`
  values other than `stub` still return an explicit 501 error.
- The current timing fields do not yet record token-level streaming events.
- Browser Long Task API support is optional and should remain a diagnostic flag,
  not an exclusion criterion.
- The fixture is still synthetic and not source-audited, so the next run remains
  a pipeline/model-adapter smoke test rather than an evidence-correctness study.

## Validation

The save guard was checked with Flask's test client:

- first save of a unique run ID returned HTTP 200;
- second save of the same run ID returned HTTP 409;
- protocol bundle validation still passed.
