import { ShieldCheck } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { ButtonLink } from "@/components/ui/button-link";

export default function HomePage() {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

  return (
    <AppShell>
      <section className="mx-auto flex min-h-[70vh] max-w-3xl flex-col justify-center gap-8 px-6 py-16">
        <div className="flex h-12 w-12 items-center justify-center rounded-md bg-primary text-primary-foreground">
          <ShieldCheck className="h-7 w-7" aria-hidden="true" />
        </div>
        <div className="space-y-4">
          <h1 className="text-4xl font-semibold tracking-normal text-foreground sm:text-5xl">
            Security Posture Dashboard
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-muted-foreground">
            Log in with GitHub, select one repository, run an OpenSSF Scorecard scan, and review the
            highest-risk fixes from one focused dashboard.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <ButtonLink href={`${apiBaseUrl}/auth/github/login`}>Log in with GitHub</ButtonLink>
          <ButtonLink href="/dashboard" variant="secondary">
            View skeleton dashboard
          </ButtonLink>
        </div>
      </section>
    </AppShell>
  );
}
