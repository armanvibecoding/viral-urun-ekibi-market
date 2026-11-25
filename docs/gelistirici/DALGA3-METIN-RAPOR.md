# Dalga 3 · metin raporu (2026-11-25)

Kaynak: `DALGA2-A-RAPOR.md` "Metin önerisi". Kural: betiğe geçen elle adım metinden silindi, betik komutu yazıldı. `*.py/*.sh` değişmedi.

## Dosya · önce → sonra satır (eklenti kökü: `plugins/viral-urun-ekibi`)
| Dosya | Önce | Sonra | Ne |
|---|---|---|---|
| ortak/roller/probe/hiz.md | 27 | 28 | `web_olcum.py hiz`, `yerel` etiketi, tara.mjs yalnız kütüphane karşılaştırması |
| ortak/roller/probe/erisim.md | 22 | 25 | "Ölçüm" bölümü: `web_olcum.py erisim` |
| agents/probe.md | 18 | 20 | araç cümlesi + `kontrol`/`kur` |
| agents/panel.md | 39 | 39 | `KOR-<n>.json` şeması; medyan betikte |
| agents/director.md | 38 | 38 | elle tablo yerine `panel_medyan.py --esleme` |
| ortak/roller/sentinel/yazim.md | 24 | 24 | `beklenen_uret.py` (elle kopyala silindi) |
| agents/copy.md | 36 | 36 | `copy_kontrol.py` (elle İ/I kontrolü silindi) |
| agents/mixer.md | 65 | 64 | anlar `ses_plan.py` taslağı, drop `ses_olc.py` |
| skills/cut/SKILL.md | 98 | 99 | 3b: `yazi_tasma.py` çıkış 0 şartı |
| ortak/rapor-sablonu.md | 8 | 8 | `ÜRETEN:` satırı, koşucu `KİM DENETLEDİ` ile karşılaştırır |
| skills/captain/SKILL.md | 120 | 121 | ön uçuş `on_ucus.py hepsi`; `juri.py yapilamadi` = KALDI |
| skills/captain/referans/kurulum-kontrol.md | 31 | 32 | web_olcum satırı (Node ≥ 22.19, Chrome, `kur`) |
| skills/builder/metinler/references/ekip-koprusu.md | 43 | 43 | `null` + `eksik[]`, `marka.ad_kaynak` |
| ortak/roller/forge/uretim.md | 32 | 32 | `indirme_al.py` |
| ortak/roller/shopper/donusum.md | 23 | 23 | `mobil_ekran.py ekran` |
| ortak/sinav/01–06 OLCUT.md | 55/51/53/50/52/46 | 56/52/54/51/53/47 | +1 satır `kim_denetledi` |
| ortak/sinav/07-site/OLCUT.md | 47 | 52 | paket_sozlesme, kanit_ani_sizinti, mobil_ekran, web_olcum satırları; ölçülemeyenler 4 kapıdan 2'ye (eşik yazılmadı, betiğe atıf) |
| ortak/sinav/README.md | - | +1 | 08 satırı |
Toplam (15 metin + 7 OLCUT): 978 → 997 satır (+19; +7'si OLCUT kapı satırı, +5'i 07). Ajan/beceri metinlerinde net: +3.

## 08-marka (madde 28)
`ortak/sinav/08-marka/`: `OLCUT.md`, `referanslar.tsv` (başlık), `vakalar/{a-kolay TR kupa, b-zor DE rulo, c-tuzak US duruş}/vaka.json` (01–07 biçimi; pazar 01–07 sırasından döndürüldü). Roller Atlas/Muse/Architect; çıktı `marka/*.md` + `magaza-paketi.json`. Mekanik kapılar: dosyalar, paket_sozlesme, iddia_kontrol, yasakli, kim_denetledi. Ölçülemez (yazıldı): renk kontrastı (HEX çifti betiği yok), ad ayırt edilebilirliği, logo/strateji kalitesi, tipografi uygulaması, kör jüri (marka türü yok). `sinav_kos.py`'ye EKLENMEDİ; OLCUT.md'de "koşucu bağlantısı yapılmadı" notu var.

## Dokunulmadı / not
- `agents/story.md` kota cümlesi (Dalga 2 notu): listede yoktu, dokunulmadı.
- `agents/copy.md` Bash aracına sahip değil: `copy_kontrol.py` komutunu lider koşar diye yazıldı. Panel de Bash'siz; medyanı lider/director koşar.
- Eşik rakamı hiçbir OLCUT'a yazılmadı.

## Test çıkışları
- `claude plugin validate plugins/viral-urun-ekibi`: Validation passed
- `scripts/sozlesme_test.py`: 63/63
- `scripts/ad_testi.py`: 0 hata, GEÇTİ
- `ortak/sinav/roller/rol_fikstur_test.py`: GEÇTİ (17 rol, 28 sabit, 28 eksik girdi)
- `scripts/anonim_kontrol.sh`: temiz
