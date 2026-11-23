# Ölçütler ve karar kuralı

Ne zaman okunur: ön eleme, marj ve kanıt dosyası yazılırken. Sayılar `esikler.tsv`'dedir (betik oradan okur); bu tablo özetidir.

| Ölçüt | SAT adayı | İZLE | ELE | Durum |
|---|---|---|---|---|
| Değerlendirme sayısı (talep) | 150–3.000 | 50–149 | < 50 ya da > 3.000 (doygun) | deneme |
| Puan | ≥ 4,2 | 4,0–4,1 | < 4,0 | deneme |
| Aynı ürünü satan satıcı | ≤ 5 | 6–15 | > 15 | varsayım |
| Alış fiyatı | 100–600 TL | 601–900 TL | < 100 ya da > 900 TL | deneme |
| Hedef satış / alış | ≥ 2,2 kat ve satış ≥ 399 TL | 1,8–2,19 kat | < 1,8 kat | kurucu kararı |
| Viral durumu | `yok` ya da `aile-var` (model farklı) | `dogrulanamadi` | `ayni-urun-viral` (≥ 500 bin izlenme) | varsayım |
| Meta TR aktif reklam | ≤ 3 | 4–10 | > 10 | varsayım (Hunter kuralı) |
| Başabaş ROAS | ≤ 2,0 | 2,01–3,0 | > 3,0 | varsayım |
| Fiyat şeffaflığı puanı | 0–1 | 2 | 3 ve aşma yolu yok | varsayım |
| Veto | — | — | lisanslı/marka görünümlü ürün, bebek güvenliği iddiası, riskli kargo (pil, sıvı, cam) | Hunter kuralı |

- Satırın kararı = en kötü ölçütün kararı. Bir ölçüt okunamadıysa o ölçüt `dogrulanamadi` yazılır ve satır en fazla İZLE olur.
- `durum` = `varsayim` ya da `deneme` eşikler 20 ürün kanıt dosyasına ulaşınca gerçek sonuçla yeniden ayarlanır; `denetle` çıktısının son satırı bunu hatırlatır ("N/20 kanıt: eşikler DENEME").
- Net marj `tr_marj.py` ile hesaplanır:
  net_gelir = satış / (1 + KDV) · alış_net = alış / (1 + KDV) (alış KDV dahil ve fatura kurumsalsa; değilse alış aynen) ·
  ödeme = satış × ödeme% + sabit + kapıda oranı × kapıda ek ücret · iade = iade% × iade birim maliyeti ·
  maliyet = alış_net + tedarik kargo + müşteri kargo + ödeme + iade · katkı = net_gelir − maliyet · çarpan = net_gelir / maliyet ·
  başabaş ROAS = satış / katkı (katkı ≤ 0 ise "zarar") · net_kar = katkı − satış × reklam payı.
- `tr-oranlari.tsv` her satırı `durum=dogrulanmadi` ve boş değerle açılır; değeri uydurma. Boşken betik bilerek HATA verir.
