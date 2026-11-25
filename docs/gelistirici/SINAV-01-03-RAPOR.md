# SINAV 01 + 03 — gerçek stok görüntüyle koşu (2026-11-24)

Çıktılar: `<referans-kok>/sinav-kosu/01-urun-videosu/tur{1,2}/` ve `.../03-hikaye-videosu/tur{1,2}/`; stok: `<referans-kok>/sinav-kosu/stok/<vaka>/` (LISANS.tsv her klasörde). Üretim betikleri depoda değil (geçici çalışma klasörü). Kör jüri bu rapor kapsamında koşmadı (lider koşacak): jüri kapısı her yerde `bekliyor` (0/3 kopya), pano hazır.

## Stok lisans özeti
8 klip, hepsi Pexels (Pexels License: ücretsiz ticari kullanım, atıf gerekmez), 24 Kas 2026, lider tarayıcıdan indirdi, kurucu onaylı. Mixkit denemesi: 429/403 ile engellendi, dolanılmadı (stok_mk.py ile 2 tarama sonrası). Müzik: sentetik (`hf-sablonlar/muzik_sentez.py`), efekt: sentetik (`ses_tasarla --sfx`, hikâyede eklentinin sfx kümesi); lisans gerekmez. Ürün şematik çizimleri (duruş bandı çizimi, ürün sahnesi ikonları) kendi üretimimiz.

| Vaka | Klipler | "Benzer ≠ aynı" notu |
|---|---|---|
| a-kolay kupa | 6206442 (siyah kupaya sıcak su + buhar), 31994495 (kırmızı kupaya su), 6801660 (beyaz kupaya sürahi) | Termokromik kupa DEĞİL; görüntüde renk/desen DEĞİŞİMİ yok, yalnız sıcak su dökme |
| b-zor rulo | 10558368 (beyaz tişörtte el aleti), 6953362 + 8498663 (kanepede köpek) | Tüy rulosu YOK; el aleti buharlı ütü/benzeri; toplanan tüy ve sayfa görüntüsü YOK |
| c-tuzak bant | 27430390 (laptopta boyun ovuşturan kişi), 8926991 (iş sonrası esneme) | Bant/korse YOK; takmadan/taktıktan sonra aynı kişi YOK |

## Tur × vaka × kapı

### 01 ürün videosu (6–10,5 sn döngü; 5–6 plan; hizli_kurgu + ses_tasarla; HyperFrames kullanılmadı, yazı hizli_kurgu kutulu)
| Vaka | Tur | Mekanik sonuç | KALDI kapıları (neden) |
|---|---|---|---|
| a-kolay | 1 | KALDI | kurgu_kontrol + goruntu: `[urun]` değişmiş ürün planı yok; `[ses]` −28 dB altı delik 0,2–1,05 sn |
| a-kolay | 2 | KALDI | kurgu_kontrol + goruntu: yalnız `[urun]` (ses deliği giderildi) |
| b-zor | 1 | KALDI | `[stok]` durağan stok toplamı 3,43 sn > 1,75; `[ses]` delik 0,2–1,05 ve 7,85–8,45 |
| b-zor | 2 | tüm mekanik GEÇTİ (jüri bekliyor) | — |
| c-tuzak | 1 | KALDI | `[stok]` 5,14 sn > 1,75; `[ses]` delik |
| c-tuzak | 2 | tüm mekanik GEÇTİ (jüri bekliyor) | — |
Geçenler tur2'de: dosyalar, kart (+vaka), ayar_beklenen, kurgu_kontrol (dongu/tatmin/cta/plan), goruntu, ses_kapi, ses_seviye (−14,1…−14,2 LUFS, tepe ≤ −1,2 dBTP, drop 9,3–9,7 dB), sure (8,5 sn), cozunurluk, ice01_fiyat, yasakli. tur1'in ilk koşu tablosu: `tur1/SONUC-ilk-kosu.md`.

### 03 hikâye videosu (25,0 sn; gerçek HyperFrames render, uret.py)
| Vaka | Tur | Mekanik | KALDI |
|---|---|---|---|
| a-kolay | 1 | KALDI | ses_seviye: tepe −0,7 dBTP (> −1) |
| b-zor | 1 | KALDI | aynı |
| c-tuzak | 1 | KALDI | aynı |
| üçü | 2 | tüm mekanik GEÇTİ (jüri bekliyor, çıkış 3) | tepe −1,3 dBTP, LUFS −14,5, drop 8,9 dB, giriş tuttu, delik/sıçrama yok, görüntü kapısı GEÇTİ |
Tur2'de b-zor ayrıca yeniden render edildi (kanca taşması, aşağıda).

