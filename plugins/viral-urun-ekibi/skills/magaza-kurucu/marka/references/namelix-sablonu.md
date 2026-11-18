# Namelix çıktı şablonu

Kaynak: `research/isim/RAPOR.md` (d) bölümü. 0.3.3: asıl yol `namelix-ajan.md` (Namelix'i model kullanır); bu şablon yalnız kullanıcı elle yapmak isterse kullanılır.

---

Plugin doldurur: `{NİŞ}`, `{K1..K4}`, `{AÇIKLAMA}`, `{STİL1}`, `{STİL2}`, `{UZUNLUK}`, `{BLACKLIST}`, `{SINIFLAR}`.

GÖSTERİM KURALI (2026-11-17, ilk gerçek koşudan): Aşağıdaki şablon modelin İÇ çalışma tarifidir; kullanıcıya KOD BLOĞU olarak verilmez (ChatGPT'de uzun satırlı, yana kaydırmalı "Düz metin" kutusu oluyor, okunmuyor).
- Çalışma modunda tarayıcı varsa: Namelix'i KENDİN kullan (adım adım tarif `namelix-ajan.md`), kullanıcıya yalnız sonucu ver: 5 adlık tablo (ad · neden · .com durumu · risk) + önerdiğin 1 ad + sonraki kontrol adımları (numaralı liste).
- Tarayıcı yoksa ya da Namelix açılmazsa: kullanıcıya numaralı kısa adımlar ver (her adım tek satır); kopyalanacak tek şey olan anahtar kelimeleri ve açıklamayı satır içi kod olarak yaz (`…`). Uzun kod bloğu yok.

```
MARKA ADI — Namelix adımları
Site: https://namelix.com → "Generate" ile başla

1) Name Style: {STİL1}
2) Randomness: Medium
3) Brand Info
   Brand keywords (kopyala):
   {K1} {K2} {K3} {K4}
   Business description (kopyala):
   {AÇIKLAMA}
4) ⚙ Optional settings
   Blacklist words (kopyala):
   {BLACKLIST}, th, ph, w, q, x, ee, oo
   Maximum length: {UZUNLUK} harf
   Check domains: yalnız .com işaretli
→ Generate

TUR 2: Beğendiğin 5–8 ada kalp at, sonra ayarları {STİL2} + High yapıp tekrar üret.

ADAYLARDAN 3 TANESİNİ SEÇ (puanla, en yüksek 3 kalsın)
Her aday için 0/1:
[ ] .com rozeti var ve "domain for sale" yazmıyor
[ ] 9 harf ya da daha kısa, 2–3 hece
[ ] Türkçe okunuşu İngilizce okunuşuyla aynı
[ ] Ürünü çağrıştırıyor ama ürünün adı değil (ör. "SleepTape" olmaz)
[ ] Birine sesli söyledim, doğru yazdı
→ 5/5 olan ilk 3 adı bana yaz. 5/5 yoksa 4/5 olanları yaz.

3 AD İÇİN KONTROL (sırayla, ilk elenen adda dur)
1. Olumsuz anlam: https://sozluk.gov.tr ve Google'da "<ad> anlamı" / "<ad> argo"
2. TÜRKPATENT: https://www.turkpatent.gov.tr/arastirma-yap?form=trademark
   Marka Adı = <ad>, "içinde geçen", Nice sınıfları: {SINIFLAR}
   Aynı ya da çok benzer ad varsa → ELE
3. AB: https://www.tmdn.org/tmview/ (aynı ad, aynı sınıflar)
4. .com.tr: https://www.trabis.gov.tr (boşsa hemen al)
5. Instagram: https://www.instagram.com/<ad>/ · TikTok: https://www.tiktok.com/@<ad>
   Doluysa: <ad>.tr / <ad>official (iki platformda aynısı)

Geçen adı ve 3 kontrolün sonucunu bana yaz. Mağaza adı, logo metni ve
alan adı önerisini buna göre hazırlayacağım.
```

Anahtar kelime kuralı: blacklist'teki harfleri (w, q, x) ve dizileri (th, ph, ee, oo) içeren kelime anahtar kelime olmaz; Namelix'te anahtar kelime blacklist'i ezer (ölçüm 2026-11-16).

Örnek doldurma (ağız bandı): `{STİL1}=Brandable names`, `{STİL2}=Auto`, `{K}=calm rest nasal somn`, `{UZUNLUK}=9`, `{BLACKLIST}=tape, snore`, `{SINIFLAR}=5, 10, 35`.
