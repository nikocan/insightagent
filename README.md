# InsightAgent Ürün Vizyonu

InsightAgent, markaların, üreticilerin ve ajansların tek panelden ürün yönetimi, pazar içgörüsü, reklam üretimi ve tedarik akışlarını uçtan uca yönetmesini sağlayan yapay zekâ destekli bir platformdur. Aşağıda ürün vizyonu, ana modüller ve teknik akışlara dair kapsamlı çerçeve sunulmaktadır.

## İçindekiler
1. [Değer Önerisi](#1-değer-önerisi)
2. [Ana Modüller](#2-ana-modüller)
3. [Yapay Zekâ Akışları](#3-yapay-zekâ-akışları)
4. [Bilgi Mimarisi & Ekranlar](#4-bilgi-mimarisi--ekranlar)
5. [Veri Şeması](#5-veri-şeması-yüksek-seviye)
6. [UI/UX Tasarım İlkeleri](#6-uiux-tasarım-ilkeleri)
7. [Paketler & Konumlandırma](#7-paketler--konumlandırma)
8. [Satın Almaya Yönlendirme](#8-satın-almaya-yönlendirme-buy-flow)
9. [Güvenlik & Uyumluluk](#9-güvenlik--uyumluluk)
10. [Ölçüm & KPI’lar](#10-ölçüm--kpilar)
11. [Örnek Kullanıcı Akışı](#11-örnek-kullanıcı-akışı)
12. [Entegrasyon Ekosistemi](#12-entegrasyon-ekosistemi)
13. [Hedef Personalar & Kullanım Senaryoları](#13-hedef-personalar--kullanım-senaryoları)
14. [Ürün İlkeleri & Deneyim Rehberi](#14-ürün-ilkeleri--deneyim-rehberi)
15. [Teknik Mimari](#15-teknik-mimari)
16. [Veri Yönetişimi & Kalite Süreçleri](#16-veri-yönetişimi--kalite-süreçleri)
17. [Onboarding & Eğitim Yolculuğu](#17-onboarding--eğitim-yolculuğu)
18. [GTM & Büyüme Stratejisi](#18-gtm--büyüme-stratejisi)
19. [Yol Haritası (12 Ay)](#19-yol-haritası-12-ay)
20. [Ek: Örnek API & Otomasyon Senaryoları](#20-ek-örnek-api--otomasyon-senaryoları)
21. [Backend Uygulaması & Kurulum](#21-backend-uygulaması--kurulum)
22. [Modüler API Yüzeyi](#22-modüler-api-yüzeyi)

## 1. Değer Önerisi
- **Tek Ekran Deneyimi:** Ürünlerin fiyatı, teknik özellikleri, rakipleri, satış tahmini, pazar payı, kanal dağılımı ve müşteri duygu analizi saniyeler içinde erişilebilir.
- **Otomatik Pazarlama Üretimi:** Reklam/SEO stratejisi, metin ve görsel/video varlıkları ile kampanya önerileri otomatikleşir.
- **Satın Alma Yönlendirme:** Tedarikçi bulma, RFQ açma ve satın alma karar akışları “tek tuşla” tetiklenir.

## 2. Ana Modüller
### 2.1 Ürün Zekâsı (Product Intelligence)
- **Global Fiyatlaştırma:** Amazon, Trendyol, Hepsiburada, N11, Alibaba/AliExpress, Google Shopping, Etsy ve benzeri kanallardan gerçek zamanlı fiyat ve stok sinyalleri.
- **Teknik Özellik Haritalama:** Ürün sayfalarındaki dağınık metinlerden standart özellik şeması (INCI, watt, volt, boyut, hacim, sertifikalar vb.).
- **Satış/Popülarite Skoru:** Kategori sırası, yorum sayısı, tarihsel fiyat, stok sinyalleri ve arama trendleri birleşimiyle heuristik + ML tabanlı skor.
- **Rakip Haritası:** Benzer veya ikame ürün gruplarını, marka ve ölçek karşılaştırmalarını gösterir.
- **Regülasyon Kütüphanesi:** MoCRA, EU CPNP, ÜTS/GS1 gibi regülasyonlara uygun etiket kontrol listeleri.
- **Operasyon Akışı:**
  1. Kanal entegrasyonları ve scraping botları ile ham veri toplama.
  2. Kimlik eşleme ve ürün normalizasyonu sonrası kategori modellerine besleme.
  3. Fiyat, stok ve satış skorları panoda gerçek zamanlı olarak güncellenir; eşik aşımı uyarı olarak gönderilir.

### 2.2 Pazar & İçgörü (Market Insight)
- **Yorum/Duygu Analizi:** Şikâyet temaları, övgüler, kalite, ambalaj ve lojistik sorunlarının ortaya çıkarılması.
- **Anahtar Kelime ve SEO Madenciliği:** Short/long-tail keyword setleri, zorluk skoru, fırsat puanı ve çok dilli öneriler.
- **Trend Radar:** Sosyal medya (X, TikTok, Instagram, Reddit) ve haberlerden ürün/niş bazlı erken uyarı sinyalleri.
- **Fiyat Elastikiyeti & Konumlandırma:** Tavsiye fiyat aralıkları ve premium/ekonomik strateji önerileri.
- **İçgörü Teslimi:** İçgörü kartları “gözden geçir” adımıyla doğrulanır; onaylanan kartlar Slack/Teams’e otomatik gönderilir.

### 2.3 Reklam & İçerik Stüdyosu (Ad Studio)
- **Reklam Metni Üretimi:** Platform ve hedef kitleye göre başlık, birincil metin, CTA ve A/B varyantları.
- **Görsel/Video Şablonları:** Marka renkleriyle otomatik kompozitler; IG, TikTok, Facebook, X, Pinterest ve Amazon için boyutlandırmalar.
- **Anahtar Görsel/Metin Denetimi:** Regülasyon uyumsuz iddialara karşı uyarılar ve “claim check”.
- **Planla & Yayınla:** Meta, TikTok, Google ve Amazon Creative entegrasyonları.
- **Otomatik Uyum Testi:** Platformlara özel metin uzunluğu, safe-zone ve logo konumu validasyonu.
- **Çıktı Yönetimi:** Her kreatif varyantı versiyonlanır, performans metriği ile eşleştirilir ve “önerilen yeniden kullanım” etiketi alır.

### 2.4 Satın Alma & Tedarik (Sourcing)
- **Tedarikçi Bulucu:** Ürün/hammadde/ambalaj için global toptancı ve üretici listesi, MOQ ve teslim süreleri.
- **RFQ Akışı:** Tek formdan birden fazla tedarikçiye teklif talebi gönderip fiyat/lead time karşılaştırma.
- **Satın Alma Asistanı:** Resmi mağaza/dağıtıcı linkleri, kargo/vergilendirme tahmini ve birim maliyet simülasyonu.
- **Süreç Otomasyonu:** Onaylanan teklif, ERP’ye PO olarak aktarılır; teslimat tarihine göre yeniden sipariş hatırlatıcısı tetiklenir.

### 2.5 Raporlama & Paylaşım
- **Proje Klasörleri:** Ürün bazlı çalışma dosyaları, notlar, versiyonlar.
- **Yatırımcı/Patron Özeti:** Pazar özeti, fiyat haritası, SWOT ve kampanya planlarını içeren PDF veya deck çıktısı.
- **API & Webhook:** ERP/CRM/Amazon/Meta Ads entegrasyonlarıyla içgörü aktarımı.
- **Paylaşım Katmanı:** Ekip içi yorumlama, sürüm karşılaştırma ve müşteriyle paylaşılabilir link yönetimi.

## 3. Yapay Zekâ Akışları
1. Çok kaynaklı toplama → temizleme → varlık eşleme (entity resolution).
2. Özellik çıkarma (NER + şema eşleştirme): "Kapasite=150 ml", "Menthol %3" gibi.
3. Fiyat normalizasyonu: Para birimi, KDV/vergi ve birim fiyat uyarlaması.
4. Satış tahmini: Kategori bazlı XGBoost + sinyal füzyonu.
5. Duygu/özet: Yorum kümeleri için konu modelleme ve özetleme.
6. Keyword generator: Çok dilli (TR/EN/ES) SEM intent kümeleri.
7. Reklam kreatif üretimi: Metin ve görsel kompozit, otomatik boyutlandırma.
8. Risk/claim denetimi: Regülasyon kurallarıyla prompt guard.
- **Model İzleme:** Drift, veri dengesizliği ve performans metrikleri (MAPE, ROUGE, BLEU) dashboard üzerinden takip edilir.
- **Human-in-the-loop:** Kritik karar noktalarında uzman onayı zorunlu; geri bildirimler sürekli öğrenme kuyruğuna aktarılır.

## 4. Bilgi Mimarisi & Ekranlar
- **Giriş/Üyelik:** Email/Telefon OTP, Google/Apple, opsiyonel 2FA.
- **Dashboard:** Hızlı arama, son projeler, "Bugünün içgörüsü" kartları.
- **Ürün Araştır:** Arama → Ürün kartı (fiyat eğrisi, satış skoru, rakipler, özellikler, yorum ısı haritası).
- **İçgörü Stüdyosu:** Keyword, trend ve rekabet boşluklarına ilişkin öneriler.
- **Ad Studio:** Brief → Metin → Görsel/Video şablonu → Yayın.
- **Satın Alma:** Tedarikçi listesi → RFQ → Karşılaştırma.
- **Raporlar:** PDF/Deck oluşturma ve paylaşım.
- **Ayarlar/Entegrasyonlar:** Marketplace ve reklam entegrasyonları, para birimi/vergi profili, ekip rolleri.
- **Insight-Aside:** Sağ panel, bağlamsal öneriler, uyarılar ve “son alınan aksiyonlar” logunu gösterir.

## 5. Veri Şeması (Yüksek Seviye)
```
products(id, gtin/ean, upc, brand, title, category, specs_json, images[])
offers(id, product_id, channel, seller, price, currency, stock, ship_from, last_seen_at)
reviews(id, product_id, source, rating, text, lang, date, sentiment, topics[])
keywords(id, product_id, term, intent, volume, difficulty, cpc_est)
insights(product_id, sales_score, trend_score, price_elasticity, SWOT_json)
suppliers(id, name, country, moq, lead_time, contact)
rfqs(id, product_id, status, quotes[])
creatives(id, product_id, copy, assets[], sizes[], channels[])
reports(id, product_id, pdf_url, created_by)
```
- **Genişletilebilirlik:** Her tabloya `source_metadata` JSONB alanı eklenerek veri kökeni ve güven skoru tutulur.
- **Performans:** OLAP sorguları için `insights`, `offers` ve `reviews` üzerinde yıldız şema özet tabloları oluşturulur.

## 6. UI/UX Tasarım İlkeleri
- **Renk Paleti:** Midnight Navy (#0B1532), Electric Blue (#3A86FF), Emerald (#00A884), Slate (#64748B), arka plan dark #0A0A0A / light #F8FAFC.
- **Tipografi:** Inter ve Poppins.
- **Yerleşim:** Kart bazlı layout, sabit başlık bar, sol navigasyon, sağda "insight-aside".
- **Responsif Kırılımlar:**
  - Mobil: Alttan beşli tab (Araştır, İçgörü, Stüdyo, Satın Al, Profil).
  - iPad: Sol mini navigasyon + iki sütun kart ızgara.
  - Masaüstü: Üç sütun, detay panelleri slide-over.
- **Erişilebilirlik:** Renk kontrastı WCAG AA, klavye navigasyonu ve ekran okuyucu etiketleri zorunlu.
- **Mikro Etkileşimler:** Lottie animasyonlu yükleme, insight kartı hover state’leri ve başarı toast’ları.

## 7. Paketler & Konumlandırma
1. **Başlangıç (Starter):** 100 ürün/ay, temel fiyat & yorum analizi, temel keyword listesi, Ad Studio Lite (metin + 5 sabit şablon), tek sayfa PDF rapor, tek kullanıcı.
2. **Orta Seviye (Pro):** Gelişmiş fiyat & satış sinyali modeli, kapsamlı duygu analizi, Keyword & Trend Radar, Ad Studio Pro (otomatik boyutlandırma, 20 şablon, A/B), çoklu kullanıcı & rol, RFQ modülü, tedarikçi veritabanı, API/Webhook.
3. **Full Donanım (Enterprise):** Özel veri konektörleri, kategoriye özgü ML modeli, SSO, SLA, özel KPI panoları, çoklu iş birimi/ülke, özel regülasyon kuralları, veri ihracı, özel raporlar.

> Fiyatlama için TR/US pazarına uygun kredi bazlı sorgu modeli + koltuk bazlı kullanıcı lisansı önerilir.
- **Add-on’lar:** Veri zenginleştirme paketleri, özel eğitim seansları, profesyonel hizmetler (kategori modelleme, sistem entegrasyonu).

## 8. Satın Almaya Yönlendirme (Buy Flow)
- **"Nereden Al?":** Resmi distribütör ve marketplace mağazalarından fiyat/teslim karşılaştırmaları.
- **RFQ Tek Tuş:** Ürün özellikleri otomatik doldurulur, tedarikçilere mail/API, teklifler tabloda.
- **Satın Alma Asistanı:** MOQ, navlun, kur ve vergi varsayımlarıyla birim maliyet simülasyonu ve önerilen sipariş miktarı.
- **Performans Ölçümü:** RFQ dönüş süresi, teklif sayısı ve maliyet tasarrufu, satın alma raporunda haftalık olarak toplanır.

## 9. Güvenlik & Uyumluluk
- OAuth 2.0, SSO, RBAC.
- PII için anonimizasyon veya AES-256 ile at-rest, TLS ile in-transit şifreleme.
- Log ve izlenebilirlik, içgörü “explain” penceresi.
- Robots.txt uyumu, yasal scraping hız sınırları, claim kontrolü.
- **Uyumluluk Sertifikaları:** ISO 27001 yol haritası, SOC 2 Type II hazırlığı, veri depolama lokasyonları GDPR uyumlu.
- **Olay Müdahalesi:** 24 saat içinde kök neden analizi ve müşteri bilgilendirme prosedürü.

## 10. Ölçüm & KPI’lar
- Ürün başına pazara çıkış süresi kısalması.
- Reklam CPA/CAC düşüşü ve ROAS artışı.
- Satın alma maliyeti tasarrufu.
- İçgörü ve kreatif üretiminde işlem başına zaman kazanımı.

## 11. Örnek Kullanıcı Akışı
1. Ürün adını/GTIN’i girer → 3 saniyede fiyat haritası + satış skoru + ana rakipler.
2. "Kampanya oluştur" → Hedef kitle seçimi → Metin + 3 görsel otomatik → TikTok ve Instagram’a tek tuşla yayın.
3. "Nereden alırım?" → Distribütör listesi → RFQ gönderimi → Teklif karşılaştırma.
- **Başarı Ölçümü:** Bu akış sonunda pazara çıkış süresi %30, kreatif üretim süresi %60 kısalır.

## 12. Entegrasyon Ekosistemi
- **Pazar Yerleri:** Amazon, Trendyol, Hepsiburada, N11, Etsy, AliExpress, Google Shopping.
- **Reklam:** Meta, TikTok, Google Ads, Pinterest, X Ads.
- **Analitik:** GA4, Meta/TikTok pixel, Amazon Attribution.
- **İş Araçları:** Slack, Teams, Notion, ClickUp; n8n ile esnek otomasyon.
- **Veri Altyapısı:** Amazon SP-API, Meta Marketing API, Google Ads API, Trendyol Satıcı API, Hepsiburada Entegrasyon API’si, Alibaba Toplu RFQ API’si.

## 13. Hedef Personalar & Kullanım Senaryoları
- **Büyüyen Marka Yöneticisi:** Yeni ürün lansmanlarında fiyatlandırma ve rakip analizine odaklanır; haftalık raporlar ve kampanya planları oluşturur.
- **Ajans Performans Lead’i:** Birden fazla marka için reklam kreatiflerini ölçekler, insight kartlarını müşterilere paylaşır.
- **Tedarik Uzmanı:** MOQ ve teslim sürelerini optimize ederek maliyet tasarrufu sağlar; RFQ süreçlerini tek panelden yönetir.
- **Ürün AR-GE Analisti:** Yorumlardan ürün geliştirme içgörüleri çıkarmak için duygu analizi ve trend radarını kullanır.

## 14. Ürün İlkeleri & Deneyim Rehberi
- **Şeffaflık:** Her içgörünün kaynağı ve model katkı oranı açıklanır.
- **Rehberlik:** Kullanıcıyı boş ekranla bırakmak yerine öneri sihirbazları ve checklist’ler sunulur.
- **Otomasyon + Kontrol:** Otomatik aksiyonlar varsayılan olarak öneri modunda başlar; kullanıcı onayı sonrası yürütülür.
- **Yerelleştirme:** Arayüz ve raporlar çok dilli; para birimi, tarih biçimleri kullanıcı profiline göre ayarlanır.

## 15. Teknik Mimari
- **Veri Katmanı:** Event-driven pipeline (Kafka) + batch ETL (Airflow) ile karma mimari.
- **Depolama:** Ham veri için Data Lake (S3/MinIO), normalize veri için PostgreSQL, analitik için BigQuery/Snowflake.
- **Uygulama Katmanı:** Node.js/TypeScript API Gateway, Python mikro servisleri (scraper, ML servisleri), GraphQL sorgu katmanı.
- **Gerçek Zamanlı Analitik:** Stream işlemci (Flink/Kafka Streams) ile stok/fiyat alarmı; Redis pub/sub ile uyarı dağıtımı.
- **Ön Yüz:** Next.js + Tailwind, component library Storybook ile versiyonlanır; design token’lar Figma ile senkronize.
- **DevOps:** Kubernetes, Helm chart’ları, GitOps (ArgoCD), CI/CD’de birim test + entegrasyon test + güvenlik taraması.

## 16. Veri Yönetişimi & Kalite Süreçleri
- **Data Catalog:** Ürün, teklif, yorum veri setleri için lineage ve sahiplik bilgisi.
- **Kalite Kuralları:** Fiyat aralığı anomali, stok negatifliği, yorum dil tutarsızlığı gibi kurallar otomatik kontrol edilir.
- **Versiyonlama:** Özellik şemaları için semver; API değişiklikleri için geri uyumlu deprecation politikası.
- **Gizlilik:** Kişisel veri içeren alanlar maskeleme + role-based erişim.

## 17. Onboarding & Eğitim Yolculuğu
- **Hafta 1:** Veri bağlantıları ve ilk ürün projelerinin oluşturulması (müşteri başarı ekibi eşliğinde).
- **Hafta 2:** İçgörü stüdyosu ve reklam otomasyon atölyeleri, kullanım skor kartı takibi.
- **Hafta 3+:** İleri seviye eğitimler (ML açıklanabilirlik, API entegrasyonu), kullanıcı sertifikasyonu.
- **Destek Kanalları:** Uygulama içi sohbet botu, aylık “insight clinic” oturumları, bilgi bankası.

## 18. GTM & Büyüme Stratejisi
- **Hedef Pazarlar:** Türkiye & MENA’da beauty/home appliance, ABD’de D2C markalar.
- **Satış Modeli:** İçeriden satış + kanal partnerleri; ajanslara gelir paylaşım modeli.
- **Fiyatlandırma Denemeleri:** Kullanım bazlı kredi modeli + yıllık taahhüt indirimleri; add-on paketleri upsell.
- **Pazarlama:** Webinar serileri, benchmark raporları, başarı hikâyeleri; topluluk odaklı Slack kanalı.
- **Ürün Geri Bildirimi:** NPS, roadmap portalı, beta programı.

## 19. Yol Haritası (12 Ay)
| Çeyrek | Odak | Başlıca Çıktılar |
| --- | --- | --- |
| Q1 | Veri altyapısı & çekirdek içgörüler | Global fiyat izleme MVP, yorum analizi dil desteği (TR/EN), Starter paket lansmanı |
| Q2 | Reklam otomasyonu & satın alma akışı | Ad Studio Pro şablonları, RFQ otomasyonları, Slack entegrasyonu |
| Q3 | Gelişmiş analitik & uyumluluk | Satış tahmin modelleri, claim denetim motoru, ISO 27001 hazırlıkları |
| Q4 | Kurumsal ölçek & özelleştirme | Çoklu ülke kur kural motoru, özel veri konektörleri, Enterprise rapor stüdyosu |

## 20. Ek: Örnek API & Otomasyon Senaryoları
- **REST API Örneği:** `GET /api/v1/products/{id}/insights` → fiyat trendi, satış skoru, rakip listesi döner.
- **Webhook Senaryosu:** Fiyat düşüşü %10’u geçince Slack kanalına uyarı + HubSpot’ta görev açma.
- **n8n Akışı:** Trend radarında “menthol” anahtar kelimesi yükselince içerik ekibine görev, tedarik ekibine yeni RFQ önerisi.
- **Zapier:** InsightAgent rapor çıktısını Google Drive klasörüne kaydet, Notion sayfasını güncelle.

---
Bu doküman InsightAgent ürününün stratejik kapsamını, veri akışlarını ve kullanıcı deneyimi bileşenlerini özetler. Detaylı yol haritası, fiyatlandırma ve teknik mimari, ekip ile yapılacak toplantılarda netleştirilecektir.

## 21. Backend Uygulaması & Kurulum
- **Teknoloji Seçimi:** FastAPI + SQLAlchemy tabanlı Python servisleri; SQLite varsayılan kurulum ile hızlı demo.
- **Kod Yapısı:**
  - `app/database.py`: Bağlantı, session yönetimi ve tablo oluşturma.
  - `app/utils/serializers.py`: Ürün, teklif, yorum, insight, tedarikçi, kreatif ve rapor ilişkilerini derler.
  - `app/routers/`: Ürün zekâsı, içgörü, SEO, reklam stüdyosu, tedarik ve raporlama uç noktaları.
  - `fastapi/`: Harici bağımlılığa gerek kalmadan çalışan hafif FastAPI uyumlu katman.
  - `app/services/sample_data.py`: Demo verisi tohumu (HydraGlow örneği).
  - `tests/`: Pytest ile sağlık kontrolü ve uçtan uca veri doğrulaması.
- **Kurulum Adımları:**
  1. Python 3.11+ kurulu olduğundan emin olun.
  2. `python -m venv .venv && source .venv/bin/activate`
  3. `pip install -r requirements.txt` (yalnızca standart kütüphane notlarını okumak için, ek paket gerekmiyor)
  4. `python -m app.server`
- **Test Çalıştırma:** `pytest`
- **API Dokümantasyonu:** Çalışan servis altında `http://localhost:8000/docs` otomatik Swagger arayüzü sunulur.

## 22. Modüler API Yüzeyi
| Modül | Temel Endpointler | Amaç |
| --- | --- | --- |
| Ürün Zekâsı | `GET /products/?q=&limit=&offset=`, `GET /products/{id}` | Ürün ve bağlı sinyallerin arama & sayfalama ile derlenmesi |
| İçgörü & Trend | `GET /insights/{product_id}` | Satış/trend skorları, SWOT özetleri |
| Fiyat & Teklifler | `GET /offers/`, `GET /offers/snapshot/{product_id}` | Kanal bazlı fiyat listesi ve anlık fiyat özeti |
| SEO & Keyword | `GET /keywords/{product_id}` | Otomatik keyword madenciliği çıktıları |
| Reklam Stüdyosu | `GET /creatives/{product_id}` | Metin/görsel kreatif önerileri |
| Yorum Analizi | `GET /reviews/`, `GET /reviews/highlights/{product_id}` | Duygu dağılımı ve konu özetleri |
| Satın Alma & Tedarik | `GET /suppliers/`, `GET /suppliers/{id}/rfqs`, `GET /suppliers/by-product/{product_id}`, `POST /rfqs/`, `PATCH /rfqs/{id}` | Tedarikçi kataloğu, RFQ oluşturma ve durum güncelleme |
| Raporlama | `GET /reports/{product_id}` | Paylaşılabilir rapor bağlantıları |
| Portföy Analitiği | `GET /analytics/dashboard`, `GET /analytics/products/{product_id}/playbook` | Ürün seti genelinde KPI özetleri ve ürün özelinde aksiyon planları |
- **Portföy Panosu:** Ortalama satış skoru, fiyat aralığı, açık RFQ sayısı, kreatif kanal kapsaması gibi metrikleri tek JSON yanıtında toplar.
- **Ürün Playbook’u:** Fiyat boşluğu, duygu özeti, keyword önceliği ve sıradaki aksiyon adımlarını içeren 360° öneri seti döner.
- **Güvenlik Hazırlığı:** Tüm endpointler için gelecekte JWT tabanlı kimlik doğrulama ve rate limiting proxy’si (Envoy/NGINX) planlanır.
- **Entegrasyon Yol Haritası:** API istemcileri için Python SDK ve Zapier connector taslakları sonraki sürümlerde eklenecek.
