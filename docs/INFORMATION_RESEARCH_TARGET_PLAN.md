# Superseded Information Research Target Plan

Generated: 2026-06-12

This document is retained as historical planning context only. It has been
superseded by `docs/JOURNAL_TARGET_STRATEGY.md`.

Information Research is no longer the first target because the official
submissions page currently says the journal is not accepting submissions, and
the current OJS archive page reports no published issues in that instance.

Primary source links:

- Information Research submissions: https://informationr.net/infres/about/submissions
- Information Research about/scope: https://informationr.net/infres/about

## Venue Status

Information Research is no longer an active target. Its user-oriented style
remains useful background, but submission planning should follow
`docs/JOURNAL_TARGET_STRATEGY.md`.

Current official submission-page status checked on 2026-06-12:

```text
This journal is not accepting submissions at this time.
```

Active target planning has moved to:

```text
Online Information Review -> Aslib Journal of Information Management ->
Journal of Information Science / The Electronic Library ->
Open Information Science / Digital Library Perspectives
```

## Fit

The paper should be written as an information-system and information-user
study, not as a retrieval algorithm paper.

Information Research's official scope emphasizes work oriented toward the
human information seeker and user, including:

- cultural heritage;
- digital humanities;
- archives and records management;
- digital curation;
- human-computer interaction;
- usability and user experience;
- information systems;
- AI and machine learning;
- information retrieval and search;
- digital libraries;
- information policy, security, and privacy.

This fits the project only if the framing stays close to user-visible answer
boundaries:

> In browser-local small-model RAG, how should user-visible answers be
> allocated between deterministic evidence/refusal lanes and generative
> synthesis lanes, so unsupported outputs and unnecessary model calls are
> reduced while answer boundaries remain understandable to information users?

## Writing Frame

Prefer:

- answer mode;
- evidence field;
- refusal boundary;
- source and rights clarity;
- user-visible answer;
- information-system design;
- browser-local information assistance.

Use sparingly or define clearly:

- WebLLM;
- WebGPU;
- MLC;
- prompt pack;
- contract checker;
- quantization.

Technical details belong in the method section or appendix, not in the title or
main contribution language.

## Working Title

Preferred:

```text
What should not be generated? Hybrid answer lanes for browser-local information assistance
```

Alternative:

```text
Hybrid answer lanes for browser-local retrieval-augmented assistance:
deterministic evidence, refusal, and bounded generation
```

Avoid titles that foreground runtime implementation details such as Qwen,
WebLLM, WebGPU, MLC, or quantization.

## Article Shape

Target article type:

```text
Information Research exploratory article
```

Target scale:

```text
source-audited 100 queries
3 conditions
300 query-condition outputs
40 sampled queries x 3 outputs = 120 blinded human-review rows
```

Main claim target:

```text
Full hybrid answer lanes reduce refusal-alignment failures and unnecessary
generation while preserving user-visible usefulness within a controlled
information-assistance fixture.
```

This claim requires a source-audited or public-derived fixture and blinded
semantic review. The current synthetic 50-query run does not yet support it.

## Backup Venues

Keep backup targets open until Information Research submissions reopen:

- JCDL short/poster/workshop: best for cultural-heritage and digital-library
  framing.
- Aslib Journal of Information Management: possible later target if the
  source-audited fixture and review package are stronger.
- A digital-libraries or information-systems workshop: appropriate if the
  project remains a method and artifact note.

## Style Constraints

Information Research-oriented writing should:

- use British English;
- avoid unnecessary jargon;
- explain the user-facing problem before the model runtime;
- use a structured abstract;
- prepare for double-blind review;
- avoid unsupported generalization beyond the fixture;
- explain that the study is a lightweight semantic audit, not a user study.
