# Ölçütler ve karar kuralı

Ne zaman okunur: ön eleme, marj ve kanıt dosyası yazılırken. Sayılar `esikler.tsv`'dedir (betik oradan okur); bu tablo özetidir.

**Yalnız SAT (eklenti kuralı).** Kullanıcıya yalnız SAT ürünleri gider; İZLE ve "SAT (koşullu)" sınıfları kalktı. Her satır `SAT-ADAYI` (kanıt dosyası gelince SAT) ya da `ELE`'dir. ELE yalnız **kanıtlanmış olumsuz engeldir**; okunamayan/ölçülemeyen ölçüt engel değildir, SAT kartında "ilk testte kontrol et" notu olur.

| Ölçüt | SAT (geçer) | ELE (kanıtlı engel) | Okunamadı / ölçülemedi | Durum |
|---|---|---|---|---|
| Değerlendirme sayısı (talep) | 150–3.000 | ölçülmüş ve bandın dışında (< 150 düşük talep, > 3.000 doygun) | not: "yorum sayısı okunamadı" | deneme |
| Puan | ≥ 4,2 | ölçülmüş ve < 4,2 | not | deneme |
| Aynı ürünü satan satıcı (doygunluk) | ≤ 5 | ölçülmüş ve > 5 | not | varsayım |
| Meta TR aktif reklam (viral-doygunluk vekili) | ≤ 3 | ölçülmüş ve > 3 | not | varsayım (Hunter kuralı) |
| Hedef satış / tedarikçi alışı (kat) | ≥ 2,2 kat ve satış ≥ 399 TL | ölçülmüş ve < 2,2 kat ya da satış < 399 TL | tedarikçi bulunamadı → not "tedarikçi bulunamadı"; kat dogrulanamadi | eklenti varsayılanı; `.ekip/isletme-profili.tsv` `kat_min` / `satis_tl_min` üstüne yazar |
| Aynı ürün viral mi | `yok` / `aile-var` | `ayni-urun-viral` (≥ 500 bin izlenme kanıtı) | `dogrulanamadi` / boş → not (viral veritabanı yok: vekil Meta reklam sayısı + satıcı sayısı) | varsayım |
| Marj katkısı (`tr_marj.py`) | katkı > 0 | katkı ≤ 0 (`zarar`) ya da marka ROAS başabaşın altı (`karar_marj` ELE) | marka ROAS yok (`karar_marj` dogrulanamadi) → not; hesap durmaz | eklenti kuralı; kapıda ödeme ve marka ROAS profilden gelir |
| Fiyat şeffaflığı puanı | 0–2 | 3 ve aşma yolu yok | — | varsayım |
| Veto | — | lisanslı/marka görünümlü ürün, tehlikeli/yasaklı (bebek güvenliği iddiası), riskli kargo (pil, sıvı, cam) | — | Hunter kuralı |

- Satırın kararı: kanıtlı engelden biri varsa ELE, yoksa SAT-ADAYI. Eski İZLE bantları (yorum 50–149, puan 4,0–4,19, satıcı 6–15, kat 1,8–2,19, Meta 4–10) ölçülmüş olduğu için artık ELE'dir; eşik değerleri değişmedi.
- **Fiyat kaynakları ayrıdır:** Trendyol fiyatı = hedef satış/rakip fiyatı (`onerilen_satis_tl`, `rakip_tl`); ASLA `alis_tl` değil. `alis_tl` tedarikçiden (AliExpress/1688 aynı ürün) gelir ve `alis_kaynak` sütununda kaynak linki taşır; bulunamazsa boş + "tedarikçi bulunamadı" notu. `denetle`, `alis_tl` = `rakip_tl` ya da `alis_kaynak` Trendyol ise HATA verir. Eski `alis_tl` bandı (100–600 TL) kalktı: o band Trendyol perakendesine göre konmuştu; engel `kat`tır.
- Trendyol'da aynı ürün bizim hedef satış fiyatımızın altındaysa ELE değil, SAT kartında fiyat notu olur (`rakip_tl` < `onerilen_satis_tl`). Kanıt ajanı "aynı ürün başka yerde daha ucuz" diye ELE vermez: tedarikçi daha ucuzsa bu marjdır.
- `durum` = `varsayim` ya da `deneme` eşikler 20 ürün kanıt dosyasına ulaşınca gerçek sonuçla yeniden ayarlanır; `denetle` çıktısının son satırı bunu hatırlatır ("N/20 kanıt: eşikler DENEME").
- Net marj `tr_marj.py` ile hesaplanır:
  net_gelir = satış / (1 + KDV) · alış_net = alış / (1 + KDV) (alış KDV dahil ve fatura kurumsalsa; değilse alış aynen) ·
  ödeme = satış × ödeme% + sabit + kapıda oranı × kapıda ek ücret · iade = iade% × iade birim maliyeti ·
  maliyet = alış_net + tedarik kargo + müşteri kargo + ödeme + iade · katkı = net_gelir − maliyet · çarpan = net_gelir / maliyet ·
  başabaş ROAS = satış / katkı (katkı ≤ 0 ise "zarar") · net_kar = katkı − satış × reklam payı.
- `tr-oranlari.tsv` kaynaklı varsayılanlarla gelir (`kaynakli` + tarih + URL; `varsayim` olanlar: iade oranı, iade birim maliyeti, reklam payı; `varsayilan`: kapıda ödeme 0; kapıda ödeme kullanıyorsan `.ekip/isletme-profili.tsv` bunun üstüne yazar). Kaynak sırası: kullanıcı (satır) > işletme profili > kaynakli > varsayim/varsayilan. Hücre ve dosya ikisi de boşsa betik bilerek HATA verir; değeri uydurma.
- ROAS markaya özeldir : sabit eşik yok. Karar, markanın kendi reklam hesabındaki gerçek ROAS'ının (`--marka-roas` ya da `.ekip/isletme-profili.tsv` `marka_roas`) ürünün başabaş ROAS'ına oranıdır. Marka ROAS'ı yoksa `karar_marj` `dogrulanamadi` olur; bu SAT'ı ENGELLEMEZ (kart notu: "marka ROAS yok"); değer uydurulmaz. Karar birleştirme: `trendyol_kontrol.py denetle adaylar.tsv --marj-sonuc marj-sonuc.tsv`.
- `tr-oranlari.tsv`'de değeri olmayan oran için kaynaklı/temkinli varsayılan kullanılır ve "varsayım" etiketlenir; marj hesabı oran yüzünden durmaz.