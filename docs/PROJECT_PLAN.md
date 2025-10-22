# Cafeoi MVP Project Plan

## 1. Vision & Value Proposition
Cafeoi, App Lab Agent altyapısından güç alan ve kullanıcıların yapay zeka destekli ürün fikirlerini hızlıca işleyip üretilebilir proje planlarına dönüştürmesini sağlayan bir platformdur. Web, PWA ve mobil (iOS, Android, iPad) yüzeyleriyle fikrin yakalanmasından geliştirilmesine kadar tüm süreci tek noktadan yönetmeyi hedefler. Gelir modeli üyelik aboneliğine dayanır (Free ve Pro planları).

## 2. Ürün Kapsamı (MVP)
### 2.1. Temel Kullanıcı Akışları
1. **Üye Olma & Profil Kurulumu**  
   - Google, Apple, SMS OTP ile kayıt.  
   - Free / Pro plan ayrımı.
2. **Fikir Girişi**  
   - Problem tanımı, hedef kullanıcı, çözüm yaklaşımı alanları.  
   - Kaydet → AI proje planı oluştur.
3. **AI Proje Planı Görüntüleme**  
   - Önerilen mimari (Frontend / AI Model / Database).  
   - Basit veritabanı şeması.  
   - 5 adımlık yol haritası.  
   - Dışa aktarma: ZIP indir, GitHub deposu oluştur, Vercel deploy tetikleme.
4. **Şablonlar**  
   - Chatbot, Form-to-App, Simple Booking.
5. **Profil & Üyelik Yönetimi**  
   - Plan yükseltme, Stripe & Iyzico ödeme akışı.  
   - Faturalandırma geçmişi.

### 2.2. Üyelik Kısıtları
| Plan | Fikir Limiti | Şablon Erişimi | Dışa Aktarma |
| --- | --- | --- | --- |
| Free | Günde 1 fikir | Önizleme | Yok |
| Pro | Sınırsız | Tam erişim + indirilebilir | GitHub, Vercel entegrasyonları |

## 3. Teknik Mimari
### 3.1. Genel Bakış
- **Frontend Web**: Next.js 14 (App Router) + Tailwind CSS, PWA yapılandırması.  
- **Mobil**: Expo (React Native) + React Query.  
- **Backend**: Supabase (Auth + Postgres + Edge Functions).  
- **AI Katmanı**: OpenAI API (gerekirse App Lab Agent orkestrasyonu).  
- **Otomasyon**: n8n ile GitHub, Vercel, Hostinger VPS tetikleyicileri.  
- **CI/CD**: GitHub Actions → Vercel Deploy (web), Expo EAS (mobil).  
- **Barındırma**: Web → Vercel, API & otomasyon → Hostinger VPS (Docker), Mobil → App Store & Google Play.

### 3.2. Modüller
1. **Auth & Billing Module**  
   - Supabase Auth provider’ları.  
   - Pro plan için Stripe + Iyzico webhook dinleyicileri (Hostinger VPS üzerinde).  
   - Kullanıcı planı Supabase profil tablosunda saklanır.
2. **Idea Intake Module**  
   - Form state yönetimi (React Hook Form).  
   - Günlük kullanım limiti kontrolü (Edge Function + RLS policy).
3. **AI Plan Generator Module**
   - Prompt şablonları (Supabase storage).
   - OpenAI API çağrısı (günlük kota kontrolü).
   - Sonuçların Markdown + JSON formatında saklanması.
   - Geçici olarak `/api/plan` endpoint’i deterministik bir taslak döndürüyor; gerçek entegrasyon bu katmanı genişletecek.
4. **Template Library Module**  
   - Supabase storage’dan şablon metadata + asset indirme.  
   - Pro kullanıcılara ZIP paket hazırlama (Serverless function).
5. **Export & Automation Module**  
   - GitHub repo oluşturma (GitHub App + n8n flow).  
   - Vercel deploy tetikleme (Vercel API).  
   - Hostinger VPS üzerinde CLI komutlarını çalıştırma (SSH + n8n).
6. **Analytics & Feedback Module**  
   - Mixpanel/Amplitude entegrasyonu.  
   - Kullanıcı memnuniyeti anketi.

## 4. Veri Modeli (Supabase)
- `profiles` (uuid, email, name, plan, billing_status, created_at).  
- `ideas` (id, user_id, problem, target_user, solution, status, created_at).  
- `ai_plans` (id, idea_id, architecture_json, db_schema_json, roadmap_json, export_links).  
- `templates` (id, slug, name, description, access_level, assets_url).  
- `usage_logs` (id, user_id, action, metadata, occurred_at).  
- `payments` (id, user_id, provider, amount, currency, status, invoice_url, created_at).

