# viral-urun-ekibi (eklenti)

Instagram'da viral ürün bulma, AliExpress'te henüz viral olmamış ürün avı, ChatGPT + Google Flow ile AI ürün videosu
üretimi ve ffmpeg ile kurgu yapan Türkçe Claude Code eklentisi. Yedi skill (`ekip-lideri`, `kesfet-urun-avi`,
`aliexpress-firsat`, `ai-video-kreatif`, `video-kurgu`, `reklam-kutuphanesi-avi`, `teklif-ve-sayfa`), altı alt ajan ve ortak bir bilgi bankası içerir.
Hareketli tasarım için HyperFrames becerileri de pakette: `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`
(çağrı adı `viral-urun-ekibi:hyperframes` vb.).
Kurulum (Claude Code içinde):

```
/plugin marketplace add armanvibecoding/viral-urun-ekibi-market
/plugin install viral-urun-ekibi@viral-urun-market
```

Başlamak için boş bir klasörde `/viral-urun-ekibi:ekip-lideri` çalıştır.

Aynı pazardaki **Mağaza Kurucu** eklentisiyle (`/plugin install magaza-kurucu@viral-urun-market`) dosya üzerinden çalışır:
bulunan ürün `urun-paketi.json` olarak Mağaza Kurucu'ya gider, kurulan mağaza `magaza-paketi.json` ile video ekibine döner,
videolar `video-paketi.json` ile mağazaya girer. Sözleşme ve doğrulayıcı: `ortak/sozlesme/`, yardımcı betik: `ortak/paket.py`.

Kurulum, ön koşullar ve kullanım: deponun kökündeki `README.md`. Katkı: `CONTRIBUTING.md`. Lisans: MIT. HyperFrames becerileri Apache-2.0 (© HeyGen, Inc.) — `THIRD_PARTY_NOTICES.md`, `licenses/APACHE-2.0.txt`.

Turkish-language Claude Code plugin for viral product research, AliExpress sourcing, AI product video generation and
ffmpeg editing. See the repository root README for setup.
