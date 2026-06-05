import type { RepositorySummary, ScanCheck, ScanSummary, TrendPoint } from "@/lib/types";

const repositories: RepositorySummary[] = [
  {
    id: "repo_1",
    fullName: "AlphaPyke/peerprep-g15",
    defaultBranch: "main",
    visibility: "private",
    criticality: "high"
  },
  {
    id: "repo_2",
    fullName: "AlphaPyke/security-lab",
    defaultBranch: "main",
    visibility: "public",
    criticality: "medium"
  }
];

const scan: ScanSummary = {
  id: "scan_1",
  status: "completed",
  overallScore: 7.4,
  riskLevel: "Medium",
  completedAt: "5 Jun 2026, 9:30 PM",
  summary: "3 high-priority checks need remediation before the next release."
};

const checks: ScanCheck[] = [
  {
    id: "finding_1",
    name: "Branch-Protection",
    score: 0,
    severity: "High",
    reason: "Default branch is not protected.",
    remediation: "Enable branch protection for main, require pull request reviews, require status checks, and block force pushes."
  },
  {
    id: "finding_2",
    name: "Token-Permissions",
    score: 3,
    severity: "High",
    reason: "Workflow token permissions are broader than necessary.",
    remediation: "Set default GitHub Actions token permissions to read-only and grant write permissions only in workflows that need them."
  },
  {
    id: "finding_3",
    name: "Code-Review",
    score: 8,
    severity: "Medium",
    reason: "Most changes are reviewed, but enforcement is incomplete.",
    remediation: "Require at least one approving review before merge and prevent dismissing stale reviews without reapproval."
  }
];

const history: TrendPoint[] = [
  { label: "Scan 1", score: 6.8, failedChecks: 7 },
  { label: "Scan 2", score: 7.1, failedChecks: 5 },
  { label: "Scan 3", score: 7.4, failedChecks: 4 }
];

export const sampleDashboard = {
  repositories,
  repository: repositories[0],
  scan,
  checks,
  history
};
