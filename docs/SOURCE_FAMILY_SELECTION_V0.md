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

## Next Families To Consider

The next source-family candidates should diversify beyond LOC:

- Wikimedia Commons metadata for explicit license fields;
- DPLA provider metadata for aggregator/source-provenance ambiguity;
- museum metadata where rights fields are present but reuse terms differ;
- Europeana metadata if rights fields are consistently accessible without
  requiring image download.

These should be added only after their metadata fields can pass the same
manifest, query-plan, compiler, and consistency checks.
