# Claims And Non-Claims

Updated: 2026-06-12

This ledger prevents exploratory instrumentation results from drifting into
unsupported paper claims.

## Current Allowed Claims

These claims are allowed for the current 50-query diagnostic fixtures:

1. The project formulates browser-local small-model RAG as an answer
   execution-policy problem: deterministic rendering, deterministic refusal,
   bounded generation, or compound output.
2. The protocol distinguishes `qwen_generation_latency` from
   `hybrid_system_latency`.
3. The protocol distinguishes evidence-to-output fidelity from evidence
   correctness.
4. In the clean synthetic q001-q050 aggregate, `full_hybrid` produced zero
   automatic contract failures, while `all_generation` and
   `hybrid_without_refusal` each produced 15 automatic contract failures.
5. In the source-audited 50-query diagnostic aggregate, `full_hybrid` produced
   zero automatic contract failures, while `all_generation` and
   `hybrid_without_refusal` each produced 10 automatic contract failures.
6. In the source-audited diagnostic aggregate, `full_hybrid` invoked Qwen on
   fewer rows than `all_generation` because deterministic refusal and
   deterministic rendering can skip generation for eligible lanes.

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

### Source-audited 50-query diagnostic

Allowed:

- the source-audited 50-query gate can be executed through the browser-local
  Qwen/WebLLM pipeline with complete condition coverage;
- the source-audited diagnostic run repeats the automatic refusal-alignment
  pattern from the synthetic fixture at 50-query scale;
- full hybrid reduces Qwen invocation count by skipping deterministic exact
  and deterministic refusal lanes.

Not allowed:

- journal-level usability claims;
- generalization beyond the controlled 50-query gate;
- legal rights correctness claims;
- strong latency superiority claims because long-task rows are present.

### Source-audited 100-query calibration

Allowed if the freeze and clean run pass:

- the source-audited fixture and frozen rule/prompt process can scale beyond
  the synthetic 50-query pilot;
- the review rubric can be calibrated on realistic source-audited outputs.

Not allowed:

- final journal-level usability claims;
- stable generalization claims;
- OIR/AJIM-level empirical claims.

### Source-audited 200-query JIS candidate

Allowed if the freeze, clean run, automatic metrics, and two-rater blinded
review pass:

- hybrid answer-lane allocation reduced specific automatic contract failures
  and under-refusal in a controlled browser-local RAG setting;
- bounded generation remained available for explanation, comparison, and
  research-guidance tasks;
- human review on 180 blinded sampled outputs did not show an unacceptable
  usefulness collapse;
- reviewer disagreement patterns can identify ambiguous lane boundaries;
- latency claims remain pinned to the declared browser/model/hardware
  environment.

This is the minimum Journal of Information Science candidate level, not the
preferred OIR/AJIM stretch level.

### Source-audited 300-query stronger/stretch candidate

Allowed if the freeze, clean run, automatic metrics, and two-rater blinded
review pass:

- the 200-query JIS claim pattern remained stable or became clearer in a
  larger source-audited fixture;
- the effect was evaluated across 900 condition outputs;
- human review on 240-300 blinded sampled outputs did not show an unacceptable
  usefulness collapse;
- the package may support a stronger JIS submission, revision response, or
  OIR/AJIM stretch submission.

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
