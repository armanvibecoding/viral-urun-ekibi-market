# Müzik kütüphanesi (ölçülen ses etiketleri)

> **Dürüst durum: müzik verisi AZ ve ölçülmedi.** Eski saha setinde 116 analizde `muzik_turu = bilinmiyor`. Aşağıdaki tek ölçüm S24 Keşfet turundan (n=7 etiket; 28 videonun çoğunda ses etiketi okunamadı). Kural = **rampa + açılışta diegetik ses** (SES-01, `ortak/kurallar.md`) + aşağıdaki sezon/trend tarifi. Bu tablo "işe yarar" kanıtı değil, "izleyicinin o dönemde duyduğu" kaydıdır.

## S24 ses etiketleri (Aralık, ABD'ye ayarlı hesap)
| Tür | Kanıt | Not |
|---|---|---|
| Noel klasiği (remaster) — 5 kanıt, **KURAL düzeyi sayı ama n küçük** | Wham! — Last Christmas (Remastered) 25,2MN [S24-G1x04] · Last Christmas (ghost/ses uyarlaması) 8,6MN [S24-G1x05] · Let It Snow! (Remastered) 4,7MN [S24-G1x03] · Jingle Bell Rap 14,6MN [S24-G2x01] · Kris Kringle II: Rudolph-O-Tron 3000 16,5MN [S24-G1x02] | Aralık'ta "tanınan Noel şarkısı / remaster" baskın |
| Slowed-down pop — 1 | Sean Paul — Give It Up to Me (Slowed Down) 3,4MN [S24-G2x03] | GÖZLEM |
| Trend beat — 1 | KURAWA MUSIC — take down 36,7MN [S24-G2x06] | GÖZLEM |
| Retro pop trend ses — 1 | Zou Bisou Bisou (Océan) 51,4MN [S24-G3x07] | GÖZLEM |
| Diğer etiketler | Dominic Fike — Babydoll [S24-G1x07] · BOMBATHERS — The Winner [S24-G1x08] | tek kanıt |

## Kullanım hakkı (önemli)
Bu şarkılar ticari kayıttır. **Instagram'ın ses kütüphanesinden yayın sırasında seçilir; ses dosyaya GÖMÜLMEZ** (SES-02: telifli şarkı indirilmez). Gömülü müzik gerekiyorsa açık lisanslı parça ya da kullanıcının dosyası kullanılır; Noel klasiği tarzı bir his gerekiyorsa lisanslı/telifsiz benzeri aranır, sanatçı adı brif'te yalnız "his referansı"dır.

## Karar tarifi
1. **Organik / after-dark / hikâye (tarif 02):** açık lisanslı parça + SES-01 rampası (ilk karede diegetik ses, müzik düşük seviyeden 1,5–2 sn rampa); drop videonun kesim noktasına oturur (`hikaye/muzik_analiz.py`).
2. **Sezon (Aralık):** Instagram ses kütüphanesinden Noel klasiği remasteri seçilebilir (yayın aşamasında); dosyadaki müzik yine rampa kuralına uyar.
3. **Sezon dışı:** trend/slowed ses etiketi aranır; ölçülmediği için önce 3 varyasyonla test (tarif 10), kazanan ses tabloya yazılır.
4. Her yayın için kullanılan ses etiketi `olcum-ve-test-plani.md` kayıt tablosuna yazılır — müzik verisi böyle birikir.
