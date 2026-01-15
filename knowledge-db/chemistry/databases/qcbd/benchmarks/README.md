# QCBD Benchmark Datasets

This directory contains structured benchmark data for quantum chemistry methods validation.

## Available Benchmark Sets

### S22 - Non-covalent Interactions
- **Systems**: 22 molecular dimers
- **Properties**: Interaction energies
- **Reference**: CCSD(T)/CBS
- **Citation**: Jurečka et al., PCCP 2006, 8, 1985
- **Data**: `data/raw/benchmarks/s22_benchmarks.jsonl` (22 records)

### S66 - Extended Non-covalent Interactions
- **Systems**: 66 molecular dimers (sample: 10 representative)
- **Properties**: Interaction energies at multiple geometries
- **Reference**: CCSD(T)/CBS
- **Citation**: Řezáč et al., JCTC 2011, 7, 2427
- **Data**: `data/raw/benchmarks/s66_benchmarks.jsonl` (10 records)

### GMTKN55 - Comprehensive Thermochemistry & Kinetics
- **Subsets**: 55 benchmark subsets (sample: 10 representative)
- **Systems**: 1505 total across all subsets
- **Properties**: Reaction energies, barrier heights, interaction energies, isomerization
- **Reference**: W1/W2 composite and CCSD(T)/CBS
- **Citation**: Goerigk et al., PCCP 2017, 19, 32184
- **Data**: `data/raw/benchmarks/gmtkn55_subsets.jsonl` (10 subset descriptions)

### Water27 - Water Cluster Binding Energies
- **Systems**: 27 water clusters (dimers to hexamers; sample: 7 representative)
- **Properties**: Binding energies
- **Reference**: CCSD(T)/CBS
- **Citation**: Bryantsev et al., JCTC 2009, 5, 1016
- **Data**: `data/raw/benchmarks/water27_benchmarks.jsonl` (7 records)

## Database Integration

All benchmark datasets are loaded into the `datasets` table during database build:

```powershell
python scripts/harvest_benchmarks.py  # Generate benchmark JSONL
python scripts/build_db.py            # Load into SQLite
```

## Searching Benchmarks

Use `search_cli.py` to query benchmark data:

```powershell
# Search for S22 benchmarks
python scripts/search_cli.py "S22" --table datasets

# Search by reference method
python scripts/search_cli.py "CCSD(T)" --table datasets

# Search by property type
python scripts/search_cli.py "interaction energy" --table datasets

# Search for water clusters
python scripts/search_cli.py "water cluster" --table datasets
```

## Data Format

Each benchmark record includes:
- `id`: Unique identifier (e.g., `benchmark.s22.01`)
- `benchmark_set`: Set name (S22, S66, GMTKN55, Water27)
- `system_name` or `subset_name`: Descriptive name
- `reference_energy_kcal` or `num_systems`: Reference value or count
- `reference_level`: Theory level (e.g., CCSD(T)/CBS)
- `property_type`: Measured property
- `domains`: ["quantum_chemistry"]
- `keywords`: Searchable tags
- `reference`: Full citation
- `doi`: DOI link
- `provenance`: "open_data"
- `trust_tier`: "A" (trusted benchmark)

## Legal & Attribution

All benchmark data are open-access and properly cited. See `BENCHMARK_ATTRIBUTION.md` for full references and usage terms.

## Extending Benchmarks

To add new benchmark sets:
1. Add harvester logic to `scripts/harvest_benchmarks.py`
2. Update `benchmark_registry.json` with metadata
3. Run `scripts/harvest_benchmarks.py` and rebuild DB
4. Update this README

Current database size: **2116 records** (including 49 benchmark entries)
