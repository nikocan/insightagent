/**
 * AI proje planı üretimi için placeholder API; istemciden aldığı fikir girdilerine göre deterministik bir plan taslağı döndürür.
 */
import { NextResponse } from "next/server";
import { getServiceSupabaseClient } from "@/lib/supabase/server";
import type { SupabaseClient } from "@supabase/supabase-js";

interface PlanRequestBody {
  problem?: string;
  targetUser?: string;
  solution?: string;
}

interface PlanResponseBody {
  summary: string;
  architecture: string[];
  databaseSchema: { table: string; description: string }[];
  roadmap: string[];
  exportOptions: string[];
  persisted?: boolean;
  persistenceMessage?: string;
}

interface PlanHistoryItem {
  ideaId: number;
  createdAt: string;
  problem: string;
  targetUser: string;
  solution: string;
  plan?: PlanResponseBody & { createdAt?: string };
}

interface PlanHistoryResponseBody {
  items: PlanHistoryItem[];
  message?: string;
}

const MIN_TEXT_LENGTH = 12;

function buildSummary(problem: string, targetUser: string, solution: string): string {
  const trimmedProblem = problem.trim();
  const trimmedTarget = targetUser.trim();
  const trimmedSolution = solution.trim();

  return `Cafeoi, ${trimmedTarget.toLowerCase()} için ${trimmedProblem.toLowerCase()} sorununu ${trimmedSolution.toLowerCase()} yaklaşımıyla çözen bir AI destekli uygulama öneriyor.`;
}

function buildArchitecture(solution: string): string[] {
  const patterns = [
    "Next.js 14 + Tailwind ile web/PWA arayüzü",
    "Supabase Auth & Postgres ile kullanıcı ve fikir yönetimi",
    "OpenAI API ile dinamik proje planı üretimi",
    "n8n üzerinde GitHub/Vercel otomasyon akışları"
  ];

  if (solution.toLowerCase().includes("mobil")) {
    patterns.push("Expo (React Native) ile iOS & Android istemcileri");
  }

  return patterns;
}

function buildDatabaseSchema(): { table: string; description: string }[] {
  return [
    { table: "profiles", description: "Kullanıcı planı, profil ve faturalandırma bilgileri" },
    { table: "ideas", description: "Fikir soruları ve oluşturulma zamanları" },
    { table: "ai_plans", description: "AI çıktılarını saklayan mimari, şema ve yol haritası verileri" },
    { table: "templates", description: "Şablon meta bilgileri ve erişim seviyeleri" },
    { table: "usage_logs", description: "Günlük limit ve entegrasyon kullanım geçmişi" }
  ];
}

function buildRoadmap(): string[] {
  return [
    "Supabase şemasını ve RLS politikalarını uygulamaya alın",
    "Fikir formunu Supabase ve AI servisine bağlayın",
    "AI plan çıktısını şablon indirme & otomasyon entegrasyonlarıyla zenginleştirin",
    "Stripe/Iyzico ile Pro plan ödemelerini aktif edin",
    "PWA + mobil istemciler için dağıtım ve izleme kurulumunu tamamlayın"
  ];
}

function buildExportOptions(planSummary: string): string[] {
  const options = ["ZIP paketi oluştur", "GitHub deposu aç", "Vercel deploy tetikle"];
  if (planSummary.includes("mobil")) {
    options.push("Expo EAS build kuyruğunu başlat");
  }
  return options;
}

function validateBody(body: PlanRequestBody): asserts body is Required<PlanRequestBody> {
  if (!body.problem || !body.targetUser || !body.solution) {
    throw new Error("Zorunlu alanlar eksik");
  }

  const fields = [body.problem, body.targetUser, body.solution];
  const hasTooShortField = fields.some((field) => field.trim().length < MIN_TEXT_LENGTH);

  if (hasTooShortField) {
    throw new Error("Her cevap en az 12 karakter içermelidir");
  }
}

