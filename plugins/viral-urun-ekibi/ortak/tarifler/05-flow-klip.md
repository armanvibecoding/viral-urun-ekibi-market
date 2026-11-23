# Tarif 05 — Flow klibi (Google Flow, Omni)

## Amaç
Gerçek bir kareden 9:16 kısa klip üretmek (ürün hareketi, metafor sahnesi). Kredi harcar: her klip deftere yazılır, tavan aşılmaz.

## Girdi
Başlangıç karesi: gerçek stok klibin karesi (`ffmpeg -ss … -frames:v 1`) ya da ChatGPT'den üretilmiş görsel · istem (İngilizce, tek hareket) · kredi tavanı (kullanıcı onaylı) · kullanıcının açık Flow oturumu (macOS Chrome).

## Sınırlar (değişmez)
- Giriş, hesap, satın alma, plan değişikliği yok; oturum kapalıysa dur.
- **"Kullanım hakları" / yeni şart / yeni onay kutusu çıkarsa ajan KABUL ETMEZ**: ekranı kullanıcıya göster, kullanıcı kendisi onaylayınca devam.
- **Politika reddinde aynı istem kelime oyunuyla tekrar denenmez** (ör. eş anlamlıya çevirip yeniden göndermek). Red kayda geçer; sahne stok/gerçek görüntüyle ya da kredisiz katmanla çözülür.
- Tek kare = tek klip (çoklu istek yanlış kareyi seçer). Aynı Chrome'da başka ajan Flow'u kullanıyorsa sırayla çalış.

## Adımlar
1. Ön ödeme tablosu (5 satır plan): hedef klip sayısı · klip başına kredi (onay kartından oku; ör. Omni 9:16 720p ×1 = 12) · toplam · tavan · durma ölçütü.
2. Başlangıç karesini `flow/kareler/` içine kaydet; kare ürünü/hayvanı/eli net göstermeli; yüz yok.
3. İstem: tek hareket, kamera sabit ya da çok yavaş; ses satırı (AUDIO) görüntüde olmayan olayı eklemesin; olması istenmeyenler "no text, no logo, no extra limbs".
4. Flow'da 9:16, Omni, ×1 seç; kare yükle; **onay kartındaki krediyi oku** ve deftere yaz; üret.
5. İndir (tek tek; Chrome çoklu indirmeyi keser — her indirmeden sonra `ls -lt ~/Downloads` ile ölç). Klibi `flow/klipler/<ad>.mp4` olarak taşı.
6. QC: `klip_qc.py flow/klipler/<ad>.mp4 --pano`; sıçrama çıkışı 0 ve `_qc.jpg` 4 fps her kare (ürün kendi kendine çalışıyor mu, uzuv/yüz değişiyor mu). Başarısızsa kırp ya da bir kez yeniden üret (tavan içinde); ikinci başarısızlıkta stok ile çöz.
7. Her klipten sonra defter satırı (aşağı).

## Kredi defteri biçimi (`flow/DEFTER.md`)
| # | Klip | Kare | Kredi | Toplam | Sonuç |
|---|---|---|---|---|---|
| 1 | F1_ad.mp4 | F1_ad.png (stok id) | 12 | 12 | indirildi |
Ekrandan okunan kalan kredi + saat; "politika reddi: N"; "yeni şart/onay kutusu: çıkmadı/çıktı".

## Kalite çıtası
Klip ≈ 4 sn (URE-01; süre uzatmak için ikinci kırpım sayılmaz) · ≥ 720p · `klip_qc` 0 · 4 fps panoda ürün mekaniği doğru · yüz/ırk/renk değişimi yok · defter satırı eksiksiz.

## Kapılar
`klip_qc.py` 0 · defterde toplam ≤ tavan · onay kutusu kabulü yok.

## Sık hata ve düzeltmesi
- Yanlış kare kullanıldı → tek kare = tek klip; iste ayrı üret.
- Patinin/elin ürüne basışı belirsiz → başlangıç karesinde temas anı hazır olsun.
- Politika reddi → istem tekrar yok; sahneyi stoğa çevir.

## Bitti tanımı
Klipler `flow/klipler/`, QC çıkışı 0, `DEFTER.md` güncel (toplam ≤ tavan), DURUM.md'de "kalan kredi" satırı.
