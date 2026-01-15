# QCBD Neo4j Automated Backup Script
# Schedule this with Windows Task Scheduler to run daily at 3 AM

param(
    [int]$RetentionDays = 30,
    [switch]$CloudBackup
)

$ErrorActionPreference = "Stop"
$QCBD_ROOT = $env:QCBD_ROOT
if (-not $QCBD_ROOT) {
    $QCBD_ROOT = "G:\My Drive\Databases\QCBD"
}

$BACKUP_DIR = Join-Path $QCBD_ROOT "neo4j_backups"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_NAME = "neo4j_backup_$TIMESTAMP"
$BACKUP_PATH = Join-Path $BACKUP_DIR $BACKUP_NAME

Write-Host "=== QCDB Neo4j Backup ===" -ForegroundColor Cyan
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# Ensure backup directory exists
if (-not (Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR | Out-Null
    Write-Host "Created backup directory: $BACKUP_DIR" -ForegroundColor Green
}

# Step 1: Stop Neo4j container gracefully
Write-Host "[1/5] Stopping Neo4j container..." -ForegroundColor Yellow
try {
    docker stop qcdb_neo4j
    Write-Host "  ✓ Container stopped" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to stop container: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Create backup using neo4j-admin
Write-Host "`n[2/5] Creating database backup..." -ForegroundColor Yellow
try {
    $neo4jDataPath = Join-Path $QCBD_ROOT "neo4j_data"
    
    # Use docker run with mounted volumes to perform backup
    docker run --rm `
        -v "${neo4jDataPath}:/data" `
        -v "${BACKUP_DIR}:/backups" `
        neo4j:5.14-community `
        neo4j-admin database dump neo4j --to-path=/backups/$BACKUP_NAME
    
    Write-Host "  ✓ Backup created: $BACKUP_NAME" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Backup failed: $_" -ForegroundColor Red
    # Try to restart Neo4j anyway
    docker start qcdb_neo4j
    exit 1
}

# Step 3: Restart Neo4j
Write-Host "`n[3/5] Restarting Neo4j container..." -ForegroundColor Yellow
try {
    docker start qcdb_neo4j
    Start-Sleep -Seconds 5
    Write-Host "  ✓ Container restarted" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Failed to restart container: $_" -ForegroundColor Yellow
}

# Step 4: Clean old backups
Write-Host "`n[4/5] Cleaning old backups (retention: $RetentionDays days)..." -ForegroundColor Yellow
try {
    $cutoffDate = (Get-Date).AddDays(-$RetentionDays)
    $oldBackups = Get-ChildItem -Path $BACKUP_DIR -Directory | 
        Where-Object { $_.CreationTime -lt $cutoffDate }
    
    $deletedCount = 0
    foreach ($backup in $oldBackups) {
        Remove-Item -Path $backup.FullName -Recurse -Force
        $deletedCount++
    }
    
    Write-Host "  ✓ Deleted $deletedCount old backup(s)" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Cleanup warning: $_" -ForegroundColor Yellow
}

# Step 5: Cloud backup (optional)
if ($CloudBackup) {
    Write-Host "`n[5/5] Syncing to Google Drive cloud storage..." -ForegroundColor Yellow
    try {
        # The backup directory is already on Google Drive, so just verify
        $backupSize = (Get-ChildItem -Path $BACKUP_PATH -Recurse | 
            Measure-Object -Property Length -Sum).Sum / 1MB
        
        Write-Host "  ✓ Backup available on Google Drive ($([math]::Round($backupSize, 2)) MB)" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ Cloud sync warning: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n[5/5] Skipping cloud backup" -ForegroundColor Gray
}

# Summary
Write-Host "`n=== Backup Complete ===" -ForegroundColor Cyan
Write-Host "Backup location: $BACKUP_PATH" -ForegroundColor Gray

$totalBackups = (Get-ChildItem -Path $BACKUP_DIR -Directory).Count
$totalSize = (Get-ChildItem -Path $BACKUP_DIR -Recurse -File | 
    Measure-Object -Property Length -Sum).Sum / 1MB

Write-Host "Total backups: $totalBackups" -ForegroundColor Gray
Write-Host "Total size: $([math]::Round($totalSize, 2)) MB" -ForegroundColor Gray
Write-Host ""

# Log backup event
$logFile = Join-Path $QCBD_ROOT "backup_log.txt"
$logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | Backup: $BACKUP_NAME | Size: $([math]::Round($backupSize, 2)) MB"
Add-Content -Path $logFile -Value $logEntry

Write-Host "✓ Backup logged to: $logFile" -ForegroundColor Green
