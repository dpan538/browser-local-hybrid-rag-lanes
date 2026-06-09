# Prompt 02: Method And Evaluation Deep Research

Generated: 2026-06-09

Copy the full prompt below into an independent deep-research agent.

---

You are an independent methods reviewer and experimental-design researcher.
Your task is to stress-test the methodology for a possible paper titled:

**What Should Not Be Generated? Hybrid Answer Lanes for Browser-Local
Small-Model RAG**

You are not being asked to run the main experiment. You are being asked to
audit and improve the research protocol before the experiment becomes too
rigid.

Use primary sources wherever possible. Preserve links. Distinguish
source-supported methodological recommendations from your own judgment.

## Repository Context

The research repo is:

`browser-local-hybrid-rag-lanes`

The repository studies hybrid answer lanes for browser-local small-model RAG.
The paper idea is that a local model should not generate every answer token.
Some answer lanes should be deterministic UI/runtime output, and other lanes
should remain generative.

This is an independent reproducible research repository. It is not an archive
product iteration. Do not modify product code, browser runtime code, model
weights, cache, private data, or downloaded image assets.

## Current Method Summary

The current experiment design compares three conditions:

1. `condition_1_all_generation`
   - Every answer is sent to the local model with the retrieved evidence.

2. `condition_2_hybrid_no_refusal`
   - Source/rights and exact evidence fields are deterministic.
   - Research guidance remains generative.
   - Insufficient-evidence refusal is still handled by the model.

3. `condition_3_full_hybrid`
   - Source/rights and exact evidence fields are deterministic.
   - Mandatory insufficient-evidence refusal is deterministic.
   - Explanatory, comparative, recommendation, and mixed-intent tasks remain
     generative or compound.

The core ablation logic is:

- Condition 1 vs Condition 2 isolates deterministic evidence-field delivery.
- Condition 2 vs Condition 3 isolates deterministic refusal.
- Mixed-intent rows test compound deterministic-plus-generative answers and
  routing ambiguity.

The key evaluation distinction is:

- `evidence_to_output_fidelity`: whether the answer preserved the supplied
  evidence under the deterministic contract.
- `evidence_correctness`: whether the supplied evidence is semantically correct
  relative to the source.

Deterministic rendering only claims the first. It does not guarantee the
second.

The key latency distinction is:

- `qwen_generation_latency`: time spent generating with the local model.
- `hybrid_system_latency`: end-to-end user-visible answer latency including
  retrieval, deterministic assembly, contract checks, optional generation, and
  UI/runtime assembly.

If a deterministic lane skips generation, the paper must not claim that Qwen
generation was faster. It can claim reduced end-to-end latency for that answer
lane if the measurement supports it.

## Local Documents To Read First

Read these repository documents before searching externally:

- `README.md`
- `docs/ABLATION_AND_EVALUATION_PROTOCOL.md`
- `docs/DETERMINISTIC_LANE_CONTRACT.md`
- `docs/REVIEW_SHEET_GUIDE.md`
- `docs/FIXTURE_SCHEMA.md`
- `docs/LANE_DECISION_FLOW.md`
- `docs/THREATS_AND_BASELINES.md`
- `docs/PAPER_NARRATIVE_DRAFT.md`
- `config/lane_rules_v1.yaml`
- `config/refusal_decision_matrix.csv`
- `schemas/run_record_schema.json`
- `schemas/environment_stability_log_schema.json`
- `schemas/experiment_fixture_schema.json`
- `schemas/golden_answers_schema.json`
- `fixtures/experiment_fixture.jsonl`
- `fixtures/drafts/mixed_intent_query_drafts.jsonl`
- `review/golden_answers.json`
- `scripts/evidence_aggregator.py`
- `scripts/validate_fixture.py`

Treat these files as project context, not as external evidence.

## Research Goal

Produce a method-and-evaluation deep research report that determines whether
the current experimental plan is strong enough for a paper attempt, and how it
should be improved before implementation.

You should focus on:

1. Whether the three-condition ablation is valid.
2. Whether deterministic lane correctness is defined precisely enough.
3. Whether refusal correctness can be judged reproducibly.
4. Whether the fixture schema is sufficient.
5. Whether mixed-intent and compound answers are handled honestly.
6. Whether latency measurement is defensible for browser-local inference.
7. Whether a 50-query first milestone can support any claims.
8. Whether the human review sheet can produce reliable labels.
9. Whether the statistical plan is appropriate for small-n exploratory work.
10. Whether reproducibility artifacts are complete.

Be critical. Identify hidden assumptions, confounds, and failure modes.

## Source Policy

Use primary sources first:

