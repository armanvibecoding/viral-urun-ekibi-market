# {URUN_ADI} — e-posta ve upsell taslağı ({PAZAR})

> Taslak; gönderim/otomasyon kurulumu kurucu kararı. Pazarlama e-postası yalnız izin veren alıcıya (TR: İYS kaydı; AB/UK: açık rıza).
> Sahte aciliyet, uydurma sayı yok. `teklif_kontrol.py tara` bu dosyada da çalışır.

## Upsell (sepet / ödeme / teşekkür sayfası)
| Yer | Teklif | Koşul |
|---|---|---|
| Ürün sayfası | 2'li/3'lü paket (teklif.tsv `paket`) | paket fiyatında iniş çarpanı ≥2× |
| Sepet | tamamlayıcı ürün `{EK_URUN}` — ana ürünle gerçekten birlikte kullanılan | aynı tedarikçi/kargo |
| Teşekkür sayfası | tek tıkla ek ürün, açık fiyat | ödeme bilgisi yeniden istenmez, iptal kolay |

## E-posta 1 — sipariş onayı (işlemsel)
- Konu: Siparişin alındı — {SIPARIS_NO}
- Gövde: ne alındı, toplam (ek ücret yok), tahmini teslim `{TESLIM_GUN}` gün, takip ne zaman gelir, iade koşulu bağlantısı, iletişim

## E-posta 2 — kargoya verildi (işlemsel)
- Konu: Kargoya verildi — takip numaran
- Gövde: takip bağlantısı, gerçek tahmini tarih, kullanım ipucu (mekanizmayı en iyi nasıl kullanırsın)

## E-posta 3 — teslimden 3–5 gün sonra (yorum isteği)
- Konu: {URUN_ADI} nasıl gitti?
- Gövde: memnun değilsen iade/destek yolu önce; sonra yorum isteği. Yorum karşılığında indirim verilecekse **olumlu yorum şartı yok**
  ve yorumda teşvik açıkça belirtilir (FTC / DMCC / Omnibus)

## E-posta 4 — terk edilen sepet (izinli alıcıya)
- Konu: Sepetinde {URUN_ADI} kaldı
- Gövde: ürün + fiyat (aynı), garanti, SSS'den 1 itiraz cevabı. Sahte "stok bitiyor" yok
