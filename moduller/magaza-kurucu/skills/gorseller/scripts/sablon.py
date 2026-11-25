# -*- coding: utf-8 -*-
"""
Galeri sablonu prototipi: urun fotografi + metin JSON -> 1080x1080 PNG.

Ilke: gorsel model yalniz urunu/sahneyi uretir; TUM yazi, ikon ve duzen burada
PIL ile basilir (Turkce harf hatasi ve dogrulanmamis iddia riski sifirlanir).

Yalniz Pillow kullanir (numpy yok). Fontlar: skill icindeki ../assets/fonts
(OFL lisansli, Google Fonts). Baska klasor icin MK_FONT_DIR ortam degiskeni.

Magaza Kurucu'da ANA yontem degildir: gorsel model gorselin tamamini uretir.
Bu script yalniz yardimcidir (bozuk Turkce baslik duzeltme, kutu-icerigi /
karsilastirma gibi bilgi kartlari). Bkz. ../references/sablon-py.md

CLI:
  python sablon.py --tpl ana-fayda --urun x.png --json metin.json --out y.png [--palet acik|koyu] [--arka-plan sahne.png]
  python sablon.py --demo --urun x.jpg --outdir cikti     # 5 sablon x 2 palet
Cikis kodu: 0 = tum olcumler gecti, 2 = olcum hatasi (kontrast / min yazi / tasma),
3 = Pillow surumu eski (Pillow >= 10 gerekir: rounded_rectangle; 9.5'te ValueError ile coker).
"""
import argparse
import json
import os
import sys

try:
    import PIL
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError as _hata:  # ham ImportError yerine anlaşılır mesaj, çıkış 3 (kurulum eksik)
    print("kurulum eksik: '%s' paketi bulunamadı. Kur: python3 -m pip install --user pillow (Windows: py -3 -m pip install --user pillow)" % (_hata.name or "pillow"), file=sys.stderr)
    sys.exit(3)

PILLOW_EN_AZ = (10, 0)


def pillow_surumu(metin=None):
    """'10.4.0' -> (10, 4). Okunamazsa (0, 0)."""
    parca = (metin or getattr(PIL, "__version__", "0")).split(".")
    try:
        return tuple(int("".join(ch for ch in p if ch.isdigit()) or 0) for p in parca[:2])
    except ValueError:
        return (0, 0)


def pillow_kontrol():
    if pillow_surumu() < PILLOW_EN_AZ:
        print("HATA: sablon.py Pillow >= %d.%d ister (rounded_rectangle); bu ortamda Pillow %s var."
              % (PILLOW_EN_AZ + (PIL.__version__,)), file=sys.stderr)
        print("Cozum: pip install -U 'Pillow>=10'. Kurulamiyorsa sablon.py'yi kullanma; gorseli "
              "gorsel model uretsin (sablon.py ana yol degildir).", file=sys.stderr)
        sys.exit(3)

W = 1080           # cikti boyu
S = 2              # ic supersampling (kenar yumusatma icin 2x cizip kucultulur)
MIN_PX = 40        # 1080'de en kucuk yazi (telefonda ~360px -> ~13px)
MIN_KONTRAST = 4.5
M = 60             # kenar boslugu

BURADA = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("MK_FONT_DIR") or os.path.normpath(os.path.join(BURADA, "..", "assets", "fonts"))
FONTLAR = {
    "baslik": "Anton-Regular.ttf",       # dar/kalin buyuk harf basliklar
    "kalin": "Barlow-Bold.ttf",
    "yarikalin": "Barlow-SemiBold.ttf",
    "orta": "Barlow-Medium.ttf",
}

PALETLER = {
    "acik": dict(bg=(255, 255, 255), ink=(11, 11, 15), muted=(70, 74, 84),
                 accent=(30, 75, 210), accent_text=(30, 75, 210), on_accent=(255, 255, 255),
                 card=(243, 245, 249), line=(218, 222, 230), ok=(16, 122, 58), no=(150, 155, 165),
                 sahne=(232, 236, 243), golge=70),
    "koyu": dict(bg=(10, 10, 12), ink=(255, 255, 255), muted=(200, 204, 212),
                 accent=(37, 99, 235), accent_text=(120, 160, 255), on_accent=(255, 255, 255),
                 card=(26, 28, 34), line=(58, 62, 72), ok=(52, 199, 89), no=(120, 124, 134),
                 sahne=(150, 160, 185), golge=0),
}


