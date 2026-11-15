# Satış videosu iskeleti (nöropazarlama) — 13–15 sn, 140 BPM

> **GÖZLEM (tek ürün):** ekranlı araç ürünü serisinden; milyon kayıt kanıtı yok. Çok sahneli kurguda seçeneklerden biridir,
> zorunlu değil. Seride ≥ 3 video tek sahne (S1, kesmesiz) ya da yazısız (K13) olabilir; bunlar iskeleti taşımaz.

Kullanıldığında altı vuruş bu sırayla gelir. Saniyeler 140 BPM ızgarasındadır (1 vuruş 0,4286 sn).

| Saniye | Beyin | Görüntü | Ses |
|---|---|---|---|
| 0–0,9 | Örüntü kırma | hareket + ürünün en güçlü anı; kanca yazısı ilk karede tam | videonun en yüksek anı |
| 0,9–3,4 | Merak boşluğu | normal/eski hal (beklenti) + elde ürün (gerçeklik kanıtı) | müzik yükselir |
| 3,4 | Ödül | değişim, beyaz flaş | müzik drop'u tam kesimde |
| 3,4–7,7 | Kişiselleştirme | 3 farklı sonuç, 0,86'şar sn | vuruşta kesim |
| 7,7–9,4 | Kontrol / kolaylık | önceki hal → dokunuş → sonuç (neden-sonuç tek akışta) | `--sfx tik@<dokunuş>,vurus@<sonuç>` |
| 9,4–son | Kimlik + düşük sürtünmeli eylem | geniş plan (sahiplik/statü) + "Rate it 1-10" / "Comment KELİME" | müzik kesilmez; döngü için `--son_fade 0.12` |

Kurallar:
- Son kare ilk kareye bağlanır (döngü, tekrar izlenme).
- Merak sorusu ("Is this legal?") videoda cevaplanmaz; yorumu tetikler, cevap DM'de ürün sayfasına göre verilir.
- Uydurulmaz: fiyat, indirim, stok, yorum, tepki, kurulum süresi, yasallık. Polis/sigorta/"gizle" ima eden kanca yok.
- Dokunuş anını gözle değil ölçerek bul (ör. seçilen karonun renk pikseli sayısı kare kare).
- Seri: sahneye klip üretilir (`ai-video-kreatif` SKILL "Seri üretim"); her videoda özne, ortam, giriş, kanca ve müzik farklı.
