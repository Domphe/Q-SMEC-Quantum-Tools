# Master_DB (Drone + Laser Knowledge Graph)

This folder contains CSVs and scripts to manage a cross-domain knowledge graph for the Drone (20 kW motor) and Laser (monochromatic VUV/hard X-ray) programs.

## Contents

- `master_nodes.csv` — entities (systems, components, orgs, phases, export control, etc.)
- `master_edges.csv` — relationships between entities
- `enums_readme.md` — controlled vocabularies for `node_type`, `relation_type`, etc.
- `mapping_notes.md` — guidance for linking to files in `../Drone` and `../Laser`
- `scripts/ingest_to_neo4j.py` — loader for Neo4j using the CSVs
- `.env.example` — template for Neo4j connection settings

## Quickstart (Neo4j)

1. Install dependencies in your preferred Python env:

```powershell
pip install neo4j python-dotenv
```

1. Provide Neo4j credentials (choose one):

- Option A: Copy `.env.example` to `.env` and edit values.
- Option B: Set env vars in the shell for this session.

```powershell
$env:NEO4J_URI = "bolt://localhost:7687"
$env:NEO4J_USER = "neo4j"
$env:NEO4J_PASSWORD = "<your_password>"
```

Verify variables are visible:

```powershell
echo $env:NEO4J_URI; echo $env:NEO4J_USER
```

1. Run ingestion:

```powershell
python "G:\\My Drive\\.0 Q-SMEC Clients\\Nikolay - Drone - Laser\\Master_DB\\scripts\\ingest_to_neo4j.py"
```

If you see a connection error, confirm Neo4j is running and the Bolt port and credentials are correct.

This will create nodes (`:Node` plus labels by `node_type` and `domain`) and edges with relationship type labels (also preserved on the relationship as a label for convenient filtering).

## Conventions

- Use `spec_json` to store structured fields and file path hints (relative to `../Drone` or `../Laser`).
- Use `primary_source` to capture provenance (e.g., `Nikolay_Email_2025-11-25`).
- Update `status` from `draft` to `validated` after review.

## Next steps

- Expand node/edge rows to include components, materials, subsystems, and test artifacts.
- Integrate search (e.g., OpenSearch/Elasticsearch) for full-text across PDFs in `../Drone` and `../Laser`.
- Add a validation script to check controlled enums and CSV integrity before ingestion.
