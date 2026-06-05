import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import type { ScanCheck } from "@/lib/types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function riskBadgeClass(severity: ScanCheck["severity"]) {
  return cn(
    "inline-flex h-6 items-center rounded-md px-2 text-xs font-medium",
    severity === "Critical" && "bg-danger text-white",
    severity === "High" && "bg-red-100 text-red-700",
    severity === "Medium" && "bg-amber-100 text-amber-800",
    severity === "Low" && "bg-emerald-100 text-emerald-700"
  );
}
