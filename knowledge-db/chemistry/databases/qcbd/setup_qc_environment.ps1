# QCDB Environment Setup Script
# Installs all required Python packages and verifies Docker services

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "QCDB Environment Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Activate virtual environment
Write-Host "[1/6] Activating Python virtual environment..." -ForegroundColor Yellow
$venvPath = "G:\My Drive\envs\.venv_QuantumAI"

if (Test-Path "$venvPath\Scripts\Activate.ps1") {
    & "$venvPath\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not found at: $venvPath" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
    & "$venvPath\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment created and activated" -ForegroundColor Green
}

# Step 2: Upgrade pip
Write-Host "`n[2/6] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green

# Step 3: Install packages
Write-Host "`n[3/6] Installing Python packages (this may take 10-15 minutes)..." -ForegroundColor Yellow
pip install -r requirements_qc.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All packages installed" -ForegroundColor Green
} else {
    Write-Host "✗ Some packages failed to install. Check logs above." -ForegroundColor Red
}

# Step 4: Set environment variables
Write-Host "`n[4/6] Setting environment variables..." -ForegroundColor Yellow
$env:QCBD_ROOT = "G:\My Drive\Databases\QCBD"
$env:NEO4J_URI = "bolt://localhost:7687"
$env:NEO4J_USER = "neo4j"
$env:NEO4J_PASSWORD = "quantum_db_2025"
$env:REDIS_URI = "redis://localhost:6379"
Write-Host "✓ Environment variables set" -ForegroundColor Green

# Step 5: Check Docker Desktop
Write-Host "`n[5/6] Checking Docker Desktop..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker is installed: $dockerVersion" -ForegroundColor Green
    
    $dockerRunning = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker Desktop is running" -ForegroundColor Green
    } else {
        Write-Host "✗ Docker Desktop is not running. Please start it." -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Docker is not installed or not in PATH" -ForegroundColor Red
}

# Step 6: Test imports
Write-Host "`n[6/6] Testing critical imports..." -ForegroundColor Yellow
$testScript = @"
try:
    import pyscf
    import ase
    import neo4j
    import chromadb
    import langchain
    import openai
    print('✓ All critical packages imported successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
"@

python -c $testScript

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Start Docker: docker-compose up -d" -ForegroundColor White
Write-Host "2. Build KB: python scripts/build_knowledge_graph.py" -ForegroundColor White
Write-Host "3. Sync to Neo4j: python scripts/sync_to_neo4j.py" -ForegroundColor White
Write-Host ""
