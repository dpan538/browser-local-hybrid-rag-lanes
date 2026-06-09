# Promotion Gate V0

- Mode: `exploratory`
- Decision: `PASS`
- Rows: 50
- Unique query IDs: 50
- Unique query texts: 50

## Failures

- None.

## Warnings

- 53 synthetic records: exploratory promotion must frame the fixture as synthetic.
- 53 records are not source-audited: evidence correctness claims remain blocked.
- 11 no-record rows are present and treated as missing-evidence refusal tests.

## Record Origin Counts

| Value | Count |
|---|---:|
| `no_records` | 11 |
| `synthetic` | 53 |

## Source Audit Counts

| Value | Count |
|---|---:|
| `no_records` | 11 |
| `not_audited` | 53 |

## Interpretation

Exploratory mode may pass with synthetic records if the study claims are
limited to evidence-to-output fidelity, refusal behavior, latency plumbing,
and usability workflow rehearsal. Paper mode requires source-audited or
derived-public-source evidence before making evidence-correctness claims.
