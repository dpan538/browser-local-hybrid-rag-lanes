# Journal Target Strategy

Generated: 2026-06-12

This document supersedes the earlier Information Research first-target plan
and the later OIR/AJIM stretch-target plan. The active strategy prioritizes
successful publication in a strong information science venue while still
keeping a high-standard experimental path.

Primary sources checked on 2026-06-12:

- Journal of Information Science: https://journals.sagepub.com/home/jis
- The Electronic Library: https://www.emeraldgrouppublishing.com/journal/el
- Open Information Science: https://www.degruyterbrill.com/journal/key/opis/html
- Digital Library Perspectives: https://www.emeraldgrouppublishing.com/journal/dlp
- Online Information Review: https://www.emeraldgrouppublishing.com/journal/oir
- Aslib Journal of Information Management: https://www.emeraldgrouppublishing.com/journal/ajim
- Information Research submissions: https://informationr.net/infres/about/submissions
- Information Research archive: https://informationr.net/infres/issue/archive

## Target Ladder

| Tier | Venue | Role | Risk |
|---|---|---|---|
| Primary | Journal of Information Science | First target | Strong but more controllable than OIR/AJIM |
| Backup | The Electronic Library | Second target | Good fit for information organisation and digital-library systems |
| Safer | Open Information Science | Broad OA fallback | APC and lower selectivity; useful if higher targets fail |
| Safer/domain | Digital Library Perspectives | Digital-library/archive fallback | Best if final framing becomes archive/digital-library specific |
| Stretch | Online Information Review | High-end target | Requires stronger socio-technical theory and larger empirical package |
| Stretch | Aslib Journal of Information Management | High-end target | Requires stronger information management/governance contribution |

Information Research is removed from the active target ladder because the
official submission page currently says the journal is not accepting
submissions, and the current archive page reports no published issues in the
new OJS instance.

## First Target: Journal of Information Science

Journal of Information Science is the active primary target because it is a
peer-reviewed international information science journal, remains active, and
fits a method paper about information-system allocation.

Official indicators checked on 2026-06-12:

- 2024 Impact Factor: 1.7.
- 5-year Impact Factor: 2.3.
- 2026 OnlineFirst articles are present on the journal page.

JIS framing:

```text
Browser-local RAG is not only a generation problem. It is an
information-system allocation problem: when should an answer be generated,
rendered from evidence, or refused?
```

Use these concepts:

- information science method;
- information-system allocation;
- evidence-bounded AI assistance;
- answer mode;
- source and rights clarity;
- refusal boundary;
- evidence-to-output fidelity;
- bounded generative synthesis.

Preferred core claim:

```text
Hybrid answer-lane allocation reduces specific contract failures and
under-refusal in a controlled browser-local RAG setting, while preserving
bounded generative synthesis for tasks that require explanation or comparison.
```

Avoid claiming:

```text
Hybrid lanes solve hallucination in browser-local RAG.
```

## Second Target: The Electronic Library

The Electronic Library is the second target if the paper becomes more strongly
about information organisation, answer organisation, or digital-library
systems.

Official indicators checked on 2026-06-12:

- 2024 Impact Factor: 1.5.
- 5-year Impact Factor: 1.7.
- Time to first decision: 32 days.
- Acceptance rate: 14.6%.

TEL framing:

```text
Hybrid answer lanes as an answer-organisation method for AI-mediated
information access.
```

TEL is a strong backup if the manuscript emphasizes:

- information organisation;
- answer organisation;
- digital-library systems;
- source, rights, and provenance display;
- rigorous methodology with more than local interest.

## Safer Backup Targets

### Open Information Science

Keep as a broad OA fallback.

Official page checked on 2026-06-12:

- Active volumes listed through 2026.
- 2024 CiteScore: 2.6.
- Scope is broad across information science, libraries, archives, digital
  libraries, cultural heritage, information technology, and research methods.

Use when the goal becomes getting a sound artifact/method paper published
rather than maximizing venue rank.

### Digital Library Perspectives

Use if the final paper becomes most naturally a digital-library/archive
application.

Official scope includes digital libraries, digital heritage, metadata, digital
humanities, usability, human-computer interaction, and digital libraries as
socio-technical systems.

## Stretch Targets

### Online Information Review

Online Information Review should be treated as a stretch target, not a safe
Q2/Q3 outlet.

Official indicators checked on 2026-06-12:

- 2025 CiteScore: 8.4.
- 2024 Impact Factor: 3.5.
- 5-year Impact Factor: 3.7.
- Acceptance rate: 9.9%.

OIR framing:

```text
Browser-local AI assistance is a socio-technical information practice. The
system must decide when to generate, when to render evidence, and when to
refuse.
```

Use these concepts:

- digital information practice;
- AI-mediated information access;
- trust calibration;
- evidence boundary;
- refusal behavior;
- platform/runtime mediation;
- source and rights transparency;
- socio-technical information systems.

### Aslib Journal of Information Management

AJIM is also a stretch target, not a fallback guarantee.

Official indicators checked on 2026-06-12:

- 2024 Impact Factor: 3.1.
- 5-year Impact Factor: 3.0.
- Acceptance rate: 8.7%.

AJIM framing:

```text
Hybrid answer lanes as information governance for AI-mediated evidence use.
```

Use these concepts:

- information management;
- information governance;
- evidence fidelity;
- data reuse;
- rights metadata;
- digital repositories;
- information/data retrieval;
- accountability;
- source/provenance preservation;
- rule-table auditability.

## Submission Route

1. Submit to Journal of Information Science if the manuscript is a clear
   information science method paper with source-audited evidence, frozen
   protocol, paired analysis, and blinded semantic review.
2. If JIS rejects for fit, revise toward information/answer organisation and
   submit to The Electronic Library.
3. If TEL is not suitable, choose:
   - Open Information Science for broad OA fallback;
   - Digital Library Perspectives if the final contribution is
     digital-library/archive specific.
4. Use OIR or AJIM only if the evidence package grows strong enough for a
   stretch attempt and the manuscript can carry the needed socio-technical or
   information-governance argument.

## Minimum JIS Evidence Standard

Do not target JIS with only the current 50-query synthetic or 100-query
calibration package.

Minimum paper-facing target:

```text
200 source-audited queries
3 conditions per query
600 outputs total
frozen protocol manifest
clean Qwen/WebLLM browser-local run
automatic contract metrics on all outputs
two-rater blinded semantic review on 60 sampled queries x 3 outputs = 180 rows
paired analysis by query
```

Preferred stronger version:

```text
300 source-audited queries
900 outputs total
human review on 80-100 sampled queries x 3 outputs = 240-300 rows
```

The 300-query version should be treated as a stronger JIS version, a revision
reserve, or the evidence threshold for OIR/AJIM stretch submission.
