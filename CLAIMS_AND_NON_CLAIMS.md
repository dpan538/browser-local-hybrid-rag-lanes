# Claims And Non-Claims

Updated: 2026-06-12

This ledger prevents exploratory instrumentation results from drifting into
unsupported paper claims.

## Current Allowed Claims

These claims are allowed for the current exploratory 50-query synthetic
fixture:

1. The project formulates browser-local small-model RAG as an answer
   execution-policy problem: deterministic rendering, deterministic refusal,
   bounded generation, or compound output.
2. The protocol distinguishes `qwen_generation_latency` from
   `hybrid_system_latency`.
3. The protocol distinguishes evidence-to-output fidelity from evidence
   correctness.
4. In the clean exploratory q001-q050 aggregate, `full_hybrid` produced zero
   automatic contract failures, while `all_generation` and
   `hybrid_without_refusal` each produced 15 automatic contract failures.
5. In the same aggregate, `full_hybrid` invoked Qwen on fewer rows than
   `all_generation` because deterministic refusal and deterministic rendering
   can skip generation for eligible lanes.

## Claims Requiring Paper v1 Evidence

These claims are not yet supported and require a Paper v1 freeze:

1. Hybrid answer lanes preserve usability while improving contract behavior.
   Requirement: blinded human review.
2. Deterministic source/rights rendering improves source or rights
   correctness.
   Requirement: source-audited or public-derived evidence.
3. Full hybrid has better latency in a generalizable browser-local setting.
   Requirement: frozen clean run with cold/warm accounting and anomaly flags.
4. The approach generalizes beyond this controlled fixture.
   Requirement: larger or independently constructed fixture.

## Claim Ladder

### Synthetic 50-query pilot

Allowed:

- the pipeline supports a three-condition hybrid-lane ablation;
- in the exploratory fixture, full hybrid removed observed automatic
  refusal-alignment failures.

Not allowed:

- generalization beyond the fixture;
- evidence-correctness or usability claims.

### Source-audited 100-query calibration

Allowed if the freeze and clean run pass:

- the source-audited fixture and frozen rule/prompt process can scale beyond
  the synthetic 50-query pilot;
- the review rubric can be calibrated on realistic source-audited outputs.

Not allowed:

- final journal-level usability claims;
- stable generalization claims;
- OIR/AJIM-level empirical claims.

### Source-audited 200-query formal pilot

Allowed if rules remain frozen:

- the pattern and review workflow remained plausible across a broader
  source-audited fixture;
- reviewer disagreement patterns can identify ambiguous lane boundaries.

Still not final for OIR/AJIM if a 300-query run is planned.

### Source-audited 300-query OIR/AJIM candidate

Allowed if the freeze, clean run, automatic metrics, and two-rater blinded
review pass:

- full hybrid answer lanes reduced refusal-alignment failures and unnecessary
  generation in a controlled source-audited information-assistance fixture;
- the effect was evaluated across 900 condition outputs;
- human review on 240-300 blinded sampled outputs did not show an unacceptable
  usefulness collapse;
- latency claims remain pinned to the declared browser/model/hardware
  environment.

Still forbidden:

- solving hallucination;
- determining legal rights truth;
- universal browser-local RAG superiority.

## Forbidden Claims

Do not claim:

- deterministic answers are semantically correct;
- the system determines legal reuse rights;
- hybrid lanes solve hallucination;
- Qwen generation became faster when the system skipped generation;
- 50 queries prove statistical superiority;
- results generalize to all browser-local RAG systems;
- this is a retrieval algorithm, learned router, or model-training
  contribution;
- synthetic evidence is equivalent to archive metadata.

## Preferred Wording

Use:

> We propose and evaluate a hybrid answer-lane execution policy for
> browser-local small-model RAG, separating deterministic evidence/refusal
> delivery from bounded generative synthesis.

Avoid:

> We solve browser-local RAG.

Use:

> Deterministic lanes preserve supplied evidence fields under a rule contract.

Avoid:

> Deterministic lanes guarantee rights correctness.

Use:

> Generation was skipped for eligible deterministic lanes.

Avoid:

> Qwen was faster on deterministic lanes.
