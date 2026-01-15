# Run sample enrichment on S22 (2 records) using local Python
$ErrorActionPreference = "Stop"
Push-Location "G:\My Drive\Databases\qc_benchmark_full_system"
if (-not (Test-Path "exports")) { New-Item -ItemType Directory -Path "exports" | Out-Null }
if (-not (Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" | Out-Null }
& python -m arxiv_qc_harvester.cli --input data/s22_sample.jsonl --output exports/s22_enriched.jsonl
Pop-Location
