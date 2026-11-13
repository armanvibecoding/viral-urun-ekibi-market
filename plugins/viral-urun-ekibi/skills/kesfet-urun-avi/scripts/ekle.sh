#!/bin/sh
# ekle.sh "ürün|@hesap|izlenme|beğeni|profil notu|site / fiyat|KARAR|neden"
# is/kesfet/urunler.md'ye otomatik numaralı satır ekler. 8 alan zorunlu; KARAR = AL | AL (sezonluk) | YEDEK | ELE.
# Hesap zaten listedeyse EKLEMEZ (çıkış 3). Aynı hesabın gerçekten FARKLI ürünüyse: ZORLA=1 sh ekle.sh "..."
P=${CLAUDE_PROJECT_DIR:-$PWD}; F="$P/is/kesfet/urunler.md"
[ -f "$F" ] || { echo "HATA: $F yok — önce baslat.sh" >&2; exit 2; }
[ -n "$1" ] || { echo "kullanım: ekle.sh \"ürün|@hesap|izlenme|beğeni|profil|site|KARAR|neden\"" >&2; exit 2; }
alan=$(printf '%s' "$1" | awk -F'|' '{print NF}')
[ "$alan" = 8 ] || { echo "HATA: 8 alan gerekli, $alan geldi (alan içinde | kullanma)" >&2; exit 2; }
hesap=$(printf '%s' "$1" | cut -d'|' -f2 | sed 's/^ *//; s/ *$//; s/^@//')
karar=$(printf '%s' "$1" | cut -d'|' -f7 | sed 's/^ *//')
case "$karar" in AL*|YEDEK*|ELE*) ;; *) echo "HATA: KARAR AL / AL (sezonluk) / YEDEK / ELE ile başlamalı, geldi: '$karar'" >&2; exit 2 ;; esac
if [ -n "$hesap" ] && [ "${ZORLA:-0}" != 1 ] && grep -iqF -- "@$hesap" "$F"; then
  echo "VAR — @$hesap zaten listede, eklenmedi:"; grep -inF -- "@$hesap" "$F"; exit 3
fi
n=$(( $(grep -c '^| [0-9]' "$F") + 1 ))
satir=$(printf '%s' "$1" | sed 's/ *| */ | /g')
echo "| $n | $satir |" >> "$F"
echo "#$n eklendi"
