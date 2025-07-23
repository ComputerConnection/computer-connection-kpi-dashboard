param(
  [switch]$Rebuild
)

if ($Rebuild) { docker compose down --remove-orphans }

docker compose --profile dev up -d --build

Write-Host "Dev stack starting..."
Write-Host "API:     https://dashboard.local/api/v1/health"
Write-Host "GraphQL: https://dashboard.local/graphql"
Write-Host "UI:      https://dashboard.local/"
Write-Host "Prefect: http://localhost:4200"
Write-Host "Mailhog: http://localhost:8025"
