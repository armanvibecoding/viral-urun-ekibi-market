#!/bin/sh
# platform.sh — çalışma modunu yazar: "iphone" veya "tarayici". Kullanıcıya sorulmaz.
# iphone: macOS + iPhone Yansıtma uygulaması + swiftc var. Diğer her durumda (Windows, Linux, eksik araç): tarayici.
# MOD=tarayici ortam değişkeni ya da kullanıcının açık isteği önceliklidir.
[ -n "$MOD" ] && { echo "$MOD"; exit 0; }
if [ "$(uname -s 2>/dev/null)" = Darwin ] && [ -d "/System/Applications/iPhone Mirroring.app" ] && command -v swiftc >/dev/null 2>&1; then
  echo iphone
else
  echo tarayici
fi
