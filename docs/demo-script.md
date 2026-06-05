# Demo Script

## One-Minute Pitch

Security Posture Dashboard helps developers understand the security posture of a GitHub repository without building a scanner from scratch. It wraps OpenSSF Scorecard results in a product workflow: select a repo, run a scan, view failed checks, understand risk, and create a GitHub issue for remediation.

## Walkthrough

1. Log in with GitHub.
2. View repositories available to the account.
3. Select one repository and set criticality.
4. Start an OpenSSF Scorecard scan.
5. Watch scan status move from queued to running to completed.
6. Review overall score, computed risk level, failed checks, and suggested fixes.
7. Create a GitHub issue for a failed check.

## Talking Points

- The scanner is OpenSSF Scorecard; the product value is orchestration, context, persistence, and remediation workflow.
- Risk is not only the raw Scorecard score. The app also considers repo exposure, criticality, scan age, and high-risk checks.
- The architecture uses a background worker so scans do not block API requests.
- The roadmap is intentionally staged: single repo first, then multi-repo governance and policy automation.
