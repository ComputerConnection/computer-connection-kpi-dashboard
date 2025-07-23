param(
    [string]$BackupDir = "$PSScriptRoot\..\backups",
    [int]$Keep = 7,
    [string]$Container = 'db',
    [string]$Database  = 'postgres',
    [string]$User      = 'postgres'
)

Set-StrictMode -Version Latest

if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
}

$timestamp = Get-Date -Format 'yyyyMMddHHmmss'
$dumpPath = Join-Path $BackupDir "postgres_$timestamp.sql"
$archivePath = "$dumpPath.zip"

Write-Host "Creating dump $dumpPath"
docker compose exec -T $Container pg_dump -U $User $Database > $dumpPath

Write-Host "Compressing $dumpPath"
Compress-Archive -Path $dumpPath -DestinationPath $archivePath
Remove-Item $dumpPath

# Cleanup old backups
$archives = Get-ChildItem $BackupDir -Filter 'postgres_*.sql.zip' | Sort-Object LastWriteTime -Descending
$archives | Select-Object -Skip $Keep | Remove-Item
