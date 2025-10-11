"use client";

/**
 * AI planı önizleme bileşeni; API’den dönen mimari, veritabanı şeması ve yol haritasını görsel olarak listeler.
 */
import { PlanResponse } from "./types";

interface PlanPreviewProps {
  plan: PlanResponse;
}

export function PlanPreview({ plan }: PlanPreviewProps) {
  return (
    <section className="grid gap-6 rounded-2xl border border-brand/40 bg-slate-900/50 p-8">
      <div className="space-y-3">
        <h2 className="text-2xl font-semibold text-brand-light">AI proje planı</h2>
        <p className="text-sm text-slate-200">{plan.summary}</p>
        {plan.persistenceMessage && (
          <p
            className={`text-xs font-medium ${
              plan.persisted ? "text-emerald-300" : "text-amber-300"
            }`}
          >
            {plan.persistenceMessage}
          </p>
        )}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <article className="rounded-xl border border-slate-800 bg-slate-950/60 p-5">
          <h3 className="text-lg font-semibold text-white">Mimari</h3>
          <ul className="mt-3 space-y-2 text-sm text-slate-300">
            {plan.architecture.map((item) => (
              <li key={item}>• {item}</li>
            ))}
          </ul>
        </article>

        <article className="rounded-xl border border-slate-800 bg-slate-950/60 p-5">
          <h3 className="text-lg font-semibold text-white">Veritabanı Şeması</h3>
          <ul className="mt-3 space-y-2 text-sm text-slate-300">
            {plan.databaseSchema.map((schema) => (
              <li key={schema.table}>
                <span className="font-medium text-slate-100">{schema.table}</span>: {schema.description}
              </li>
            ))}
          </ul>
        </article>
      </div>

      <article className="rounded-xl border border-slate-800 bg-slate-950/60 p-5">
        <h3 className="text-lg font-semibold text-white">5 Adımlık Yol Haritası</h3>
        <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm text-slate-300">
          {plan.roadmap.map((step) => (
            <li key={step}>{step}</li>
          ))}
        </ol>
      </article>

      <div className="flex flex-wrap gap-3">
        {plan.exportOptions.map((option) => (
          <button key={option} type="button" className="rounded-lg bg-slate-800 px-4 py-2 text-sm text-slate-100">
            {option} (yakında)
          </button>
        ))}
      </div>
    </section>
  );
}
