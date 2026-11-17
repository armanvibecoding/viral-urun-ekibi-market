#!/bin/sh
# Oturum başında / sıkıştırma sonrasında proje hafızasını bağlama geri yükler.
# Çıktı Claude'un bağlamına eklenir. Hafıza yoksa sessiz kalır.
D="${CLAUDE_PROJECT_DIR:-.}/.ekip"
K="${CLAUDE_PLUGIN_ROOT:-}"
echo "Viral Ürün Ekibi eklentisi yüklü. Bilgi bankası dizini: $K/ortak/bilgi/README.md · viral DNA: $K/ortak/viral-dna.md · marka skoru: $K/ortak/marka-skoru.md"
echo "Ürün/viral/video sorularında önce bu dosyalara bak; diski tarama. İş başlatmak için ekip-lideri becerisini çağır."
echo "CEVAP BİÇİMİ (ADHD dostu, her mesajda; kullanıcı 'normal mod' diyene kadar): ilk satır yapılacak iş · çok adımlı iş numaralı liste · her mesajda durum ('5 adımdan 3'ü bitti') · süre somut · biten iş dosya yoluyla görünür · liste ≤5 öğe · giriş/özet tekrarı/'umarım yardımcı olur' yok · hata düz tonla: sebep + düzeltme · tek somut sonraki adımla bitir. Tam kurallar: $K/ortak/adhd-kurallari.md"
[ -f "$D/DURUM.md" ] || exit 0
echo "=== EKİP HAFIZASI (.ekip/) — bağlam sıfırlandıysa buradan devam et ==="
cat "$D/DURUM.md"
if [ -f "$D/KARARLAR.md" ]; then
  echo ""; echo "--- Son kullanıcı kararları (KARARLAR.md, son 25) ---"
  tail -n 25 "$D/KARARLAR.md"
fi
if [ -f "$D/DERSLER.md" ]; then
  echo ""; echo "--- Dersler: başlıklar (tamamı .ekip/DERSLER.md) ---"
  grep '^- ' "$D/DERSLER.md" | tail -n 15
fi
echo "=== Hafıza sonu. İşe devam etmeden önce DURUM.md'deki 'Sıradaki adım'ı oku. ==="
