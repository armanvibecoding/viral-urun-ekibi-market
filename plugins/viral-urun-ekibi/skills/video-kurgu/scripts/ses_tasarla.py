#!/usr/bin/env python3
"""Araba videosu ses tasarımı: abartılı ama gerçekçi egzoz + (isteğe bağlı) müzik.

ARAÇ PROFİLİ: varsayılan ayarlar egzoz içindir. Başka ürünlerde --patlama_db 0 --crackle_db 0 ile yalnız
müzik + sentetik efekt (--sfx tik@sn,vurus@sn) öne çıkar. Not: EQ, doygunluk ve garaj yankısı
klip sesine yine uygulanır; yankıyı --yankı_db ile kıs.

EFEKT KATMANI (ses tasarımcısı, 2026-11-16; hepsi isteğe bağlı, verilmezse çıktı eskisiyle aynı):
  --sfx tik@8.24,vurus@8.57,boom@3.43,whoosh@1.70   sentetik türler: tik · vurus · boom (vine-boom
                                                    benzeri bas darbe) · whoosh (gürültü süpürmesi)
  --sfx_dosya "whoosh.mp3@3.20:-6,boom.mp3@3.43:-3:0-0.8"  dosya@saniye[:tepe_dB[:kırp_bas-kırp_bit]];
                                                    yol yoksa --sfx_klasor altında aranır (lisans: klasörün LISANS.md'si)
  --riser 3.429:1.2:-10                             drop'ta BİTEN sentetik yükseliş (bit_sn:süre[:dB])
  --sessizlik_vurusu 0.2                            drop'tan önce 0,15-0,25 sn müzik+klip kesmesi (kontrast)
  --sessizlik "1.70-1.80"                           elle kesme aralıkları (komedi duraklaması vb.)
  --sfx_max_10sn 5                                  yoğunluk kapısı: 10 sn'de bundan çok efekt -> hedef_tuttu false
Efektler müzik+klip karışımına son seviyeden önce eklenir; drop kapısı (drop_artis_db) efektler dahil ölçülür.

MÜZİK GİRİŞİ KAPISI (2026-11-17 kurucu: "müzik bir anda açılıyor"): açılış diegetik ses olayıyla (klip sesi/efekt);
müzik videonun 0. saniyesinde −30 dB'den başlar ve --muzik_fade_in (varsayılan 1,75 sn) içinde dB-doğrusal rampayla yatak
seviyesine çıkar. Yerleştirilmiş müzik stem'i + son karışım ses_olc.muzik_giris ile ölçülür (başlangıç ≤ −20 dB · rampa
1,2–3,0 sn · ilk 1 sn ≥ −20 dB · 3 sn pencerede basamak ≤ +10 dB · açılış olayı ≥ −6 dB); tutmazsa hedef_tuttu false, çıkış 2.
--muzik_bas > --drop_video_sn olmalı (müzik videodan önce başlar); tersi müziği geç başlatır ve kapıdan kalır.

Kullanım:
  python3 ses_tasarla.py --video PILOT.mp4 --cikti Y.mp4
  python3 ses_tasarla.py --video PILOT.mp4 --muzik A.mp3 --muzik_bas 8.0 \
      --drop_video_sn 4.26 --cikti Y.mp4

--muzik_bas    : müzik dosyasında DROP'un saniyesi (hizalanacak nokta)
--drop_video_sn: o drop'un videoda düşeceği saniye
Müzik yoksa yalnız egzoz tasarımı yapılır. Video akışı yeniden kodlanmaz (-c:v copy).

Zincir (egzoz): kesme yerlerinde 5 ms mikro-fade -> (isteğe bağlı) rölanti boşluk
doldurma -> EQ (55 Hz +5, 110 Hz +2, 380 Hz -2.5, 2.2 kHz +2) -> paralel tanh doygunluk
-> olay anlarında crackle (1.2-9 kHz) +8 dB ve bas darbe (<160 Hz) +5 dB -> beton
otopark yankısı (erken yansıma + bant-bağımlı RT60 kuyruk, afir) -> müzik sidechain
(yalnız olay anlarında duck_db kadar) -> -14 LUFS / -1 dBTP (192 kHz'de limiter,
AAC sonrası ölçülerek doğrulanır).
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ses_olc import muzik_giris  # noqa: E402
import numpy as np

SR = 48000


def ffmpeg_yolu():
    yol = shutil.which("ffmpeg")
    try:
        import imageio_ffmpeg
        yol = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    if not yol:
        sys.exit("ffmpeg bulunamadı (imageio_ffmpeg ya da PATH)")
    return yol


FF = ffmpeg_yolu()


def kos(args, yakala=True):
    r = subprocess.run([FF, "-hide_banner", "-y"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        sys.exit(f"ffmpeg hata verdi (kod {r.returncode})")
    return r.stderr


def raw_giris(yol, kanal=2):
    return ["-f", "f32le", "-ar", str(SR), "-ac", str(kanal), "-i", yol]


def raw_oku(yol, kanal=2):
    return np.fromfile(yol, np.float32).reshape(-1, kanal).astype(np.float64)


def raw_yaz(yol, x):
    np.asarray(x, np.float32).tofile(yol)


def olc(args_giris):
    """ebur128 özeti: (I LUFS, LRA, true peak dBTP)."""
    e = kos(args_giris + ["-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    s = e[e.rfind("Summary:"):]
    sayi = lambda k: float(re.search(k + r"\s+(-?[\d.]+|-inf)", s).group(1).replace("-inf", "-120"))
    tp = float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf)", s).group(1).replace("-inf", "-120"))
    return sayi("I:"), sayi("LRA:"), tp


def bant(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f >= hi)] = 0
    return np.fft.irfft(X, len(x))


def zarf_db(y, h):
    n = len(y) // h
    return 20 * np.log10(np.sqrt((y[: n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)


def yumusat(g, n):
    if n < 2:
        return g
    k = np.hanning(n)
    return np.convolve(g, k / k.sum(), mode="same")


def kesmeleri_bul(video):
    e = kos(["-i", video, "-an", "-vf", "select='gt(scene,0.30)',showinfo", "-f", "null", "-"])
    return [round(float(t), 3) for t in re.findall(r"pts_time:([\d.]+)", e)]


def olaylari_bul(mono, kesmeler):
    """2-10 kHz bandında ani yükseliş (pop/crackle) + 200-2k bantta patlama."""
    h = 480  # 10 ms
    H = zarf_db(bant(mono, 2000, 10000), h)
    M = zarf_db(bant(mono, 200, 2000), h)
    medH, medM = np.median(H), np.median(M)
    onset = []
    for j in range(1, len(H)):
        t = j * 0.01
        if t < 0.08 or any(abs(t - k) < 0.05 for k in kesmeler):
            continue
        yuksel = H[j] - H[j - 1] > 9 and H[j] > medH + 15
        patla = M[j] - M[j - 1] > 8 and M[j] > medM + 12
        if yuksel or patla:
            onset.append(round(t, 2))
    return onset


def gruplar(onset, bosluk=0.30):
    g = []
    for t in onset:
        if g and t - g[-1][-1] <= bosluk:
            g[-1].append(t)
        else:
            g.append([t])
    return g


def olay_zarfi(n, grp, on=0.04, son=0.45):
    g = np.zeros(n)
    for grup in grp:
        a = max(0, int((grup[0] - on) * SR))
        b = min(n, int((grup[-1] + son) * SR))
        g[a:b] = 1
    # 20 ms giriş / 150 ms çıkış yumuşatma (tıklama olmasın)
    return np.clip(yumusat(g, int(0.17 * SR)), 0, 1)


def darbe_zarfi(n, grp):
    g = np.zeros(n)
    for grup in grp:
        for t in grup[:2]:  # grubun ilk iki darbesi (patlama + ilk pop)
            i = int(t * SR)
            L = min(n - i, int(0.18 * SR))
            if L <= 0:
                continue
            tt = np.arange(L) / SR
            g[i:i + L] = np.maximum(g[i:i + L], np.minimum(tt / 0.004, 1) * np.exp(-tt / 0.07))
    return g


def garaj_ir(rt60=1.5, seed=7):
    """Beton otopark IR'ı: 12 ms ön gecikme, erken yansımalar, bant-bağımlı kuyruk."""
    rng = np.random.default_rng(seed)
    L = int((rt60 * 1.3 + 0.05) * SR)
    t = np.arange(L) / SR
    ir = np.zeros((L, 2))
    for kanal in range(2):
        gurultu = rng.standard_normal(L)
        kuyruk = np.zeros(L)
        # alçak (<300 Hz) ×1.2 RT, orta ×1.0, tiz (>3.5 kHz) ×0.55 RT (hava + beton emilimi)
        for (lo, hi, kat) in [(20, 300, 1.2), (300, 3500, 1.0), (3500, 16000, 0.55)]:
            b = bant(gurultu, lo, hi)
            kuyruk += b * np.exp(-6.91 * t / (rt60 * kat))
        on = int(0.012 * SR)
        kuyruk[:on] = 0
        kuyruk[on:on + int(0.03 * SR)] *= np.linspace(0, 1, int(0.03 * SR))
        ir[:, kanal] = kuyruk * 0.35
        # erken yansımalar (tavan ~2.6 m, kolonlar, yan duvar) - kanal başına hafif farklı
        for ms, kaz in [(7, 0.55), (13, 0.42), (19, 0.33), (29, 0.27), (41, 0.2), (57, 0.14)]:
            i = int((ms + kanal * 1.3) * SR / 1000)
            ir[i, kanal] += kaz * (1 if (ms + kanal) % 2 else -1)
    ir /= np.sqrt((ir ** 2).sum(0).max())
    return ir


