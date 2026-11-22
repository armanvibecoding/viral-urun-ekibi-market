# Hüküm hattı (ölçü = betik · zevk = kör jüri · kök neden = direktör)

**Hüküm hattı (ön-üretimde kredi onayından önce ve teslimde; üç ayrı el):**
1. **Ölçü = betik.** Ölçülebilir her şey `kapi.py` altındaki betiklerdedir (§5c); ajan ölçülebilir şeyi puanlamaz.
2. **Zevk = kör jüri.** `python3 "${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/juri.py" pano --cikti is/NN/juri/tur-T --mod teslim|onuretim
   --bizim VNN=<video ya da kare klasörü> --referans <gerçek viral 1> --referans <2> --referans <3>` (referans: `viral-referans.md`'deki,
   performansı ölçülmüş videoların kareleri; ekran görüntüsüyse `--arayuz-maske`). Sonra `video-juri` ajanını **3 ayrı çağrıyla** çalıştır;
   brief yalnız pano klasörü + kopya no (senaryo, kontrat, önceki puan, hangisinin bizim olduğu verilmez). Birleştir:
   `juri.py birlestir is/NN/juri/tur-T --kayit is/NN/elestiri/juri.jsonl --tur T --proje .` → GEÇTİ/KALDI betiğindir.
3. **Kök neden = direktör.** Kaldıysa eşleşmeyi aç ve `video-elestirmen`i bir kez çağır: kök neden sınıfı, dur/devam, ≤ 3 emir.
   `hikâye`, `malzeme` ya da `tavan` çıkarsa kurgu turu açma. Aynı video için en fazla 3 tur.
**"En iyi" performanstan öğrenilir, beğeniden değil:** jürinin kendisi gerçek sonuçla sınanır — `juri.py set` (analiz veritabanından
performansı ölçülmüş videolar) → `pano --mod kalibrasyon` → 3 kopya → `juri.py kalibrasyon` (jüri sırası ↔ izlenme/takipçi, kaydetme +
paylaşım, reklamın yayında kalma süresi, sepete ekleme). Sonuç UYUMLU değilse jüri hükmü DENEME sayılır; kullanıcıya böyle söyle.
Ayda bir ve jüri talimatı her değiştiğinde yeniden koş. Kullanıcıdan "beğendin mi" toplanmaz.

## Kalibrasyon adımları
1. `python3 "${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/juri.py" set --analiz-db <proje>/veri/analiz.db --cikti is/kalibrasyon/set-N --nis <niş> --adet 20`
   (veritabanı yoksa çıkış 3: "veri yok"; uydurma set kurulmaz).
2. Her videonun karelerini topla, `kalibrasyon.tsv` `yol` sütununa yaz; reklam (aktif_gun, varyant) ve mağaza
   (sepete_ekleme_orani; Shopify analitiğinden yalnız okunur) ölçütleri varsa aynı TSV'ye sütun olarak ekle.
3. `juri.py pano --mod kalibrasyon --tsv … --cikti is/kalibrasyon/set-N [--arayuz-maske]` → `video-juri` 3 kopya → `juri.py kalibrasyon is/kalibrasyon/set-N --proje .`
4. UYUMLU (ρ ≥ 0,5, n ≥ 8) değilse: jüri hükmü DENEME; "ayırt etmiyor" ya da "performansı öngörmüyor" işaretli alanın tanımı
   `agents/video-juri.md`'de yeniden yazılır ve kalibrasyon yeniden koşulur. Talimat kalibrasyonsuz değiştirilmez.
5. Kendi yayınlanan videoların 48. saat ölçümü (`yayin_olc.py`) geldikçe sete eklenir: jürinin o videoya verdiği puan ile sonucu.
