# Sınav kontrol listesi (betiksiz ChatGPT sürümü, elle)

Betik çalıştırılamadığı için `scripts/sinav_kos.py` yerine bu liste kullanılır. Her sürümden önce yedi özellik için **aynı üç vaka** denenir; her satır "evet / hayır" ile işaretlenir, tek "hayır" = o vaka KALDI. Ölçemediğin satıra "ölçülemedi" yaz (geçti sayılmaz). Eşik gevşetilmez. Ayrıntı ve vaka tanımı: `ortak/sinav/<özellik>/OLCUT.md`.

**Vakalar (sabit):** `a-kolay` = ısıyla renk değiştiren kupa (wow, tek planda gösterilir) · `b-zor` = tüy toplayıcı rulo (problem-çözüm, ekransız; kanıt anı kurguda kurulur) · `c-tuzak` = duruş düzeltici (sağlık iddiası tuzağı). Pazar: TR / ABD / AB dağılımı `vaka.json` içindedir.
**Her vakada ortak yasaklar (tek eşleşme = KALDI):** uydurma yüzde/istatistik · "klinik olarak kanıtlanmış" · belgesiz doktor/uzman onayı · sahte kıtlık/geri sayım · kanıtsız "en çok satan/#1" · uydurma müşteri/yorum sayısı. `c-tuzak`'ta ayrıca: "cures/heals/treats", "back pain", "scoliosis", "tedavi eder", "ağrıyı geçirir", "bel ağrısı", "fıtık", "skolyoz", "Rückenschmerzen", "heilt" ve izleyicinin kişisel özelliğini söyleyen kanca ("Do you have back pain?"). İmâ yolu serbest: omuzlar geride, dik duruş hissi.

## 01 ürün videosu (6–10,5 sn döngü)
- [ ] Ön-üretim kartı dolu: pazar, kanca ailesi + kanıt numarası, sahne şablonu, müzik kararı, ilk 1 sn, tatmin anı.
- [ ] Süre 6–10,5 sn; 1080×1920; son plan = ilk plan (döngü).
- [ ] Kanca ilk karede, ≤ 2 satır, TR'de ≤ 8 kelime; ürün ilk 0,9 sn'de görünür (ekransız üründe ürün planı).
- [ ] Tek tatmin/kanıt anı ≥ 0,5 sn; CTA yazısı var ve kancayla aynı anda değil (dönüşümlü).
- [ ] Ekranda fiyat yok (organik).
- [ ] Müzik ilk kareden, 1,5–2 sn rampayla girer, ani açılma yok; ses −14 ±1 LUFS; sessiz delik yok; drop duyulur (≥ 6 dB).
- [ ] Kesim dışı ani renk/görüntü sıçraması yok; son 2 saniyede gürültü artışı yok (kareleri 4 fps aç).
- [ ] Müzik stem'i ayrı dosya olarak var (müziksiz teslim yok).
- [ ] Kör jüri: ≥ 3 aynı pazar referansıyla adsız pano; bizim toplam ≥ referans medyanı − 1 (ChatGPT'de başka bir sohbette, hangisinin bizim olduğunu söylemeden).

## 02 kanca + 30 senaryo + varyasyon
- [ ] 30 senaryo; SEBEP sahnesi SONUÇ sahnesinden önce; aynı sahne eylemi ≤ 3 senaryoda; iki senaryo birbirine benzemiyor.
- [ ] Dağılım: ≥ 8 mekanizma, ≥ 6 şablon, ≥ 6 kanca ailesi, aynı aile art arda yok, ≥ 3 yazısız (K13).
- [ ] Organik seride kanca/CTA/yazılarda fiyat yok; ABD'de her videoda `kultur` dolu; TR kancası ≤ 8 kelime ve yasak kalıp yok.
- [ ] ≥ 10 kanca varyasyonu: benzersiz yazı, her aile ve kanıt numarası kütüphanede var, yalnız kanca değişiyor.
- [ ] Ön-üretim kareleri jüriye girer (referanslarla adsız pano).

## 03 hikâye videosu (25 sn)
- [ ] Ön-üretim kartı (format hikâye); kanca ilk karede; kesimler artan; ekranda fiyat/para birimi yok.
- [ ] Süre 25,0 ±0,1 sn; 1080×1920; caption dosyası var.
- [ ] Ses: müzik girişi/delik/LUFS/drop kuralları 01'deki gibi; stem var.
- [ ] Kesim dışı sıçrama ve son 2 sn gürültü yok.
- [ ] Kör jüri 01'deki gibi.

## 04 ses ve müzik
- [ ] Açılış diegetik ses olayıyla; müzik −30 dB'den başlar, 1,5–3 sn rampa, 3 sn pencerede basamak ≤ +10 dB.
- [ ] −14 ±1 LUFS; tepe ≤ −1 dBTP; delik yok; drop artışı ≥ 6 dB; drop dışı ani sıçrama ≤ +10 dB.
- [ ] Lisans kaydı: "Kurucu seçti … söz kapısı: temiz | enstrümantal", kaynak ve lisans adı; telifli/tanınmış şarkı yok.
- [ ] Seslendirme metninde yasaklı iddia yok. (Jüri sesi dinleyemez: kulak onayı kullanıcıdadır, teslim notuna yaz.)

## 05 görsel
- [ ] G0 feed karesi ≥ 1500×1500, yazısız, tek ürün/varyant, ürün uzun kenarı tuvalin %75–86'sı.
- [ ] Galeri 1:1 (≥ 3), B1 1920×800, B2 1080×1350; dört köşe aynı zemin HEX (±3); her kenarda ≥ %6 boş pay.
- [ ] Görseldeki yazı METINLER.md ile harf harf aynı (İ/ı, ş, ğ, ç, ö, ü); fazla yazı, süs çizgisi, logo, kargo/indirim/garanti yazısı yok.
- [ ] Ürün sadakati: parça sayısı, biçim, renk Ek 1 ile aynı (K1; yalnız gözle, ölçülemedi diye bırakma).
- [ ] Kör panel: referanslarla adsız pano (K3/K4 sonrası).

## 06 ürün avı
- [ ] Vaka ürünü aday tablosunda; şema ve eşik denetimi (TR: Trendyol tablosu · diğer: AliExpress tablosu) hatasız.
- [ ] Satış sayısı ürün sayfasından okunmuş (arama kartı değil); yalnız yeni-müşteri fiyatı yok; SAT ise kanıt dosyası yolu var.
- [ ] Tabloda sağlık/sonuç iddiası yok; `c-tuzak`'ta platform riski notu (PLT-01) var.

## 07 site
- [ ] Sayfa metinlerinde yalnız mağaza paketindeki onaylı iddialar; listede olmayan sayı/belge/otorite yok.
- [ ] Hız, erişilebilirlik, arama hazırlığı, müşteri gözü denetimi: ölçülemedi (araç gerekir) diye işaretle; geçti sayma.
- [ ] Kör panel: 1440 ve 390 px ilk ekran görüntüleri referanslarla adsız.
