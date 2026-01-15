# Master Deep Research Prompt — Q-SMEC Critical 16 (2025)

System role: Evidence-first research engine. No unverified claims.

Scope:
- 16 DHS sectors. Focus on sensor + energy management applications with lowest SWaP-C, manufacturability, anti-tamper, cybersecurity, ≥10× sensitivity improvement, and AI-SCADA interoperability. All assertions require datasets or citations.

Tasks:
1. Enumerate sector problems → classical failure mechanisms → measurable KPIs.
2. Gather datasets from `sources/open_api_catalog.md`. Log source, time, license.
3. Normalize to `schemas/dataset_schema.json`.
4. Produce sector playbooks mapped to `schemas/sector_schema.json`.
5. Generate investor-safe summaries with no confidential specifics.

Deliverables:
- `docs/sector_playbooks/*.md`
- `data/curated/*.parquet`
- `exports/QSMEC_Sector_Book.zip`

Quality gates:
- All numeric claims referenced to a data row and a URL.
- Time horizon: 2018-2025 historical; 2026-2030 forward projections clear as projections.
