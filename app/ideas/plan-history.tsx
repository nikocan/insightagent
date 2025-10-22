"use client";

/**
 * Plan geçmişi modülü; son oluşturulan fikir ve AI plan kayıtlarını listeleyip kullanıcıya hızlı geri dönüş sağlar.
 */
import { PlanHistoryItem } from "./types";

interface PlanHistoryProps {
  items: PlanHistoryItem[];
  isLoading: boolean;
  isRefetching: boolean;
  error?: string;
  infoMessage?: string;
  onRetry: () => void;
}

export function PlanHistory({ items, isLoading, isRefetching, error, infoMessage, onRetry }: PlanHistoryProps) {
  return (
    <section className="grid gap-4 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold text-white">Son planlar</h2>
          <p className="text-sm text-slate-300">
            Cafeoi fikirlerini kaydedip AI planlarıyla eşleştirilen son 10 giriş burada listelenir.
          </p>
        </div>
        <button
          type="button"
          onClick={onRetry}
          disabled={isRefetching}
          className="rounded-md border border-slate-700 px-3 py-2 text-xs font-medium text-slate-200 disabled:cursor-not-allowed"
        >
          {isRefetching ? "Yenileniyor..." : "Yenile"}
        </button>
      </header>

      {isLoading ? (
        <p className="text-sm text-slate-400">Plan geçmişi yükleniyor...</p>
      ) : error ? (
        <div className="rounded-lg border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-200">
          {error}
        </div>
      ) : items.length === 0 ? (
        <p className="text-sm text-slate-400">{infoMessage ?? "Henüz oluşturulmuş bir plan bulunmuyor."}</p>
      ) : (
        <ul className="grid gap-4">
          {items.map((item) => (
            <li key={item.ideaId} className="rounded-xl border border-slate-800 bg-slate-950/50 p-5">
              <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-xs uppercase tracking-wide text-brand-light">Fikir #{item.ideaId}</p>
                  <h3 className="text-lg font-semibold text-white">{item.problem}</h3>
                </div>
                <span className="text-xs text-slate-400">
                  {new Date(item.createdAt).toLocaleString("tr-TR", { dateStyle: "medium", timeStyle: "short" })}
                </span>
              </div>

              <dl className="mt-4 grid gap-3 text-sm text-slate-300 md:grid-cols-3">
                <div>
                  <dt className="font-semibold text-slate-200">Hedef kullanıcı</dt>
                  <dd>{item.targetUser}</dd>
                </div>
                <div>
                  <dt className="font-semibold text-slate-200">Çözüm yaklaşımı</dt>
                  <dd>{item.solution}</dd>
                </div>
                <div>
                  <dt className="font-semibold text-slate-200">Plan kaydı</dt>
                  <dd>{item.plan ? "Supabase'de saklandı" : "Plan henüz kaydedilmedi"}</dd>
                </div>
              </dl>

              {item.plan && (
                <div className="mt-4 grid gap-3 rounded-lg border border-slate-800 bg-slate-900/40 p-4 text-xs text-slate-200 md:grid-cols-2">
                  <div>
                    <p className="font-semibold text-slate-100">Mimari özet</p>
                    <ul className="mt-2 space-y-1">
                      {item.plan.architecture.slice(0, 3).map((line) => (
                        <li key={line}>• {line}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <p className="font-semibold text-slate-100">Yol haritası</p>
                    <ul className="mt-2 space-y-1">
                      {item.plan.roadmap.slice(0, 3).map((step) => (
                        <li key={step}>• {step}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
