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

Windows notu: kancalar ve `.sh` betikleri için Git for Windows (Git Bash) gerekir; Python betikleri doğrudan çalışır.
iPhone modu Windows'ta yoktur; ürün avı Chrome'da instagram.com/reels ile yapılır.
