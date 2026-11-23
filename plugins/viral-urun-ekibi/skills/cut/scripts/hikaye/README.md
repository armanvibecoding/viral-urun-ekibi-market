# Hikâye hattı (organik 25 sn video)

Tarif: `ortak/tarifler/02-hikaye-videosu-organik.md`. Ayar JSON'dan çalışır; marka/kişi/yol sabiti yoktur. Kredi harcamaz.

| Dosya | İş |
|---|---|
| `uret.py ayar.json` | kur → render (HyperFrames; `--sessiz-ffmpeg` yalnız test) → ses → panolar → görüntü kapısı → TESLIM |
| `hikaye_kur.py` | ayar → stok klip hazırlama + `hf/index.html` (kapılar: kanca ilk karede, fiyat yok, klip dosyası var) |
| `bloklar.py`, `kit.py`, `stil.css` | kinetik tipografi blokları (kanca, blok, iki, damga, balonlar, urun, bilgi, son, flas, bolum); tema değişkenleri |
| `ses.py` | müzik girişi düzleme + `ses_tasarla` + VO duck + −14 LUFS + `ses_olc --kapi` |
| `muzik_analiz.py` | drop adayı (bas zarfı) |
| `kes.py` | düz zeminli ürün fotoğrafından kesme (alfa) |
| `pano.py` | 4 fps pano, ilk 2 sn, kontrol kareleri, klip şeridi |
| `stok_px.py`, `stok_mk.py` | Pexels / Mixkit stok arama-indirme + lisans kaydı (Restricted indirilmez) |
| `alici.py` | tarayıcıdan yerel dosyaya alıcı (ElevenLabs ses vb.) |
| `sfx/sentez.py` | sentetik efektler (ilk kullanımda önbelleğe) |
| `ayar-ornek.json`, `test_hikaye.py` | örnek ayar ve uçtan uca + kırma testi |
