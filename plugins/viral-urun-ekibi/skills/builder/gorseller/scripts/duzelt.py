"""Üretilmiş görsellere güvenli son dokunuşlar (yalnız Pillow; ChatGPT Python aracında da çalışır).
  python duzelt.py kenar  <girdi> <cikti> <oran>          # içeriği merkezden küçült, zemini köşe renginden doldur
  python duzelt.py zemin  <girdi> <cikti> <#hex>          # kenara bağlı zemini bölüm rengine boya; ürün kenara değiyorsa RED, dosya yazılmaz
  python duzelt.py logo   <girdi> <cikti> [--kern X:PX]     # kırp, isteğe bağlı harf kaydırma, tuvalin %45'ine ortala, düz renk bas
Çıkış kodu: 0 = tamam, 2 = kullanım hatası, 3 = RED (zemin: ürün kenara değiyor; çıktı yazılmadı).
"""
import re
import sys
from PIL import Image, ImageChops

def zemin(im):
    w, h = im.size
    pts = [im.getpixel(p) for p in [(4, 4), (w - 5, 4), (4, h - 5), (w - 5, h - 5)]]
    return tuple(sorted(c[i] for c in pts)[1] for i in range(3))

def kenar(src, dst, oran):
    im = Image.open(src).convert("RGB"); w, h = im.size; bg = zemin(im)
    k = im.resize((round(w * oran), round(h * oran)), Image.LANCZOS)
    out = Image.new("RGB", (w, h), bg); out.paste(k, ((w - k.width) // 2, (h - k.height) // 2)); out.save(dst, quality=92)

def logo(src, dst, kern=None, renk=(0x14, 0x30, 0x4F), zem=(0xF2, 0xEE, 0xE8), genislik=0.45, tuval=1254):
    im = Image.open(src).convert("RGB"); bg = zemin(im)
    fark = ImageChops.difference(im, Image.new("RGB", im.size, bg)).convert("L")
    maske = fark.point(lambda v: 0 if v < 18 else min(255, (v - 18) * 4))
    bb = maske.point(lambda v: 255 if v > 40 else 0).getbbox(); m = maske.crop(bb)
    if kern:  # "x:px" -> x'ten sağını px kadar sağa kaydır
        x, px = map(int, kern.split(":")); x -= bb[0]
        yeni = Image.new("L", (m.width + px, m.height), 0)
        yeni.paste(m.crop((0, 0, x, m.height)), (0, 0)); yeni.paste(m.crop((x, 0, m.width, m.height)), (x + px, 0)); m = yeni
    tw = int(tuval * genislik); m = m.resize((tw, round(m.height * tw / m.width)), Image.LANCZOS)
    out = Image.new("RGB", (tuval, tuval), zem)
    out.paste(Image.new("RGB", m.size, renk), ((tuval - m.width) // 2, (tuval - m.height) // 2), m)
    out.save(dst, quality=95)

def zemin_hile(src, dst, hexrenk, tol=26, kenar_payi=0.06):
    """Zemin hilesi: görselin kenara bağlı zemin bölgesini tam bölüm rengine boyar, geçişi yumuşatır.
    Ürün/kart görselin kenarına değiyorsa sayfada düz kutu kenarı görünür: 3 koduyla çıkar (yeniden üret)."""
    from PIL import ImageDraw, ImageFilter
    im = Image.open(src).convert("RGB"); w, h = im.size
    T = tuple(int(hexrenk.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    bg = zemin(im)
    yakin = ImageChops.difference(im, Image.new("RGB", im.size, bg)).convert("L").point(lambda v: 255 if v <= tol else 0)
    m = Image.new("L", (w + 2, h + 2), 255); m.paste(yakin, (1, 1))
    ImageDraw.floodfill(m, (0, 0), 128, thresh=0)
    bagli = m.crop((1, 1, w + 1, h + 1)).point(lambda v: 255 if v == 128 else 0)
    p = max(2, int(min(w, h) * kenar_payi))
    seritler = [bagli.crop(b) for b in [(0, 0, w, p), (0, h - p, w, h), (0, 0, p, h), (w - p, 0, w, h)]]
    dolu = sum(s.histogram()[0] for s in seritler) / sum(s.width * s.height for s in seritler)
    print(f"zemin {bg} -> {T}; kenarda zemin olmayan oran {dolu:.3f}")
    if dolu > 0.01:   # önce karar: reddedilen görsel diske yazılmaz
        print("RED: ürün/kart kenara değiyor; zemin hilesinde kutu kenarı görünür. Her kenarda >= %6 boş zeminle yeniden üret.")
        sys.exit(3)
    maske = bagli.filter(ImageFilter.GaussianBlur(3))
    Image.composite(Image.new("RGB", im.size, T), im, maske).save(dst, quality=95)

def kullanim(mesaj):
    print("HATA: " + mesaj, file=sys.stderr)
    print(__doc__.strip(), file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    ARG = {"kenar": (4, 4), "zemin": (4, 4), "logo": (3, 5)}   # alt komut dahil en az/en çok argüman
    if not a or a[0] not in ARG:
        kullanim("alt komut yok ya da bilinmiyor: %s" % (a[0] if a else "-"))
    if not ARG[a[0]][0] <= len(a) <= ARG[a[0]][1]:
        kullanim("%s için argüman sayısı yanlış" % a[0])
    if a[0] == "kenar":
        try:
            oran = float(a[3])
        except ValueError:
            kullanim("oran sayı olmalı: %s" % a[3])
        if not 0 < oran <= 1:
            kullanim("oran 0 ile 1 arasında olmalı: %s" % a[3])
        kenar(a[1], a[2], oran)
    elif a[0] == "zemin":
        if not re.fullmatch(r"#?[0-9a-fA-F]{6}", a[3]):
            kullanim("renk #rrggbb olmalı: %s" % a[3])
        zemin_hile(a[1], a[2], a[3])
    elif a[0] == "logo":
        if len(a) == 4 or (len(a) == 5 and a[3] != "--kern"):
            kullanim("logo: isteğe bağlı argüman yalnız --kern X:PX")
        logo(a[1], a[2], a[4] if len(a) == 5 else None)
