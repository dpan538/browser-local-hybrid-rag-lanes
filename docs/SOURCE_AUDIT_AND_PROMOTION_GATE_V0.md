# Source Audit And Promotion Gate V0

Generated: 2026-06-10

This note formalizes when the compiled 50-row fixture can be promoted from
draft data into an experiment fixture.

## Two Promotion Modes

### Exploratory Mode

Exploratory promotion allows synthetic and not-source-audited records if the
claims are limited to:

- evidence-to-output fidelity;
- refusal behavior under declared evidence states;
- latency plumbing and accounting;
- reviewer workflow rehearsal;
- UI/runtime reproducibility.

Exploratory mode does not allow evidence-correctness or legal-rights claims.

### Paper Mode

Paper mode requires the fixture evidence to be source-audited or derived from
public-source records with documented provenance. Synthetic-only records are
not enough for evidence-correctness claims.

Paper mode blocks promotion if:

- query IDs are duplicated;
- query texts are duplicated without justification;
- no-record rows are not explicit missing-evidence refusal tests;
- records are synthetic when the paper needs source-grounded evidence;
- records are not source-audited when the claim depends on evidence
  correctness.

## Scripted Gate

Run the exploratory gate:

```bash
.venv/bin/python scripts/check_promotion_gate.py --mode exploratory
```

Run the stricter paper gate:

```bash
.venv/bin/python scripts/check_promotion_gate.py --mode paper
```

Default report:

- `reports/PROMOTION_GATE_V0.md`

## Current Interpretation

The current compiled draft is suitable for exploratory workflow development if
the study is clearly framed as synthetic. It is not yet suitable for a
paper-facing evidence-correctness study.
