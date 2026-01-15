#requires -version 5.1
param(
    [switch]$DryRun
)

Write-Host "[Run-All] Starting auto execution..." -ForegroundColor Cyan

# Activate verified venv
$envPath = "G:/My Drive/.01 API Keys/.venv/Scripts/Activate.ps1"
if (Test-Path $envPath) {
    Write-Host "[Env] Activating: $envPath" -ForegroundColor Cyan
    . $envPath
} else {
    Write-Host "[Env] No activation script found; using system Python." -ForegroundColor Yellow
}

# Ensure pip packages are installed
Write-Host "[Env] Ensuring dependencies..." -ForegroundColor Cyan
& python -m pip install --quiet --upgrade pip
& python -m pip install --quiet requests beautifulsoup4 lxml pyyaml jsonschema jsonschema-specifications referencing python-docx python-pptx urllib3

# Set workspace root for modules
$workspace = "g:/My Drive/Databases/QCBD"
Push-Location $workspace

# 0) Deep scan of Databases
Write-Host "[Step 0] Deep scan Databases" -ForegroundColor Cyan
python -c "import sys; from pathlib import Path; sys.path.append(str(Path('$workspace'))); import scripts.deep_scan_databases as d; d.main()"; if ($LASTEXITCODE -ne 0) { Write-Error "Deep scan failed"; Pop-Location; exit 1 }

# 0.1) QCDB ingest (if present)
Write-Host "[Step 0.1] QCDB ingest" -ForegroundColor Cyan
python -c "import sys; from pathlib import Path; sys.path.append(str(Path('$workspace'))); import scripts.ingest_qcdb as i; i.main()"; if ($LASTEXITCODE -ne 0) { Write-Error "QCDB ingest failed"; Pop-Location; exit 1 }

# === Step 0.2: Run all harvesters ===
Write-Host "[Step 0.2] Running harvesters..." -ForegroundColor Cyan
& python "$workspace/scripts/harvest_publishers.py"
& python "$workspace/scripts/harvest_nist_cccbdb.py"
& python "$workspace/scripts/harvest_nist_asd.py"
& python "$workspace/scripts/harvest_open_source_docs.py"
& python "$workspace/scripts/harvest_courses.py"
& python "$workspace/scripts/harvest_local_enhanced.py"
& python "$workspace/scripts/harvest_crossref.py"
& python "$workspace/scripts/harvest_arxiv.py"
& python "$workspace/scripts/harvest_benchmarks.py"
Write-Host "  OK All harvesters complete." -ForegroundColor Green

# === Step 0.25: Deep inventory + cross report + entity extraction ===
Write-Host "[Step 0.25] Deep inventory + cross report + entity extraction" -ForegroundColor Cyan
& python "$workspace/scripts/deep_inventory.py"
& python "$workspace/scripts/generate_cross_report.py"
& python "$workspace/scripts/extract_entities_from_report.py"
if ($LASTEXITCODE -ne 0) { Write-Host "[WARNING] Entity extraction had issues" -ForegroundColor Yellow }

# === Step 0.3: Validate schemas ===
Write-Host "[Step 0.3] Validating schemas..." -ForegroundColor Cyan
& python "$workspace/scripts/validate_schemas.py"
if ($LASTEXITCODE -ne 0) { Write-Host "[WARNING] Schema validation found errors" -ForegroundColor Yellow }

# === Step 0.4: Build database ===
Write-Host "[Step 0.4] Building SQLite database..." -ForegroundColor Cyan
& python "$workspace/scripts/build_db.py"
if ($LASTEXITCODE -ne 0) { Write-Error "Database build failed"; Pop-Location; exit 1 }

# 0.5) Ingest registry inserts into DB
Write-Host "[Step 0.5] Ingest registry inserts" -ForegroundColor Cyan
& python "$workspace/scripts/ingest_registry_inserts.py"
if ($LASTEXITCODE -ne 0) { Write-Host "[WARNING] Registry inserts ingestion failed" -ForegroundColor Yellow }

