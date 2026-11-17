---
name: aliexpress-firsat
description: Instagram'da viral olmuş ürünlerin ortak DNA'sını ölçüt yapıp AliExpress'te HENÜZ viral olmamış ürünleri bulur, "zaten viral mi" kontrolünü pazara göre yapar (TR Trendyol, ABD Amazon + TikTok Shop), kanıt dosyası yazar ve SAT / İZLE / ELE diye sıralar. "AliExpress'ten ürün bul", "henüz patlamamış ürün ara", "viral olacak ürün", "fırsat ürünü bul", "winner ürün avı", "yeni ürün adayı çıkar", "bu ürün tutar mı" isteklerinde çağır.
---

# AliExpress fırsat avı

**Amaç:** seçilen pazarda henüz kimsenin büyütmediği ama viral ürün DNA'sına uyan ürünü kanıtla bulmak.
**Bitiş durumu:** `is/firsat/adaylar.md` sıralı ve denetimden geçmiş; kısa listedeki her ürünün
`is/firsat/kanit/` altında kanıt dosyası var; kullanıcıya 5–10 satırlık özet verilmiş; `.ekip/DURUM.md` güncel.

Önce oku: `${CLAUDE_PLUGIN_ROOT}/ortak/viral-dna.md` (ölçüt) ve `${CLAUDE_PLUGIN_ROOT}/ortak/sozluk.md` (terimler).
Terimler (aday, kanıt, tutmamış, tutabilir, SAT/İZLE/ELE) yalnız sözlükteki anlamıyla kullanılır.

## Hafıza protokolü (her aşamada)
| Ne zaman | Ne yapılır |
|---|---|
| Başlarken | `.ekip/DURUM.md` ve `.ekip/KARARLAR.md` okunur. `is/firsat/` yoksa `${CLAUDE_SKILL_DIR}/referans/dosya-sablonlari.md`'ye göre kurulur. |
| Başlarken (ivme) | `is/firsat/ivme.csv` varsa `python3 "${CLAUDE_SKILL_DIR}/scripts/ivme_olc.py" bekleyen is/firsat/ivme.csv` → t7 günü gelen ürünler önce ölçülür. |
| Pazar | KARARLAR.md'de `\| pazar \|` satırı varsa o kullanılır. Yoksa kullanıcıya **bir kez** sorulur (TR / ABD / diğer: hangi ülke) ve `- YYYY-AA-GG \| pazar \| <cevap>` eklenir. |
| Her terim aranmadan önce | `is/firsat/aramalar.md`'de var mı bakılır; aranan terim aynı satıra sonucuyla yazılır. |
| Her ürün önerilmeden önce | Tekrar kontrolü (aşağıdaki komut). "DAHA ONCE GORULDU" çıkan ürün önerilmez. |
| Her aşama sonunda | `.ekip/DURUM.md` üzerine yazılır (aktif iş, aşama, son çıktı, sıradaki adım, bekleyen onay). |
| Kullanıcı karar verince | Hemen `.ekip/KARARLAR.md`'ye eklenir (pazar, onaylanan ürün, yasak, harcama onayı). Yazılmayan karar yok sayılır. |
| Hata tekrarlanınca | `.ekip/DERSLER.md`'ye "- konu: ders (kanıt dosyası)" eklenir. |

Tekrar kontrolü — Python komutu macOS/Linux `python3`, Windows `py -3` (Windows'ta `python3` Microsoft Store'u açar):
`python3 "${CLAUDE_SKILL_DIR}/scripts/firsat_kontrol.py" tekrar is/firsat "<AliExpress linki veya ürün adı>"`

Uzun tablo sohbete yazılmaz, dosyaya yazılır. Sohbete yalnız özet + dosya yolu.

## Akış
1. **Pazar** — yukarıdaki kurala göre. Pazar belli olmadan "zaten viral" kontrolü yapılmaz.
2. **DNA ölçütü** — `viral-dna.md` §3'ten 3–5 mekanizma seç; yüksek paylaşımlı (M14, M11, M7, M8, M6) ve
   yüksek izlenmeli (M3, M2) gruplardan en az birer tane. Kullanıcının kendi keşif notları (`kesfet-urun-avi` çıktısı) varsa
   onlardaki milyonluk ürünler akraba olarak eklenir.
3. **Arama terimleri** — mekanizmadan üretilir, ürün adından değil: `${CLAUDE_SKILL_DIR}/referans/aliexpress-okuma.md` §2.
4. **Aday listesi** — ağır tarama `firsat-avcisi` ajanına verilir. Her aday: ürün sayfası linki, normal fiyat,
   **ürün sayfasındaki** satış, görsele bakıldı mı, mekanizma + akraba not no, DNA. Hedef varsayılan 20–30 aday.
5. **Zaten viral mi** — `${CLAUDE_SKILL_DIR}/referans/zaten-viral-kontrolu.md` (TR: Trendyol; ABD: Amazon + TikTok Shop; ayrıca video ve Meta Reklam Kütüphanesi).
6. **Denetim + sınama** — `firsat_kontrol.py denetle is/firsat/adaylar.md` hatasız dönmeli; sonra `sinama` ile rastgele 3 satır
   ürün sayfasından açılıp kontrol edilir (`${CLAUDE_SKILL_DIR}/referans/kanit-ve-karar.md` §4).
