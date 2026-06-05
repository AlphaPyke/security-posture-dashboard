import { ExternalLink } from "lucide-react";
import type { ScanCheck } from "@/lib/types";
import { ButtonLink } from "@/components/ui/button-link";

export function SuggestedFixes({ checks }: Readonly<{ checks: ScanCheck[] }>) {
  return (
    <section className="rounded-md border border-border bg-white shadow-sm">
      <div className="border-b border-border px-4 py-3">
        <h2 className="text-base font-semibold tracking-normal">Suggested fixes</h2>
      </div>
      <div className="divide-y divide-border">
        {checks.slice(0, 3).map((check) => (
          <article key={check.name} className="space-y-3 p-4">
            <div>
              <h3 className="text-sm font-semibold">{check.name}</h3>
              <p className="mt-1 text-sm leading-6 text-muted-foreground">{check.remediation}</p>
            </div>
            <ButtonLink href={`/findings/${check.id}/issue`} variant="secondary">
              <ExternalLink className="h-4 w-4" aria-hidden="true" />
              Create issue
            </ButtonLink>
          </article>
        ))}
      </div>
    </section>
  );
}
