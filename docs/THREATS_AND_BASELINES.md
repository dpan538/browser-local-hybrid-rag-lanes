# Threats, Baselines, And Generalization

Generated: 2026-06-09

This document collects threats that should be explicit in the paper framing.

## Evidence Correctness Threat

The system preserves supplied evidence. It does not repair wrong upstream
metadata, OCR errors, missing source fields, or incomplete rights metadata.

Mitigation:

- separate `evidence_to_output_fidelity` from `evidence correctness`;
- report `source_audit_status`;
- avoid legal or semantic correctness claims beyond audited evidence.

## Rule Evolution Threat

The rule table can overfit the first 50-query fixture.

Mitigation:

- commit `lane_rules_v1.yaml`;
- treat any rule-table change as a new condition or version;
- log `routing_undefined`;
- evaluate mixed-intent rows separately;
- report rule coverage and routing confusion.

## Router Ambiguity Threat

Real user queries can cross deterministic and generative boundaries.

Mitigation:

- include mixed-intent rows;
- support `compound_answer`;
- report a routing confusion matrix for mixed-intent rows;
- do not use mixed-intent rows alone to claim deterministic lane success.

## Latency Stability Threat

Browser-local measurements can be affected by cold start, tab suspension, GC,
thermal state, WebGPU adapter behavior, and network variance.

Mitigation:

- run 3-5 warmup queries before the measured run;
- report cold-start separately;
- tag rows with environment anomaly flags;
- report raw and anomaly-flagged/trimmed sensitivity summaries;
- keep P95 exploratory for 50-query milestones.

## Human Review Threat

Reviewers may disagree on helpfulness, refusal clarity, or over-conservatism.

Mitigation:

- use a 5-example calibration set;
- document rubric disagreements;
- report Cohen's kappa or ICC when there are at least two reviewers;
- fall back to consensus labels when agreement is low.

## Baselines

Primary baseline:

- all-generation over the same retrieved evidence.

Hybrid conditions:

- deterministic field rendering without deterministic refusal;
- full hybrid with deterministic refusal;
- compound answer for mixed-intent rows.

Rejected as primary baseline:

- all-deterministic, because research guidance and comparison require
  synthesis. It may be discussed as a counterfactual boundary, not a realistic
  assistant condition.

## Dominance And Tradeoff Claims

Condition 3 can be claimed better than Condition 1 only if:

- contract failures do not increase;
- median warm `hybrid_system_latency` is lower or comparable;
- warm P95 does not exceed the exploratory guardrail after anomaly analysis;
- helpfulness does not drop by more than 0.5 points on the 5-point scale.

If compliance improves but helpfulness drops more than 0.5 points, report a
tradeoff rather than a win.
