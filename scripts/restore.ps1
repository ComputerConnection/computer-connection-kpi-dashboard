param(
    [Parameter(Mandatory=$true)]
    [string]$BackupFile,
    [string]$Container = 'db',
    [string]$Database  = 'postgres',
    [string]$User      = 'postgres'
)

Set-StrictMode -Version Latest

if (-not (Test-Path $BackupFile)) {
    Write-Error "Backup file not found"
    exit 1
}

$tmp = $null
if ($BackupFile -like '*.zip') {
    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ([System.IO.Path]::GetRandomFileName())
    Expand-Archive $BackupFile $tmp
    $sql = Get-ChildItem $tmp -Filter *.sql | Select-Object -First 1
    $BackupFile = $sql.FullName
}

docker compose down

docker compose up -d $Container

Write-Host "Restoring $BackupFile"
docker compose exec -T $Container psql -U $User $Database < $BackupFile

docker compose up -d

if ($tmp) { Remove-Item -Recurse -Force $tmp }
