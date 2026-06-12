# Source-Audited 50 Expansion 15 Summary V0

Generated: 2026-06-12

This report summarizes the first expansion cycle after the pre-run backup. It
is an authoring/provenance milestone, not a Paper v1 Qwen/WebLLM result.

## Scope

The `source_audited_50` fixture now contains:

- 15 source-audited manifest rows;
- 15 query-plan rows;
- 15 compiled experiment fixture rows;
- 15 runtime rows;
- 15 evaluation rows;
- 1 explicit warmup row.

All current source records are Library of Congress Prints and Photographs
Division item-level metadata records. The batch remains metadata-only:

- no images downloaded;
- no model weights downloaded;
- no browser cache committed;
- `rights_label` and `reuse_permission` preserve LOC source wording;
- `public_domain_status` remains `not_explicitly_stated_by_source`.

## Self-Audit Patch

Before adding rows, the deterministic-field coverage was hardened:

- `source_citation` is now treated as a deterministic contract-bearing field;
- `image_state_label` is now available for deterministic contract checking;
- Flask stub/API answer shape and the Qwen WebLLM browser panel use the same
  deterministic field list;
- automatic contract checks can detect source-citation and image-state
  mutation/omission;
- source pointer preservation can pass by exact source or exact source
  citation.

This prevents provenance/citation failures from being hidden as successful
source/rights answers.

## Distribution

Current query-plan distribution:

| Category | Count |
|---|---:|
| `source_rights` | 4 |
| `mixed_intent` | 6 |
| `explanation` | 3 |
| `more_context` | 1 |
| `recommendation` | 1 |

Primary lane distribution:

| Primary lane | Count |
|---|---:|
| `deterministic_exact` | 4 |
| `compound` | 6 |
| `generative` | 5 |

## Validation

Commands run:

```bash
.venv/bin/python -m py_compile app.py scripts/auto_contract_check.py \
  scripts/compile_source_audited_fixture.py scripts/compile_blueprint.py

node --check tools/qwen_webllm_smoke/qwen_webllm_smoke.js

.venv/bin/python scripts/validate_source_audit_manifest.py \
  fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --min-rows 15 \
  --require-pass

.venv/bin/python scripts/validate_source_audited_query_plan.py \
  fixtures/source_audited_50/query_plan_v0.jsonl \
  --min-rows 15

.venv/bin/python scripts/sync_query_manifest.py \
  --manifest fixtures/source_audited_50/source_audit_manifest_v0.jsonl \
  --query-plan fixtures/source_audited_50/query_plan_v0.jsonl

.venv/bin/python scripts/compile_source_audited_fixture.py --warmup-count 1

.venv/bin/python scripts/check_source_audited_consistency.py \
  --expected-rows 15 \
  --require-explicit-warmup

.venv/bin/python scripts/validate_protocol_bundle.py

.venv/bin/python scripts/freeze_manifest.py \
  --profile paper-v1-source-audited \
  --output /private/tmp/hybrid_lane_paper_v1_source_audited_freeze_manifest.json
```

All checks passed after the compile/consistency race was rerun sequentially.

## Next Expansion Needs

The next source-audited batch should add:

- refusal/no-evidence rows;
- first/earliest refusal rows;
- comparison rows with two or more audited records;
- a second source family, preferably Wikimedia Commons or DPLA, to test license
  and provider-provenance diversity.

