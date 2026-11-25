# Dalga 2-A raporu: betik maddeleri (2026-11-25)

Kapsam: Ekip denetimi 13, 17, 22, 24 + Dalga 1-B'den devredilen 3 iş. Git commit/add yok; para ve tarayıcı yok. Yollar: `<depo>` depo kökü, `<eklenti>` = `<depo>/plugins/viral-urun-ekibi`, `<referans-kok>` sınav çıktı kökü (SONUC.md ve eski çıktılar EZİLMEDİ).
Durum: 13 YAPILDI · 17 YAPILDI · 22 YAPILDI (kurulum başarılı) · 24 YAPILDI (5 betik) · devredilen 3/3 YAPILDI. Eşik gevşetilmedi.
kurucuyu ilgilendiren: yok (yalnız aşağıdaki "metin önerisi" listesi lidere).

## Madde 13: ön uçuş (`<eklenti>/ortak/on_ucus.py`, test `on_ucus_test.py`)
`on_ucus.py hepsi --ozellik 07 [--is is/NN] [--referans-kok K]` · `malzeme` · `referans` · `arac` · `kutuphane`. Çıkış 0 hazır · 1 ÜRETİME BAŞLAMA · 3 başlanabilir ama kapılar ölçülemez kalacak.
- malzeme: KAYNAK.tsv yok / satırın dosyası yok / (`--yayin`) lisans sütunları boş; referans: ≥ 3 pazar-uyumlu çözülen pano; araç: ffmpeg, Pillow, OCR, Tesseract, Node ≥ 22.19, Chrome, Lighthouse+axe, openpyxl; kütüphane: kanca K1–K15 başlıkları, sahne S1–S10, 6 pazar kartı, kartın kendi şablon sınaması.
- Kırma (V6'nın 6 kaybından 5'i üretimden önce yakalanır): 01 malzemesiz → çıkış 1; 02 K14/K15 başlığı silinmiş kütüphane → çıkış 1 `K14, K15`; 07 referans yok → 1 `0/3`; 07 ölçüm aracı yok → 1; 05 Tesseract yok → 3 (K2 TR ölçülemez). İyi girdiler çıkış 0.
- Komut: `python3 on_ucus_test.py` → 14 test, 0 kaldı. Gerçek veride: `hepsi --ozellik 07` → 3 referans eksik (0/3), çıkış 1 (ölçüt doğru: referans yuvası boş).

## Madde 17: şema `null` + `eksik[]` (kaynak `<depo>/moduller/magaza-kurucu/src/ortak/sozlesme/`, kopya `sozlesme_esitle.py` ile eşitlendi)
- `magaza-paketi.schema.json:` `eksik[]`, `marka.ad_kaynak`; `marka.ad`, `urun.baslik`, `urun.fiyat`, `urun.para`, `gorseller` null olabilir. `urun-paketi.schema.json:` `eksik[]`. `paket_dogrula.py` `eksik_kontrol` (yeni): null ama `eksik[]`'te yok = HATA; eksik[]'te ama dolu = HATA; fiyat 0/negatif/sayı değil, yer tutucu ad/dosya (`yok-yer-tutucu.jpg`, `<…>`, lorem…), `marka.ad_kaynak` yok ya da "jenerik/tahmin" = HATA; dürüst eksik paket GEÇER ve `UYARI: EKSİK: …` basar; `--tam` eksik de HATA (yayın). urun-paketi: kanıt yoksa `EKSİK: kanit (kanıt: yok)`.
- `ortak/paket.py`: `dogrula … --tam`; `magaza-oku` null fiyat/ad/görselde `BİLİNMİYOR` + EKSİK satırı yazar (0 TRY basmaz); `urun-yaz` kanıtsızsa "kanıt yok" basar. `captain/scripts/kapi.py` yayın sözleşme kapısı `--tam`. `scripts/sinav_kos.py` 07 yeni kapı `paket_sozlesme` (KALDI / dürüst eksik = olculemedi).
- Kırma (önce kötü KALDI, sonra iyi GEÇTİ): `scripts/sozlesme_test.py` 63/63 (14 yeni: fiyat 0, "0,00 TL", yer tutucu görsel, kaynaksız ad, `<marka adı>`, null+eksik yok, çelişki, `--tam`…). Eski 07 tur1 üç vakanın paketi artık `paket.py dogrula magaza` → `KALDI (3 hata)`. `kapi_test.py` yayın: eksik paket → 1, fiyat 0 → 1, tam paket → 0. `sinav_kos_test.py`: fiyat 0 / yer tutucu görsel / kaynaksız ad → `paket_sozlesme` KALDI çıkış 1; null+eksik → olculemedi çıkış 3.
- Not (kırıcı değişiklik): `marka.ad_kaynak` artık zorunlu; `ornek/magaza-paketi.json` güncellendi. Belge tablosu = şema testi gereği `arayuz-sozlesmesi.md` (kaynak + kopya) tablolarına `eksik` ve `ad_kaynak` satırı eklendi (metin kuralı değil, sözleşme tablosu; lider görsün).

