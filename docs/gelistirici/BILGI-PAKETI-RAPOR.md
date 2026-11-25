# Bilgi paketi raporu (2026-11-25)

## Girenler
- `plugins/viral-urun-ekibi/ortak/bilgi/viral-urunler.tsv`: 542 ürün, 15 sütun (beyaz liste). Üretici: `scripts/bilgi_paketi.py <analiz.db>`; aynı db iki kez koşuldu, çıktı bayt bayt aynı.
- `ortak/viral_db.py` + `ortak/viral_db_test.py`: `ara(urun_metni, aile=None)` -> `{durum: yok|aile-var|ayni-urun-viral, eslesen}`; tablo yoksa `dogrulanamadi`. Eşleşme kuralı `bazaar_kontrol.py viral` ile aynı (>=4 ortak sözcük + VIRAL-URUN; aile kesişimi).
- `ortak/bilgi/dersler.md`: "Kurucu hafızasından (sansürlü)" bölümü, 25 ders. `README.md` tablosuna 2 satır.

## Dışarıda bırakılanlar ve neden
- url, hesap, hesap_id, kaynak_ref, not_dosyasi, sayilar_ham, yorum: kişi/hesap kimliği ve ham veri.
- Ham `urun_id`: 400+ satırda `h-in-<hesap adı>` biçiminde hesap adı taşıyor; yerine ad kökünden türetilen 8 haneli özet kod (`vXXXXXXXX`) kondu.
- reklam_mi: beyaz listede yok. `yayin_tarihi` db'de tamamen boş; ilk/son görülme `okuma_tarihi`, o da yoksa kayıt tarihinden türetildi.
- Ürün adından atılanlar: " — " sonrası, parantez içi, cümle ortası özel ad, tamamı büyük harf, model kodu, camelCase, katalogdaki hesap/alan adı jetonları, bilinen marka listesi.
- Dersler: proje/kişi/marka/hesap adı, yol, sunucu, fiyat sözleşmesi, danışmanlık konuşması, test/kapı genel dersleri (kapsam dışı) alınmadı.

## Sansür testi
- `python3 scripts/bilgi_paketi_test.py --db <analiz.db>` -> `GEÇTİ (542 satır, 28 kara liste deseni okundu)`, çıkış 0. Kırma testleri (sahte `@ornekhesap` + `https://x` satırı, ek sütun, sentetik kara liste deseni, telefon, e-posta, ev yolu) kapıyı kırdı.
- `sh scripts/anonim_kontrol.sh` -> temiz, çıkış 0. `claude plugin validate plugins/viral-urun-ekibi` -> geçti.

## Sınırlar
- Ürün adı sansürü sezgiseldir (küçük harfle yazılmış marka kaçabilir); yeni db sonrası test ve çıktının göz taraması tekrarlanmalı.
- `ad_jenerik` kısaldığı için "ayni-urun-viral" için gereken 4 ortak sözcük bazen analiz.db'ye göre daha az eşleşir (daha temkinli).

## Lidere bağlantı önerisi
`bazaar_kontrol.py viral`: `--db` verilmemiş ya da dosya yoksa `dogrulanamadi` yerine `from viral_db import ara` ile TSV'den sınıflandır (ortak/ klasörünü sys.path'e ekle).
