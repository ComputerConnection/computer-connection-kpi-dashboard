# computer-connection-kpi-dashboard
KPI Dashboard – Local‑First (Windows) MVP

One URL to see the truth about your business & life. Local-first, mock-data ready, API‑switchable.

1. What Is This?

A modular, self‑hosted dashboard for Zach Henry (Computer Connection, OKC) that aggregates business + personal KPIs (sales, margin, quotes, repairs, cash, habits) into a single UI. Runs entirely on your Windows box via Docker Desktop/WSL2. Starts with mock data; flip a flag to pull from real APIs when creds are ready.

2. Quick Start (Windows 11)

Prereqs

Docker Desktop (WSL2 backend enabled)

Git & PowerShell 7+

Clone & Run

git clone https://github.com/computer-connection/kpi-dashboard.git
cd kpi-dashboard
cp .env.sample .env.dev   # or copy manually
# (edit .env.dev if you want – defaults are fine for mocks)

./scripts/dev_up.ps1 -Rebuild

Then open:

UI: https://dashboard.local/

API Health: https://dashboard.local/api/v1/health

GraphQL IDE: https://dashboard.local/graphql

Prefect UI: http://localhost:4200

Mailhog (dev email): http://localhost:8025

If the browser complains about certs, import Caddy’s internal CA (instructions in /docs/ops-runbook.md) or just bypass in dev.

3. Stack Overview

Layer

Tech

Path

Frontend

React + Vite + Tailwind + Zustand + Recharts

frontend/

Backend API

FastAPI (REST) + Strawberry GraphQL

backend/app/

Data/DB

PostgreSQL + SQLAlchemy + materialized views

infra/db/

Orchestration

Prefect 2.x (Orion)

etl/flows/

Cache/Queue

Redis

docker service redis

Reverse Proxy

Caddy (TLS, routing)

infra/Caddyfile

4. Environment & Secrets

Mock mode: USE_MOCK_DATA=true (default), uses JSON generators to seed the DB.

Real mode: Set creds in .env.prod (never commit). Toggle USE_MOCK_DATA=false.

.env.sample lists all variables; copy to .env.dev or .env.prod.

Optional: run Vaultwarden/HashiCorp Vault and point services to it (see /docs/ops-runbook.md).

5. Common Commands

# Start dev stack (detached)
./scripts/dev_up.ps1

# Rebuild containers
docker compose down --remove-orphans
./scripts/dev_up.ps1 -Rebuild

# Seed mock data manually
python ./scripts/seed_mock_data.py

# Run backend tests
cd backend; poetry run pytest --cov=app

# Run frontend lint/build
cd frontend; npm run lint && npm run build

# Backup database (PowerShell)
./scripts/backup.ps1

6. Project Structure

kpi-dashboard/
├─ backend/              # FastAPI + GraphQL
├─ frontend/             # React app
├─ etl/                  # Prefect flows, mocks
├─ infra/                # Caddy, DB init, Prefect config
├─ scripts/              # PowerShell + Python helpers
├─ docs/                 # Deep docs (architecture, formulas, runbook)
├─ docker-compose.yml
├─ .github/workflows/    # CI pipelines
└─ .env.sample

7. Contributing & Workflow

Branch naming: feature/<short-desc>, fix/<short-desc>, chore/...

Issues: Use EPIC → Story → Task hierarchy. Link PRs to issues.

PR checklist: Code + tests + docs updated, migrations included, CI green.

Commits: Conventional commits preferred (feat:, fix:, docs: …).

See /docs/contributing.md for details.

8. Roadmap

✅ Local mock MVP

🔜 Real API connectors (Lightspeed, WooCommerce, QuoteMachine, QBO, Stripe, HubSpot, Meta Ads)

🔜 Automation hooks (SMS follow-ups, HubSpot sequences)

🔜 Forecasting/AI insights

🔜 Plugin/widget manifest

Track progress in GitHub Projects/Issues under EPIC: Unified KPI Dashboard MVP (Local Windows).

9. Troubleshooting

Symptom

Likely Cause

Fix

dashboard.local won’t load

Hostname not resolved

Add to C:\Windows\System32\drivers\etc\hosts or use localhost

HTTPS cert warning

Self-signed TLS

Import Caddy root CA or use HTTP in dev

Prefect UI blank

Port conflict

Change port in compose or stop other service

Docker permission errors

WSL path issues

Ensure repo in WSL-friendly path, restart Docker Desktop

More in /docs/ops-runbook.md.

10. License & Credits

Proprietary for now (Computer Connection internal). Update when/if open-sourcing.

Built by Zach + autonomous agents. ♥

11. Contact / Support

Open a GitHub issue or ping via your internal comms channel. For urgent breakages, mark the issue as sev1