def yatak_dongu(x, a, b, n):
    seg = x[int(a * SR):int(b * SR)]
    xf = int(0.08 * SR)
    w = np.sin(np.linspace(0, np.pi / 2, xf)) ** 2
    out = seg.copy()
    while len(out) < n:
        bas = seg.copy()
        out[-xf:] = out[-xf:] * (1 - w)[:, None] + bas[:xf] * w[:, None]
        out = np.concatenate([out, bas[xf:]])
    return out[:n]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True)
    ap.add_argument("--muzik")
    ap.add_argument("--muzik_bas", type=float, default=0.0, help="müzik dosyasında drop saniyesi")
    ap.add_argument("--drop_video_sn", type=float, default=0.0, help="drop'un videodaki saniyesi")
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--duck_db", type=float, default=None,
                    help="egzoz anında müzik kısma (4-6); varsayılan 5, egzozsuz profilde (patlama=crackle=0) 0")
    ap.add_argument("--muzik_db", type=float, default=-3.0, help="müzik/egzoz LUFS farkı")
    ap.add_argument("--drop_oncesi_db", type=float, default=-8.0,
                    help="drop'tan önceki 1,7 sn'de klip sesini kısma (drop kontrastı); 0 = kapalı")
    ap.add_argument("--drop_esik_db", type=float, default=6.0, help="drop anında ölçülen en az ses artışı (kapı)")
    ap.add_argument("--rt60", type=float, default=1.5, help="garaj kuyruğu (1.2-1.8 sn)")
    ap.add_argument("--yankı_db", dest="yanki_db", type=float, default=-13.0, help="yankı dönüş seviyesi")
    ap.add_argument("--patlama_db", type=float, default=6.0, help="patlama anı tam-bant vurgu")
    ap.add_argument("--crackle_db", type=float, default=10.0, help="olay anı 1.2-9 kHz vurgu")
    ap.add_argument("--rolanti_db", type=float, default=4.0, help="olay dışı kısma (kontrast)")
    ap.add_argument("--olaylar", help="elle egzoz olay saniyeleri, virgüllü (otomatik yerine)")
    ap.add_argument("--kesmeler", default="otomatik", help="'otomatik' | 'yok' | virgüllü saniyeler")
    ap.add_argument("--yatak", help="rölanti boşluk doldurma kaynağı 'BAS-BIT' (videodaki saniye)")
    ap.add_argument("--hedef_lufs", type=float, default=-14.0)
    ap.add_argument("--tepe", type=float, default=-1.0, help="tavan dBTP")
    ap.add_argument("--stem_klasoru", help="ara stem'leri buraya kopyala")
    ap.add_argument("--sfx", help="sentetik efekt: 'tik@8.24,vurus@8.57' (tik = ekrana dokunma, vurus = değişim darbesi)")
    ap.add_argument("--sfx_db", type=float, default=-9.0, help="efekt tepe seviyesi (dBFS, son seviyeden önce)")
    ap.add_argument("--son_fade", type=float, default=0.8, help="müzik sonu kararma (döngülü videoda 0.12)")
    ap.add_argument("--sfx_dosya", help="dosya efektleri: 'yol@sn[:dB[:bas-bit]]' virgüllü; dB = tepe (varsayılan --sfx_db)")
    ap.add_argument("--sfx_klasor", help="--sfx_dosya'da yalın ad verilirse aranacak klasör (ör. uretim-4/sfx)")
    ap.add_argument("--riser", help="sentetik yükseliş 'bit_sn:sure[:dB]' — drop'ta biter (ör. 3.429:1.2:-10)")
    ap.add_argument("--sessizlik_vurusu", type=float, default=0.0,
                    help="drop'tan önce bu kadar sn (0.15-0.25) müzik+klip kesilir; --drop_video_sn gerekir")
    ap.add_argument("--sessizlik", help="elle kesme aralıkları 'bas-bit,bas-bit' (sn); efektler kesmeden etkilenmez")
    ap.add_argument("--sfx_max_10sn", type=int, default=5, help="herhangi 10 sn penceresinde en çok efekt (kapı)")
    ap.add_argument("--muzik_fade_in", type=float, default=1.75,
                    help="müzik 0. sn'de −30 dB'den bu sürede (dB-doğrusal) yatak seviyesine çıkar (1,5–2)")
    a = ap.parse_args()
    if a.duck_db is None:  # egzozsuz videoda rölanti/söküm sesi "olay" sanılıp müzik kısılıyordu (ölçülen ses delikleri)
        a.duck_db = 0.0 if (a.patlama_db == 0 and a.crackle_db == 0) else 5.0

    if os.path.abspath(a.cikti) == os.path.abspath(a.video):
        sys.exit("çıktı girdi videonun üstüne yazamaz")
    tmp = tempfile.mkdtemp(prefix="ses_")
    P = lambda ad: os.path.join(tmp, ad)
    rapor = {"video": a.video, "muzik": a.muzik}

    # 1) videonun sesi
    kos(["-i", a.video, "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", P("ham.f32")])
    x = raw_oku(P("ham.f32"))
    n = len(x)
    sure = n / SR
    rapor["sure_sn"] = round(sure, 3)

    # 2) kesmeler + 5 ms mikro-fade
    if a.kesmeler == "otomatik":
        kesmeler = kesmeleri_bul(a.video)
    elif a.kesmeler == "yok":
        kesmeler = []
    else:
        kesmeler = [float(v) for v in a.kesmeler.split(",")]
    f5 = int(0.005 * SR)
    for k in kesmeler:
        i = int(k * SR)
        if f5 < i < n - f5:
            x[i - f5:i] *= np.cos(np.linspace(0, np.pi / 2, f5))[:, None] ** 2
            x[i:i + f5] *= np.sin(np.linspace(0, np.pi / 2, f5))[:, None] ** 2
    rapor["kesmeler"] = kesmeler

    # 3) seviye sabitleme (zincir parametreleri seviyeden bağımsız olsun): tepe -6 dBFS
    x *= 10 ** (-6 / 20) / (np.abs(x).max() + 1e-12)
    mono = x.mean(1)

    # 4) olaylar
    if a.olaylar:
        onset = [float(v) for v in a.olaylar.split(",")]
    else:
        onset = olaylari_bul(mono, kesmeler)
    grp = gruplar(onset)
    rapor["olay_gruplari"] = grp

    # 5) rölanti boşluk doldurma (isteğe bağlı)
    if a.yatak:
        ya, yb = [float(v) for v in a.yatak.split("-")]
        yat = yatak_dongu(x, ya, yb, n)
        h = 2400
        Lo = zarf_db(bant(mono, 20, 200), h)
        Lb = np.median(zarf_db(bant(yat.mean(1), 20, 200), h))
        g = np.clip((Lb - 8 - Lo) / 6, 0, 1)  # orijinal bas, yataktan 8 dB'den fazla düşükse doldur
        g = np.repeat(g, h)[:n]
        g = np.pad(g, (0, n - len(g)), mode="edge")
        g = yumusat(g, int(0.25 * SR)) * 10 ** (-4 / 20)
        x = x + yat * g[:, None]
        rapor["yatak"] = {"kaynak": a.yatak, "doldurulan_sn": round(float((g > 0.1).sum() / SR), 2)}

    oz = olay_zarfi(n, grp)
    dz = darbe_zarfi(n, grp)
    # patlama anı tam-bant vurgu: darbe zarfı boyunca +patlama_db (70 ms sönüm)
    x = x * (1 + (10 ** (a.patlama_db / 20) - 1) * dz)[:, None]
    # kontrast: olay dışı rölanti -rolanti_db (son -14 LUFS kazancı olayları öne iter)
    rg = 10 ** (-abs(a.rolanti_db) / 20)
    x = x * (rg + (1 - rg) * oz)[:, None]
    raw_yaz(P("egz_giris.f32"), x)
    raw_yaz(P("olay.f32"), np.stack([oz, oz], 1))
    raw_yaz(P("darbe.f32"), np.stack([dz, dz], 1))
    raw_yaz(P("ir.f32"), garaj_ir(a.rt60))

    # 6) egzoz stem'i (ffmpeg)
    yd = a.yanki_db
    egz_graf = (
        "[0]asplit=5[a][b][c][d][e];"
        "[a]highpass=f=25,equalizer=f=55:t=q:w=1.2:g=5,equalizer=f=110:t=q:w=1.0:g=2,"
        "equalizer=f=380:t=q:w=1.5:g=-2.5,equalizer=f=2200:t=q:w=1.0:g=2[dry];"
        "[b]volume=10dB,asoftclip=type=tanh:oversample=4,highpass=f=40,lowpass=f=5000,volume=-11dB[sat];"
        "[c]highpass=f=1200,lowpass=f=9000[c0];[c0][1]amultiply,"
        f"volume={a.crackle_db}dB,"
        "asoftclip=type=tanh:threshold=0.9:oversample=4[crk];"
        "[d]lowpass=f=160[d0];[d0][2]amultiply,volume=5dB[thm];"
        "[e]highpass=f=150,lowpass=f=8000[e0];[e0][3]afir=dry=0:wet=1:gtype=none:irnorm=-1,"
        f"volume={yd}dB[wet];"
        "[dry][sat][crk][thm][wet]amix=inputs=5:normalize=0[out]"
    )
    kos(raw_giris(P("egz_giris.f32")) + raw_giris(P("olay.f32")) + raw_giris(P("darbe.f32"))
        + raw_giris(P("ir.f32")) + ["-filter_complex", egz_graf, "-map", "[out]",
                                    "-t", f"{sure:.4f}", "-f", "f32le", "-ar", str(SR), "-ac", "2", P("egz.f32")])
    I_e, _, _ = olc(raw_giris(P("egz.f32")))
    rapor["egz_stem_lufs_ham"] = I_e
    # 6b) drop kontrastı: klip sesi drop'tan hemen önce kısılır, drop anında tam döner (ölçülen sorun:
    # rölanti/söküm sesi drop öncesi yüksek kalınca müzik drop'u karışımda duyulmuyordu)
    if a.muzik and a.drop_video_sn > 0 and a.drop_oncesi_db < 0:
        eg = raw_oku(P("egz.f32")).copy()
        z = np.arange(len(eg)) / SR
        b0, b1 = max(0.0, a.drop_video_sn - 1.714), a.drop_video_sn
        g = np.ones(len(eg))
        ic = (z >= b0) & (z < b1)
        g[ic] = 10 ** (a.drop_oncesi_db / 20)
        g = np.convolve(g, np.ones(int(0.04 * SR)) / int(0.04 * SR), mode="same")  # 40 ms yumuşak geçiş
        g[z >= b1] = 1.0
        (eg * g[:, None]).astype(np.float32).tofile(P("egz.f32"))
        rapor["drop_oncesi_db"] = a.drop_oncesi_db
    egz_kaz = -17.0 - I_e

    # 7) müzik stem'i
    muzik = a.muzik and os.path.exists(a.muzik)
    if a.muzik and not muzik:
        print(f"UYARI: müzik bulunamadı ({a.muzik}) — yalnız egzoz tasarımı", file=sys.stderr)
    if muzik:
        ofs = a.drop_video_sn - a.muzik_bas
        hiza = f"adelay={int(ofs*1000)}|{int(ofs*1000)}," if ofs >= 0 else f"atrim=start={-ofs:.4f},asetpts=PTS-STARTPTS,"
        fade_in = ""  # rampa aşağıda numpy ile (−30 dB -> 0 dB, dB-doğrusal)
        mgraf = (f"[0:a]aresample={SR},aformat=sample_fmts=flt:channel_layouts=stereo,{hiza}{fade_in}"
                 "highpass=f=30,equalizer=f=80:t=q:w=1.0:g=-3,apad,"
                 f"atrim=end={sure:.4f},afade=t=out:st={max(0,sure-a.son_fade):.3f}:d={a.son_fade}[m]")
        kos(["-i", a.muzik, "-filter_complex", mgraf, "-map", "[m]", "-f", "f32le", "-ar", str(SR),
             "-ac", "2", P("muz.f32")])
        if a.muzik_fade_in > 0:
            mz = raw_oku(P("muz.f32")).copy()
            tz = np.arange(len(mz)) / SR
            mz *= np.where(tz < a.muzik_fade_in, 10 ** ((-30 + 30 * tz / a.muzik_fade_in) / 20), 1.0)[:, None]
            raw_yaz(P("muz.f32"), mz)
        I_m, _, _ = olc(raw_giris(P("muz.f32")))
        rapor["muzik_stem_lufs_ham"] = I_m
        rapor["muzik_ofset_sn"] = round(ofs, 3)
        muz_kaz = -17.0 + a.muzik_db - I_m
        oran = 1 / (1 - a.duck_db / 20.0)  # anahtar 0 dBFS, eşik -20 dB -> GR = duck_db
        karisim = (
            f"[0]volume={egz_kaz:.2f}dB[eg];[1]volume={muz_kaz:.2f}dB[mu];"
            f"[mu][2]sidechaincompress=threshold=0.1:ratio={oran:.4f}:attack=15:release=250:knee=1:makeup=1,asplit=2[md][mdo];"
            "[eg][md]amix=inputs=2:normalize=0[mix]"
        )
        kos(raw_giris(P("egz.f32")) + raw_giris(P("muz.f32")) + raw_giris(P("olay.f32"))
            + ["-filter_complex", karisim, "-map", "[mix]", "-f", "f32le", "-ar", str(SR), "-ac", "2", P("mix.f32"),
               "-map", "[mdo]", "-f", "f32le", "-ar", str(SR), "-ac", "2", P("muz_duck.f32")])
        # gerçekleşen duck ölçümü: olay penceresinde ön/son RMS farkı
        m0 = raw_oku(P("muz.f32")).mean(1) * 10 ** (muz_kaz / 20)
        m1 = raw_oku(P("muz_duck.f32")).mean(1)
        k = min(len(m0), len(m1), n)
        maske = oz[:k] > 0.95
        if maske.sum() > SR * 0.05:
            r = lambda v: np.sqrt(np.mean(v[maske] ** 2) + 1e-20)
            rapor["olcululen_duck_db"] = round(20 * np.log10(r(m1[:k]) / r(m0[:k])), 2)
            disari = oz[:k] < 0.01
            rr = lambda v: np.sqrt(np.mean(v[disari] ** 2) + 1e-20)
            rapor["olay_disi_degisim_db"] = round(20 * np.log10(rr(m1[:k]) / rr(m0[:k])), 2)
    else:
        kos(raw_giris(P("egz.f32")) + ["-af", f"volume={egz_kaz:.2f}dB", "-f", "f32le", "-ar", str(SR),
                                       "-ac", "2", P("mix.f32")])

    # 7b) efekt katmanı: sessizlik vuruşu -> sentetik efektler -> riser -> dosya efektleri -> yoğunluk kapısı
    efektler = []  # {"tur","sn","db"} — yoğunluk kapısı ve rapor için
    yeni_katman = any([a.sfx, a.sfx_dosya, a.riser, a.sessizlik, a.sessizlik_vurusu > 0])
    if yeni_katman:
        mix = raw_oku(P("mix.f32")).copy()
        rng = np.random.default_rng(7)

        def ekle(x, sn, db, tur):
            """x: mono (n,) ya da stereo (n,2), tepe 1'e normalize edilir, dB tepe seviyesiyle karışıma eklenir."""
            x = np.asarray(x, np.float64)
            if x.ndim == 1:
                x = np.stack([x, x], 1)
            x = x / (np.abs(x).max() + 1e-12) * 10 ** (db / 20)
            i0 = int(round(sn * SR))
            j = min(len(mix), i0 + len(x)) - i0
            if j > 0:
                mix[i0:i0 + j] += x[:j]
                efektler.append({"tur": tur, "sn": round(sn, 3), "db": db})

        # sessizlik: müzik+klip kesilir (10 ms çıkış, 5 ms giriş); efektler bundan SONRA eklenir, etkilenmez
        aralik = []
        if a.sessizlik_vurusu > 0 and a.drop_video_sn > 0:
            aralik.append((a.drop_video_sn - a.sessizlik_vurusu, a.drop_video_sn))
        if a.sessizlik:
            aralik += [tuple(float(v) for v in r.split("-")) for r in a.sessizlik.split(",")]
        for b0, b1 in aralik:
            i0, i1 = max(0, int(b0 * SR)), min(len(mix), int(b1 * SR))
            if i1 <= i0:
                continue
            f_out, f_in = int(0.010 * SR), int(0.005 * SR)
            if i0 - f_out >= 0:
                mix[i0 - f_out:i0] *= np.cos(np.linspace(0, np.pi / 2, f_out))[:, None] ** 2
            mix[i0:i1] = 0
            if i1 + f_in <= len(mix):
                mix[i1:i1 + f_in] *= np.sin(np.linspace(0, np.pi / 2, f_in))[:, None] ** 2
        if aralik:
            rapor["sessizlik"] = [[round(b0, 3), round(b1, 3)] for b0, b1 in aralik]

        # sentetik efektler (telifsiz, kodla üretilir)
        def sentez(tur):
            if tur == "tik":  # 25 ms: 3,2 kHz tını + kısa gürültü, hızlı sönüm (ekrana dokunma)
                t = np.arange(int(0.025 * SR)) / SR
                return (np.sin(2 * np.pi * 3200 * t) * 0.6 + rng.standard_normal(len(t)) * 0.4) * np.exp(-t / 0.004)
            if tur == "vurus":  # 60 Hz'e inen bas darbe + 120 ms hava, 0,35 sn (değişim)
                t = np.arange(int(0.35 * SR)) / SR
                f = 60 + 90 * np.exp(-t / 0.03)
                x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)
                return x + rng.standard_normal(len(t)) * np.exp(-t / 0.04) * 0.25
            if tur == "boom":  # vine-boom BENZERİ (sentetik): 45 Hz'e inen doygun bas darbe + 0,9 sn oda kuyruğu
                t = np.arange(int(0.9 * SR)) / SR
                f = 45 + 110 * np.exp(-t / 0.05)
                x = np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 0.22)
                x += rng.standard_normal(len(t)) * np.exp(-t / 0.012) * 0.5          # vuruş transienti
                x += bant(rng.standard_normal(len(t)), 80, 900) * np.exp(-t / 0.28) * 0.12  # kuyruk
                return x
            if tur == "whoosh":  # 0,45 sn gürültü süpürmesi: 300 Hz->5 kHz bant, tepe %60'ta
                L = int(0.45 * SR)
                t = np.arange(L) / SR
                g = np.sin(np.pi * np.clip(t / 0.45, 0, 1) ** 0.7) ** 2
                parcalar = np.array_split(rng.standard_normal(L), 9)
                x = np.concatenate([bant(p, 300 * 1.4 ** k, 1200 * 1.25 ** k) for k, p in enumerate(parcalar)])
                return yumusat(x, 48) * g
            sys.exit(f"bilinmeyen sentetik efekt: {tur} (tik|vurus|boom|whoosh)")

        if a.sfx:
            for parca in a.sfx.split(","):
                tur, sn = parca.split("@")
                ekle(sentez(tur), float(sn), a.sfx_db, tur)
            rapor["sfx"] = a.sfx

        if a.riser:  # drop'ta biten yükseliş: gürültü (200 Hz->6 kHz) + 180->1400 Hz sinüs, üstel zarf, drop'ta kesilir
            kis = a.riser.split(":")
            bit, sure = float(kis[0]), float(kis[1])
            db = float(kis[2]) if len(kis) > 2 else a.sfx_db - 3
            L = int(sure * SR)
            t = np.arange(L) / SR
            u = t / sure
            parcalar = np.array_split(rng.standard_normal(L), 12)
            gur = np.concatenate([bant(p, 200 * 1.3 ** k, 1500 * 1.15 ** k) for k, p in enumerate(parcalar)])
            ton = np.sin(2 * np.pi * np.cumsum(180 * (1400 / 180) ** u) / SR)
            x = (yumusat(gur, 48) * 0.8 + ton * 0.35) * u ** 2.2
            x[:int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))
            ekle(x, bit - sure, db, "riser")
            rapor["riser"] = a.riser

        if a.sfx_dosya:  # dosya tabanlı efektler (lisansı klasörün LISANS.md'sinde kayıtlı olmalı)
            for parca in a.sfx_dosya.split(","):
                yol, kalan = parca.split("@")
                alan = kalan.split(":")
                sn = float(alan[0])
                db = float(alan[1]) if len(alan) > 1 and alan[1] != "" else a.sfx_db
                kirp = alan[2] if len(alan) > 2 else None
                if not os.path.exists(yol) and a.sfx_klasor:
                    yol = os.path.join(a.sfx_klasor, yol)
                if not os.path.exists(yol):
                    sys.exit(f"efekt dosyası yok: {parca}")
                ek = []
                if kirp:
                    k0, k1 = kirp.split("-")
                    ek = ["-ss", k0] + (["-to", k1] if k1 else [])
                hedef = P(f"sfx_{len(efektler)}.f32")
                kos(ek + ["-i", yol, "-vn", "-ac", "2", "-ar", str(SR), "-af", "afade=t=in:d=0.005", "-f", "f32le", hedef])
                x = raw_oku(hedef)
                f_out = min(len(x), int(0.02 * SR))
                x[-f_out:] *= np.cos(np.linspace(0, np.pi / 2, f_out))[:, None] ** 2  # 20 ms çıkış, tık olmasın
                ekle(x, sn, db, os.path.basename(yol))
            rapor["sfx_dosya"] = a.sfx_dosya

        mix.astype(np.float32).tofile(P("mix.f32"))
        rapor["efektler"] = efektler
        rapor["efekt_sayisi"] = len(efektler)
        zamanlar = sorted(e["sn"] for e in efektler)
        yog = max((sum(1 for z in zamanlar if t0 <= z < t0 + 10) for t0 in zamanlar), default=0)
        rapor["efekt_yogunlugu_10sn"] = yog
        yogunluk_asildi = yog > a.sfx_max_10sn
    else:
        yogunluk_asildi = False

    # 8) son seviye: -14 LUFS / -1 dBTP; AAC sonrası ölçerek en çok 4 tur düzelt
    I_mix, _, _ = olc(raw_giris(P("mix.f32")))
    kaz = a.hedef_lufs - I_mix
    tavan = a.tepe - 0.5
    for tur in range(4):
        lim = 10 ** (tavan / 20)
        kos(raw_giris(P("mix.f32")) + ["-af",
            f"volume={kaz:.2f}dB,aresample=192000,alimiter=limit={lim:.5f}:attack=1:release=60:level=0:latency=1,"
            f"aresample={SR}", "-f", "f32le", "-ar", str(SR), "-ac", "2", P("son.f32")])
        kos(["-i", a.video] + raw_giris(P("son.f32")) + ["-map", "0:v:0", "-map", "1:a", "-c:v", "copy",
            "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-shortest", "-movflags", "+faststart", P("cikti.mp4")])
        I, LRA, TP = olc(["-i", P("cikti.mp4")])
        print(f"tur {tur+1}: I={I} LUFS  LRA={LRA}  TP={TP} dBTP  (kazanç {kaz:+.2f} dB, tavan {tavan:.2f})")
        ok_I = abs(I - a.hedef_lufs) <= 0.5
        ok_T = TP <= a.tepe
        if ok_I and ok_T:
            break
        if not ok_T:
            tavan -= (TP - a.tepe) + 0.2
        if not ok_I:
            kaz += a.hedef_lufs - I
    os.makedirs(os.path.dirname(os.path.abspath(a.cikti)), exist_ok=True)
    shutil.copy(P("cikti.mp4"), a.cikti)
    rapor.update({"cikti": a.cikti, "I_lufs": I, "LRA": LRA, "true_peak_dbtp": TP,
                  "hedef_tuttu": bool(ok_I and ok_T)})
    if yogunluk_asildi:  # efekt yoğunluğu kapısı: 10 sn'de > --sfx_max_10sn efekt "ucuz" hissi verir
        print(f"UYARI efekt yoğunluğu: 10 sn'de {rapor['efekt_yogunlugu_10sn']} efekt > {a.sfx_max_10sn} — "
              "efekt sil ya da --sfx_max_10sn'yi gerekçesiyle yükselt", file=sys.stderr)
        rapor["hedef_tuttu"] = False
    # drop kapısı: drop anındaki ses artışı karışımda ÖLÇÜLÜR (müzik dosyasındaki drop yetmez)
    if a.muzik and a.drop_video_sn > 0:
        son = raw_oku(P("son.f32")).mean(1)
        d = int(a.drop_video_sn * SR)
        rr = lambda v: np.sqrt(np.mean(v ** 2) + 1e-20)
        artis = 20 * np.log10(rr(son[d:d + int(0.43 * SR)]) / rr(son[max(0, d - int(0.6 * SR)):d - int(0.05 * SR)]))
        rapor["drop_artis_db"] = round(float(artis), 1)
        rapor["drop_tuttu"] = bool(artis >= a.drop_esik_db)
        if not rapor["drop_tuttu"]:
            print(f"UYARI drop duyulmuyor: {artis:+.1f} dB < {a.drop_esik_db} dB — --drop_oncesi_db'yi düşür, "
                  "drop öncesi planların ses_db'sini kıs ya da --muzik_db'yi artır", file=sys.stderr)
            rapor["hedef_tuttu"] = False
    if muzik:
        rapor["muzik_giris"] = muzik_giris(raw_oku(P("muz.f32")).mean(1), SR, karisim=raw_oku(P("son.f32")).mean(1))
    if "muzik_giris" in rapor and not rapor["muzik_giris"]["tuttu"]:
        print("UYARI müzik girişi: " + rapor["muzik_giris"]["neden"] + " — müziği 0. sn'den başlat "
              "(--muzik_bas > --drop_video_sn), --muzik_fade_in 1,5–2; açılışa diegetik ses (klip sesi/efekt); "
              "kısık/boğuk yatak + tam drop tarifi YASAK",
              file=sys.stderr)
        rapor["hedef_tuttu"] = False
    if a.stem_klasoru:
        os.makedirs(a.stem_klasoru, exist_ok=True)
        for ad in ["egz.f32", "muz.f32", "muz_duck.f32", "mix.f32", "olay.f32"]:
            if os.path.exists(P(ad)):
                kos(raw_giris(P(ad)) + [os.path.join(a.stem_klasoru, ad.replace(".f32", ".wav"))])
    shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps(rapor, ensure_ascii=False, indent=1))
    sys.exit(0 if rapor["hedef_tuttu"] else 2)


if __name__ == "__main__":
    main()
