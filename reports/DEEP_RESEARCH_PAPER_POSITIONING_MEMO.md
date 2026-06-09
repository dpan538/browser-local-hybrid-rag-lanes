# Deep Research Paper Positioning Memo

Generated: 2026-06-09

Scope: paper narrative research for `browser-local-hybrid-rag-lanes`. This memo
uses primary sources where possible and focuses on whether the hybrid
answer-lane idea is sufficiently distinct from adjacent literatures.

## Provisional Thesis

The paper should not be framed as "we added deterministic templates to RAG."
That sounds too small.

The stronger framing is:

Browser-local small-model RAG exposes a generation allocation problem. Because
local 0.8B-class generation is expensive, less reliable than larger cloud
models, and operating over contract-bearing archive evidence, the system must
decide which answer tokens should be generated, which should be rendered from
evidence, and which should be refused.

The paper studies answer execution modes:

- deterministic evidence rendering;
- deterministic refusal;
- bounded local generation;
- compound deterministic plus generative answers.

This is related to RAG, guardrails, extractive QA, model routing, and HCI, but
the combination is not yet well covered.

## Nearby Literatures And The Gap

### 1. Browser-Local Inference And Retrieval

WebLLM establishes browser-local LLM inference using WebGPU and WebAssembly,
with an OpenAI-style API and browser deployment target:
https://arxiv.org/abs/2412.15803

The WebLLM repository and MLC docs make the engineering path concrete:
https://github.com/mlc-ai/web-llm
https://llm.mlc.ai/docs/deploy/webllm.html

MeMemo establishes browser-side retrieval augmentation and private/local RAG
prototyping:
https://arxiv.org/abs/2407.01972
https://zijie.wang/papers/mememo/

Gap: these works establish browser-local generation and retrieval. They do not
ask when a browser-local RAG system should avoid generation entirely and render
contract-bearing evidence fields instead.

### 2. RAG Grounding, Attribution, And Sufficiency

The original RAG paper frames retrieval as non-parametric memory for
knowledge-intensive generation:
https://arxiv.org/abs/2005.11401

AIS evaluates whether generated text is attributable to identified sources:
https://arxiv.org/abs/2112.12870

ALCE evaluates citation quality in long-form generated answers:
https://arxiv.org/abs/2305.14627
https://github.com/princeton-nlp/ALCE

Sufficient Context reframes RAG failures around whether retrieved context is
enough to answer and explores guided abstention:
https://arxiv.org/abs/2411.06037

Self-RAG and CRAG introduce adaptive retrieval/critique/correction mechanisms:
https://arxiv.org/abs/2310.11511
https://arxiv.org/abs/2401.15884

Gap: these works primarily evaluate or improve generated answers, or decide
when to retrieve/abstain. Our question is earlier and more operational: when
the evidence already contains a contract-bearing value, should that value be
generated at all?

### 3. Extractive QA

SQuAD is the canonical extractive QA precedent: answers are spans in a
provided passage:
https://arxiv.org/abs/1606.05250

This is an important reviewer objection. A deterministic source/rights lane
looks extractive because it preserves evidence text.

Distinction: the proposed method is not a learned answer-span extractor. It is
a lane-level execution policy over structured archive evidence. It decides
whether to render fields, refuse, call a local model, or compose a compound
answer. The unit of contribution is the execution policy and its evaluation,
not extraction accuracy.

### 4. Guardrails, Neuro-Symbolic Systems, And Structured Generation

MRKL motivates modular neuro-symbolic systems:
https://arxiv.org/abs/2205.00445

NeMo Guardrails motivates programmable rails around LLM applications:
https://arxiv.org/abs/2310.10501

LMQL and SGLang show that LLM applications can be programmed and optimized as
structured language-model programs:
https://arxiv.org/abs/2212.06094
https://arxiv.org/abs/2312.07104

Gap: these works support programmatic control around generation. Our point is
not only "constrain the model." It is "do not invoke the model for some answer
lanes." That makes latency attribution and usability tradeoffs central.

### 5. LLM Routing And Cascades

FrugalGPT and RouteLLM show that routing can reduce cost or optimize
quality/cost tradeoffs across models:
https://arxiv.org/abs/2305.05176
https://arxiv.org/abs/2406.18665

Hybrid LLM studies routing between smaller edge-deployable models and larger
cloud models:
https://arxiv.org/abs/2404.14618

Gap: model-routing work chooses which model to call. This project chooses
whether to call a model, render evidence, refuse, or compose. The route target
is an execution mode, not a model endpoint.

### 6. UI/Runtime-Mediated AI Systems

Mixed-initiative UI work argues that automation and direct manipulation should
be coordinated:
https://doi.org/10.1145/302979.303030
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/chi99horvitz.pdf

Human-AI Interaction Guidelines provide a design basis for uncertainty,
appropriate trust, and user control:
https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/

AI Chains shows that decomposed LLM workflows can improve transparency and
controllability:
https://arxiv.org/abs/2110.01691

Gap: these works support UI/runtime mediation, but they do not provide a RAG
evaluation protocol for browser-local small-model answer lanes with separate
evidence fidelity, source correctness, latency, and usability metrics.

### 7. Latency Accounting

