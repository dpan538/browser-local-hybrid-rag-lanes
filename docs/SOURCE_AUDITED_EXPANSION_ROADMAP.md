# Source-Audited Expansion Roadmap

Generated: 2026-06-12

The next experimental problem is not simply increasing sample size. The study
must generalize along four dimensions:

| Dimension | Current Limitation | Expansion Requirement |
|---|---|---|
| Sample size | 50-query exploratory fixture | 100-query Paper v1, then 200/300 robustness sets |
| Evidence | Synthetic, not source-audited records | Source-audited or public-derived evidence |
| Lane coverage | Strongest signal currently comes from refusal rows | Enough rows per lane to test allocation, not only refusal |
| Environment | Browser latency is sensitive to cold/warm state, GC, and backgrounding | Clean runs plus sensitivity analysis |

## Stage 0: Current Protocol Development

Status: complete enough for methodology scaffolding.

Purpose:

- validate the pipeline;
- run the three-condition ablation;
- confirm automatic contract checker behavior;
- record latency fields;
- generate clean exploratory Qwen/WebLLM aggregate.

Boundary:

- synthetic fixture;
- no evidence-correctness claim;
- no usability claim;
- no journal-ready empirical claim.

## Stage 1: Source-Audited 50-Query Clean Run

Purpose:

- replace synthetic evidence with source-audited or public-derived evidence;
- freeze rules and prompt pack before running;
- prove the paper-facing pipeline can run cleanly.

Requirements:

- 50 queries;
- 3 conditions per query = 150 outputs;
- source-audited or public-derived evidence;
- frozen `lane_rules_v1.yaml`;
- frozen `condition_prompt_pack_v1.json`;
- frozen schemas;
- 0 schema errors;
- 0 duplicate query-condition pairs;
- 0 missing query-condition pairs;
- clean environment log;
- no hidden rerouting after seeing results.

Output:

```text
runs/paper_v1_qwen_webllm_50_clean/
reports/PAPER_V1_QWEN_WEBLLM_50_AGGREGATE.md
```

This stage permits a first human-review calibration, not final journal claims.

## Stage 2: 100-Query Paper V1

Purpose:

- create the minimum Information Research-style article package;
- give every answer lane enough observations;
- run a lightweight two-rater blinded semantic audit.

Suggested lane distribution:

| Lane / stratum | Count |
|---|---:|
| source/rights exact field delivery | 15 |
| no-evidence refusal | 15 |
| first/earliest refusal | 15 |
| current-object explanation | 10 |
| comparison | 10 |
| region/period recommendation | 10 |
| more-context / research guidance | 10 |
| mixed-intent / compound answer | 15 |
| Total | 100 |

Human review:

- sample 40 queries;
- review all three condition outputs for sampled queries;
- 120 blinded review rows total;
- include all automatic contract-failure rows;
- include at least half of refusal-expected rows;
- include at least 10 mixed-intent queries;
- stratify remaining rows by lane.

## Stage 3: 200-Query Robustness Expansion

Purpose:

- test whether the pattern survives broader fixture variation.

Add:

- more source families;
- more missing, partial, and contradictory evidence states;
- more rights/source ambiguity;
- more mixed-intent rows;
- more current-object explanation rows.

Human review:

- sample about 60 queries x 3 outputs = 180 blinded rows;
- review all contract-failure and flagged rows.

## Stage 4: 300-Query Stronger Journal Version

Purpose:

- produce a stronger held-out robustness package if needed.

Automatic metrics:

- all 300 queries x 3 outputs = 900 outputs.

Human review:

- stratified sample around 80 queries x 3 outputs = 240 blinded rows;
- all contract-failure or anomaly rows included;
- do not ask reviewers to score all 900 outputs unless there is a specific
  reason.

## Rule Freeze Policy

The rule table must be frozen before evaluation.

Recommended split:

```text
50 dev queries: adjust rule table, prompt pack, and review rubric
100 evaluation queries: first paper-facing evaluation
100-200 holdout queries: robustness without rule changes
```

If resources are limited:

```text
50 dev + 50 eval = 100
```

Do not tune rules on the same query set used for final claims.

## Human Review Entry Gate

Do not begin formal human review until all of the following are true:

1. Fixture is source-audited or explicitly public-derived.
2. Rule table and prompt pack are frozen.
3. Three-condition run is complete with 0 schema errors.
4. Automatic contract check is complete.
5. Blind review pack is generated.
6. Any system change after human review triggers a rerun and a new review pack.

Before this gate, only calibration review is appropriate.
