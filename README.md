# KPI Dashboard – Local-First (Windows)

> One URL to see business + personal KPIs. Runs on your PC with Docker. Starts with mock data; flip a flag for real APIs.

## Quick Start (Windows 11)

**Prereqs:** Docker Desktop (WSL2), Git, PowerShell 7+

```powershell
git clone https://github.com/<org>/kpi-dashboard.git
cd kpi-dashboard
Copy-Item .env.sample .env.dev
./scripts/dev_up.ps1 -Rebuild
```

Open:

- UI: https://dashboard.local/ (or https://localhost/)
- API: https://dashboard.local/api/v1/health
- GraphQL: https://dashboard.local/graphql
- Prefect: http://localhost:4200
- Mailhog: http://localhost:8025

## Stack

| Layer        | Tech                                      | Path         |
| ------------ | ----------------------------------------- | ------------ |
| Frontend     | React + Vite + Tailwind + Zustand + Recharts | frontend/    |
| Backend      | FastAPI + Strawberry GraphQL              | backend/     |
| Data         | Postgres + SQLAlchemy/Views               | infra/db/    |
| ETL          | Prefect 2.x                               | etl/         |
| Cache        | Redis                                     | (docker svc) |
| Proxy        | Caddy                                     | infra/Caddyfile |

## Env & Secrets

Mock mode: `USE_MOCK_DATA=true` (default).
Real mode: put creds in `.env.prod`, set `USE_MOCK_DATA=false`.
Never commit real secrets.

## Commands

```powershell
./scripts/dev_up.ps1                # start
docker compose down --remove-orphans
./scripts/dev_up.ps1 -Rebuild       # rebuild
python ./scripts/seed_mock_data.py  # seed data
cd backend; poetry run pytest       # backend tests
cd frontend; npm run lint && npm run build  # frontend
./scripts/backup.ps1                # backup DB
```

## Structure

```
kpi-dashboard/
  backend/
  frontend/
  etl/
  infra/
  scripts/
  docs/
  docker-compose.yml
  .env.sample
  .github/workflows/
```

## Workflow

Issues → feature branches → PR → merge.

## Roadmap

- ✅ Mock MVP local
- 🔜 Real API connectors
- 🔜 Automation hooks
- 🔜 Forecasting/AI
- 🔜 Plugin/widget manifest

## Troubleshooting

| Problem                       | Cause             | Fix                                      |
| ----------------------------- | ----------------- | ---------------------------------------- |
| dashboard.local not loading   | Host entry missing| Use localhost or add to hosts file       |
| HTTPS warning                 | Self-signed TLS   | Import Caddy CA or use HTTP in dev       |
| Prefect UI blank              | Port conflict     | Change port or stop conflicting app      |
| Docker errors on paths        | WSL path quirks   | Keep repo in local disk, restart Docker  |

## License & Contact

Proprietary (internal). Open a GitHub issue for help.
