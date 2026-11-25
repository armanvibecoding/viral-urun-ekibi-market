# Dalga 1-A raporu: ölçüm ve kapı maddeleri (2026-11-25)

Kapsam: Ekip denetimi maddeleri 1, 2, 3, 5, 6, 10, 11, 12 (kurucu: "hepsini düzelt"). Strateji değişmedi; eşik gevşetilmedi, yalnız sıkılaştırıldı.
Yollar: `<depo>` = depo kökü, `<eklenti>` = `<depo>/plugins/viral-urun-ekibi`, `<referans-kok>` = sınav çıktı kökü. Git commit ve `git add` yok; para ve tarayıcı yok.
Durum özeti: 8/8 madde YAPILDI. Kırma testi yöntemi: yeni kapı önce eski kusurlu çıktıda KALDI, sonra iyi çıktıda GEÇTİ verdi; "önce" ölçümleri git HEAD'deki eski betikle alındı.

## Madde 1: Jüri panosu tek biçim, eşleşme ayrı dizin, kopya başına klasör
Değişen: `<eklenti>/skills/cut/scripts/juri.py` (`pano` satır 284, `maskele` 196, `ocr_sizinti` 247, `esleme_yolu` 278, `kopyalari_oku` 381, `pano_gecerli` 418) · `juri_test.py` · `<depo>/scripts/sinav_kos.py` (`k_juri`: yeni API + video/kanca için `--arayuz-maske`) · `sinav_kos_test.py`.
- Her öge (video, kare klasörü, tek görsel) aynı biçimde: 20 kare, 5x4 ızgara, 1080x1536. Video: ilk 2 sn 5 kare/sn (10 kare) + kalanından 10 eşit aralıklı kare.
- Maske: üst %6, alt %20, sağ %15'in %38'den aşağısı kapanır; video ögeleri HER ZAMAN, öbürleri `--arayuz-maske` ile; bizim öge dahil hepsi aynı maskeyi alır. Kurgu kontratı K5 zaten alt %20 ve sağ %15'i boş bırakıyor.
- Maskeden sonra OCR ile `@hesap`, `1.2M`, `likes/beğeni` türü metin kalırsa `PANO GEÇERSİZ` (çıkış 1). OCR ortamı yoksa uyarı basılır: "ölçülemedi" (geçti denmez). Maskeli/maskesiz karışık pano da geçersiz.
- Eşleşme jürinin okuduğu dizinde değil: `<cikti>.gizli/_esleme.json`. Her kopya kendi klasöründe (`<cikti>/kopya-1..3/{BRIEF.md,pano/}`) ve kendi harf sırasıyla; `birlestir` kod → öge kimliği eşlemesini eşlemeden çözer. Kopya klasörü dışındaki `KOR-*.json` yok sayılır. `birlestir` pano boyutları farklıysa `PANO GEÇERSİZ` verir.
- Kırma, önce (git HEAD `juri.py`): `_esleme.json` jüri dizininde = True, pano boyutu `{(216, 384)}` (tek görsel biçimi, ızgara yok).
- Kırma, sonra: `python3 <eklenti>/skills/cut/scripts/juri_test.py` -> 39 test, 0 kaldı (ffmpeg ile; ffmpegsiz 35 + ATLANDI uyarısı). İçinde: tek biçim 1080x1536 · `_esleme.json` jüri ağacında yok · 3 kopya klasörü ve farklı harf sırası · bir pano farklı boyutta -> 1 · kopya dışı KOR yok sayıldı · karede `@hesapadi` + `1.2M likes` -> `PANO GEÇERSİZ` · video karesinde üst/alt şerit siyah · video + tek görsel karışımı -> 1, `--arayuz-maske` ile 0.
- Açık not: jüri talimatı `agents/jury.md:15` ve `agents/fixer.md:20` "`_esleme.json` aynı klasörde" varsayımıyla yazılmış; BRIEF.md yeni kopya klasörünü söylüyor ama bu iki metni rol sahibi güncellemeli (benim alanım değil).

