/**
 * Şablon kütüphanesi sayfası; her template için açıklama, kullanım durumu ve erişim seviyesini listeler.
 */
const templates = [
  {
    slug: "chatbot",
    name: "Chatbot Asistan",
    description:
      "Kullanıcı sorularını OpenAI destekli olarak yanıtlayan ve Supabase knowledge base’i kullanan sohbet arayüzü.",
    access: "Pro"
  },
  {
    slug: "form-to-app",
    name: "Form-to-App",
    description:
      "Form girdilerini alıp otomatik frontend + backend kodu üreten tek tıkla deploy edilebilir paket.",
    access: "Pro"
  },
  {
    slug: "simple-booking",
    name: "Simple Booking",
    description:
      "Rezervasyon saatlerini yöneten, Stripe ödeme bağlantılarıyla entegre basit randevu sistemi.",
    access: "Free Önizleme"
  }
];

export default function TemplateLibraryPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-10 px-6 py-16">
      <header className="space-y-3">
        <h1 className="text-4xl font-semibold">Şablon kütüphanesi</h1>
        <p className="text-slate-300">
          MVP’ye başlamak için hazır blueprint’ler. Pro üyeler ZIP indirip GitHub depolarına aktarabilir.
        </p>
      </header>

      <section className="grid gap-6 md:grid-cols-3">
        {templates.map((template) => (
          <article
            key={template.slug}
            className="flex flex-col gap-3 rounded-2xl border border-slate-800 bg-slate-900/60 p-6"
          >
            <div>
              <span className="text-xs uppercase tracking-wide text-brand-light">{template.access}</span>
              <h2 className="text-xl font-semibold text-white">{template.name}</h2>
            </div>
            <p className="text-sm text-slate-300">{template.description}</p>
            <button type="button" className="mt-auto bg-slate-800 hover:bg-slate-700">
              İndir / Aktar (yakında)
            </button>
          </article>
        ))}
      </section>
    </main>
  );
}
