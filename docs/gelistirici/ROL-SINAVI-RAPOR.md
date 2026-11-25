# Rol sınavı raporu (madde 14) · 2026-11-25

Sonuç: dört özellik (07, 02, 01, 05) ilk kez eklentinin kendi rolleriyle koşuldu; 21 rol çağrısının (11 rol) hepsi kendi sınırında durdu, uydurma yok. Hiçbir özellik çıkış 0 vermedi: kalanların kök nedeni rol değil, üç eklenti kusuru (07 `pdp_url` şeması, 01 jüri panosu deseni, 05 rapor yüzdesi taraması) ve 05te kurucu onayı gerektiren üretim durması.

- Kapsam: 07 site · 02 kanca/senaryo · 01 ürün videosu · 05 görsel (kurucu onayı 2026-11-25; 05 ChatGPT tavanı 22).
- Çıktı kökü: `<referans-kok>/sinav-kosu/rol/<NN>/tur1/<vaka>/` (eski turlara ve SONUC dosyalarına dokunulmadı). Rol ara dosyaları `tur1/_is/<vaka>/` altında (vaka klasöründe taranmasın diye).
- Ham rol karnesi (her çağrı bir satır): `<referans-kok>/sinav-kosu/rol/KARNE-HAM.tsv`.
- Her özellikte 1 tur koşuldu (sınır 2). İkinci tur açılmadı: kalan kapıları rol değil eklenti/sözleşme düzeltmesi ya da kurucu onayı kapatır (aşağıda).
- Jüri kopyaları koşulmadı (lider koşacak); panolar hazır olan yerde `juri/kopya-1..3/pano` duruyor.

## 1. Kapı tabloları (koşucu: `scripts/sinav_kos.py`, `SINAV_REFERANS_KOK=<referans-kok>`)

### 07 site · çıkış 1 (KALDI)
| Kapı | a-kolay US | b-zor TR | c-tuzak DE |
|---|---|---|---|
| dosyalar | GEÇTİ | GEÇTİ | GEÇTİ |
| iddia_kontrol | KALDI | KALDI | KALDI |
| yasakli | GEÇTİ | GEÇTİ | GEÇTİ |
| paket_sozlesme | KALDI | KALDI | KALDI |
| kanit_ani_sizinti | GEÇTİ | GEÇTİ | GEÇTİ |
| mobil_ekran | GEÇTİ | GEÇTİ | GEÇTİ |
| hiz_cwv (yerel) | GEÇTİ | GEÇTİ | GEÇTİ |
| erisim_wcag (yerel) | GEÇTİ | GEÇTİ | GEÇTİ |
| arama_merchant | olculemedi | olculemedi | olculemedi |
| donusum_kullanilabilirlik | olculemedi | olculemedi | olculemedi |
| juri | olculemedi (ref 0/3) | olculemedi (ref 0/3) | olculemedi (ref 0/3) |
| kim_denetledi | GEÇTİ (probe, shopper) | GEÇTİ | GEÇTİ |

