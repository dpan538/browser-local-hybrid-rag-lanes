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

### Source-audited 100-query Paper v1

Allowed if the freeze, run, and human review pass:

- in a source-audited 100-query fixture, deterministic refusal reduced
  under-refusal without increasing observed automatic contract failures;
- hybrid lanes reduced Qwen invocations for exact/refusal tasks;
- blinded semantic review did not show a large usefulness collapse.

Still cautious:

- latency claims remain pinned to the browser/model/hardware environment.

### 200/300-query holdout

Allowed if rules remain frozen:

- the observed pattern remained stable across a larger held-out fixture.

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
