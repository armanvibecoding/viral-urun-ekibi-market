# Tarif 04 — Seslendirme (ElevenLabs) · betiksiz ChatGPT sürümü

## Amaç
Sahne cümlelerini seslendirmeye hazırlamak ve karışım talimatını yazmak. ChatGPT ElevenLabs'e giriş yapmaz, satın alma yapmaz; üretimi ve indirmeyi **kullanıcı** yapar.

## Adımlar
1. Cümle tablosu: no · cümle · sahne başlangıç sn; kelime başına ≈ 0,35–0,45 sn ile süre bütçesi; pencereye sığmayan cümleyi kısalt (sadık senaryoda kısaltma yok → sahne süresini uzat).
2. Ses seçimi: dil ve ürüne göre (ABD/AB-UK İngilizce sakin güven veren; TR Türkçe); seçilen ses adı DURUM bloğuna yazılır, seri boyunca değişmez.
3. Kullanıcıya talimat: kendi ElevenLabs oturumunda her cümleyi üretir; kredi harcar (önce cümle sayısı × tahmini kredi tablosu); indirme Chrome'da tek tek (Chrome çoklu indirmeyi sessizce keser: her indirmeden sonra dosyanın indiğini kontrol et); dosyalar `vo01.mp3 …` adıyla sohbete yüklenir.
4. Karışım talimatı (CapCut/InShot ya da ffmpeg): VO başlangıçları sahne başlangıcından ≤ 0,4 sn sonra; **müzik VO altında −8…−12 dB** (duck); ilk karede diegetik ses; müzik 1,5–2 sn rampa; çıkış −14 ±1 LUFS, tepe ≤ −1 dBTP.
5. Not: ses kapısı konuşma hecelerini müzik sıçraması saymaz; ölçüm müzik katmanında yapılır (eklentinin yerel `ses_olc --vo` kapısı). ChatGPT'de ölçüm yok: kullanıcı videoyu bir kez sesli izleyip "VO anlaşılıyor mu, müzik ani açılıyor mu" diye cevap verir.

**Pazar:** VO dili pazarın dili; ABD güçlü veri; AB/UK eşik ABD'nin yarısı; TR verisi zayıf, ilk testten sonra kalibre. Müzik ölçülmedi, kural = rampa.

## Kalite çıtası
−14 ±1 LUFS · tepe ≤ −1 dBTP · müzik VO altında −8…−12 dB · VO başlangıcı sahne başından ≤ 0,4 sn · cümle başına tek dosya `voNN` · kredi tablosu yazılı.

## Kendi çıktını şu 10 maddeyle denetle
1. Her cümlenin süre bütçesi pencereye sığıyor. 2. Ses adı DURUM'da, seri boyunca aynı. 3. Kredi tablosu (cümle × kredi) kullanıcıya gösterildi. 4. Giriş/satın alma adımı ChatGPT'ye bırakılmadı. 5. İndirme tek tek; her dosya sohbete yüklendi. 6. Dosya adları `voNN`. 7. Duck −8…−12 dB yazılı. 8. VO başlangıçları ≤ 0,4 sn kuralına uyuyor. 9. Müzik rampası ve diegetik açılış talimatta var. 10. Sesi dinleyemediğin açıkça yazıldı.

## Bitti tanımı
Cümle tablosu + karışım talimatı + kullanıcı onayı ("VO anlaşılıyor, müzik ani açılmıyor") + DURUM bloğu.
