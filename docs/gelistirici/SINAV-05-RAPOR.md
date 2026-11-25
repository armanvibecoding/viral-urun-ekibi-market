# SINAV 05-gorsel · TUR 1 raporu (2026-11-25)

Çıktı: `<referans-kok>/sinav-kosu/05-gorsel/tur1/<vaka>/` · kapı dökümü `.../tur1/SONUC.md` · üretim kaydı `.../tur1/URETIM.md`

## Üretim sayısı
- ChatGPT: 18 planlı + 2 yeniden = 20 görsel isteği (tavan 22). Yeniden üretim: b-zor galeri-2 ve c-tuzak galeri-3 (ilk sürüm ürünü kenarda kırpık). Kırpık ilk hâller `ham/*-ilk-kirpik.png`.
- Yazı ChatGPT'ye yazdırılmadı; Pillow ile basıldı. Zemin/kenar payı Pillow ile tam HEX'e oturtuldu. G0 ham 1254² Lanczos ile 1600²'ye büyütüldü.

## Kapı tablosu (`python3 scripts/sinav_kos.py 05-gorsel <tur1>`, çıkış 1)
| Vaka | dosyalar | K3 tuval | yasakli | K2 OCR | K1 sadakat | jüri |
|---|---|---|---|---|---|---|
| a-kolay | geçti | geçti | geçti | olculemedi | KALDI (SADAKAT'ta 2 kırmızı) | olculemedi |
| b-zor | geçti | geçti | geçti | olculemedi | olculemedi | olculemedi |
| c-tuzak | geçti | geçti | geçti | olculemedi | olculemedi | olculemedi |
K3 ilk koşuda G0 uzun kenar %73–75 ile kaldı; Pillow ölçeği düzeltilerek (1 düzeltme) geçti. yasakli ilk koşuda kendi istem dosyalarımdaki "78%" gibi ölçülerden kaldı; istemlerde "percent" yazıldı (1 düzeltme).

## SADAKAT özeti (gözle, üreten kendisi bakıyor; bağımsız sentinel değil)
- a-kolay: 4/6 temiz. galeri-3 ve b1'de sap pençe biçimli (kilit-118'de sivri kuyruk): set içinde sap tutarsız.
- b-zor: 6/6 temiz (sap ucu deliği kilitte görünmüyor, küçük ekleme).
- c-tuzak: 6/6 temiz; galeri-2 ile galeri-3 neredeyse aynı açı.

## Açık sorunlar
1. a-kolay sap tutarsızlığı: galeri-3 + b1 yeniden üretilmeli (tavanda 2 hak kaldı) ya da kilit-118 sap karesi ek referans verilmeli.
2. Tesseract/RapidOCR kurulu değil: K2 olculemedi. Türkçe/Almanca harfler (İ, Ö, Ü, Ğ, Ä, Ü) kontak sayfasında gözle okundu, hata görmedim.
3. Jüri: referanslar.tsv boş, `olculemedi`. Çıkış kodu bu yüzden en iyi 3.
4. Araç kısıtı: dosya yükleme aracı yok; referans kareler panoya kopyalanıp yapıştırıldı. c-tuzak galeri-3 yeniden üretiminde iki sekmenin metni karıştı (rulo+bant istemi aynı mesajda); sonuç ürüne uygun çıktı, kayıt URETIM.md'de.
5. Kaza (düzeltildi): kayıt betiğim, indirme klasöründe yeni dosya yokken kurucunun eski bir PNG'sini (2026-11-23 02:45, Noel ağacı) hedef klasöre taşıdı; aynı dakikada ~/Downloads'a geri taşındı. Özgün dosya adı kayıp: `geri-konan-noel-agaci-2026-11-23-0245.png`. Betik artık yalnız son 2 dakikanın dosyasını alıyor.
6. ChatGPT'de iş Business deneme afişi göründü; dokunulmadı.