## Madde 2: `yapilamadi` kaydı kurucu aşım cümlesi ister
Değişen: `<eklenti>/skills/captain/scripts/kapi.py:135-140,146` (+ başlık notu satır 22) · `juri.py` `yapilamadi` (`gecti: false` yazar, çıktıda aşım biçimini gösterir) · `kapi_test.py` ("referans 2 + neden" vakası bilinçli olarak 0 -> 1 yapıldı, kurucu onaylı; yeni vaka: aynı kayıt + `KARARLAR.md` aşım cümlesi -> 0 `AŞILDI`).
- Önce: kayıt `GEÇTİ` ("JÜRİ YAPILAMADI notuyla"). Sonra: `hukum@V` KALDI "kurucu aşım cümlesi şart"; kredi geçişinde de `yapilamadi` kaydı KALDI sayılır.
- Komut: `python3 <eklenti>/skills/captain/scripts/kapi_test.py` -> 53 test, 0 kaldı. Not: dosyanın başında (bu görevden önce) 4 vaka zaten kırıktı; sebep `senaryolar` fikstüründe `kanca_sorusu`/`cevap_an` eksikliğiydi, fikstür düzeltildi, kapı değişmedi.
- Açık not: `skills/studio/SKILL.md:62` ve `skills/cut/SKILL.md:70` hâlâ "kapı notla geçer" diyor; metin rol sahibinde.

## Madde 3: Geçme kuralına `dururdum` / `gonderirdim` tabanı
Değişen: `juri.py:75` (`ALAN_TABAN`) ve `birlestir` (satır ~498). Rapordaki değer 6.
- Önce (HEAD `juri.py`, toplam 9,5 · dururdum 5,5 · hiçbir alan < 5): `GEÇTİ V01`, çıkış 0.
- Sonra: `KALDI V01 … taban < 6: dururdum`; gonderirdim 5,5 için de aynısı; tam 6/6 -> GEÇTİ (eşik dahil). Testler `juri_test.py` içinde (3 vaka).

## Madde 5: Kontrat kapısı satır sayısı -> alan denetimi
Değişen: `kapi.py:163-199` (`k_kontrat`, `KONTRAT_ZORUNLU`) · `kapi_test.py` (fikstür `KONTRAT_IYI` + 3 kırma vakası).
- Şart: `İmza:` (tarihli) ve `İzleyici:` dolu · K1, K2, K9, K10 satırları var · her K satırında alan/kural/eşik/ölçüm dolu · `<...>` yer tutucu yok (kod aralığı içindeki `<drop>` yer tutucu sayılmaz) · en az 5 K satırı.
- Önce (5 satırlık "K1 süre 12-15 sn" kontratı): kapı GEÇTİ. Sonra: KALDI "`İmza:` satırı yok; zorunlu K1/K2/K9/K10 satırı yok". Şablondan kopyalanıp doldurulmamış dosya -> KALDI (yer tutucu). 9 gerçek ürün kontratı (arşivdeki seri klasörleri) GEÇTİ.

## Madde 6: Plan 0.6 Ö1 kapıları
Değişenler: `<eklenti>/skills/cut/scripts/kurgu_kontrol.py` (ESIK `ilk2_*`, `ilk2_olay_say` 151, kural 9-10 satır 398-406, bayrak `--kaynak` ve `--malzeme-zorunlu`) · yeni `malzeme_kaynak.py` · yeni `kurgu_kontrol_test.py` (10 test) · `<eklenti>/skills/builder/gorseller/scripts/ocr_kontrol.py` (+ yeni `ocr_kontrol_test.py`) · `<depo>/scripts/sinav_kos.py` (`k_kanit_sizinti` 340, `k_mobil_ekran` 361) · yeni `<eklenti>/ortak/mobil_ekran.py` · yeni `<eklenti>/ortak/indirme_al.py` (+ `indirme_al_test.py`).
1. İlk 2 sn kare farkı (`ilk2sn`): 54x96 gri, 10 kare/sn; son olaydan fark > 15 olan "belirgin değişim" >= 3 (el titremesi olay sayılmaz). KALİBRASYON NOTU: plandaki ">= 2" eşiği 01 tur3/a-kolay'ı (2 olay) ayırmadı; 9 sınav videosunda iyiler 5-8, kötüler 1-2 olay verdiği için eşik 3 (sıkılaştırma).
   - Önce (HEAD kurgu_kontrol): tur3/a-kolay çıkış 0. Sonra: çıkış 1 `HATA [ilk2sn] ... yalnız 2 belirgin kare değişimi`. İyi: tur3/b-zor (6 olay) çıkış 0.
