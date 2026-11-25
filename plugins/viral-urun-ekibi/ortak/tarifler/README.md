# Tarifler (recipes)

Eklentideki her yetenek bir **tarif**: tek dosya, çalıştırılabilir komutlar, ölçülebilir kalite çıtası, kapılar ve "bitti" tanımı.
Hedef: ilk deneme, elle uzun iterasyonla ulaşılan kaliteyle çıksın. Beceri dosyaları (SKILL.md) kısa yönlendirir, uzun metin burada durur.
Betik yolları `${CLAUDE_PLUGIN_ROOT}/…`; her tarif aynı iskelet: Amaç → Girdi → Adımlar → Kalite çıtası → Kapılar → Sık hata → Bitti tanımı.

| Tarif | Ne zaman | Komut (özet) | Kapı | Örnek çıktı |
|---|---|---|---|---|
| [01 ürün videosu TR Reels](01-urun-videosu-tr-reels.md) | tek ürün reklam videosu (VARSAYILAN) | `cut/scripts/hizli_kurgu.py ayar.json --katı` | `kurgu_kontrol` · `--goruntu` · `ses_olc --kapi` 0 | 8–15 sn MP4, kutulu yazı, güvenli alan, müzik rampası |
| [02 hikâye videosu organik](02-hikaye-videosu-organik.md) | stok + ürün fotoğrafı + kinetik yazı, 25 sn | `cut/scripts/hikaye/uret.py ayar.json` | `hikaye_kur --dogrula` · `ses_olc --kapi` · `--goruntu` 0 | 25,0 sn MP4 + 10 karelik pano + lisans tablosu |
| [03 müşteri senaryosu A+B](03-musteri-senaryosu-sadik-ve-yorum.md) | müşteri/ortak kendi senaryosunu verdi | tarif 02 iki kez (A sonra B) | tarif 02 kapıları, "Değişenler" listesi | `_A-sadik.mp4` + `_B-yorum.mp4` |
| [04 seslendirme ElevenLabs](04-seslendirme-elevenlabs.md) | sahnelere VO gerekli | Chrome + `hikaye/alici.py` + `ses.py` (`ses.vo`) | `ses_olc --kapi` 0, kredi tablosu | `ses/voNN.mp3` + karışmış video |
| [05 Flow klibi](05-flow-klip.md) | gerçek kareden kısa klip | Flow (Chrome) + `klip_qc.py` | `klip_qc` 0, defter toplamı ≤ tavan | `flow/klipler/*.mp4` + `DEFTER.md` |
| [06 Trendyol + AliExpress avı](06-trendyol-ve-aliexpress-avi.md) | TR'de satılacak ürün bulma | `hunter/trendyol/scripts/*` + oran turu | `trendyol_kontrol` · `kirma_testi` 0 | 5 niş × 5 ürün + tek öneri |
| [07 Excel teslim](07-excel-teslim.md) | ürün listesini dosya olarak ver | `ortak/excel_yaz.py … --kopya <dosya.xlsx>` | `excel_yaz` · `excel_test` 0 | `.xlsx` (3 sayfa) |
| [08 geri bildirim döngüsü](08-geri-bildirim-dongusu.md) | kullanıcı/ortak geri bildirimi geldi | kontrata/derslere yaz → eklenti kuralı | `geri_bildirim_kontrol` 0 | kalıcı kural, ikinci kez gelmeyen madde |
| [09 limit ve devam](09-limit-ve-devam.md) | limit/bağlam/ağ kesintisi | `DURUM.md` + `schedule`/`CronCreate` | devam sonrası `ls` + kapı çıktısı | güncel DURUM.md + devam zamanlayıcısı |
| [10 kanca varyasyon testi](10-kanca-varyasyon-testi.md) | aynı çekimden 10+ kanca sürümü (+ tekrar yayın deneyi) | `cut/scripts/kanca_varyasyon.py ayar.json kancalar.json --render` | `kanca_varyasyon_test` 0 + tarif 01 kapıları | N video + yayın planı + kayıt tablosu |
| [11 biçim kopyala](11-bicim-kopyala.md) | tutmuş biçimin KARE SIRASI + kendi çekimin (başkasının görüntüsü/sesi/yüzü alınmaz) | `cut/scripts/klip_qc.py referans.mp4 --pano` (çözümleme) → tarif 01/02 | `senaryo_kontrol` 0 + tarif 01/02 kapıları | zamanlı kare sırası + video + haftalık ≥ 10 kayıtlık biçim kütüphanesi |

**Video tarifleri (01, 02, 03, 10, 11) önce ön-üretim kartı ister:** `studio/scripts/on_uretim_karti.py` (pazar kartı → kanca ailesi + kanıt → sahne şablonu → müzik kararı → ilk 1 sn). Kart yoksa hat çalışmaz. Pazar ayrımı her video tarifinde: ABD güçlü veri · AB/UK eşik ABD'nin yarısı · TR verisi zayıf.

## Yeni tarif yazma
1. Tek dosya `NN-ad.md`; kural metnini çoğaltma, kimliğe atıf yap (SES-01, ICE-01 … `ortak/kurallar.md`).
2. Komutlar kopyala-yapıştır çalışmalı; kapılar çıkış koduyla ölçülür.
3. Betik varsa kırma testi yaz (kapıyı bozup çıkış ≠ 0 gör).

## Her sürümden önce: `sinav_kos` (sabit sınav seti)
Sürüm etiketi/paket çıkarmadan önce yedi özelliğin sınavı koşulur; hangisi KALDI ise sürüm çıkmaz, `olculemedi` kalanlar sürüm notuna "ölçülemedi" diye yazılır (geçti sayılmaz).
1. Üretimi sınav vakalarıyla yap: her özellik için `a-kolay` · `b-zor` · `c-tuzak` (`ortak/sinav/<özellik>/vakalar/*/vaka.json` girdisi) → `<çıktı>/<özellik>/{a-kolay,b-zor,c-tuzak}/`.
2. Depo kökünde (kurulan eklentide değil): `python3 scripts/sinav_kos.py <özellik> <çıktı>/<özellik> --referans-kok <referans kareleri klasörü>` — özellikler: 01-urun-videosu · 02-kanca-senaryo · 03-hikaye-videosu · 04-ses-muzik · 05-gorsel · 06-urun-avi · 07-site.
3. Kör jüri (01, 02, 03, 05, 07): koşucu adsız panoyu hazırlar (`juri/`); `jury` ajanı 3 bağımsız kopya (`KOR-1..3.json`) yazar; koşucu yeniden koşunca hüküm verir (bizim ≥ referans medyanı − 1 ve `juri.py` eşikleri).
4. Çıkış 0 değilse `SONUC.md`'deki KALDI satırı düzeltilir (tarif 08 döngüsü); eşik gevşetilmez.
5. Koşucunun kendisi bozulduysa: `python3 scripts/sinav_kos_test.py` (kırma testi) yeşil olmadan koşucu sürümde kullanılmaz.
Ayrıntı ve vaka tanımı: `ortak/sinav/README.md`; ChatGPT sürümünde betik yok: `ekler/chatgpt/tarifler/sinav-kontrol-listesi.md` (elle liste).
