# Robust arXiv backfill runner with auto-adjustments
# Usage: .\run_arxiv_backfill.ps1 [-Since "YYYY-MM-DD"]
param(
    [string]$Since
)

$ErrorActionPreference = "Stop"

# Activate venv
& "G:/My Drive/.01 API Keys/.venv/Scripts/Activate.ps1"
Push-Location "G:\My Drive\Databases\QCBD"

# Initial conservative settings
$env:ARXIV_DELAY = "1.5"
$env:ARXIV_MAX_RESULTS = "100"
$env:ARXIV_MAX_PAGES = "5" # per category
if ($Since) { $env:ARXIV_SINCE = $Since }

function Invoke-Arxiv {
    param([int]$attempt)
    Write-Host "[Run] arXiv backfill attempt $attempt with settings: delay=$env:ARXIV_DELAY results=$env:ARXIV_MAX_RESULTS pages=$env:ARXIV_MAX_PAGES since=$env:ARXIV_SINCE" -ForegroundColor Cyan
    & python "g:\My Drive\Databases\QCBD\scripts\harvest_arxiv.py" $(if ($env:ARXIV_SINCE) {"--since $env:ARXIV_SINCE"} )
    return $LASTEXITCODE
}

for ($i = 1; $i -le 4; $i++) {
    $code = Invoke-Arxiv -attempt $i
    if ($code -eq 0) {
        Write-Host "[OK] arXiv harvest completed successfully." -ForegroundColor Green
        break
    }
    Write-Host "[WARN] arXiv harvest exit code $code; applying backoff and retry..." -ForegroundColor Yellow
    # Auto-adjust: increase delay, lower page size, cap pages tighter
    $env:ARXIV_DELAY = [string]([double]$env:ARXIV_DELAY + 0.5)
    $env:ARXIV_MAX_RESULTS = [string]([int]$env:ARXIV_MAX_RESULTS - 20)
    if ([int]$env:ARXIV_MAX_RESULTS -lt 50) { $env:ARXIV_MAX_RESULTS = "50" }
    $env:ARXIV_MAX_PAGES = [string]([int]$env:ARXIV_MAX_PAGES - 1)
    if ([int]$env:ARXIV_MAX_PAGES -lt 2) { $env:ARXIV_MAX_PAGES = "2" }
}

Pop-Location
