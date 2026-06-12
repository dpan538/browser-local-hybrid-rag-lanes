# Paper V1 Freeze Plan

Generated: 2026-06-12

The next phase is not another loose diagnostic run. It is a controlled Paper v1
freeze that either produces a paper-facing evidence package or clearly records
why the project remains exploratory.

## Freeze Goal

Produce a reproducible Paper v1 package for:

- hybrid answer-lane allocation;
- deterministic evidence-field delivery;
- deterministic refusal;
- bounded Qwen/WebLLM generation;
- latency attribution;
- blinded usability review.

The active primary target is Journal of Information Science. The paper-facing
minimum for that route is a 200-query source-audited run. A source-audited
50-query clean run is the entry gate, and a 100-query run is a calibration
stage, not the final journal package. A 300-query run remains the preferred
stronger version and the stretch route for OIR/AJIM.

## Research Questions

RQ1. Which answer components in browser-local small-model RAG should avoid
generation and be handled by deterministic rendering or refusal?

RQ2. Compared with all-generation and hybrid-without-refusal baselines, does
full hybrid lane allocation reduce automatic contract failures and
under-refusal?

RQ3. How should latency be attributed when a browser-local RAG system can skip
model generation for some lanes?

RQ4. Does deterministic refusal or deterministic field rendering reduce
perceived usefulness, or preserve usability while improving fidelity?

## Unit Of Analysis

The unit of analysis is the query-condition pair:

```text
q001-C1
q001-C2
q001-C3
...
```

All primary contrasts must be paired by query.

## Conditions

| Condition | Name | Meaning |
|---|---|---|
| C1 | All generation | Qwen generates all answer values, caveats, and refusal behavior. |
| C2 | Hybrid field | Deterministic source/rights/exact-field rendering; refusal remains generated. |
| C3 | Full hybrid | Deterministic field rendering, deterministic refusal, and bounded generation for synthesis. |

## Primary Contrasts

1. C1 vs C2: deterministic field-rendering effect.
2. C2 vs C3: deterministic refusal effect.

The current exploratory result suggests C2 vs C3 is the strongest signal, but
Paper v1 must test it under a frozen fixture and review protocol.

## Paper V1 Gates

### Gate 1: Fixture Provenance

Paper v1 cannot use the current synthetic fixture for evidence-correctness
claims. Before freeze, create one of:

- `fixtures/source_audited_50/`, with explicit source audit status; or
- a public-derived fixture where every source field is reproducibly derived
  from committed non-image metadata.

The synthetic fixture may remain as a development fixture.

Recommended path:

```text
synthetic 50 -> source-audited 50 -> source-audited 100 calibration ->
source-audited 200 JIS candidate -> source-audited 300 stronger/stretch
```

Do not treat sample-size expansion as the only form of generalization. Paper
v1 must also improve evidence provenance, lane coverage, and environment
accounting.

### Gate 2: Freeze Manifest

Generate:

```text
manifests/protocol_v1_freeze_manifest.json
```

The manifest must include:

- fixture;
- runtime view;
- evaluation view;
- warmup queries;
- rule table;
- refusal matrix;
- condition prompt pack;
- run-record schema;
- review instructions;
- automatic contract checker;
- diagnostics and aggregation scripts;
- analysis script;
- claim/non-claim ledger.

### Gate 3: Clean Browser Run

Target:

```text
runs/paper_v1_qwen_webllm_50_clean/
```

Requirements:

- 50 queries x 3 conditions = 150 rows;
- 0 schema errors;
- 0 duplicate query-condition pairs;
- 0 missing query-condition pairs;
- `tab_backgrounded_rows = 0`;
- long-task/GC flags recorded, not hidden;
- cold-start and warm rows separated;
- Qwen model id and primary identity recorded.

Segmented runs are acceptable if every segment uses the same freeze manifest.

The 50-query clean run is used to prove the source-audited protocol. The
100-query run calibrates the fixture and review process. The 200-query run is
the JIS paper-facing candidate. The 300-query run is the preferred stronger
version, revision reserve, or OIR/AJIM stretch package.

### Gate 4: Automatic Analysis

Generate the six standard tables:

1. Fixture composition by lane and evidence state.
2. Contract failures by condition.
3. Refusal false positive / false negative by condition.
4. Qwen invocation count and skipped-generation rows.
5. Warm latency by condition and lane.
6. Human review outcome by condition.

### Gate 5: Blinded Human Review

Generate condition-hidden review packs for at least two reviewers.

Reviewers should not see:

- condition names;
- rule traces;
- latency;
- expected failure labels;
- automatic contract flags.

Reviewers should see:

- query;
- answer;
- minimal source/evidence display if needed for faithfulness;
- simple scoring fields.

Formal human review starts only after:

1. the fixture is source-audited or public-derived;
2. rules and prompt pack are frozen;
3. the three-condition run has 0 schema errors;
4. automatic contract checks are complete;
5. blind review packs are generated;
6. no system changes will be made without rerunning the review package.

Before this gate, use only calibration review.

For a 200-query JIS candidate run, review a paired stratified sample:

```text
60 queries x 3 condition outputs = 180 blinded review rows
```

Include all automatic contract-failure rows, anomaly rows, enough
refusal-expected rows, enough mixed-intent rows, and stratified remaining rows
by lane. Use the 100-query stage only for calibration. If the study expands to
300 queries, rerun or extend the review sample to 80-100 queries x 3 condition
outputs.

## Stop Conditions

Do not call a run paper-facing if:

- the fixture is still synthetic and the claim needs evidence correctness;
- the run has tab-background contamination;
- condition labels leak into human review;
- raw records are missing or not indexed;
- scripts changed after manifest generation;
- claims are stronger than `CLAIMS_AND_NON_CLAIMS.md` allows.

## Next Immediate Work

1. Build or select the source-audited 50-query fixture candidate.
2. Generate Paper v1 runtime/evaluation views.
3. Create the Paper v1 freeze manifest.
4. Run the clean browser Qwen/WebLLM 50-query gate.
5. If the gate passes, expand to source-audited 100-query calibration.
6. Run the 200-query JIS candidate experiment.
7. Generate blind review packs for 180 sampled outputs.
8. Run two-rater review.
9. Produce final claim ledger.
10. If time allows, expand to 300 queries as a stronger version or stretch
    venue package.