## Madde 22: Probe yerel ölçüm (`<eklenti>/ortak/web_olcum.py`, `web_olcum_axe.mjs`, `web_olcum_test.py`)
- arac-ekle kapısı: lighthouse@13.6.0 (GoogleChrome/lighthouse; npm bakımcıları Chrome ekibi; 2026-10-27), axe-core@4.14.0 (dequelabs; Lighthouse'un kendi sabit bağımlılığı), puppeteer-core@25.18.1 (Lighthouse bağımlılığı, tarayıcı indirmez). Yer: `~/.local/share/viral-urun-ekibi/web-olcum/`, `npm install --save-exact --ignore-scripts`, global kurulum yok. Yetki: yalnız 127.0.0.1'e açılır, yazma yok. Sınama: `lighthouse --version` 13.6.0; uçtan uca yerel sayfa ölçüldü; araç/sürüm sabit değilse `kontrol` çıkış 3. Kurulum BAŞARILI (YAPILAMAZ yok).
- Kapılar: hiz (Lighthouse mobil, medyan N koşu): LCP ≤ 2500 ms, CLS ≤ 0,1, TBT ≤ 200 ms (INP vekili); erisim (axe, WCAG 2.0–2.2 A/AA etiketleri, 390 ve 1440 px): tek ihlal = KALDI, `incomplete` UYARI. Etiket "yerel" (laboratuvar; canlı mağaza yerine geçmez); URL verilirse "canlı".
- Bağlama: `scripts/sinav_kos.py` `k_web_olcum`: 07 `hiz_cwv` ve `erisim_wcag` artık `ekran/*.html`/`site/*.html`'i (ya da `canli-url.txt`) ölçer; HTML yoksa olculemedi. `SINAV_WEB_KOSU` (varsayılan 3).
- Kırma: `python3 web_olcum_test.py` → 7/7: kontrastı bozuk sayfa `erisim` çıkış 1 (`color-contrast`, 1,91:1); temiz sayfa 0; ana iş parçacığını 3 sn kilitleyen sayfa `hiz` çıkış 1 (TBT); hafif sayfa 0; araç klasörü yok / sürüm 9.9.9 → çıkış 3. `sinav_kos_test.py` 07: temiz HTML hiz+erisim GEÇTİ (`[yerel]`), bozuk kontrast `erisim_wcag` KALDI, kilitli sayfa `hiz_cwv` KALDI.

## Madde 24: betiğe taşıma (V3 tablosu)
| V3 adımı | Betik | Kırma / kanıt |
|---|---|---|
| Panel medyanı + puan tablosu | `skills/builder/gorseller/scripts/panel_medyan.py` (+ `panel_medyan_test.py`) | elle hesap (toplam 6,0, medyan sıra 3, yapay 2/3); aynı girdi iki koşu bayt bayt aynı; 2 kopya, `pano_sorunu` dolu, puan 11, sıra eksik, hepsine aynı puan → çıkış 1; 10/10 |
| Sentinel beklenen metin | `beklenen_uret.py` (METINLER.md → `<ad>.txt`) | `<referans-kok>` 05 tur1 a-kolay METINLER.md → 6/6 dosya el yazımıyla bayt bayt AYNI |
| Copy kelime/karakter, İ/I | `copy_kontrol.py` (+ `metinler.py`, `copy_kontrol_test.py`) | başlık 8 kelime, etiket 21 karakter, açıklama 13, kare 60 kelime, uzun tire, ünlem, ondalık nokta, büyük satırda küçük i, BITIŞ↔bilgi "BİTİŞ" → 1; doğru metin 0; bilgide olmayan İ/I'li kelime → 3 (ölçülemedi); 18/18. Sınır: İ/I yalnız doğrulanmış bilgi dosyasındaki kelimeler için ölçülür |
| Mixer anları / plan | `skills/cut/scripts/ses_plan.py` (+ test) | drop = ilk flaş (3,2 sn, "tahmin: ölçülmedi" işaretli), kanca 0. sn, riser drop−0,2'de biter, 8 punch/8 sn → ≤ 5 efekt, bozuk ayar → 1; müzik drop'u uydurulmaz (`<MUZIK_DROP_SN>`, komut ÇALIŞTIRILAMAZ); 12/12 |
| Yazı taşması | `skills/cut/scripts/yazi_tasma.py` (+ test) | tek uzun kelime / `yazilar[]` taşması → 1; kısa ve bölünen kanca 0; yazı yok → 3; 6/6 |
Zaten vardı (D1): forge indirme alımı `indirme_al.py`, kontrat/klip↔kaynak (`kapi.py`, `malzeme_kaynak.py`), mobil ekran `mobil_ekran.py`, Decoder `desen_say.py`.

## Devredilenler
1. `SAT-KOŞULLU`: `hunter/scripts/firsat_kontrol.py` (denetle: eksik tek kanıt şart, "numune ve alıcı videosu" gibi çoklu eksik = HATA, ELE sebebiyle birlikte HATA), `hunter/scripts/excel_hazirla.py` (→ "SAT (koşullu)", kanıt dosyası yoksa İZLE), `bazaar/scripts/bazaar_kontrol.py` + `bazaar/scripts/excel_hazirla.py` ve `ortak/excel_yaz.py` (skeptic yazımı kabul, `SAT-KOŞUL` gibi uydurma ret). Testler: hunter `kirma_testi.py` 23/23, bazaar `kirma_testi.py` 75/75, `excel_test.py` 68/68.
2. `KİM DENETLEDİ` / `ÖZ-DENETİM`: `scripts/sinav_kos.py` `k_denetleyen` (her özellikte, SADAKAT/KAPI/OCR/ELESTIRI/KOR/SES… raporları): satır yok / `ÖZ-DENETİM` / ÜRETEN = denetleyen → `kim_denetledi` olculemedi; bağımsız rol adı → GEÇTİ. 05 tur1 gerçek SADAKAT.md → olculemedi. `sinav_kos_test.py` 4 yeni test.
3. `excel_test.py` openpyxl: dürüst yol seçildi = openpyxl'i ayrı venv'e kur (arac-ekle: PyPI openpyxl==3.1.5 + et-xmlfile==2.0.0, `--only-binary`, `~/.local/share/viral-urun-ekibi/excel-venv`, global yok) ve test sistem Python'unda yoksa kendini o venv ile yeniden koşar; venv de yoksa çıkış 3 "ÖLÇÜLEMEDİ" (atla-ve-geç değil). Sonuç: test artık gerçekten koşuyor (68 test). Kırma: `EXCEL_TEST_VENV=1` ile venv devre dışı → çıkış 3.

## Yan bulgu (düzeltildi)
`skills/captain/scripts/kapi_test.py` her koşuda ~600 MB geçici klasör bırakıyordu (24 sızıntı = diski doldurdu, birkaç testi "No space left on device" ile düşürdü). Başarılı koşuda temizliyor. Ölçüm: önce sızıntı 24 klasör ≈ 14 GB, sonra 0.

## Test çıkışları (son koşu, `SINAV_REFERANS_KOK` ayarlı)
Bütün `*_test.py`/`kirma_testi.py`/`test_hikaye.py` (27 dosya) + `kacak_kirma_test.py` + `sozlesme_test.py` çıkış 0 (`test_hikaye.py` tam suite içinde bir kez 1 verdi: disk doluydu; tek başına 17/17, çıkış 0). `scripts/sinav_kos_test.py` 96/96, 0 kaldı. `scripts/kacak_kirma_test.py` (SINAV_REFERANS_KOK ile) 0. `scripts/sozlesme_test.py` 63/63. `anonim_kontrol.sh` çıkış 0.
`surum_oncesi.sh <referans-kok>/sinav-kosu` (gerçek eski çıktılar): çıkış 1 (beklenen). Birim 26 GEÇTİ / 1 KALDI (sinav_kos_test: aşağıdaki test hatası, düzeltildi, sonra 96/96) / 0 ölçülemedi: openpyxl artık ölçülüyor. Sınav: 01 KALDI (D1 kapıları: ilk 2 sn, jüri), 02 bekliyor, 03 ve 05 olculemedi, 04 ve 06 GEÇTİ, 07 KALDI (eski tur1 çıktısı yeni `paket_sozlesme` kapısında: fiyat 0, yer tutucu görsel, kaynaksız ad; yani eski kusur yakalanıyor).
Test hatası düzeltildi: `sinav_kos_test.py` `kos()` dış `SINAV_REFERANS_KOK`'u temizliyor (01 "referans yokken olculemedi" testleri ortam değişkeniyle bozuluyordu; surum_oncesi.sh onu ayarlayınca KALDI veriyordu). Önce: ortam ayarlıyken 4 kaldı; sonra 0 kaldı.
Not: `surum_oncesi.sh` `<referans-kok>/sinav-kosu/*/tur*/SONUC-HEPSI.md` dosyalarını (koşucunun kendi türev dosyası) yeniden yazar; SONUC.md dokunulmadı.

## Metin önerisi (SKILL/agent/references; lider uygular)
- `ortak/roller/probe/hiz.md:8` ve `erisim.md` "Ölçüm": → "Araç: `python3 ${CLAUDE_PLUGIN_ROOT}/ortak/web_olcum.py hiz|erisim <html|klasör|URL>`; çıktı etiketi `yerel` ise laboratuvar ölçümüdür, canlı mağaza ölçümü değildir; araç yoksa `olculemedi: araç yok` yaz."
- `agents/probe.md`: aynı cümle + `web_olcum.py kontrol` ve `kur` komutları.
- `ortak/sinav/07-site/OLCUT.md` §i tablosu: hiz_cwv/erisim_wcag satırı "(betik yok)" → "`ortak/web_olcum.py` (yerel Lighthouse+axe; eşik LCP ≤ 2500 ms, CLS ≤ 0,1, TBT ≤ 200 ms; axe WCAG 2.2 AA 0 ihlal)"; yeni satır `paket_sozlesme` (`paket.py dogrula magaza`); "Ölçülemeyenler": dört kapı yerine ikisi (arama_merchant, donusum_kullanilabilirlik).
- `skills/captain/SKILL.md` (Aşama 0/üretim öncesi): "Üretime başlamadan `python3 ${CLAUDE_PLUGIN_ROOT}/ortak/on_ucus.py hepsi --is is/NN-urun` çalıştır; çıkış 1 ise başlama."
- `agents/panel.md` Çıktı: "`KOR-<kopya no>.json` yaz (puanlar{kod:{tipografi,renk,kompozisyon,urun,metin,nise,mobil}}, sira, yapay, ajans, pano_sorunu); medyanı `panel_medyan.py` çıkarır" · `agents/director.md:21`: "puan tablosu: `panel_medyan.py <tur> --esleme pano/_esleme.json` çıktısı".
- `ortak/roller/sentinel/yazim.md` Yap 1: "`beklenen_uret.py METINLER.md --cikti gorseller/`".
- `agents/copy.md` Sınırlar: "Sınırları `copy_kontrol.py METINLER.md --pazar TR` sayar; çıkışı rapora yaz."
- `agents/mixer.md` Yöntem 1: "Anların taslağı: `ses_plan.py VNN.json`; sen onaylar/düzeltirsin; müzik drop'unu `ses_olc.py` ile ölç."
- `skills/cut/SKILL.md`: kurgudan sonra `yazi_tasma.py ayar.json` çıkış 0 şartı.
- `agents/builder` / magaza-ekibi: `magaza-paketi.json` bilinmeyen değer için `null` + `eksik[]`, marka adı için `marka.ad_kaynak` yazar (fiyat 0 / yer tutucu yazmaz).
- `ortak/rapor-sablonu.md` madde 5 sonu: "Raporda `ÜRETEN: <rol>` satırı da yer alır; koşucu `KİM DENETLEDİ` ile karşılaştırır."
- `agents/story.md` (B devri #2): kota cümlesi `senaryo_kontrol.py` ≥ 8 mekanizma / ≥ 6 şablon kapısıyla çelişebilir: bu dalgada DOKUNULMADI (listede yoktu).
- `skills/captain/referans/kurulum-kontrol.md`: web_olcum (Node ≥ 22.19, Chrome, `web_olcum.py kur`) ve excel-venv satırı.
