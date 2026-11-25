# SINAV-04 raporu · 04-ses-muzik (2026-11-24)

Yöntem: görüntü düz renk yer tutucu; müzik `hf-sablonlar/muzik_sentez.py` (sentetik), karışım `scripts/ses_tasarla.py` (`--stem_klasoru` ile yerleştirilmiş stem), sentetik efekt (`tik`, `vurus`). Ücretli servis yok. Ses kulakla dinlenmedi; yalnız ölçüm. Çıktı klasörleri depo dışındadır (`<çıktı-kök>/04-ses-muzik/tur1`, `tur2`; üretim betiği `uret.sh`). Eşik, kapı, koşucu, `ses_olc.py` ve OLCUT.md değiştirilmedi.

## Tur 1 — `sinav_kos.py` çıkış 1 (a GEÇTİ · b GEÇTİ · c KALDI)
| Vaka | dosyalar | ses_kapi | ses_seviye | sure | lisans_kaydi | yasakli | juri |
|---|---|---|---|---|---|---|---|
| a-kolay | GEÇTİ | GEÇTİ (0) | GEÇTİ −14,1 LUFS · −1,2 dBTP · drop 6,2 dB | 12 sn GEÇTİ | GEÇTİ | GEÇTİ | uygulanmaz |
| b-zor | GEÇTİ | GEÇTİ (0) | GEÇTİ −14,1 · −1,2 · drop 6,1 | 15 sn GEÇTİ | GEÇTİ | GEÇTİ | uygulanmaz |
| c-tuzak | GEÇTİ | KALDI (3): ilk 1 sn müzik yok (−100,1 dB) | GEÇTİ −14,2 · drop 6,7 | 18 sn GEÇTİ | GEÇTİ | GEÇTİ | uygulanmaz |

Kök neden c (sınıf b, benim üretim hatam): müzik drop'u dosyada 7,5 sn, videoda 8,8 sn istendi; `muzik_bas < drop_video_sn` olunca müzik 1,3 sn geç başlıyor. Araç bunu zaten uyarıyor ve çıkış 2 veriyor (`ses_tasarla.py` UYARI satırı); ben çıkış kodunu yok saymıştım. Araç hatası değil.

## Tur 2 — çıkış 1 (a GEÇTİ · b GEÇTİ · c KALDI)
Değişiklik (üretim): c'de `drop_bar` 4 (müzik drop'u 10 sn > video drop'u 8,8 sn); tüm vakalarda `--drop_oncesi_db -12`.
| Vaka | ses_kapi | ses_seviye | diğerleri |
|---|---|---|---|
| a-kolay | GEÇTİ (0) | GEÇTİ −14,1 · −1,2 dBTP · drop 6,2 dB · giriş −29,7 dB, rampa 1,55 sn, basamak 6,3 dB | GEÇTİ |
| b-zor | GEÇTİ (0) | GEÇTİ −14,1 · −1,1 · drop 6,1 · giriş −40,9, rampa 1,6, basamak 5,8 | GEÇTİ |
| c-tuzak | GEÇTİ (0): giriş −32,6, rampa 1,9, basamak 4,4 | KALDI: drop artışı 4,9 dB (< 6) | GEÇTİ |

Kök neden c (sınıf b, üretim seçimi): `muzik_sentez.py` demosunda drop artışı toniğe bağlı; tonik 52 → 4,0–5,0 dB, tonik 57 → 6,1–6,9 dB (aynı video, 6 yapılandırma süpürmesi, `ses_tasarla.py` drop_artis_db). c'yi tonik 52 ile üretmiştim. Tonik 57 + 96 bpm = 6,9 dB ölçüldü, ancak bu ÜÇÜNCÜ bir koşu olurdu; "en çok 2 tur" kuralı gereği resmî tur olarak koşulmadı. Yani resmî sonuç: c-tuzak KALDI.

## Değişen dosya
- `plugins/viral-urun-ekibi/skills/cut/hf-sablonlar/muzik_sentez.py`: yalnız docstring, tonik–drop artışı ölçüm notu eklendi (davranış aynı; `drop_sn=` çıktısı doğrulandı). Eklenti kodunda başka hata bulunmadı.

## Kapılar
anonim_kontrol.sh 0 · musteri_icerik_kontrol.py 0 · sozlesme_test.py 0 · sinav_kos_test.py --hizli 0.

## Kalan açıklar
1. c-tuzak resmî olarak KALDI; düzeltme (tonik 57) tur dışı ölçümle doğrulandı, koşucu ile doğrulanmadı. Sonraki turda `uret.sh` içinde c için `tonik` 52 → 57 yapmak yeter.
2. Drop artışı marjı ince: 6,1–6,9 dB (eşik 6). Pembe gürültü tohumsuz olduğundan koşular arası ±0,2 dB oynar; aynı b-zor bir ara 5,9 verdi (tohumsuz yer tutucu ses). Demo müziğinin drop kontrastı tonik/bpm'e duyarlı; gerçek müzikte bu ayrıca ölçülmeli.
3. Yer tutucu video ile ses sınandı; gerçek klip sesi (konuşma, VO) yok, `vo.txt` boş ("yok"). Kulak onayı kullanıcıda.
4. Kapı yanlış ölçüyor mu: bu koşuda kapının yanlış ölçtüğüne dair kanıt yok.
