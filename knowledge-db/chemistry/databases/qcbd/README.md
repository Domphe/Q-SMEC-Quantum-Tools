# Quantum Chemistry Knowledge Base Database (QCBD)

**Version:** 1.0.0  
**Date:** December 1, 2025  
**Maintainer:** Q-SMEC Development Team

---

## Overview

QCBD is a production-grade, AI-queryable quantum chemistry knowledge base combining:

- **Comprehensive QC Theory:** 100+ concepts covering Hartree-Fock, DFT, coupled cluster, multireference methods
- **Software Ecosystem:** 15+ tools (Gaussian, ORCA, Psi4, PySCF, CP2K, xTB, etc.) with version tracking
- **Curated Benchmarks:** S22, S66, GMTKN55, G2/97, HEAT298 with reference data
- **Production Workflows:** 20+ validated computational protocols
- **AI Integration:** RAG pipeline, semantic search, LangChain orchestration
- **Enterprise Security:** RBAC, encryption, audit logging, client extensions

---

## Quick Start

### 1. Environment Setup

```powershell
# Navigate to QuantumAI environment
cd "G:\My Drive\envs\QuantumAI"

# Run setup script
.\setup_qc_environment.ps1
```

This will:
- Activate Python virtual environment
- Install all dependencies (PySCF, ASE, Neo4j, LangChain, etc.)
- Start Docker containers (Neo4j + Redis)
- Set environment variables
- Test imports

### 2. Build Knowledge Graph

```powershell
# Build unified knowledge graph from JSON files
python scripts/build_knowledge_graph.py

# Sync to Neo4j graph database
python scripts/sync_to_neo4j.py
```

### 3. Access the Knowledge Base

**Python API:**
```python
from api.secure_kb_loader import SecureKBLoader
from pathlib import Path

# Load knowledge base
loader = SecureKBLoader(
    Path(r"G:\My Drive\Databases\QCBD"),
    user_id="your_user_id"
)
kb = loader.get_merged_kb()

# Query entities
concepts = kb['Concepts']
methods = kb['Methods']
```

**Neo4j Browser:**
- Open: http://localhost:7474
- Username: `neo4j`
- Password: `qcdb_password_2025`

**Cypher Query Examples:**
```cypher
// Find all methods based on DFT
MATCH (c:Concept {name: "Density Functional Theory"})<-[:BASED_ON]-(m:Method)
RETURN m.name, m.scaling

// Find workflows using ORCA
MATCH (t:SoftwareTool {name: "ORCA"})<-[:USED_IN]-(w:Workflow)
RETURN w.name, w.goal

// Get methods validated on S22
MATCH (m:Method)-[:VALIDATED_ON]->(b:BenchmarkSet {name: "S22 Set"})
RETURN m.name
```

---

## Architecture

### Directory Structure

```
QCBD/
├── api/                          # Python API modules
│   ├── qcdb_embeddings.py       # Embedding system with caching
│   ├── secure_kb_loader.py      # RBAC + encryption
│   ├── extension_validator.py   # Client extension validation
│   └── unified_qc_api.py        # Unified query interface
│
├── scripts/                      # Build & maintenance scripts
│   ├── build_knowledge_graph.py # Merge JSON → unified KB
│   ├── sync_to_neo4j.py         # Sync to graph database
│   └── neo4j_backup.ps1         # Automated backups
│
├── benchmarks/                   # Curated benchmark data
│   ├── benchmark_registry.json  # Metadata catalog
│   ├── BENCHMARK_ATTRIBUTION.md # Citations & licenses
│   ├── s22/                     # S22 dataset
│   ├── s66/                     # S66 dataset
│   └── gmtkn55/                 # GMTKN55 dataset
│
├── embeddings/                   # Embedding models & training
│   ├── fine_tuning/             # QC corpus fine-tuning scripts
│   └── models/                  # Trained embedding models
│
├── embeddings_cache/             # Content-addressed embedding cache
│
├── tests/                        # Comprehensive test suite
│   ├── test_kb_integrity.py
│   ├── test_neo4j_ops.py
│   ├── test_api_comprehensive.py
│   └── run_all_tests.ps1
│
├── docs/                         # Documentation
│   ├── methods/                 # Method documentation
│   ├── software/                # Software guides
│   ├── workflows/               # Workflow protocols
│   └── tutorials/               # End-to-end tutorials
│
├── exports/                      # Multi-format exports
│   └── excel/                   # Excel workbooks
│
├── QCBD_client_extensions/      # Client-specific extensions
│   ├── template/                # Extension template
│   └── {client_name}/           # Per-client directories
│
├── access_control/              # RBAC configuration
│   └── roles.json               # Role definitions
│
├── schemas/                     # JSON schemas
│   └── client_extension_schema.json
│
├── evaluation/                  # Agent evaluation
│   ├── ground_truth_qa.json    # Test question-answer pairs
│   └── evaluate_agent.py       # Metrics computation
│
├── neo4j_data/                  # Neo4j database files
├── neo4j_backups/               # Automated backups (30-day retention)
│
├── qc_knowledge_graph_full.json # Unified knowledge graph
├── docker-compose.yml           # Neo4j + Redis containers
└── README.md                    # This file
```

