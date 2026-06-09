# Ablation And Evaluation Protocol

Generated: 2026-06-09

This protocol turns the hybrid answer-lane framing into a reproducible first
experiment.

## Experimental Conditions

### Condition 1: All Generation

All answer lanes are sent to the local model with the retrieved evidence
packet.

Purpose:

- baseline for user-visible latency;
- baseline for contract failure/warning rate;
- baseline for answer usefulness and refusal behavior.

Expected risk:

- exact source/rights fields may be paraphrased, omitted, or upgraded;
- refusal may be too verbose, too weak, or absent.

### Condition 2: Hybrid Without Refusal Lane

Source/rights and exact evidence-field answers are deterministic. Research
guidance remains generative. Refusal is not handled by a deterministic lane;
insufficient-evidence rows are passed to the model under the same evidence
contract as the baseline.

Purpose:

- isolates the value of deterministic evidence-field delivery;
- keeps refusal behavior as a model responsibility;
- creates a direct comparison against Condition 3.

Key question:

Does exact field rendering improve contract compliance and latency before
adding deterministic refusal behavior?

### Condition 3: Full Hybrid

Source/rights and exact evidence-field answers are deterministic. Mandatory
insufficient-evidence refusals are deterministic. Explanatory, comparative,
and research-guidance lanes remain generative or mixed.

Purpose:

- tests the complete answer-lane policy;
- directly measures whether refusal lanes reduce contract risk;
- compares usability impact against Condition 2.

Key question:

Does deterministic refusal reduce compliance failures without making the
assistant over-conservative or less useful?

## Why Condition 2 Matters

Condition 2 vs Condition 3 directly tests whether refusal lanes hurt usability.

If Condition 3 improves compliance but lowers helpfulness, the paper has a
real tradeoff to report. If Condition 3 improves compliance without meaningful
usability loss, deterministic refusal becomes a stronger design claim.

## Sample Size And Latency Interpretation

The first milestone uses 50 queries. This is an exploratory milestone, not a
statistical final.

Rules:

- Treat P95 as exploratory.
- Report P50, P75, P90, P95, max, and slow-row counts.
- Report per-lane results rather than only aggregate results.
- Flag browser GC, tab suspension, model warmup, and cache state when visible.
- Avoid absolute P95 success claims from 50 rows.

Initial latency success rule:

The hybrid condition should not have P95 `hybrid_system_latency` above 1.5x the
all-generation baseline unless the increase is explained by a small number of
audited runtime anomalies. For deterministic exact/refusal lanes, the expected
direction is lower latency than all generation; for generative lanes, parity is
acceptable if contract/usability improves.

## Required Metrics

Mechanical metrics:

- completed rows;
- runtime errors;
- metric issues;
- contract failures;
- contract warnings;
- field omissions;
- field mutations;
- unsupported rights/status upgrades;
- refusal false positives;
- refusal false negatives.

Latency metrics:

- `retrieval_latency`;
- `deterministic_assembly_latency`;
- `qwen_generation_latency`;
- `hybrid_system_latency`;
- `ttft`;
- `total_latency`;
- `tokens_per_second`;
- P50/P75/P90/P95/max by lane and condition.

Usability metrics:

- helpfulness;
- source clarity;
- rights clarity;
- refusal clarity;
- research usefulness;
- over-conservatism;
- whether enough next-step guidance was provided.

Correctness split:

- deterministic lane correctness: did output follow rules over provided
  evidence?
- evidence correctness: did the provided evidence match the source?
- answer usefulness: did the answer help the user accomplish the task?

## First Milestone Dataset Shape

Recommended 50-query distribution:

| Lane | Count | Purpose |
|---|---:|---|
| source/rights | 10 | exact field delivery |
| no-evidence refusal | 8 | mandatory refusal |
| first/earliest refusal | 7 | chronology/evidence refusal |
| comparison | 8 | generative synthesis |
| region/period recommendation | 7 | generative research guidance |
| current-object explanation | 5 | explanatory generation |
| more-context | 5 | long-tail guidance |

The distribution intentionally over-samples refusal and exact-field lanes
because those lanes define the hybrid claim.

## Success Criteria

Exploratory milestone success requires:

1. No increase in contract failures relative to all generation.
2. Lower or equal field mutation/omission rates for source/rights lanes.
3. Lower refusal false-negative rate in Condition 3 than Condition 2.
4. No large usability collapse in Condition 3 relative to Condition 2.
5. P95 interpreted as exploratory, with the 1.5x rule used only as a guardrail.

## Failure Modes Worth Publishing

The experiment remains valuable if it finds:

- deterministic refusal is safer but too conservative;
- exact field rendering improves compliance but feels under-informative;
- all-generation gives better perceived help but worse rights/source fidelity;
- mixed prefill plus bounded generation is the best usability compromise.

These are method findings, not merely implementation bugs.
