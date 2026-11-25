# Dalga 2 B: metin ve fikstür maddeleri (2026-11-25)
Sonuç: 15, 25 (belge kısmı), 29, 30 ve devredilen Story çelişkisi uygulandı; YAPILAMAZ yok, ama 25'in betiği yok (belgede "yazılacak" yazıyor).
kurucuyu ilgilendiren: karar yok. `dist/` zipleri eski; sürüm çıkarken `paketle.sh` ile yeniden üretilecek (madde 29).
Yollar: `<eklenti>` = `plugins/viral-urun-ekibi`. Git commit/add yok; para ve tarayıcı yok.

| Madde | Dosyalar | Önce → sonra | Durum |
|---|---|---|---|
| 15 rol fikstürleri | yeni `<eklenti>/ortak/sinav/roller/<rol>/vaka.json` (17 dosya) + `rol_fikstur_test.py`; `ortak/sinav/README.md` (+4 satır bölüm) | fikstür 0 → 17 rol, 28 sabit girdi (mod başına 1), 28 eksik girdi vakası (hepsi `dur` bekler, uydurma yasak listesi dolu) | tamam |
| 25 kurulum kontrolü | `README.md` (+31 satır): "ölçülen / ölçülemeyen" tablosu, sürümlü araç listesi, tek komut belgesi | bölüm yoktu → var; `scripts/kurulum_kontrol.sh` depoda YOK, belgeye "betik henüz yazılmadı" yazıldı (yerine `ffaraclar.py`) | belge tamam, betik Dalga2-A'da |
| 29 kopya eşitliği | `CHANGELOG.md` (0.6.0 yayınlanmadı girdisi, ~30 satır); sürümler | plugin.json, marketplace.json, README rozetleri, claude/README, PRIVACY: hepsi 0.5.0 = tutarlı, değiştirilmedi (0.6.0 yayında bumplanır, girdi bunu yazıyor); dist yeniden üretilmedi | tamam |
| 30 okuma zinciri | `agents/story.md`, `ortak/roller/forge/istem.md`, `skills/builder/SKILL.md`, `ortak/roller/sentinel/kilit.md`, 10 mağaza mod/ajan dosyasında "Önce oku" satırı | aşağıdaki tablo | tamam |
| devir: Story kota ↔ `senaryo_kontrol.py` | `agents/story.md`, `skills/studio/referans/asamalar.md` | metin betiğe uydu; betik eşiği (30'da ≥ 8 mekanizma / ≥ 6 şablon / ≥ 6 aile) DEĞİŞMEDİ | tamam |

## 15 detay
Biçim: `{rol, sabit_urun (a-kolay kupa, TR), moduller[{mod, brief, beklenen{cikti_dosyasi, zorunlu_bolumler}}], eksik_girdi[{mod, brief, eksik, beklenen:"dur", ilk_satir_icerir, yasak}]}`. Test ajan koşturmaz; kontrol eder: 17 ajan dosyası = 17 klasör · modlar ajan tanımındaki mod tablosuyla aynı · her modun eksik girdi vakası var ve `dur` bekliyor · mutlak ev yolu yok · `ortak/sozlesme-rol.md` "Girdi eksikse dur" kuralını içeriyor.
- Çıkış: `python3 ortak/sinav/roller/rol_fikstur_test.py` → `GEÇTİ: 17 rol · 28 sabit girdi · 28 eksik girdi vakası`, çıkış 0.
- Kırma: scout eksik girdi vakasında `dur` → `devam` yapıldı → `KALDI`, çıkış 1; geri alınınca GEÇTİ.
- Sınır: bu yalnız fikstür ve şema testidir; rolün gerçekten durduğunu ölçmez (denetim #14 rol-gerçek sınav ayrı iş).

## 25 detay
Araç tablosu bu makinede ölçüldü: Python 3.9.6, ffmpeg v7.1 (imageio_ffmpeg; PATH'te yok, ffprobe yok), Pillow 11.3.0, numpy 2.0.2, openpyxl kurulu değil, OCR ortamı rapidocr-onnxruntime 1.4.4 / Python 3.12.13 / onnxruntime 1.32.0, Tesseract yok, Node v22.20.0, `hyperframes` npx ile sürümsüz (ağa çıkılmadı, ölçülmedi). Probe yerel ölçümü "yazılacak" diye belgelendi (denetim #22).

## 30 detay (zorunlu okuma, kelime; ölçü `wc -w`)
| Rol | Önce | Sonra | Ne yapıldı |
|---|---|---|---|
| Story | zorunlu 3.196 (tanım 622 + asamalar 1.785 + format 789) + "gerektikçe" 5 dosya 17.162 kelime = ~20.400 olası | zorunlu 3.287 (tanım 695 + 1.803 + 789); kütüphaneler yalnız ilgili bölüm | zorunlu 2 referans; `kanca-kutuphanesi` §1b + R74, `kurgu-ve-yasaklar` §7–§8 bölüm bazında; `kreatif-mantigi`/`pazar-katmani` yalnız belirsizlikte. (Zorunlu kısım Story kota/çelişki cümlesi yüzünden +91 kelime büyüdü; hedef ≤ 5.000 sağlandı.) |
| Forge `istem` | 12.071 (mod 611 + bloklar 1.609 + `istemler/*.md` 9.832) | ~3.200 (slot başına ~970 şablon) | klasörün tamamı yerine yalnız turdaki slotun şablonu |
| Builder (her aşama) | 2.830 ortak kural her aşamada | 0 (kartta işaret varsa) | DEVAM KARTI'na `okundu: 00,01`; işaret yoksa ya da bağlam sıfırlandıysa oku (kural kaybolmadı) |
| 10 mağaza rolü | `is/arastirma/…` yolları için arama turu | arama yok | "Önce oku" satırına "yolları varsa; yoksa arama, gömülü sayıyı kullan" (13 dosya); Sentinel `kilit`'ten eklentide olmayan örnek kayıt atfı silindi |
Toplam talimat satırı (agents + ortak/*.md + ortak/roller + skills/*/SKILL.md): önce 2.525 → sonra 2.524 (kelime: agents 7.094 → 7.191, ortak/roller 6.002 → 6.090). Kazanç satırda değil okuma yükünde; kural silinmedi, sil/atıf verilen yerlerde kural aynı dosyada ya da `magaza-ekibi.md` §3'te duruyor. Mağaza rolleri ≤ 2.500 hedefi ölçülmedi.

## Devir: Story kota çelişkisi
Betik `n ≥ 30` iken mekanizma < 8 / şablon < 6 / aile < 6 durumunu ❌ yapar; `n < 30` iken dağılım denetimi yalnız UYARI. Metin: ürün çeşitliliği vermiyorsa 30'a tamamlama, 30'dan az yaz, raporda "N senaryo: ürüne uyan mekanizma M" de; çeşitliliği tekrar ya da zorlama senaryoyla uydurma. `studio/SKILL.md` ve ajan "30 senaryo" ifadesi hedef olarak kaldı. `senaryo_kontrol_test.py`: 19 GEÇTİ, 0 KALDI.

## 29 detay: dağıtım kopyası farkı (düzeltilmedi, yalnız listelendi)
Zipler git dışı (`dist/` .gitignore'da).
- **CLAUDE v0.5.0 zip ↔ kaynak** (`diff -rq`, bu raporun yazıldığı an): 87 değişen dosya · 17 yalnız kaynakta · 0 yalnız zipte. Değişenler: 17 ajan dosyasının tamamı, `ortak/ekip.md`, `ortak/magaza-ekibi.md`, 7 `ortak/roller/*` dosyası, 11 `SKILL.md` ve `skills/{bazaar,captain,cut,studio,hunter,builder}` altındaki referans ve betikler, `ekler/chatgpt/tarifler/{README,10-...}.md`, `ortak/tarifler/{README,06,10}.md`. Yalnız kaynakta: `ortak/{sozlesme-rol.md, rapor-sablonu.md, mcp-kanit-araclari.md, indirme_al.py, indirme_al_test.py, mobil_ekran.py, sinav/}`, `ortak/tarifler/11-bicim-kopyala.md`, `ekler/chatgpt/tarifler/{11-bicim-kopyala.md, sinav-kontrol-listesi.md}`, `skills/cut/{hf-sablonlar/, referans/tipografi-ve-kanca-gorseli.md, scripts/kurgu_kontrol_test.py, scripts/malzeme_kaynak.py}`, `skills/radar/referans/prompt-dosyasi-sablonu.md`, `skills/builder/gorseller/scripts/ocr_kontrol_test.py`, `skills/studio/scripts/senaryo_kontrol_test.py`.
- **CHATGPT v0.5.0 (`dist/chatgpt/viral-urun-ekibi`)**: ortak dosyalar `skills/ekip-bilgi/references/` altında dönüştürülmüş kopya, bayt eşitliği beklenmez; ölçülen: `sozlesme-rol.md`, `rapor-sablonu.md`, `mcp-kanit-araclari.md` yok; `ekler/chatgpt/tarifler/11-bicim-kopyala.md` ve `sinav-kontrol-listesi.md` yok; `skills/studio/SKILL.md` "R74" 0 kez (kaynakta 1); `skills/studio` ve `cut` ChatGPT ek dosyaları 23 Kasım, kaynak SKILL'ler 24–25 Kasım. İçerik karşılaştırması dönüşüm yüzünden dosya adı/anahtar kelime düzeyinde; tam eşitlik için yeniden üretim gerekir (yasak, sürüm kapısı).
- **Sürüm numaraları**: `plugin.json` 0.5.0 · `marketplace.json` 0.5.0 · `README.md`/`README.en.md` rozet 0.5.0 · `claude/README.md` 0.5.0 · `PRIVACY.md` 0.5.0 · zip adları 0.5.0 → tutarlı. `moduller/magaza-kurucu` 0.6.0 ayrı modül sürümüdür (yanlış değil).
- Eşitlik kontrolü önerisi (Ek 15/3: ADHD kuralları, MCP paragrafı, mod tablosu kopyaları) betik işi, bu dalgada yapılmadı.

## Test çıkışları
- `claude plugin validate plugins/viral-urun-ekibi`: Validation passed (çıkış 0).
- `scripts/sozlesme_test.py`: 49/49, çıkış 0 · `scripts/ad_testi.py`: 0 hata, çıkış 0.
- `captain/scripts/kapi_test.py`: TOPLAM 53 test, 0 kaldı · `studio/scripts/senaryo_kontrol_test.py`: 19 GEÇTİ, 0 KALDI, çıkış 0.
- `ortak/sinav/roller/rol_fikstur_test.py`: GEÇTİ 17 rol / 28+28 vaka, çıkış 0.
- `bash scripts/anonim_kontrol.sh`: temiz, çıkış 0 (ilk koşuda yeni test dosyasındaki yol deseni 1 satır yakaladı, desen parçalara bölünerek düzeltildi).
- Frontmatter: 17 ajan ve değişen SKILL dosyaları `validate` ile geçerli.

## Dokunulan dosyalar
Yeni: `ortak/sinav/roller/<17 rol>/vaka.json`, `ortak/sinav/roller/rol_fikstur_test.py`, bu rapor. Değişen: `README.md`, `CHANGELOG.md`, `ortak/sinav/README.md`, `agents/{story,copy,panel,director}.md`, `skills/studio/referans/asamalar.md`, `skills/builder/SKILL.md`, `ortak/roller/{architect,atlas,forge,probe,sentinel,shopper}/*` ("Önce oku" etiketi, forge istem, sentinel kilit). `*.py/*.sh` betiklere dokunulmadı (yeni test dosyası hariç).
