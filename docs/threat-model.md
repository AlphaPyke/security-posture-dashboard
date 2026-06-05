# Threat Model

## Assets

- GitHub OAuth access tokens.
- Repository metadata and security findings.
- Scan history and remediation state.
- User session cookies.

## Primary Risks

- OAuth token leakage through logs, database reads, or browser exposure.
- Overbroad GitHub scopes during authorization.
- Unauthorized access to another user's selected repositories or scans.
- Worker command injection through repository names.
- Misleading risk ratings if stale scan results are presented as fresh.

## MVP Controls

- Store GitHub tokens encrypted at rest.
- Keep tokens server-side only.
- Scope all repository, scan, and finding reads by authenticated user ownership.
- Run Scorecard through a fixed argument list rather than shell interpolation.
- Track scan status, start time, completion time, and errors.
- Keep GitHub issue creation as an explicit user action.

## Follow-Up Controls

- Rotate encryption keys.
- Add CSRF protection for state-changing endpoints.
- Add audit logs for scans, issue creation, ignored findings, and token refresh.
- Add rate limiting for scan creation.
- Add GitHub OAuth state validation.
