# Runs Directory

This directory is reserved for generated experiment outputs.

Default smoke/pilot outputs are ignored by git:

- `collected_records.jsonl`
- `auto_evaluated_records.jsonl`
- `analysis_summary.md`
- `freeze_manifest.json`

Paper-facing runs should be copied into an explicitly named subdirectory and
added intentionally after the protocol, fixture, rule table, prompt pack, and
analysis plan have been frozen.
