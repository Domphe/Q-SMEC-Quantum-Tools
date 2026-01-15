
# AI R&D Research Stack — PRO

## What you get
- `database.db` — SQLite with R&D entities, compliance, funding, supply chain, TRL/MRL, tasks.
- Python package `ai_rnd/` — CLI + modules for:
  - Auto-installing prerequisites
  - Source trust & recency verification (Gov/Official/Open-source)
  - URL ingestion with artifact logging
- `requirements.txt` — dependencies
- `scripts/install.sh` — one-liner setup

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m ai_rnd.runner setup
python -m ai_rnd.runner seed
python -m ai_rnd.runner ingest-url "https://www.nato.int/" --project 1 --recency-days 730
```

## Policies
- Trust priority: Government > Official standards > Curated Open-source.
- Freshness: default requires updates within ~2 years (configurable).
- Interactions logged into `interaction` table.
- Export-controlled items must pass `approval_gate` before export.
