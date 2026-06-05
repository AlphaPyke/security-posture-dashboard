import type { TrendPoint } from "@/lib/types";

export function TrendPanel({ points }: Readonly<{ points: TrendPoint[] }>) {
  const maxFailed = Math.max(...points.map((point) => point.failedChecks), 1);

  return (
    <section className="rounded-md border border-border bg-white p-4 shadow-sm">
      <div className="mb-4 flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="text-base font-semibold tracking-normal">Historical trend</h2>
          <p className="text-sm text-muted-foreground">Score and failed checks over recent scans</p>
        </div>
      </div>
      <div className="grid gap-3 sm:grid-cols-3">
        {points.map((point) => (
          <div key={point.label} className="rounded-md border border-border p-3">
            <div className="flex items-center justify-between text-sm">
              <span className="font-medium">{point.label}</span>
              <span>{point.score.toFixed(1)} / 10</span>
            </div>
            <div className="mt-3 h-2 rounded-full bg-muted">
              <div
                className="h-2 rounded-full bg-primary"
                style={{ width: `${Math.max(8, point.score * 10)}%` }}
              />
            </div>
            <div className="mt-3 h-2 rounded-full bg-muted">
              <div
                className="h-2 rounded-full bg-danger"
                style={{ width: `${Math.max(8, (point.failedChecks / maxFailed) * 100)}%` }}
              />
            </div>
            <p className="mt-2 text-xs text-muted-foreground">{point.failedChecks} failed checks</p>
          </div>
        ))}
      </div>
    </section>
  );
}