export async function POST(request: Request) {
  try {
    const body: PlanRequestBody = await request.json();
    validateBody(body);

    const summary = buildSummary(body.problem, body.targetUser, body.solution);
    const architecture = buildArchitecture(body.solution);
    const databaseSchema = buildDatabaseSchema();
    const roadmap = buildRoadmap();
    const exportOptions = buildExportOptions(summary);

    const response: PlanResponseBody = {
      summary,
      architecture,
      databaseSchema,
      roadmap,
      exportOptions
    };

    const supabase = getServiceSupabaseClient();

    if (supabase) {
      const persistenceResult = await persistPlanWithSupabase({
        request,
        supabase,
        idea: body as Required<PlanRequestBody>,
        plan: response
      });

      response.persisted = persistenceResult.persisted;
      response.persistenceMessage = persistenceResult.message;
    } else {
      response.persisted = false;
      response.persistenceMessage = "Supabase yapılandırması bulunamadığı için kayıt atlandı.";
    }

    return NextResponse.json(response);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Beklenmeyen bir hata oluştu";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}

export async function GET() {
  const supabase = getServiceSupabaseClient();

  if (!supabase) {
    const response: PlanHistoryResponseBody = {
      items: [],
      message: "Supabase yapılandırması eksik olduğu için plan geçmişi yüklenemedi."
    };

    return NextResponse.json(response);
  }

  try {
    const history = await fetchPlanHistory(supabase);
    return NextResponse.json(history);
  } catch (error) {
    console.error("Plan geçmişi alınamadı", error);
    const message = error instanceof Error ? error.message : "Plan geçmişi yüklenirken hata oluştu.";
    return NextResponse.json({ items: [], message }, { status: 500 });
  }
}

const DEFAULT_PROFILE_EMAIL = "demo@cafeoi.local";
const DEFAULT_PROFILE_NAME = "Cafeoi Demo";

interface PersistenceParams {
  request: Request;
  supabase: SupabaseClient;
  idea: Required<PlanRequestBody>;
  plan: PlanResponseBody;
}

async function persistPlanWithSupabase({ request, supabase, idea, plan }: PersistenceParams) {
  try {
    const { email, fullName, planOverride } = extractProfileMetadata(request);
    const profileId = await upsertProfile({ supabase, email, fullName, planOverride });
    const ideaId = await insertIdea({ supabase, profileId, idea });
    await insertPlan({ supabase, ideaId, plan });

    return {
      persisted: true,
      message: "Plan Supabase veritabanına kaydedildi."
    } as const;
  } catch (error) {
    console.error("Supabase kaydı sırasında hata", error);
    return {
      persisted: false,
      message: error instanceof Error ? error.message : "Plan Supabase'e kaydedilemedi."
    } as const;
  }
}

function extractProfileMetadata(request: Request) {
  const headers = request.headers;
  const email = headers.get("x-cafeoi-email") ?? DEFAULT_PROFILE_EMAIL;
  const fullName = headers.get("x-cafeoi-name") ?? DEFAULT_PROFILE_NAME;
  const planOverride = headers.get("x-cafeoi-plan") ?? undefined;

  return { email, fullName, planOverride };
}

interface UpsertProfileParams {
  supabase: SupabaseClient;
  email: string;
  fullName?: string;
  planOverride?: string;
}

async function upsertProfile({ supabase, email, fullName, planOverride }: UpsertProfileParams) {
  const payload: Record<string, string> = { email };

  if (fullName) {
    payload.full_name = fullName;
  }

  if (planOverride) {
    payload.plan = planOverride;
  }

  const { data, error } = await supabase
    .from("profiles")
    .upsert(payload, { onConflict: "email" })
    .select("id")
    .single();

  if (error) {
    throw new Error(`Profil oluşturulamadı: ${error.message}`);
  }

  return data.id as string;
}

interface InsertIdeaParams {
  supabase: SupabaseClient;
  profileId: string;
  idea: Required<PlanRequestBody>;
}

async function insertIdea({ supabase, profileId, idea }: InsertIdeaParams) {
  const { data, error } = await supabase
    .from("ideas")
    .insert({
      user_id: profileId,
      problem: idea.problem,
      target_user: idea.targetUser,
      solution: idea.solution,
      status: "planned"
    })
    .select("id")
    .single();

  if (error) {
    throw new Error(`Fikir kaydedilemedi: ${error.message}`);
  }

  return data.id as number;
}

interface InsertPlanParams {
  supabase: SupabaseClient;
  ideaId: number;
  plan: PlanResponseBody;
}

async function insertPlan({ supabase, ideaId, plan }: InsertPlanParams) {
  const { error } = await supabase.from("ai_plans").insert({
    idea_id: ideaId,
    summary: plan.summary,
    architecture: plan.architecture,
    database_schema: plan.databaseSchema,
    roadmap: plan.roadmap,
    export_options: plan.exportOptions
  });

  if (error) {
    throw new Error(`Plan kaydedilemedi: ${error.message}`);
  }
}

async function fetchPlanHistory(supabase: SupabaseClient): Promise<PlanHistoryResponseBody> {
  const { data, error } = await supabase
    .from("ideas")
    .select(
      `id, problem, target_user, solution, created_at, ai_plans (summary, architecture, database_schema, roadmap, export_options, created_at)`
    )
    .order("created_at", { ascending: false })
    .limit(10);

  if (error) {
    throw new Error(`Plan geçmişi alınamadı: ${error.message}`);
  }

  const items: PlanHistoryItem[] = (data ?? []).map((idea) => {
    const planRecord = Array.isArray(idea.ai_plans) ? idea.ai_plans[0] : null;

    return {
      ideaId: idea.id as number,
      createdAt: idea.created_at as string,
      problem: idea.problem as string,
      targetUser: idea.target_user as string,
      solution: idea.solution as string,
      plan: planRecord
        ? {
            summary: planRecord.summary as string,
            architecture: (planRecord.architecture ?? []) as string[],
            databaseSchema: (planRecord.database_schema ?? []) as { table: string; description: string }[],
            roadmap: (planRecord.roadmap ?? []) as string[],
            exportOptions: (planRecord.export_options ?? []) as string[],
            createdAt: planRecord.created_at as string
          }
        : undefined
    };
  });

  return {
    items,
    message: items.length === 0 ? "Henüz kayıtlı bir plan geçmişi bulunmuyor." : undefined
  };
}