## Kök neden + sınıf
1. **03 tüm vakalar, tepe −0,7 dBTP — SINIF (a) eklenti aracı hatası.** `skills/cut/scripts/hikaye/ses.py` teslim kodlaması (ses_tasarla çıkışı −1,7 dBTP, `uzun.mp4`) AAC'yi ikinci kez kodlarken true peak'i ~+1 dB şişiriyordu (ölçüldü: −1,7 → −0,7). Düzeltme: o kodlamaya `alimiter=limit=0.794` (aynı dosyada ölçüm: −1,3 dBTP, LUFS değişmedi). Kapı gevşetilmedi. Test: `test_hikaye.py`'ye "teslim true peak ≤ −1,0 dBTP" eklendi; 17/17 geçti. Dürüst sınır: sentetik test müziğinde hata eklemeden önce de geçiyor (kırma testi hatayı yakalamıyor), gerçek karışımda yakalanıyor; kanıt gerçek vaka ölçümü (−0,7 → −1,3). VO'lu yol (`vo_karistir`, loudnorm sonrası AAC) aynı riski taşıyabilir, bu turda ölçülmedi.
2. **01 ses deliği — SINIF (b) üretim hatam.** Taban ses çok kısıktı (pembe gürültü a=0,02); müzik −38 dB'den rampalanırken 0,2–1,05 sn −28 dB altına düştü. Taban ses 0,15'e çıkarıldı. (ses_olc kendi kapısı −45 dB'de delik görmedi; −28 dB eşiği kurgu_kontrol'de.)
3. **01 b-zor/c-tuzak `[stok]` — SINIF (b) üretim.** Kural: durağan stok toplamı ≤ 1,75 sn. Tur2'de b-zor'da tek stok plan (köpek, 1,71 sn), c-tuzak'ta iki 0,857 sn'lik stok plan + şematik ürün çizimi planları. Not: c-tuzak'ta ürün planı kuralı yalnız bu çizimle sağlandı (gerçek ürün görüntüsü yok).
4. **01 a-kolay `[urun]` — SINIF malzeme/tavan (YAPILAMAZ: ücretsiz stokta ısıyla renk değiştiren kupa değişim görüntüsü yok).** Vaka `urun_tipi != ekransiz` ister (değişmiş ürün planı). Siyah kupaya su dökme planını `urun` diye etiketlemek yanlış beyan olurdu; etiketlenmedi, sahte renk değişimi kurulmadı. Kapı/OLCUT gevşetilmedi; çözüm gerçek termokromik kupa çekimi ya da kredili/Flow üretimi (bu işin kapsamı dışı).
5. **Araç/yönerge uyuşmazlığı (düzeltilmedi, öneri; SINIF (a) olası):** 01 döngüsünde `drop_sn` varsayılanı 3,429 ile 8,6 sn'lik videoda müzik rampası ölçülen 3,25 sn çıkıyor (eşik ≤ 3,0): `ses_olc.muzik_giris` rampayı "medyan seviyenin −3 dB'ine ulaşma" diye ölçüyor, drop videonun %40'ından önce ise medyan drop sonrası seviyeye kayıyor. Ölçülen: drop 3,43 → rampa 3,25 KALDI; 4,29 → 3,0 sınırda; 4,8 → 1,65; 5,14 → 1,5 GEÇTİ. Bu koşuda drop 5,143 sn'ye alındı ve `tatmin_ani` penceresine drop dahil edildi (tatmin başlangıcı 3,43 sn). Tarif 01 "drop 3,429" örneği 8,6 sn'lik döngüde tutmuyor; doküman düzeltmesi/lider kararı gerekir (ölçüt gevşetilmedi).
6. **03 b-zor kanca taşması — üretim hatası, mekanik kapı yakalamadı.** `to a DOG MOM.` boy 150'de sağ kenardan taşıyordu (kare gözleminde fark edildi); boy 116'ya çekilip tur2'de yeniden render edildi. Yazı taşmasını ölçen mekanik kapı yok (öneri: hikâye kurucuya kanca satır genişliği kapısı).

