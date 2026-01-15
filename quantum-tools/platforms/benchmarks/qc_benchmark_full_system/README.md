
# Quantum Chemistry Benchmark CLI System

This is a complete CLI-driven, container-ready scientific enrichment and validation platform for quantum chemistry benchmark datasets.

## 🔧 Features

- ✅ Pydantic schema validation for benchmark entries
- 🔁 Retry processor for missing or incomplete records
- 🧬 Structure resolution via PubChem (SMILES, InChI, InChIKey)
- 🧠 DOI enrichment via Crossref (journal + publication year)
- 🖥️ Full CLI tool for enrichment, filtering, and export
- 🐳 Dockerfile + docker-compose for isolated execution

## 📁 Directory Structure

```
.
├── lib/                       # Core Python modules
├── data/                     # Input files + retry storage
├── exports/                  # Enriched outputs
├── logs/                     # Validation + enrichment logs
├── Dockerfile                # Container build file
├── docker-compose.yml        # Volume persistence + CLI service
├── requirements.txt          # Python dependencies
└── README.md                 # This guide
```

## 🚀 Usage

### 🔨 Build Docker Image

```bash
docker-compose build
```

### ▶️ Run CLI in Container

```bash
docker-compose run qcbench bash
```

Then inside container:

```bash
python -m arxiv_qc_harvester.cli --input data/s22.jsonl --output exports/s22_enriched.jsonl
```

### 🔁 Retry Failed

```bash
python -m arxiv_qc_harvester.cli --retry
```

### 🔍 Filter on Key/Value

```bash
python -m arxiv_qc_harvester.cli --input data/all.jsonl --output exports/filtered.jsonl --filter-key benchmark_set --filter-value S66
```

## 📦 Outputs

- Enriched records to `exports/*.jsonl`
- Logs in `logs/benchmark_enrichment.log`
- Retry queue in `data/retry_records.jsonl`

## 🧪 Requirements

```txt
pydantic
pubchempy
requests
```

Install locally:

```bash
pip install -r requirements.txt
```

---

© QCBD Benchmarking Suite • 2025
