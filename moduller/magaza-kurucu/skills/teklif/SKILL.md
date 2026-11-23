---
name: teklif
description: Mağaza Kurucu Aşama 1, 3. adım (ürün araştırmasından sonra, marka adımından önce). SAT kararı almış ürün için rakip tekliflerini toplar (fiyat, paket, garanti, kargo, ödeme), pazara göre (TR, ABD, UK, DE, FR, ES) kendi teklifini tasarlar, itiraz SSS ile e-posta ve upsell taslağı yazar; uydurma iddia, yorum ve stok sayısını betikle tarar. "Teklif kur", "fiyat ve paket ne olsun", "itiraz SSS", "upsell", "rakip teklifleri topla" isteklerinde çağır.
---

# Teklif (Aşama 1, Adım 3)

> **Karakter hatırlatma.** Kod adı: Atlas (marka ve stil stratejisti). 1. satır eylem · 2. satır `AŞAMA 1/3 · ADIM 3/9 · Atlas · senden ~1 dk · ✓1–2 ▶3 ○4–9` · ≤5 madde · kod bloğu yok · son satır `Sonraki:`. Her karar: karar → gerekçe → satışa etkisi. Varsayılanı sen seç.

**Amaç:** videonun getirdiği ziyaretçiyi satın almaya çevirecek, o pazarda yasal ve yalnız gerçek kanıta dayanan teklif.
**Bitiş:** `is/NN-urun/teklif/teklif.tsv` (rakip satırları + 1 `bizim` satırı) şema ve yasak-ifade kontrolünden çıkış 0 ile geçti; SSS ve e-posta taslağı yazıldı; DEVAM KARTI'nın Teklif satırı dolu.

## Akış (Mağaza Kurucu, 3 aşama)
1 `urun-analiz` → 2 `teklif` → 3 `marka` → 4 `metinler` → 5 `gorseller` → 6 `shopify-kurulum`. Bu bölüm: **2** (adım 3/9).
- İlk mesajda `references/00-calisma-tarzi.md` ve `references/01-kurallar.md` BAŞTAN SONA okunur.
- Ön koşul kartta aranır: araştırma bulguları (ürün, pazar, 3 rakip). Yoksa `urun-analiz`e dön. Pazar kartta yoksa bir kez sor.
- **Atlanır:** `urun-paketi.json` içinde `teklif.kaynak` = `teklif.tsv` ise teklif onaylıdır; kartın Teklif satırı pakettekiyle doldurulur.
- Eklentiyle gelen dosyalar varsa oku: `ortak/sozluk.md`, `ortak/kurallar.md`, pazar katmanı. Yoksa devam et.

## Modlar
- **Tam mod** (tarayıcı var, Claude Code): aşağıdaki 1–6.
- **Hafif mod** (tarayıcı yok ya da ChatGPT): araştırmadaki 3 rakip + sabit kural (2'li %10, 3'lü %18); `bizim` satırı yine yazılır; karta "teklif: hafif mod" notu.

## Adımlar (çıktılar `is/NN-urun/teklif/`)
1. **Rakip teklifleri topla**: ≥10 satır (aynı pazardan ≥5), şema `references/teklif-semasi.md`. Görülmeyen alan `gorulmedi`. Sahte aciliyet ya da yorum gözlem olarak yazılır, kopyalanmaz. Aynı URL ikinci kez okunmaz.
2. **Desen**: sütun başına sayım. n≥3 olmayan desen "tek örnek" yazılır. → `teklif-deseni.md`.
3. **Teklif**: desen + `references/pazar-teklif-kurallari.md` + iniş maliyeti (paket indirimi sonrası çarpan ≥2×). Sonuç `tur=bizim` satırı: fiyatın TEK kaynağı, `urun-paketi.json` `teklif` alanına birebir girer.
4. `python3 scripts/teklif_kontrol.py sema is/NN-urun/teklif/teklif.tsv` → çıkış 0 olmadan ilerleme.
5. **İtiraz SSS** (`references/itiraz-bankasi.md`) ve **e-posta/upsell** (`assets/eposta-upsell.md`). Cevap ürünün gerçek özelliğinden; bilinmeyen soru sayfaya alınmaz. Temasız modda ürün sayfası düzeni `assets/sayfa-iskeleti.md` → `sayfa.md`.
6. `python3 scripts/teklif_kontrol.py tara --pazar <TR|US|UK|DE|FR|ES> <SSS> <e-posta> [sayfa.md]` → çıkış 0; sonra `references/kontrol-listesi.md`.
7. Sor: "Araştırma ve teklif onaylı mı? (revize için numara yaz)". Onayda DEVAM KARTI ver; sıradaki `marka`.

## Kurallar
Pazarlıksız kurallar `references/teklif-kurallari.md` (uydurma yasak, sahte aciliyet yok, çizili fiyat, AI görsel, rakip metni kopyalanmaz). Yasak desenler `references/yasak-ifadeler.tsv`; yeni desen oraya.
Sayfa yayını, fiyat değişikliği, uygulama kurulumu, reklam, satın alma: kurucu kararı; bu bölüm yalnız taslak üretir.

## Dosyalar
| Dosya | Ne zaman |
|---|---|
| `references/00-calisma-tarzi.md`, `references/01-kurallar.md` | ilk mesajda bir kez |
| `references/ekip-koprusu.md` | fiyatın tek kaynağı (§2), tema modu, `urun-paketi.json` alanları |
| `references/teklif-semasi.md` | teklif.tsv sütunları ve izinli değerler |
| `references/pazar-teklif-kurallari.md` | pazara göre teklif ve mevzuat |
| `references/itiraz-bankasi.md` | pazar başına itiraz → cevap yönü |
| `references/kontrol-listesi.md` | son kontrol |
| `scripts/teklif_kontrol.py`, `scripts/kirma_testi.py` | doğrulama, betiğin kendi testi |

## Kullanıcıya özet (≤8 satır)
Pazar · okunan rakip (n) · en güçlü 3 desen (n/N) · önerilen teklif (fiyat, paket, garanti, kargo, ödeme) · çarpan · kontrol çıkış kodu · bulunamayan veri · onaylanacak tek şey.