2. Klip <-> malzeme (`malzeme`): `urun/urun_elde/telefon/sokum` etiketli klibin `kaynak` metni KAYNAK.tsv `dosya` satırına bağlanmalı; vaka eşleşir (başka vakanın klibi = yanlış ürün), `kullanma` işaretli satır sayılmaz. KAYNAK.tsv yoksa UYARI (ölçülemedi); `--malzeme-zorunlu` ile HATA.
   - Önce: tur2/b-zor çıkış 0. Sonra: çıkış 1 `HATA [malzeme] klip b-tuy-10558368 'urun_elde' etiketli ama kaynağı KAYNAK.tsv'de yok (etiket: "stok Pexels (LISANS.md)")`. İyi: tur3/b-zor çıkış 0.
3. OCR birebir: Latin metinde (Türkçe özel harf içermeyen öğe) normalize beklenen, okunan satırda aynen geçmeli; Türkçe harfli öğe Tesseract yoksa KALDI değil `olculemedi` (çıkış 2, rapor "yazım hatası bulunmadı, ölçülemedi").
   - Önce (HEAD): "KLEBEBLAT ABZIEHN" çıkış 0, "KLEBEBLATT ANZIEHEN" çıkış 0 (kaçıyordu). Sonra: ikisi çıkış 1; doğru metin 0; "HAARE ENTFERNEN" 1; "SOĞUKKEN SİYAH" çıkış 2 olculemedi. Gerçek tur1 b-zor galerisi: 6/6 görsel çıkış 0.
   - Komut: `~/.local/share/viral-urun-ekibi/ocr-venv/bin/python <eklenti>/skills/builder/gorseller/scripts/ocr_kontrol_test.py` -> 5 test, 0 kaldı. `<depo>/moduller/magaza-kurucu/.../ocr_kontrol.py` kopyasına DOKUNMADIM (kopya senkronu ayrı iş, denetim #29).
4. Kanıt anı / iç dil sızıntısı (`sinav_kos.py` 07, `kanit_ani_sizinti`): `## The moment / Der Moment / Kanıt` başlığı, cümle başı "Kanıt", `kanıt anı` iç terimi ve vaka `kanit_ani` cümlesinin (>= 4 sözcük) sitede aynen geçmesi = KALDI.
   - Önce: 07 tur1 üç vaka mekanik GEÇTİ (çıkış 3). Sonra: b-zor `«. Kanıt» -> cümle 'Kanıt' etiketiyle başlıyor`, c-tuzak `«## Der Moment»`; ayrıca a-kolay `«## The moment»` da KALDI (aynı sınıf; plan yalnız b ve c'yi saymıştı). İyi: iç terimler silinmiş aynı metin GEÇTİ.
5. Mobil ekran yardımcısı `mobil_ekran.py`: `ekran` = geniş pencerede 390 px iframe'i keser; `kontrol` = aynı sayfayı iframe ile çizip piksel farkı > 6 ise `MOBİL EKRAN YANLIŞ ALINMIŞ`, `scrollWidth` > 390 ise `TASMA`. Chrome yoksa `olculemedi` (çıkış 2).
   - Önce: kapı yoktu (07 tur1 `-390.png` yöntem hatası lider gözüyle bulundu: 500 px düzen 390'a kırpılmış, yazı sağdan kesik). Sonra: 6/6 eski ekran çıkış 1 (ortalama fark 12,5); `ekran` ile yeniden alınan ekran fark 0,00, çıkış 0, scrollWidth 390.
6. İndirme alımı `indirme_al.py` (zaman + boyut + ad deseni): yalnız `--baslangic` sonrası inen, `--min-boyut` üstü, boyutu 1 sn arayla sabit, `.crdownload/.part` olmayan dosyayı HEDEFE KOPYALAR; eski dosyaya dokunmaz, `--tasi` bile yalnız yeni dosyayı taşır; hedefte aynı ad varsa üzerine yazmaz.
   - Önce: eski indirme betiği klasördeki eski kurucu dosyasını taşımıştı (kapı yoktu). Sonra: `python3 <eklenti>/ortak/indirme_al_test.py` -> 7 test, 0 kaldı (eski dosya + uyan ad deseni -> çıkış 1, dosya yerinde, boyut ve zaman aynı).

## Madde 10: Lisans kapısı
Değişen: `kapi.py` (`k_lisans` 246; kapı listesi `lisans@V`, `liste` 9 kapı) · yeni `malzeme_kaynak.py` (KAYNAK.tsv sözleşmesi) · `kapi_test.py` (fikstür + 7 kırma vakası).
- KAYNAK.tsv yeni sütunlar: `lisans` (kurucu | uretim | stok | yazili), `kullanim` (yayin), `yapay_mi` (evet | hayir), `bakildi` (tarih). Boş sütun, `sinav-ici`, `kullanim=sinav`, `kullanma` işaretli kaynak, etiketsiz klip, kayıtsız klip, KAYNAK.tsv yok = `lisans@V` KALDI (karar kurucuda, kayıt kapıda).
- Önce: lisans kapısı yoktu. Sonra: 01 tur3/b-zor (gerçek tedarikçi klibi, KAYNAK.tsv'de lisans sütunları yok) -> KALDI "lisans boş / kullanim boş / yapay_mi boş / bakildi boş" (SINAV-01-TUR3: "yazılı ticari lisans yok" ile tutarlı); tur2/b-zor -> KALDI "kaynağı KAYNAK.tsv'de yok". İyi: sütunları dolu kayıt GEÇTİ (`kapi_test.py` y0).
- Not: `<referans-kok>/sinav-kosu/tedarikci/KAYNAK.tsv` dosyasına yeni sütunlar eklenmedi (kurucu kararı: lisans değeri benim yazacağım bir şey değil).

## Madde 11: `sinav_kos.py --hepsi`, `surum_oncesi.sh`, `paketle.sh` şartı
Değişen: `sinav_kos.py` (`hepsi` 692, `kos_ozellik` 649, `tur_klasoru` 683) · yeni `<depo>/scripts/surum_oncesi.sh` · `<depo>/scripts/paketle.sh` (0. adım).
- `python3 scripts/sinav_kos.py --hepsi <cikti_koku> [--tur tur3] [--referans-kok K]`: 7 özellik, her biri kendi en son turunda; tek satır özet `HEPSİ: 7 özellik · GEÇTİ n · KALDI n · ölçülemedi/bekliyor n · çıkış X`. Çıktısı olmayan özellik KALDI. Önceki `SONUC.md` ezilmez, `SONUC-HEPSI.md` yazılır. Çıkış 0/1/3.
- `surum_oncesi.sh`: birim testleri (çıkış 3 = ölçülemedi ayrı sayılır) + `--hepsi` + `anonim_kontrol.sh`; çıkış 0 yalnız hepsi GEÇTİ ise. Sınav çıktı kökü yoksa çıkış 2.
- `paketle.sh`: `surum_oncesi.sh` çıkış 0 değilse paket üretilmez (çıkış 1). Geliştirme taslağı için `PAKETLE_TASLAK=1` (açık uyarı basar). DİKKAT: bu yüzden başka oturumların `paketle.sh` koşuları artık `SINAV_CIKTI_KOK` ya da `PAKETLE_TASLAK=1` ister.
- Önce: 7 sınavı koşan tek komut ve paketleme şartı yoktu. Sonra, kırma: `sinav_kos_test.py` "boş kök -> 1, 7 KALDI" ve "yalnız 04 çıktısı var -> 04 GEÇTİ, 6 KALDI, çıkış 1".
- Bugünkü gerçek durum (`--hepsi <referans-kok>/sinav-kosu`, yeni kapılarla): `HEPSİ: 7 özellik · GEÇTİ 2 (04, 06) · KALDI 2 (01, 07) · ölçülemedi/bekliyor 3 (02, 03, 05) · çıkış 1`. Yani yeni kapılar mevcut çıktılarla sürüm engeller (beklenen).
- UYARI (veri): `--hepsi`'nin ilk deneme koşusu, bayrak `SONUC-HEPSI.md`'ye taşınmadan önce, 7 eski `SONUC.md` dosyasını (01 tur3 · 02 tur2 · 03 tur2 · 04 tur3 · 05 tur1 · 06 tur2 · 07 tur1) YENİ kapılarla üretilmiş içerikle üzerine yazdı. Eski içerik bu raporlardaki tablolarda duruyor: `SINAV-01-TUR3-RAPOR.md`, `SINAV-02-RAPOR.md`, `SINAV-04-RAPOR.md`, `SINAV-05-RAPOR.md`, `SINAV-06-RAPOR.md`, `SINAV-07-RAPOR.md`. Hata düzeltildi (artık ezmiyor).

## Madde 12: Defterde `KAÇAK` kaynağı ve 4 kaçağın kırma testleri
Değişen: `<depo>/docs/gelistirici/GELISTIRME-DEFTERI.json` (`kaynak_turleri.KAÇAK` tanımı + `kacaklar` 4 kayıt: 01a, 01b, 07c, 07d; her birinde kaçıran kapı, yeni kapı, eski/yeni/iyi çıktı) · yeni `<depo>/scripts/kacak_kirma_test.py`.
- Komut: `python3 scripts/kacak_kirma_test.py --referans-kok <referans-kok>` (FFMPEG_DIZIN/PATH'te ffmpeg gerekir) -> 9 test, 0 kaldı, çıkış 0:
  - (a) tur2/b-zor KALDI `[malzeme]` · tur3/b-zor GEÇTİ
  - (b) tur3/a-kolay KALDI `[ilk2sn]`
  - (c) 07 b-zor ve c-tuzak `kanit_ani_sizinti` KALDI · iç terimler silinince GEÇTİ
  - (d) 6 eski mobil ekran KALDI · yeniden alınan ekran GEÇTİ
- Referans kökü verilmezse çıkış 3 `OLCULEMEDI` (geçti sayılmaz).

## Test özeti (bu görev sonu)
Bütün `*_test.py` ve `kirma_testi.py` dosyaları koşturuldu (ffmpeg için `FFMPEG_DIZIN`): juri_test 39/39 · kapi_test 53/53 · kurgu_kontrol_test 10/10 · ocr_kontrol_test 5/5 · indirme_al_test 7/7 · sinav_kos_test 81/81 · sozlesme_test 49/49 · karne_test 18/18 · hikaye 17/17 · bazaar 71/71 · teklif 34/34 · on_uretim_karti 20/20 · hunter 16/16 · kanca_varyasyon 8/8 · cut kendini_test, spy kendini/toplayıcı geçti.
Bu görevle ilgisiz, koşulamayanlar: `ortak/excel_test.py` çıkış 3 (openpyxl kurulu değil, ortam; `surum_oncesi.sh` bunu "ölçülemedi" sayar ve sürümü engeller); `skills/spy/scripts/geri_test.py` bağımsız değişken ister (kendi başına test değil, `surum_oncesi.sh` dışarıda tutar); `moduller/magaza-kurucu/tests/test_ocr_kontrol.py` RapidOCR sistem Python'unda yok, ATLANDI.
Eski, bu görevden önce kırık: `kapi_test.py` 4 vaka (senaryo fikstürü eksik alan; düzeltildi), `test_hikaye.py` 1 vaka (PATH'te ffmpeg yoktu; ortam).

## Değişen / eklenen dosyalar (özet)
Değişen: `skills/cut/scripts/{juri.py,juri_test.py,kurgu_kontrol.py}` · `skills/captain/scripts/{kapi.py,kapi_test.py}` · `skills/builder/gorseller/scripts/ocr_kontrol.py` · `<depo>/scripts/{sinav_kos.py,sinav_kos_test.py,paketle.sh}` · `<depo>/docs/gelistirici/GELISTIRME-DEFTERI.json`.
Eklenen: `skills/cut/scripts/{malzeme_kaynak.py,kurgu_kontrol_test.py}` · `skills/builder/gorseller/scripts/ocr_kontrol_test.py` · `ortak/{mobil_ekran.py,indirme_al.py,indirme_al_test.py}` · `<depo>/scripts/{surum_oncesi.sh,kacak_kirma_test.py}` · bu rapor.
Dokunulmayan: `agents/*.md`, `ortak/roller/**`, `ortak/ekip.md`, `skills/*/SKILL.md`, `ortak/sinav/**/vaka.json`.
