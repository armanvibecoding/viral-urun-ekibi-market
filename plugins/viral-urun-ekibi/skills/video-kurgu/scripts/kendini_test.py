#!/usr/bin/env python3
"""Kurulum + uçtan uca öz-test (kredi harcamaz, internet gerekmez).

Yapar: 3 adet 4 sn 720x1280 renkli test klibi (ses tonlu) + 1 sıçramalı klip üretir -> klip_qc'nin temizleri
geçirip sıçramayı YAKALADIĞINI ölçer -> Türkçe kanca + pazara göre CTA + efektle kurgular -> süre/çözünürlük/LUFS
ölçer -> ara kareyi PNG olarak çıkarır (Türkçe harflere gözle bak).

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
    for ad, ok in sonuc:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    print("klasör:", d)
    sys.exit(0 if all(ok for _, ok in sonuc) else 1)


if __name__ == "__main__":
    main()
