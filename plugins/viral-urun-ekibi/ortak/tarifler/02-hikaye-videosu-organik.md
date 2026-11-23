# Tarif 02 — Hikâye videosu (organik, 25 sn)

## Amaç
Gerçek stok + gerçek ürün fotoğrafı + kinetik tipografi (HyperFrames) ile 25 sn'lik, kancası ilk karede, işlevi ima eden organik video.
Betikler hazırdır: `${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/hikaye/` (ayar JSON → video; kredi harcamaz).

## Girdi
Senaryo (kanca cümlesi, 4–6 kısa cümle, kapanış) · pazar kültür ögesi (ABD: en az bir görünen ABD unsuru, ICE-02; TR: yerel gün/ifade) · gerçek ürün fotoğrafı (düz zeminli) · müzik (açık lisanslı, drop saniyesi bilinir) · gerekirse Flow metafor klibi (tarif 05).

## Adımlar
0. **Ön-üretim kartı (zorunlu, ilk adım).** `python3 "${CLAUDE_PLUGIN_ROOT}/skills/studio/scripts/on_uretim_karti.py" sablon --pazar <US|UK|DE|FR|ES|TR> > is/NN/on-uretim-karti.json`, sonra doldur: pazar kartı seçimi (`pazar-kartlari/<P>.md`) → kanca ailesi K<n> + kanca metni, kanıt numarasıyla (`studio/referans/kanca-kutuphanesi.md`'den; kopyalama, numara göster) → sahne şablonu S<n> (`sahne-sablonlari.md`) → müzik/ses kararı (`muzik-kutuphanesi.md`) → ilk 1 sn'de ne görünecek. Kapı: `python3 …/on_uretim_karti.py kontrol is/NN/on-uretim-karti.json` çıkış 0. **Kart yoksa ya da geçersizse sonraki adım çalışmaz** (hikaye_kur.py ve kutulu `hizli_kurgu.py` kartı kendileri denetler; kırma testi `on_uretim_karti_test.py`).
1. Klasör: `is/NN/hikaye/` içine `stok/`, `muzik/`, `ayar.json`. Ayar şeması: `hikaye/ayar-ornek.json`.
2. Stok: yüzsüz, lisanslı planlar. Pexels: `python3 stok_px.py api "<sorgu>"` (PEXELS_API_KEY) ya da Chrome yöntemi (`stok_px.py` başlığı) → `stok_px.py on <sorgu>` panoya bak → `stok_px.py al stok <id>…`. Mixkit: `stok_mk.py tara <terim>` → `al` (Restricted indirilmez). Her klip `LISANS-ham.tsv`'ye yazılır; bunu `stok/LISANS.md`'ye çevir (kaynak URL + lisans adı + okuma tarihi).
3. Ürün: gerçek fotoğraf `kes.py foto.png urun.png x0 y0 x1 y1` ile kesilir. Fotoğraf yoksa ChatGPT görseli son çare ve raporda yazılır.
4. Müzik: `python3 muzik_analiz.py muzik/parca.mp3` → drop adayı; ayara `muzik_bas` (müzikte drop sn) ve `drop` (videoda sn; kesimin üstüne oturt).
5. Ayar: `"on_uretim_karti": "on-uretim-karti.json"` (kart yoksa `hikaye_kur.py` durur) · `kesimler` (7 kesim = 8 aralık), `klipler` (aralık başına; ürün sahnesi `null`), `sahneler` (kanca bas=0 → blok → ürün → kapanış), `ses`. Fiyat ve para birimi yazma (ICE-01; `hikaye_kur.py` reddeder (ayarda `fiyat_izin` bilinçli açılmadıkça)).
6. Koştur: `python3 uret.py is/NN/hikaye/ayar.json` (HyperFrames render + ses + panolar + görüntü kapısı + TESLIM).
7. Panolara bak (`TESLIM/<ad>_pano_4fps.jpg`, `_pano10.jpg`, `_kontrol.jpg`): yazı okunuyor mu, ürün örtülüyor mu, ilk 2 sn kanca var mı.
8. Sağlık cümlesi varsa `bilgi` sahnesi (çip): "Info note: …" (IDD-01).


## Pazar ayrımı (kart `pazar` alanı; kaynak: `skills/studio/referans/pazar-katmani.md` §0–§3, `pazar-kartlari/<P>.md`)
| Pazar | Veri gücü | Kural |
|---|---|---|
| **ABD** (varsayılan) | güçlü (79 milyon kayıt) | kanca kütüphanesinin tüm KURAL aileleri geçerli; ICE-02 ABD kültür ögesi |
| **AB / UK** (DE, FR, ES, UK) | orta (12 kayıt, 7'si İngilizce) | paylaşım beklentisi ABD'nin yarısından az (paylaşım/beğeni 0,27 vs 0,69): **ABD eşiğiyle video öldürülmez**; kart `esik: "abd-yarisi"` |
| **TR** | **zayıf (1 kayıt; GÖZLEM)** | **TR verisi zayıf, ilk testten sonra kalibre edilir.** Kanca ≤ 8 kelime; kalıp yasakları `pazar-kartlari/TR.md`; kart `tr_veri_zayif: true`; TR eşiği yok (`olcum-ve-test-plani.md`) |
Saha notu: Keşfet verisi ABD'ye ayarlı hesaptan geldi (26 ürün videosunun ~23'ü ABD, TR 0); TR kanıtı ayrı yöntemle toplanır.

**Müzik: ölçülmedi.** Saha verisinde müzik türü bilinmiyor (116 analizde `muzik_turu = bilinmiyor`; yalnız n=7 ses etiketi, `studio/referans/muzik-kutuphanesi.md`). Kural = rampa (SES-01) + after-dark/trend tarifi (kütüphane "Karar tarifi"); iddia etme, ilk testten sonra ses etiketini kayıt tablosuna yaz.

## Kalite çıtası
| Madde | Çıta |
|---|---|
| Süre | 25,0 ± 0,1 sn · 1080×1920 · 30 fps |
| Kanca | ilk karede (sahne `bas=0`); `hikaye_kur` yoksa durdurur |
| Ürün | gerçek fotoğraf; ekran süresi ≥ 3 sn |
| Yazı | kelime kelime çıkış, her sahnede ≤ 8 kelime, kesim başına bir fikir |
| Fiyat | ekranda yok (ICE-01) |
| Ses | −14 ±1 LUFS · müzik girişi `tuttu=true` · drop artışı ≥ 6 dB · delik yok · sıçrama yok |
| Görüntü | kesim dışı RGB sıçraması yok, son 2 sn gürültü oranı ≤ 1,5 |
| Lisans | her stok klip için satır |

## Kapılar
`hikaye_kur.py --dogrula` 0 · `ses_olc --kapi` 0 · `kurgu_kontrol --goruntu` 0 · süre ±0,1 · caption dosyası.

## Sık hata ve düzeltmesi
- `can.wav` tepeyi şişirip drop'u eziyor → ses listesinden çıkar.
- `sessizlik_vurusu` 0,25 "delik" sayılıyor → 0,2 (varsayılan).
- Drop duyulmuyor (< 6 dB) → `giris_hedef` artır ya da `drop_oncesi_db` düşür.
- Son 2 sn gürültü oranı > 1,5 → son sahneyi sadeleştir (yoğun stok kareyi kaldır), yeniden render.
- Pexels `curl` 403 → API anahtarı ya da Chrome yöntemi; Mixkit'te Restricted lisanslı klip hiç indirilmez.

## Bitti tanımı
`TESLIM/<ad>.mp4` + 10 karelik pano + caption; kapıların çıkış kodları DURUM.md'de; lisans tablosu klasörde; kullanılan Flow kredisi (varsa) defterde (tarif 05).
