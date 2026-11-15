#!/usr/bin/env python3
"""Hızlı (viral) kurgu: kısa planlar + geçiş (sert kesim / beyaz flaş / zoom punch) + plan başına TikTok tarzı yazı.

Klasik kurgu.py'nin yapamadıkları için: 0,4–1,7 sn'lik planlar, plan başına yazı konumu, tek kelime renk vurgusu,
kelime kelime çıkan yazı, CTA ikinci satırı. Çıktı 1080x1920, 30 fps, H.264 + AAC 48 kHz stereo (klip sesi).
Müzik ve egzoz tasarımı ayrı adımdır (ses_tasarla.py). Ses −14 LUFS'a o adımda çekilir.

Kullanım:  python3 hizli_kurgu.py ayar.json
ayar.json (yollar ayar dosyasına göre göreli):
{
  "font": "font/TikTokSans.ttf", "font_agirlik": "Bold", "kontur_oran": 0.06,   # TikTok Sans (OFL)
  "yazilar": [{"bas": 0.0, "bit": 1.71, "yazi": "Is this even legal?", "vurgu": "legal?", "konum": 0.13}],  # kesimden bağımsız
  "planlar": [
    {"klip": "klipler/P3.mp4", "bas": 1.20, "bit": 2.06, "gecis": "kesim",
     "yazi": "IS THIS EVEN LEGAL?", "vurgu": "LEGAL?", "renk": "#FF2D2D", "konum": 0.16, "kelime_kelime": false},
    {"klip": "klipler/P4.mp4", "bas": 0.0, "bit": 1.71, "gecis": "punch", "punch": 1.15, "yazi": "ANY ANIMATION", "konum": 0.70}
  ],
  "cta": {"satir1": "RATE IT 1-10", "vurgu": "1-10", "renk": "#FFE600", "satir2": "Comment \"BADGE\" and I'll DM you the link",
          "plan": 7, "konum": 0.16},
  "cikti": "kurgu/V01_hizli.mp4"
}
gecis: kesim | flas (2 kare beyaz) | punch (ilk 0,15 sn'de punch katsayısından 1'e ölçek).
konum: yazının üst kenarı, kare yüksekliğinin oranı (0,15–0,17 üst; 0,68–0,74 alt). Alt %20'ye ve ürüne koyma.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
KONTUR_ORAN = 0.085


def ffmpeg():
    f = shutil.which("ffmpeg")
    if f:
        return f
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


YEDEK_FONTLAR = ["/System/Library/Fonts/Supplemental/Arial Black.ttf", "C:/Windows/Fonts/ariblk.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def font_yukle(yol, boyut, agirlik):
    if not os.path.exists(yol):  # Montserrat (OFL, Google Fonts) yoksa sistemdeki kalın font
        yol = next((y for y in YEDEK_FONTLAR if os.path.exists(y)), None)
        if not yol:
            sys.exit("Kalın font bulunamadı: Montserrat'ı Google Fonts'tan indirip ayar.json 'font' alanına yaz.")
    f = ImageFont.truetype(yol, boyut)
    if agirlik:
        try:
            f.set_variation_by_name(agirlik)
        except Exception:
            pass
    return f


def yazi_png(cikti, satirlar, font_yol, agirlik, ust_oran):
    """satirlar: [(metin, boyut, vurgu_kelime, vurgu_renk)] — ortalı, siyah konturlu, tek kelime renkli."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = int(H * ust_oran)
    for metin, boyut, vurgu, renk in satirlar:
        f = font_yukle(font_yol, boyut, agirlik)
        kontur = max(4, int(boyut * KONTUR_ORAN))
        bosluk = d.textlength(" ", font=f)
        # satırlara böl (en fazla 900 px)
        kelimeler, satir, liste = metin.split(), [], []
        for k in kelimeler:
            dene = " ".join(satir + [k])
            if satir and d.textlength(dene, font=f) > 900:
                liste.append(satir)
                satir = [k]
            else:
                satir.append(k)
        if satir:
            liste.append(satir)
        for s in liste:
            gen = sum(d.textlength(k, font=f) for k in s) + bosluk * (len(s) - 1)
            x = (W - gen) / 2
            for k in s:
                dolgu = renk if (vurgu and k.strip(".,!?").upper() == vurgu.strip(".,!?").upper()) else "#FFFFFF"
                d.text((x, y), k, font=f, fill=dolgu, stroke_width=kontur, stroke_fill="#000000")
                x += d.textlength(k, font=f) + bosluk
            y += int(boyut * 1.12)
        y += int(boyut * 0.15)
    golge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    golge.putalpha(im.getchannel("A").point(lambda v: int(v * 0.55)))
    golge = golge.transform((W, H), Image.AFFINE, (1, 0, -6, 0, 1, -8)).filter(ImageFilter.GaussianBlur(10))
    golge.alpha_composite(im)
    golge.save(cikti)