DistServe separates prefill and decoding and explicitly treats TTFT and TPOT
as phase-specific latency targets:
https://arxiv.org/abs/2401.09670

vLLM/PagedAttention evaluates throughput under latency constraints:
https://arxiv.org/abs/2309.06180

WebGPU dispatch-overhead work shows that browser-local batch-size-1 LLM
inference has distinct overheads across browsers, backends, and GPUs:
https://arxiv.org/abs/2604.02344

Gap: serving papers separate model-inference phases. Our paper separates model
generation from deterministic assembly inside a user-facing RAG answer. That
requires reporting `qwen_generation_latency` and `hybrid_system_latency`
separately.

## Narrative Risk Register

| Reviewer objection | Why it is plausible | Required response |
|---|---|---|
| "This is just extractive QA." | Deterministic source/rights lanes copy fields from evidence. | We route among render/refuse/generate/compound modes; extraction is not the contribution. |
| "This is just guardrails." | Refusal and exact field rules look like rails. | Guardrails constrain generation; we evaluate non-generation as an execution mode. |
| "This is just RAG abstention." | Refusal lanes overlap with guided abstention. | We include abstention, but also exact field rendering and compound answers. |
| "This is just model routing." | The method routes requests. | The route target is execution mode, not which LLM to call. |
| "This is product engineering." | Rule tables and UI rendering sound implementation-specific. | The contribution is an auditable evaluation protocol for generation allocation under browser-local constraints. |
| "Metadata can be wrong." | Deterministic output preserves upstream errors. | We separate evidence-to-output fidelity from evidence correctness and require source audit status. |

## Recommended Paper Claim

Main claim:

Browser-local small-model RAG benefits from answer-lane execution policies that
separate deterministic evidence delivery from generative synthesis.

Careful version:

On a controlled rights-aware archive fixture, a static hybrid answer-lane
policy can reduce unnecessary local generation for exact/refusal tasks while
preserving the model for synthesis tasks. The method must be evaluated with
separate evidence fidelity, evidence correctness, latency, and usability
metrics.

Avoid:

- "Deterministic answers are correct."
- "The model is faster."
- "Hybrid lanes solve RAG hallucination."
- "The system determines legal reuse."

## Paper Shape

1. Introduction: local small-model RAG makes generation allocation visible.
2. Problem: not every answer token should be generated.
3. Related work: browser-local RAG, RAG attribution/sufficiency, extractive QA,
   guardrails, model routing, HCI, latency accounting.
4. Method: answer-lane execution policy.
5. Fixture: rights-aware archive-like records and mixed-intent queries.
6. Conditions: all-generation, hybrid without refusal, full hybrid.
7. Metrics: contract, evidence fidelity, source audit, latency, usability.
8. Findings: expected tradeoff patterns, not only wins.
9. Limitations: rule overfitting, evidence correctness, reviewer variability,
   browser variance.

## Current Confidence

Paper value: moderate-to-high if framed as generation allocation, not as a
template trick.

Highest-risk issue: novelty. The paper must make clear that "what should not
be generated?" is the research question, and that browser-local small models
make this question empirically important.

Most publishable empirical angle: Condition 2 vs Condition 3. It tests whether
deterministic refusal improves compliance at the cost of usability. That is a
real result even if the answer is a tradeoff.

Best venue framing:

- JCDL: rights-aware archive evidence, provenance, and reproducible fixture.
- CHI: user trust, format consistency, refusal usability, mixed-intent
  interaction.
- CIKM/SIGIR applied track: RAG evaluation and retrieval/evidence policy.

## Source List

- WebLLM: https://arxiv.org/abs/2412.15803
- WebLLM repo: https://github.com/mlc-ai/web-llm
- MLC WebLLM docs: https://llm.mlc.ai/docs/deploy/webllm.html
- MeMemo: https://arxiv.org/abs/2407.01972
- MeMemo project: https://zijie.wang/papers/mememo/
- RAG: https://arxiv.org/abs/2005.11401
- AIS: https://arxiv.org/abs/2112.12870
- ALCE: https://arxiv.org/abs/2305.14627
- Sufficient Context: https://arxiv.org/abs/2411.06037
- Self-RAG: https://arxiv.org/abs/2310.11511
- CRAG: https://arxiv.org/abs/2401.15884
- SQuAD: https://arxiv.org/abs/1606.05250
- MRKL: https://arxiv.org/abs/2205.00445
- NeMo Guardrails: https://arxiv.org/abs/2310.10501
- LMQL: https://arxiv.org/abs/2212.06094
- SGLang: https://arxiv.org/abs/2312.07104
- FrugalGPT: https://arxiv.org/abs/2305.05176
- RouteLLM: https://arxiv.org/abs/2406.18665
- Hybrid LLM routing: https://arxiv.org/abs/2404.14618
- Mixed-initiative UI: https://doi.org/10.1145/302979.303030
- Microsoft Human-AI Interaction Guidelines:
  https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/
- AI Chains: https://arxiv.org/abs/2110.01691
- DistServe: https://arxiv.org/abs/2401.09670
- vLLM/PagedAttention: https://arxiv.org/abs/2309.06180
- WebGPU dispatch overhead: https://arxiv.org/abs/2604.02344
