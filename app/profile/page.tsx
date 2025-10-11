/**
 * Profil ve üyelik sayfası; kullanıcının plan durumunu, faturalandırma geçmişi özetini ve yükseltme CTA’sını gösterir.
 */
const invoices = [
  { id: "INV-1001", amount: "249 ₺", status: "Ödendi", date: "04.06.2024" },
  { id: "INV-1000", amount: "249 ₺", status: "Ödendi", date: "04.05.2024" }
];

export default function ProfilePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-10 px-6 py-16">
      <header className="space-y-3">
        <h1 className="text-4xl font-semibold">Profil & Üyelik</h1>
        <p className="text-slate-300">
          Plan durumunu yönet, ödeme yöntemlerini güncelle ve fatura geçmişini incele.
        </p>
      </header>

      <section className="grid gap-6 rounded-2xl border border-slate-800 bg-slate-900/70 p-8">
        <div className="flex flex-col gap-1">
          <span className="text-sm uppercase tracking-wide text-brand-light">Aktif Plan</span>
          <h2 className="text-2xl font-semibold text-white">Pro (Ay bazlı)</h2>
          <p className="text-sm text-slate-300">Sınırsız fikir üretimi ve tüm entegrasyonlara erişim.</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button type="button">Planı yönet</button>
          <button type="button" className="bg-slate-800 hover:bg-slate-700">
            Ödeme yöntemleri
          </button>
        </div>
      </section>

      <section className="grid gap-4 rounded-2xl border border-slate-800 bg-slate-900/70 p-8">
        <header>
          <h2 className="text-xl font-semibold text-white">Fatura geçmişi</h2>
          <p className="text-sm text-slate-400">Stripe & Iyzico ödemeleri tek listede görüntülenir.</p>
        </header>
        <div className="overflow-hidden rounded-xl border border-slate-800">
          <table className="min-w-full divide-y divide-slate-800 text-left text-sm">
            <thead className="bg-slate-950/80 text-slate-300">
              <tr>
                <th className="px-4 py-3 font-medium">Fatura #</th>
                <th className="px-4 py-3 font-medium">Tutar</th>
                <th className="px-4 py-3 font-medium">Durum</th>
                <th className="px-4 py-3 font-medium">Tarih</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-200">
              {invoices.map((invoice) => (
                <tr key={invoice.id}>
                  <td className="px-4 py-3">{invoice.id}</td>
                  <td className="px-4 py-3">{invoice.amount}</td>
                  <td className="px-4 py-3">{invoice.status}</td>
                  <td className="px-4 py-3">{invoice.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
