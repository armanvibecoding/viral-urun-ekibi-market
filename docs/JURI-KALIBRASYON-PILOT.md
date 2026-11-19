# Kör jüri: ilk geriye dönük test (pilot) — 2026-11-19

**Sonuç:** kör jüri kendi içinde tutarlı, ama ilk kareye bakarak gerçek performansı öngörmedi (ρ ≈ 0). Jüri hükmü şimdilik
DENEME'dir; tam video kareleriyle ve aynı nişten daha geniş bir setle yeniden ölçülmeden "jüri en iyiyi biliyor" denemez.

## Ne ölçüldü
- Set: çalışma projesindeki analiz veritabanından 20 gerçek ürün videosunun **ilk karesi** (tek kare; uygulama arayüzündeki
  beğeni/yorum sayaçları maskelendi, yoksa performans sızıyordu). 17'sinde izlenme + takipçi + paylaşım dolu; 3'ü "veri yok".
- Jüri: `video-juri` talimatıyla 3 bağımsız kopya (en güçlü model), eşleşmeyi ve sayıları görmeden.
- Komut: `juri.py pano --mod kalibrasyon --arayuz-maske` → 3 kopya → `juri.py kalibrasyon`.

## Sayılar (betik çıktısı)
| Ölçüm | Değer |
|---|---|
| Jüri toplamı ↔ performans (izlenme/takipçi + paylaşım/izlenme sıra ortalaması), n = 17 | ρ = −0,02 → UYUMSUZ |
| Jüri toplamı ↔ ham izlenme, n = 17 | ρ = −0,22 |
| Kopyalar arası sıra uyumu (3 çift, n = 20) | ρ = 0,91 – 0,94 |
| Alan yayılımı (std) | 1,28 – 2,27 (eski eleştirmende kanca 0,74, ikna 0,91) |
| `gercek` alanı ↔ performans | ρ = −0,48 (gerçekçi görünen kare daha az izlenmiş) |
| `ritim` alanı ↔ performans | ρ = −0,38 |
| `anlasilir`, `yazi` ↔ performans | ρ = +0,19 (eşik 0,2'nin altında) |

Eski eleştirmen kayıtlarında ayırt edicilik (`juri.py ayirt`, 45 satır): kanca ort. 6,76 · std 0,74 · aralık 6–8 ("ayırt etmiyor");
ikna ort. 7,35 · std 0,91 ("ayırt etmiyor"); gerçekçilik, yazı, ritim, ses std 1,04–1,39.

## Okuma
1. Yeni alanlar ayırt ediyor (aralık 2–10), yani "hep 6–8" sorunu kapandı. Ama ayırt etmek öngörmek değildir.
2. Üç kopya neredeyse aynı sıralamayı veriyor: üç kopya bağımsız üç göz değil, aynı zevkin üç tekrarı. Medyan gürültüyü alır,
   yanlılığı almaz. Yanlılığı yalnız performans verisi düzeltir.
3. En dikkat çekici bulgu: jürinin "gerçekçi" bulduğu kareler daha az izlenmiş. Bu sette çok izlenenler abartılı, tuhaf, açıkça
   yapay kareler. "Yapay görünüyor" bu ürün türünde tek başına kusur olmayabilir (tek set, tahmin; doğrulanmadı).

## Sınırlar (bu yüzden pilot)
- Tek kare videonun kendisi değildir; ritim, ses ve ilk 1,5 saniye yok.
- Set dar: 17 videonun 14'ü 8 milyon üstü izlenme (alt dilim neredeyse yok); nişler karışık; izlenme/takipçi hesabın
  büyüklüğünden etkilenir.
- Kaydetme sayısı veritabanında hiç yok (0/628); reklam veritabanında 0 reklam; mağaza analitiği yok.

## Sıradaki ölçüm (jüriyi kalibre etmek için)
1. Aynı nişten 20+ video, üst/orta/alt dilim eşit (`juri.py set --nis …`), her videodan tam kare dizisi (ilk 2 sn 5 kare/sn).
2. Aynı hesabın çok izlenen ve az izlenen videoları eşlenerek (hesap etkisini sabitlemek için).
3. ρ ≥ 0,5 çıkmadan jüri eşiği (toplam ≥ 7, sonuncu değil) kapı olarak sıkılaştırılmaz; çıkmazsa alan tanımları
   performansla en çok uyuşan alanlara göre yeniden yazılır (bu pilotta aday: `anlasilir`, `yazi`).