- evaluation papers;
- benchmark or dataset papers;
- official schema or standard documents;
- statistical-method references from credible sources;
- official system papers for latency/runtime issues;
- HCI papers on human evaluation, calibration, and trust where relevant.

Avoid relying on:

- generic blog posts;
- unverified claims about browser performance;
- secondary summaries unless used only to discover primary sources.

For every important source, record:

- title;
- authors or organization;
- year;
- link;
- what the source establishes;
- how it changes or supports the proposed method.

If you use web search, include links in the final report.

## Required Method Areas

### 1. Validity Of The Three-Condition Ablation

Audit the current conditions:

- all-generation baseline;
- hybrid without deterministic refusal;
- full hybrid with deterministic refusal.

Questions:

- Does Condition 2 cleanly isolate deterministic evidence-field rendering?
- Does Condition 3 cleanly isolate deterministic refusal?
- Are there hidden differences between conditions, such as output formatting,
  prompt length, retrieval behavior, or evidence packet structure?
- Should all conditions receive the same retrieved evidence packet?
- Should all conditions receive the same query order?
- Should condition order be randomized or counterbalanced?
- Should reviewers be blinded to condition?
- Does the all-generation baseline need structured-output prompting, or would
  that make the baseline too strong/too weak?
- Is an all-deterministic counterfactual necessary, even if not a primary
  baseline?

Required output:

- A verdict on whether the ablation is internally valid.
- A list of confounds to control.
- Any recommended fourth condition or rejected condition, with rationale.

### 2. Deterministic Lane Correctness

The current contract says deterministic lanes guarantee rule-following over
provided evidence, not semantic truth. Audit this distinction.

Questions:

- Is `evidence_to_output_fidelity` enough to avoid the "metadata can be wrong"
  objection?
- Should deterministic lane correctness include:
  - all required fields rendered;
  - placeholders for missing fields;
  - no field mutation;
  - no unsupported upgrade;
  - source citation preserved;
  - field labels not misleading;
  - output format consistent?
- How should source-audit status interact with deterministic-lane pass/fail?
- Should an answer with correct field fidelity but failed source audit be a
  deterministic pass and evidence-correctness fail?
- How should OCR errors, missing metadata, inconsistent fields, or conflicting
  records be reported?

Required output:

- A deterministic lane correctness rubric.
- A failure taxonomy.
- A table separating contract failure, contract warning, source-audit failure,
  and usability issue.

### 3. Rule Table And Routing Audit

The current static rules live in `config/lane_rules_v1.yaml`.

Questions:

- Is a static rule table the right first-version methodology?
- Does a versioned rule table make the experiment reproducible enough?
- How should `routing_undefined` be counted?
- Should a routing bug count as contract failure, configuration error, or
  separate routing failure?
- Are intent labels too close to expected behavior labels?
- Should query labels be assigned by humans independently from rule authors?
- How can rule overfitting to the 50-query fixture be detected?
- Does the rule table need pre-registration before outputs are inspected?

Required output:

- Rule-table audit.
- Suggested rule-table fields, if any are missing.
- Recommended versioning and pre-registration procedure.
- Routing confusion-matrix design.

### 4. Fixture Schema And Evidence-State Aggregation

The current canonical fixture is a single JSONL file:

`fixtures/experiment_fixture.jsonl`

Each row contains:

- `query`;
- `evidence_packet`;
- `expected_behavior`.

The evidence packet contains:

- records;
- field-state checklist;
- aggregated evidence state.

Questions:

- Is the single-file fixture design better than separate records/queries/labels
  for this experiment?
- Is there too much label leakage from `expected_behavior` into routing?
- Should the runner see `expected_behavior`, or should it be used only by
  evaluators?
- Should `query.intent_label` be visible to the runtime, or only to the
  experimental controller?
- Are `field_checklist` and `aggregated_evidence_state` operational enough?
- Does `mixed` defaulting to sufficient hide risk?
- Does the schema support multiple records and contradictory fields?
- Should record-level `source_audit_status` be aggregated at row level?
- Are retrieved snippets needed to separate retrieval failure from generation
  failure?
- Should synthetic records be labeled differently from source-audited records?

Required output:

- Fixture-schema critique.
- Recommended schema changes.
- A minimal v1 fixture row checklist.
- A validation checklist that complements `scripts/validate_fixture.py`.

### 5. Refusal Correctness And Refusal Decision Trace

The current review labels include:

- `correct_refusal`;
- `over_refusal`;
- `under_refusal`;
- `qualified_answer_correct`;
- `ambiguous_refusal_boundary`.

Questions:

