# Geliştirme Ortamı Sorun Giderme

## `npm install` 403 Forbidden Hatası
- **Belirti:** `npm install` çalıştırıldığında `403 Forbidden - GET https://registry.npmjs.org/<paket>` mesajı alınır.
- **Neden:** Bulunduğunuz ağ, dış dünyaya yalnızca kurum içi proxy üzerinden çıkmanıza izin veriyor ve bu proxy `registry.npmjs.org` isteklerini engelliyor.
- **Çözüm Adımları:**
1. Proxy sunucusunun erişimine izin verdiği bir mirror adresi belirleyin. Varsayılan mirror olarak `https://registry.npmmirror.com` kullanılabilir.
2. Depo kökünde yer alan [`.npmrc`](../.npmrc) dosyasında gerekli registry ayarını yapın veya aşağıdaki komutla geçici olarak değiştirin:
     ```bash
     npm config set registry https://registry.npmmirror.com
     ```
3. Bazı paketler (örneğin `@supabase` scope'u) mirror üzerinde yetki hatası döndürebilir. Bu durumda sadece ilgili scope'u resmi kayda yönlendirin:
     ```bash
     npm config set @supabase:registry https://registry.npmjs.org/
     ```
4. Proxy kimlik doğrulaması gerekiyorsa kullanıcı adı/parola ekleyin:
     ```bash
     npm config set proxy http://kullanici:parola@proxy-adresi:port
     npm config set https-proxy http://kullanici:parola@proxy-adresi:port
     ```
5. Eğer mirror üzerinden de engelleniyorsa Hostinger VPS içinde bir `verdaccio` ya da `npm-proxy-cache` kurup `.npmrc` dosyasını o adresi gösterecek şekilde güncelleyin.
6. Son olarak `npm cache clean --force` ve `npm install --prefer-offline` komutlarıyla kurulumun tekrarlandığından emin olun.

> **Not:** CI/CD ajanları için de aynı `.npmrc` dosyasının ortam değişkenleriyle (ör. `NPM_REGISTRY_URL`) güncellenmesi gerekir.
