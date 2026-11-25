# AliExpress'i okuma: arama terimi, ürün sayfası, tuzaklar

Ne zaman okunur: arama terimi üretirken ve aday listesi çıkarırken (akış adım 2–3).

## 1. Erişim (ölçülmüş)
- Düz istek (`curl`, WebFetch) AliExpress'te **CAPTCHA sayfası** ya da **giriş sayfasına yönlendirme** döndürüyor. Bu yolla okunan "veri" veri değildir.
- Çalışan yol: kullanıcının kendi tarayıcısında sayfayı açıp metnini okumak (Claude in Chrome: `navigate` + `get_page_text`).
- Tempo: istekler arası **≥15–20 sn** (araya WebSearch koymak süreyi doldurur). Bir oturumda ~15 arama + ~20 ürün sayfası güvenli görüldü.
- **CAPTCHA çıkarsa:** çözme, atlatma, gizli pencere deneme. Dur, sekmeyi kapat, o ana kadar okunanı dosyaya yaz, kalan terimleri "taranmadı (CAPTCHA)" diye işaretle.
- Satın alma, sepete ekleme, hesap/adres değiştirme yok. Yalnız okuma.
- Ürün linki: arama sayfasında kartı tıklamak yeni sekme açar; bunun yerine `javascript_tool` ile `a[href*="/item/"]` bağlantılarını oku, `item/<no>` biçimine indir (`firsat_kontrol.py` bunu bekler).
- Para birimi ve ülke: ABD pazarı için `aliexpress.us` (USD). TR pazarı için ürün sayfasında **Türkiye'ye gönderim var mı** ayrıca bakılır; bakılamadıysa "TR gönderim doğrulanamadı" yazılır.

## 2. Arama terimi üretme (mekanizmadan, ürün adından değil)
1. `ortak/viral-dna.md` §3'ten bir mekanizma seç (ör. M3 "obje başka bir şeye benziyor").
2. Mekanizmanın "ürünün taşıması gereken özellik" sütununu somut ürün biçimine çevir (ör. "yiyecek şeklinde evcil yatak").
3. İngilizce, 3–5 kelimelik arama terimi yaz (`food shaped pet bed funny`). Bilinen viral ürünün adını aratma; onun mekanizmasını başka nesneye taşı.
4. Her terimi aramadan önce `is/firsat/aramalar.md`'de ara; aranmışsa atla.

Kaynak çalışmada denenmiş terim örnekleri (tekrar aramak yerine yeni nesne bulmak için ilham):
| Mekanizma | Örnek terimler |
|---|---|
| M2 canlıyı karaktere çevirme | pet costume food shaped funny · lobster costume dog cat · turtle shell costume for dog cat |
| M3 görsel şaka | sushi shaped pet bed · fish shaped slippers funny · bathtub shaped pet bed · shark pet bed |
| M4 görünmeyeni görünür yapma | pet urine detector uv flashlight · car cleaning gel slime dust |
| M5 kimlik/ritüel | portable prayer mat travel pocket · ramadan lantern quran speaker light |
| M7 canlıyı bedende taşıma | pet carrier chest bag hands free small dog |
| M8 hayvan problem → huzur | radiator cat bed hanging · dog paw cleaner cup |
| M11 küçük sürtünme | couch armrest cup holder tray silicone · door draft stopper under door |
| M12 ekransız aile oyunu | tabletop hockey game family fast |
| M14 zararsız şaka | remote control prank toy adult |

## 3. Ürün sayfasından ne okunur
| Alan | Doğru kaynak | Tuzak (gerçekten yaşandı) |
|---|---|---|
| **Ürün satışı** | Başlık satırındaki "N sold" | Arama kartındaki sayı fiyatla yapışık okunuyor ve yanlış (bir turda 461 yazıldı, sayfada 33'tü). Sayfa başlığında yalnız mağaza toplamı ("5,000+ sold" mağaza geneli) ya da "100K+ benzer" varsa: **"ürün satışı görünmedi (mağaza N)"** yaz. |
| Puan / yorum | Başlık satırı | 1,5★ / 5 yorum gibi düşük puan kalite sinyalidir, satış sayısıyla telafi edilmez. |
| **Normal fiyat** | Herkese açık güncel satış fiyatı (yeni müşteri/kupon teklifi DEĞİL) | "$1.09 yeni müşteri", "erken kuş", "only 1 left" fiyatı tek adetlik tekliftir. Üstü çizili "liste" fiyatı çoğu zaman şişirilmiştir (saha 2026-11-24: %92 "indirim") → normal fiyat sayılmaz; teklif dışı satış fiyatı görünmüyorsa "normal fiyat doğrulanamadı" yaz, marj İZLE'de kalır. Marj normal fiyattan hesaplanır. Fiyatlar gün içinde oynar → okuma tarihini yaz. |
| Görsel | Ürün fotoğrafları + **yorum fotoğrafları** | Satıcı fotoğrafı AI üretimi olabilir (ürün kareden kareye değişiyor). Mekanizma (ör. "tuşa basınca mama düşer") yalnız gerçek alıcı fotoğrafı/videosuyla doğrulanır; yoksa "mekanizma doğrulanamadı". |
| Filigran / başka marka logosu | Fotoğraf | Reklamda kendi görseli gerekir → not düş. |

## 4. Benzer ≠ aynı
Aynı ürün sayılması için üçü de tutmalı: **form** (şekil, boyut sınıfı), **ana parça** (ör. köpekbalığı başı + oluklu gövde), **mekanizma** (ne yaptığı).
Örnek: "balık şeklinde terlik" diye bulunan ilan, fotoğrafta yalnız nakışlı düz terlikti → elendi.
Ürünü görmeden tarif yazma: bir turda görülmemiş ürüne "kuyruk yüzgeci" yazıldı, gerçek üründe yoktu.

## 5. Aday satırına yazılacaklar
Link (ürün sayfası) · ürün satışı (sayfa) · normal fiyat (+ teklif fiyatı ayrıca) · puan/yorum · görsel notu (bakıldı mı, AI gibi mi, filigran) ·
mekanizma kodu + akraba not no · DNA (geçen V'ler: `V1,V2,V4,V6`) · okuma tarihi.
Okunamayan alan: `doğrulanamadı` (sebep: CAPTCHA / giriş duvarı / sayfada yok).
