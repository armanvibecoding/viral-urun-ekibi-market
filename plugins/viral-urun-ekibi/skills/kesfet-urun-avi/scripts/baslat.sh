#!/bin/sh
# baslat.sh — kullanıcının proje klasöründe keşif dosyalarını (yoksa) oluşturur. Var olan dosyaya dokunmaz.
#   is/kesfet/urunler.md        ana ürün tablosu (tek kaynak; satır yalnız ekle.sh ile)
#   is/kesfet/rakipler.md       aynı ürünün başka satıcıları, lisans yüzünden elenenler, format notları
#   is/kesfet/marka-skorlari.md hesap başına marka skoru (ortak/marka-skoru.md rubriği)
#   is/kesfet/DURUM.md          tur kaydı (yalnız ekleme)
#   .ekip/DURUM.md KARARLAR.md DERSLER.md  ekip hafızası (yoksa boş şablon)
P=${CLAUDE_PROJECT_DIR:-$PWD}; K="$P/is/kesfet"
mkdir -p "$K/kareler" "$K/kreatif/notlar" "$P/.ekip"
[ -f "$K/urunler.md" ] || cat > "$K/urunler.md" <<'T'
# Instagram keşif — ürün listesi

| # | Ürün | Hesap | İzlenme | Beğeni | Profil notu | Site / fiyat | Karar | Neden |
|---|------|-------|---------|--------|-------------|--------------|-------|-------|
T
[ -f "$K/rakipler.md" ] || printf '# Rakipler, elenenler ve notlar\n\n' > "$K/rakipler.md"
[ -f "$K/marka-skorlari.md" ] || cat > "$K/marka-skorlari.md" <<'T'
# Marka skorları (rubrik: eklentideki ortak/marka-skoru.md)

| # (urunler.md) | Hesap | Odak | Süreklilik | Kimlik | Site | Tekrar | TOPLAM | Sınıf | Etiket | Not |
|---|---|---|---|---|---|---|---|---|---|---|
T
[ -f "$K/DURUM.md" ] || printf '# Keşif tur kaydı (yalnız ekleme)\n\n' > "$K/DURUM.md"
[ -f "$P/.ekip/DURUM.md" ] || printf '# DURUM\n\n- Aktif iş: Instagram keşif\n- Aşama: başlangıç\n- Sıradaki adım: ilk tarama turu\n' > "$P/.ekip/DURUM.md"
[ -f "$P/.ekip/KARARLAR.md" ] || printf '# KARARLAR (yalnız ekleme: "- YYYY-AA-GG | konu | karar")\n\n' > "$P/.ekip/KARARLAR.md"
[ -f "$P/.ekip/DERSLER.md" ] || printf '# DERSLER (yalnız ekleme: "- konu: ders (kanıt dosyası)")\n\n' > "$P/.ekip/DERSLER.md"
echo "HAZIR: $K ($(grep -c '^| [0-9]' "$K/urunler.md") ürün kayıtlı)"
