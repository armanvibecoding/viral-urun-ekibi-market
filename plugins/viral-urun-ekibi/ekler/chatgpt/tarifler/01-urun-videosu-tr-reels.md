# Tarif 01 — Ürün videosu (Reels, döngü) · betiksiz ChatGPT sürümü

## Amaç
Tek ürün için 6–10,5 sn başa saran döngü videosunun (ya da 8–15 sn klasik) **tam üretim paketini** hazırlamak: kart, senaryo tablosu, kare/klip istemleri, saniye saniye kurgu ve yazı çizelgesi, ses kararı. Betik yok; son montajı kullanıcı CapCut/InShot'ta bu çizelgeyle yapar (kod yorumlayıcıda ffmpeg varsa `ffmpeg -version` ile ölç, yoksa montaj kullanıcıdadır).

## Girdi
Ürün fotoğrafı + 1 cümle ürün · pazar (yoksa ABD; TR ise TR) · ürün tipi (ekranlı/ekransız/sağlık).

## Adımlar
0. **Ön-üretim kartı (zorunlu; kart yoksa sonraki adıma geçme).** Sohbette şu 6 satırı yaz ve kullanıcıya göster: `pazar` (US / UK / DE / FR / ES / TR) · `kanca ailesi + kanca metni + kanıt numaraları` (yalnız `ozet-kanca-sahne-pazar.md`'deki numaralar; TR'de kanca ≤ 8 kelime) · `sahne şablonu` (S1–S10) · `format` (döngü 7–10 sn | hikâye 25 sn) + döngüde `tatmin anı` · `müzik kararı` (ölçülmedi; kural = rampa + açılışta diegetik ses; dayanak yaz) · `ilk 1 saniyede ne görünecek`. AB/UK'de "eşik ABD'nin yarısı", TR'de "TR verisi zayıf, ilk testten sonra kalibre" satırını ekle.
1. Kanca: kart satırındaki aileden 3 aday yaz, birini seç, gerekçeyi tek satır yaz (soru sorma).
2. Çizelge tablosu (saniye · plan · görüntü · ekran yazısı · ses): döngü için 3–6 plan, plan ~1,3–2 sn, **son plan = ilk plan**, tek tatmin anı. Yazı: **kutulu** (yarı saydam koyu kutu, kontursuz), tek kelime vurgu **sarı #FFE600 ya da yeşil #22C55E**, **kelime kelime çıkış**, ≤ 5 kelime/yazı, kelime başına ≥ 0,25 sn + 0,5 sn tepki. Yazı konumu: üst %12 ve alt %20 boş; kanca üstte (%16), CTA alt üçte birde ama alt %20'ye inmez. Kanca ve CTA yazısı sırayla değişir; ayrı bitiş kartı yok: `Comment "KELİME" and I'll DM you the link` / LINK IN BIO.
3. Görsel/klip istemleri: `uretim-istemleri.md` §1–§3 (kare başına bir istem; görseli ChatGPT'de üret, her kareyi denetle). Klip Flow'da kullanıcıdadır (kredi = önce onay).
4. Sağlık ürünüyse kapanışa bilgi notu satırı: `Tıbbi tedavi amaçlı değildir`.
5. Ses: müzik ilk kareden girer, **1,5–2 sn rampa**, ani açılma yok; ilk karede diegetik ses (tık, dokunuş); müzik kullanıcının dosyası ya da açık lisanslı parça; Aralık'ta Instagram ses kütüphanesi (dosyaya gömülmez). Ses −14 ±1 LUFS (kullanıcı dışa aktarırken normalleştirir).
6. Çıktıyı ver: kart · çizelge tablosu · istemler · caption (tek fayda cümlesi + CTA) · DURUM bloğu.

**Pazar:** ABD güçlü veri · AB/UK paylaşım beklentisi ABD'nin yarısı (eşikle öldürme yok) · **TR verisi zayıf (1 kayıt), ilk testten sonra kalibre; kanca ≤ 8 kelime.** Müzik: **ölçülmedi**, kural = rampa. Özet ve kanıt numaraları: `ozet-kanca-sahne-pazar.md`.

## Kalite çıtası (ölçülebilir)
Döngü 6–10,5 sn (klasik 8–15) · 1080×1920 · 30 fps · kanca bas < 0,05 sn · ürün ilk 0,9 sn'de (ekransız üründe ürün planı yeterli) · yazı kutulu + tek kelime vurgu + kelime kelime · güvenli alan (üst %12 / alt %20 / sağ %15 boş) · müzik rampası 1,5–2 sn · sağlıkta bilgi notu · jüri için ≥ 3 viral referans yoksa iş durmaz, teslim notuna "jüri yapılamadı (referans < 3)" yazılır.

## Kendi çıktını şu 10 maddeyle denetle (her maddeye ✓ ya da ✗ + kanıt yaz; ✗ varsa düzeltip yeniden denetle)
1. Ön-üretim kartı 6 satırıyla yazılı ve kanıt numaraları özet dosyasında var.
2. Kanca ilk karede (0. saniye) ve ≤ 2 satır; TR ise ≤ 8 kelime.
3. Kanca ailesi/şablonu özetteki aileden; kimlik BÜYÜK harf (K1/K2).
4. İlk 1 saniyede ürün ya da sonuç görünüyor (kutu açılışı değil).
5. Tek tatmin/kanıt anı belirlenmiş ve zaman çizelgesinde işaretli.
6. Yazı ürünü örtmüyor; üst %12 ve alt %20, sağ %15 boş (güvenli alan).
7. Ekranda fiyat/indirim yüzdesi yok (ICE-01); uydurma sayı, yorum, stok yok (IDD-02).
8. Sağlık/sonuç cümlesi varsa sonunda bilgi notu satırı var (IDD-01); platform riski varsa uyarı yazıldı (PLT-01).
9. Müzik kararı yazılı: ilk karede diegetik ses + 1,5–2 sn rampa; ani açılma yok; telifli şarkı dosyaya gömülmedi (SES-02).
10. Süre ve yapı: döngüde 6–10,5 sn, 3–6 plan, son plan = ilk plan, CTA yazısı kancayla dönüşümlü; hikâyede 25 sn.

## Bitti tanımı
Kart + çizelge + istemler + caption + 10 maddelik denetim tablosu sohbette; kullanıcı montajı yaptıktan sonra videoyu yüklerse 10 maddeyi video üzerinde yeniden işaretle.
