# Smart Water Research Agent (Deep-Tech, Database-Ready)

This repo is a **research+ETL scaffold** that continuously ingests authoritative sources about the *Smart Water eHandbook* case studies and their vendor stacks, normalizes them into a **granular knowledge schema**, and updates:
- a relational store (Postgres/SQLite)
- a document store (JSONL)
- a graph view (optional export)
- a vector index (optional)

It is designed to be opened in **VS Code** and run locally.

## What it covers (v1)
Case studies & vendors pulled from WaterWorld’s *Smart Water* eHandbook summary page (Nov 24, 2025):
- Frisco, TX AMR→AMI overlay using **Neptune R900** endpoints + collectors (9 zones), 15-minute intervals
- Dublin trunk mains inspection using **Aganova Nautilus** sphere with **SUEZ**, **Microsoft**, **Uisce Éireann**
- Walla Walla, WA smart DMAs using PRV instrumentation + **FlexNet** telemetry
- Mobile workforce rugged devices (field ops)
- Partnerships + digital twins (Bentley Systems referenced)

Sponsors and associated vendors:
- **Tadiran Batteries**
- **KROHNE Inc.** (listed on the Aug 4, 2025 version of the eHandbook page)

## Quickstart
1) Create a venv
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) Copy environment template
```bash
cp .env.example .env
```

3) Run one-shot ingestion (SQLite by default)
```bash
python -m agent.ingest --once
```

4) Run continuous mode (polling)
```bash
python -m agent.ingest --loop --minutes 180
```

## Storage backends
- Default: SQLite (file: `data/agent.db`)
- Optional: Postgres (set `DB_URL`)

## Safety & compliance
This project uses a **polite fetcher** with:
- rate limiting
- caching
- user agent identification
- respect for `robots.txt` (configurable)

You are responsible for ensuring source terms allow automated access.

## Outputs
- `data/raw/` : fetched html/pdf (by URL hash)
- `data/normalized/` : normalized JSONL entities/events
- `data/agent.db` : SQLite knowledge base

## Next extensions
- Add a vector store (Chroma/FAISS) for semantic retrieval
- Add EPANET/WNTR simulation adapters for hydraulic model calibration
- Add model registry hooks for “QuantumAI/DBs/Models/Simulations” integration
