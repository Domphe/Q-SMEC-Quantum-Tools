# Q-SMEC Registry Full Platform

This archive includes all concept, use case, model, enrichment, and deployment modules for the Q-SMEC quantum chemistry and quantum sensing platform.

## Included Modules

- `concept_registry/`: Core knowledge graph concepts
- `enrichment_engine/`: Enrichment from real APIs (QCDB, PubChem, OpenAlex)
- `models/`: Graph-based deep learning models (GAT, DimeNet, Graphormer)
- `training/`: Training logic and datasets (JSONL format)
- `notebooks/`: Model training, evaluation, and explainability
- `dashboard/`: Streamlit-based explorer for TRL/MRL, sensors, models
- `server/`: FastAPI inference server
- `cli/`: Command-line tools for enrichment, linking, training

## Usage

- Run `docker-compose up` to launch the full dashboard and API.
- Use the notebooks for molecule-wise predictions and evaluation.
- Use CLI for enrichment and updates.

License: Proprietary with open integration layers.

