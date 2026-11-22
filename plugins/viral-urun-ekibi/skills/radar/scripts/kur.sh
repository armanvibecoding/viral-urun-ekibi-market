#!/bin/sh
# kur.sh — iPhone modunun araçlarını kurar (yalnız macOS). Kullanıcının proje klasöründen çalıştırılır:
#   sh <beceri>/scripts/kur.sh            → <proje>/.ekip/arac/
#   HEDEF=/baska/klasor sh .../kur.sh      → oraya
# Swift kaynaklarını swiftc ile derler, yardımcı betikleri yanına kopyalar. Tekrar çalıştırmak güvenlidir.
set -e
KAYNAK=$(cd "$(dirname "$0")" && pwd)
HEDEF=${HEDEF:-${CLAUDE_PROJECT_DIR:-$PWD}/.ekip/arac}
[ "$(uname -s)" = Darwin ] || { echo "Bu kurulum yalnız macOS içindir. Windows/Linux'ta 'tarayici' modu kullanılır (kurulum gerekmez)."; exit 1; }
command -v swiftc >/dev/null 2>&1 || { echo "swiftc yok. Kur: Terminal'de 'xcode-select --install' (Xcode komut satırı araçları), sonra tekrar çalıştır."; exit 1; }
mkdir -p "$HEDEF"
for f in tikla kay; do
  swiftc -O "$KAYNAK/$f.swift" -o "$HEDEF/$f"
done
for f in ortak.sh ekran.sh dokun.sh kaydir.sh izle.sh begen.sh ara.sh kalibre.sh yaz.py pano.py; do
  cp "$KAYNAK/$f" "$HEDEF/$f"
done
chmod +x "$HEDEF"/*.sh "$HEDEF"/*.py "$HEDEF/tikla" "$HEDEF/kay"
[ -f "$HEDEF/klavye" ] || echo us > "$HEDEF/klavye"
echo "KURULDU: $HEDEF"
echo "İzinler (bir kez): Sistem Ayarları > Gizlilik ve Güvenlik > Erişilebilirlik VE Ekran Kaydı → Claude'u çalıştıran uygulamayı (Terminal / Claude) aç."
