# Tarif 10 — Kanca varyasyon testi (aynı çekim, 10+ kanca)

## Amaç
Küçük drop-marka hesapları aynı çekimle 10–25 farklı kanca dener; hit oranı ~1/25, hit çoğu kez tek varyasyondan gelir (saha S24: 3 profil). Bu tarif aynı çekimden N sürüm üretir, yayın planını ve ölçüm kaydını yazar.

## Girdi
Tamamlanmış tarif 01 ayarı (kutulu stil, ön-üretim kartı dahil) · `kancalar.json` (≥ 10 kanca; her biri `id`, `aile` K<n>, `yazi`, `vurgu`, `kanit` numaraları — kütüphaneden) · pazar (kartta).

## Adımlar
0. **Ön-üretim kartı** (tarif 01 adım 0) geçerli olmalı; varyasyonlar kartın pazar/format/sahne kararını paylaşır, yalnız kanca değişir.
1. Kanca listesini kütüphaneden seç (`studio/referans/kanca-kutuphanesi.md`): farklı ailelerden (K1 yasak, K2 zorunluluk, K14 itiraz alıntısı, K12 soru, K13 yazısız…) en az 10; aynı aileden ikiden fazla değil. Her satıra kanıt numarası.
2. Üret: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/kanca_varyasyon.py" is/NN/kurgu/V01.json is/NN/kurgu/kancalar.json --render`
   → `varyasyon_V01.json …` + `varyasyon/V01.mp4 …` + `varyasyon/yayin-plani.md` + `varyasyon/kayit.tsv`.
3. Her videoyu tarif 01 kapılarından geçir (`kurgu_kontrol`, `--goruntu`, `ses_olc --kapi`).
4. Yayın: plan tablosundaki sırayla (varsayılan 24 saat arayla); yayın aşamasında ses etiketi seçilir ve `kayit.tsv`'ye yazılır.
5. Ölç: 24 s / 48 s / 7 gün (`olcum-ve-test-plani.md` §3–4); karar 48. saatte, ≥ 2.000 izlenmede. Eşikler: DEVAM paylaşım/izlenme ≥ %0,61 ve beğeni/izlenme ≥ %1,01 · ÖLDÜR < %0,21 ve < %0,75. **AB/UK'de ABD eşiğiyle öldürme yok; TR'de eşik yok, ilk partiden sonra kalibre.**
6. Parti kararı: hiçbiri DEVAM değilse **görüntüyü** değiştir (kanca değil), yeni klip setiyle 2. parti. Kazanan: aynı kanca + yeni sahne ya da aynı görüntü + 3 yeni kanca. Kazanan kancayı `kanca-kutuphanesi.md`'ye kanıt olarak ekleme kuralı: tarif 08.

## Pazar ayrımı
ABD güçlü veri; AB/UK paylaşım beklentisi ABD'nin yarısı (eşikle öldürme yok); TR verisi zayıf — kanca ≤ 8 kelime ve ilk testten sonra kalibre (`kanca_varyasyon.py` TR'de 8 kelimeyi aşan kancayı reddeder).

## Kalite çıtası
≥ 10 benzersiz kanca · her kancada aile + kanıt numarası · yalnız kanca değişir · her video tarif 01 kapılarından geçmiş · yayın planı + kayıt tablosu dosyada.

## Kapılar
`kanca_varyasyon.py` çıkış 0 · `kanca_varyasyon_test.py` 0 · her varyasyon için tarif 01 kapıları 0.

## Sık hata ve düzeltmesi
- 9 kanca → betik reddeder (en az 10). · Aynı kanca iki kez → reddeder. · Kütüphanede olmayan kanıt numarası → reddeder (uydurma kanıt yok).
- Üç hafta sonra hiçbiri DEVAM değil → kanca değil görüntü sorunu (N2: kanca paylaşım çarpanıdır, durduran şey görüntü).

## Bitti tanımı
N video + `yayin-plani.md` + `kayit.tsv`; yayın sonrası 48. saat kararı tabloya yazılmış; kazanan kalıp DURUM.md'de.
