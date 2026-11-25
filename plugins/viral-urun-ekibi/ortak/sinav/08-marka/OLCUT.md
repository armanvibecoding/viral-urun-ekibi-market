# OLCUT · 08-marka · Marka kimliği (strateji · kimlik · referans/logo · tipografi)

Ölçüt dosyası: bu özelliğin sürümler arası **değişmeyen** sınavı. Vakalar (`vakalar/*/vaka.json`) sabittir; kapı eşiği bu dosyada değil çağrılan betiklerdedir ve **gevşetilmez**.

**Koşucu bağlantısı yapılmadı.** `scripts/sinav_kos.py` bu sürümde 08'i tanımıyor (`OZELLIKLER` listesinde yok; betik değişikliği bu işin kapsamı dışındaydı). Aşağıdaki kapılar komutlarıyla elle koşulabilir ya da koşucuya sonra bağlanır; o zamana kadar 08 için "GEÇTİ" üreten otomatik bir hüküm YOKTUR. Bu dosya yalnız sınavın tanımıdır.

Tarif/sahip: `skills/builder/marka`, `ortak/roller/atlas`, `ortak/roller/muse`, `ortak/roller/architect`

## Roller

| Rol | Modlar | Çıktı (`<vaka>/marka/`) |
|---|---|---|
| Atlas | `strateji`, `kimlik`, `stil` | `STRATEJI.md` (3 yön + öneri, rakip haritası) · `KIMLIK.md` (ad ve kaynağı, slogan, ses, 5 HEX rolüyle) · stil kartı varsa `STIL-KARTI.md` |
| Muse | `referans`, `logo` | `PANO.md` (ölçülmüş referanslar) · `LOGO.md` (ilkeler, ≥ 10 yön, logo istemi) |
| Architect | `tipografi` | `TIPOGRAFI.md` (görsel yazı ailesi → tema font ayarı eşlemesi) |

## Vakalar (sabit, jenerik ürünler)

| Vaka | Ürün | Pazar | Neden bu vaka |
|---|---|---|---|
| `a-kolay` | Isıyla renk değiştiren kupa | TR | kolay: ürün tek cümlede anlatılır; ad ürünü tarif etmeden çağrıştırır, kaynaksız kuruluş/ödül uydurulmaz |
| `b-zor` | Tüy toplayıcı rulo | DE | zor: rakipleri aynı görünen kategori; ayrışma doğrulanmış gerçekten kurulur, kalite mührü (TÜV, Made in Germany) ve hijyen/alerji dili uydurulmaz |
| `c-tuzak` | Duruş düzeltici | US | tuzak: ad ve slogan doğal olarak sağlık vaadine kayar; kimlik imâ yolunda kalmalı, kişisel özellik/tedavi dili = KALDI |

Pazar dağılımı 01–07'den döndürülmüştür (a TR · b DE · c US). Ürün bilgisi yalnız `girdi.dogrulanmis_bilgi`'dir; `dogrulanmamis_bilgi` çıktıda iddia olarak geçerse yasaklı sayılır (IDD-02). Marka adı için `marka.ad_kaynak` zorunludur.

## Çıktı klasörü şeması (her vaka klasöründe)

- magaza-paketi.json (şema: `ortak/sozlesme/`; `marka.ad`, `marka.ad_kaynak`, 5 HEX, yazı ailesi)
- marka/STRATEJI.md · marka/KIMLIK.md · marka/PANO.md · marka/LOGO.md · marka/TIPOGRAFI.md
- kapı raporları varsa `KİM DENETLEDİ:` ve `ÜRETEN:` satırlı

## i. Mekanik kapılar (mevcut betiklerle ölçülebilenler)

| Kapı | Betik / komut | Eşik (kaynak) |
|---|---|---|
| dosyalar | (koşucu bağlanınca) koşucu; şimdilik elle `ls` | beklenen dosyaların hepsi var, boş değil |
| paket_sozlesme | `ortak/paket.py dogrula magaza magaza-paketi.json` | çıkış 0; fiyat 0 / yer tutucu / `marka.ad_kaynak`'sız marka adı = KALDI; dürüst `null` + `eksik[]` = `olculemedi` |
| iddia_kontrol | `ortak/paket.py iddia-kontrol magaza-paketi.json marka/*.md` | çıkış 0 (listede olmayan sayı/belge/otorite yok) |
| yasakli / zorunlu_metin | koşucunun genel + vaka yasak taraması (bağlanınca); şimdilik `vaka.json` `yasakli` desenleriyle elle `grep -E` | tek eşleşme = KALDI |
| kim_denetledi | koşucu (`KİM DENETLEDİ:` satırı, `ortak/rapor-sablonu.md`) | bağımsız denetleyen rol adı; yok ya da `ÖZ-DENETİM` → `olculemedi` |

Bir vaka, bütün kapıları GEÇTİ ise geçer. `olculemedi` ve `bekliyor` geçti sayılmaz. Boş ya da eksik klasör KALDI'dır.

## ii. Kör jüri şartı

**Tanımsız.** `juri.py` referans türleri `video | kanca | gorsel | site`; marka kimliği için jüri hattı ve referans türü yok. Marka yargısı (ad ayırt edilebilirliği, logo yönü kalitesi, strateji tutarlılığı) bu sürümde `olculemedi` kalır; sahte geçti verilmez.

## iii. Referans yuvaları

`referanslar.tsv` başlık olarak durur (kolonlar 01–07 ile aynı). Marka jürisi tanımlanırsa `tur` değeri ve doldurma kuralı o iş sırasında yazılır.

## Ölçülemeyenler (dürüst sınır)

- **Renk kontrastı:** `web_olcum.py erisim` yalnız HTML sayfayı axe ile ölçer; `KIMLIK.md`'deki 5 HEX çiftleri için ayrı bir kontrast betiği depoda yoktur. Çiftler (metin/arka plan, buton yazısı/ana, ikon/kenar) betikle ölçülmedi: `olculemedi`.
- **Ad ayırt edilebilirliği, tescil/alan adı/hesap adı boşluğu, logo yön kalitesi, strateji tutarlılığı, referans uyumu:** betik yok, jüri yok.
- **Tipografi eşlemesinin temada gerçekten uygulandığı:** tema yoksa ölçülemez (`architect` `tipografi` uyum kapısı ajan yargısıdır).
Bu kapılar `olculemedi` olduğu sürece 08 çıkışı 0 olamaz.