## Kare gözlemleri (0 · 0,5 · 1 · 2 · 3 · 5 · son; `pano.jpg` her vaka klasöründe, tur2)
**01 a-kolay:** 0 sn'de siyah kupa kadrajda ve su dökülüyor (ürün ≤0,5 sn, hareketli); kanca "Watch this mug closely" kutulu, okunuyor; 2–3 sn kırmızı kupa dökme planı; 5 sn tekrar siyah kupa (drop); son karede CTA kupa üstünde, okunuyor. Kanıt anı: sıcak su + buhar var, **renk/desen değişimi YOK** (ürünün asıl kanıtı eksik). Döngü: son plan ilk planın hemen öncesi (dökme başlangıcı).
**01 b-zor:** 0 sn'de el aleti tişört üstünde hareketli (ürün benzeri, ≤0,5 sn); kanca "Kanepede tüy mü var?" okunuyor; 2–3 sn kanepede köpek (problem anı); 5 sn alet kumaşta gezinir; son karede CTA "Ürün yaz, sana da göndereyim" okunuyor. **Toplanan tüy / dolu sayfa kanıt anı YOK**, sahte önce/sonra kurulmadı; alet beyaz-beyaz zeminde düşük kontrast.
**01 c-tuzak:** 0–1 sn şematik bant çizimi (omuzlar geride oku), kanca "POV: Schultern zurück." okunuyor, sağlık iddiası yok; 2 sn laptopta egik kişi; 3 sn esneyen kişi (farklı kişi); 5 sn yakın bant çizimi, CTA "Kommentiere "BAND" / und ich schicke dir den Link" okunuyor (satır2 iki satıra kırılıyor, kutu karede). Ürünün gerçek görüntüsü yok; kanıt anı (aynı kişi önce/sonra) YOK, yerine çizim + esneme geçti. Boyun ovuşturan klip sağlık imgesi taşıyor, metinde iddia yok.
**03 a-kolay (DE):** 0 sn'de siyah kupa kadrajda, kanca "Heißes Wasser. Eine Tasse. / Schau hin." okunuyor; 3 ve 5 sn kırmızı kupa dökme; 13,5 sn ürün sahnesi (şematik kupa ikonu, "KERAMIK · 350 ML" çip, okunuyor, 4 sn); son: "Speicher dir das / für morgen." Kanıt anı: renk değişimi YOK.
**03 b-zor (US):** 0–2 sn kanepede köpek + "DO NOT show this / to a DOG MOM." (tur2'de taşma giderildi, okunuyor); 3–5 sn "Fur on the couch." iki köpek; ürün sahnesi şematik rulo ikonu ("PEEL TO RENEW"); alet-kumaş planları 8–22 sn arası; kanıt anı (toplanan tüy) YOK; `bilgi` notu "results vary by fabric".
**03 c-tuzak (TR):** 0–2 sn boyun ovuşturan kişi + "Omuzlar geride. Kafa dik." okunuyor, iddia yok; 3–5 sn "Gün boyu masada."; ürün sahnesi şematik bant ikonu; son kare esneyen kişi + "Kaydet, yarın masada."; `bilgi`: "Tıbbi ürün değildir." Kanıt anı (omuz hizası karşılaştırması) YOK.
Genel gözlem: mekanik kapılar geçse de kanıt anı üç vakada da ürünün KENDİ sonucunu göstermiyor (malzeme tavanı); kör jüri bunu düşürecektir, ölçüt gevşetilmeli değil, gerçek ürün çekimi gerekir.

## Değişen dosyalar (eklenti)
- `plugins/viral-urun-ekibi/skills/cut/scripts/hikaye/ses.py` (teslim kodlamasına limiter, −1,7 → ölçülen −1,3 dBTP)
- `plugins/viral-urun-ekibi/skills/cut/scripts/hikaye/test_hikaye.py` (true peak ≤ −1 testi)
Kapı/eşik/koşucu/OLCUT/vaka dosyalarına dokunulmadı; `skills/studio/` ve `agents/story.md` dokunulmadı; depoda `.hyperframes/` yok.

## Kapılar (çıkış 0)
`anonim_kontrol.sh` temiz · `musteri_icerik_kontrol.py` GEÇTİ · `sozlesme_test.py` 49/49 · `sinav_kos_test.py --hizli` 61/61 · `test_hikaye.py` 17/17 · `hf-sablonlar/sablon_test.py` 16/16.

## Lider için
Jüri: `01 tur2` (b, c) ve `03 tur2` (a, b, c) `juri/pano` hazır; a-kolay 01 mekanik KALDI (malzeme). Sonucu `SONUC.md` her tur klasöründe.
