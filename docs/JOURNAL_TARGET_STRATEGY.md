# Journal Target Strategy

Generated: 2026-06-12

This document supersedes the earlier Information Research first-target plan.
Information Research remains useful as a historical style reference, but it is
not the first submission target because its current submission page is closed
and the active archive state is uncertain.

Primary sources checked on 2026-06-12:

- Online Information Review: https://www.emeraldgrouppublishing.com/journal/oir
- Aslib Journal of Information Management: https://www.emeraldgrouppublishing.com/journal/ajim
- Journal of Information Science: https://journals.sagepub.com/home/jis
- The Electronic Library: https://www.emeraldgrouppublishing.com/journal/el
- Open Information Science: https://www.degruyterbrill.com/journal/key/opis/html
- Digital Library Perspectives: https://www.emeraldgrouppublishing.com/journal/dlp
- Information Research submissions: https://informationr.net/infres/about/submissions
- Information Research archive: https://informationr.net/infres/issue/archive

## Target Ladder

| Tier | Venue | Role | Risk |
|---|---|---|---|
| Stretch | Online Information Review | First target | High competition; requires socio-technical framing and strong empirical package |
| Stretch | Aslib Journal of Information Management | Second target | Also high competition; requires information management/governance framing |
| Realistic | Journal of Information Science | Backup if theory/method remains information-science strong | Still selective |
| Realistic | The Electronic Library | Backup if contribution is strongest as information organisation/system method | Needs clear non-local contribution |
| Safer | Open Information Science | Broad OA fallback | APC and lower selectivity; useful if higher targets fail |
| Safer/domain | Digital Library Perspectives | Backup if final framing becomes digital-library/archive specific | Best for digital library application angle |

Information Research is removed from the active target ladder because the
official submission page currently says the journal is not accepting
submissions, and the current archive page reports no published issues in the
new OJS instance.

## First Target: Online Information Review

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

Avoid presenting the paper as only:

```text
We ran a 300-query RAG ablation.
```

Preferred core claim:

```text
Browser-local RAG should not be evaluated only as a generation problem. It is
also an answer-allocation problem: systems must decide which parts of an answer
should be generated, which should be rendered from evidence, and which should
be refused.
```

## Second Target: Aslib Journal of Information Management

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

AJIM is stronger if the paper emphasizes contract-bearing evidence fields,
source/rights/provenance preservation, and the separation of evidence
correctness from evidence-to-output fidelity.

## Backup Targets

### Journal of Information Science

Use if the manuscript remains a general information-science method paper.

Official page checked on 2026-06-12:

- Impact Factor: 1.7.
- 5-year Impact Factor: 2.3.

Suggested framing:

```text
Answer-lane allocation as an information science method for evidence-bounded
AI assistance.
```

### The Electronic Library

Use if the contribution is strongest as information organisation or answer
organisation.

Official scope language emphasizes well thought-out problems in information
organisation, rigorous methodology, more than local interest, and new
knowledge for the readership.

Suggested framing:

```text
Hybrid answer lanes as an answer-organisation method for AI-mediated
information access.
```

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

## Submission Route

1. Submit to OIR if the final manuscript has a strong socio-technical argument,
   source-audited 300-query evidence, and two-rater blinded semantic review.
2. If OIR rejects for theory/framing fit, revise toward information
   management/governance and submit to AJIM.
3. If AJIM is not suitable, choose:
   - Journal of Information Science if the theory/method remains broad;
   - The Electronic Library if the system/method is strongest as information
     organisation;
   - Open Information Science for broad OA fallback;
   - Digital Library Perspectives if the final contribution is
     digital-library/archive specific.

## Minimum OIR/AJIM Evidence Standard

Do not target OIR or AJIM with a 100-query exploratory package.

Minimum target:

```text
300 source-audited queries
3 conditions per query
900 outputs total
frozen protocol manifest
clean Qwen/WebLLM browser-local run
automatic contract metrics on all outputs
two-rater blinded semantic review on 240-300 sampled outputs
clear socio-technical or information-governance framing
```

Human review should be stratified, not exhaustive:

```text
80-100 sampled queries x 3 condition outputs = 240-300 blinded rows
```

Review all automatic contract-failure and anomaly rows. Do not require
reviewers to score all 900 outputs unless a future protocol gives a specific
reason.
