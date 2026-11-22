#!/bin/sh
# claude.ai / ChatGPT Projesi'ne yüklenecek dosyaları ortak/ altından kopyalar (tek klasör, düz yapı).
# Kullanım: sh scripts/proje_paketi_yap.sh   (depo kökünden)
set -e
KOK="$(cd "$(dirname "$0")/.." && pwd)"
E="$KOK/plugins/viral-urun-ekibi"
H="$E/ekler/proje-paketi/yuklenecek"
mkdir -p "$H"
rm -f "$H"/*.md
# Proje içinde klasör yok: "../x.md" atıfları düz ada çevrilir, README "bilgi-rehberi" olur.
duzle() { sed -e 's#\.\./\([a-z-]*\.md\)#\1#g' -e 's#`README.md`#`bilgi-rehberi.md`#g' "$1" > "$2"; }
duzle "$E/ortak/bilgi/README.md" "$H/bilgi-rehberi.md"
for f in urun-katalogu kreatif-notlar firsat-gecmisi uretim-deneyimi dersler; do
  duzle "$E/ortak/bilgi/$f.md" "$H/$f.md"
done
for f in viral-dna marka-skoru sozluk; do
  if [ -f "$E/ortak/$f.md" ]; then duzle "$E/ortak/$f.md" "$H/$f.md"; else echo "EKSİK (eklenecek): ortak/$f.md"; fi
done
ADET=$(ls "$H"/*.md | wc -l | tr -d ' ')
BOYUT=$(cat "$H"/*.md | wc -c | tr -d ' ')
echo "dosya: $ADET (sınır 10) · toplam: $BOYUT bayt (sınır 1572864)"
[ "$ADET" -le 10 ] && [ "$BOYUT" -le 1572864 ] || { echo "SINIR AŞILDI"; exit 1; }