# === Step 0.6: External pipelines (arXiv bundle, benchmark CLI, linking graph) ===
Write-Host "[Step 0.6] External pipelines" -ForegroundColor Cyan

# 0.6.1 arXiv QC Harvester Dashboard bundle
$arxivRoot = "G:\My Drive\Databases\arxiv_qc_harvester_complete_final"
if (Test-Path $arxivRoot) {
    Push-Location $arxivRoot
    if (Test-Path "$arxivRoot\requirements.txt") {
        & python -m pip install --quiet -r "$arxivRoot\requirements.txt"
    }
    if (Test-Path "$arxivRoot\run_arxiv.ps1") {
        Write-Host "  [EXT] Running arXiv harvester bundle" -ForegroundColor DarkCyan
        & "$arxivRoot\run_arxiv.ps1"
    } else {
        Write-Host "  [EXT] arXiv runner not found; skipping" -ForegroundColor Yellow
    }
    Pop-Location
}

# 0.6.2 QC Benchmark Full System (sample enrichment)
$benchRoot = "G:\My Drive\Databases\qc_benchmark_full_system"
if (Test-Path $benchRoot) {
    Push-Location $benchRoot
    if (Test-Path "$benchRoot\requirements.txt") {
        & python -m pip install --quiet -r "$benchRoot\requirements.txt"
    }
    if (Test-Path "$benchRoot\run_benchmarks.ps1") {
        Write-Host "  [EXT] Running benchmark enrichment sample" -ForegroundColor DarkCyan
        & "$benchRoot\run_benchmarks.ps1"
    } else {
        Write-Host "  [EXT] Benchmark runner not found; skipping" -ForegroundColor Yellow
    }
    Pop-Location
}

# 0.6.3 Full Scientific Linking Graph Pipeline
$graphRoot = "G:\My Drive\Databases\full_scientific_linking_graph_pipeline"
if (Test-Path $graphRoot) {
    Push-Location $graphRoot
    if (Test-Path "$graphRoot\requirements.txt") {
        & python -m pip install --quiet -r "$graphRoot\requirements.txt"
    }
    if (Test-Path "$graphRoot\run_linking.ps1") {
        Write-Host "  [EXT] Building linking graph" -ForegroundColor DarkCyan
        & "$graphRoot\run_linking.ps1"
    } else {
        Write-Host "  [EXT] Linking runner not found; skipping" -ForegroundColor Yellow
    }
    Pop-Location
}

# 1) Ingestion
Write-Host "[Step 1] Ingestion pipeline" -ForegroundColor Cyan
python -c "from expert.ingestion_pipeline import main as m; m()"; if ($LASTEXITCODE -ne 0) { Write-Error "Ingestion failed"; Pop-Location; exit 1 }

# 2) Build embeddings
Write-Host "[Step 2] Build embeddings" -ForegroundColor Cyan
python -c "from expert.semantic_search import build_embeddings; build_embeddings(persist=False)"; if ($LASTEXITCODE -ne 0) { Write-Error "Embeddings failed"; Pop-Location; exit 1 }

# 3) Rank methods
Write-Host "[Step 3] Rank methods" -ForegroundColor Cyan
python -c "from expert.query_api import rank_methods; import json; print(json.dumps(rank_methods(limit=10), indent=2))" | Out-String | Write-Output

# 4) Context pack
Write-Host "[Step 4] Build context" -ForegroundColor Cyan
python -c "from expert.context_builder import build_context; import json; print(json.dumps(build_context('electron correlation in molecules'), indent=2))" | Out-String | Write-Output

# 5) Snapshot
Write-Host "[Step 5] Snapshot" -ForegroundColor Cyan
python -c "from expert.versioning import create_snapshot; print(create_snapshot('auto_run_all'))" | Out-String | Write-Output

# 6) Gap analysis
Write-Host "[Step 6] Gap analysis" -ForegroundColor Cyan
python -c "from expert.gap_analysis import analyze; import json; print(json.dumps(analyze(), indent=2))" | Out-String | Write-Output

Pop-Location
Write-Host "[Run-All] Completed successfully." -ForegroundColor Green