### Technology Stack

**Databases:**
- Neo4j 5.14 (graph database)
- SQLite (cost tracking, audit logs)
- Redis (query caching)
- ChromaDB (vector store)

**Python Packages:**
- `pyscf`, `ase`, `cclib` (quantum chemistry)
- `neo4j`, `chromadb`, `redis` (databases)
- `sentence-transformers`, `openai` (embeddings)
- `langchain` (AI orchestration)
- `fastapi`, `uvicorn` (API server)

**AI/ML:**
- OpenAI `text-embedding-3-large` (cloud embeddings)
- `all-mpnet-base-v2` (local embeddings)
- LangChain (RAG pipeline)

---

## Features

### 1. Unified Knowledge Graph

- **8 Entity Types:** Concepts, Methods, SoftwareTools, Parameters, Workflows, ExampleProblems, BenchmarkSets, Resources
- **Bidirectional Cross-References:** Navigate between related entities
- **Version Tracking:** Software version compatibility tracking
- **Failure Diagnostics:** Structured troubleshooting guides

### 2. Dual Embedding System

- **Cost-Optimized:** Automatic fallback from OpenAI to local model
- **Intelligent Caching:** Content-addressed cache with SHA256 hashing
- **Budget Monitoring:** Monthly cost tracking with alerts
- **Fine-Tuned Models:** Domain-specific QC corpus training

### 3. Security & Access Control

- **Role-Based Access Control (RBAC):** Admin, Developer, Client User, Public User
- **AES-256 Encryption:** For confidential client extensions
- **Audit Logging:** All access events logged to SQLite
- **Client Isolation:** Namespace-based ID collision prevention

### 4. Benchmark Data Repository

- **9 Curated Datasets:** S22, S66, S66x8, GMTKN55, G2/97, G3/99, HEAT298, W4-11, WATER27
- **Full Attribution:** Citations, DOIs, licenses
- **Reference Energies:** CCSD(T)/CBS, experimental data
- **Method Performance:** MAE/RMSE for common functionals

### 5. AI Expert Agent

- **Multi-Interface:** FastAPI REST, VS Code extension, Jupyter magic
- **RAG Pipeline:** LangChain-orchestrated retrieval
- **Semantic Search:** ChromaDB vector similarity
- **Citation Generation:** Grounded in KB references

---

## Usage Examples

### Semantic Search

```python
from api.qcdb_embeddings import EmbeddingManager
from api.semantic_search import SemanticSearch

# Initialize
manager = EmbeddingManager(cache_dir, openai_api_key="...")
search = SemanticSearch(manager, kb)

# Search
results = search.search(
    "How do I choose between B3LYP and PBE0 for a transition metal complex?",
    top_k=5
)

for result in results:
    print(f"{result['entity_type']}: {result['name']}")
    print(f"  Relevance: {result['score']:.3f}")
```

