# Paper Narrative Draft

Generated: 2026-06-09

## Working Title

What Should Not Be Generated? Hybrid Answer Lanes for Browser-Local
Small-Model RAG

## Alternative Titles

- Hybrid Answer Lanes for Browser-Local Small-Model RAG
- Generation Allocation in Browser-Local RAG
- Separating Evidence Delivery from Research Guidance in Local RAG
- When Local RAG Should Not Generate

## One-Sentence Claim

Browser-local small-model RAG needs an answer-lane policy that decides when to
render evidence, when to refuse, when to generate, and when to compose
deterministic and generative components.

## Abstract Draft

Browser-local RAG systems promise private, low-dependency access to local
archives, but small browser-resident language models make every generated
token costly and error-prone. We argue that such systems should not treat the
local model as the universal answer surface. In rights-aware archive RAG, some
answers are contract-bearing evidence delivery tasks, such as source URLs,
rights labels, image-state caveats, and insufficient-evidence refusals, while
others require explanatory synthesis or research guidance. We propose hybrid
answer lanes: a static, auditable execution policy that routes each query and
evidence state to deterministic rendering, deterministic refusal, bounded
generation, or compound deterministic-plus-generative output. We introduce a
public-safe evaluation protocol that separates evidence-to-output fidelity from
source correctness, and reports model generation latency separately from
end-to-end hybrid system latency. The first experiment compares all-generation,
hybrid without deterministic refusal, and full hybrid conditions on a
50-query fixture with exact-field, refusal, generative, and mixed-intent lanes.

## Introduction Spine

1. Browser-local LLMs make private RAG possible, but local small models are not
   cheap universal narrators.
2. RAG papers often ask whether generated answers are grounded. We ask a prior
   systems question: should this answer be generated?
3. Rights-aware archives are a sharp setting because source, rights, reuse,
   public-domain, and image-state fields are contract-bearing.
4. Generating those fields can add latency and risk without adding user value.
5. But fully deterministic answering is not viable because research guidance,
   comparison, and explanation need synthesis.
6. The paper therefore studies answer-lane execution policy.

## Research Questions

RQ1. Which archive RAG answer lanes should bypass local model generation?

RQ2. Can deterministic evidence-field rendering improve source/rights fidelity
and latency without reducing usability?

RQ3. Does deterministic refusal reduce unsafe or unsupported answers, or does
it create over-refusal that harms research usefulness?

RQ4. How should latency be reported when some answers are generated and others
are assembled by deterministic runtime logic?

RQ5. How do mixed-intent queries expose the boundary between deterministic
evidence delivery and generative synthesis?

## Contributions

1. Generation allocation framing for browser-local small-model RAG.
2. A hybrid answer-lane execution policy with deterministic render,
   deterministic refusal, generative, and compound answer modes.
3. A reproducible evaluation protocol separating evidence-to-output fidelity,
   evidence correctness, latency, and usability.
4. A three-condition ablation: all generation, hybrid without deterministic
   refusal, and full hybrid.
5. A mixed-intent analysis protocol with routing confusion and format
   consistency metrics.

## What This Is Not

Not extractive QA:

The method does not learn answer spans. It routes among execution modes over
structured evidence.

Not only guardrails:

Guardrails usually constrain or filter model behavior. This method treats
non-generation as a first-class execution mode.

Not only RAG abstention:

Refusal is one lane. The method also includes exact evidence rendering and
compound answers.

Not model routing:

The router does not choose among LLMs. It chooses whether to render, refuse,
generate, or compose.

Not a product optimization:

The goal is a reproducible methodology for evaluating generation allocation in
browser-local RAG.

## Method Summary

Input:

- query;
- retrieved evidence packet;
- fixture intent label;
- field-state checklist.

Rule:

- apply `lane_rules_v1.yaml`;
- if no rule matches, default to generation and log `routing_undefined`.

Execution modes:

- `deterministic_render`;
- `deterministic_refusal`;
- `generative_answer`;
- `compound_answer`.

Metrics:

- contract failures/warnings;
- field omissions/mutations;
- unsupported upgrades;
- hallucination count/severity;
- refusal false positives/false negatives;
- format consistency;
- `qwen_generation_latency`;
- `hybrid_system_latency`;
- `latency_saved_by_deterministic`.

## Core Figure

Use the flowchart in `docs/LANE_DECISION_FLOW.md` as Figure 1.

Caption:

Hybrid answer-lane execution policy. The system uses a static rule table over
query intent and evidence state to select deterministic rendering,
deterministic refusal, bounded local generation, or compound output. Rows with
no rule match default to generation and are logged as routing coverage gaps.

## Expected Results Framing

Do not promise universal improvement.

Expected outcomes worth reporting:

- deterministic source/rights lanes reduce field mutations and local
  generation time;
- deterministic refusal lowers under-refusal but may increase over-refusal;
- compound answers may be best for mixed-intent usability;
- P95 is noisy in 50 rows, so distribution plots and anomaly logs matter more
  than a hard threshold.

## Claim Language

Strong but safe:

"Hybrid answer lanes reduce unnecessary generation for contract-bearing
archive answers while preserving local generation for synthesis tasks."

Tradeoff-friendly:

"The method exposes a measurable compliance-usability tradeoff in deterministic
refusal lanes."

Avoid:

"Hybrid lanes solve hallucination."

Avoid:

"Deterministic answers are semantically correct."

Avoid:

"Qwen generation is faster."

## Venue Notes

JCDL:

Emphasize archive evidence, rights metadata, provenance, source audit, and
reproducible public-safe fixtures.

CHI:

Emphasize user trust, refusal usability, format consistency, mixed-intent
interaction, and the user-visible difference between field rendering and
generated guidance.

CIKM/SIGIR Applied:

Emphasize RAG evaluation, evidence sufficiency, execution-mode routing, and
latency/quality tradeoffs.

## Next Drafting Tasks

1. Build a 5-example reviewer calibration set.
2. Draft 10 mixed-intent queries before coding a runner.
3. Draft the fixture schema with field-state checklist.
4. Write a related-work section using the objection structure:
   - extractive QA;
   - RAG attribution/sufficiency/abstention;
   - guardrails and structured generation;
   - model routing/cascades;
   - browser-local inference/retrieval;
   - UI/runtime-mediated AI.
5. Decide primary venue story before finalizing experiment emphasis.
