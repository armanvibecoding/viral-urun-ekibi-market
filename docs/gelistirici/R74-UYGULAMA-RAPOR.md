# R74 uygulama raporu (uzman yöntemi, 2026-11-24)

Etiket: "uzman yöntemi (R74)" = uygulayıcı yöntemi, istatistik kanıtı değil. Depo kökü: `plugins/viral-urun-ekibi/`.

## Karar -> nereye işlendi
| Karar | Dosya |
|---|---|
| A açık döngü (`kanca_sorusu`, `cevap_an`) | `skills/studio/scripts/senaryo_kontrol.py` (eksik = HATA, aralık süre×0,4..süre dışı = UYARI) · `referans/senaryo-formati.md` · `agents/story.md` |
| B soru zinciri (`zincir`) | `senaryo_kontrol.py` (≤25 sn en çok 2, üstü 3, aşarsa HATA) · `story.md` · `kanca-kutuphanesi.md` |
| C kanca sıkılaştırma (`kanca_onceki`, `sayi_kaniti`) | `story.md` (10 kancaya tur) · `senaryo-formati.md` · betik UYARI |
| D biçim kopyala | `ortak/tarifler/11-bicim-kopyala.md` + `ekler/chatgpt/tarifler/11-bicim-kopyala.md` (betiksiz sürüm elle yazıldı; build.py depoda yok) · iki README tablosu |
| E içerik hunisi | `skills/studio/referans/olcum-ve-test-plani.md` §3b (erişim / satış ayrı tablo, "en çok izlenen en çok satan değildir") · `story.md` |
| F tekrar yayın | `ortak/tarifler/10-kanca-varyasyon-testi.md` adım 7 + chatgpt 10 adım 6 · olcum §3d |
| G tutma eğrisi | olcum §3c + `agents/fixer.md` (kök neden adımı) |
| H sahte AI reklam | `referans/uretim-kurallari.md` §6 madde 3 + `studio/SKILL.md` |
| I tek planlı test | `referans/sahne-sablonlari.md` S11 (senaryoda `sablon: S1` olarak kaydedilir) |
| J biçim kütüphanesi | tarif 11 (haftada ≥10 kayıt, kare sırası zorunlu) |
| R1/R2 | `skills/cut/hf-sablonlar/tipografi.py`: `ikili_kiyas`, `deneme_sayaci`; `sablon.css`; README (parametre + dayanak satırı); `ornek_uret.py` iki örnek (`ornekler/ikili_kiyas`, `ornekler/deneme_sayaci`) |
| R4 | `senaryo_kontrol.py`: marka (kökte `marka`) / biz / we / our / yeni koleksiyon / new collection ile başlayan kanca = HATA |

## Test çıktıları
- `hf-sablonlar/sablon_test.py`: 12/12 geçti (yeni: test_ikili_kiyas, test_deneme_sayaci; kırma: çift soru, 8 kelime, boş etiket, kötü kazanan, cevap anı dışı, adım sayısı/sırası/aralığı, güvenli alan).
- `studio/scripts/senaryo_kontrol_test.py` (yeni): hepsi geçti, çıkış 0 (7 R4 kırma, A/B/C).
- `on_uretim_karti_test.py`, `cut/scripts/juri_test.py`, `kanca_varyasyon_test.py`: çıkış 0.
- `scripts/anonim_kontrol.sh`: temiz · `musteri_icerik_kontrol.py`: GEÇTİ · `sozlesme_test.py`: 49/49.
- Örnek HTML üretildi; `npx hyperframes check` KOŞMADI (paket yerelde kurulu değil, render şart değildi). `.hyperframes/` yok.

## Bilinenler / dikkat
- `build.py` depoda yok; `--check` koşulamadı.
- `kendini_test.py` (cut) ve `sinav_kos_test.py` 100 sn üstü sürdü, durduruldu; bu işle ilgisiz, koşulmadı.
- Yeni zorunlu alanlar (`kanca_sorusu`, `cevap_an`) eski senaryolar.json'ları HATA verir; `kapi.py` ve `sinav_kos.py` aynı betiği çağırır, üretim ajanları yeni alanları yazmalı.
- `senaryo_kontrol.py` mevcut "işte" yasak kalıbı alt dizgiyle eşleşir ("geçişte" yakalanır); dokunulmadı.
- Commit/git add yapılmadı.
