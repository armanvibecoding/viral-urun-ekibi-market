#!/usr/bin/env python3
"""Ortak yardımcılar: ffmpeg bulma, medya ölçümü, font seçimi, pazar okuma, yazı katmanı (PNG).

Çapraz platform (macOS / Windows / Linux). Bağımlılık: Python 3.8+, Pillow (yazı ve pano için).
ffmpeg bulma sırası: PATH (shutil.which) -> imageio_ffmpeg paketi -> kurulum talimatıyla çıkış.
Doğrudan çalıştırılırsa ortam raporu verir:  python3 ffaraclar.py [--font-test cikti.png]
"""
import json
import os
import re
import shutil
import subprocess
import sys

for _akis in (sys.stdout, sys.stderr):  # Windows konsolunda Türkçe karakter hatasını önle
    try:
        _akis.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

W, H = 1080, 1920
TR_TEST = "çğıİöşü ÇĞÖŞÜ"


def kurulum_talimati():
    if sys.platform == "darwin":
        return "brew install ffmpeg   (ya da: python3 -m pip install imageio-ffmpeg)"
    if os.name == "nt":
        return "winget install Gyan.FFmpeg   (ya da: py -3 -m pip install imageio-ffmpeg)"
    return "sudo apt install ffmpeg   (ya da: python3 -m pip install imageio-ffmpeg)"


_FF = None


def ffmpeg_bul():
    global _FF
    if _FF:
        return _FF
    yol = shutil.which("ffmpeg")
    if not yol:
        try:
            import imageio_ffmpeg
            yol = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            yol = None
    if not yol:
        sys.exit("ffmpeg bulunamadı. Kur: " + kurulum_talimati())
    _FF = yol
    return yol


def ffprobe_bul():
    yol = shutil.which("ffprobe")
    if yol:
        return yol
    ff = ffmpeg_bul()
    aday = os.path.join(os.path.dirname(ff), "ffprobe" + (".exe" if os.name == "nt" else ""))
    return aday if os.path.exists(aday) else None


def calistir(cmd, yakala=False):
    """Komutu çalıştırır; hata olursa stderr kuyruğunu gösterip çıkar."""
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        kuyruk = r.stderr.decode("utf-8", "replace")[-1500:]
        sys.exit(f"ffmpeg hatası (kod {r.returncode}):\n{kuyruk}")
    return r if yakala else None


def medya_bilgi(yol):
    """{'sure': sn, 'w': px, 'h': px, 'ses': bool, 'fps': float}. ffprobe yoksa `ffmpeg -i` çıktısından okur."""
    if not os.path.exists(yol):
        sys.exit(f"dosya yok: {yol}")
    fp = ffprobe_bul()
    if fp:
        r = subprocess.run([fp, "-v", "error", "-show_streams", "-show_format", "-of", "json", yol],
                           capture_output=True)
        j = json.loads(r.stdout.decode("utf-8", "replace") or "{}")
        v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), {})
        a = any(s.get("codec_type") == "audio" for s in j.get("streams", []))
        fr = v.get("avg_frame_rate", "0/1").split("/")
        fps = float(fr[0]) / float(fr[1]) if len(fr) == 2 and float(fr[1]) else 0.0
        return {"sure": float(j.get("format", {}).get("duration", 0) or 0), "w": int(v.get("width", 0)),
                "h": int(v.get("height", 0)), "ses": a, "fps": fps}
    r = subprocess.run([ffmpeg_bul(), "-hide_banner", "-i", yol], capture_output=True)
    t = r.stderr.decode("utf-8", "replace")
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", t)
    sure = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0
    v = re.search(r"Stream #.*Video:.*?(\d{2,5})x(\d{2,5})", t)
    f = re.search(r"([\d.]+) fps", t)
    return {"sure": sure, "w": int(v.group(1)) if v else 0, "h": int(v.group(2)) if v else 0,
            "ses": bool(re.search(r"Stream #.*Audio:", t)), "fps": float(f.group(1)) if f else 0.0}


