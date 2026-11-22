# Gizlilik

Bu belge `viral-urun-ekibi` eklentisinin verilerinizle ne yaptığını anlatır. Kısa özet: **eklenti kendisi veri toplamaz,
sunucusu yoktur, hiçbir yere telemetri göndermez.** Her şey sizin bilgisayarınızda ve kendi hesaplarınızla çalışır.

## Eklentinin kendisi
- Veri toplamaz, analitik/izleme kodu içermez, bir sunucuya kullanım bilgisi göndermez. Yazarın sizin verinize erişimi yoktur.
- Çalışma çıktıları (ürün listeleri, kanıt dosyaları, senaryolar, videolar) sizin proje klasörünüzde kalır: hafıza `.ekip/`,
  ürün çıktıları `is/`. Eklentinin kendi klasörüne kullanıcı verisi yazılmaz.
- Oturum kancası (`hooks/durum-yukle.sh`) yalnızca `.ekip/` dosyalarını yerelde okuyup Claude'a bağlam olarak verir; ağa çıkmaz.
- Eklentideki betikler (kurgu, doğrulama, paket yazıcı) yerelde çalışır. Tek istisna: `spy` becerisinin
  `shopify_kontrol.py` betiği, bir mağazanın herkese açık ürün listesini (`/products.json`) okumak için o mağazanın adresine
  salt-okunur bir HTTP isteği atar; hesap bilgisi göndermez.

## Sizin adınıza gidilen dış servisler
Eklenti bu servislere kendi hesabı ya da anahtarıyla değil, **sizin oturumunuz ve izinlerinizle** bağlanır. Bu servislerde
verinizin nasıl işlendiği o servislerin kendi gizlilik politikalarına tabidir.

| Servis | Ne için | Nasıl |
|---|---|---|
| Anthropic (Claude Code) | Eklentiyi çalıştıran model; komutlarınız ve okuduğu dosyalar modele gider | Kendi Claude hesabınız |
| Shopify (`setup.shopify.com/mcp`, `.mcp.json`) | Mağaza kurulumu: ürün, metin, görsel, sayfa yazımı | Uzak MCP; ilk kullanımda `/mcp` ile sizin Shopify girişiniz |
| Tarayıcı üzerinden (Claude in Chrome / bilgisayar kontrolü) | Instagram, AliExpress, Meta Reklam Kütüphanesi, ChatGPT, Google Flow, Google Trends gibi sayfaları gezmek | Sizin tarayıcı oturumunuz; şifre girilmez, giriş ekranında size devredilir |
| ChatGPT / Google Flow | Görsel ve klip üretimi (kredi harcayabilir) | Kendi hesabınız; her harcamadan önce onayınız istenir |
| Web arama ve sayfa okuma | Pazar ve ürün araştırması | Claude'un arama araçları |
| HeyGen (yalnız isteğe bağlı HyperFrames/`media-use` becerileri) | Üretilmiş medya, ses, müzik | Kendi HeyGen girişiniz; kurmazsanız kullanılmaz |

## Siz ne yapabilirsiniz
- Eklentiyi kaldırmak (`/plugin uninstall`) yerel `.ekip/` ve `is/` klasörlerinizi silmez; istemiyorsanız kendiniz silin.
- Üçüncü taraf bağlantılarını `/mcp` ve tarayıcı eklentisi izinlerinden istediğiniz an kapatabilirsiniz.
- Kişisel veri, müşteri verisi, şifre ya da API anahtarını proje klasörüne ve sohbete yazmayın.

## İletişim
Gizlilikle ilgili soru ve bildirimler için GitHub deposunda issue açın; güvenlik açığı için [SECURITY.md](SECURITY.md).

Son güncelleme: 2026-11-23 · Sürüm 0.3.0
