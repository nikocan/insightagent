/**
 * Supabase service rol anahtarıyla çalışan sunucu tarafı istemcisi; API route'ları aynı bağlantıyı paylaşarak
 * gereksiz bağlantı oluşumunu engeller ve yapılandırmayı ortam değişkenlerine dayandırır.
 */
import { createClient, type SupabaseClient } from "@supabase/supabase-js";

let cachedClient: SupabaseClient | null = null;
let isInitialized = false;

function readSupabaseConfig() {
  const url = process.env.SUPABASE_URL;
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!url || !serviceRoleKey) {
    return null;
  }

  return { url, serviceRoleKey };
}

export function getServiceSupabaseClient(): SupabaseClient | null {
  if (!isInitialized) {
    isInitialized = true;
    const config = readSupabaseConfig();

    if (!config) {
      console.warn("SUPABASE_URL veya SUPABASE_SERVICE_ROLE_KEY eksik olduğu için Supabase'e bağlanılmadı.");
      cachedClient = null;
    } else {
      cachedClient = createClient(config.url, config.serviceRoleKey, {
        auth: {
          autoRefreshToken: false,
          persistSession: false
        }
      });
    }
  }

  return cachedClient;
}
