# Methodology Build Plan

Generated: 2026-06-08

This plan defines the next steps for turning the hybrid answer-lane idea into
a reproducible research method.

## Phase 1: Research Definition

Goal: make the paper problem precise before implementing a new runner.

Tasks:

1. Define the lane taxonomy.
2. Define which evidence fields are contract-bearing.
3. Define deterministic, generative, and mixed execution modes.
4. Define the latency vocabulary:
   - `retrieval_latency`;
   - `deterministic_assembly_latency`;
   - `qwen_generation_latency`;
   - `hybrid_system_latency`;
   - `ttft`;
   - `total_latency`;
   - `tokens_per_second`.
5. Define prohibited claims:
   - no inferred rights permission;
   - no public-domain upgrade;
   - no unsupported first/earliest claim;
   - no claim that deterministic answers are Qwen-generated.

Deliverables:

- lane taxonomy memo;
- metric schema;
- contract field specification.
- deterministic lane contract.

## Phase 2: Minimal Reproducible Fixture

Goal: build a small public-safe fixture that can reproduce the method without
depending on private product state.

Tasks:

1. Create a compact fixture format for archive-like records.
2. Include source, rights, image-state, date, region, title, and topology
   fields.
3. Create labeled queries for:
   - source/rights;
   - no-evidence refusal;
   - first/earliest refusal;
   - comparison;
   - more-context;
   - region/period recommendation;
   - current-object explanation.
4. Add a fixture manifest explaining provenance and non-product status.

Deliverables:

- `fixtures/records.jsonl`;
- `fixtures/queries.jsonl`;
- `fixtures/labels.jsonl`;
- fixture README.

## Phase 3: Execution Policy Specification

Goal: define the method independently of a specific runtime implementation.

Tasks:

1. Write a routing policy:
   - deterministic source/rights;
   - deterministic refusal;
   - generative explanation;
   - generative comparison/recommendation;
   - mixed deterministic prefill plus bounded generation.
2. Specify how each lane assembles the evidence packet.
3. Specify output contracts for each lane.
4. Specify when Qwen/WebLLM is invoked and when it is skipped.

Deliverables:

- execution policy spec;
- lane output contract table;
- metric attribution rules.

## Phase 4: Baseline Runner

Goal: produce comparable baseline data without large experiments.

Tasks:

1. Implement a deterministic-only oracle for exact lanes.
2. Implement a generation-runner interface that can be wired to WebLLM later.
3. Emit JSONL run records with lane, execution mode, contract result, and
   latency fields.
4. Add small smoke tests for schema and contract validation.
5. Keep deterministic lane assignment rule-based and fixture-auditable for the
   first version; learned/model-assisted routers are later ablations.

Deliverables:

- local runner skeleton;
- JSON schema;
- smoke test fixture;
- sample run export.

## Phase 5: Evaluation Protocol

Goal: evaluate contract compliance, latency, and usability together.

Tasks:

1. Mechanical contract metrics:
   - runtime errors;
   - metric issues;
   - contract failures;
   - contract warnings;
   - exact source/rights preservation;
   - refusal correctness.
2. Latency metrics:
   - P50/P95/max by lane;
   - model-only latency for generated lanes;
   - full hybrid system latency for all lanes.
3. Human review metrics:
   - helpfulness;
   - rights clarity;
   - source clarity;
   - refusal clarity;
   - research usefulness.
4. Report deterministic and generated outputs separately.

Deliverables:

- evaluation protocol;
- review sheet template;
- metric summary script.
- refusal examples and over-refusal/under-refusal labels.

## Phase 6: Paper Framing

Goal: turn the method into a publishable contribution.

Tasks:

1. Refine related work into categories:
   - browser-local inference;
   - browser-local retrieval and private RAG;
   - RAG grounding and citation faithfulness;
   - refusal and abstention;
   - guardrails and structured generation;
   - UI/runtime-mediated AI systems;
   - latency accounting.
2. Define claims that do not overstate model performance.
3. Identify the strongest venue framing:
   - JCDL for archive/evidence method;
   - CHI for interaction and trust;
   - SIGIR for retrieval/evaluation method.

Deliverables:

- paper outline;
- contribution statement;
- threat model and limitations.

## First Experimental Milestone

The first real experiment should be small:

1. 50-query fixture.
2. Three execution conditions:
   - all-generation baseline;
   - hybrid without refusal lane: deterministic source/rights plus generative
     guidance, but refusal remains model-handled;
   - full hybrid: deterministic source/rights plus deterministic refusal plus
     generative guidance.
3. Required output:
   - contract results;
   - `qwen_generation_latency`;
   - `hybrid_system_latency`;
   - lane-level usability review sample.

Success condition:

The hybrid policy should reduce user-visible latency for exact/refusal lanes
without adding contract failures, while preserving useful generative answers in
research-guidance lanes. For the 50-query milestone, P95 is exploratory rather
than definitive; use a 1.5x all-generation baseline guardrail and inspect
slow-row causes before making claims.

## Method Decisions Approved 2026-06-09

1. Deterministic lanes guarantee rule-conforming output from supplied evidence,
   not upstream semantic truth. Evidence correctness is a separate source-audit
   metric.
2. The 50-query milestone treats P95 as exploratory. P50/P75/P90/P95/max and
   slow-row counts should all be reported by lane and condition.
3. Refusal correctness must distinguish correct refusal, over-refusal,
   under-refusal, qualified answers, and ambiguous boundaries.
4. The first ablation uses three conditions: all generation, hybrid without
   deterministic refusal, and full hybrid with deterministic refusal.
5. First-version deterministic lanes are rule-based rendering over structured
   retrieved evidence. They are not learned routers or small-model distillation.