# ---------------------------------------------------------------- yardimcilar
def s(v):
    return int(round(v * S))


def tr_upper(t):
    """Turkce buyuk harf: i->I-noktali, i-noktasiz->I. Python .upper() 'i'yi 'I' yapar (yanlis)."""
    return t.replace("i", "İ").replace("ı", "I").upper()


_font_cache = {}


def font(rol, px):
    key = (rol, px)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, FONTLAR[rol]), s(px))
    return _font_cache[key]


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminans(rgb):
    r, g, b = rgb[:3]
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def kontrast(a, b):
    la, lb = luminans(a), luminans(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


class Tuval:
    """2x tuval + olcum gunlugu. Her yazi cizilmeden once arkasindaki zemin orneklenir."""

    def __init__(self, pal, arka_plan=None):
        self.pal = pal
        self.im = Image.new("RGB", (s(W), s(W)), pal["bg"])
        if arka_plan:
            sc = Image.open(arka_plan).convert("RGB")
            r = max(s(W) / sc.width, s(W) / sc.height)
            sc = sc.resize((int(sc.width * r + 1), int(sc.height * r + 1)), Image.LANCZOS)
            l, t = (sc.width - s(W)) // 2, (sc.height - s(W)) // 2
            self.im.paste(sc.crop((l, t, l + s(W), t + s(W))))
        self.sahne_var = bool(arka_plan)
        self.d = ImageDraw.Draw(self.im)
        self.olcum = []
        self.uyarilar = []

    # -- yazi
    def yazi(self, xy, metin, rol, px, renk, anchor="la"):
        f = font(rol, px)
        x, y = s(xy[0]), s(xy[1])
        bb = self.d.textbbox((x, y), metin, font=f, anchor=anchor)
        k = self._zemin_kontrast(bb, renk)
        self.olcum.append(dict(metin=metin, px=px, kontrast=round(k, 2),
                               gecti=bool(px >= MIN_PX and k >= MIN_KONTRAST)))
        self.d.text((x, y), metin, font=f, fill=renk, anchor=anchor)
        return [v / S for v in bb]

    def _zemin_kontrast(self, bb, renk):
        x0, y0, x1, y1 = [max(0, min(s(W), int(v))) for v in bb]
        if x1 <= x0 or y1 <= y0:
            return 21.0
        reg = self.im.crop((x0, y0, x1, y1)).resize((max(1, (x1 - x0) // 4), max(1, (y1 - y0) // 4)))
        bts = reg.convert("RGB").tobytes()
        lums = sorted(luminans(bts[i:i + 3]) for i in range(0, len(bts), 3))
        # en kotu durum: zeminin %5 ve %95 dilimine karsi kontrast
        lo, hi = lums[int(len(lums) * 0.05)], lums[min(len(lums) - 1, int(len(lums) * 0.95))]
        lt = luminans(renk)
        return min((max(lt, z) + 0.05) / (min(lt, z) + 0.05) for z in (lo, hi))

    def sonuc(self):
        return self.im.resize((W, W), Image.LANCZOS)


# ---------------------------------------------------------------- metin sigdirma
def sar(metin, rol, px, max_w):
    f = font(rol, px)
    satirlar, cur = [], ""
    for k in metin.split():
        aday = (cur + " " + k).strip()
        if f.getlength(aday) <= s(max_w):
            cur = aday
        else:
            if cur:
                satirlar.append(cur)
            cur = k
    if cur:
        satirlar.append(cur)
    tasti = any(f.getlength(l) > s(max_w) for l in satirlar)
    return satirlar, tasti


def sigdir(metin, rol, max_px, min_px, max_w, max_satir):
    for px in range(max_px, min_px - 1, -2):
        satirlar, tasti = sar(metin, rol, px, max_w)
        if len(satirlar) <= max_satir and not tasti:
            return px, satirlar, True
    satirlar, _ = sar(metin, rol, min_px, max_w)
    return min_px, satirlar, False


SATIR_ARALIK = {"baslik": 1.16, "kalin": 1.18, "yarikalin": 1.18, "orta": 1.2}


def blok(tv, metin, rol, max_px, max_w, max_satir, x, y, renk, hiza="sol", min_px=MIN_PX):
    """Metni kutuya sigdirip ciz; alt y'yi doner. Sigmazsa uyari kaydeder."""
    px, satirlar, ok = sigdir(metin, rol, max_px, min_px, max_w, max_satir)
    if not ok:
        tv.uyarilar.append("SIGMADI (%s): '%s' -> metni kisalt" % (rol, metin))
        tv.olcum.append(dict(metin=metin, px=px, kontrast=0, gecti=False, not_="tasma"))
    adim = px * SATIR_ARALIK[rol]
    asc = font(rol, px).getmetrics()[0] / S
    for i, l in enumerate(satirlar):
        by = y + asc + i * adim
        if hiza == "orta":
            tv.yazi((x, by), l, rol, px, renk, anchor="ms")
        elif hiza == "sag":
            tv.yazi((x, by), l, rol, px, renk, anchor="rs")
        else:
            tv.yazi((x, by), l, rol, px, renk, anchor="ls")
    return y + asc + (len(satirlar) - 1) * adim + font(rol, px).getmetrics()[1] / S


def basliklar(tv, t, y=64, genislik=W - 2 * M, x=M, hiza="sol"):
    pal = tv.pal
    if t.get("ust_baslik"):
        y = blok(tv, t["ust_baslik"], "yarikalin", 44, genislik, 1, x, y, pal["accent_text"], hiza) + 8
    b = t.get("baslik", "")
    if len(b.split()) > 6:
        tv.uyarilar.append("Baslik 6 kelimeyi asiyor: '%s'" % b)
    return blok(tv, tr_upper(b), "baslik", 104, genislik, 2, x, y, pal["ink"], hiza, min_px=64)


# ---------------------------------------------------------------- urun
def urun_hazirla(yol, esik=240, buyuk_bosluk=0.004):
    """Beyaz zeminli JPG'den saydam PNG. Seffaflik zaten varsa dokunmaz.
    1) kenara bagli beyaz bolge, 2) urun icindeki BUYUK kapali beyaz bosluklar (kulp ici)
    saydam olur; kucuk beyaz parcalar (LED, logo) korunur. Beyaz urunde basarisiz olur."""
    im = Image.open(yol)
    if im.mode in ("RGBA", "LA") and im.getextrema()[-1][0] < 250:
        return im.convert("RGBA").crop(im.getbbox())
    from PIL import ImageChops
    im = im.convert("RGB")
    r, g, b = im.split()
    # min kanal >= esik -> beyaz say
    minch = ImageChops.darker(ImageChops.darker(r, g), b)
    beyaz = minch.point(lambda v: 255 if v >= esik else 0)
    # kucuk kopyada bilesen analizi
    oran = 400.0 / max(im.size)
    kw, kh = max(1, int(im.width * oran)), max(1, int(im.height * oran))
    k = beyaz.resize((kw, kh), Image.NEAREST)
    k = Image.eval(k, lambda v: 255 if v > 127 else 0)
    pad = Image.new("L", (kw + 2, kh + 2), 255)
    pad.paste(k, (1, 1))
    ImageDraw.floodfill(pad, (0, 0), 128)
    zemin = pad.point(lambda v: 255 if v == 128 else 0)
    # kalan beyaz bilesenler
    px = pad.load()
    etiket = 1
    for yy in range(kh + 2):
        for xx in range(kw + 2):
            if px[xx, yy] == 255:
                ImageDraw.floodfill(pad, (xx, yy), etiket)
                hist = pad.histogram()
                if hist[etiket] >= buyuk_bosluk * kw * kh:
                    zemin.paste(255, mask=pad.point(lambda v, e=etiket: 255 if v == e else 0))
                etiket = etiket + 1 if etiket < 120 else 1
    zemin = zemin.crop((1, 1, kw + 1, kh + 1)).filter(ImageFilter.MaxFilter(3))
    zemin = zemin.resize(im.size, Image.NEAREST)
    zemin = ImageChops.multiply(zemin, beyaz)   # yalniz gercekten beyaz pikseller
    alfa = ImageChops.invert(zemin).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert("RGBA")
    out.putalpha(alfa)
    return out.crop(alfa.point(lambda v: 255 if v > 10 else 0).getbbox())


def urun_yerlestir(tv, urun, kutu, isik=True, golge=True):
    """Urunu kutuya (1080 birim) sigdir, ortala; koyu palette arkaya isik halesi."""
    x0, y0, x1, y1 = kutu
    bw, bh = s(x1 - x0), s(y1 - y0)
    r = min(bw / urun.width, bh / urun.height)
    u = urun.resize((max(1, int(urun.width * r)), max(1, int(urun.height * r))), Image.LANCZOS)
    px = s(x0) + (bw - u.width) // 2
    py = s(y0) + (bh - u.height) // 2
    pal = tv.pal
    if isik and not tv.sahne_var and pal["golge"] == 0:
        # koyu palet: koyu urun zeminde kaybolmasin diye arkada yumusak isik halesi
        rr = int(max(u.width, u.height) * 0.80)
        g = Image.new("L", (96, 96), 0)
        ImageDraw.Draw(g).ellipse((28, 28, 68, 68), fill=230)
        g = g.filter(ImageFilter.GaussianBlur(9)).resize((2 * rr, 2 * rr), Image.BICUBIC)
        cx, cy = px + u.width // 2, py + u.height // 2
        tv.im.paste(Image.new("RGB", g.size, pal["sahne"]), (cx - rr, cy - rr), g)
    if golge and pal["golge"]:
        sw, sh = int(u.width * 0.7), max(4, int(u.width * 0.07))
        sg = Image.new("L", (sw + 80, sh + 80), 0)
        ImageDraw.Draw(sg).ellipse((40, 40, 40 + sw, 40 + sh), fill=pal["golge"])
        sg = sg.filter(ImageFilter.GaussianBlur(14))
        tv.im.paste((0, 0, 0), (px + (u.width - sw) // 2 - 40, py + u.height - sh // 2 - 40), sg)
    tv.im.paste(u, (px, py), u)
    return [px / S, py / S, (px + u.width) / S, (py + u.height) / S]


# ---------------------------------------------------------------- ikonlar (kodla cizilir)
def ikon(tv, ad, merkez, boy, renk):
    """Cizgi ikon. 4x katmanda cizilir, kucultulur. Bilinmeyen ad -> 'nokta'."""
    K = 4 * S
    n = int(boy * K)
    lay = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    w = max(2, int(n * 0.075))
    c = tuple(renk) + (255,)
    P = lambda *xy: [(int(a * n), int(b * n)) for a, b in zip(xy[0::2], xy[1::2])]

    def poly(pts):
        d.line(pts + [pts[0]], fill=c, width=w, joint="curve")
        for p in pts:
            d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=c)

    def oval(a, b, cc, e):
        d.ellipse((int(a * n), int(b * n), int(cc * n), int(e * n)), outline=c, width=w)

    if ad == "sicaklik":
        d.rounded_rectangle((int(.40 * n), int(.08 * n), int(.60 * n), int(.62 * n)), radius=int(.1 * n), outline=c, width=w)
        oval(.30, .56, .70, .94)
        d.ellipse((int(.40 * n), int(.66 * n), int(.60 * n), int(.84 * n)), fill=c)
        d.line(P(.5, .30, .5, .70), fill=c, width=w)
        for yy in (.2, .32, .44):
            d.line(P(.66, yy, .78, yy), fill=c, width=w)
    elif ad == "sarj":
        poly(P(.56, .06, .22, .56, .48, .56, .40, .94, .78, .42, .52, .42, .62, .06))
    elif ad == "saat":
        oval(.10, .10, .90, .90)
        d.line(P(.5, .5, .5, .24), fill=c, width=w)
        d.line(P(.5, .5, .68, .62), fill=c, width=w)
    elif ad == "kalkan":
        poly(P(.5, .06, .86, .2, .82, .56, .5, .94, .18, .56, .14, .2))
        d.line(P(.34, .5, .46, .62, .68, .38), fill=c, width=w, joint="curve")
    elif ad == "damla":
        d.arc((int(.22 * n), int(.36 * n), int(.78 * n), int(.92 * n)), 150, 390, fill=c, width=w)
        d.line(P(.26, .52, .5, .06, .74, .52), fill=c, width=w, joint="curve")
    elif ad == "yaprak":
        poly(P(.16, .84, .2, .44, .44, .18, .86, .14, .8, .56, .56, .8))
        d.line(P(.16, .84, .62, .38), fill=c, width=w)
    elif ad == "kupa":
        d.rectangle((int(.14 * n), int(.22 * n), int(.66 * n), int(.86 * n)), outline=c, width=w)
        d.arc((int(.54 * n), int(.36 * n), int(.90 * n), int(.70 * n)), -90, 90, fill=c, width=w)
    elif ad == "kutu":
        poly(P(.5, .08, .9, .28, .9, .74, .5, .94, .1, .74, .1, .28))
        d.line(P(.1, .28, .5, .48, .9, .28), fill=c, width=w, joint="curve")
        d.line(P(.5, .48, .5, .94), fill=c, width=w)
    elif ad == "altlik":
        oval(.08, .50, .92, .84)
        oval(.30, .58, .70, .74)
        d.line(P(.5, .16, .5, .42), fill=c, width=w)
        d.line(P(.38, .30, .5, .16, .62, .30), fill=c, width=w, joint="curve")
    elif ad == "kablo":
        d.rounded_rectangle((int(.34 * n), int(.06 * n), int(.66 * n), int(.40 * n)), radius=int(.06 * n), outline=c, width=w)
        d.line(P(.44, .06, .44, .0), fill=c, width=w)
        d.line(P(.56, .06, .56, .0), fill=c, width=w)
        d.line(P(.5, .40, .5, .62), fill=c, width=w)
        d.arc((int(.2 * n), int(.5 * n), int(.8 * n), int(1.1 * n)), 180, 270, fill=c, width=w)
    elif ad == "telefon":
        d.rounded_rectangle((int(.28 * n), int(.06 * n), int(.72 * n), int(.94 * n)), radius=int(.08 * n), outline=c, width=w)
        d.line(P(.44, .82, .56, .82), fill=c, width=w)
    elif ad == "kitapcik":
        poly(P(.14, .14, .5, .22, .86, .14, .86, .84, .5, .92, .14, .84))
        d.line(P(.5, .22, .5, .92), fill=c, width=w)
    elif ad == "tik":
        d.line(P(.2, .52, .42, .74, .82, .3), fill=c, width=int(w * 1.6), joint="curve")
    elif ad == "carpi":
        d.line(P(.26, .26, .74, .74), fill=c, width=int(w * 1.6))
        d.line(P(.74, .26, .26, .74), fill=c, width=int(w * 1.6))
    else:
        oval(.2, .2, .8, .8)
        d.ellipse((int(.42 * n), int(.42 * n), int(.58 * n), int(.58 * n)), fill=c)
    lay = lay.resize((s(boy), s(boy)), Image.LANCZOS)
    tv.im.paste(lay, (s(merkez[0] - boy / 2), s(merkez[1] - boy / 2)), lay)


IKON_LISTESI = ["sicaklik", "sarj", "saat", "kalkan", "damla", "yaprak", "kupa", "kutu",
                "altlik", "kablo", "telefon", "kitapcik", "tik", "carpi"]


def daire(tv, merkez, cap, renk):
    cx, cy, r = s(merkez[0]), s(merkez[1]), s(cap / 2)
    tv.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=renk)


def scrim(tv, y0, y1, yukari=True):
    """Sahne gorseli uzerinde yazi icin palet zemini -> saydam gecis."""
    if not tv.sahne_var:
        return
    h = s(y1 - y0)
    m = Image.linear_gradient("L").resize((s(W), h))
    if yukari:
        m = Image.eval(m, lambda v: 255 - v)
    m = m.point(lambda v: min(255, int(v * 1.15)))
    tv.im.paste(Image.new("RGB", (s(W), h), tv.pal["bg"]), (0, s(y0)), m)


# ---------------------------------------------------------------- sablonlar
def t_hero_temiz(tv, urun, t):
    # Google Merchant: yazi/logo/filigran yok; urun kareyi ~%75-90 doldurur
    hedef = 0.82
    pay = W * (1 - hedef) / 2
    bb = urun_yerlestir(tv, urun, (pay, pay, W - pay, W - pay))
    kap = max(bb[2] - bb[0], bb[3] - bb[1]) / W
    tv.olcum.append(dict(metin="(urun kaplama)", px=0, kontrast=0, kaplama=round(kap, 3),
                         gecti=bool(0.75 <= kap <= 0.90)))


def t_ana_fayda(tv, urun, t):
    pal = tv.pal
    scrim(tv, 0, 420, True)
    scrim(tv, 760, W, False)
    alt = basliklar(tv, t)
    fay = t.get("faydalar", [])[:3]
    zone_top = W - M - 214
    urun_yerlestir(tv, urun, (M + 60, alt + 16, W - M - 60, zone_top - 16))
    kol = (W - 2 * M) / max(1, len(fay))
    for i, f in enumerate(fay):
        cx = M + kol * i + kol / 2
        ikon(tv, f.get("ikon", ""), (cx, zone_top + 44), 84, pal["ink"])
        blok(tv, f["metin"], "kalin", 44, kol - 36, 2, cx, zone_top + 100, pal["ink"], "orta")
        if i:
            x = s(M + kol * i)
            tv.d.line((x, s(zone_top + 10), x, s(W - M - 10)), fill=pal["accent"], width=s(3))


def t_nasil_kullanilir(tv, urun, t):
    pal = tv.pal
    scrim(tv, 0, 400, True)
    alt = basliklar(tv, t)
    adim = t.get("adimlar", [])[:3]
    urun_yerlestir(tv, urun, (M - 20, alt + 40, 470, W - M))
    x_txt, top, bot = 600, alt + 50, W - M
    h = (bot - top) / max(1, len(adim))
    cap = 86
    merkezler = [(530, top + h * i + h / 2) for i in range(len(adim))]
    if len(merkezler) > 1:
        tv.d.line((s(530), s(merkezler[0][1]), s(530), s(merkezler[-1][1])), fill=pal["line"], width=s(4))
    for i, (a, m) in enumerate(zip(adim, merkezler)):
        daire(tv, m, cap, pal["accent"])
        tv.yazi((m[0], m[1] + 2), str(i + 1), "baslik", 54, pal["on_accent"], anchor="mm")
        # metni daire merkezine dikey hizala
        px, satir, _ = sigdir(a, "kalin", 46, MIN_PX, W - M - x_txt, 3)
        yuk = px * SATIR_ARALIK["kalin"] * len(satir)
        blok(tv, a, "kalin", 46, W - M - x_txt, 3, x_txt, m[1] - yuk / 2 - 4, pal["ink"])


def t_karsilastirma(tv, urun, t):
    pal = tv.pal
    scrim(tv, 0, 420, True)
    alt = basliklar(tv, t)
    satir = t.get("satirlar", [])[:4]
    c_biz, c_on = (590, 800), (820, 1030)
    top = alt + 30
    # vurgulu "biz" kolonu
    tv.d.rounded_rectangle((s(c_biz[0]), s(top), s(c_biz[1]), s(W - M + 10)), radius=s(28),
                           fill=pal["card"], outline=pal["accent"], width=s(5))
    urun_yerlestir(tv, urun, (c_biz[0] + 30, top + 18, c_biz[1] - 30, top + 170), isik=False, golge=False)
    head_y = top + 182
    e1 = blok(tv, t.get("biz", "Bu ürün"), "kalin", 42, c_biz[1] - c_biz[0] - 24, 2,
              sum(c_biz) / 2, head_y, pal["ink"], "orta")
    e2 = blok(tv, t.get("onlar", "Sıradan"), "kalin", 42, c_on[1] - c_on[0] - 10, 2,
              sum(c_on) / 2, head_y, pal["muted"], "orta")
    rtop = max(e1, e2) + 24
    rh = (W - M - rtop) / max(1, len(satir))
    for i, r in enumerate(satir):
        y0 = rtop + rh * i
        cy = y0 + rh / 2
        if i:
            tv.d.line((s(M), s(y0), s(c_biz[0] - 10), s(y0)), fill=pal["line"], width=s(2))
            tv.d.line((s(c_on[0] + 10), s(y0), s(c_on[1]), s(y0)), fill=pal["line"], width=s(2))
        px, sl, _ = sigdir(r["ozellik"], "yarikalin", 44, MIN_PX, c_biz[0] - M - 24, 2)
        yuk = px * SATIR_ARALIK["yarikalin"] * len(sl)
        blok(tv, r["ozellik"], "yarikalin", 44, c_biz[0] - M - 24, 2, M, cy - yuk / 2 - 4, pal["ink"])
        for col, val in ((c_biz, r.get("biz")), (c_on, r.get("onlar"))):
            m = (sum(col) / 2, cy)
            if val:
                daire(tv, m, 66, pal["ok"])
                ikon(tv, "tik", m, 46, (255, 255, 255))
            else:
                daire(tv, m, 66, pal["no"])
                ikon(tv, "carpi", m, 40, (255, 255, 255))


def t_kutu_icerigi(tv, urun, t):
    pal = tv.pal
    scrim(tv, 0, 400, True)
    alt = basliklar(tv, t, hiza="orta", x=W / 2)
    parca = t.get("parcalar", [])[:4]
    rh = 104
    list_top = W - M + 6 - rh * len(parca)
    etk = t.get("etiketler", [])
    yan = 270 if etk else 150
    bb = urun_yerlestir(tv, urun, (yan, alt + 24, W - yan, list_top - 24))
    for e in etk:
        px_ = bb[0] + (bb[2] - bb[0]) * e["x"]
        py_ = bb[1] + (bb[3] - bb[1]) * e["y"]
        sol = e["x"] < 0.5
        tx = M if sol else W - M
        f = font("kalin", 40)
        tw = f.getlength(e["metin"]) / S
        pill = (tx, py_ - 32, tx + tw + 40, py_ + 32) if sol else (tx - tw - 40, py_ - 32, tx, py_ + 32)
        ux = pill[2] if sol else pill[0]
        tv.d.line((s(ux), s(py_), s(px_), s(py_)), fill=pal["accent"], width=s(4))
        tv.d.rounded_rectangle(tuple(s(v) for v in pill), radius=s(32), fill=pal["accent"])
        tv.yazi(((pill[0] + pill[2]) / 2, py_ + 1), e["metin"], "kalin", 40, pal["on_accent"], anchor="mm")
        daire(tv, (px_, py_), 26, pal["on_accent"])
        daire(tv, (px_, py_), 16, pal["accent"])
    for i, p in enumerate(parca):
        y0 = list_top + rh * i
        cy = y0 + rh / 2
        tv.d.line((s(M), s(y0), s(W - M), s(y0)), fill=pal["line"], width=s(2))
        ikon(tv, p.get("ikon", ""), (M + 38, cy), 64, pal["ink"])
        tv.yazi((M + 100, cy), p["ad"], "kalin", 48, pal["ink"], anchor="lm")
        if p.get("adet"):
            tv.yazi((W - M, cy), p["adet"], "yarikalin", 44, pal["accent_text"], anchor="rm")


SABLONLAR = {
    "hero-temiz": t_hero_temiz,
    "ana-fayda": t_ana_fayda,
    "nasil-kullanilir": t_nasil_kullanilir,
    "karsilastirma": t_karsilastirma,
    "kutu-icerigi": t_kutu_icerigi,
}


def render_slot(template, product_png, texts, palette="acik", arka_plan=None, urun_img=None):
    """template: SABLONLAR anahtari; product_png: yol (urun_img verilirse o kullanilir);
    texts: dict; palette: 'acik'|'koyu' ya da renk dict'i. Doner: (PIL.Image 1080x1080, rapor dict)."""
    if pillow_surumu() < PILLOW_EN_AZ:
        raise RuntimeError("sablon.py Pillow >= 10 ister; bu ortamda %s var" % PIL.__version__)
    pal = PALETLER[palette] if isinstance(palette, str) else palette
    urun = urun_img if urun_img is not None else urun_hazirla(product_png)
    tv = Tuval(pal, arka_plan)
    SABLONLAR[template](tv, urun, texts or {})
    im = tv.sonuc()
    rapor = dict(sablon=template, olcum=tv.olcum, uyarilar=tv.uyarilar,
                 gecti=all(o["gecti"] for o in tv.olcum) and not tv.uyarilar)
    return im, rapor


# ---------------------------------------------------------------- CLI
DEMO = {
    "hero-temiz": {},
    "ana-fayda": {"ust_baslik": "Akıllı ısı kontrolü", "baslik": "Kahveniz hep doğru sıcaklıkta",
                  "faydalar": [{"ikon": "sicaklik", "metin": "Sıcaklığı sen seç"},
                               {"ikon": "sarj", "metin": "Şarj altlığıyla gün boyu"},
                               {"ikon": "telefon", "metin": "Uygulamadan ayarla"}]},
    "nasil-kullanilir": {"baslik": "Üç adımda hazır",
                         "adimlar": ["Kahveni kupaya dök", "Uygulamadan ısıyı seç",
                                     "Altlığa koy, ılık kalsın"]},
    "karsilastirma": {"baslik": "Neden bu kupa?", "biz": "Bu kupa", "onlar": "Sıradan kupa",
                      "satirlar": [{"ozellik": "Ayarlanabilir ısı", "biz": True, "onlar": False},
                                   {"ozellik": "Şarj altlığı", "biz": True, "onlar": False},
                                   {"ozellik": "Uygulama kontrolü", "biz": True, "onlar": False},
                                   {"ozellik": "Bulaşık makinesi", "biz": False, "onlar": True}]},
    "kutu-icerigi": {"baslik": "Kutuda ne var?",
                     "parcalar": [{"ikon": "kupa", "ad": "Isıtmalı kupa", "adet": "1 adet"},
                                  {"ikon": "altlik", "ad": "Şarj altlığı", "adet": "1 adet"},
                                  {"ikon": "kitapcik", "ad": "Türkçe kılavuz", "adet": "1 adet"}],
                     "etiketler": [{"metin": "Gövde", "x": 0.25, "y": 0.35},
                                   {"metin": "Işık göstergesi", "x": 0.68, "y": 0.87}]},
}


def main():
    pillow_kontrol()
    ap = argparse.ArgumentParser()
    ap.add_argument("--tpl", choices=list(SABLONLAR))
    ap.add_argument("--urun", required=True)
    ap.add_argument("--json")
    ap.add_argument("--out")
    ap.add_argument("--palet", default="acik", choices=list(PALETLER))
    ap.add_argument("--arka-plan")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--outdir", default="cikti")   # calisma klasorune (skill klasoru salt-okunur olabilir)
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    urun = urun_hazirla(a.urun)
    isler = []
    if a.demo:
        os.makedirs(a.outdir, exist_ok=True)
        for tpl, metin in DEMO.items():
            for pal in PALETLER:
                isler.append((tpl, metin, pal, os.path.join(a.outdir, "%s_%s.png" % (tpl, pal))))
    else:
        if not (a.tpl and a.out):
            ap.error("--tpl ve --out gerekli (ya da --demo)")
        metin = json.load(open(a.json, encoding="utf-8")) if a.json else {}
        isler.append((a.tpl, metin, a.palet, a.out))
    hepsi_gecti, raporlar = True, []
    for tpl, metin, pal, out in isler:
        im, r = render_slot(tpl, None, metin, pal, a.arka_plan, urun_img=urun)
        im.save(out, optimize=True)
        r["dosya"] = out
        r["palet"] = pal
        raporlar.append(r)
        en_kucuk = min([o["px"] for o in r["olcum"] if o["px"]] or [0])
        en_dusuk = min([o["kontrast"] for o in r["olcum"] if o["px"]] or [0])
        print("%-18s %-5s gecti=%s  min_px=%s  min_kontrast=%s  %s" % (
            tpl, pal, r["gecti"], en_kucuk, en_dusuk, "; ".join(r["uyarilar"])))
        for o in r["olcum"]:
            if not o["gecti"]:
                print("    KALDI:", o)
        hepsi_gecti &= r["gecti"]
    with open(os.path.splitext(isler[-1][3])[0] + ".olcum.json" if not a.demo
              else os.path.join(a.outdir, "_olcum.json"), "w", encoding="utf-8") as fh:
        json.dump(raporlar, fh, ensure_ascii=False, indent=1)
    sys.exit(0 if hepsi_gecti else 2)


if __name__ == "__main__":
    main()
