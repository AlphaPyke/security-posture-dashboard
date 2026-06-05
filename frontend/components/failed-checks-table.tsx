import type { ScanCheck } from "@/lib/types";
import { riskBadgeClass } from "@/lib/ui";

export function FailedChecksTable({ checks }: Readonly<{ checks: ScanCheck[] }>) {
  return (
    <section className="rounded-md border border-border bg-white shadow-sm">
      <div className="border-b border-border px-4 py-3">
        <h2 className="text-base font-semibold tracking-normal">Failed checks</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[720px] text-left text-sm">
          <thead className="bg-muted text-xs uppercase tracking-normal text-muted-foreground">
            <tr>
              <th className="px-4 py-3 font-medium">Check</th>
              <th className="px-4 py-3 font-medium">Score</th>
              <th className="px-4 py-3 font-medium">Risk</th>
              <th className="px-4 py-3 font-medium">Reason</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {checks.map((check) => (
              <tr key={check.name}>
                <td className="px-4 py-3 font-medium">{check.name}</td>
                <td className="px-4 py-3">{check.score} / 10</td>
                <td className="px-4 py-3">
                  <span className={riskBadgeClass(check.severity)}>{check.severity}</span>
                </td>
                <td className="px-4 py-3 text-muted-foreground">{check.reason}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
