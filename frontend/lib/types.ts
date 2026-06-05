export type RepositorySummary = {
  id: string;
  fullName: string;
  defaultBranch: string;
  visibility: "public" | "private";
  criticality: "low" | "medium" | "high";
};

export type ScanSummary = {
  id: string;
  status: "queued" | "running" | "completed" | "failed";
  overallScore: number;
  riskLevel: "Low" | "Medium" | "High" | "Critical";
  completedAt: string;
  summary: string;
};

export type ScanCheck = {
  id: string;
  name: string;
  score: number;
  severity: "Low" | "Medium" | "High" | "Critical";
  reason: string;
  remediation: string;
};

export type TrendPoint = {
  label: string;
  score: number;
  failedChecks: number;
};
