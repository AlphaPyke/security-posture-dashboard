# Architecture

## MVP Flow

```text
User
  -> Next.js frontend
  -> FastAPI OAuth callback
  -> GitHub API
  -> PostgreSQL users/repositories/scans
  -> Redis queue
  -> Scorecard worker
  -> Dashboard and remediation workflow
```

## Services

- `frontend`: Next.js app-router UI for login, repo selection, scan status, findings, and trends.
- `backend`: FastAPI API for GitHub OAuth, repository selection, scans, findings, and issue creation.
- `worker`: RQ worker that runs OpenSSF Scorecard and persists normalized checks.
- `postgres`: Durable store for users, selected repositories, scans, and findings.
- `redis`: Queue backend for scan jobs.

## Data Model

- `users`: GitHub identity and encrypted OAuth token.
- `repositories`: User-selected GitHub repositories with visibility and criticality context.
- `scans`: Scorecard scan lifecycle, raw JSON, overall score, and computed risk level.
- `scan_checks`: Normalized check results, severity, remediation text, and optional GitHub issue URL.

## Boundaries

The app uses OpenSSF Scorecard as the scanner and focuses on productizing the signal: context, history, remediation, and GitHub issue workflows. Organization governance, policy gates, and AI recommendations are later roadmap items.
