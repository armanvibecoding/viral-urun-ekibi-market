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

## .ekip/DURUM.md (aliexpress-firsat aşamasındayken örnek)
```
# DURUM
Aktif iş: aliexpress-firsat · pazar ABD
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
Sıradaki beceri: ai-video-kreatif
```
