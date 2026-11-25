#!/usr/bin/env python3
""""Sonra" karesindeki ekran bölgesini "önce" karesine taşır: kadraj, plaka, arka plan "önce"den kalır, yalnız ekran değişir.

Neden: ChatGPT'ye "aynı fotoğraf, yalnız ekranı değiştir" denince kadrajı/plakayı da değiştirebiliyor (ölçüldü: 3 araçtan
2'sinde). Çözüm: "sonra" karesini üret, sonra ekran + parıltı bölgesini yumuşak dairesel maskeyle "önce" karesinin üstüne koy.
İki kare arasındaki küçük kaymayı ekranın ÇEVRESİNDEKİ halkada blok eşlemeyle bulur (ekranın içi farklı olduğu için
eşlemeye katılmaz), "sonra" karesini o kadar kaydırıp maskeler.

Maske: iç yarıçap boyunca tam "sonra"; dış yarıçap 1,45·r'de sıfır; yumuşak kenar genişliği 0,35·r.
Kayma araması: ±25 px (--arama ile değişir), önce 3 px adımlı kaba ızgara, sonra 1 px. Eşleme hatası yüksekse (kareler çok farklı) uyarı verir.

Kullanım:
  python3 ekran_tasi.py k2_once.png k3_sonra.png CX CY R k3_hizali.png
    CX, CY : ekran merkezi ("önce" karesinin pikselinde)
    R      : ekran yarıçapı (çerçeve dahil, px)
Çıkış kodu: 0 = yazıldı · 1 = eşleme hatası eşiği aştı (dosya yine yazılır, panoyla bak) · 2 = girdi hatası.
"""
import argparse
import sys

try:
    import numpy as np
    from PIL import Image
except ImportError as _hata:  # ham ImportError yerine anlaşılır mesaj, çıkış 3 (kurulum eksik)
    print("kurulum eksik: '%s' paketi bulunamadı. Kur: python3 -m pip install --user numpy pillow (Windows: py -3 -m pip install --user numpy pillow)" % (_hata.name or "numpy pillow"), file=sys.stderr)
    sys.exit(3)

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DIS, KENAR = 1.45, 0.35


def kayma_bul(A, B, cx, cy, r, arama):
    """Ekranın dışındaki halkada (1,45r–4r) ortalama mutlak farkı en küçük yapan (dx, dy)."""
    h, w = A.shape[:2]
    y0, y1 = max(0, cy - 4 * r), min(h, cy + 4 * r)
    x0, x1 = max(0, cx - 4 * r), min(w, cx + 4 * r)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    halka = np.hypot(xx - cx, yy - cy) > r * DIS
    a = A[y0:y1, x0:x1][halka]
    def fark(dx, dy):
        by0, by1, bx0, bx1 = y0 + dy, y1 + dy, x0 + dx, x1 + dx
        if by0 < 0 or bx0 < 0 or by1 > h or bx1 > w:
            return float("inf")
        return float(np.abs(a - B[by0:by1, bx0:bx1][halka]).mean())

    # kaba ızgara (3 px adım), sonra en iyinin çevresinde 1 px adım
    adim = 3
    kaba = min(((fark(dx, dy), dx, dy) for dy in range(-arama, arama + 1, adim)
                for dx in range(-arama, arama + 1, adim)), key=lambda t: t[0])
    _, kx, ky = kaba
    return min(((fark(dx, dy), dx, dy)
                for dy in range(max(-arama, ky - adim), min(arama, ky + adim) + 1)
                for dx in range(max(-arama, kx - adim), min(arama, kx + adim) + 1)), key=lambda t: t[0])


def main():
    ap = argparse.ArgumentParser(description="Sonra karesinin ekran bölgesini önce karesine taşır (kadraj sabit kalır).")
    ap.add_argument("once", help="önce karesi (k2): kadraj buradan gelir")
    ap.add_argument("sonra", help="sonra karesi (k3): yalnız ekran bölgesi alınır")
    ap.add_argument("cx", type=int, help="ekran merkezi x (px, önce karesinde)")
    ap.add_argument("cy", type=int, help="ekran merkezi y (px, önce karesinde)")
    ap.add_argument("r", type=int, help="ekran yarıçapı (px)")
    ap.add_argument("cikti", help="çıktı PNG")
    ap.add_argument("--arama", type=int, default=25, help="kayma arama aralığı ±px (varsayılan 25)")
    ap.add_argument("--esik", type=float, default=20.0, help="halka ortalama fark eşiği (0-255); üstü = uyarı, çıkış 1")
    a = ap.parse_args()

    once = Image.open(a.once).convert("RGB")
    sonra = Image.open(a.sonra).convert("RGB")
    if sonra.size != once.size:
        sonra = sonra.resize(once.size, Image.LANCZOS)
    w, h = once.size
    if a.r <= 0 or not (0 <= a.cx < w and 0 <= a.cy < h):
        print(f"HATA: merkez ({a.cx},{a.cy}) ya da yarıçap {a.r} kare dışında ({w}x{h})")
        sys.exit(2)

    A = np.asarray(once).astype(np.float32)
    B = np.asarray(sonra).astype(np.float32)
    fark, dx, dy = kayma_bul(A, B, a.cx, a.cy, a.r, a.arama)
    if fark == float("inf"):
        print("HATA: arama penceresi kare dışına taşıyor; --arama küçült")
        sys.exit(2)

    # sonra karesini kaymanın tersine kaydır: B2[y, x] = B[y + dy, x + dx]
    B2 = np.roll(np.roll(B, -dy, axis=0), -dx, axis=1)
    yy, xx = np.mgrid[0:h, 0:w]
    m = np.clip((a.r * DIS - np.hypot(xx - a.cx, yy - a.cy)) / (a.r * KENAR), 0, 1)[..., None]
    O = A * (1 - m) + B2 * m
    Image.fromarray(np.clip(O, 0, 255).astype(np.uint8)).save(a.cikti)

    print(f"kayma dx={dx} dy={dy} · halka farkı {fark:.1f} (eşik {a.esik}) · maske dış {a.r * DIS:.0f} px · {a.cikti}")
    if abs(dx) == a.arama or abs(dy) == a.arama:
        print("UYARI: kayma arama sınırında; --arama büyüt ya da kareleri kontrol et")
    if fark > a.esik:
        print("UYARI: çevre eşleşmiyor (kadraj çok farklı) — taşınan bölge yapıştırma gibi durabilir; panoyla bak")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
