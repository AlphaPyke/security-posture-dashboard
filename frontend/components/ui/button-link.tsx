import Link from "next/link";
import { cn } from "@/lib/ui";

type ButtonLinkProps = Readonly<{
  href: string;
  children: React.ReactNode;
  variant?: "primary" | "secondary";
}>;

export function ButtonLink({ href, children, variant = "primary" }: ButtonLinkProps) {
  return (
    <Link
      href={href}
      className={cn(
        "inline-flex h-10 items-center justify-center gap-2 rounded-md px-4 text-sm font-medium transition-colors",
        variant === "primary"
          ? "bg-primary text-primary-foreground hover:bg-primary/90"
          : "border border-border bg-white text-foreground hover:bg-muted"
      )}
    >
      {children}
    </Link>
  );
}
