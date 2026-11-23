# ChatGPT parçası: Viral Ürün Ekibi

Aynı ekibin ChatGPT sürümü: 16 beceri (8 iş akışı + 7 ekip rolü + bilgi bankası). Mağaza kolu tam çalışır (görsel üretimi sohbette,
Shopify ChatGPT'nin kendi bağlantısıyla, Çalışma modu şart). Betikler kod yorumlayıcıda koşar. Sürüm: 0.4.0.

## Hangi yoldan kuracağım?

| Ne istiyorsun? | Ne indir | Nereye yükle |
|---|---|---|
| **ChatGPT plugin** (önerilen) | [Releases](https://github.com/armanvibecoding/viral-urun-ekibi-market/releases/latest) → `viral-urun-ekibi-CHATGPT-v0.4.0.zip` (açma) | ChatGPT → **Plugins** → yükleme seçeneği |
| **Proje** (plugin yoksa; claude.ai'de de olur) | bu klasördeki [`proje-paketi/`](proje-paketi/KURULUM.md) | ChatGPT ya da claude.ai → **Projects** |

## Plugin kurulumu (3 adım)

1. `viral-urun-ekibi-CHATGPT-v0.4.0.zip` dosyasını Releases'tan indir. ZIP'i açma.
2. ChatGPT → **Plugins** → yükleme seçeneği. İş alanında: yönetici konsolu → **Plugins** → **Add** → **Upload plugin**. Seçenek yoksa
   **Plugins → Skills → Create → Upload** ile ZIP'in içindeki `skills/` altındaki klasörleri tek tek yükle (önce `ekip-bilgi` ve `captain`).
   Kişisel hesapta hangi planın gerektiği belgelerde net değil.
3. Yeni sohbette yaz: `Ekibi başlat. Pazarım Türkiye.` Her cevabın sonunda DURUM bloğu çıkar; yeni sohbete geçerken onu yapıştır.

Plugin yüklenemezse Proje yolu (`proje-paketi/KURULUM.md`, 10 dakika) aynı bilgi bankasıyla çalışır.

## ChatGPT'de çalışmayan ya da senin yapman gereken adımlar

| Adım | Durum | Ne yapacaksın |
|---|---|---|
| Instagram'da gezinme, AliExpress/Meta Reklam Kütüphanesi tarama | Tarayıcı otomasyonu yok | Sayfayı sen açar, ekran görüntüsü ya da sayfa metnini sohbete yüklersin |
| iPhone Yansıtma modu | Yok | Kullanılamaz; ekran görüntüsü yükle |
| Google Flow ile klip üretimi | Otomatik yükleme yok | Ekip prompt verir, Flow'da sen üretirsin; klipleri sohbete yüklersin |
| ffmpeg kurgusu | Kod yorumlayıcıda | Klipleri yükle; ffmpeg'i kullanmadan önce `ffmpeg -version` ile ölçtür |
| Alt ajanlar, oturum kancası, otomatik `.ekip/` hafızası | Yok | Hafıza DURUM bloğu + DEVAM KARTI ile taşınır |
| Hareketli tasarım (HyperFrames) | Pakette yok | Yerel Node 22+ ve Chrome ister; Claude Code parçasını kullan |
| Shopify bağlantısı | ChatGPT'nin kendi bağlantısı | Çalışma modunda bağla; `.mcp.json` pakete girmez |

Tam liste `captain` becerisinin başındadır. Tam hat (otomatik gezinme, 17 ajan, hafıza) için [Claude parçası](../claude/README.md).

## ZIP'i kendin üretmek

ZIP depoda tutulmaz; her sürümde Releases'a yüklenir. Kendin üretmek için (depo kökünden):

```sh
sh scripts/paketle.sh              # iki ZIP birden: dist/viral-urun-ekibi-CLAUDE-v<sürüm>.zip ve ...-CHATGPT-v<sürüm>.zip
sh scripts/chatgpt_paketi_yap.sh   # yalnız ChatGPT ZIP'i
sh scripts/proje_paketi_yap.sh     # proje-paketi/yuklenecek/ dosyalarını bilgi bankasından yeniden üretir
```

`proje-paketi/yuklenecek/` bilgi bankasının (`plugins/viral-urun-ekibi/ortak/`) üretilmiş kopyasıdır; elle düzenleme, betikle yeniden üret.

Ana sayfa: [../README.md](../README.md)
