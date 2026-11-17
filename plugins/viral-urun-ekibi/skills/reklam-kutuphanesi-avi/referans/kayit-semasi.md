# Kayıt şeması ve kazanan sinyalleri

Hepsi kullanıcı projesinde `is/meta/` altında, sekme ayrılmış (TSV), ilk satır başlık. Başlık betikle aynı olmalı
(`kayit_denetle.py` denetler). Okunamayan alan **`görünmüyor`** yazılır — `0` değil. Satırları betikler yazar; elle yazılan
tek dosya `teklif.tsv`'dir (ve `reklamlar.tsv`'de yalnız `izlendi` / `not_no` sütunları).

| Dosya | Yazan | Sütunlar |
|---|---|---|
| `aramalar.tsv` | `nis_kelime.py kaydet/sonuc`, `meta_kayit.py` | tarih · saat · ulke · nis · aile(U/S/K/KONTROL/ALAN) · sorgu · siralama · kart · durum(ACIK/TAMAM/GERCEK-SIFIR/SINIRLAMA) · ham_dosya |
| `ham/<tarih>-<ülke>-<sorgu>-<parça>.txt` | lider (meta_aktar.js çıktısı) | `#REKLAMAVI v1` başlığı + kart satırları (kod · sayfa · tarih_metni · kopya_metni · kart_tam · link · cta · medya · govde) |
| `reklamlar.tsv` | `meta_kayit.py` | kutuphane_kodu · okuma_tarihi · ulke · nis · sorgu · aile · siralama · sayfa_adi · ilk_yayin · aktif_gun · kopya · govde_ilk200 · cta · hedef_alan · hedef_yol · tip · medya · izlendi(E/H) · not_no · etiket |
| `sayfalar.tsv` | `meta_kayit.py` | ulke · birim · sayfa_adi · tip · nis · reklam_sayisi · kopya_toplami · ilk_baslangic · son_baslangic · max_aktif_gun · kazanan_kreatif · alan_sorgu · son_okuma · urun_yollari · etiket |
| `sayfa_gecmis.tsv` | `meta_kayit.py` | tarih · ulke · birim · reklam_sayisi · kopya_toplami (ivme için gün gün) |
| `alan_olcek.tsv` | `meta_kayit.py alan` | tarih · ulke · alan · sonuc ("~N sonuç") |
| `magazalar.tsv` | `magaza_gecis.py aktar` | alan · okuma_tarihi · durum(OK/KAPALI/HATA-x) · urun_sayisi · ilk_urun · son_urun · medyan_fiyat · ana_urun · ana_urun_eklenme · ana_fiyat · ana_cizili · ana_handle |
| `teklif.tsv` | lider (elle, OLCEKLENIYOR mağazanın ürün sayfasından) | alan · okuma_tarihi · fiyat · cizili · paket(1/2/3) · kargo_esigi · garanti · yorum_app · yorum_sayisi · sss(E/H) · odeme(COD/kart) · ilk_ekran |
| `aliexpress-esleme.md` | `magaza_gecis.py esleme` | kaynak META-<kod> · mağaza · ana ürün · fiyat · ürün sayfası · İngilizce tanım · AliExpress linki · durum |
| `nis-raporu-<tarih>.md` | `haftalik_rapor.py` | pazar × niş özeti |

**Birim** = mağaza = reklamın hedef alan adı (linksizse `sayfa:<sayfa adı>`). Birim sayımı aynı haftanın (7 gün) okumalarını
birlikte sayar. **Kopya** = kartın "N reklam bu kreatifi ve metni kullanıyor" sayısı; kartta bu satır yoksa 1; kart yapısı
okunamadıysa `görünmüyor` (birim toplamına girmez — toplam alt sınırdır). **Tip:** SHOPIFY (`/products/` ya da myshopify) ·
ALTALAN-LANDING (ürün başına alt alan adlı tek sayfa) · PAZARYERI (Trendyol, Amazon, Etsy…) · DİĞER (sosyal, kendi sitesi) · LİNKSİZ.

## Kazanan sinyalleri (hepsi vekil; eşikler DENEME — ilk 4 haftadan sonra kendi verimizle kalibre)
| Sinyal | Okuma | Eşik |
|---|---|---|
| Aktif gün | okuma tarihi − ilk yayın | ≥30 gün |
| Kopya | "N reklam bu kreatifi" | ≥3 |
| Birim başına aktif reklam | `sayfalar.tsv` ya da alan sorgusu | ≥10 |
| Mağaza yaşı | `/products.json` en eski `created_at` | ≤180 gün ve ≤30 ürün |
| İvme | `sayfa_gecmis.tsv` gün 0 → gün 7 | artış |

Etiketler (`kazanan_puan.py` verir, elle yazılmaz; `--denetle` elle değişikliği yakalar):
- Reklam: `OLCEKLENIYOR` (≥30 gün + ≥3 kopya, ≤180 gün) · `ESKI-KAZANAN` (aynı, >180 gün) · `TEST` · `BILINMIYOR` (gün/kopya görünmüyor).
- Birim: sinyal = ≥10 aktif reklam **ya da** ≥1 kazanan kreatif. Sinyal + genç/yaşı okunmamış → `OLCEKLENIYOR`;
  sinyal + (mağaza >180 gün ya da >30 ürün ya da ilk reklam >180 gün) → `ESKI-KAZANAN`; sinyal yok → `TEST`.
Reklam sinyali satış kanıtı değildir: Ad Library satış, hedefleme ve ROAS göstermez; bazı reklamlar test/farkındalık için uzun kalır.
Bant kararı (`aliexpress-firsat`): **erken dalga** (1–10 reklamveren, artış) hedef, **doymuş** ELE.

## kayit.csv (kreatif desen sayımı için, `is/kesfet/kreatif/kayit.csv`)
Başlık (virgül ya da sekme): `id,kaynak,hesap,pazar,yayin_tarihi,okuma_tarihi,izlenme,begeni,yorum,paylasim,takipci,hesap_medyan,reklam_gun,kopya,kanca_metni,kanca_ailesi,giris_turu,format,ses,cta,duygu,mizah,mekanizma,kazanan`
- `kaynak`: IG-organik / TT-organik / YT / META-reklam / TTCC-topads / BIZ · `pazar`: TR / ABD / AB-<ülke>.
- Sayılar ham yazılır (12000, 1,2MN değil). `kazanan` boş bırakılır — `desen_say.py` hesaplar; elle yazılan değer hesapla çelişirse reddeder.
- Reklam satırı izlenen her OLCEKLENIYOR kreatif için **ve** aynı sorgudan en az bir TEST kreatif için yazılır (kaybeden olmadan desen ayırt edilemez).
