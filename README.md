# Q-SMEC Quantum Tools

**Reorganized:** January 15, 2026

## Structure

### 📁 quantum-tools/
Quantum computing and AI tools for computation and analysis.
- `models-open/` - Open-source AI models
- `models-paid/` - Commercial/proprietary models
- `simulations-open/` - Open simulation tools
- `simulations-paid/` - Commercial simulation tools
- `platforms/` - QC computing platforms, benchmarks, registries
- `docs/` - Guides and reference documentation

### 📁 knowledge-db/
Domain-specific knowledge databases.
- `chemistry/` - Quantum chemistry databases (QCBD, benchmarks)
- `physics/` - Quantum physics frameworks
- `materials/` - Materials science databases and simulations
- `papers/` - Research papers and collection tools

### 📁 projects/
Active development projects.
- `qsmec-apps/` - Production Q-SMEC applications
  - `answer-engine/` - Main inference service
  - `automation/` - Background workers and pipelines
  - `connectors/` - Client integrations
- `research/` - Experimental work and notebooks

### 📁 .venv/
Python virtual environment with quantum computing dependencies.

## Quick Start

```bash
# Activate environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate    # Windows

# Run QCBD
cd knowledge-db/chemistry/databases/qcbd
python scripts/build_knowledge_graph.py

# Start answer engine
cd projects/qsmec-apps/answer-engine
python src/main.py
```

## Migration Log

Original sources consolidated from:
- `Google Drive - Z/Databases/` (50 quantum folders)
- Duplicates removed (~3 MB saved)
- Structure optimized for scalability

See `migration_log.json` for detailed migration history.
