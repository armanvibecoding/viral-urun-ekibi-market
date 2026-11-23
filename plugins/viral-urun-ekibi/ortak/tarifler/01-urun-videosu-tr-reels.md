# Tarif 01 — Ürün videosu (TR Reels) · VARSAYILAN

## Amaç
Tek ürün için 8–15 sn, 1080×1920, Türkçe, Reels güvenli alanında, ilk turda "geri bildirim gerektirmeyen" reklam videosu.
Bu tarif studio ve cut'ın varsayılanıdır; kullanıcı başka stil istemedikçe aşağıdaki stil uygulanır.

## Girdi
Ürün adı + 1 gerçek ürün fotoğrafı/klibi · pazar = TR · ürün tipi (ekranlı / ekransız / sağlık) · ≥3 viral referans (yoksa 3. adım "jüri yapılamadı" notuyla geçer).

## Adımlar
0. **Ön-üretim kartı (zorunlu, ilk adım).** `python3 "${CLAUDE_PLUGIN_ROOT}/skills/studio/scripts/on_uretim_karti.py" sablon --pazar <US|UK|DE|FR|ES|TR> > is/NN/on-uretim-karti.json`, sonra doldur: pazar kartı seçimi (`pazar-kartlari/<P>.md`) → kanca ailesi K<n> + kanca metni, kanıt numarasıyla (`studio/referans/kanca-kutuphanesi.md`'den; kopyalama, numara göster) → sahne şablonu S<n> (`sahne-sablonlari.md`) → müzik/ses kararı (`muzik-kutuphanesi.md`) → ilk 1 sn'de ne görünecek. Kapı: `python3 …/on_uretim_karti.py kontrol is/NN/on-uretim-karti.json` çıkış 0. **Kart yoksa ya da geçersizse sonraki adım çalışmaz** (hikaye_kur.py ve kutulu `hizli_kurgu.py` kartı kendileri denetler; kırma testi `on_uretim_karti_test.py`).
1. Ürün kontratı: `is/NN/kurgu/KURALLAR.md` (`cut/referans/KURALLAR-sablon.md`'den). Ürün tipi ekransız ise kurgu ayarına `"urun_tipi": "ekransiz"` yaz.
2. Klipler hazır (Flow klibi ya da gerçek çekim). Kontrol: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/klip_qc.py" is/NN/klipler/*.mp4 --pano`; `_qc.jpg`'yi 4 fps her kare aç.
3. Kurgu ayarı `is/NN/kurgu/V01.json` (hizli_kurgu biçimi) — **varsayılan stil alanları**:
   ```json
   {"yazi_stil": "kutulu", "urun_tipi": "ekransiz", "font": "font/TikTokSans.ttf", "font_agirlik": "Bold",
    "planlar": [{"klip": "klipler/P1.mp4", "bas": 0.0, "bit": 1.7, "gecis": "kesim",
                 "yazi": "Dizin ağrıyor mu?", "vurgu": "ağrıyor", "renk": "#FFE600", "konum": 0.16, "kelime_kelime": true}],
    "cta": {"satir1": "Ürün yaz, sana da göndereyim", "vurgu": "Ürün", "renk": "#22C55E", "plan": 7, "konum": 0.60},
    "cikti": "kurgu/V01.mp4"}
   ```
   Tek kelime vurgu sarı (`#FFE600`) ya da yeşil (`#22C55E`); yazı kelime kelime çıkar; kutu yarı saydam koyu, kontursuz.
4. Koştur: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/hizli_kurgu.py" is/NN/kurgu/V01.json --katı`
5. Sağlık ürünüyse (ürün sayfası sağlık/sonuç dili taşıyorsa) kapanış planına bilgi notu satırı: `Tıbbi tedavi amaçlı değildir` (IDD-01 bilgi notu; sağlık cümlesi elenmez).
6. Ses: müzik ilk kareden girer (SES-01), 1,5–2 sn rampa; ani açılma yok. `ses_tasarla.py --muzik … --muzik_fade_in 1.75 --stem_klasoru is/NN/ses/stem_V01 …`; müzik kaynağı açık lisanslı ya da kullanıcının dosyası (SES-02).
7. Kapılar (tek tek, çıkış 0): `ses_olc.py V01.mp4 --muzik_stem …/muz.wav --kapi` · `kurgu_kontrol.py is/NN/kurgu/V01.json --video kurgu/V01.mp4` · `kurgu_kontrol.py --goruntu kurgu/V01.mp4 --kesimler <plan başları>`.
8. Jüri: referans ≥ 3 ise `juri.py` hattı (tarif 08 "Hüküm"); < 3 ise iş durmaz, teslim notuna `jüri yapılamadı (referans < 3)` yazılır ve referans bulma ayrı iş olarak DURUM.md'ye eklenir.


## Pazar ayrımı (kart `pazar` alanı; kaynak: `skills/studio/referans/pazar-katmani.md` §0–§3, `pazar-kartlari/<P>.md`)
| Pazar | Veri gücü | Kural |
|---|---|---|
| **ABD** (varsayılan) | güçlü (79 milyon kayıt) | kanca kütüphanesinin tüm KURAL aileleri geçerli; ICE-02 ABD kültür ögesi |
| **AB / UK** (DE, FR, ES, UK) | orta (12 kayıt, 7'si İngilizce) | paylaşım beklentisi ABD'nin yarısından az (paylaşım/beğeni 0,27 vs 0,69): **ABD eşiğiyle video öldürülmez**; kart `esik: "abd-yarisi"` |
| **TR** | **zayıf (1 kayıt; GÖZLEM)** | **TR verisi zayıf, ilk testten sonra kalibre edilir.** Kanca ≤ 8 kelime; kalıp yasakları `pazar-kartlari/TR.md`; kart `tr_veri_zayif: true`; TR eşiği yok (`olcum-ve-test-plani.md`) |
Saha notu: Keşfet verisi ABD'ye ayarlı hesaptan geldi (26 ürün videosunun ~23'ü ABD, TR 0); TR kanıtı ayrı yöntemle toplanır.

**Müzik: ölçülmedi.** Saha verisinde müzik türü bilinmiyor (116 analizde `muzik_turu = bilinmiyor`; yalnız n=7 ses etiketi, `studio/referans/muzik-kutuphanesi.md`). Kural = rampa (SES-01) + after-dark/trend tarifi (kütüphane "Karar tarifi"); iddia etme, ilk testten sonra ses etiketini kayıt tablosuna yaz.

## Döngü sürümü (varsayılan format; saha: 4/4 hit 6–10 sn başa saran döngü)
Ayara `"format": "dongu"` ve `"tatmin_ani": {"bas": 3.0, "bit": 4.5}` yaz. Kurulum: 3–6 plan, plan ~1,3–2 sn, toplam 6–10,5 sn; **son plan ilk plan** (aynı klip: son kare ilk kareye bağlanır); video tek **tatmin/kanıt anı** etrafında kurulur (kaşık soğuyor, kirli su gidere dökülüyor, buzlu cam tek hamlede temizleniyor); yazı **kanca ↔ CTA dönüşümlü** (kanca ilk karede, CTA `Comment "KELİME" and I'll DM you the link` / LINK IN BIO sonra; ayrı bitiş kartı yok). Ölçülebilir karşılığı `kurgu_kontrol.py` kuralları `dongu`, `tatmin`, `cta`, `plan` (6–10,5 sn) — kırma testleri `kendini_test.py`'de. 25 sn hikâye ayrı format (tarif 02).

## Kalite çıtası (ölçülebilir)
| Madde | Çıta |
|---|---|
| Süre / çözünürlük | döngü: 6–10,5 sn · aksi 8–15 sn · 1080×1920 · 30 fps |
| Ön-üretim kartı | geçerli (`on_uretim_karti.py kontrol` 0) |
| Döngü / tatmin / CTA | son plan = ilk plan · tatmin anı ≥ 0,5 sn · CTA yazısı var, kancayla aynı anda değil (`kurgu_kontrol` 0) |
| Güvenli alan | yazı üst %12 ve alt %20 boş; sağ %15 boş; kutu karenin içinde (hizli_kurgu `kutulu` bunu kendisi sıkıştırır) |
| Yazı | kutulu, kontursuz; ≤ 5 kelime; kelime başına ≥ 0,25 sn okunma + 0,5 sn tepki; vurgu = tek kelime |
| Kanca | ilk karede (bas < 0,05 sn), ≤ 2 satır |
| Ürün | ilk 0,9 sn'de görünür (ekransız üründe `urun` planı yeterli) |
| Müzik | ilk kareden, 1,5–2 sn rampa, ani açılma yok (`muzik_giris.tuttu=true`) |
| Ses | −14 ±1 LUFS, tepe ≤ −1 dBTP, delik yok |
| Sağlık | bilgi notu satırı kapanış planında |

## Kapılar
`hizli_kurgu --katı` 0 · `kurgu_kontrol` 0 (ayar + video) · `--goruntu` 0 · `ses_olc --kapi` 0 · `captain/scripts/kapi.py yayin is/NN --proje .` 0.

## Sık hata ve düzeltmesi
- Yazı düz beyaz, küçük, üstte → `yazi_stil` yazılmamış; ayara `"yazi_stil": "kutulu"` ekle (ilk turda geri bildirim gerektiren tek büyük sebep).
- "videoda değişmiş ekranlı plan yok" ekransız üründe → ayara `"urun_tipi": "ekransiz"`; `urun` planı yeterli (kırma testi: `cut/scripts/kendini_test.py`).
- Müzik bir anda açılıyor → `--muzik_fade_in 1.75`, müzik başlangıcı ses_olc `muzik_giris` ile ölç.
- Yazı kancayı örtüyor → `konum` 0,16–0,20 (üst) ya da 0,60–0,70 (alt üçte bir); alt %20'ye inme.

## Bitti tanımı
Kapıların hepsi çıkış 0, `is/NN/teslim/` altında MP4 + kontrol karesi + caption, DURUM.md güncel, kullanıcıya tek mesaj: dosya yolu + 3 satır ölçüm özeti.
