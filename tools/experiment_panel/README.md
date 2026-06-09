# Experiment Panel

This is a small browser-local operation panel for the first hybrid answer-lane
pilot. It is designed to run in the Codex in-app browser against the local
Flask runner.

Start the API runner:

```bash
.venv/bin/python app.py
```

Open:

```text
http://127.0.0.1:8787/tools/experiment_panel/
```

Before opening the panel, generate fixture views:

```bash
.venv/bin/python scripts/split_fixture_views.py \
  fixtures/experiment_fixture.jsonl \
  fixtures/runtime_view/experiment_fixture.runtime.jsonl \
  fixtures/evaluation_view/experiment_fixture.eval.jsonl
```

The panel is intentionally simple:

- runtime rows are visible for operation;
- evaluator labels are loaded separately and hidden by default;
- the Run button calls `/api/run`;
- timings and auto-contract checks are returned by the server;
- run records can be exported as JSON from the browser.