### Query Neo4j

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "qcdb_password_2025"))

with driver.session() as session:
    # Find all workflows for geometry optimization
    result = session.run("""
        MATCH (w:Workflow)
        WHERE w.name CONTAINS 'Geometry'
        RETURN w.name, w.goal, w.difficulty
    """)
    
    for record in result:
        print(record['w.name'])
```

### Client Extension

```json
{
  "client_id": "airtronics",
  "extension_version": "1.0.0",
  "visibility": "client_specific",
  "entities": {
    "Workflows": [
      {
        "id": "client_airtronics_workflow_sensor_simulation",
        "name": "THz Sensor Simulation Protocol",
        "goal": "Simulate THz spectroscopy for materials detection",
        "visibility": "client_specific",
        "proprietary": true
      }
    ]
  }
}
```

---

## Maintenance

### Daily Automated Backups

Backups run daily at 3 AM via Windows Task Scheduler:

```powershell
# Manual backup
.\scripts\neo4j_backup.ps1

# With cloud backup
.\scripts\neo4j_backup.ps1 -CloudBackup
```

### Quarterly Updates

Per `MAINTENANCE_SCHEDULE.md`:
- **March 1:** Check software releases, update version matrix
- **June 1:** Add new benchmark datasets
- **September 1:** Review method developments
- **December 1:** Update documentation

### Cost Monitoring

```python
from api.qcdb_embeddings import EmbeddingManager

manager = EmbeddingManager(cache_dir)
stats = manager.get_stats()

print(f"Monthly cost: ${stats['monthly_cost_usd']:.2f}")
print(f"Budget remaining: ${stats['budget_remaining_usd']:.2f}")
```

---

## Testing

```powershell
# Run all tests
cd tests
.\run_all_tests.ps1

# Run specific test suite
pytest test_kb_integrity.py -v
pytest test_api_comprehensive.py --cov=api
```

---

## Documentation

- **API Documentation:** `QCDB_API_DOCUMENTATION.md`
- **User Guide:** `QCDB_USER_GUIDE.md`
- **Developer Guide:** `QCDB_DEVELOPER_GUIDE.md`
- **Architecture:** `QCDB_ARCHITECTURE.md`
- **Security:** `CLIENT_EXTENSION_SECURITY.md`
- **Benchmarks:** `benchmarks/BENCHMARK_ATTRIBUTION.md`

---

## Contributing

### Git Workflow

1. Create feature branch
2. Make changes to JSON files
3. Run validation: `python scripts/build_knowledge_graph.py`
4. Commit changes
5. Create pull request
6. Automated tests run
7. Peer review
8. Merge triggers Neo4j sync

### Adding New Entities

1. Edit appropriate JSON file (`qc_methods_expanded.json`, etc.)
2. Follow ID naming convention: `{type}_{name}`
3. Add cross-references
4. Rebuild: `python scripts/build_knowledge_graph.py`
5. Sync: `python scripts/sync_to_neo4j.py`

---

## Troubleshooting

### Neo4j Connection Failed

```powershell
# Check if container is running
docker ps

# Start containers
docker-compose up -d

# Check logs
docker logs qcdb_neo4j
```

### Embedding Budget Exceeded

```python
# Check current usage
manager = EmbeddingManager(cache_dir)
stats = manager.get_stats()

# Increase budget
manager.monthly_budget = 100.0

# Or use local model only
embeddings = manager.embed(texts, model="local")
```

### Import Errors

```powershell
# Reinstall dependencies
pip install -r requirements_qc.txt --force-reinstall

# Test imports
python -c "import pyscf, ase, neo4j, langchain; print('OK')"
```

---

## License & Attribution

QCBD Core Knowledge Base: Internal Q-SMEC Development  
Benchmark Data: See `benchmarks/BENCHMARK_ATTRIBUTION.md`  
Dependencies: See individual package licenses

---

## Support

For issues, questions, or feature requests:
- Internal: Contact Q-SMEC Development Team
- External: See documentation or create issue in repository

---

**Last Updated:** December 1, 2025  
**Version:** 1.0.0
