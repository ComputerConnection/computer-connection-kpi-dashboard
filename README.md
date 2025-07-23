# Computer Connection KPI Dashboard

This repository contains a monorepo setup for a KPI dashboard application with backend, frontend, ETL and infrastructure configuration.

## Development

1. Copy `.env.sample` to `.env` and adjust values if needed.
2. Run the development stack:

```powershell
scripts/dev_up.ps1
```

The services will be available at:
- API: <https://dashboard.local/api/v1/health>
- GraphQL: <https://dashboard.local/graphql>
- UI: <https://dashboard.local/>
- Prefect: <http://localhost:4200>
- Mailhog: <http://localhost:8025>

## Repository Layout

- `backend/` – FastAPI application
- `frontend/` – React dashboard
- `etl/` – ETL flow definitions
- `infra/` – Docker/Caddy configuration
- `scripts/` – Helper scripts and seed data
