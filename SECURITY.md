# Güvenlik politikası

## Desteklenen sürümler
Yalnızca en son yayımlanan sürüm (şimdilik **0.3.x**) güvenlik düzeltmesi alır.

## Açık bildirme
Güvenlik açığını **herkese açık issue olarak açmayın.** GitHub'da deponun **Security** sekmesinden
**Report a vulnerability** (özel bildirim) ile gönderin. Bildirime şunları yazın:
- etkilenen dosya ve sürüm, adım adım yeniden üretme,
- gerçek etkisi (neyi okutabilir, neyi yazdırabilir, para ya da hesap riski var mı).

Beklenen süreler: bildirimi 7 gün içinde yanıtlarız; doğrulanan açık için düzeltme planını 30 gün içinde paylaşırız.
Bu proje gönüllü olarak sürdürülüyor, süreler hedeftir, garanti değildir.

## Kapsam
Kapsam içinde:
- eklentideki betikler (`plugins/viral-urun-ekibi/**/scripts`, `ortak/paket.py`, `scripts/`),
- oturum kancası `hooks/durum-yukle.sh` ve `.mcp.json` içindeki uzak bağlantı tanımı,
- becerilerin ve ajanların araç izinlerini gereğinden geniş açan ya da kullanıcı onayı olmadan para harcatan yönergeleri,
- kişisel veri sızıntısı (depoya yanlışlıkla girmiş anahtar, e-posta, yerel yol).

Kapsam dışında: Claude Code, Shopify, ChatGPT, Google Flow gibi üçüncü taraf servislerin kendi açıkları (ilgili üreticiye bildirin);
`plugins/viral-urun-ekibi/skills/hyperframes*` ve `media-use` (HeyGen'in Apache-2.0 paketi; kaynağına bildirin).

## Sır ve kimlik bilgisi
Depoda anahtar, token ya da müşteri verisi bulunmamalıdır. Bulursanız yukarıdaki özel kanaldan bildirin; ilgili anahtarı
kendi hesabınızdan da iptal edin. Gizlilik bilgisi: [PRIVACY.md](PRIVACY.md).