- How should reviewers decide if a refusal is correct?
- What evidence states should trigger deterministic refusal?
- What evidence states should trigger qualified answers?
- What evidence states should trigger answer-with-caveat instead of refusal?
- How should contradictory evidence be treated?
- What if a refusal gives the wrong reason?
- How should "policy refusal" differ from "missing evidence refusal"?
- How should over-refusal be measured when evidence is partial?
- How should usability be scored for a correct but unhelpful refusal?

Required output:

- Refusal decision rubric with examples.
- Evidence-state-to-action decision table.
- `refusal_decision_trace` schema recommendations.
- A plan for measuring over-refusal and under-refusal separately.

### 6. Mixed-Intent And Compound Answers

The current plan includes 10 mixed-intent or ambiguous queries in the 50-query
first milestone.

Questions:

- Is 10 mixed-intent rows enough to reveal routing ambiguity?
- Should mixed-intent rows be evaluated separately from clean-lane rows?
- Can compound answers fairly compare against all-generation answers?
- Should compound outputs be structured fields plus paragraph, or another
  format?
- Does format consistency become a usability confound?
- Should reviewers score the deterministic and generative parts separately?
- How should a compound answer be marked if the deterministic part is perfect
  but the generative part hallucinates?
- How should a compound answer be marked if the generative part is useful but
  the deterministic part omits a required field?

Required output:

- Compound-answer evaluation rubric.
- Mixed-intent routing-confusion design.
- Guidance on how to avoid overclaiming from mixed-intent rows.

### 7. Latency Measurement For Browser-Local Hybrid Systems

The first experiment must separate:

- cold start;
- warm execution;
- retrieval latency;
- deterministic assembly latency;
- local generation latency;
- total user-visible latency;
- browser environment anomalies.

Questions:

- How should warmup be handled?
- Should 3-5 dummy warmup queries be enough?
- Should the first measured query be reported separately?
- How should tab suspension, GC, long tasks, thermal throttling, model load,
  WebGPU adapter selection, and network retrieval be logged?
- Should rows with anomalies remain in primary results?
- Is P95 meaningful with 50 queries?
- Should P90 plus anomaly counts be primary?
- Should latency be reported per-lane and per-condition?
- How should `latency_saved_by_deterministic` be computed?
- Should condition order be randomized to avoid warmup bias?
- Should a fixed hardware/browser configuration be required?

Required output:

- Latency instrumentation plan.
- Warm/cold reporting plan.
- Environment stability log recommendations.
- A statement of what latency claims are allowed and forbidden.

### 8. Small-N Statistics And Exploratory Claims

The first milestone has 50 queries, repeated across conditions.

Questions:

- What claims are legitimate from 50 queries?
- Should results be treated as paired by query across conditions?
- Should the analysis use paired tests rather than independent tests?
- Should latency use nonparametric paired methods?
- Should contract failures use McNemar's test, Fisher exact test, bootstrap, or
  descriptive counts?
- Should helpfulness use ordinal models, Wilcoxon signed-rank, Mann-Whitney U,
  or descriptive summaries?
- How should multiple comparisons be handled?
- Should confidence intervals be reported?
- Should effect sizes matter more than p-values?
- How should the paper discuss exploratory versus confirmatory findings?

Required output:

- Statistical analysis plan.
- Which tests to use and which to avoid.
- Recommended plots.
- Minimum reporting table.
- Claims permitted at n=50.

### 9. Human Review, Calibration, And Inter-Rater Agreement

The current plan includes reviewer calibration and possible Cohen's kappa or
ICC.

Questions:

- How many reviewers are minimally defensible?
- Should reviewers be blinded to condition?
- Should the same reviewer score all conditions for a query?
- How should calibration examples be selected?
- Should there be gold answers for every query or only calibration queries?
- How should disagreements be resolved?
- Which dimensions need categorical agreement versus numeric agreement?
- Is Cohen's kappa appropriate for refusal labels?
- Is ICC appropriate for 1-5 helpfulness scores?
- What threshold should trigger recalibration?

Required output:

- Human-review protocol.
- Calibration procedure.
- Inter-rater agreement plan.
- Consensus resolution procedure.
- Reviewer-sheet field recommendations.

### 10. Hallucination And Unsupported Claims

The current plan includes:

- hallucination count;
- hallucination severity;
- unsupported claims;
- unsupported rights/status upgrades.

Questions:

- How should hallucination be defined when evidence is partial?
- How should unsupported interpretation differ from fabricated fact?
- Should unsupported rights/status upgrades be a separate high-severity class?
- Should reviewers count every unsupported claim or only material claims?
- Should deterministic fields be exempt from hallucination scoring but subject
  to field mutation scoring?
- How should generated historical context be evaluated if it is plausible but
  not in evidence?

Required output:

- Hallucination taxonomy.
- Severity scale.
- Examples for rights/source/provenance versus historical explanation.

### 11. Reproducibility Package

