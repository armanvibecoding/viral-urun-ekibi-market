#!/usr/bin/env python3
"""Kurulum + uçtan uca öz-test (kredi harcamaz, internet gerekmez).

Yapar: 3 adet 4 sn 720x1280 renkli test klibi (ses tonlu) + 1 sıçramalı klip üretir -> klip_qc'nin temizleri
geçirip sıçramayı YAKALADIĞINI ölçer -> Türkçe kanca + pazara göre CTA + efektle kurgular -> süre/çözünürlük/LUFS
ölçer -> ara kareyi PNG olarak çıkarır (Türkçe harflere gözle bak) -> müzik girişi kapısını kırarak sınar
(−30 dB'den 1,75 sn rampalı müzik GEÇER; geç başlayan müzik, kısık yatak + tam drop, rampasız açılış KALIR;
ses_tasarla uçtan uca: müzik 0'dan → 0, müzik 4. sn'de → 2, açılışta diegetik ses yok → 2) -> ses_olc --kapi
(delik → 3, +10 dB üstü sıçrama → 4) ve kurgu_kontrol --goruntu (bildirilmemiş kesim / son 2 sn gürültü → 3) kırılarak sınanır.

Kullanım: python3 kendini_test.py [--klasor <çıktı_klasörü>]   (varsayılan: geçici klasör)
Çıkış kodu 0 = hepsi geçti.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)
import ffaraclar as F  # noqa: E402


def klip(yol, renk, frek, sure=4):
    F.calistir([F.ffmpeg_bul(), "-v", "error", "-y", "-f", "lavfi", "-i",
                f"color=c={renk}:s=720x1280:r=24:d={sure},noise=alls=10:allf=t",
                "-f", "lavfi", "-i", f"sine=frequency={frek}:duration={sure}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", yol])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--klasor")
    a = ap.parse_args()
    d = os.path.abspath(a.klasor or tempfile.mkdtemp(prefix="kurgu_test_"))
    os.makedirs(os.path.join(d, "klipler"), exist_ok=True)
    os.makedirs(os.path.join(d, ".ekip"), exist_ok=True)
    py = sys.executable
    sonuc = []

    print("ffmpeg:", F.ffmpeg_bul())
    font = F.font_test(os.path.join(d, "font_testi.png"))
    print("font:", font, "-> font_testi.png")

    for ad, renk, frek in (("S1", "0x2a6f97", 330), ("S2", "0x7a3e9d", 440), ("S3", "0x2e8b57", 550)):
        klip(os.path.join(d, "klipler", f"V01_{ad}.mp4"), renk, frek)
    # sıçramalı klip: 2 sn koyu + 2 sn açık (klip içi gizli kesme benzeri)
    k1, k2 = os.path.join(d, "klipler", "_a.mp4"), os.path.join(d, "klipler", "_b.mp4")
    klip(k1, "0x202020", 300, 2)
    klip(k2, "0xe0e0e0", 300, 2)
    liste = os.path.join(d, "klipler", "_liste.txt")
    with open(liste, "w", encoding="utf-8") as f:
        f.write(f"file '{os.path.basename(k1)}'\nfile '{os.path.basename(k2)}'\n")
    F.calistir([F.ffmpeg_bul(), "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-c", "copy",
                os.path.join(d, "klipler", "SICRAMA.mp4")])
    # efekt: kullanıcı kendi telifsiz sesini koyar; testte sentetik tık
    F.calistir([F.ffmpeg_bul(), "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=1200:duration=0.15",
                os.path.join(d, "tik.wav")])

    temiz = [os.path.join(d, "klipler", f"V01_S{i}.mp4") for i in (1, 2, 3)]
    r = subprocess.run([py, os.path.join(BURASI, "klip_qc.py")] + temiz + ["--pano"])
    sonuc.append(("klip_qc temiz klipler -> 0", r.returncode == 0))
    r = subprocess.run([py, os.path.join(BURASI, "klip_qc.py"), os.path.join(d, "klipler", "SICRAMA.mp4")])
    sonuc.append(("klip_qc sıçramalı klip -> 1 (kapı kırılınca tutuyor)", r.returncode == 1))

    with open(os.path.join(d, ".ekip", "KARARLAR.md"), "w", encoding="utf-8") as f:
        f.write("# KARARLAR\n- 2000-01-01 | pazar | Türkiye\n")
    ayar = {"planlar": [["klipler/V01_S1.mp4", 0, 4.0], ["klipler/V01_S2.mp4", 0, 4.0], ["klipler/V01_S3.mp4", 0, 4.0]],
            "kanca": "Kedim bunu görünce aklı gitti 😂 / ÇĞİÖŞÜ çğıöşü", "cta_kelime": "PİYANO",
            "sfx": [{"dosya": "tik.wav", "sn": 5.0, "db": -6, "hizala": True}], "cikti": "kurgu/V01.mp4"}
    with open(os.path.join(d, "ayar.json"), "w", encoding="utf-8") as f:
        json.dump(ayar, f, ensure_ascii=False, indent=1)
    r = subprocess.run([py, os.path.join(BURASI, "kurgu.py"), os.path.join(d, "ayar.json"), "--proje", d])
    sonuc.append(("kurgu.py çıkış 0", r.returncode == 0))

    cikti = os.path.join(d, "kurgu", "V01.mp4")
    if os.path.exists(cikti):
        m = F.medya_bilgi(cikti)
        lufs = F.lufs_olc(cikti)
        print(f"ÖLÇÜM: süre {m['sure']:.2f} sn · {m['w']}x{m['h']} · ses {m['ses']} · {lufs:.1f} LUFS")
        sonuc.append(("süre 12 ± 0,1 sn", abs(m["sure"] - 12.0) <= 0.1))
        sonuc.append(("çözünürlük 1080x1920", (m["w"], m["h"]) == (1080, 1920)))
        sonuc.append(("ses −14 ± 1 LUFS", abs(lufs + 14) <= 1.0))
        kare = os.path.join(d, "ara_kare_10sn.png")
        F.calistir([F.ffmpeg_bul(), "-v", "error", "-y", "-ss", "10", "-i", cikti, "-frames:v", "1", kare])
        print("ara kare (kanca + CTA görünmeli, Türkçe harflere bak):", kare)

        # müzik girişi kapısı (2026-11-17 kurucu geri bildirimi: "müzik bir anda açılıyor") — önce kır, sonra geçir
        import numpy as np
        from ses_olc import muzik_giris
        sr = 48000
        t = np.arange(int(14 * sr)) / sr
        muz = 0.3 * np.sin(2 * np.pi * 220 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 2 * t))
        fade = np.where(t < 1.75, 10 ** ((-30 + 30 * t / 1.75) / 20), 1.0)  # −30 dB -> yatak, dB-doğrusal
        gec = muz.copy(); gec[t < 5] = 0                                    # 5. sn'ye kadar müzik yok
        yatak = muz * np.where(t < 7, 10 ** (-20 / 20), 1)                  # kısık yatak, 7. sn'de tam (drop)
        for ad, x, bek in (("−30 dB'den 1,75 sn rampa", muz * fade, True), ("5. sn'de başlayan müzik", gec, False),
                           ("kısık yatak + 7. sn'de tam drop", yatak * fade, False), ("rampasız tam açılış", muz, False)):
            r = muzik_giris(x, sr)
            sonuc.append((f"müzik girişi kapısı: {ad} -> {'tuttu' if bek else 'KALDI'} ({r.get('neden', 'temiz')})",
                          r["tuttu"] == bek))
        mp = os.path.join(d, "muzik.wav")
        F.calistir([F.ffmpeg_bul(), "-v", "error", "-y", "-f", "lavfi", "-i",
                    "aevalsrc=0.3*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*2*t)):s=48000:d=20", mp])
        sessiz = os.path.join(d, "kurgu", "V01_sessiz.mp4")
        F.calistir([F.ffmpeg_bul(), "-v", "error", "-y", "-i", cikti, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-shortest", sessiz])
        for ad, vid, bas, drop, bek in (("ses_tasarla müzik 0'dan", cikti, 6.0, 3.0, 0),
                                        ("ses_tasarla müzik 4. sn'de başlıyor", cikti, 0.0, 4.0, 2),
                                        ("ses_tasarla açılışta diegetik ses yok (sessiz klip)", sessiz, 6.0, 3.0, 2)):
            r = subprocess.run([py, os.path.join(BURASI, "ses_tasarla.py"), "--video", vid, "--muzik", mp,
                                "--muzik_bas", str(bas), "--drop_video_sn", str(drop), "--drop_esik_db", "-99",
                                "--patlama_db", "0", "--crackle_db", "0", "--kesmeler", "yok",
                                "--cikti", os.path.join(d, "kurgu", f"ses_{len(sonuc)}.mp4")], capture_output=True, text=True)
            sonuc.append((f"{ad} -> çıkış {bek}", r.returncode == bek))
    # ses_olc --kapi: delik → 3, drop dışı sıçrama > +10 dB → 4 (2026-11-18 eleştirmen reçeteleri) — önce kır
    ff = F.ffmpeg_bul()
    for ad, ifade, bek in (("temiz ton", "0.3*sin(2*PI*220*t)", 0),
                           ("0,5 sn ses deliği", "0.3*sin(2*PI*220*t)*(1-between(t,3,3.5))", 3),
                           ("+20 dB ani sıçrama (3. sn)", "(0.03+0.27*gte(t,3))*sin(2*PI*220*t)", 4)):
        w = os.path.join(d, f"ses_kapi_{bek}.wav")
        F.calistir([ff, "-v", "error", "-y", "-f", "lavfi", "-i", f"aevalsrc='{ifade}':s=48000:d=6", w])
        r = subprocess.run([py, os.path.join(BURASI, "ses_olc.py"), w, "--kapi"], capture_output=True, text=True)
        sonuc.append((f"ses_olc --kapi {ad} -> çıkış {bek}", r.returncode == bek))
    # kurgu_kontrol --goruntu: kesim dışı RGB sıçraması / son 2 sn gürültü → 3
    kl = os.path.join(d, "klipler")
    gur = os.path.join(kl, "_gurultu.mp4")
    F.calistir([ff, "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x2a6f97:s=720x1280:r=24:d=4,noise=alls=10:allf=t",
                "-f", "lavfi", "-i", "color=c=0x2a6f97:s=720x1280:r=24:d=2,noise=alls=70:allf=t",
                "-filter_complex", "[0][1]concat=n=2:v=1[v]", "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", gur])
    for ad, yol, kes, bek in (("temiz klip", os.path.join(kl, "V01_S1.mp4"), None, 0),
                              ("bildirilmemiş kesim (koyu→açık)", os.path.join(kl, "SICRAMA.mp4"), None, 3),
                              ("aynı sıçrama kesim olarak bildirilince", os.path.join(kl, "SICRAMA.mp4"), "2.0", 0),
                              ("son 2 sn gürültü artışı (kesim bildirilse de)", gur, "4.0", 3)):
        cmd = [py, os.path.join(BURASI, "kurgu_kontrol.py"), "--goruntu", yol] + (["--kesimler", kes] if kes else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        sonuc.append((f"kurgu_kontrol --goruntu {ad} -> çıkış {bek}", r.returncode == bek))
    for ad, ok in sonuc:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    print("klasör:", d)
    sys.exit(0 if all(ok for _, ok in sonuc) else 1)


if __name__ == "__main__":
    main()
