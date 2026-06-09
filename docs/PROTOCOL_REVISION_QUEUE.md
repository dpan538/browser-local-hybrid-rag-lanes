# Protocol Revision Queue

Generated: 2026-06-09

This queue turns the deep-research method audit into concrete repository work.
It is intentionally stricter than the first methodology draft.

## Readiness Verdict

Current state:

Needs major revision before paper-facing experiments.

Meaning:

The idea is not rejected, but the first run must not be presented as a
confirmatory paper result until the protocol prevents label leakage, condition
format confounds, unstable latency claims, and vague human review.

## Blocking Before First Paper-Facing Run

| Item | Decision | Repo action |
|---|---|---|
| Runtime/evaluation leakage | Runtime must not see evaluator-only labels such as `expected_behavior`, gold lane, or gold refusal action. | Add runtime and evaluation fixture view schemas; document the split in `docs/FIXTURE_SCHEMA.md`. |
| Identical evidence packets | All conditions must use the same frozen evidence packet for each query. | Update ablation protocol and run metadata requirements. |
| Format-matched baseline | Condition 1 must use the same visible answer sections as hybrid conditions, while still generating all values. | Update baseline definition in `docs/ABLATION_AND_EVALUATION_PROTOCOL.md`. |
| Mixed evidence state | `mixed` rows must not default to `sufficient`. | Add row-level `decisive_fields`; update aggregator and validator. |
| Refusal decision protocol | Refusal correctness must be judged from a gold evidence-state-to-action table before viewing system output. | Expand review guide and refusal trace fields. |
| Paired statistics | Comparisons must preserve query pairing across conditions. | Replace Mann-Whitney/Fisher defaults with paired tests where applicable. |

## High-Priority Before Pilot Interpretation

| Item | Decision | Repo action |
|---|---|---|
| Rule pre-registration | Rule table, refusal matrix, prompt pack, fixture, and analysis plan should be content-hashed before official runs. | Add pre-registration checklist to protocol. |
| Prompt packs | Each condition needs a frozen prompt pack. | Add artifact requirement; create prompt files later. |
| Latency anomaly logs | Browser lifecycle and Long Tasks anomalies stay in primary results and are flagged. | Strengthen environment-stability schema and protocol text. |
| Human review decomposition | Factual dimensions should be binary or categorical checklists; Likert only for perception/usefulness. | Update review sheet guide. |
| Reviewer blinding | Reviewers should not see condition names, routing traces, or rule IDs during primary scoring. | Update review protocol. |
| Source-audit separation | Source audit failures should not be deterministic-render failures. | Keep separate fields and reporting tables. |

## Medium-Priority Before Submission

| Item | Decision | Repo action |
|---|---|---|
| Optional deterministic-only diagnostic | Useful for exact-field and refusal subsets, not a main baseline. | Add as appendix/diagnostic option. |
| Mixed-intent stratum | Ten rows expose failure modes but do not support stable ambiguity-rate claims. | Report separately and avoid pooled claims. |
| Dev/eval split | Rule authoring should use a development fixture separate from the reporting fixture. | Add when expanding beyond the one-row sample. |
| Output examples | Public-safe raw outputs should be preserved after a run. | Add later under `runs/raw/`. |
| Larger fixture | Fifty queries are exploratory. | Plan expansion before full-paper submission. |

## Method Changes Accepted Now

1. Treat the first 50-query run as exploratory unless a sealed evaluation
   fixture and pre-registered rule table are in place.
2. Report Condition 1 vs Condition 2 and Condition 2 vs Condition 3 as the two
   primary planned contrasts.
3. Use paired-by-query analysis:
   - McNemar or exact paired binary tests for pass/fail and refusal errors;
   - Wilcoxon signed-rank or paired permutation for latency and ordinal scores;
   - paired effect sizes and confidence intervals before p-value rhetoric.
4. Treat P95 as descriptive only at n=50; report median, IQR, P90, max, and
   anomaly counts.
5. Use one pinned browser/model/hardware configuration for v1 and state that
   latency claims are within-configuration.

## Claims Gate

A claim can appear in a paper-facing result only if it is backed by a metric
whose scope matches the claim.

| Claim | Required support |
|---|---|
| Deterministic lanes improve field fidelity | Required-field checklist, field mutation/omission counts, same evidence packet across conditions. |
| Deterministic refusal reduces under-refusal | Gold evidence-state-to-action table and separate under-refusal count. |
| Refusal does not harm usability too much | Blinded reviewer helpfulness/usefulness scores with paired analysis. |
| Hybrid improves latency | Warm end-to-end paired differences on the same query set, anomaly logs included. |
| Compound answers help mixed intent | Separate mixed-intent stratum with deterministic and generative sub-scores. |

## Remaining Open Questions

- Should v1 add an optional deterministic-only diagnostic condition before the
  first pilot, or wait until after the three-condition run?
- Should the first fixture expansion include a second metadata-heavy domain
  beyond archive/source/rights records?
- How much of the runtime router should be rule-based versus a frozen
  pre-labeled intent signal for the first study?
- What is the minimum reviewer count we can realistically support: two plus
  adjudicator, or one reviewer plus audit spot-checks for a pilot?
- Should source-audited rows and synthetic rows be reported in separate
  result tables?
