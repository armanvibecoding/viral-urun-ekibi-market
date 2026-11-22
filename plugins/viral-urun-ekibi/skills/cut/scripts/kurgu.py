#!/usr/bin/env python3
"""Tek video kurgusu: N plan (klip + saniye aralığı) -> 1080x1920, 30 fps, H.264 + AAC, +faststart.

Kapılar (geçmezse kurgu YAPILMAZ):
  - Kaynak klip yüksekliği < 1280 (720p dikey altı)      -> çıkış 3
  - Kullanılan aralıkta sıçrama (klip_qc.sicramalar)     -> çıkış 3  (gözle bakılıp doğal denen plan: "qc_izin")
Yazı: kanca (+ CTA hemen altında) saydam PNG katmanı; konum "oto" ise her planın orta karesinde en boş bant
seçilir (üst / orta / alt; alt %20 ve sağ %15 hariç). Emoji videoya konmaz (kutucuk olur) -> caption'a taşı.
Ses: klip sesi + isteğe bağlı efektler (kullanıcının kendi telifsiz dosyaları); ölç-düzelt döngüsüyle −14 LUFS.
Çıktı: MP4 + <ad>_kontrol.jpg (her planın ortası + son kare). Kontrol karesine gözle bak.

Kullanım:  python3 kurgu.py ayar.json [--proje <proje_kökü>] [--font <ttf>]
ayar.json (yollar ayar dosyasına göre göreli):
{
  "planlar": [["klipler/V01_S1.mp4", 0, 4.0], ["klipler/V01_S2.mp4", 0.3, 4.0], ["klipler/V01_S3.mp4", 0, 4.0]],
  "kanca": "Kedim bunu görünce aklı gitti",          # ya da plan başına liste: ["...", null, "..."]; " / " = satır sonu
  "cta": null, "cta_kelime": "PİYANO",                 # cta yoksa kelime + pazar (.ekip/KARARLAR.md) ile kurulur
  "cta_plan": -1,                                      # CTA'nın başladığı plan (varsayılan son plan; en az 3 sn)
  "yazi_konum": "oto",                                 # oto | ust | orta | alt | piksel (yazının üst kenarı)
  "kanca_gizle": [],                                   # yakın planda ürün yazısını örtmesin diye kancasız planlar
  "sfx": [{"dosya": "ses/tik.wav", "sn": 5.2, "db": -6, "hizala": true}],
  "klip_sesi_db": 0, "qc_izin": [], "pazar": null, "cikti": "kurgu/V01.mp4"
}
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ffaraclar as F  # noqa: E402
from klip_qc import sicramalar  # noqa: E402

HEDEF_LUFS = -14.0
FPS = 30
BANTLAR = {"ust": (0.10, 0.30, 0.12), "orta": (0.36, 0.56, 0.38), "alt": (0.55, 0.75, 0.57)}  # ölçüm bandı + yazı üstü


def gri_kare(yol, sn, w=108, h=192):
    raw = subprocess.run([F.ffmpeg_bul(), "-v", "error", "-ss", f"{sn:.3f}", "-i", yol, "-frames:v", "1", "-vf",
                          f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return raw if len(raw) == w * h else None


def bant_yogunlugu(raw, w=108, h=192):
    """Her bant için kenar yoğunluğu (|dx|+|dy| ortalaması); sağ %15 ve kenar boşlukları hariç."""
    x0, x1 = int(w * 0.08), int(w * 0.85)
    out = {}
    for ad, (b0, b1, _) in BANTLAR.items():
        top, n = 0, 0
        for y in range(int(h * b0), int(h * b1) - 1):
            r, r2 = y * w, (y + 1) * w
            for x in range(x0, x1 - 1):
                top += abs(raw[r + x] - raw[r + x + 1]) + abs(raw[r + x] - raw[r2 + x])
                n += 1
        out[ad] = top / max(n, 1)
    return out


def ses_rms_db(yol, bas, son):
    """50 ms pencerelerde dB dizisi (efekti klipteki gerçek ses anına hizalamak için)."""
    import array
    import math
    raw = subprocess.run([F.ffmpeg_bul(), "-v", "error", "-ss", str(bas), "-to", str(son), "-i", yol, "-ac", "1",
                          "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    a = array.array("h")
    a.frombytes(raw[: len(raw) // 2 * 2])
    w = 400
    return [20 * math.log10((math.sqrt(sum(v * v for v in a[i:i + w]) / w) + 1) / 32768)
            for i in range(0, len(a) - w, w)]


def hizala(db, yerel, sure):
    """Plan saniyesine ±1,2 sn içindeki en belirgin ses yükselişi; yoksa plan saniyesi."""
    en, puan = None, 11.0
    for j in range(1, len(db)):
        t = j * 0.05
        if t < 0.15 or t > sure - 0.25 or abs(t - yerel) > 1.2:
            continue
        d = db[j] - db[j - 1]
        p = d - 4 * abs(t - yerel)
        if d >= 12 and p > puan:
            en, puan = t, p
    return en if en is not None else min(max(yerel, 0.1), max(sure - 0.3, 0.1))


def main():
    ap = argparse.ArgumentParser(description="Tek video kurgusu (ffmpeg)")
    ap.add_argument("ayar")
    ap.add_argument("--proje", default=os.getcwd(), help="pazarın okunacağı proje kökü (.ekip/KARARLAR.md)")
    ap.add_argument("--font")
    g = ap.parse_args()
    with open(g.ayar, encoding="utf-8") as f:
        a = json.load(f)
    kok = os.path.dirname(os.path.abspath(g.ayar))
    yol = lambda p: p if os.path.isabs(p) else os.path.join(kok, p)  # noqa: E731
    planlar = [(yol(p[0]), float(p[1]), float(p[2])) for p in a["planlar"]]
    n = len(planlar)
    bilgi = [F.medya_bilgi(p[0]) for p in planlar]

    # ---- KAPILAR ----
    for i, ((k, b, e), bi) in enumerate(zip(planlar, bilgi)):
        if bi["h"] < a.get("min_yukseklik", 1280):
            sys.exit(f"KAPI: plan {i + 1} {k} {bi['w']}x{bi['h']} — 720p (1280 yükseklik) altı; yeniden indir/üret")
        if e - b < 0.3 or e > bi["sure"] + 0.05:
            sys.exit(f"KAPI: plan {i + 1} aralığı geçersiz ({b}-{e}, klip {bi['sure']:.2f} sn)")
        if i in a.get("qc_izin", []):
            continue
        kotu = [round(t, 2) for t, _, _ in sicramalar(k) if b + 0.05 < t < e - 0.05]
        if kotu:
            sys.exit(f"KAPI: plan {i + 1} ({k}) {b}-{e} aralığında sıçrama @{kotu} — kırp, yeniden üret "
                     f"ya da 4 fps panoya bakıp doğalsa qc_izin'e ekle")

    sure = [e - b for _, b, e in planlar]
    bas = [sum(sure[:i]) for i in range(n)]
    top = sum(sure)

    # ---- METİN ----
    pazar = a.get("pazar") or F.pazar_oku(g.proje)
    cta = a.get("cta")
    if not cta and a.get("cta_kelime"):
        if not pazar:
            sys.exit("Pazar bulunamadı: .ekip/KARARLAR.md'ye '- YYYY-AA-GG | pazar | Türkiye' yaz ya da ayara \"pazar\" ekle")
        cta = F.cta_metni(a["cta_kelime"], pazar)
    uyar = []
    kl = a.get("kanca")
    kl = kl if isinstance(kl, list) else [kl] * n
    if len(kl) != n:
        sys.exit("kanca listesi plan sayısıyla aynı uzunlukta olmalı")
    kl = [None if (i in a.get("kanca_gizle", []) or not k) else k for i, k in enumerate(kl)]
    temiz = []
    for k in kl:
        if k:
            k, c = F.emoji_temizle(k)
            if c:
                uyar.append("emoji kancadan çıkarıldı (caption'a koy)")
        temiz.append(k or None)
    kl = temiz
    if cta:
        cta, c = F.emoji_temizle(cta)
        if c:
            uyar.append("emoji CTA'dan çıkarıldı")
    font = F.font_bul(g.font or a.get("font"))

    # ---- KONUM ----
    konum = a.get("yazi_konum", "oto")
    if isinstance(konum, (int, float)):
        ust_px, bant = int(konum), f"{int(konum)}px"
    else:
        if konum == "oto":
            puan = {b_: 0.0 for b_ in BANTLAR}
            for (k, b, e) in planlar:
                raw = gri_kare(k, (b + e) / 2)
                if raw:
                    for b_, v in bant_yogunlugu(raw).items():
                        puan[b_] = max(puan[b_], v)
            konum = min(puan, key=lambda x: (round(puan[x], 1), list(BANTLAR).index(x)))
        if konum not in BANTLAR:
            sys.exit(f"yazi_konum geçersiz: {konum}")
        ust_px, bant = int(BANTLAR[konum][2] * F.H), konum

    gecici = tempfile.mkdtemp(prefix="kurgu_")
    try:
        katmanlar = []  # (png, t0, t1)
        kbloklar = {}
        i = 0
        while i < n:
            if not kl[i]:
                i += 1
                continue
            j = i
            while j + 1 < n and kl[j + 1] == kl[i]:
                j += 1
            boy = 72 if len(kl[i]) < 40 else 64
            kbloklar[(i, j)] = F.yazi_blogu(kl[i], font, boy)
            i = j + 1
        cta_bas = None
        if cta:
            cp = a.get("cta_plan", -1)
            cp = cp % n
            cta_bas = min(bas[cp], max(top - 3.0, 0))  # CTA en az 3 sn
            cblok = F.yazi_blogu(cta, font, 56)
            kanca_h = max([b_.size[1] for (i0, j0), b_ in kbloklar.items() if bas[j0] + sure[j0] > cta_bas] or [0])
            cta_ust = ust_px + (kanca_h + 24 if kanca_h else 0)
            if cta_ust + cblok.size[1] > F.H * 0.80:
                uyar.append("CTA alt %20'ye taşıyor; yazi_konum'u yukarı al")
        # her zaman dilimi için tek PNG (kanca + CTA birlikte) -> çakışma yok
        sinirlar = sorted({0.0, top} | {bas[i0] for i0, _ in kbloklar} | {bas[j0] + sure[j0] for _, j0 in kbloklar}
                          | ({cta_bas} if cta_bas is not None else set()))
        for t0, t1 in zip(sinirlar, sinirlar[1:]):
            orta = (t0 + t1) / 2
            bl = [(b_, ust_px) for (i0, j0), b_ in kbloklar.items() if bas[i0] <= orta < bas[j0] + sure[j0]]
            if cta_bas is not None and orta >= cta_bas:
                bl.append((cblok, cta_ust))
            if bl:
                p = os.path.join(gecici, f"y{len(katmanlar)}.png")
                F.katman_png(bl, p)
                katmanlar.append((p, t0, t1))

        # ---- FFMPEG GRAFİĞİ ----
        gir, fl, idx = [], [], 0
        for i, ((k, b, e), bi) in enumerate(zip(planlar, bilgi)):
            d = e - b
            gir += ["-ss", f"{b:.3f}", "-t", f"{d:.3f}", "-i", k]
            vi = idx
            idx += 1
            if bi["ses"]:
                ai = f"{vi}:a"
            else:
                gir += ["-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
                ai = f"{idx}:a"
                idx += 1
            fl.append(f"[{vi}:v]scale={F.W}:{F.H}:force_original_aspect_ratio=increase,crop={F.W}:{F.H},setsar=1,"
                      f"fps={FPS},tpad=stop_mode=clone:stop_duration=0.5,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{i}]")
            fl.append(f"[{ai}]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
                      f"atrim=duration={d:.3f},apad=whole_dur={d:.3f},asetpts=PTS-STARTPTS[a{i}]")
        fl.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v0][a0]")
        son = "v0"
        for j, (p, t0, t1) in enumerate(katmanlar):
            gir += ["-loop", "1", "-t", f"{top:.3f}", "-i", p]
            fl.append(f"[{son}][{idx}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1 - 0.001:.3f})'[o{j}]")
            son, idx = f"o{j}", idx + 1
        fl.append(f"[a0]volume={float(a.get('klip_sesi_db', 0))}dB[ak]")
        karis, kayit = ["[ak]"], []
        for j, s in enumerate(a.get("sfx", [])):
            sp = yol(s["dosya"])
            if not os.path.exists(sp):
                sys.exit(f"efekt dosyası yok: {sp} (telifsiz kendi sesini koy)")
            t = float(s["sn"])
            if s.get("hizala"):
                c = max(i for i in range(n) if bas[i] <= t)
                k, b, e = planlar[c]
                t = bas[c] + hizala(ses_rms_db(k, b, e), t - bas[c], sure[c])
            gir += ["-i", sp]
            ms = int(t * 1000)
            fl.append(f"[{idx}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
                      f"volume={float(s.get('db', 0))}dB,adelay={ms}:all=1[s{j}]")
            karis.append(f"[s{j}]")
            kayit.append(f"{os.path.basename(sp)}@{t:.2f}s")
            idx += 1
        fl.append("".join(karis) + f"amix=inputs={len(karis)}:normalize=0:duration=first,aresample=48000[ao]")

        cikti = yol(a.get("cikti", "kurgu.mp4"))
        os.makedirs(os.path.dirname(cikti) or ".", exist_ok=True)
        ham = os.path.join(gecici, "ham.mp4")
        F.calistir([F.ffmpeg_bul(), "-v", "error", "-y"] + gir + ["-filter_complex", ";".join(fl),
                   "-map", f"[{son}]", "-map", "[ao]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                   "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-t", f"{top:.3f}", ham])

        # ---- SES: ölç -> kazanç -> tekrar ölç (tek geçiş videolar arası 8 dB fark bıraktı) ----
        i2 = F.lufs_olc(ham)
        if i2 < -60:
            shutil.copy(ham, cikti)
            uyar.append("ses yok/çok sessiz; normalleştirme atlandı")
        else:
            kaz = 0.0
            for _ in range(4):
                kaz += HEDEF_LUFS - i2
                F.calistir([F.ffmpeg_bul(), "-v", "error", "-y", "-i", ham, "-c:v", "copy", "-af",
                            f"volume={kaz:.2f}dB,alimiter=limit=0.89:level=false", "-c:a", "aac", "-b:a", "192k",
                            "-movflags", "+faststart", cikti])
                i2 = F.lufs_olc(cikti)
                if abs(i2 - HEDEF_LUFS) <= 0.5:
                    break
            if abs(i2 - HEDEF_LUFS) > 1.0:
                uyar.append(f"ses {i2:.1f} LUFS (hedef {HEDEF_LUFS})")

        # ---- KONTROL KARESİ: her planın ortası + son kare ----
        zam = [bas[i] + sure[i] / 2 for i in range(n)] + [max(top - 0.2, 0)]
        kontrol = os.path.splitext(cikti)[0] + "_kontrol.jpg"
        Image = F._pil()[0]
        pano = Image.new("RGB", (270 * len(zam), 480))
        for j, z in enumerate(zam):
            p = os.path.join(gecici, f"k{j}.png")
            F.calistir([F.ffmpeg_bul(), "-v", "error", "-y", "-ss", f"{z:.3f}", "-i", cikti, "-frames:v", "1",
                        "-vf", "scale=270:480", p])
            pano.paste(Image.open(p).convert("RGB"), (270 * j, 0))
        pano.save(kontrol, quality=90)
    finally:
        shutil.rmtree(gecici, ignore_errors=True)

    m = F.medya_bilgi(cikti)
    print(f"tamam: {cikti}")
    print(f"süre {m['sure']:.2f} sn · {m['w']}x{m['h']} · {i2:.1f} LUFS · yazı bandı {bant} · pazar {pazar or '-'}")
    print(f"planlar başlangıç {[round(x, 2) for x in bas]} · efekt {kayit or '-'} · font {os.path.basename(font)}")
    print(f"kontrol karesi: {kontrol}  (yazı ürünü/çıkış noktasını örtüyor mu, CTA son ≥3 sn'de mi — gözle bak)")
    for u in dict.fromkeys(uyar):
        print("UYARI:", u)


if __name__ == "__main__":
    main()
