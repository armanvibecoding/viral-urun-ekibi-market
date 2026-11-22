# Kurulum kontrolü (ilk oturumda bir kez; sonucu .ekip/DURUM.md'ye "Ortam:" satırı olarak yaz)

Her satırı ölç, tahmin etme. Eksik olanı kullanıcıya tek listede, kurulum komutuyla bildir.

| Gereksinim | Ölçüm | Eksikse |
|---|---|---|
| İşletim sistemi | `uname -s` (Darwin=Mac) ya da Windows ortamı | — |
| ffmpeg | `ffmpeg -version` ya da `python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"` | Mac: `brew install ffmpeg` · Windows: `winget install Gyan.FFmpeg` |
| Python 3 | `python3 --version` (Windows: `py --version`) | python.org'dan kur |
| openpyxl (Excel) | `python3 -c "import openpyxl"` | `python3 -m pip install --user openpyxl` |
| Chrome + Claude eklentisi | tarayıcı araçları yanıt veriyor mu | Chrome'a "Claude" eklentisini kur, `/chrome` ile bağla |
| Bilgisayar kontrolü (yalnız Mac iPhone modu) | computer-use araçları var mı | `/mcp` → computer-use → Enable; Erişilebilirlik + Ekran Kaydı izni |
| iPhone Yansıtma (yalnız Mac) | uygulama açılıyor mu | macOS 15+, iPhone aynı Apple hesabında; yoksa "tarayıcı" modu kullanılır |
| Swift derleyici (yalnız Mac iPhone modu) | `swiftc --version` | `xcode-select --install` |
| Shopify bağlantısı (yalnız mağaza kolu) | `/mcp` listesinde `shopify` bağlı mı (eklenti `.mcp.json` ile gelir) | `/mcp` → shopify → giriş; giriş ekranını kullanıcı geçer |
| Pillow ≥ 10 (mağaza görsel betikleri) | `python3 -c "import PIL; print(PIL.__version__)"` | `python3 -m pip install --user "pillow>=10"` |
| Node.js 22+ (hareketli tasarım, HyperFrames) | `node --version` · `npx --version` | nodejs.org'dan LTS (22+) · Mac: `brew install node` · Windows: `winget install OpenJS.NodeJS.LTS` |
| HyperFrames CLI | `npx --no-install hyperframes --version` (paket yoksa hata verir, indirmez) | Kullanıcı onayıyla: `npx hyperframes doctor --json` (ilk çağrı CLI'yi indirir) → `.ok` true olmalı; Chrome eksikse `npx hyperframes browser ensure` |

Windows notu: kancalar ve `.sh` betikleri için Git for Windows (Git Bash) gerekir; Python betikleri doğrudan çalışır.
iPhone modu Windows'ta yoktur; ürün avı Chrome'da instagram.com/reels ile yapılır.
HyperFrames notu: becerileri bu eklentinin içinde gelir (`viral-urun-ekibi:hyperframes` vb.); `npx hyperframes skills`,
`skills update` ya da `npx skills add` ÇALIŞTIRILMAZ (kişisel kopya kurar, eklentiyle çakışır). `init` her zaman `--skip-skills` ile.
CLI kullanım sayacı (telemetri) gönderir; kullanıcı isterse `npx hyperframes telemetry disable`. HyperFrames yoksa video yine
çıkar (yazı `hizli_kurgu.py` ile), ama `studio` hareketli katman kuralı karşılanmamış olur → raporda yaz.

## HyperFrames beceri adları (SKILL.md'den taşındı)
**Beceri adları:** HyperFrames becerileri bu eklentiden `viral-urun-ekibi:hyperframes`, `viral-urun-ekibi:hyperframes-cli`,
   `viral-urun-ekibi:hyperframes-registry`, `viral-urun-ekibi:media-use` adıyla çağrılır. Kullanıcının `~/.claude/skills` altında
   aynı adlı kişisel kopyası olabilir (öneksiz `hyperframes`); ekip işinde öneklisini kullan, ajana da öneklisini yaz.
   Becerilerin içindeki `/hyperframes-cli` gibi atıflar = aynı paketteki öneklisi. Lisans: `${CLAUDE_PLUGIN_ROOT}/THIRD_PARTY_NOTICES.md`.
