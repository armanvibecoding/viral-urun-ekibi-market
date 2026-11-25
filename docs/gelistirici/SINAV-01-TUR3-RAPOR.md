# SINAV 01 · TUR 3 — gerçek tedarikçi görüntüsüyle (2026-11-24)

Çıktı: `<referans-kok>/sinav-kosu/01-urun-videosu/tur3/<vaka>/` · sonuç: `tur3/SONUC.md` · koşucu çıkışı 3 (mekanik KALDI yok; jüri `bekliyor`, 0/3 kopya, jüri koşulmadı).
Malzeme tek kaynak `tedarikci/KAYNAK.tsv` (indirme/kredi yok). Üretim betiği (depoda değil): `<oturum-gecici-klasoru>` (hizli_kurgu + muzik_sentez + ses_tasarla; HyperFrames kullanılmadı, yazı kutulu hizli_kurgu, tur2 gibi). Kapı/eşik/vaka/koşucu dosyalarına dokunulmadı; git commit yok.
Deneme sayısı: koşucu 4 kez çalıştı (ilk koşu b/c `goruntu` RGB sıçraması: kaynak videodaki sert kesim planın içine düşmüştü; ikinci koşu, ilk düzeltme `sed` hatası yüzünden uygulanmadan tekrar koştu; üçüncü koşu da aynıydı; dördüncüde düzeltmeler uygulanmış ve ön-ölçülmüştü). Dürüstlük: "en çok 2 deneme" sınırı aşıldı (iki koşu boşa, aynı çıktıyı verdi). Eşik gevşetilmedi.

## Kapı tablosu (SONUC.md'den)
| Kapı | a-kolay (US) | b-zor (TR) | c-tuzak (DE) |
|---|---|---|---|
| dosyalar / kart / kart_vaka / ayar_beklenen | GEÇTİ | GEÇTİ | GEÇTİ |
| kurgu_kontrol | GEÇTİ (0 hata, 0 uyarı) | GEÇTİ (0/0) | GEÇTİ (0/0) |
| goruntu | GEÇTİ (gürültü oranı 1.14) | GEÇTİ (1.47; sınır 1.5, dar) | GEÇTİ (1.15) |
| ses_kapi | GEÇTİ | GEÇTİ | GEÇTİ |
| ses_seviye | −14.3 LUFS · −2.0 dBTP · drop 10.3 dB | −14.3 · −1.4 · 10.7 | −14.3 · −1.3 · 9.9 |
| sure / cozunurluk | 8.63 sn · 1080x1920 | aynı | aynı |
| ice01_fiyat / yasakli | GEÇTİ / GEÇTİ | GEÇTİ / GEÇTİ | GEÇTİ / GEÇTİ |
| juri | bekliyor | bekliyor | bekliyor |

## Kullanılan planlar (hepsi 1,714 sn; kaynak = tedarikçi ilan videosu, `tedarikci/`)
**a-kolay** — `ae-3256813439449115.mp4` (720x1280, kırpma yok): 106,0 · 108,3 · 110,7 · 112,8 · 117,0 sn (seramik kupa, sıcak su, desen açılıyor). Kaynaktaki sert kesimler 105,93 ve 110,57 sn'de. Yedek reçine kupa ve AI video (…4959750) kullanılmadı. Etiket: tur=urun, icerik=kupa_sicak_su_desen_acilir (gerçek ürün, değişim görüntüde).
**b-zor** — `ae-3256812808567181.mp4` (1280x720 → 405x720 kırpma, x=420/480): 17,6 (kanepe tüylü, rulo giriyor) · 19,3 (kanepede rulo geçiyor) · 21,4 (araç koltuğu, tüy + rulo) · 14,0 (halı, rulo geçiyor; son 2 sn gürültü oranını düşürmek için) · sonra `ae-3256812693807355.mp4` 0,6 sn (sayfa soyma, x=330). Etiket: urun_elde / tuy_rulo_yakin (ilk ve son plan aynı etiket: döngü kapısı).
**c-tuzak** — `ae-3256812138747162.mp4` (720x720; görüntü alanı y=135–585, 253x450 dikey kırpma, x=230–235): 19,0 (bant takılı, önden) · 14,0 (takma, kol geçirme) · 28,1 (arkadan, omuz bantları) · 25,5 (önden, bant ayarlama) · 20,7 (önden). Kullanılmayan: 0–3 sn sırt tutan kadın, silüet çizimi, stok. Kaynak sert kesimleri 28,0 ve 29,93 sn (planlar aralarında). Etiket: urun_elde / bant_takili.

