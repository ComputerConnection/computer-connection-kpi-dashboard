# Computer Connection KPI Dashboard

This monorepo contains the backend API, frontend web application, ETL jobs and infrastructure configuration for the KPI dashboard.

## Local Development

1. Copy `.env.sample` to `.env` and adjust values if needed.
2. Start the development stack:
   ```powershell
   scripts/dev_up.ps1
   ```
   This spins up Docker services for the API, database, Prefect, Mailhog and a Caddy proxy.

Once running you can access:
- API: <https://dashboard.local/api/v1/health>
- GraphQL: <https://dashboard.local/graphql>
- UI: <https://dashboard.local/>
- Prefect: <http://localhost:4200>
- Mailhog: <http://localhost:8025>

### Running Tests

Backend tests require Poetry:
```bash
cd backend
poetry install
poetry run pytest
```

Frontend lint and build:
```bash
cd frontend
npm ci
npm run lint && npm run build
```

### Seed Mock Data

Populate Postgres with fake values:
```bash
python scripts/seed_mock_data.py
```

## Repository Layout

- `backend/` – FastAPI application
- `frontend/` – React dashboard
- `etl/` – ETL flow definitions
- `infra/` – Docker/Caddy configuration
- `scripts/` – Helper scripts and seed data