Current artifacts include:

- rule table;
- refusal decision matrix;
- fixture schema;
- golden answers schema;
- run record schema;
- environment stability log schema;
- sample fixture;
- validation script;
- analysis notebook placeholder.

Questions:

- What else is required for a reproducible first study?
- Should there be a frozen prompt pack for each condition?
- Should model/browser versions be pinned?
- Should hardware details be included?
- Should randomization seeds and query order be recorded?
- Should output examples be committed?
- Should raw run records be public-safe?
- Should source-audit logs be separated from fixture labels?

Required output:

- Reproducibility checklist.
- Required metadata for each run.
- Folder structure recommendation.
- Which artifacts must be immutable after pre-registration.

## External Literature To Consult

Search for primary sources on:

- RAG evaluation and attribution;
- abstention/refusal evaluation;
- human evaluation of QA or generated answers;
- inter-rater agreement for categorical and ordinal labels;
- latency measurement in LLM serving;
- browser-local WebGPU performance measurement;
- HCI evaluation of AI assistance and trust;
- reproducibility guidelines for information retrieval or digital libraries.

Seed sources:

- RAG: https://arxiv.org/abs/2005.11401
- AIS: https://arxiv.org/abs/2112.12870
- ALCE: https://arxiv.org/abs/2305.14627
- Sufficient Context: https://arxiv.org/abs/2411.06037
- Self-RAG: https://arxiv.org/abs/2310.11511
- CRAG: https://arxiv.org/abs/2401.15884
- WebLLM: https://arxiv.org/abs/2412.15803
- MLC WebLLM docs: https://llm.mlc.ai/docs/deploy/webllm.html
- WebGPU dispatch overhead: https://arxiv.org/abs/2604.02344
- DistServe: https://arxiv.org/abs/2401.09670
- vLLM / PagedAttention: https://arxiv.org/abs/2309.06180
- Microsoft Human-AI Interaction Guidelines:
  https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/

Add additional primary sources as needed.

## Required Output

Write the final report as:

`reports/deep_research_outputs/method_evaluation/METHOD_AND_EVALUATION_DEEP_RESEARCH_REPORT.md`

If your environment cannot write files, provide the complete Markdown report in
your answer.

The report must include these sections:

1. Executive summary
2. Bottom-line methodology verdict
3. Validity of the three-condition ablation
4. Deterministic lane correctness rubric
5. Rule-table and routing audit
6. Fixture schema audit
7. Refusal correctness decision protocol
8. Mixed-intent and compound-answer evaluation
9. Latency instrumentation and reporting plan
10. Small-n statistical analysis plan
11. Human-review calibration and IRA plan
12. Hallucination and unsupported-claim taxonomy
13. Reproducibility package checklist
14. Threats to validity
15. Concrete recommended changes before running the first experiment
16. Open questions that must remain limitations
17. Full source list with links

## Required Tables

Include at least these tables:

1. Condition comparison and isolated variable table.
2. Metric-to-claim table.
3. Deterministic lane pass/fail/warning table.
4. Evidence-state-to-refusal-action table.
5. Compound-answer scoring table.
6. Latency metric definitions table.
7. Statistical test recommendation table.
8. Reviewer-label agreement table.
9. Reproducibility artifact checklist.
10. Threat-to-mitigation table.

## Required Verdict Format

End with a short verdict:

- Methodology readiness: Ready / Needs minor revision / Needs major revision /
  Not ready
- Biggest internal-validity risk:
- Biggest external-validity risk:
- Biggest latency-measurement risk:
- Biggest human-review risk:
- Most important change before running:
- Claim that is currently supportable:
- Claim that is not yet supportable:

## Allowed And Forbidden Claims

You must explicitly state which claims are allowed.

Examples of potentially allowed claims:

- "In this controlled fixture, deterministic source/rights lanes reduced field
  mutation compared with all-generation."
- "Condition 3 reduced under-refusal but may have increased over-refusal."
- "Deterministic lanes reduced warm end-to-end latency for exact-field tasks."
- "The study separates evidence-to-output fidelity from source correctness."

Examples of forbidden claims unless separately proven:

- "Deterministic answers are semantically correct."
- "The system determines legal reuse rights."
- "Hybrid lanes solve hallucination."
- "Qwen generation is faster."
- "The findings generalize to all browser-local RAG systems."
- "Fifty queries prove statistical superiority."

## Quality Bar

The report should be strong enough that the project team can revise the
protocol before running experiments, and strong enough that a skeptical
reviewer can see that obvious threats were anticipated.

Do not write a generic evaluation plan. Write a concrete audit of this
specific hybrid answer-lane methodology.

Your job is to make the experiment harder to fool and easier to reproduce.
