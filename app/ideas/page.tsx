"use client";

/**
 * Fikir giriş sayfası; kullanıcıdan problem, hedef kitle ve çözüm bilgisini toplayarak AI planı için temel veriyi hazırlar.
 * Aynı zamanda Supabase'te saklanan son plan geçmişini React Query ile yükleyip kullanıcıya sunar.
 */
import { FormEvent, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { PlanPreview } from "./plan-preview";
import { PlanHistory } from "./plan-history";
import { PlanHistoryResponse, PlanResponse } from "./types";

interface IdeaFormData {
  problem: string;
  targetUser: string;
  solution: string;
}

export default function IdeaCapturePage() {
  const [formData, setFormData] = useState<IdeaFormData>({
    problem: "",
    targetUser: "",
    solution: ""
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [generatedPlan, setGeneratedPlan] = useState<PlanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const {
    data: historyData,
    error: historyError,
    isLoading: isHistoryLoading,
    isRefetching: isHistoryRefetching,
    refetch: refetchHistory
  } = useQuery<PlanHistoryResponse, Error>({
    queryKey: ["plan-history"],
    queryFn: fetchPlanHistory,
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60
  });

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setError(null);
    setGeneratedPlan(null);

    try {
      const response = await fetch("/api/plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const payload = (await response.json()) as { error?: string };
        throw new Error(payload.error ?? "Plan oluşturulamadı");
      }

      const plan = (await response.json()) as PlanResponse;
      setGeneratedPlan(plan);
      void refetchHistory();
    } catch (apiError) {
      const message = apiError instanceof Error ? apiError.message : "Bilinmeyen bir hata oluştu";
      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-10 px-6 py-16">
      <header className="space-y-3">
        <h1 className="text-4xl font-semibold">Yeni fikir oluştur</h1>
        <p className="text-slate-300">
          Aşağıdaki üç soruyu yanıtla; Cafeoi fikrini AI ile analiz edip birkaç dakika içinde proje planı oluşturacak.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="grid gap-6 rounded-2xl border border-slate-800 bg-slate-900/70 p-8">
        <label className="grid gap-2">
          <span className="text-sm font-semibold text-slate-200">Problem nedir?</span>
          <textarea
            required
            rows={4}
            className="rounded-lg border border-slate-700 bg-slate-950/60 px-4 py-3 text-sm text-slate-100 focus:border-brand focus:outline-none"
            placeholder="Örn. Serbest çalışanlar için teklif oluşturma süreci çok zaman alıyor."
            value={formData.problem}
            onChange={(event) => setFormData((prev) => ({ ...prev, problem: event.target.value }))}
          />
        </label>

        <label className="grid gap-2">
          <span className="text-sm font-semibold text-slate-200">Hedef kullanıcı kim?</span>
          <textarea
            required
            rows={3}
            className="rounded-lg border border-slate-700 bg-slate-950/60 px-4 py-3 text-sm text-slate-100 focus:border-brand focus:outline-none"
            placeholder="Örn. Tasarım ve yazılım alanında freelance çalışan profesyoneller."
            value={formData.targetUser}
            onChange={(event) => setFormData((prev) => ({ ...prev, targetUser: event.target.value }))}
          />
        </label>

        <label className="grid gap-2">
          <span className="text-sm font-semibold text-slate-200">Nasıl çözmek istiyorsun?</span>
          <textarea
            required
            rows={3}
            className="rounded-lg border border-slate-700 bg-slate-950/60 px-4 py-3 text-sm text-slate-100 focus:border-brand focus:outline-none"
            placeholder="Örn. Kullanıcı girdilerini alıp otomatik teklif PDF’i üreten bir AI asistanı."
            value={formData.solution}
            onChange={(event) => setFormData((prev) => ({ ...prev, solution: event.target.value }))}
          />
        </label>

        <button type="submit" disabled={isSubmitting} className="disabled:cursor-not-allowed disabled:bg-brand/50">
          {isSubmitting ? "Plan hazırlanıyor..." : "AI planını oluştur"}
        </button>
      </form>

      {error && (
        <div className="rounded-lg border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-200">{error}</div>
      )}

      {generatedPlan && <PlanPreview plan={generatedPlan} />}

      <PlanHistory
        items={historyData?.items ?? []}
        infoMessage={historyData?.message}
        isLoading={isHistoryLoading}
        isRefetching={isHistoryRefetching}
        error={historyError?.message}
        onRetry={() => {
          void refetchHistory();
        }}
      />
    </main>
  );
}

async function fetchPlanHistory(): Promise<PlanHistoryResponse> {
  const response = await fetch("/api/plan");

  if (!response.ok) {
    const payload = (await response.json().catch(() => ({}))) as { message?: string };
    throw new Error(payload.message ?? "Plan geçmişi alınamadı");
  }

  return (await response.json()) as PlanHistoryResponse;
}
