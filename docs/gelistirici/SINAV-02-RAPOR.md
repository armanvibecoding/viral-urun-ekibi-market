# SINAV-02 raporu · 02-kanca-senaryo (2026-11-24)

Çıktılar depo dışında: `kreatif/sinav-kosu/02-kanca-senaryo/tur1|tur2/{a-kolay,b-zor,c-tuzak}` (vakalar: a TR, b DE, c US). Üretim bir betikle yapıldı (30 senaryo × 3 vaka elle yazılmış veri + şablon alanları); kareler HyperFrames şablonlarıyla (`kalin_kontur` kanca karesi, `urun_gecisi` yer tutucu ürün karesi) `snapshot` ile alındı. AI üretimi, kredi, indirme yok.

## Tur × vaka × kapı
| Kapı | tur1 a | tur1 b | tur1 c | tur2 a | tur2 b | tur2 c |
|---|---|---|---|---|---|---|
| dosyalar | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ |
| on_uretim_karti (+_vaka) | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ |
| senaryo_kontrol | GEÇTİ | GEÇTİ | KALDI (`an` tekrarı) | GEÇTİ | GEÇTİ | GEÇTİ |
| senaryo_adedi (30) | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ |
| kanca_varyasyon | KALDI (K14) | KALDI (K14) | KALDI (K14) | GEÇTİ | GEÇTİ | GEÇTİ |
| yasakli / zorunlu | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ | GEÇTİ |
| juri | bekliyor | bekliyor | bekliyor | bekliyor | bekliyor | bekliyor |
Koşucu çıkışı: tur1 = 1 (KALDI), tur2 = 3 (yalnız jüri `bekliyor`; 0/3 kör kopya, referans panosu 3+ çözüldü, pano hazır). Not: tur1 klasörü, düzeltilmiş veriyle yeniden yazıldı; tur1 sonuçları yukarıdaki ilk koşudan.

## Kök neden
1. **kanca_varyasyon: "aile 'K14' kütüphanede yok" — sınıf (a), eklenti.** `kanca-kutuphanesi.md` S24 turunda K14 ve K15'i yalnız tablo satırı olarak ekledi; `on_uretim_karti.py` ve `kanca_varyasyon.py` aileyi `### K<n>.` başlığı olarak arıyor. Yani belgelenmiş (KURAL etiketli, `hf-sablonlar/README.md`'de şablona bağlı) iki aile, kapılar tarafından reddediliyordu; story ajanı K14 kullanınca kapı kırılıyordu. Düzeltme: kütüphaneye `### K14.` ve `### K15.` başlıkları eklendi (içerik tabloda kalır, çift yazılmadı). Eşik/kapı gevşetilmedi. Test: `kanca_varyasyon_test.py`'ye "K14 ve K15 kabul edilir" eklendi (8/8).
2. **senaryo_kontrol c-tuzak: `an` iki videoda aynı — sınıf (b), benim üretim hatam.** Veri girişinde kopya; benzersiz yapıldı.
Ajan yönergesi (`agents/story.md`) değişmedi: yanlış yönlendiren cümle bulunmadı; K14 kullanımını engelleyen şey kütüphane/başlık uyumsuzluğuydu.

## Değişen dosyalar (depo)
- `plugins/viral-urun-ekibi/skills/studio/referans/kanca-kutuphanesi.md` (K14/K15 başlıkları)
- `plugins/viral-urun-ekibi/skills/cut/scripts/kanca_varyasyon_test.py` (yeni test)
- `docs/gelistirici/SINAV-02-RAPOR.md`

## Kapılar
`musteri_icerik_kontrol.py` 0 · `sozlesme_test.py` 0 (49/49) · `sinav_kos_test.py --hizli` 0 · `kanca_varyasyon_test.py` 0 · `on_uretim_karti_test.py` 0 · `senaryo_kontrol` her vaka 0. `anonim_kontrol.sh` çıkış 1: tek eşleşme başka ajanın `SINAV-06-RAPOR.md` dosyasında (4. satır, yerel yol benzeri ifade); benim dosyalarımdan değil, dokunulmadı. `.hyperframes/` önbelleği depoda yok (işler depo dışında çalışma klasöründe).

## Açıklar
- Jüri kapısı ölçülmedi (kör kopyalar liderde); mekanik kapılar tamam ≠ kalite kanıtı: onuretim kareleri yer tutucu (düz zemin + daire + kanca yazısı), jüri gerçek ürün karesi olmadan düşük puan verebilir.
- Kancanın gerçekten durdurup durdurmadığı ve kanıt numarası-kanca anlam uyumu ölçülemez (OLCUT).
- Kanca karesi `tipografi.py` kuralı 7 kelime sınırlı; `on_uretim_karti.py` TR dışı pazarda sınır koymuyor. c-tuzak kartında 9 kelimelik K12 render'da reddedildi, kart için ≤7 kelimelik kanca seçildi (iki araç arasında tutarsızlık, küçük; kapı değiştirilmedi).
- Senaryo metinleri şablon desteğiyle toplu üretildi; ortam/giriş alanları otomatik, jüri ve insan gözü "tekdüze" bulabilir. Sağlık iddiası yok (c-tuzak imâ: omuzlar geride, hatırlatır), yasaklı desen taraması temiz.
