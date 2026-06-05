import { Shield } from "lucide-react";
import Link from "next/link";

export function AppShell({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className="min-h-screen">
      <header className="border-b border-border bg-white">
        <nav className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link href="/" className="flex items-center gap-2 text-sm font-semibold">
            <Shield className="h-5 w-5 text-primary" aria-hidden="true" />
            Security Posture
          </Link>
          <Link href="/dashboard" className="text-sm font-medium text-muted-foreground hover:text-foreground">
            Dashboard
          </Link>
        </nav>
      </header>
      {children}
    </div>
  );
}