İki KALDI'nın tek kaynağı: `magaza.pdp_url` şemada zorunlu (`^https://`, null olamaz) ama vakada mağaza adresi yok. Copy adresi uydurmadı, alanı `eksik[]`'e yazdı (doğru davranış). Önceki tur bu alanı `.invalid` yer tutucuyla doldurmuştu. Bu turda kanıt anı sızıntısı ve mobil ekran (önceki turun iki KALDI'sı) GEÇTİ.

### 02 kanca + senaryo · çıkış 3 (bekliyor)
| Kapı | a-kolay TR | b-zor DE | c-tuzak US |
|---|---|---|---|
| dosyalar | GEÇTİ | GEÇTİ | GEÇTİ |
| on_uretim_karti / _vaka | GEÇTİ / GEÇTİ | GEÇTİ / GEÇTİ | GEÇTİ / GEÇTİ |
| senaryo_kontrol | GEÇTİ | GEÇTİ | GEÇTİ |
| senaryo_adedi | GEÇTİ (30) | GEÇTİ (30) | GEÇTİ (30) |
| kanca_varyasyon | GEÇTİ (12) | GEÇTİ (13) | GEÇTİ (12) |
| yasakli | GEÇTİ | GEÇTİ | GEÇTİ |
| juri | bekliyor (pano hazır) | bekliyor (pano hazır) | bekliyor (pano hazır) |

Mekanik kapıların hepsi GEÇTİ; tek açık kapı lider jürisi.

### 01 ürün videosu · çıkış 1 (KALDI)
| Kapı | a-kolay US | b-zor TR | c-tuzak DE |
|---|---|---|---|
| dosyalar · kart · ayar | GEÇTİ | GEÇTİ | GEÇTİ |
| kurgu_kontrol | GEÇTİ | GEÇTİ | GEÇTİ |
| goruntu | GEÇTİ | GEÇTİ | GEÇTİ |
| ses_kapi / ses_seviye | GEÇTİ (−14,3 LUFS, drop 9,8 dB) | GEÇTİ (−14,3, 10,1 dB) | GEÇTİ (−14,3, 11,3 dB) |
| sure / cozunurluk | GEÇTİ (8,63 sn, 1080×1920) | GEÇTİ | GEÇTİ |
| ice01_fiyat · yasakli | GEÇTİ | GEÇTİ | GEÇTİ |
| kim_denetledi | GEÇTİ (mixer) | GEÇTİ | GEÇTİ |
| juri | KALDI (pano geçersiz) | bekliyor (pano hazır) | KALDI (pano geçersiz) |

a-kolay'ın tur3'teki kurgu_kontrol KALDI'sı (ilk 2 sn durağan) kapandı: desen değişimi ilk 1,5 sn'ye alındı (ilk iki plan 2 vuruş, kaynak 109,4 ve 111,2 sn). Kalan KALDI videoda değil panoda (§3, bulgu 2).

### 05 görsel · DURDU (koşucu tam set olmadan KALDI verir)
- Üretim 4/22 (a-kolay, b-zor, c-tuzak galeri-1; c-tuzak'ta ChatGPT kendiliğinden 2 kare üretti).
- Sentinel ara kapısı: a-kolay K1 AÇIK, K2 olculemedi (Tesseract yok) · b-zor K1 AÇIK, K2 GEÇTİ · c-tuzak K1 KAPALI (ayar şeridi yok) + K2 KALDI (fazla kelime "together").
- Kalan 10 görselin ilk gönderimi izin sistemi tarafından reddedildi: onay lider mesajıyla iletilmişti, ajan mesajı kullanıcı onayı sayılmaz. Forge dolanmadı, durdu (doğru davranış). Devam için kurucunun kendi mesajıyla onayı gerekir.
- Koşucu (`ocr-venv` python ile) çıkış 1:

| Kapı | a-kolay TR | b-zor DE | c-tuzak US |
|---|---|---|---|
| dosyalar | GEÇTİ | GEÇTİ | KALDI (gorseller/ boş: K1 kapalı) |
| K3_tuval_olcu | KALDI (set eksik: 1/6) | KALDI (set eksik: 1/6) | — |
| K2_yazim_ocr | olculemedi (Tesseract yok) | GEÇTİ | — |
| K1_sadakat | olculemedi (betik yok; sentinel 6/6) | olculemedi (sentinel 5/5) | — (sentinel 5/6 ❌) |
| yasakli | KALDI (KAPI.md ölçüm yüzdesi) | KALDI (KAPI.md ölçüm yüzdesi) | — |
| juri | olculemedi (ref 0/3) | olculemedi (ref 0/3) | — |
| kim_denetledi | GEÇTİ (sentinel) | GEÇTİ (sentinel) | — |

## 2. Rol karnesi
| Rol | İş (özellik · mod) | Süre (dk) | Kapıya takılan hatası | Sınırına uydu mu |
|---|---|---|---|---|
| architect | 07 · bolum (3 sayfa planı) | 0,9 | yok | evet: kütüphane yokluğunu `olculemedi` yazdı, uydurma bölüm (yorum, basın) açmadı |
| copy | 07 · site (6 metin + 3 paket) | 1,4 | `pdp_url` yok → iddia_kontrol + paket_sozlesme KALDI (veri yok) | evet: adresi uydurmadı; renk/tipografiye nötr varsayılan koyup `eksik[]`'e işaretledi |
| shopper | 07 · ses (güçlü model) | 2,1 | yok | evet: strateji yokluğunu `olculemedi`, emin olmadığı DE/EN cümleyi geçirmedi |
| probe | 07 · hiz + erisim (yerel) | 4,2 | yok | evet: `yerel` etiketini korudu, ölçemediğini (hedef boyutu, odak, CrUX) yazdı |
| story | 02 · banka + 30 senaryo + kanca | 14,9 | yok (senaryo_kontrol 3/3 çıkış 0) | kısmen: hikaye-bankasi.md brief'teki `_is/` yerine vaka klasörüne yazıldı |
| mixer | 01 · ses planı + ölçüm | 1,6 | yok (ses_olc --kapi 3/3 çıkış 0) | evet: dinleyemediğini ve sınav içi atlanan "kurucu seçti" kapısını açıkça yazdı |
| fixer | 01 · kök neden | 3,1 | yok | evet: jüri yokken puan uydurmadı; "sınıf dışı: pano" dedi, emir 0, eşik önerisini emir değil kurucu kararı diye ayırdı |
| sentinel | 05 · kilit (Görev A) | 2,1 | yok | evet: girdi çelişkisini (giysi altı ↔ fotoğraf) soru olarak üste yazdı |
| atlas | 05 · stil | 4,5 | yok | evet: marka ölçümünü `olculemedi` yazdı, tek önerilen yön + HEX verdi |
| copy | 05 · gorsel (2 çağrı) | 2,2 + 1,2 | ilk yazım copy_kontrol çıkış 2 (biçim) — kök neden lider brief'i | evet: doğrulanmamış parça adlarını ve eksik kareyi lidere işaretledi |
| forge | 05 · istem (18 istem) | 5,6 | yok | evet: üretim yapmadı, lider kararına aykırı model önerisini uygulamadı |
| forge | 05 · uretim (galeri-1 ×3; 3 çağrı) | 0,9 + ~9 + ~2,5 | yok | evet: dosya yükleme aracı yokken eksiz göndermedi (YAPILAMAZ); izin reddinde dolanmadı |
| sentinel | 05 · kilit B + yazim (galeri-1 ×3) | 2,1 | yok | evet: Tesseract yokken TR yazımı geçti saymadı; c-tuzak'ta ara kapıyı tetikledi |
| forge | 05 · istem düzeltme turu 1 | 0,6 | yok | evet: tek değişken; kusurlu kareyi çapa yapmadı |
| forge | 05 · ayrı düzeltme adımı (duzelt.py, a/b galeri-1) | 0,6 | yok | evet: K1 kapalı c-tuzak'a dokunmadı, ham dosyayı ezmedi |
| sentinel | 05 · seri (a/b galeri-1) | 1,9 | KAPI.md'deki ölçüm yüzdeleri yasakli kapısında "uydurma yüzde" sayıldı | evet: referanssız kör panoyu kurmadı, tek görselle set puanı vermedi |
| panel | 05 · kör pano (kopya 1) | ~1,5 | yok | evet: pano yokken puan vermedi, ilk satırda DUR |

Gözlem: 21 çağrının hiçbirinde uydurma sayı, marka ya da fiyat yok; eksik girdi her seferinde `olculemedi`/`YAPILAMAZ`/soru olarak yazıldı. Üreten = denetleyen olan raporlar kendini `ÖZ-DENETİM` diye işaretledi.

## 3. Bulgular (rol değil, eklenti; düzeltme kurucu/eklenti kararı, bu turda koda dokunulmadı)
1. **07 sözleşme ↔ vaka çelişkisi:** `magaza-paketi.schema.json` `magaza.pdp_url`'yi zorunlu tutuyor; 07 vakalarında mağaza adresi yok. Dürüst rol her koşuda KALDI alır, yer tutucu yazan rol geçer. Karar: vakaya sınav adresi eklemek ya da şemada `null + eksik[]`'i `olculemedi` saymak.
2. **01 jüri panosu ↔ kurgu kapısı çelişkisi (fixer bulgusu, lider doğruladı):** `skills/cut/scripts/juri.py` `SIZINTI_RE` `comments?` kelimesini tek başına sızıntı sayıyor; `kurgu_kontrol.py` döngü CTA'sı olarak `Comment "KELİME"` istiyor. Sonuç: EN CTA'lı video ve O03 referansı ("Comment "Dog" to get yours!") panoyu geçersiz kılıyor; DE CTA'lı video etkilenmiyor (dile göre farklı sonuç).
3. **forge araç listesi eksik:** `agents/forge.md` araçlarında `file_upload` ve `javascript_tool` yok; `flow-ve-chatgpt.md` ek yüklemeyi ve `chatgpt_indir.js`'i bunlarla anlatıyor. Bu turda ekler Bash ile panoya alınıp yapıştırıldı (çalıştı).
4. **Üretim onayı zinciri:** kurucu onayı lider brief'inde olsa da alt ajana mesajla iletilen ikinci onay izin sisteminde reddedildi. Çok çağrılı üretimde kurucunun onayı her üretim çağrısının brief'inde ilk satırda olmalı ya da üretim tek çağrıda bitmeli.
5. **OCR:** Tesseract kurulu değil (TR K2 `olculemedi`); `ocr_kontrol.py --dil` yalnız `tr|en` kabul ediyor, DE yok.
6. **Koşucu yasakli kapısı ↔ sentinel seri:** `sinav_kos.py` `GENEL_YASAKLI` yüzde deseni vaka klasöründeki KAPI.md'yi de tarıyor; seri.md ise K3'ü yüzde ölçümüyle yazdırıyor. Ölçüm raporu 05'i tek başına KALDI yapıyor (a-kolay %58, b-zor %80). Karar: KAPI.md'yi tarama dışına almak ya da rapora oran yerine `0,58` yazdırmak.
7. **Lider kaynaklı hatalar (karneye rol hatası diye yazılmadı):** 05 copy brief'inde "Slot" sütunlu tablo istendi (betik okuyamadı); 07 HTML dönüştürücüsü "Button:" satırını düz paragraf yaptı ve gri yer tutucu blok kontrastı 1,21:1 (probe yakaladı).

## 4. YAPILAMAZ ve durmalar
- 05 kalan üretim (a-kolay, b-zor: g0, galeri-2, galeri-3, b1, b2; c-tuzak: düzeltilmiş galeri-1 + 5): izin sistemi reddi → kurucunun kendi onay mesajı gerekir. Hazır: istemler (`_is/<vaka>/istem/`), c-tuzak düzeltme turu 1, sayaç 4/22.
- 05 ön uçuş `on_ucus.py` çıkış 1 (referans 0/3, Tesseract yok): üretime kurucu onayıyla başlandı; jüri kapısı bu yüzden zaten `olculemedi` kalır.
- 07 ön uçuş çıkış 1 (referans 0/3): metin üretimi kredisiz olduğu için koşuldu; jüri `olculemedi`.
- Jüri (3 kör kopya): talimat gereği koşulmadı (02 ×3 ve 01 b-zor panosu hazır).
- Hiçbir rol çağrılamadı durumu yaşanmadı.

## 5. Sapmalar (dürüst kayıt)
- 02'de hikâye bankası ve 30 senaryo tek story çağrısında (varsayılan model) yapıldı; studio "banka + ilk 5 seçimi ayrı çağrı, en güçlü model" diyor.
- 02 Aşama 1 viral referans izlemesi (lider, TikTok) yapılmadı; referanslar `referanslar.tsv`'den.
- 07 ekran HTML'i ve 01 kurgu/klip kesimi lider (cut) tarafından betikle yapıldı; ön-üretim kartları ve ayarlar liderde (studio/cut).
- 07 için ikinci tur açılmadı: shopper'ın dil düzeltmeleri (EN 5, TR 6, DE 6 ❌) kapı değiştirmiyor; kalan kapı sözleşme kusuru.

Sonraki adım: kurucu 05'in kalan 16 görselini kendi mesajıyla onaylarsa aynı istemlerle üretim sürer; ardından bulgu 1 ve 2 için eklenti kararı.