7. **Kanıt dosyası** — sıra puanı en yüksek ≤5 aday `kanit-savcisi` ajanına; `is/firsat/kanit/NN-urun-adi.md`.
   Kısa listeye giren her aday için aynı gün: `is/firsat/marj.csv` satırı (iniş maliyeti: gümrük/tarife, aracı, ödeme,
   iade/COD reddi, teslim günü) ve `is/firsat/ivme.csv` `t0` satırı. `marj_hesap.py` çıkış 0 olmadan marj yazılmaz;
   7 gün sonra `t7` ölçülür, `ivme_olc.py bant` → ERKEN DALGA / BOŞ / DOYMUŞ. Kanıt dosyasına 10 ölçütlü puan (0–20) tablosu
   girer: `${CLAUDE_SKILL_DIR}/referans/marj-ivme-puan.md`.
8. **Karar** — SAT / İZLE / ELE (`kanit-ve-karar.md` §2). ELE olanlar sebebiyle `is/firsat/elenenler.md`'ye.
   SAT olan ürün için `is/NN-urun-adi/DURUM.md` açılır; kullanıcı onaylarsa KARARLAR.md'ye yazılır.

## Ajana iş verirken (brief)
Brief'te beş şey olur: hedef, okunacak dosyalar (DNA, sözlük, adaylar, elenenler, aramalar), yazılacak dosya,
durma ölçütü (aday sayısı veya CAPTCHA) ve "zaten bilinenler/elenenler" listesi. Brief'e kendi tahminini yazma;
veri ver. Aynı anda en fazla 2 ajan. Ajan çıktısı sınamadan geçmeden kullanıcıya "bulundu" denmez.

## Erişim gerçekleri (ölçülmüş)
- AliExpress, Trendyol, Amazon ve Meta Reklam Kütüphanesi düz istekte (curl/WebFetch) CAPTCHA, engel ya da giriş sayfası döndürüyor.
  Bunlar tarayıcıdan (Claude in Chrome) okunur. Tarayıcı yoksa sonuç "doğrulanamadı" yazılır ve kullanıcıya söylenir.
- CAPTCHA çözülmez, atlatılmaz: tarama durur, okunan kadarı kaydedilir.
- AliExpress'te istekler arası ≥15–20 sn; Meta Reklam Kütüphanesi'nde oturumda ≤30 arama.

## Kurallar
- Sayı uydurmak yasak. Okunamayan her alan `doğrulanamadı` yazılır; bu geçerli bir sonuçtur.
- Ürün satışı yalnız ürün sayfasının başlık satırından okunur; mağaza toplamı ("5,000+") ve arama kartı sayısı ürün satışı değildir.
- Marj normal fiyattan hesaplanır; yeni-müşteri/erken-kuş fiyatı ayrıca not edilir.
- Marj **iniş maliyetiyle** (`marj_hesap.py`) hesaplanır; oran bilinmiyorsa satır hesaplanmaz, "doğrulanamadı" yazılır.
  Betik değişirse önce `python3 "${CLAUDE_SKILL_DIR}/scripts/kirma_testi.py"` (16 test) çıkış 0 vermeli.
- Benzer ürün aynı ürün değildir: form + ana parça + mekanizma fotoğrafla eşleşmeden satış/video/yorum aktarılmaz.
- Mekanizma gerçek alıcı fotoğrafı/videosuyla doğrulanmadan SAT verilmez.
- Veto (lisans/marka görünümü, sağlık iddiası, bebek güvenliği iddiası, riskli kargo) olan ürün puanlanmaz.
- Satın alma, sepet, numune siparişi, ücretli araç: kullanıcı onayı olmadan yok; onay KARARLAR.md'ye yazılır. TrendTrack kullanılmaz.
- Instagram/TikTok'ta yalnız izle ve oku; takip, yorum, mesaj yok.
- Her SAT/ELE gerekçesi ürüne özgü tek cümledir.

## Referanslar (gerektiğinde oku)
| Dosya | Ne zaman |
|---|---|
| `${CLAUDE_SKILL_DIR}/referans/aliexpress-okuma.md` | Terim üretme, ürün sayfası okuma, satış/fiyat/görsel tuzakları |
| `${CLAUDE_SKILL_DIR}/referans/zaten-viral-kontrolu.md` | Pazara göre mağaza, video, reklam kontrolü |
| `${CLAUDE_SKILL_DIR}/referans/kanit-ve-karar.md` | Sıra puanı, kanıt dosyası şablonu, SAT/İZLE/ELE, sınama |
| `${CLAUDE_SKILL_DIR}/referans/dosya-sablonlari.md` | `is/firsat/` ve `.ekip/` dosya biçimleri |
| `${CLAUDE_SKILL_DIR}/referans/marj-ivme-puan.md` | İniş maliyeti (marj.csv), 7 günlük ivme (ivme.csv), 10 ölçütlü puan |
| `${CLAUDE_SKILL_DIR}/referans/pazar-oranlari.tsv` | Pazar başına gümrük eşiği/KDV — tarihli, kaynaklı; değişince güncelle |
| `${CLAUDE_PLUGIN_ROOT}/ortak/marka-skoru.md` | Akraba ürün hesabının örnek alınabilir marka olup olmadığı |

## Kullanıcıya özet (her tur sonunda, ≤10 satır)
Pazar · aranan terim sayısı · bakılan ürün sayfası · aday / elenen (sebep dağılımı) · sınama sonucu (3/3 tuttu mu) ·
en iyi 3–5 aday (ürün, fiyat, ürün satışı, sıra puanı, karar) · doğrulanamayanlar · sıradaki adım ve gereken onay.
