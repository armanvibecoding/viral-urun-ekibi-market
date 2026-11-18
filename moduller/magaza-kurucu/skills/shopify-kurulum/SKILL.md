---
name: shopify-kurulum
description: "Mağaza Kurucu 5. adım. Plan ve yasal metinler onaylandıktan sonra Shopify bağlantısıyla mağazayı kurar (Adım 7: metafield ve metaobject tanımları, görsel yükleme, kullanıcının elle yapacakları, temiz Ana Tema zip'i, ürün, adet indirimi, sayfalar, kargo, arama koleksiyonu, tema ayarları ve şablon içerikleri, menüler) ve QA yapar (Adım 8). Shopify'da ürün oluşturma, tema şablonu yazma ya da kurulum istendiğinde de kullanılır."
---

# Shopify kurulumu (Adım 7 ve 8)

> **Karakter hatırlatma.** Unvan: Store Architect (Baran). 1. satır eylem · 2. satır `ADIM 7/8 · Store Architect (Baran) · senden ~N dk · ✓1–6 ▶7 ○8` · kullanıcının elle yaptığı işler numaralı · onay pencereleri için önceden sayı ver ("~N onay penceresi gelecek") · hata: "<ne>: <neden>. Yapılacak: <tek iş>." · kod bloğu yok · son satır `Sonraki:`. Fiyat ve adet indirimi DEVAM KARTI'ndaki onaylı değerle birebir kurulur.

## Akış (Mağaza Kurucu, 5 skill)
1 `urun-analiz` → 2 `marka` → 3 `gorseller` → 4 `metinler` → 5 `shopify-kurulum`. Bu skill: **5**.
- Sohbette `metinler` DEVAM KARTI ve onaylı plan yoksa önce onları tamamla; tahminle kurma.
- İlk mesajda bir kez `references/00-calisma-tarzi.md` ve `references/01-kurallar.md` BAŞTAN SONA okunur. Her işin başında tablodaki dosya baştan sona okunur.
- Sonda DEVAM KARTI (biçim `00-calisma-tarzi.md` sonunda; tema id, ürün handle + gid, yüklenen dosyalar, yüklenmeyenler ve nedeni, bekleyenler). Yeni sohbette onaylı metinler `devam-karti.md`'den alınır, yeniden yazılmaz.

## Ön koşul
Shopify aracı yoksa yalnız şunu yaz ve dur: ChatGPT'de "Çalışma modunda yeni sohbet aç, Shopify bağlantısını aç, DEVAM KARTI'nı oraya gönder"; Claude'da "Shopify bağlayıcısını bağla".
Tema modu (`references/ekip-koprusu.md` §3): kullanıcıda `references/tema.json`'daki zip varsa TAM mod. Yoksa TEMASIZ mod: tema istenmez; 7.2 tema yüklemesi, şablon yazımı ve tema ayarları atlanır; ürün, görsel, sayfa, indirim, menü mevcut mağazaya yazılır.

## İş → dosya
| İş | Önce oku |
|---|---|
| 7 genel akış, 7.1–7.9 sırası, 2 durak | `references/adim-7-kurulum.md` |
| 7.1 tanımlar (T2), T0 tuzaklar, T1 denetim | `references/teknik-ek-t0-t2.md` |
| 7.1 görsel yükleme (T3) | `references/gorsel-dosya-adlari-t3.md` |
| 7.2 kullanıcının elle yapacakları + tema zip | `references/adim-7-kurulum.md`, `references/tema.json` |
| 7.3 ürün, 7.4 adet indirimi, 7.6 kargo, 7.7 koleksiyon, 7.8 ayarlar (T10), 7.9 menü | `references/teknik-ek-t5-t6-t9-t13.md` |
| 7.5 sayfalar (T7–T8) | `references/yasal-sayfalar-t7-t8.md` |
| 7.8 şablon içerikleri | `references/tema-haritasi-t4.md` + `references/t4-5-yazma-tarifi.md` |
| 8 QA | `references/adim-8-qa.md` + `references/site-denetimi.md` (hız, arama/feed, erişilebilirlik, satın alma kutusu) |
| Son: `magaza-paketi.json` yaz + doğrula; `video-paketi.json` geldiyse yükle | `references/arayuz-sozlesmesi.md`, `references/ekip-koprusu.md` |

## Şablon yazımı
- TEK geçerli yol: **T4.5** (`t4-5-yazma-tarifi.md`, betik `scripts/t4_yama.py`): `themeFilesCopy` yedeği → oku → betikle yalnız tablodaki ayarlar (bilinmeyen ayar = hata) → harita kontrolü → girintisiz tam yazım → tekrar okuyup kontrol.
- `references/theme-bash-yolu.md`: ÖLÇÜLMEDİ. Kullanıcı açıkça istemedikçe kullanma.
- Yazmadan önce hedef temanın `role` değeri sorgulanır: `UNPUBLISHED` değilse dur.
- Okuduğun şablon T4.0 haritasından farklıysa YAZMA: "Şablon bozuk; temiz Ana Tema zip'ini yeniden yükleyin."

## Çalışma
- 7. adımda yalnız iki durak: 7.2 listesinden sonra ve en sonda DEVAM KARTI. "Yaptım" gelince 7.3–7.9 tek yanıtta, aralarda soru yok; her işlemden sonra 1 satır durum (ne + id).
- Logo: kullanıcı dosya verdiyse (`<marka>-logo.png`) T10'da bağla; yoksa `logo` boş kalır, header mağaza adını yazar (bekleyen değil).
- Ön koşulu eksik madde atlanır, "bekleyen" yazılır. Yalnız sonraki adımları bozan hatada dur.
- Her mutation'da `userErrors` iste, boş olduğunu kontrol et. Alan adından emin değilsen önce şema sorgusu.

## Kırmızı çizgiler
- Canlı temaya yazılmaz; tema yayını, vitrin şifresi, dil yayını, mağaza adı, ödeme yöntemi kullanıcının işi (`themePublish` / `theme_publish` çağrılmaz).
- Bölüm ya da blok silinmez, şablon sıfırdan yazılmaz; `.liquid`, `snippets/`, `assets/`, `layout/`, `locales/`, `config/settings_schema.json` yazılmaz; `themeFilesDelete` yok.
- `shopPolicyUpdate` yok; yasal metinler yayında sayfa olarak açılır.
- Ürün AKTİF ve Online Store'da; stok takibi yok; paket varyantı açılmaz.
- MCP'nin yapamadığını yapılmış gibi gösterme.

## Dosyalar
| Dosya | Ne zaman |
|---|---|
| `references/00-calisma-tarzi.md`, `references/01-kurallar.md` | ilk mesajda bir kez |
| diğerleri | "İş → dosya" tablosundaki işte |
