# Dosya şablonları (kullanıcının proje klasörü)

Ne zaman okunur: `is/firsat/` ilk kez kurulurken ya da bir dosyanın biçimi belirsizse.
Tüm dosyalar kullanıcının projesinde durur; eklenti klasörüne hiçbir şey yazılmaz.

```
.ekip/DURUM.md          ← ≤40 satır, üzerine yazılır
.ekip/KARARLAR.md       ← yalnız ekleme
.ekip/DERSLER.md        ← yalnız ekleme
is/firsat/aramalar.md   ← aranan terimler (tekrar aranmasın)
is/firsat/adaylar.md    ← aday tablosu (sıralı)
is/firsat/elenenler.md  ← elenenler + sebep (bir daha önerilmez)
is/firsat/kanit/NN-urun-adi.md ← kanıt dosyaları
is/firsat/marj.csv      ← iniş maliyeti satırları (şablon: sablon/marj.csv)
is/firsat/ivme.csv      ← t0/t7 talep sinyalleri (şablon: sablon/ivme.csv)
is/firsat/pazar-oranlari.tsv ← (isteğe bağlı) kendi ödeme/aracı/iade oranların; eklentidekinin üstüne okunur
is/NN-urun-adi/DURUM.md ← SAT olan ürünün kendi klasörü
is/NN-urun-adi/magaza/urun-paketi.json ← onaylanan SAT ürünü; mağaza kolunun girdisi (betik yazar)
```

## is/firsat/aramalar.md
```
| Tarih | Mekanizma | Terim | Bakılan ürün sayfası | Sonuç |
|---|---|---|---|---|
| 2026-01-15 | M3 | sushi shaped pet bed | 3 | 1 aday (#4), 2 benzer-değil |
| 2026-01-15 | M8 | radiator cat bed hanging | 0 | taranmadı (CAPTCHA) |
```

## is/firsat/adaylar.md
Sütun adları betiğin okuyabilmesi için aynen kalır. DNA sütununa yalnız **geçen** ölçütler yazılır (`V1,V2,V4,V6`).
```
# Adaylar — pazar: <TR/ABD/…>

| # | Ürün | Ali link | Ürün satışı (sayfa) | Normal fiyat | Görsel | Mekanizma · akraba | DNA (V1–V7) | A | B | C | D | Zaten viral? | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | <ürün> | https://www.aliexpress.us/item/<no>.html | 57 sold (sayfa) · 5,0/8 | $13.63 (yeni müşteri $3.63) | bakıldı, filigran | M7 · 086, 079 | V1,V2,V3,V4,V7 | 2 | 2 | 2 | 2 | tutmamış — … | AÇIK |
```
Durum değerleri: `AÇIK` (karar yok) · `KISA LİSTE` · `SAT — is/firsat/kanit/NN-…md` · `İZLE — <ne bekleniyor>` · `ELE`.

## is/firsat/elenenler.md
```
| Tarih | Ürün | Ali link | Sebep (ürüne özgü, tek cümle) |
|---|---|---|---|
| 2026-01-15 | <ürün> | https://www.aliexpress.us/item/<no>.html | veto: ünlü terlik markasının görünümü (IP) |
```

## .ekip/KARARLAR.md satırı
`- YYYY-AA-GG | pazar | ABD` · `- YYYY-AA-GG | firsat | <ürün> SAT onaylandı` · `- YYYY-AA-GG | yasak | <kullanıcının yasakladığı şey>`

## .ekip/DURUM.md (hunter aşamasındayken örnek)
```
# DURUM
Aktif iş: hunter · pazar ABD
Aşama: 4/7 zaten-viral kontrolü (12 adaydan 7'si bitti)
Son çıktı: is/firsat/adaylar.md (12 aday, 3 ELE)
Sıradaki adım: kalan 5 adayın Amazon + TikTok Shop kontrolü, sonra sınama
Açık sorular: —
Bekleyen onaylar: numune siparişi (#2) — kullanıcı onayı yok
```

## is/NN-urun-adi/DURUM.md (SAT sonrası)
```
# NN — <ürün> — aşama: fırsat SAT
Kanıt: is/firsat/kanit/NN-urun-adi.md
Ürün paketi: is/NN-urun-adi/magaza/urun-paketi.json (mağaza koluna gider)
Sıradaki beceri: studio (mağaza kurulacaksa önce builder)
```

## is/NN-urun-adi/magaza/urun-paketi.json (SAT onayından sonra; elle yazılmaz, betik yazar ve doğrular)
```
python3 "<eklenti kökü>/ortak/paket.py" urun-yaz --cikti is/NN-urun-adi/magaza/urun-paketi.json \
  --ad "<ürün sayfasındaki ad>" --foto <görsel dosyası ya da URL> --pazar TR \
  --marj-csv is/firsat/marj.csv --kanit-md is/firsat/kanit/NN-urun-adi.md [--teklif-tsv is/NN-urun-adi/teklif/teklif.tsv] \
  --ozellik "ad|değer|birim|kaynak link" --varyant "Gri|var" [--rakip "marka|link|fiyat"] [--kanit "kaynak|link|YYYY-AA-GG|ölçü"]
```
| Seçenek | Nereden okunur |
|---|---|
| `--ad`, `--foto` (≥1), `--pazar` ya da `--ulke` | zorunlu. Ad ve görseller ürün sayfasından; ilk görsel en temiz ürün karesi. Pazar KARARLAR.md pazar satırından (TR, US, ABD, DE …; `--pazar` dil ve parayı kendisi doldurur, `--ulke` ile `--dil`/`--para` elle verilir) |
| `--tedarik` ya da `--marj-csv` | `--tedarik "13.63 USD"`: `adaylar.md` normal fiyatı (yeni müşteri fiyatı değil); `--marj-csv`: `marj.csv`'de ürün adıyla eşleşen son satırın `urun_maliyeti` |
| `--kanit-md` | kanıt dosyasının URL + ölçü içeren her satırı `kanit[]` olur (satırda tarih yoksa dosyadaki ilk tarih); ölçüsüz URL alınmaz |
| `--teklif-tsv` | `teklif-ve-sayfa` çalıştıysa: `bizim` satırı = fiyatın TEK kaynağı, `rakip` satırları `rakipler[]`; dosya sürüm 2 olur. `bizim` satırı yoksa sabit kural (2'li %10, 3'lü %18) |
| `--ozellik` (tekrarlanır) | ürün sayfasında OKUNAN değer; 4. parça kaynak linki. Kaynaksız özellik "doğrulanmış" sayılmaz |
| `--varyant` (tekrarlanır) | ürün sayfasındaki seçenekler; stok `var` / `yok` |
| `--rakip` (tekrarlanır) | zaten-viral kontrolünde bulunan mağaza / pazar yeri satırları |
| `--kanit` (tekrarlanır) | kanıt dosyasındaki ölçümler: kaynak, link, ölçüm günü, ölçü (ör. `ürün sayfası 57 satış`, `Meta: 0 aktif reklam`, `ivme: ERKEN DALGA`) |
| `--nis` ya da `--nis-kodu` | `--nis nis-ev` doğrudan; `--nis-kodu mutfak` ekibin niş kodunu `ortak/nis-esleme.tsv` ile çevirir (tabloda yoksa nis-gadget + UYARI). Bilinmiyorsa verilmez; mağaza kolu seçer |

Okunamayan alanın seçeneği hiç yazılmaz (uydurma yok). Çıkış 1 ise dosya yazılmamıştır: hata satırını düzelt, yeniden koştur.
Alanların tam tanımı: `<eklenti kökü>/ortak/sozlesme/arayuz-sozlesmesi.md`.
