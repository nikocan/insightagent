# Cafeoi Bulut Dağıtım Kontrol Listesi

Bu rehber, Hostinger VPS + Supabase + GitHub entegrasyonlu Cafeoi kurulumunu uçtan uca doğrulamak için gereken adımları listeler. Her bölüm, mevcut eksiklikleri tespit edip takip etmek için kısa bir özet ve yapılacaklar sunar.

## 1. Altyapı Görünürlüğü
- [ ] Hostinger VPS üzerindeki Next.js runtime’ının Node.js 18+ ve pnpm/npm CLI ile uyumlu olduğunu doğrula.
- [ ] Supabase projesi için `anon` ve `service_role` anahtarlarını güvenli değişken yönetimi (Hostinger Secrets, GitHub Actions Secrets) altına al.
- [ ] Uygulama günlüklerini merkezi bir dizinde (örn. `/var/log/cafeoi`) topla ve rotasyonu ayarla.

## 2. Supabase Yapılandırması
- [ ] `supabase/migrations` klasöründeki şema dosyalarını üretim veritabanına uygula.
- [ ] RLS politikalarını ve kullanım limit tetikleyicilerini yazıp migration dosyalarına ekle.
- [ ] Plan kayıtları için yedekleme (Point-in-Time Recovery veya günlük export) planı oluştur.

## 3. Uygulama Ortam Değişkenleri
- [ ] `.env.local` ve dağıtım ortamları için aşağıdaki değişkenleri tanımla:
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `OPENAI_API_KEY`
  - Stripe/Iyzico entegrasyonları hazır olduğunda ilgili anahtarlar
- [ ] `.npmrc` ile gelen mirror registry ayarının Hostinger’da erişilebilir olduğunu test et; değilse alternatif proxy adresi tanımla.

## 4. CI/CD ve GitHub Entegrasyonu
- [ ] GitHub Actions üzerinden Supabase migration ve lint/test komutlarını çalıştıran bir pipeline kur.
- [ ] Başarılı pipeline sonrasında Hostinger VPS’ye otomatik dağıtım (SSH deploy, Docker image veya PM2 restart) tetikle.
- [ ] Supabase Access Token’ı ile `supabase db push` komutuna yetki ver.

## 5. Uygulama Özellikleri İçin Sıradaki Adımlar
- [ ] `/api/plan` servisini OpenAI API çağrısıyla üretim senaryosuna taşı ve hata durumlarını logla.
- [ ] Plan sürümlerini `ai_plans` tablosunda tarihçeli olarak sakla.
- [ ] Şablon paketlerini Supabase Storage’a yükleyip indirme/Deploy bağlantılarını uygulamada göster.
- [ ] Stripe/Iyzico ödeme akışlarını profil ekranına bağla ve Pro plan yetkilendirmesini RLS ile enforce et.

## 6. Mobil (Expo) Yol Haritası
- [ ] Expo projesini bu depo içinde `apps/mobile` dizinine ekle.
- [ ] Web ile paylaşılan bileşenleri `packages/ui` benzeri bir monorepo yapısında toplu.
- [ ] Expo EAS yapılandırmasını (Android keystore, iOS certificates) README’ye ekle.

Bu kontrol listesi, `docs/TASK_SUMMARY.md` ve `docs/DELIVERY_BACKLOG.md` ile birlikte güncel tutulmalıdır. Her dağıtım öncesinde bu maddeleri gözden geçirerek eksik kalemleri backlog’a taşıyın.
