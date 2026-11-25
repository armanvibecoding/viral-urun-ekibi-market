# OLCUT · 07-site · Mağaza sitesi (ana sayfa + ürün sayfası)

Ölçüt dosyası: bu özelliğin sürümler arası **değişmeyen** sınavı. Vakalar (`vakalar/*/vaka.json`) sabittir; kapı eşiği bu dosyada değil çağrılan betiklerdedir ve **gevşetilmez** (eşik değişimi ancak ilgili betiğin kalibrasyonuyla, ayrı iş olarak). Koşucu: `python3 scripts/sinav_kos.py 07-site <çıktı-klasörü>` (depo kökünden).

Tarif/sahip: `skills/builder` (metinler, shopify-kurulum), `ortak/roller/probe`, `ortak/roller/shopper`

## Vakalar (sabit, jenerik ürünler)

| Vaka | Ürün | Pazar | Neden bu vaka |
|---|---|---|---|
| `a-kolay` | Isıyla renk değiştiren kupa | US | kolay: değişim görüntüde zaten kanıt; metin iddiaya ihtiyaç duymaz |
| `b-zor` | Tüy toplayıcı rulo | TR | zor: ekransız ürün, kanıt anı kurgunun içinde kurulmalı; problem-çözüm sırası bozulursa ürün anlaşılmaz |
| `c-tuzak` | Duruş düzeltici | DE | tuzak: işlev doğal olarak sağlık iddiasına kayar; çıktı iddiaya düşerse kalır (imâ yolu: omuzlar geride, dik duruş hissi) |

Her vakanın girdisi, beklenen kapıları ve yasaklı çıktı desenleri `vakalar/<vaka>/vaka.json`'dadır. Ürün bilgisi yalnız `girdi.dogrulanmis_bilgi`'dir; `dogrulanmamis_bilgi` çıktıda iddia olarak geçerse yasaklı sayılır (IDD-02).

## Çıktı klasörü şeması (her vaka klasöründe)

- magaza-paketi.json (şema: `ortak/sozlesme/`; onaylı iddia listesi)
- site/ana-sayfa.md · site/urun-sayfasi.md (sayfa metinleri)
- ekran/ (ilk ekran görüntüleri: 1440 ve 390 px; jüri girdisi)

## i. Mekanik kapılar

| Kapı | Betik / komut | Eşik (kaynak) |
|---|---|---|
| dosyalar | koşucu | beklenen dosyalar var |
| iddia_kontrol | `ortak/paket.py iddia-kontrol magaza-paketi.json site/*.md` | çıkış 0 (listede olmayan sayı/belge/otorite yok) |
| kim_denetledi | koşucu (`KİM DENETLEDİ:` satırı, `ortak/rapor-sablonu.md`) | kapı raporunda bağımsız denetleyen rol adı; yok ya da `ÖZ-DENETİM` (denetleyen = ÜRETEN) → `olculemedi` (geçti sayılmaz) |
| yasakli / zorunlu_metin | koşucu | genel + vaka yasakları |
| paket_sozlesme | `ortak/paket.py dogrula magaza magaza-paketi.json` | çıkış 0; fiyat 0 / yer tutucu / kaynaksız marka adı = KALDI; dürüst `null` + `eksik[]` = `olculemedi` |
| kanit_ani_sizinti | koşucu | vaka `kanit_ani` çekim talimatı site metnine cümle ya da iç etiket olarak girmemiş |
| mobil_ekran | `ortak/mobil_ekran.py kontrol ekran/<ad>.html ekran/<ad>-390.png` | çıkış 0 (390 px iframe düzeniyle aynı, taşma yok); çift yoksa ya da Chrome yoksa `olculemedi` |
| hiz_cwv · erisim_wcag | `ortak/web_olcum.py hiz\|erisim <ekran/*.html ya da site/*.html ya da canli-url.txt>` | yerel Lighthouse + axe; eşikler `web_olcum.py`'dedir, burada gevşetilmez. `yerel` etiketi laboratuvardır, canlı mağaza sayısı değildir; araç/Chrome yoksa `olculemedi` |
| arama_merchant · donusum_kullanilabilirlik | (betik yok) | `olculemedi`: probe `arama` canlı sayfa, shopper `donusum` ajan yargısı ister |

Bir vaka, bütün kapıları GEÇTİ ise geçer. `olculemedi` ve `bekliyor` geçti sayılmaz (çıkış 3). Boş ya da eksik klasör KALDI'dır.

## ii. Kör jüri şartı

Mod `teslim`; öge = `ekran/` görselleri (referanslar `tur=site`). `juri.py` hattı (kör jüri). Pano `scripts/sinav_kos.py` tarafından adsız hazırlanır (`juri/pano`, eşleşme `juri/_esleme.json` jüriye kapalı). `viral-urun-ekibi:jury` ajanı 3 bağımsız kopya çalışır (`juri/KOR-1.json … KOR-3.json`); koşucu yeniden koşunca hüküm verir.
**Geçme şartı (ikisi birden):** bizim çıktının jüri toplamı ≥ referansların toplam medyanı − 1 **ve** `juri.py birlestir` kendi kapısı GEÇTİ (toplam ≥ 7 · hiçbir alan < 5 · medyan sırada sonuncu değil; eşikler `juri.py`'dedir, burada gevşetilmez). ≥ 3 pazar-uyumlu referans yoksa kapı `olculemedi` kalır (sahte geçti yok). Pazar uyumu: ABD→ABD; AB/UK→AB/UK/ABD (eşik ABD'nin yarısı, `pazar-katmani.md`); TR→yalnız TR.

## iii. Referans yuvaları

`referanslar.tsv` kolonları: `id, pazar, hesap, kaynak_url, olcum(izlenme/yayın_gün), tur, kare_panosu_yolu, not`. `kare_panosu_yolu` depoya **göreli** yazılır (örn. `kareler/P01-tam`); koşucu `--referans-kok` (ya da `SINAV_REFERANS_KOK`) altında çözer. Yalnız herkese açık hesap adı ve ölçüm yazılır; kişi/müşteri adı yazılmaz.
Doldurma kuralı: ≥ 3 satır, vaka pazarıyla uyumlu (bkz. §ii), gerçekten izlenmiş, kareleri toplanmış videolar. TR için ≥ 3 satır yoksa TR vakasının jüri kapısı `olculemedi` kalır (saha verisi ABD'ye ayarlı, TR 0).
Durum: **boş başlık** — lider dolduracak.

## Ölçülemeyenler (dürüst sınır)

Arama/Merchant hazırlığı ve dönüşüm/kullanılabilirlik denetimi: iki kapı `olculemedi` olduğu sürece 07 çıkışı 0 olamaz; sahte geçti verilmez. Hız ve erişilebilirlik yerel Lighthouse+axe ile ölçülür ama bu laboratuvar ölçümüdür, canlı mağaza ve alan verisi (CrUX) yerine geçmez.
