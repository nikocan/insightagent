/**
 * Uygulamanın kök layout bileşeni; global stilleri, üst navigasyonu ve AppProviders sargısını tanımlar.
 */
import "./globals.css";
import type { Metadata } from "next";
import { ReactNode } from "react";
import { TopNav } from "./components/top-nav";
import { AppProviders } from "./providers";

export const metadata: Metadata = {
  title: "Cafeoi | AI Proje Planlama Platformu",
  description:
    "Fikirlerinizi birkaç soruda yakalayıp AI destekli proje planlarına dönüştüren uçtan uca platform."
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="tr" suppressHydrationWarning>
      <body className="bg-slate-950 text-slate-50">
        <AppProviders>
          <TopNav />
          {children}
        </AppProviders>
      </body>
    </html>
  );
}
