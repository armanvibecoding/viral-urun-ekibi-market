# Tarif 04 — Seslendirme (ElevenLabs, Chrome web arayüzü)

## Amaç
Sahne cümlelerini seslendirme (VO) dosyalarına çevirip videoya karıştırmak: müzik VO altında duck, −14 LUFS.

## Girdi
Cümle listesi (`is/NN/ses/vo.tsv`: `no · cümle · sahne başlangıç sn`) · ses seçimi (aşağıda) · kullanıcının AÇIK ElevenLabs oturumu.

## Sınırlar (değişmez)
Giriş yapma, hesap açma, satın alma, plan/kredi satın alma YOK; oturum kapalıysa dur ve kullanıcıya "ElevenLabs'e giriş yap" de. Chrome'da macOS tarayıcısını seç. Kredi harcaması üretimdir: önce cümle sayısı × tahmini kredi tabloya yazılır; kullanıcı tavan vermediyse parça sayısı kadar tek tur üretilir, tekrar denemeler tavanı aşmaz.

## Adımlar
1. Ses seçimi: video diline ve ürüne göre (ör. İngilizce, sakin, güven veren kadın sesi; TR için Türkçe konuşan ses). Seçilen ses adı DURUM.md'ye yazılır; aynı seri boyunca değişmez.
2. Her cümleyi sayfaya yaz, üret. **Chrome tek seferde çok indirmeyi sessizce engeller** (ikinci indirmeden sonra); bu yüzden indirme düğmesi değil:
   a. Geçmiş (History) listesinde üretilen öğeye tıkla (sayfa yenilenmeden liste güncellenmeyebilir; gerekirse sayfayı yenile).
   b. Sayfadaki `<audio>` öğesinin `src` değeri bir `data:` URI'dir; `javascript_tool` ile oku.
   c. Yerel alıcıyı arka planda aç: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/hikaye/alici.py" is/NN/ses 8765`; sayfada `fetch("http://127.0.0.1:8765/vo01.mp3", {method:"POST", body: document.querySelector("audio").src})` (ElevenLabs sayfası localhost'a bağlanmayı engellemez; ChatGPT sayfası engeller).
   d. Alıcı `is/NN/ses/voNN.mp3` dosyasını yazar; `ffprobe` ile süresini ölç; işin sonunda alıcıyı kapat.
3. Süre bütçesi: VO'nun sahne penceresine sığdığını kontrol et (kelime başına ≈ 0,35–0,45 sn). Sığmıyorsa cümleyi kısalt (A sürümünde kısaltma yasak → sahne süresini uzat).
4. Karıştırma: ayar `ses.vo = [{"dosya":"ses/vo01.mp3","bas":0.3}, …]`, `vo_duck_db: -10` (−8…−12 arası). `ses.py` müziği VO altında duck eder, −14 LUFS'a çeker.
5. Ölç: `ses_olc.py TESLIM/<ad>.mp4 --kapi` çıkış 0; VO'nun anlaşılırlığı için VO'lu bölümde müzik VO'dan en az 8 dB geride.

## Kalite çıtası
−14 ±1 LUFS · tepe ≤ −1 dBTP · müzik VO altında −8…−12 dB duck · VO başlangıçları sahne başlangıcından ≤ 0,4 sn sonra · cümle başına tek dosya, adı `voNN`.

## Kapılar
`ses_olc --kapi` 0 · her `voNN.mp3` süresi > 0 ve sahne penceresine sığıyor · kredi tablosu yazıldı.

## Sık hata ve düzeltmesi
- İkinci dosya inmiyor → indirme yolunu bırak, `data:` URI yöntemini kullan.
- Geçmişte yeni öğe yok → sayfayı yenile.
- Dosya adı ses adını yanlış gösteriyor (isimlendirme tuhaflığı) → önemli değil; ses seçimini DURUM.md'dekiyle eşle, adı dosya adından okuma.
- VO müzikte boğuluyor → `vo_duck_db` −12.

## Bitti tanımı
`ses/voNN.mp3` dosyaları + karışmış `TESLIM/<ad>.mp4` + `ses_olc` çıkış 0 + harcanan kredi satırı DURUM.md'de.
