# Tarif 0.5.0 durum (dal tarif-0.5.0) — 2026-11-24

| # | İş | Durum |
|---|---|---|
| 1 | ortak/tarifler/ (01–09 + README) | yazıldı |
| 2 | skills/cut/scripts/hikaye/ hat + test_hikaye.py | uçtan uca 13/13 hem ffmpeg yedeğiyle hem GERÇEK HyperFrames render'ıyla (`test_hikaye.py --hf`, hf@0.9.65) |
| 3 | Kullanım bulguları 6/6 | (1) kurgu_kontrol `urun_tipi` + kırma testi · (2) studio/cut → tarif 01, hizli_kurgu `kutulu` · (3) `juri.py yapilamadi` + kapi.py + test · (4) bazaar SAT-KOSULLU + kırma + oran turu · (5) captain tek öneri · (6) README uyarısı |
| 4 | SKILL.md yönlendirmeleri | yapıldı (butce_kontrol 0) |
| 5 | Sürüm 0.5.0 | plugin.json, CHANGELOG, marketplace, README'ler |
| 6 | Kapılar | anonim · validate ×2 · sozlesme · ad_testi (+kendini) · butce (+kendini) → 0; build --check · pytest · captain kapi/karne · cut kendini/juri · spy kendini/toplayici · hunter/bazaar kirma · excel_test · hikaye testi → hepsi 0 |
| 7 | paketle + ZIP kopyası | CLAUDE 4.023.561 B · CHATGPT 1.875.121 B → masaüstüne kopyalandı (0.5.0 adıyla) |

Not: CHANGELOG 0.4.0 "Kaldırılacak (0.5.0): eski beceri adı yönlendirmeleri" der; görevde yoktu, kaldırılmadı (lider kararı).

## Kurucu eki (2026-11-24 01:40–02:17) — aynı dalda
| # | Ek | Durum |
|---|---|---|
| E1 | Bilgiyi zorunlu kullan: video tariflerinin ilk adımı ön-üretim kartı (`studio/scripts/on_uretim_karti.py`; hikaye_kur + kutulu hizli_kurgu kartsız çalışmaz) | yapıldı; kırma testi `on_uretim_karti_test.py` (20) + `test_hikaye.py` |
| E2 | Pazar ayrımı (ABD / AB-UK yarı eşik / TR zayıf) ve müzik "ölçülmedi" tarif 01–04, 06, 10'da | yapıldı; kart şeması AB'de `esik`, TR'de `tr_veri_zayif` + ≤ 8 kelime ister |
| E3 | ChatGPT betiksiz tarifler (`ekler/chatgpt/tarifler/` 10 tarif + özet + istemler), paketleyici güncel | yapıldı; ZIP içeriği okundu |
| E4 | `ses_olc --vo`: sıçrama müzik stem'inde (duck uygulanmış); kapı gevşetilmedi | yapıldı; kırma: VO+duck −10 dB GEÇER (0), --vo'suz konuşma hecesine takılır (4), rampasız ani müzik KALIR (3) |
| E5 | Saha S24: kanca kütüphanesine K14/K15 + gözlemler, `muzik-kutuphanesi.md`, pazar-katmani ABD'ye ayarlı notu, S8 vekil nesne | yapıldı (kullanıcı adı yok, kanıt kodu S24-…) |
| E6 | Video yapısı: sahne-sablonlari "Ortak: süre ve döngü"; tarif 01 döngü + tatmin + kanca↔CTA; `kurgu_kontrol` `format=dongu` kuralları (dongu/tatmin/cta/plan) + kırma testi | yapıldı |
| E7 | Tarif 10 kanca varyasyon testi + `kanca_varyasyon.py` (N sürüm, plan, kayıt) + kırma testi | yapıldı |
| E8 | Radar profil derin tarama + `radar/referans/profil-notu.md` | yapıldı |
