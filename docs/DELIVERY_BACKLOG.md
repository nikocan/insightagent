# Cafeoi MVP Delivery Backlog

Bu belge, `docs/PROJECT_PLAN.md` içindeki yol haritasını geliştirilebilir iş kalemlerine dönüştürür. Önceliklendirme `P0` (kritik) → `P2` (iyi olur) şeklindedir.

## Sprint 1 – Auth & Fikir Akışı
- [ ] **P0** Supabase şema migration dosyaları (profiles, ideas, ai_plans, usage_logs, payments) — `0001_initial_schema.sql` temel tabloları ekledi, RLS ve trigger adımları beklemede.
- [ ] **P0** Supabase Auth provider konfigürasyonu (Google, Apple, OTP).
- [ ] **P0** RLS politikaları ve günlük kullanım limit Edge Function’ı.
- [ ] **P1** OpenAI API çağrısını yapan Next.js Route Handler (`app/api/plan/route.ts`).
- [x] **P2** Idea formu için deterministik plan taslağı üreten geçici API (`/api/plan`).
- [x] **P1** Idea formunun bu API’ye bağlanması ve sonuçların Supabase’e kaydedilmesi.

## Sprint 2 – Şablonlar & Export
- [ ] **P0** Supabase storage’da şablon metadata yönetimi.
- [ ] **P0** Pro üyelik kontrolü ile ZIP paket üretimi için Node tabanlı servis.
- [ ] **P1** n8n flow’ları için JSON blueprint’lerin versiyonlanması.
- [ ] **P1** GitHub & Vercel entegrasyonlarını tetikleyen API katmanı.

## Sprint 3 – Ödeme & Mobil
- [ ] **P0** Stripe & Iyzico ödeme akışı ve webhook doğrulaması.
- [ ] **P0** Kullanıcı plan yükseltme UI’ının canlı ödeme durumu ile senkronize edilmesi.
- [ ] **P1** Expo mobil uygulamasının fikir oluşturma ekranı.
- [ ] **P2** Mobilde offline cache (React Query persist).

## Sprint 4 – Yayın & Operasyon
- [ ] **P0** PWA yapılandırması ve Lighthouse optimizasyonu.
- [ ] **P0** Sentry + Amplitude entegrasyonları.
- [ ] **P1** App Store / Google Play gönderim hazırlıkları.
- [ ] **P2** Beta kullanıcı geri bildirim otomasyonları (n8n + Supabase).

## Süreç İyileştirmeleri
- [ ] **P0** CI/CD pipeline (lint, test, build) GitHub Actions.
- [ ] **P1** Kod standartları ve PR template’i.
- [ ] **P1** Teknik dokümantasyon için Docusaurus kurulumu.