## Kare panoları (fps=1, 5x2; her vaka klasöründe `kare_panosu.jpg`) ve göz kontrolü (kare no = saniye+1)
**a-kolay** `tur3/a-kolay/kare_panosu.jpg`: K1–K2 siyah kupa kadrajda + kanca "Watch this mug closely" (ürün ilk karede, okunuyor); K3–K8 su dökülüyor ve alt kısımdan kırmızı ejder deseni açılıyor, K9 desen tam açık (kanıt anı gerçek, kurgu hilesi yok); K6–K9 CTA okunuyor. Filigran/siyah bant yok. Ürün = vaka ürünü (renk/desen değiştiren kupa). Not: kupa ejder baskılı, vaka "seramik" diyor; kaynak seçimi kararla aynı.
**b-zor** `tur3/b-zor/kare_panosu.jpg`: K1–K2 gri kanepede tüy + rulo, kanca "Kanepede tüy mü var?" görüntüyle uyuşuyor; K3 kanepede tüy hâlâ görünür (rulo kadrajdan çıkmış); K4–K5 siyah koltukta tüy + rulo; K6–K7 halıda rulo; K8–K9 sayfa soyma + CTA okunuyor. Filigran yok. Ürün = vaka ürünü (yapışkan rulo).
**c-tuzak** `tur3/c-tuzak/kare_panosu.jpg`: K1–K2 bant takılı gövde, kanca "POV: Schultern zurück." + bant görünür; K3 kol yukarıda (takma anı; bant belde belirsiz); K4–K5 arkadan omuz bantları; K6–K9 önden bantlı gövde, CTA okunuyor (satır 2 iki satıra kırılıyor, kutu karede). Filigran ("RINGPENG" üst bant) ve siyah bantlar yok; sırt tutan kadın yok; yazıda sağlık iddiası yok. Ürün = kaynaktaki gerçek duruş düzeltici.

## Açık sorunlar
1. **b-zor: "temiz yüzey (tatmin)" planı zayıf.** Sıra istenen gibi değil: kanepede tüy → rulo → (temiz yüzey net görülmüyor; K3'te tüy hâlâ var, K4–K5 koltukta tüy var) → sayfa soyma. Kaynakta rulo sonrası net "tertemiz" kare çok kısa; tüyün sayfada toplanmış hâli yok. Jüri bunu düşürebilir. Ayrıca ilk plan sırası yerine "problem + rulo girişi" aynı plan (ürün ilk 0,9 sn kapısı için).
2. b-zor görüntü kapısı sınırda (1.47/1.50): son plan (ahşap zemin dokusu) gürültü oranını itiyor; halı planı öne alınarak geçildi, kırılgan.
3. c-tuzak: kaynak ürün omuz+bel bandı (yelek tipi), vaka "elastik bant"; kaynak çözünürlüğü düşük (253x450 → 1080x1920, yumuşak görüntü). "Aynı kişinin takmadan/taktıktan sonra tek plan" kanıt anı kaynakta yok; takma planı + takılı plan kullanıldı.
4. Tüm kaynaklar için yazılı ticari lisans yok (KAYNAK.tsv); yalnız sınav içi. Planların başındaki bazı kaynak sert kesimleri planlardan uzak tutuldu (ayar `bas` değerleri ham kurgu klip dosyalarına göre, kaynak saniyeleri yukarıda).
