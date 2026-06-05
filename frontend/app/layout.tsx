import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Security Posture Dashboard",
  description: "OpenSSF Scorecard-powered security posture dashboard for GitHub repositories"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
