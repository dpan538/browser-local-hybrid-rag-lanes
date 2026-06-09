# Paper Positioning Decisions

Generated: 2026-06-09

This document consolidates the two external deep-research reports placed in
`reports/` into paper-facing decisions. The reports are treated as external
reviewer-style feedback, not as authoritative implementation state.

Source reports:

- `reports/Literature Positioning Report for Hybrid Answer Lanes in Browser-Local Small-Model RAG.docx`
- `reports/Method And Evaluation Deep Research Report.docx`

Important caveat:

Both reports state that the repo documents were not accessible in their
research environment. Their recommendations are therefore used as independent
review feedback and must be reconciled against this repository's actual
protocol files.

## Bottom-Line Decision

The paper remains viable, but only under a narrower claim:

Browser-local small-model RAG exposes a generation-allocation problem: some
answer components should be deterministic evidence delivery or deterministic
refusal rather than generated text.

The paper should not be framed as a general solution to RAG grounding,
hallucination, rights correctness, or local-model superiority.

## Recommended Title

Working title:

What Should Not Be Generated in Browser-Local Small-Model RAG? Hybrid Answer
Lanes for Deterministic Evidence, Refusal, and Bounded Synthesis

Short title:

Hybrid Answer Lanes for Browser-Local Small-Model RAG

## Final Narrative Frame

Use generation allocation as the top-level frame.

Use rights-aware archive RAG as the stress-test domain, not the whole claim.
Rights, source, provenance, reuse, public-domain, and image-state fields make
the non-generation problem visible because these fields are contract-bearing
and paraphrastic generation can mutate or upgrade them.

The core sentence:

In browser-local small-model RAG, some answer components are better handled as
deterministic evidence or refusal lanes than as generated text, and this
allocation can be evaluated with fidelity, refusal, latency, and usability
metrics.

## Accepted Contribution Set

The paper should present four contributions:

1. Problem formulation: browser-local small-model RAG creates a
   generation-allocation problem.
2. Answer-lane taxonomy and policy: deterministic evidence rendering,
   deterministic refusal, bounded generation, and compound answers.
3. Domain-grounded design case: contract-bearing source, provenance, and
   rights fields are poor candidates for paraphrastic generation.
4. Evaluation protocol: separate evidence-to-output fidelity, evidence
   correctness, over/under-refusal, latency, and usability.

Avoid presenting seven or more contributions. The broader list is useful for
method building, but it weakens the paper story.

## Research Questions

RQ1. Under what combinations of query intent and evidence state should a
browser-local RAG system avoid generation altogether?

RQ2. Does hybrid answer-lane allocation improve evidence-field fidelity and
reduce unsupported outputs relative to always-generate baselines?

RQ3. When evidence is partial or missing, does deterministic
insufficient-evidence refusal reduce unsupported answers without unacceptable
over-refusal?

RQ4. For mixed-intent questions, do compound answers improve clarity,
research usefulness, or trust calibration relative to purely generated
answers?

RQ5. How should latency be reported when browser-local RAG answers can skip
generation entirely?

## Adjacent Work Positioning

### Not Extractive QA

Extractive QA recovers spans, cells, or denotations from evidence. This project
does not propose a reader model. It proposes an answer execution policy over
render, refuse, generate, and compound modes.

### Not Only Guardrails

Guardrails constrain model workflows. This project treats non-generation as a
first-class answer outcome with its own fidelity, latency, and usability
metrics.

### Not Only RAG Abstention

Abstention covers one lane. The paper also studies deterministic field
delivery and compound deterministic-plus-generative answers.

### Not Model Routing

Model routing chooses among model endpoints. Answer-lane routing chooses among
execution modes: deterministic evidence rendering, deterministic refusal,
bounded generation, or compound output.

### Not Legal Rights Determination

The system can preserve supplied rights fields. It cannot determine legal reuse
truth unless a separate source audit establishes that truth.

## Venue Decision

Primary target:

- JCDL, because the strongest evidence and motivation are source, provenance,
  rights metadata, reproducible archive-like fixtures, and public-safe
  evaluation artifacts.

Secondary target:

- SIGIR/CIKM applied or resource track only if the fixture grows beyond the
  first 50-query pilot and includes stronger retrieval/evaluation baselines.

Not yet primary:

- CHI, unless the project adds a real user study around compound answers,
  trust calibration, and visible evidence/generation boundaries.

## Allowed Claims

Allowed after a controlled first study:

- In this controlled fixture, deterministic source/rights lanes reduced field
  mutation relative to all generation.
- The study separates evidence-to-output fidelity from evidence correctness.
- Deterministic refusal can be evaluated for under-refusal and over-refusal as
  separate outcomes.
- On a pinned browser/model/hardware configuration, deterministic lanes can
  reduce warm end-to-end latency for generation-skipping rows.
- Compound answers can be analyzed as a separate mixed-intent stratum.

## Forbidden Claims

Do not claim:

- Deterministic answers are semantically correct.
- The system determines legal reuse rights.
- Hybrid lanes solve hallucination.
- Qwen generation is faster when the lane simply skipped generation.
- Fifty queries prove statistical superiority.
- Results generalize to all browser-local RAG systems.
- The method is a new retrieval algorithm, learned router, or model-training
  contribution.

## Paper-Risk Register

| Risk | Severity | Response |
|---|---:|---|
| Reviewers call it templating | High | Admit one lane is template-like; claim the research question is when templating is the right answer mode. |
| Reviewers call it guardrails | High | Distinguish control-around-generation from non-generation as evaluated output. |
| Reviewers call it extractive QA | Medium | Emphasize execution-mode policy, not span recovery. |
| Metadata can be wrong | Critical | Separate fidelity from source correctness and report audit status. |
| 50 queries are too small | Critical for full paper | Treat first milestone as exploratory or expand before submission. |
| Rule table overfits fixture | High | Freeze rule table, use dev/eval split, and log `routing_undefined`. |
| Browser latency is platform-specific | High | Pin hardware/browser/model and limit latency claims to that environment. |

## Decision For This Repo

The next repository work should prioritize methodology hardening over more
literature prose:

1. Split runtime-visible fixture data from evaluator-only labels.
2. Use a format-matched all-generation baseline.
3. Replace unpaired statistical tests with paired-by-query analysis.
4. Make mixed-intent evidence aggregation explicit, not default sufficient.
5. Convert factual review dimensions into checklist fields.
6. Freeze prompt packs, rule-table hashes, fixture hashes, and anomaly policy
   before any paper-facing run.
