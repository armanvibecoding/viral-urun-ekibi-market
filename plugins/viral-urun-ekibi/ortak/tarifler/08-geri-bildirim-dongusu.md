# Tarif 08 — Geri bildirim döngüsü

## Amaç
Kullanıcı ya da ortak aynı geri bildirimi ikinci kez yazmak zorunda kalmasın: bir kez alınır, kalıcı kurala dönüşür, bir sonraki üretimde ilk turdan uygulanır.

## Girdi
Geri bildirim metni (sohbet, ekran görüntüsü, ortak mesajı) · hangi videoya/ürüne ait olduğu.

## Sınırlar
WhatsApp ve benzeri mesajlaşma uygulamaları **yalnız okunur** (yazma, yanıtlama, onay yok). Kişisel veri (ad, numara) kurala/depoya yazılmaz.

## Adımlar
1. Geri bildirimi maddelere böl; her madde: **gözlem** (ne görüldü) · **kök neden** (sınıf: kurgu · yazı · ses · malzeme · tavan) · **kural önerisi**.
2. Önce **ürün kontratına** (`is/NN/kurgu/KURALLAR.md`) ya da `.ekip/DERSLER.md`'ye yaz (URE-02 basamak 1).
3. Aynı kusur anahtarı ikinci kez (başka ürün/video) görülünce eklenti dosyasında yerinde düzelt (kural, tarif ya da betik varsayılanı). Tarif varsa tarifin "Sık hata" bölümüne bir satır, betikte varsayılan değişikliği ayrı commit.
4. `geri_bildirim_kontrol.py` (captain/scripts) çalıştır → çıkış 0.
5. Düzeltmeyi uygula, yeni sürümü üret; kullanıcıya "şu 3 madde artık varsayılan" diye tek mesaj.
6. **Hüküm hattı** (video): referans ≥ 3 → `juri.py pano --mod teslim` → `jury` 3 kopya → `juri.py birlestir`; kalırsa `fixer` kök neden + tek değişkenli emir. Referans < 3 → iş durmaz; "jüri yapılamadı (referans < 3)" notuyla teslim edilir, referans bulma ayrı iş olarak DURUM.md'ye yazılır.

## Kalite çıtası
Her geri bildirim maddesi 24 saat içinde kontrata ya da derslere yazılmış · aynı madde ikinci kez gelmemiş (gelirse eklenti kuralı eksik demektir) · kullanıcıya soru yok, karar + gerekçe var.

## Kapılar
`geri_bildirim_kontrol.py` 0 · `butce_kontrol.py` 0 (kural tek kaynakta).

## Sık hata ve düzeltmesi
- Geri bildirim sohbette kaldı, dosyaya yazılmadı → "yazılmayan karar yok sayılır"; aynı turda yaz.
- Kural uzun anlatıyla SKILL.md'ye girdi → anlatı `ortak/bilgi/dersler.md`'ye, kural `kurallar.md`'ye.

## Bitti tanımı
Kural dosyada, kapı 0, bir sonraki üretimde ilk tur aynı geri bildirimi almadı.
