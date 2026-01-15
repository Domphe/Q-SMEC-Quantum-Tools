# Compliance & Ethical Ingestion

This expert layer:
- Stores only metadata, structured facts, and derived metrics.
- Avoids verbatim copying of copyrighted narrative text.
- Uses public domain / permissively licensed government data directly (values + citation).
- Journal / textbook content: only bibliographic metadata + high-level structured summaries added manually.
- Preprints: metadata + factual extraction within fair scholarly use.
- Equations: encoded as symbolic patterns without full derivation text.
- Quality scores are heuristic and non-defamatory; they assess suitability, not value judgments.

If removal / correction is requested for any source, a tombstone record will replace the entry and snapshots will keep provenance.


## Allowed

- Public domain datasets (NIST constants) and standards metadata (IUPAC identifiers, CODATA values)
- DOI bibliographic metadata (title, authors, year, journal, volume, pages)
- Short algorithmically derived factual summaries (not verbatim)
- Symbolic equation patterns (e.g. `H =`, `∇^2`) without full textbook exposition

## Avoided

- Paragraph-level verbatim text from copyrighted sources
- Full magazine feature text reproduction
- Proprietary internal documents
- Supplemental data with redistribution restrictions

## Derivation Rules

1. Keyword heuristic extracts only minimal context; prefer abstraction.
2. No direct copying beyond brief factual phrases (< 10 words, non-expressive).
3. Citation keys hashed from source id for traceability.
4. If `extraction_allowed=false`, skip content parsing; retain metadata only.

## Update & Takedown

Maintain snapshot history; on takedown mark record with `{ "tombstone": true, "reason": "request" }`.

### Last Updated

2025-12-01
