# Security Posture Dashboard

Security Posture Dashboard is a DevSecOps MVP that helps developers understand the security posture of one GitHub repository at a time. It ingests OpenSSF Scorecard results, enriches them with repository context, computes custom risk ratings, tracks trends over time, and supports remediation workflows through GitHub issues.

## MVP Scope

The first version supports this flow:

```text
Login with GitHub
-> View repositories
-> Select one repository
-> Run OpenSSF Scorecard scan
-> Store scan results
-> Show dashboard, failed checks, and suggested fixes
```

Multi-repo governance, SLOs, deployment gates, and AI recommendations are intentionally left for later versions.

## Stack

- `frontend`: Next.js, React, Tailwind CSS
- `backend`: FastAPI, SQLAlchemy, Alembic
- `database`: PostgreSQL
- `queue`: Redis + RQ worker
- `scanner`: OpenSSF Scorecard CLI, with a stubbed dev mode enabled by default

## Project Structure

```text
frontend/   Next.js app and UI components
backend/    FastAPI API, models, services, migrations, worker
infra/      Docker Compose and local infrastructure
docs/       Architecture, threat model, and demo script
```

## Local Development

Start the full stack:

```bash
docker compose -f infra/docker-compose.yml up --build
```

Run the initial database migration:

```bash
docker compose -f infra/docker-compose.yml exec backend alembic upgrade head
```

Open:

- Frontend: http://localhost:3000
- API health: http://localhost:8000/healthz
- API docs: http://localhost:8000/docs

## GitHub OAuth

Create a GitHub OAuth app with callback URL:

```text
http://localhost:8000/auth/github/callback
```

Then copy `backend/.env.example` to `backend/.env`, fill in `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`, and update `infra/docker-compose.yml` to load `../backend/.env` instead of the example file.

## Scorecard

`SCORECARD_USE_STUB=true` keeps scan development fast by returning sample Scorecard-style results. Set it to `false` and install the OpenSSF Scorecard CLI in the backend image when you are ready to run real scans.