def lufs_olc(yol):
    r = subprocess.run([ffmpeg_bul(), "-hide_banner", "-nostats", "-i", yol, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True)
    bul = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr.decode("utf-8", "replace"))
    return float(bul[-1]) if bul else -70.0


# ---------------- pazar ve metin ----------------

def pazar_oku(proje_kok="."):
    """`.ekip/KARARLAR.md` içindeki SON '| pazar |' satırından 'TR' ya da 'ABD' döndürür; yoksa None."""
    yol = os.path.join(proje_kok, ".ekip", "KARARLAR.md")
    if not os.path.exists(yol):
        return None
    son = None
    with open(yol, encoding="utf-8") as f:
        for satir in f:
            p = [x.strip() for x in satir.split("|")]
            if len(p) >= 3 and p[1].lower() == "pazar":
                son = p[2]
    if not son:
        return None
    k = son.lower()
    if "türk" in k or k.startswith("tr"):
        return "TR"
    return "ABD"  # yurt dışı: İngilizce


def tr_buyuk(s):
    """Türkçe doğru büyük harf (upper() 'i'yi 'I' yapar; burada 'İ' olur)."""
    return s.replace("i", "İ").replace("ı", "I").upper()


def cta_metni(kelime, pazar):
    if pazar == "TR":
        return f'Yorumlara "{kelime}" yaz, linki DM\'den atayım'
    return f'Comment "{kelime}" and I\'ll DM you the link'


_EMOJI = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\uFE0F\u200D\u2B50\u2B06\u2194-\u21AA]")


def emoji_temizle(s):
    """Videodaki yazıdan emojiyi çıkarır (fontlar emojiyi kutucuk çizer). (temiz_metin, çıkarıldı_mı)."""
    t = _EMOJI.sub("", s)
    t = re.sub(r"[ \t]{2,}", " ", t).strip()
    return t, t != s.strip()


# ---------------- font ----------------

def _aday_fontlar():
    l = []
    if sys.platform == "darwin":
        for d in ("/System/Library/Fonts/Supplemental", "/Library/Fonts"):
            l += [os.path.join(d, a) for a in ("Arial Bold.ttf", "Arial Black.ttf", "Verdana Bold.ttf", "Arial Unicode.ttf")]
    elif os.name == "nt":
        d = os.path.join(os.environ.get("WINDIR", os.environ.get("SystemRoot", "")), "Fonts")
        l += [os.path.join(d, a) for a in ("arialbd.ttf", "ariblk.ttf", "seguisb.ttf", "verdanab.ttf", "segoeuib.ttf")]
    else:
        l += ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
              "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"]
    if shutil.which("fc-list"):  # fontconfig: Türkçe karakter kümesini destekleyen kalın fontlar
        r = subprocess.run(["fc-list", ":style=Bold:charset=11e 11f 130 131 15e 15f", "file"], capture_output=True)
        l += [x.strip().rstrip(":") for x in r.stdout.decode("utf-8", "replace").splitlines() if x.strip()]
    return [x for x in l if x and os.path.exists(x)]


