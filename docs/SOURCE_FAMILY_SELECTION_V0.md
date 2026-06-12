# Source Family Selection V0

Generated: 2026-06-12

This document starts Paper v1 source-family selection for the
`source_audited_50` gate. It records why the first rows use Library of Congress
item-level metadata and what claims those rows can and cannot support.

## Selected First Family

`loc_metadata` is selected for the first batch because it provides:

- stable public item pages;
- item-level JSON metadata via `?fo=json`;
- title, date, repository, call number, reproduction number, and rights fields;
- metadata-visible image resource information without requiring image download;
- rights language that can be preserved verbatim in deterministic lanes.

The first batch uses Library of Congress Prints and Photographs Division WPA
public-health poster records. These records are suitable for source/rights,
provenance, explanation, and mixed-intent lane tests.

## Audit Boundary

The first batch is metadata-only:

- no image files are downloaded;
- no image contents are visually inspected;
- `rights_label` and `reuse_permission` preserve LOC source wording;
- `public_domain_status=not_explicitly_stated_by_source` means the source
  rights field does not explicitly assert public-domain status;
- `image_state_label=image_rights_unknown` avoids converting "No known
  restrictions on publication" into a stronger legal claim.

## First Batch Records

| Query | LOC item | Lane purpose |
|---|---|---|
| `q001` | `98516603` | Warmup source/rights deterministic rendering |
| `q002` | `98513455` | Source/rights exact field delivery |
| `q003` | `98508392` | Compound rights plus bounded public-health interpretation |
| `q004` | `98513584` | Bounded explanation with provenance |
| `q005` | `98518818` | Compound reuse caveat plus bounded interpretation |

## Expansion To 15 Rows

The first expansion keeps the same source family and adds ten more LOC
item-level metadata records:

| Query | LOC item | Lane purpose |
|---|---|---|
| `q006` | `98513524` | Source/rights exact field delivery |
| `q007` | `98516179` | Compound rights plus bounded title interpretation |
| `q008` | `98518824` | Source/rights plus metadata image-state delivery |
| `q009` | `98513398` | Bounded explanation with provenance |
| `q010` | `98508162` | Compound reuse caveat plus bounded interpretation |
| `q011` | `98508384` | More-context / research guidance |
| `q012` | `98513469` | Compound rights plus safety-message interpretation |
| `q013` | `98508416` | Bounded explanation with provenance |
| `q014` | `98507705` | Compound source/rights plus bounded interpretation |
| `q015` | `98510127` | Recommendation / research usefulness |

This expansion also treats `source_citation` and `image_state_label` as
contract-bearing deterministic fields when listed in a row's decisive fields.

## Structural Expansion To 26 Rows

The structural expansion keeps the 15 LOC metadata records and adds rows that
exercise fixture shapes needed before a Paper v1 run:

| Query range | Fixture shape | Purpose |
|---|---|---|
| `q016`-`q018` | 0-record no-evidence cases | Deterministic refusal when the evidence packet is missing |
| `q019`-`q020` | 1-record earliest/superlative cases | Refusal when a comparison corpus is unavailable |
| `q021`-`q023` | 2-record LOC comparison cases | Multi-record generative comparison over audited metadata |
| `q024`-`q026` | Wikimedia Commons metadata cases | Second source family for source/rights, mixed, and explanation lanes |

This expansion intentionally adds structural diversity before simply adding
more LOC source/rights successes. It does not complete the 50-query Paper v1
gate.

## Second Family: Wikimedia Commons Metadata

`wikimedia_commons_metadata` is selected as the second family because Wikimedia
Commons file metadata exposes title, date, source, author/credit, and license
metadata through public file pages and the official API. The current batch uses
metadata-only rows for WPA or public-health poster files:

| Query | Commons record | Lane purpose |
|---|---|---|
| `q024` | `commons_11160794` | Source/rights exact field delivery |
| `q025` | `commons_127390131` | Compound rights plus bounded public-health interpretation |
| `q026` | `commons_46307977` | Bounded explanation using Commons metadata |

For these rows:

- `rights_label` and `reuse_permission` preserve source-visible license terms;
- `public_domain_status` records only the metadata-level status;
- no media file is downloaded or visually inspected;
- `image_state_label` remains a metadata-derived label, not an image-content
  claim.

## Third Family: Museum Metadata

`museum_metadata` is introduced through official Metropolitan Museum of Art
Collection API records. These rows are useful because they are partial rather
than complete rights records:

- title, date, repository, and object URL are available;
- `isPublicDomain=false` is visible in the object metadata;
- `rightsAndReproduction` is empty for the selected records;
- no primary image URL is provided by the API for these selected records.

The fixture therefore marks Met rows as `source_audit_status=partial` and
records `rights_label` and `reuse_permission` as `missing`. This creates
controlled partial-evidence cases without inventing rights claims.

| Query range | Met object(s) | Lane purpose |
|---|---|---|
| `q027`-`q031` | `853621`, `916015`, `922252`, `922247`, `966971` | Partial source/rights, mixed, and explanation rows |
| `q032`-`q034` | Reused Met records | Comparison and recommendation rows where rights fields are not decisive |
| `q038`, `q040`, `q043`, `q045`, `q048`, `q050` | Reused Met records | Earliest refusal, cross-source comparison, partial mixed, and source/rights rows |

This family also required a consistency-checker correction: a partial
source-audit record may support a query-level `sufficient` evidence state when
the missing fields are not decisive for that query.

## Completion Of The 50-Query Gate

The current `source_audited_50` gate contains:

- 50 query rows;
- 23 source-audit manifest records;
- 3 source families (`loc_metadata`, `wikimedia_commons_metadata`,
  `museum_metadata`);
- 32 sufficient-evidence rows;
- 10 missing-evidence deterministic-refusal rows;
- 8 partial-evidence rows.

This completes the first mechanically valid 50-query source-audited fixture
gate. It does not yet create a paper-facing Qwen/WebLLM result.

## Next Families To Consider

The next source-family candidates should diversify beyond LOC:

- DPLA provider metadata for aggregator/source-provenance ambiguity;
- Europeana metadata if rights fields are consistently accessible without
  requiring image download.

These should be added only after their metadata fields can pass the same
manifest, query-plan, compiler, and consistency checks.
