# Insightagent

Cafeoi projesi için MVP odaklı ürün, geliştirme planı ve artık Next.js tabanlı web uygulaması bu repo altında tutuluyor.
Detaylı mimari, yol haritası ve aksiyon listesi için [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md) belgesini; sprint bazlı
backlog içinse [`docs/DELIVERY_BACKLOG.md`](docs/DELIVERY_BACKLOG.md) dosyasını inceleyebilirsiniz. Hızlı durum özeti ve öncelikli
adımlar için [`docs/TASK_SUMMARY.md`](docs/TASK_SUMMARY.md) dosyası güncel tutulur. Bulut dağıtımı ve ortam kontrolleri için
[`docs/CLOUD_DEPLOYMENT_CHECKLIST.md`](docs/CLOUD_DEPLOYMENT_CHECKLIST.md) rehberini kullanabilirsiniz.

## Monorepo Yapısı
- `app/` – Next.js 14 (App Router) tabanlı web/PWA istemcisi (fikir formu `/api/plan` endpoint’i ile konuşur).
- `app/ideas` – Fikir giriş formu, AI plan önizlemesi ve Supabase plan geçmişi listesi.
- `docs/` – Ürün vizyonu, proje planı ve teslimat backlog’u.
- `package.json` – Ortak bağımlılıklar (`next`, `react`, `@supabase/supabase-js`, `tailwindcss`).
- `supabase/` – Postgres şemasını oluşturan migration dosyaları.

## Hızlı Başlangıç
1. Bağımlılıkları yükleyin:
   ```bash
   npm install
   ```
   > Eğer `403 Forbidden` hatası alırsanız proxy ayarlarınızı veya `.npmrc` dosyasını güncellemek için [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) rehberine bakın. Depodaki `.npmrc`, varsayılan registry erişime kapandığında npmmirror üzerinden kurulum yapmaya yardımcı olur; mirror'ın Supabase paketlerini engellemesi halinde sadece `@supabase` scope'unu resmi registry'e yönlendiren ek kuralı da içerir.
2. Geliştirme sunucusunu başlatın:
   ```bash
   npm run dev
   ```
3. Tarayıcıdan [http://localhost:3000](http://localhost:3000) adresine giderek ana sayfa, fikir girişi, şablon ve profil sayfalarını
   görüntüleyin. Fikirler sayfasında formu doldurduktan sonra AI plan önizlemesini ve Supabase’te tutulan son plan geçmişini
   inceleyebilirsiniz.

> **Not:** Kısıtlı network ortamlarında `npm install` komutu paket kayıtlarına erişemeyebilir. Bu durumda Hostinger VPS üzerinde
> aynalama ya da `npm config set registry` ile alternatif registry kullanılması gerekir.

### Ortam Değişkenleri
- `NEXT_PUBLIC_SUPABASE_URL` – İstemcinin Supabase’e bağlanacağı URL.
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` – Tarayıcıdan Supabase çağrıları için anon anahtar.
- `SUPABASE_SERVICE_ROLE_KEY` – Sunucu tarafı kayıt işlemleri için service role anahtarı.
- `OPENAI_API_KEY` – `/api/plan` servisini gerçek AI çıktısı verecek şekilde yapılandırmak için gerekli anahtar.

Bu değişkenler tanımlı değilse `/api/plan` endpoint’i çalışmaya devam eder fakat fikir ve plan verileri Supabase’e yazılmaz ve AI planı üretilemez.
Yerel denemelerde isteğe `x-cafeoi-email`, `x-cafeoi-name` ve `x-cafeoi-plan` başlıklarını ekleyerek hangi profil adına kayıt oluşturulacağını kontrol edebilirsiniz.

## Sonraki Adımlar
- Supabase RLS tanımlarını ve günlük kullanım tetikleyicilerini ekleme.
- `/api/plan` endpoint’ini OpenAI entegrasyonu ile gerçek AI çıktısı üretir hale getirme ve plan geçmişini versiyonlayarak genişletme.
- n8n blueprint’lerini sürümlemek ve Hostinger VPS’e CI/CD kurmak.
- Expo mobil uygulaması için `apps/mobile` dizinini başlatmak.
- Kapalı beta kullanıcıları ile geri bildirim döngüsü kurma.
