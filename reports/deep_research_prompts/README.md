# Deep Research Prompt Package

Generated: 2026-06-09

This folder contains two long-form prompts for independent deep research on
hybrid answer lanes for browser-local small-model RAG.

These prompts are intended for read-only use by other branches or by external
research agents. They should be treated as task specifications, not as
completed research outputs.

## Prompts

- `PROMPT_01_LITERATURE_POSITIONING_DEEP_RESEARCH.md`
  - Purpose: literature positioning, novelty test, reviewer-objection map,
    venue framing, and contribution sharpening.

- `PROMPT_02_METHOD_AND_EVALUATION_DEEP_RESEARCH.md`
  - Purpose: methodology stress test, evaluation design, fixture/rule audit,
    latency/statistics plan, reviewer calibration, and reproducibility risks.

## Suggested Output Location

When running these prompts, keep outputs separate from the prompt package:

- `reports/deep_research_outputs/literature_positioning/`
- `reports/deep_research_outputs/method_evaluation/`

The prompts intentionally ask the researcher to preserve primary-source links
and to distinguish source-supported findings from interpretation.

## Boundaries

Do not use these prompts to modify product code, archive runtime code, browser
cache, model weights, downloaded images, or private archive state.

This repository is a reproducible research artifact for the paper framing and
methodology around hybrid answer lanes.
