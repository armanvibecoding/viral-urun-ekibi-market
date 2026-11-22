# Sıra puanı, kanıt dosyası ve SAT / İZLE / ELE

Ne zaman okunur: aday sıralanırken ve kısa listeye kanıt dosyası yazılırken (akış adım 5–7).

## 1. Sıra puanı (yalnız K1–K3 kapılarını geçmiş, DNA ≥4 adaylar)
DNA puanı adayları ayırt etmiyor (gerçek listede çoğu 5–7/7 aldı). Sıralama bu dört eksenle yapılır:

| Eksen | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **A** Mekanizma gücü | akraba yok | akraba var, mekanizma zayıf (M4/M13 tek başına) | akraba 1–2 milyon | akraba ≥3 bağımsız markada milyon ya da M2/M3 |
| **B** Girilebilirlik (pazar) | aynı ürün pazarda çok satıcı + ucuz | aynı ürün var, birkaç satıcı | yalnız niş satıcı / pahalı orijinal | pazarda aynısı yok |
| **C** Marj (hedef satış ÷ normal maliyet+kargo) | <1,5× | 1,5–2× | 2–3× | ≥3× |
| **D** Üretilebilirlik (videoda gösterme) | — | gösterilir ama mekanizma doğrulanmadı / AI bozabilir | gerçek çekim ya da AI ile net gösterilir | — |

Toplam 0–11. Eşitlikte B büyük olan önde. Satış fiyatı hedefi: seçilen pazarda 25–70 $ bandı veya pazardaki en yakın rakibin biraz altı/üstü (gerekçesiyle).

## 2. Karar kuralı
- **SAT:** sıra ≥8 **ve** kanıt dosyası var **ve** çürütme denemeleri tutmadı **ve** mekanizma gerçek alıcı fotoğrafı/videosuyla doğrulandı **ve** sınama geçti.
- **İZLE:** sıra 6–7, ya da SAT koşullarından biri "doğrulanamadı" (numune şart, sezon uzak, TR gönderim belirsiz…). Ne beklendiği tek cümleyle yazılır.
- **ELE:** kapıdan kalan, veto, zaten viral, ya da sıra ≤5. Sebep ürüne özgü tek cümle → `is/firsat/elenenler.md`.
- Gerekçe ürüne özgü olmalı ("güzel ürün" değil, "aynı ürün Walmart'ta 24 $, bizim maliyet 22 $ → marj yok").

**Ders (kaynak çalışma):** en yüksek puanlı aday seçildi, satıcı videosu AI'dı ve ürün kareden kareye değişiyordu; mekanizma hiç doğrulanmadan 30 video üretildi ve kullanılamadı.
→ Mekanizma doğrulanmadan SAT verilmez; şüphede İZLE + numune.

## 3. Kanıt dosyası şablonu — `is/firsat/kanit/NN-urun-adi.md`
```
# NN — <ürün adı> — Karar: SAT | İZLE | ELE
Tek cümle gerekçe (ürüne özgü).
Pazar: <TR/ABD/…> · Tarih: YYYY-AA-GG · Aday satırı: is/firsat/adaylar.md #N

## Çürütme denemeleri (önce bunlar; her biri bulgu + URL)
1. Daha önce denendi mi? (TikTok/YouTube/Instagram, Shopify mağazaları; denenip öldüyse neden)
2. Doygunluk (pazar mağazası: aynı ürün kaç satıcı, fiyat)
3. İlgi trendi (Google Trends = göreli ilgi, satış değildir)
4. Marj (tablo aşağıda)
5. Risk: reklam politikası, kargo (kırılgan/ağır/pil/sıvı), iade, IP/tasarım tescili, gümrük
6. Gösterilebilirlik: fayda 3 sn'de gösterilir mi, hangi mekanizma (M kodu)?
7. Mekanizma doğrulama: gerçek alıcı fotoğrafı/videosu linki — yoksa "doğrulanamadı"

## Lehte kanıt (çürütme bittikten sonra)
## Marj tablosu (iniş maliyetiyle — `marj_hesap.py` çıktısından kopyala; `referans/marj-ivme-puan.md` §1)
| Pazar | Ürün | Kargo | Gümrük/tarife | Aracı | Ödeme | İade/COD reddi | İniş | Satış (net) | Kâr | Çarpan | Teslim (gün) | Rakip fiyatı (URL) |
UYARI satırları (doğrulanmamış oran) "Bulunamayan veri"ye aynen yazılır.
## İvme (t0 → t7, `ivme_olc.py bant`)
| Sinyal | t0 (tarih) | t7 (tarih) | Bant |
## Ürün puanı (P1–P10, 0–20; eşik deneme)
## Riskler
## Nasıl viral olur: en uygun 3 kanca + format (mekanizma kodu ve akraba not no ile)
## Bulunamayan veri
```
Bulunamayan veri "bulunamadı/doğrulanamadı" yazılır, tahminle doldurulmaz.

## 4. Sınama (ajan çıktısı kabulünden önce, zorunlu)
1. `python3 "<beceri klasörü>/scripts/firsat_kontrol.py" sinama is/firsat/adaylar.md` → rastgele 3 satır.
2. Üçünün ürün sayfasını aç: satış, normal fiyat, ürün kimliği (benzer ≠ aynı) tutuyor mu?
3. Desen iddiası varsa (akraba not no): `ortak/viral-dna.md`'de o not o mekanizmada geçiyor mu?
4. Biri tutmazsa tablonun tamamı "şüpheli" → ajan bulguyla tekrar çağrılır; hata türü `.ekip/DERSLER.md`'ye yazılır.
   Aynı hata türü 2. kez görülürse ajan talimatındaki yanlış yönlendiren cümle değiştirilir (kural eklemek yetmez).
