
# Quantum Chemistry Method Registry

## Features
- ✅ Schema-based method representation
- 🔗 Auto-link related quantum chemistry methods
- 📡 Enrich methods with citation counts and software metadata
- 📊 Explore via Streamlit dashboard
- 📦 Containerized with Docker

## How to Run

```bash
# Build Docker
docker build -t qc_registry .

# Run the dashboard
docker run -p 8501:8501 qc_registry
```

## CLI Usage
```bash
# Enrich methods with citation data
python cli/enrich.py

# Link related methods
python cli/link_methods.py
```
