/**
 * Fikir formu ve AI planı arasındaki veri alışverişi için istemci tarafında kullanılan tip tanımları.
 */
export interface PlanResponse {
  summary: string;
  architecture: string[];
  databaseSchema: { table: string; description: string }[];
  roadmap: string[];
  exportOptions: string[];
  persisted?: boolean;
  persistenceMessage?: string;
}

export interface PlanHistoryItem {
  ideaId: number;
  createdAt: string;
  problem: string;
  targetUser: string;
  solution: string;
  plan?: PlanResponse & { createdAt?: string };
}

export interface PlanHistoryResponse {
  items: PlanHistoryItem[];
  message?: string;
}
