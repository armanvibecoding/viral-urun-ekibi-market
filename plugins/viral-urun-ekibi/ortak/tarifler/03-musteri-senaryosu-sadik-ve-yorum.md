# Tarif 03 — Müşteri/ortak senaryosu: A (sadık) + B (yorum)

## Amaç
Müşteri ya da ortak kendi senaryosunu verdiğinde onun sözünü bozmadan video üretmek; yorumumuz ayrı bir sürüm olarak sunulur. Önce A.

## Girdi
Senaryo metni (sahne sırası, ekran yazıları, seslendirme cümleleri) · ürün listesi/gerçek ürün fotoğrafı · müşterinin yasakları (varsa) · tarif 02 hattı.

## Adımlar
1. Senaryoyu sahne tablosuna çevir: `sahne · ekran yazısı · VO cümlesi · önerilen görüntü`. Tabloyu `is/NN/senaryo-A.md`'ye yaz; müşteri metnini satır satır koru.
2. **A (sadık) kuralı:** sahne sırası, ekran yazısı ve VO cümleleri aynen kalır. Yalnız şunlar çıkar/değişir ve her biri `senaryo-A.md` altındaki "Değişenler" listesine gerekçeyle yazılır:
   - uydurma ürün adı → gerçek ürün kod adı (sitedeki ad),
   - fiyat (ICE-01), kanıtsız istatistik/yüzde (IDD-02),
   - sitede olmayan teklif/ürün (rehber, danışmanlık, jel…) → çıkar, yerine sahne metni değiştirilmez, "ürünsüz" sahne olarak bırakılır,
   - organ/eylem adı, tanınabilir yüz (platform riski, PLT-01 uyarısı).
3. A için `hikaye/ayar.json` kur (tarif 02): her cümle tek sahne; müşterinin sırası = `sahneler` sırası.
4. VO varsa tarif 04; müzik VO altında duck edilir.
5. Kapılar (tarif 02) → `TESLIM/<ad>_A-sadik.mp4`.
6. Ancak A teslim edildikten sonra **B (yorum)**: aynı ürün için kendi kancamız, daha sıkı kurgu, Flow metafor klipleri (tarif 05). Dosya adı `_B-yorum`. B, A'yı geçmeden A'nın yerine sunulmaz.
7. Müşteriye iki dosya + "Değişenler" listesi gider; hangisinin hangisi olduğu dosya adında yazar.

## Kalite çıtası
- A'da senaryo metninin %100'ü korunur; sapma yalnız "Değişenler" listesindeki maddelerdir (liste boşsa sapma yok demektir).
- Her çıkarılan madde için gerekçe (kaynak: ürün sayfası ya da kural kimliği).
- A ve B ayrı dosya, ayrı kapı çıktısı.

## Kapılar
Tarif 02 kapıları iki sürüm için ayrı ayrı 0 · `senaryo-A.md` "Değişenler" bölümü var.

## Sık hata ve düzeltmesi
- A'yı "daha iyi yapmak" için cümle değiştirmek → geri al; iyileştirme B'dedir.
- Sitede olmayan ürünü ekranda göstermek → çıkar, "ürünsüz marka hikâyesi" olarak kur (ürün sahnesi yok).
- Kanıtsız istatistik ekranda kaldı → `senaryo-A.md` kontrol: her sayı için kaynak satırı yoksa çıkar.

## Bitti tanımı
İki video (A önce, B sonra) + "Değişenler" listesi + kapı çıktıları; DURUM.md'de her biri ayrı satır.
