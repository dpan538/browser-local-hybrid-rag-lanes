# Lane Decision Flow

Generated: 2026-06-09

This document gives the reviewer-facing flowchart for the first hybrid
answer-lane method.

## Flow

```mermaid
flowchart TD
  A["User query + retrieved evidence packet"] --> B["Fixture intent label + field-state checklist"]
  B --> C["Static rule table: lane_rules_v1.yaml"]
  C --> D{"Rule matched?"}
  D -- "No" --> E["Default generative answer"]
  E --> F["Log routing_undefined"]
  D -- "Yes" --> G{"Execution mode"}
  G -- "deterministic_render" --> H["Render exact fields with placeholders for missing fields"]
  G -- "deterministic_refusal" --> I["Render refusal template linked to evidence state"]
  G -- "generative_answer" --> J["Call local model for bounded answer"]
  G -- "compound_answer" --> K["Render deterministic fields + call local model for bounded research guidance"]
  H --> L["Measure hybrid_system_latency"]
  I --> L
  J --> M["Measure qwen_generation_latency + hybrid_system_latency"]
  K --> M
  F --> M
  L --> N["Contract + usability review"]
  M --> N
```

## Interpretive Rule

The flowchart is not a learned router. It is a static experimental policy.
Changing the rule table changes the experimental condition.

## Counterfactual Baseline

An all-deterministic baseline is not the primary comparison because some lanes
require explanatory synthesis, comparison, and research guidance. This boundary
is the point of the paper: deterministic rendering is appropriate for exact
contract-bearing evidence, while generation remains appropriate for synthesis.

The primary baseline is all-generation. The primary hybrid comparisons are:

- hybrid without deterministic refusal;
- full hybrid with deterministic refusal;
- compound answers for mixed-intent rows.
