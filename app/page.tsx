/**
 * Ana sayfa modülü; kullanıcıyı fikir girişi, şablonlar ve üyelik aksiyonlarına yönlendiren giriş ekranını oluşturur.
 */
import Link from "next/link";

const featureCards = [
  {
    title: "Yeni Fikir Yakala",
    description: "Problem, hedef kullanıcı ve çözümünü 3 adımda kaydet.",
    href: "/ideas"
  },
  {
    title: "AI Planını İncele",
    description: "OpenAI destekli proje planlarını mimari ve yol haritasıyla gör.",
    href: "/ideas"
  },
  {
    title: "Şablon Kütüphanesi",
    description: "Chatbot, Form-to-App ve Simple Booking paketlerini keşfet.",
    href: "/templates"
  }
];

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-12 px-6 py-16">
      <header className="flex flex-col gap-4">
        <span className="rounded-full bg-brand/20 px-4 py-1 text-sm text-brand-light">
          App Lab Agent ile güçlendirildi
        </span>
        <h1 className="text-4xl font-semibold md:text-5xl">Fikrini yaz, dakikalar içinde proje planını al.</h1>
        <p className="max-w-2xl text-lg text-slate-300">
          Cafeoi, fikir aşamasından yayına kadar tüm süreci otomatikleştiren AI destekli bir üretim hattı sunar.
          GitHub entegrasyonu, Vercel deploy’u ve hazır şablonları tek yerden yönet.
        </p>
        <div className="flex flex-wrap gap-4">
          <Link href="/ideas" className="rounded-md bg-brand px-6 py-3 text-base font-medium text-white">
            Yeni fikir oluştur
          </Link>
          <Link
            href="/templates"
            className="rounded-md border border-brand-light px-6 py-3 text-base font-medium text-slate-100"
          >
            Şablonları gör
          </Link>
        </div>
      </header>

      <section className="grid gap-6 md:grid-cols-3">
        {featureCards.map((card) => (
          <Link
            key={card.title}
            href={card.href}
            className="flex flex-col gap-2 rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg transition hover:border-brand"
          >
            <h3 className="text-xl font-semibold text-white">{card.title}</h3>
            <p className="text-sm text-slate-300">{card.description}</p>
            <span className="mt-auto text-sm text-brand-light">Detaylara git →</span>
          </Link>
        ))}
      </section>

      <section className="grid gap-8 rounded-2xl bg-slate-900/70 p-10 md:grid-cols-2">
        <div className="space-y-4">
          <h2 className="text-3xl font-semibold">Free vs Pro planları</h2>
          <p className="text-slate-300">
            Fikirlerini test etmeye ücretsiz başla, sınırsız üretim ve otomasyon entegrasyonları için Pro plana geç.
          </p>
          <ul className="space-y-2 text-sm text-slate-200">
            <li>✔︎ Free: Günde 1 fikir, şablon önizlemeleri</li>
            <li>✔︎ Pro: Sınırsız fikir, ZIP indirme, GitHub & Vercel entegrasyonları</li>
            <li>✔︎ Güvenli Stripe & Iyzico ödemeleri</li>
          </ul>
        </div>
        <div className="space-y-4 rounded-xl border border-slate-800 bg-slate-950/80 p-6">
          <h3 className="text-2xl font-semibold">Gelir Modeli</h3>
          <p className="text-sm text-slate-300">Aylık abonelik 5-10 USD / 200-300 TL bandında önerilir.</p>
          <div className="flex flex-col gap-3">
            <div className="rounded-lg bg-slate-900 px-4 py-3">
              <p className="text-xs uppercase tracking-wide text-brand-light">Free</p>
              <p className="text-2xl font-semibold text-white">0 ₺</p>
              <p className="text-xs text-slate-400">Günde 1 fikir</p>
            </div>
            <div className="rounded-lg bg-brand px-4 py-3">
              <p className="text-xs uppercase tracking-wide text-white">Pro</p>
              <p className="text-2xl font-semibold text-white">249 ₺</p>
              <p className="text-xs text-white/80">Sınırsız fikir + otomasyonlar</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