def turkce_destekli(font_yolu):
    """Her Türkçe harfi, kesin olmayan bir glifle (U+E000) karşılaştırır; aynı çiziliyorsa harf fontta yok."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return True  # ölçülemedi; font testi karesine gözle bakılır
    try:
        f = ImageFont.truetype(font_yolu, 48)
    except Exception:
        return False

    def ciz(ch):
        im = Image.new("L", (80, 80), 0)
        ImageDraw.Draw(im).text((10, 5), ch, font=f, fill=255)
        return im.tobytes()
    yok = ciz("\ue000")
    return all(ciz(ch) != yok for ch in "çğıİöşüÇĞÖŞÜ")


def font_bul(tercih=None):
    if tercih:
        if not os.path.exists(tercih):
            sys.exit(f"font yok: {tercih}")
        if not turkce_destekli(tercih):
            sys.exit(f"font Türkçe harfleri (çğıİöşü) içermiyor: {tercih}")
        return tercih
    for y in _aday_fontlar():
        if turkce_destekli(y):
            return y
    sys.exit("Türkçe destekli kalın font bulunamadı; --font ile bir .ttf ver (ör. Arial Bold, DejaVu Sans Bold).")


# ---------------- yazı katmanı ----------------

def _pil():
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
        return Image, ImageDraw, ImageFilter, ImageFont
    except ImportError:
        sys.exit("Pillow gerekli. Kur: python3 -m pip install pillow   (Windows: py -3 -m pip install pillow)")


def satirlara_bol(metin, font, max_gen):
    """' / ' elle satır sonu; uzun satır kelimeden kaydırılır."""
    satirlar = []
    for parca in metin.split(" / "):
        kel, cur = parca.split(), ""
        for k in kel:
            dene = (cur + " " + k).strip()
            if font.getlength(dene) <= max_gen or not cur:
                cur = dene
            else:
                satirlar.append(cur)
                cur = k
        if cur:
            satirlar.append(cur)
    return satirlar


def yazi_blogu(metin, font_yolu, boyut, max_gen=900):
    """Saydam RGBA blok döndürür (ortalanmış satırlar, siyah kontur, hafif gölge)."""
    Image, ImageDraw, ImageFilter, ImageFont = _pil()
    f = ImageFont.truetype(font_yolu, boyut)
    satirlar = satirlara_bol(metin, f, max_gen)
    kontur = max(3, boyut // 12)
    ara = int(boyut * 0.18)
    yuk = [f.getbbox(s, stroke_width=kontur) for s in satirlar]
    sat_h = max(b[3] - b[1] for b in yuk) if yuk else boyut
    bh = len(satirlar) * sat_h + (len(satirlar) - 1) * ara + 2 * kontur + 12
    img = Image.new("RGBA", (W, bh), (0, 0, 0, 0))
    golge = Image.new("RGBA", (W, bh), (0, 0, 0, 0))
    d, g = ImageDraw.Draw(img), ImageDraw.Draw(golge)
    y = kontur
    for s in satirlar:
        x = (W - f.getlength(s)) / 2
        g.text((x, y + 4), s, font=f, fill=(0, 0, 0, 120), stroke_width=kontur, stroke_fill=(0, 0, 0, 120))
        d.text((x, y), s, font=f, fill=(255, 255, 255, 255), stroke_width=kontur, stroke_fill=(0, 0, 0, 255))
        y += sat_h + ara
    golge = golge.filter(ImageFilter.GaussianBlur(6))
    golge.alpha_composite(img)
    return golge


def katman_png(bloklar, cikti):
    """bloklar: [(RGBA_blok, ust_px)] -> 1080x1920 saydam PNG."""
    Image = _pil()[0]
    tuval = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for blok, ust in bloklar:
        tuval.alpha_composite(blok, (0, int(ust)))
    tuval.save(cikti)
    return cikti


def font_test(cikti, font_yolu=None):
    """Seçilen fontla Türkçe test karesi (gri zemin) üretir; gözle bakılır."""
    Image = _pil()[0]
    fy = font_bul(font_yolu)
    zemin = Image.new("RGBA", (W, 600), (90, 110, 130, 255))
    zemin.alpha_composite(yazi_blogu(TR_TEST + " / IĞDIR İSTANBUL ŞİŞLİ", fy, 72), (0, 120))
    zemin.convert("RGB").save(cikti)
    return fy


if __name__ == "__main__":
    print("ffmpeg :", ffmpeg_bul())
    print("ffprobe:", ffprobe_bul() or "yok (ffmpeg -i çıktısından ölçülecek)")
    print("font   :", font_bul())
    print("pazar  :", pazar_oku(os.getcwd()) or "KARARLAR.md'de yok")
    if "--font-test" in sys.argv:
        c = sys.argv[sys.argv.index("--font-test") + 1]
        font_test(c)
        print("font test karesi:", os.path.abspath(c))
