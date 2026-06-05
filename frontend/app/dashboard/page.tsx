import { RepoSelector } from "@/components/repo-selector";
import { ScoreSummary } from "@/components/score-summary";
import { FailedChecksTable } from "@/components/failed-checks-table";
import { SuggestedFixes } from "@/components/suggested-fixes";
import { TrendPanel } from "@/components/trend-panel";
import { sampleDashboard } from "@/lib/sample-data";

export default function DashboardPage() {
  return (
    <main className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-6 sm:px-6 lg:px-8">
      <div className="flex flex-col gap-3 border-b border-border pb-5 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm font-medium text-primary">Repository posture</p>
          <h1 className="text-2xl font-semibold tracking-normal">Single-repo security overview</h1>
        </div>
        <RepoSelector repositories={sampleDashboard.repositories} selectedId={sampleDashboard.repository.id} />
      </div>

      <ScoreSummary scan={sampleDashboard.scan} repository={sampleDashboard.repository} />

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1.35fr)_minmax(360px,0.65fr)]">
        <FailedChecksTable checks={sampleDashboard.checks} />
        <SuggestedFixes checks={sampleDashboard.checks} />
      </div>

      <TrendPanel points={sampleDashboard.history} />
    </main>
  );
}
