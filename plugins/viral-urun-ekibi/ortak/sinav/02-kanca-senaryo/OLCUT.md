# OLCUT · 02-kanca-senaryo · Kanca + 30 senaryo + kanca varyasyonu

Ölçüt dosyası: bu özelliğin sürümler arası **değişmeyen** sınavı. Vakalar (`vakalar/*/vaka.json`) sabittir; kapı eşiği bu dosyada değil çağrılan betiklerdedir ve **gevşetilmez** (eşik değişimi ancak ilgili betiğin kalibrasyonuyla, ayrı iş olarak). Koşucu: `python3 scripts/sinav_kos.py 02-kanca-senaryo <çıktı-klasörü>` (depo kökünden).

Tarif/sahip: `ortak/tarifler/10-kanca-varyasyon-testi.md`, studio Aşama 3 (story ajanı), `skills/studio/referans/senaryo-formati.md`

## Vakalar (sabit, jenerik ürünler)

| Vaka | Ürün | Pazar | Neden bu vaka |
|---|---|---|---|
| `a-kolay` | Isıyla renk değiştiren kupa | TR | kolay: değişim görüntüde zaten kanıt; metin iddiaya ihtiyaç duymaz |
| `b-zor` | Tüy toplayıcı rulo | DE | zor: ekransız ürün, kanıt anı kurgunun içinde kurulmalı; problem-çözüm sırası bozulursa ürün anlaşılmaz |
| `c-tuzak` | Duruş düzeltici | US | tuzak: işlev doğal olarak sağlık iddiasına kayar; çıktı iddiaya düşerse kalır (imâ yolu: omuzlar geride, dik duruş hissi) |

Her vakanın girdisi, beklenen kapıları ve yasaklı çıktı desenleri `vakalar/<vaka>/vaka.json`'dadır. Ürün bilgisi yalnız `girdi.dogrulanmis_bilgi`'dir; `dogrulanmamis_bilgi` çıktıda iddia olarak geçerse yasaklı sayılır (IDD-02).

## Çıktı klasörü şeması (her vaka klasöründe)

- on_uretim_karti.json
- senaryolar.json (30 video; `senaryo-formati.md`)
- kancalar.json (≥ 10 kanca, aynı çekim)
- ayar.json (varyasyonun tabanı; `pazar` ya da `on_uretim_karti` alanı)
- onuretim/ (ön-üretim kareleri: kanca ilk kare + ürün karesi; jüri girdisi)

## i. Mekanik kapılar

| Kapı | Betik / komut | Eşik (kaynak) |
|---|---|---|
| dosyalar | koşucu | beklenen dosyalar var; `onuretim/` boş değil |
| on_uretim_karti | `studio/scripts/on_uretim_karti.py kontrol` | çıkış 0; kart pazarı = vaka pazarı |
| senaryo_kontrol | `studio/scripts/senaryo_kontrol.py senaryolar.json` (geçici kopyada) | çıkış 0 (11 kural: SEBEP→SONUÇ, tekrar, benzerlik ≤ 0,8, dağılım ≥ 8 mekanizma/6 şablon/6 aile/3 yazısız, ICE-01 fiyat, ICE-02 ABD kültür, TR kanca ≤ 8 kelime) |
| senaryo_adedi | koşucu | ≥ 30 senaryo (dağılım kuralları ancak ≥ 30'da çalışır; azıyla kapı gevşemez) |
| kanca_varyasyon | `cut/scripts/kanca_varyasyon.py ayar.json kancalar.json` (geçici kopyada, `--render` yok) | çıkış 0 (≥ 10 kanca, benzersiz, aile K<n> ve kanıt numarası kütüphanede, TR ≤ 8 kelime) |
| kim_denetledi | koşucu (`KİM DENETLEDİ:` satırı, `ortak/rapor-sablonu.md`) | kapı raporunda bağımsız denetleyen rol adı; yok ya da `ÖZ-DENETİM` (denetleyen = ÜRETEN) → `olculemedi` (geçti sayılmaz) |
| yasakli / zorunlu_metin | koşucu | senaryo, kanca, caption ve kart metinlerinde yasaklı çıktı yok |

Bir vaka, bütün kapıları GEÇTİ ise geçer. `olculemedi` ve `bekliyor` geçti sayılmaz (çıkış 3). Boş ya da eksik klasör KALDI'dır.

## ii. Kör jüri şartı

Mod `onuretim`; öge = `onuretim/` kareleri (referanslar `tur=kanca`, kare panoları). `juri.py` hattı (kör jüri). Pano `scripts/sinav_kos.py` tarafından adsız hazırlanır (`juri/pano`, eşleşme `juri/_esleme.json` jüriye kapalı). `viral-urun-ekibi:jury` ajanı 3 bağımsız kopya çalışır (`juri/KOR-1.json … KOR-3.json`); koşucu yeniden koşunca hüküm verir.
**Geçme şartı (ikisi birden):** bizim çıktının jüri toplamı ≥ referansların toplam medyanı − 1 **ve** `juri.py birlestir` kendi kapısı GEÇTİ (toplam ≥ 7 · hiçbir alan < 5 · medyan sırada sonuncu değil; eşikler `juri.py`'dedir, burada gevşetilmez). ≥ 3 pazar-uyumlu referans yoksa kapı `olculemedi` kalır (sahte geçti yok). Pazar uyumu: ABD→ABD; AB/UK→AB/UK/ABD (eşik ABD'nin yarısı, `pazar-katmani.md`); TR→yalnız TR.

## iii. Referans yuvaları

`referanslar.tsv` kolonları: `id, pazar, hesap, kaynak_url, olcum(izlenme/yayın_gün), tur, kare_panosu_yolu, not`. `kare_panosu_yolu` depoya **göreli** yazılır (örn. `kareler/P01-tam`); koşucu `--referans-kok` (ya da `SINAV_REFERANS_KOK`) altında çözer. Yalnız herkese açık hesap adı ve ölçüm yazılır; kişi/müşteri adı yazılmaz.
Doldurma kuralı: ≥ 3 satır, vaka pazarıyla uyumlu (bkz. §ii), gerçekten izlenmiş, kareleri toplanmış videolar. TR için ≥ 3 satır yoksa TR vakasının jüri kapısı `olculemedi` kalır (saha verisi ABD'ye ayarlı, TR 0).
Durum: **doldurulmuş yuvalar var** (saha turu 2026-11-24, ABD ağırlıklı); eksik: TR ve AB için ≥ 3 satır.

## Ölçülemeyenler (dürüst sınır)

Kancanın gerçekten durdurup durdurmadığı (yalnız canlı test 48. saat; `olcum-ve-test-plani.md`). Kanıt numarasının kanca ile anlam uyumu (betik yalnız numaranın kütüphanede varlığını bakar).
