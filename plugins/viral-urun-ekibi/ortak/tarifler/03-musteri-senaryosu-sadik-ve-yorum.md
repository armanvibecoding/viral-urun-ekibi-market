# Tarif 03 — Müşteri/ortak senaryosu: A (sadık) + B (yorum)

## Amaç
Müşteri ya da ortak kendi senaryosunu verdiğinde onun sözünü bozmadan video üretmek; yorumumuz ayrı bir sürüm olarak sunulur. Önce A.

## Girdi
Senaryo metni (sahne sırası, ekran yazıları, seslendirme cümleleri) · ürün listesi/gerçek ürün fotoğrafı · müşterinin yasakları (varsa) · tarif 02 hattı.

## Adımlar
0. **Ön-üretim kartı (zorunlu, ilk adım; A ve B için ayrı kart).** A'da kanca ve sahne sırası müşterinin senaryosundan gelir: kart onları kayda geçirir, kütüphanedeki en yakın aile/şablonu ve kanıtı gösterir (müşteri metni değiştirilmez). `python3 "${CLAUDE_PLUGIN_ROOT}/skills/studio/scripts/on_uretim_karti.py" sablon --pazar <US|UK|DE|FR|ES|TR> > is/NN/on-uretim-karti.json`, sonra doldur: pazar kartı seçimi (`pazar-kartlari/<P>.md`) → kanca ailesi K<n> + kanca metni, kanıt numarasıyla (`studio/referans/kanca-kutuphanesi.md`'den; kopyalama, numara göster) → sahne şablonu S<n> (`sahne-sablonlari.md`) → müzik/ses kararı (`muzik-kutuphanesi.md`) → ilk 1 sn'de ne görünecek. Kapı: `python3 …/on_uretim_karti.py kontrol is/NN/on-uretim-karti.json` çıkış 0. **Kart yoksa ya da geçersizse sonraki adım çalışmaz** (hikaye_kur.py ve kutulu `hizli_kurgu.py` kartı kendileri denetler; kırma testi `on_uretim_karti_test.py`).
1. Senaryoyu sahne tablosuna çevir: `sahne · ekran yazısı · VO cümlesi · önerilen görüntü`. Tabloyu `is/NN/senaryo-A.md`'ye yaz; müşteri metnini satır satır koru.
2. **A (sadık) kuralı:** sahne sırası, ekran yazısı ve VO cümleleri aynen kalır. Yalnız şunlar çıkar/değişir ve her biri `senaryo-A.md` altındaki "Değişenler" listesine gerekçeyle yazılır:
   - uydurma ürün adı → gerçek ürün kod adı (sitedeki ad),
   - fiyat (ICE-01), kanıtsız istatistik/yüzde (IDD-02),
   - sitede olmayan teklif/ürün (rehber, danışmanlık, jel…) → çıkar, yerine sahne metni değiştirilmez, "ürünsüz" sahne olarak bırakılır,
   - organ/eylem adı, tanınabilir yüz (platform riski, PLT-01 uyarısı).
3. A için `hikaye/ayar.json` kur (tarif 02): her cümle tek sahne; müşterinin sırası = `sahneler` sırası.
4. VO varsa tarif 04; müzik VO altında duck edilir.
5. Kapılar (tarif 02) → `TESLIM/<ad>_A-sadik.mp4`.
6. Ancak A teslim edildikten sonra **B (yorum)**: aynı ürün için kendi kancamız, daha sıkı kurgu, Flow metafor klipleri (tarif 05). Dosya adı `_B-yorum`. B, A'yı geçmeden A'nın yerine sunulmaz.
7. Müşteriye iki dosya + "Değişenler" listesi gider; hangisinin hangisi olduğu dosya adında yazar.


## Pazar ayrımı (kart `pazar` alanı; kaynak: `skills/studio/referans/pazar-katmani.md` §0–§3, `pazar-kartlari/<P>.md`)
| Pazar | Veri gücü | Kural |
|---|---|---|
| **ABD** (varsayılan) | güçlü (79 milyon kayıt) | kanca kütüphanesinin tüm KURAL aileleri geçerli; ICE-02 ABD kültür ögesi |
| **AB / UK** (DE, FR, ES, UK) | orta (12 kayıt, 7'si İngilizce) | paylaşım beklentisi ABD'nin yarısından az (paylaşım/beğeni 0,27 vs 0,69): **ABD eşiğiyle video öldürülmez**; kart `esik: "abd-yarisi"` |
| **TR** | **zayıf (1 kayıt; GÖZLEM)** | **TR verisi zayıf, ilk testten sonra kalibre edilir.** Kanca ≤ 8 kelime; kalıp yasakları `pazar-kartlari/TR.md`; kart `tr_veri_zayif: true`; TR eşiği yok (`olcum-ve-test-plani.md`) |
Saha notu: Keşfet verisi ABD'ye ayarlı hesaptan geldi (26 ürün videosunun ~23'ü ABD, TR 0); TR kanıtı ayrı yöntemle toplanır.

**Müzik: ölçülmedi.** Saha verisinde müzik türü bilinmiyor (116 analizde `muzik_turu = bilinmiyor`; yalnız n=7 ses etiketi, `studio/referans/muzik-kutuphanesi.md`). Kural = rampa (SES-01) + after-dark/trend tarifi (kütüphane "Karar tarifi"); iddia etme, ilk testten sonra ses etiketini kayıt tablosuna yaz.

## Kalite çıtası
- A'da senaryo metninin %100'ü korunur; sapma yalnız "Değişenler" listesindeki maddelerdir (liste boşsa sapma yok demektir).
- Her çıkarılan madde için gerekçe (kaynak: ürün sayfası ya da kural kimliği).
- A ve B ayrı dosya, ayrı kapı çıktısı.

## Kapılar
Tarif 02 kapıları iki sürüm için ayrı ayrı 0 · `senaryo-A.md` "Değişenler" bölümü var.

## Sık hata ve düzeltmesi
- A'yı "daha iyi yapmak" için cümle değiştirmek → geri al; iyileştirme B'dedir.
- Sitede olmayan ürünü ekranda göstermek → çıkar, "ürünsüz marka hikâyesi" olarak kur (ürün sahnesi yok).
- Kanıtsız istatistik ekranda kaldı → `senaryo-A.md` kontrol: her sayı için kaynak satırı yoksa çıkar.

## Bitti tanımı
İki video (A önce, B sonra) + "Değişenler" listesi + kapı çıktıları; DURUM.md'de her biri ayrı satır.
