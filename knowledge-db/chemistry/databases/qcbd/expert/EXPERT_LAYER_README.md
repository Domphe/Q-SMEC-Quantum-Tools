# Expert Layer Overview

Purpose: Provide a robust, queryable quantum chemistry & physics knowledge layer with ontology extensions, reasoning metrics, semantic search, provenance-aware ingestion, and evolution tracking.

## Components

1. Ontology Extensions: Chemistry (Hamiltonians, BasisSets, Approximations, Interactions, ExperimentalTechniques, MaterialSystems) + Physics (ManyBodyMethods, QFTApproaches, SolidStateModels, SpectroscopyLines).
2. Graph Loader: `load_expert_graph.load_graph()` merges base + extensions with inline fallback for reliability.
3. Reasoning Metrics: `reasoning.ranked_methods()` composite score (efficiency + scaling heuristic).
4. Query API: `query_api.rank_methods()`, `filter_methods()`, `suggest()` safe querying.
5. Context Builder: `context_builder.build_context(query)` returns concept + method pack.
6. Semantic Search: `semantic_search.search_methods(query)` deterministic hash embeddings (64-D) for similarity.
7. Ingestion Pipeline: `ingestion_pipeline.ingest_all()` modular fetch/parse/extract/citation/quality/persist with compliance safeguards.
8. Citations & Quality: `citations.normalize_record()` and `quality.score()` utilities for provenance and confidence.
9. Versioning: `versioning.create_snapshot()` + `versioning.diff_snapshots(a,b)` track evolution.
10. Gap Analysis: `gap_analysis.analyze()` surfaces missing ontology sections & metadata gaps.
11. CLI: `python -m expert.expert_cli <command>` operational interface.

## CLI Commands

`rank` composite method ranking
`semantic <query>` hash-embedding similarity search
`context <query>` build LLM-ready pack
`suggest <goal>` goal-text heuristic suggestions
`snapshot [--name tag]` write timestamped graph snapshot
`gap` run ontology & metadata gap analysis

## Compliance & Ethics

No verbatim copyrighted bodies ingested. Only metadata, structured facts, equations (symbolic), short factual summaries. See `expert/compliance.md`.

## Extensibility

Replace hash embeddings with real vector models (e.g., local sentence transformer) by swapping `_embed` implementation. Integrate CrossRef / DOI resolution inside `citations.py`. Expand quality signals with reproducibility, benchmark coverage.

## Quick Examples (PowerShell)

```powershell
python -m expert.expert_cli rank --limit 5
python -m expert.expert_cli semantic "coupled cluster"
python -m expert.expert_cli context "electron correlation"
python -m expert.expert_cli snapshot --name initial
python -m expert.expert_cli gap
```

## Tests

`tests/test_expert_layer.py` core functionality; additional semantic search and versioning tests can be added.

## Roadmap

- Replace placeholder extraction with NLP pipeline.
- Add embeddings for Concepts & Tools.
- Provenance scoring with cross-source consistency.
