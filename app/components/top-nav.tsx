"use client";

/**
 * Üst gezinme çubuğu; ana bölümlere hızlı erişim ve plan yükseltme butonu sağlar.
 */
import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { label: "Ana Sayfa", href: "/" },
  { label: "Fikirler", href: "/ideas" },
  { label: "Şablonlar", href: "/templates" },
  { label: "Profil", href: "/profile" }
];

export function TopNav() {
  const pathname = usePathname();

  return (
    <nav className="sticky top-0 z-50 border-b border-slate-900 bg-slate-950/80 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-lg font-semibold text-white">
          Cafeoi
        </Link>
        <div className="flex items-center gap-6 text-sm text-slate-300">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`transition hover:text-white ${isActive ? "text-white" : ""}`}
              >
                {item.label}
              </Link>
            );
          })}
        </div>
        <Link href="/profile" className="rounded-md bg-brand px-4 py-2 text-sm font-medium text-white">
          Pro’ya geç
        </Link>
      </div>
    </nav>
  );
}
