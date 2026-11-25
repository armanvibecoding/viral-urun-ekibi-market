# viral-urun-ekibi (eklenti)

Tek liderli Türkçe e-ticaret ekibi: ürün bul → doğrula → teklif → Shopify mağazasını kur → kreatif üret → yayınla. Sekiz iş akışı
(`captain`, `radar`, `hunter`, `spy`, `builder`, `studio`,
`cut`), 17 alt ajan (kadro: `ortak/ekip.md`), kollar arası köprü (`ortak/sozlesme/` + `ortak/paket.py`) ve ortak bir bilgi bankası içerir.
Tek giriş `captain` becerisidir. Mağaza kolu Shopify bağlantısını (`.mcp.json`) getirir; özel tema paketi yoksa **temasız mod**da
çalışır (ürün, metin ve görseller mağazanın mevcut temasına yazılır). `skills/builder/` üretilen klasördür; kaynağı depodaki
`moduller/magaza-kurucu/`.
Hareketli tasarım için HyperFrames becerileri de pakette: `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`
(çağrı adı `viral-urun-ekibi:hyperframes` vb.).
Kurulum (Claude Code içinde):

```
/plugin marketplace add armanvibecoding/viral-urun-ekibi-market
/plugin install viral-urun-ekibi@viral-urun-market
```

Başlamak için boş bir klasörde `/viral-urun-ekibi:captain` çalıştır.

Her yetenek bir **tarif**tir: `ortak/tarifler/README.md` (video, seslendirme, Flow, ürün avı, Excel, geri bildirim, limit/devam).

Mağaza kolu (`builder` becerisi) aynı eklentinin içindedir; kollar dosya üzerinden çalışır:
bulunan ürün `urun-paketi.json` olarak mağaza koluna gider, kurulan mağaza `magaza-paketi.json` ile video ekibine döner,
videolar `video-paketi.json` ile mağazaya girer. Sözleşme ve doğrulayıcı: `ortak/sozlesme/`, yardımcı betik: `ortak/paket.py`.

Kurulum, ön koşullar ve kullanım: deponun `claude/README.md` dosyası. Katkı: `CONTRIBUTING.md`. Lisans: MIT. HyperFrames becerileri Apache-2.0 (© HeyGen, Inc.) — `THIRD_PARTY_NOTICES.md`, `licenses/APACHE-2.0.txt`.

Turkish-language Claude Code plugin for viral product research, AliExpress sourcing, AI product video generation and
ffmpeg editing. See the repository root README for setup.
