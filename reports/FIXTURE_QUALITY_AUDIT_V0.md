# Fixture Quality Audit V0

This report audits the compiled draft fixture before promotion. It is
descriptive and intentionally conservative: findings here do not mean the
fixture is invalid, only that it is not yet ready for paper-facing use.

## Summary

- Rows: 50
- Unique query texts: 50
- Duplicate query text groups: 0

## Promotion Blockers

- 53 records are synthetic; promotion needs explicit reporting language.
- 53 records are not source-audited; evidence correctness claims are blocked.
- 11 rows have no records: q009, q010, q011, q012, q013, q014, q015, q017, q019, q043, q047.

## Role Counts

| Value | Count |
|---|---:|
| `dev` | 15 |
| `eval` | 35 |

## Stratum Counts

| Value | Count |
|---|---:|
| `comparison` | 6 |
| `explanation` | 5 |
| `first_earliest_refusal` | 5 |
| `mixed_intent` | 10 |
| `more_context` | 5 |
| `no_evidence_refusal` | 6 |
| `recommendation` | 5 |
| `source_rights` | 8 |

## Evidence State Counts

| Value | Count |
|---|---:|
| `contradictory` | 2 |
| `missing` | 11 |
| `not_applicable` | 1 |
| `partial` | 18 |
| `sufficient` | 18 |

## Refusal Expected Counts

| Value | Count |
|---|---:|
| `False` | 35 |
| `True` | 15 |

## Conflict Expected Counts

| Value | Count |
|---|---:|
| `False` | 48 |
| `True` | 2 |

## Record Origin Counts

| Value | Count |
|---|---:|
| `synthetic` | 53 |

## Source Audit Counts

| Value | Count |
|---|---:|
| `no_records` | 11 |
| `not_audited` | 53 |

## Duplicate Query Text

- No repeated query text.

## Recommended Next Edits

1. Keep synthetic/source-audit limitations explicit in the paper and evaluation metadata.
2. Review no-record refusal rows to ensure they are intentional missing-evidence tests.
3. Do not promote the draft fixture until source-audit and no-record limitations are accepted or revised.