def plan_isle(ff, p, i, kok, tmp, a):
    hiz = p.get("hiz", 1.0)
    kaynak = round(p["bit"] - p["bas"], 3)
    sure = round(kaynak / hiz, 3)
    klip = os.path.join(kok, p["klip"])
    vf = []
    if p.get("kirp"):  # yakınlaştırma: kaynağın 1/k'sı, merkez oranı (fx, fy) etrafında
        k = p["kirp"]
        fx, fy = p.get("kirp_merkez", [0.5, 0.5])
        vf.append(f"crop=iw/{k}:ih/{k}:'min(max(0,iw*{fx}-iw/{k}/2),iw-iw/{k})':'min(max(0,ih*{fy}-ih/{k}/2),ih-ih/{k})'")
    if hiz != 1.0:
        vf.append(f"setpts=PTS/{hiz}")
    vf += [f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={W}:{H}", f"fps={FPS}", "setsar=1"]
    if p.get("gecis") == "punch":
        k = p.get("punch", 1.15) - 1
        z = f"(1+{k}*max(0\\,1-t/0.15))"
        vf += [f"scale=w='2*trunc({W / 2}*{z})':h='2*trunc({H / 2}*{z})':eval=frame", f"crop={W}:{H}"]
    if p.get("gecis") == "flas":
        vf.append("fade=t=in:st=0:d=0.07:color=white")
    girdiler = ["-ss", f"{p['bas']:.3f}", "-t", f"{kaynak:.3f}", "-i", klip]
    pngler = []
    if p.get("yazi"):
        if p.get("kelime_kelime"):
            kel = p["yazi"].split()
            adim = sure / max(len(kel), 1) * 0.5
            for j in range(len(kel)):
                yol = os.path.join(tmp, f"y{i}_{j}.png")
                yazi_png(yol, [(" ".join(kel[:j + 1]), p.get("boyut", 104), p.get("vurgu"), p.get("renk", "#FF2D2D"))],
                         a["font"], a.get("font_agirlik"), p.get("konum", 0.16))
                bas, bit = j * adim, (sure if j == len(kel) - 1 else (j + 1) * adim)
                pngler.append((yol, bas, bit))
        else:
            yol = os.path.join(tmp, f"y{i}.png")
            yazi_png(yol, [(p["yazi"], p.get("boyut", 112), p.get("vurgu"), p.get("renk", "#FF2D2D"))],
                     a["font"], a.get("font_agirlik"), p.get("konum", 0.16))
            pngler.append((yol, 0, sure))
    cta = a.get("cta")
    if cta and i >= cta["plan"]:
        yol = os.path.join(tmp, f"cta{i}.png")
        yazi_png(yol, [(cta["satir1"], 100, cta.get("vurgu"), cta.get("renk", "#FFE600")),
                       (cta["satir2"], 58, None, None)], a["font"], a.get("font_agirlik"), cta.get("konum", 0.16))
        pngler.append((yol, 0, sure))
    zincir = f"[0:v]{','.join(vf)}[v0]"
    son = "v0"
    for j, (yol, bas, bit) in enumerate(pngler):
        girdiler += ["-loop", "1", "-t", f"{sure:.3f}", "-i", yol]
        zincir += f";[{son}][{j + 1}:v]overlay=0:0:enable='between(t,{bas:.3f},{bit:.3f})'[v{j + 1}]"
        son = f"v{j + 1}"
    af = "aresample=48000,aformat=channel_layouts=stereo"
    if hiz != 1.0:
        af += f",atempo={max(0.5, min(2.0, hiz))}"
    if p.get("ses_db"):
        af += f",volume={p['ses_db']}dB"
    af += f",afade=t=in:d=0.008,afade=t=out:st={max(0, sure - 0.008):.3f}:d=0.008"
    cikti = os.path.join(tmp, f"p{i:02d}.mp4")
    r = subprocess.run([ff, "-v", "error", "-y", *girdiler, "-filter_complex", zincir, "-map", f"[{son}]", "-map", "0:a?",
                        "-af", af, "-t", f"{sure:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                        "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", cikti])
    if r.returncode:
        sys.exit(f"plan {i} işlenemedi")
    return cikti


def yazilari_bindir(ff, video, yazilar, a, tmp, cikti):
    """Kesimden bağımsız yazılar: her biri videonun kendi zamanında (bas–bit sn), 0,12 sn yumuşak giriş."""
    girdiler, zincir, son = ["-i", video], [], "0:v"
    for j, y in enumerate(yazilar):
        satirlar = [(y["yazi"], y.get("boyut", 96), y.get("vurgu"), y.get("renk", "#FF2D2D"))]
        if y.get("satir2"):
            satirlar.append((y["satir2"], y.get("boyut2", 60), None, None))
        yol = os.path.join(tmp, f"z{j}.png")
        yazi_png(yol, satirlar, a["font"], a.get("font_agirlik"), y.get("konum", 0.16))
        girdiler += ["-loop", "1", "-i", yol]
        bas, bit = y["bas"], y["bit"]
        zincir.append(f"[{j + 1}:v]format=rgba,fade=t=in:st={bas:.3f}:d=0.12:alpha=1,"
                      f"fade=t=out:st={bit - 0.06:.3f}:d=0.06:alpha=1[y{j}]")
        zincir.append(f"[{son}][y{j}]overlay=0:0:shortest=1:enable='between(t,{bas:.3f},{bit:.3f})'[o{j}]")
        son = f"o{j}"
    r = subprocess.run([ff, "-v", "error", "-y", *girdiler, "-filter_complex", ";".join(zincir), "-map", f"[{son}]",
                        "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
                        "-r", str(FPS), "-c:a", "copy", "-movflags", "+faststart", cikti])
    if r.returncode:
        sys.exit("yazı bindirme başarısız")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ayar = os.path.abspath(sys.argv[1])
    kok = os.path.dirname(ayar)
    a = json.load(open(ayar, encoding="utf-8"))
    global KONTUR_ORAN
    KONTUR_ORAN = a.get("kontur_oran", KONTUR_ORAN)
    a["font"] = os.path.join(kok, a["font"]) if not os.path.isabs(a["font"]) else a["font"]
    ff = ffmpeg()
    tmp = tempfile.mkdtemp(prefix="hizli_")
    parcalar = [plan_isle(ff, p, i, kok, tmp, a) for i, p in enumerate(a["planlar"])]
    liste = os.path.join(tmp, "liste.txt")
    with open(liste, "w") as f:
        for p in parcalar:
            f.write(f"file '{p}'\n")
    cikti = os.path.join(kok, a["cikti"])
    os.makedirs(os.path.dirname(cikti), exist_ok=True)
    ara = os.path.join(tmp, "birlesik.mp4") if a.get("yazilar") else cikti
    r = subprocess.run([ff, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-c", "copy",
                        "-movflags", "+faststart", ara])
    if r.returncode:
        sys.exit("birleştirme başarısız")
    if a.get("yazilar"):
        yazilari_bindir(ff, ara, a["yazilar"], a, tmp, cikti)
    for y in a.get("yazilar", []):  # okunma kapısı: kelime başına 0,25 sn + 0,5 sn tepki
        gerek = 0.5 + 0.25 * len((y["yazi"] + " " + y.get("satir2", "")).split())
        if y["bit"] - y["bas"] < gerek:
            print(f"UYARI okunmaz: '{y['yazi']}' {y['bit'] - y['bas']:.2f} sn ekranda, en az {gerek:.2f} sn gerekir")
    toplam = sum((p["bit"] - p["bas"]) / p.get("hiz", 1.0) for p in a["planlar"])
    print(f"tamam: {cikti}  ·  {len(parcalar)} plan  ·  {toplam:.2f} sn")
    sinirlar, t = [], 0.0
    for p in a["planlar"]:
        sinirlar.append(round(t, 2))
        t += (p["bit"] - p["bas"]) / p.get("hiz", 1.0)
    print("plan başlangıçları:", sinirlar)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
