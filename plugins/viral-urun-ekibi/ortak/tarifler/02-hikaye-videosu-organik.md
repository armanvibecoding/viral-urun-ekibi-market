# Tarif 02 — Hikâye videosu (organik, 25 sn)

## Amaç
Gerçek stok + gerçek ürün fotoğrafı + kinetik tipografi (HyperFrames) ile 25 sn'lik, kancası ilk karede, işlevi ima eden organik video.
Betikler hazırdır: `${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/hikaye/` (ayar JSON → video; kredi harcamaz).

## Girdi
Senaryo (kanca cümlesi, 4–6 kısa cümle, kapanış) · pazar kültür ögesi (ABD: en az bir görünen ABD unsuru, ICE-02; TR: yerel gün/ifade) · gerçek ürün fotoğrafı (düz zeminli) · müzik (açık lisanslı, drop saniyesi bilinir) · gerekirse Flow metafor klibi (tarif 05).

## Adımlar
1. Klasör: `is/NN/hikaye/` içine `stok/`, `muzik/`, `ayar.json`. Ayar şeması: `hikaye/ayar-ornek.json`.
2. Stok: yüzsüz, lisanslı planlar. Pexels: `python3 stok_px.py api "<sorgu>"` (PEXELS_API_KEY) ya da Chrome yöntemi (`stok_px.py` başlığı) → `stok_px.py on <sorgu>` panoya bak → `stok_px.py al stok <id>…`. Mixkit: `stok_mk.py tara <terim>` → `al` (Restricted indirilmez). Her klip `LISANS-ham.tsv`'ye yazılır; bunu `stok/LISANS.md`'ye çevir (kaynak URL + lisans adı + okuma tarihi).
3. Ürün: gerçek fotoğraf `kes.py foto.png urun.png x0 y0 x1 y1` ile kesilir. Fotoğraf yoksa ChatGPT görseli son çare ve raporda yazılır.
4. Müzik: `python3 muzik_analiz.py muzik/parca.mp3` → drop adayı; ayara `muzik_bas` (müzikte drop sn) ve `drop` (videoda sn; kesimin üstüne oturt).
5. Ayar: `kesimler` (7 kesim = 8 aralık), `klipler` (aralık başına; ürün sahnesi `null`), `sahneler` (kanca bas=0 → blok → ürün → kapanış), `ses`. Fiyat ve para birimi yazma (ICE-01; `hikaye_kur.py` reddeder (ayarda `fiyat_izin` bilinçli açılmadıkça)).
6. Koştur: `python3 uret.py is/NN/hikaye/ayar.json` (HyperFrames render + ses + panolar + görüntü kapısı + TESLIM).
7. Panolara bak (`TESLIM/<ad>_pano_4fps.jpg`, `_pano10.jpg`, `_kontrol.jpg`): yazı okunuyor mu, ürün örtülüyor mu, ilk 2 sn kanca var mı.
8. Sağlık cümlesi varsa `bilgi` sahnesi (çip): "Info note: …" (IDD-01).

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
