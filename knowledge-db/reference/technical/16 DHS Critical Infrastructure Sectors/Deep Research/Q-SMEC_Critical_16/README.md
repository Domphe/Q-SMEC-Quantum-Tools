# Q-SMEC_Critical_16

Operational package to research, validate, and package **National Security–critical sensor and energy management applications** across the **16 DHS Critical Infrastructure Sectors**. Includes reproducible prompts, schemas, data-gathering scripts, and export utilities.

## Objectives
- Gather trusted 2025-current data from official APIs and open sources.
- Normalize to strict schemas and validate with rule sets.
- Produce sector playbooks and investor-ready artifacts without speculative claims.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # win: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # fill keys
python scripts/generate_sector_templates.py
python scripts/gather_openapis.py
python scripts/fetch_gov_data.py
python scripts/clean_normalize.py
python scripts/validate_schema.py
python scripts/build_indexes.py
python scripts/export_packages.py
