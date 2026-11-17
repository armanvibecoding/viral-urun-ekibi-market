# Kurgu kuralları ve ayar dosyası

Kaynak: ~100 milyon izlenen ürün videosunun ölçümü (süre, yazı, CTA) + 30 videoluk gerçek AI serisinde ölçülen hatalar.
Gerekçeler ve kanıt numaraları: `<eklenti kökü>/skills/ai-video-kreatif/referans/kurgu-ve-yasaklar.md`.

## Ayar dosyası (is/NN/kurgu/VNN.json — yollar BU dosyaya göre göreli)
```json
{
  "planlar": [["../klipler/V01_S1.mp4", 0, 4.0], ["../klipler/V01_S2.mp4", 0.4, 4.0], ["../klipler/V01_S3.mp4", 0, 3.6]],
  "kanca": "Kedim bunu görünce aklı gitti",
  "cta_kelime": "PİYANO",
  "cta_plan": -1,
  "yazi_konum": "oto",
  "kanca_gizle": [],
  "sfx": [{"dosya": "../ses/tik.wav", "sn": 5.2, "db": -6, "hizala": true}],
  "klip_sesi_db": 0,
  "qc_izin": [],
  "cikti": "V01.mp4"
}
```
| Alan | Anlam |
|---|---|
| `planlar` | [klip, başlangıç sn, bitiş sn]. Hatalı uç burada kırpılır. Her planda ekranda 2–4 sn. |
| `kanca` | metin ya da plan başına liste (`null` = o planda yazı yok; K11 kart akışı: `["The problem", "Vs…", "The solution"]`). `" / "` satır sonu. |
| `cta` / `cta_kelime` | `cta` yoksa kelime + pazar: TR `Yorumlara "KELİME" yaz, linki DM'den atayım` · yurt dışı `Comment "WORD" and I'll DM you the link`. |
| `cta_plan` | CTA'nın başladığı plan (varsayılan son). Betik en az 3 sn olmasını zorlar. |
| `yazi_konum` | `oto` (her planın orta karesinde en az kenar/detay olan bant: ust/orta/alt) · `ust` · `orta` · `alt` · piksel. |
| `kanca_gizle` | yakın planda ürün yazısının üstüne binmesin diye kancasız planlar. |
| `sfx` | kullanıcının telifsiz ses dosyası; `hizala: true` = plan saniyesinin ±1,2 sn'sindeki gerçek ses yükselişine oturur. |
| `qc_izin` | ölçüm işaretledi ama 4 fps panoda doğal hareket görülen plan numaraları (0'dan). Gerekçeyi DURUM'a yaz. |
| `pazar`, `font`, `min_yukseklik` | isteğe bağlı geçersiz kılma (varsayılan: KARARLAR.md, otomatik font, 1280). |

## Süre ve kesme
- Toplam 8–15 sn, hedef 10–12 (milyonların medyanı 12 sn; bu aralıkta kısaltmak tek başına kazandırmaz).
- Tek sahne şablonunda (S1) kesmesiz; 2–3 klip aynı kadrajda devam eder.
- Son kare ilk kareye bağlanıyorsa döngü (tekrar izlenme).

## Yazı
- Kanca beyaz, kalın sans-serif, siyah kontur, 1–3 satır; 40 karakter altı 72 px, üstü 64 px; CTA 56 px, kancanın hemen altında.
- Yazı ürünü ve çıkış noktasını örtmez: ürünün en büyük olduğu karede kontrol (kontrol karesi). Ürün alt yarıdaysa yazı üstte.
- Alt %20 (Instagram açıklama alanı) ve sağ %15 (düğmeler) boş.
- Emoji fontta kutucuk olur → videoya koyma, caption'a taşı. Koyu emoji koyu zeminde kaybolur.
- Türkçe büyük harf elle yazılır (`upper()` "i"yi "I" yapar); font test karesinde İ ve ı'yı kontrol et.
- Yazısız (K13) videoda yalnız caption'da CTA.
- **Organik videoda fiyat yok** (ağır kusur); fiyat caption/bio/ürün sayfasında. Ekran yazısı merak/ikna/kimlik taşır;
  ölçü/ağırlık/renk listesi yazı değildir (`ai-video-kreatif/referans/kanca-kutuphanesi.md` §1b Ekran yazısı).

## Ses
- Klibin kendi gerçek sesi esas. Efekt: kullanıcının kendi telifsiz dosyası; ürün sesi gerçek basış/olay anına (hizala).
- Lisanslı popüler müzik yok. Konuşma/seslendirme yok (kurallar ses düzeyinde dinlenebilir videoya göre).
- Açılış diegetik ses olayıyla; müzik 0. sn'de −30 dB'den başlar, 1,5–2 sn'de yatak seviyesine çıkar; ortada "bir anda açılma" yok (`ses_olc.py --muzik_stem --kapi`).
- Hedef −14 LUFS; tek geçişli normalleştirme videolar arasında 8 dB fark bıraktı → betik ölç-kazanç-ölç döngüsü yapar.
- Seri halinde videoları art arda dinlemek mümkün değilse LUFS satırlarını karşılaştır (±1 içinde olmalı).

## Klip kalite kapısı — neden 4 fps
Gerçek seride saniyede ~1,5 kareye bakılan 30 videonun 17'sinde sonradan hata çıktı: yanlış parçaya basınca sonuç,
kimse dokunmadan ürün çalışması, ışınlanma, hayvanın yavaşça cins değiştirmesi. Ölçüm (sıçrama) ışınlanma ve gizli
kesmeyi yakalar; yavaş dönüşümü yalnız 4 fps pano yakalar. İkisi birlikte zorunlu.
Kök sebepler: başlangıç karesi (pati havadaysa yanlış yere iner) · prompt (belirsiz yön, AUDIO satırındaki olmayan olay) ·
video modeli (kesme/dönüşüm → kırp ya da yeniden üret).