Row-Level Security (RLS) tüm kullanıcı tablolarda zorunlu; plan limitleri `usage_logs` üzerinden takip edilir.

## 5. Yol Haritası
### 5.1. Hazırlık (Hafta 0)
- [ ] Gereksinimlerin doğrulanması, kullanıcı senaryoları.  
- [ ] Tasarım sistemi (Figma) + bileşen kütüphanesi.  
- [ ] Domain ve DNS Hostinger üzerinden Vercel & Supabase’e yönlendirme kontrolü.

### 5.2. Sprint 1 (Hafta 1-2): Auth & Fikir Akışı
- [ ] Supabase projesinde şema oluşturma, RLS yazma.  
- [ ] Next.js’de Auth + profil onboarding.  
- [ ] Günlük fikir limiti kontrolü.  
- [ ] AI prompt altyapısı (OpenAI API anahtarı güvenli saklama).  
- [ ] İlk AI plan çıktısı (metin + JSON).

### 5.3. Sprint 2 (Hafta 3-4): Şablonlar & Export
- [ ] Şablon kartları, filtreleme, detay sayfası.  
- [ ] Pro plan kullanıcılarına ZIP üretimi.  
- [ ] GitHub & Vercel entegrasyonlarını n8n üzerinden tanımlama.  
- [ ] Hostinger VPS’de otomasyon servisinin containerize edilmesi.

### 5.4. Sprint 3 (Hafta 5-6): Mobil & Ödeme
- [ ] Expo uygulaması, Supabase auth bağlama.  
- [ ] Fikir oluşturma ve plan görüntüleme mobil uyarlaması.  
- [ ] Stripe + Iyzico entegrasyonları, webhook doğrulama.  
- [ ] Plan yükseltme UI ve faturalandırma kayıtlarının gösterimi.

### 5.5. Sprint 4 (Hafta 7-8): Performans & Yayın
- [ ] PWA optimizasyonu, Lighthouse >= 90.  
- [ ] Analytics ve hata takip (Sentry).  
- [ ] Güvenlik testi (rate limit, abuse prevention).  
- [ ] Beta kullanıcı testi, geri bildirim döngüsü.  
- [ ] App Store / Google Play gönderimleri, Vercel prod yayın.

## 6. Operasyonel Kontroller
- **DevOps**: GitHub Actions → lint, test, build.  
- **Sürümleme**: Semantik versiyonlama (`web@v1.0.0`, `mobile@1.0.0`).  
- **Monitoring**: Supabase logs, Vercel analytics, n8n flow logları.  
- **Dokümantasyon**: README güncellemeleri, API referansları (Docusaurus?).

## 7. Açık Aksiyon Listesi
1. Supabase’de şema ve RLS politikalarını IaC (SQL migration) olarak hazırlamak.  
2. OpenAI API kullanım metrikleri için kota dashboard’u oluşturmak.  
3. n8n flow’ları için Hostinger VPS’de Docker Compose setup’ı.  
4. Stripe + Iyzico entegrasyonlarını aynı kullanıcı tablosuna bağlayacak unify layer.  
5. Mobil uygulamada offline cache (React Query persist).  
6. Şablon ZIP üretimi için Node tabanlı CLI (VPS).  
7. AI çıktılarının kalite değerlendirmesi için kullanıcı geri bildirim döngüsü.

## 8. Riskler & Önlemler
- **AI Çıktı Kalitesi**: Prompt tuning + kullanıcı geri bildirim mekanizması.  
- **Ödeme Uyumları**: PCI DSS uyumu, test kartları, webhook güvenliği.  
- **Skalalama**: Supabase limitleri → gerektiğinde dedicated plan veya Prisma + kendi Postgres’e geçiş.  
- **Mobil Store Onayları**: App Store yönergelerine uyum, privacy policy dokümantasyonu.  
- **Veri Gizliliği**: Kullanıcı fikirlerinin sadece kullanıcılara açık olması, paylaşım izinleri.

## 9. Sonraki Adımlar
1. `docs/` klasöründe teknik dokümantasyonu genişletmek (API sözleşmeleri, UI wireframe’leri).  
2. Supabase migration dosyalarını oluşturup depo içine almak.  
3. Next.js ve Expo projelerini başlatmak, temel UI scaffold’u kurmak.  
4. Otomasyon için n8n blueprint’lerini JSON olarak versiyonlamak.  
5. İlk kapalı beta için 20 kullanıcı adayı belirlemek ve geri bildirim sürecini tasarlamak.

