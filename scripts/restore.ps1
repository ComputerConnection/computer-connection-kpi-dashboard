param(
    [Parameter(Mandatory=$true)]
    [string]$BackupFile
)

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

docker compose up -d db

Write-Host "Restoring $BackupFile"
docker exec -i db psql -U postgres postgres < $BackupFile

docker compose up -d

if ($tmp) { Remove-Item -Recurse -Force $tmp }
