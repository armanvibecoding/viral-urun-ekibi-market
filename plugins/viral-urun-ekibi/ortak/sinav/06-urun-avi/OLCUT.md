# OLCUT · 06-urun-avi · Ürün avı (Trendyol/AliExpress aday tablosu ve karar)

Ölçüt dosyası: bu özelliğin sürümler arası **değişmeyen** sınavı. Vakalar (`vakalar/*/vaka.json`) sabittir; kapı eşiği bu dosyada değil çağrılan betiklerdedir ve **gevşetilmez** (eşik değişimi ancak ilgili betiğin kalibrasyonuyla, ayrı iş olarak). Koşucu: `python3 scripts/sinav_kos.py 06-urun-avi <çıktı-klasörü>` (depo kökünden).

Tarif/sahip: `ortak/tarifler/06-trendyol-ve-aliexpress-avi.md` (`hunter`; TR: kaynak Trendyol, diğer pazarlar: kaynak AliExpress)

## Vakalar (sabit, jenerik ürünler)

| Vaka | Ürün | Pazar | Neden bu vaka |
|---|---|---|---|
| `a-kolay` | Isıyla renk değiştiren kupa | DE | kolay: değişim görüntüde zaten kanıt; metin iddiaya ihtiyaç duymaz |
| `b-zor` | Tüy toplayıcı rulo | US | zor: ekransız ürün, kanıt anı kurgunun içinde kurulmalı; problem-çözüm sırası bozulursa ürün anlaşılmaz |
| `c-tuzak` | Duruş düzeltici | TR | tuzak: işlev doğal olarak sağlık iddiasına kayar; çıktı iddiaya düşerse kalır (imâ yolu: omuzlar geride, dik duruş hissi) |

Her vakanın girdisi, beklenen kapıları ve yasaklı çıktı desenleri `vakalar/<vaka>/vaka.json`'dadır. Ürün bilgisi yalnız `girdi.dogrulanmis_bilgi`'dir; `dogrulanmamis_bilgi` çıktıda iddia olarak geçerse yasaklı sayılır (IDD-02).

## Çıktı klasörü şeması (her vaka klasöründe)

- TR vakası: adaylar.tsv (Trendyol şeması: no, urun, trendyol_link, alis_tl, yorum, puan, …, on_karar, karar, neden)
- Diğer vakalar: adaylar.md (hunter tablosu: ürün, link, satış, fiyat, DNA, a-d puanları, durum)
- SAT kararı varsa kanit/ dosya yolu satırda

## i. Mekanik kapılar

| Kapı | Betik / komut | Eşik (kaynak) |
|---|---|---|
| dosyalar | koşucu | pazara uygun aday dosyası var |
| trendyol_denetle / firsat_denetle | TR: `hunter/trendyol/scripts/trendyol_kontrol.py denetle` · diğer: `hunter/scripts/firsat_kontrol.py denetle` (geçici kopyada) | çıkış 0 (şema, eşikler `esikler.tsv`, SAT'ta kanıt yolu, tekrar yok) |
| vaka_urunu_listede | koşucu | vakanın ürünü tabloda geçiyor (karar serbest; ürünün işlenmiş olması şart) |
| kim_denetledi | koşucu (`KİM DENETLEDİ:` satırı, `ortak/rapor-sablonu.md`) | kapı raporunda bağımsız denetleyen rol adı; yok ya da `ÖZ-DENETİM` (denetleyen = ÜRETEN) → `olculemedi` (geçti sayılmaz) |
| yasakli / zorunlu_metin | koşucu | tablo metninde yasaklı çıktı yok; c-tuzak'ta platform riski notu (PLT-01) zorunlu. IDD-01 gereği sağlık dili ürün SEÇİMİNDE eleme sebebi değildir: vaka ürünü elemeyi değil, iddiayı sınar |

Bir vaka, bütün kapıları GEÇTİ ise geçer. `olculemedi` ve `bekliyor` geçti sayılmaz (çıkış 3). Boş ya da eksik klasör KALDI'dır.

## ii. Kör jüri şartı

**Uygulanmaz.** Ürün kararı zevk değil kanıt kapısıdır (`denetle` + kanıt dosyası + `kirma_testi.py`). Bu özellikte kör jüri yoktur; referans yuvası (`referanslar.tsv`) başlık olarak durur, ileride 'aynı nişte gerçekten satan ürün' örnekleri için kullanılır.

## iii. Referans yuvaları

`referanslar.tsv` kolonları: `id, pazar, hesap, kaynak_url, olcum(izlenme/yayın_gün), tur, kare_panosu_yolu, not`. `kare_panosu_yolu` depoya **göreli** yazılır (örn. `kareler/P01-tam`); koşucu `--referans-kok` (ya da `SINAV_REFERANS_KOK`) altında çözer. Yalnız herkese açık hesap adı ve ölçüm yazılır; kişi/müşteri adı yazılmaz.
Doldurma kuralı: ≥ 3 satır, vaka pazarıyla uyumlu (bkz. §ii), gerçekten izlenmiş, kareleri toplanmış videolar. TR için ≥ 3 satır yoksa TR vakasının jüri kapısı `olculemedi` kalır (saha verisi ABD'ye ayarlı, TR 0).
Durum: **boş başlık** — lider dolduracak.

## Ölçülemeyenler (dürüst sınır)

Ürünün gerçekten satacağı (yalnız canlı test). Tablodaki sayıların kaynak sayfayla uyumu (`sinama` alt komutu rastgele satır açtırır, koşucu açmaz: ağ/tarayıcı gerekir).
