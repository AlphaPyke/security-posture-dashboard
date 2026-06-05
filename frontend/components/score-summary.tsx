import { AlertTriangle, Clock3, GitBranch, LockKeyhole, ShieldCheck } from "lucide-react";
import type { RepositorySummary, ScanSummary } from "@/lib/types";

export function ScoreSummary({
  repository,
  scan
}: Readonly<{ repository: RepositorySummary; scan: ScanSummary }>) {
  const tiles = [
    { label: "Overall score", value: `${scan.overallScore.toFixed(1)} / 10`, icon: ShieldCheck },
    { label: "Risk level", value: scan.riskLevel, icon: AlertTriangle },
    { label: "Default branch", value: repository.defaultBranch, icon: GitBranch },
    { label: "Last scan", value: scan.completedAt, icon: Clock3 }
  ];

  return (
    <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {tiles.map((tile) => {
        const Icon = tile.icon;
        return (
          <div key={tile.label} className="rounded-md border border-border bg-white p-4 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm text-muted-foreground">{tile.label}</p>
              <Icon className="h-4 w-4 text-primary" aria-hidden="true" />
            </div>
            <p className="mt-3 text-2xl font-semibold tracking-normal">{tile.value}</p>
          </div>
        );
      })}
      <div className="rounded-md border border-border bg-white p-4 shadow-sm md:col-span-2 xl:col-span-4">
        <div className="flex flex-wrap items-center gap-x-6 gap-y-3 text-sm text-muted-foreground">
          <span className="font-medium text-foreground">{repository.fullName}</span>
          <span className="flex items-center gap-2">
            <LockKeyhole className="h-4 w-4" aria-hidden="true" />
            {repository.visibility}
          </span>
          <span>Criticality: {repository.criticality}</span>
          <span>{scan.summary}</span>
        </div>
      </div>
    </section>
  );
}
