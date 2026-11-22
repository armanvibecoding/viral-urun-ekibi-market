#!/bin/sh
# kontrol.sh KELIME [KELIME...] — listede var mı? is/kesfet/urunler.md + rakipler.md içinde (büyük/küçük harf duyarsız) arar.
# Çıkış: 0 = YENİ (hiçbiri yok) · 1 = VAR (eşleşen satırlar yazılır). Hesap adı VE ürünün ayırt edici kelimesiyle ayrı ayrı ara.
P=${CLAUDE_PROJECT_DIR:-$PWD}; K="$P/is/kesfet"
[ $# -ge 1 ] || { echo "kullanım: kontrol.sh KELIME [KELIME...]" >&2; exit 2; }
bulundu=0
for k in "$@"; do
  k=$(echo "$k" | sed 's/^@//')
  if grep -inF -- "$k" "$K/urunler.md" "$K/rakipler.md" 2>/dev/null; then bulundu=1; fi
done
[ $bulundu = 1 ] && { echo "VAR"; exit 1; }
echo "YENİ"
