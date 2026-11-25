#!/usr/bin/env python3
"""İndirme alımı yardımcısı: tarayıcının indirme klasöründen YALNIZ bu işin başladığı andan sonra inen, beklenen adda ve
yeterli boyutta dosyayı alır; eski (kurucuya ya da başka işe ait) dosyaya DOKUNMAZ.

Neden (2026-11-25 sınav 05): indirme betiği klasördeki eski bir kurucu dosyasını taşıdı. Bu yardımcı hiçbir dosyayı taşımaz/silmez;
seçilen YENİ dosyayı hedef klasöre KOPYALAR (`--tasi` ile açıkça istenirse yalnız o yeni dosya taşınır).

  python3 indirme_al.py --kaynak ~/Downloads --hedef is/05/ham --baslangic simdi-5 --ad 'galeri-*.png' [--min-boyut 20000]
         [--bekle 60] [--yeni-ad galeri-1.png] [--tasi]
--baslangic   alım penceresinin başı: ISO zaman (2026-11-25T03:10:00), epoch saniye ya da `simdi-N` (N saniye önce). İndirmeyi
              BAŞLATMADAN önce `date +%s` ile not al; bu andan önceki mtime/oluşturma zamanlı dosya aday değildir.
--ad          kabuk deseni (fnmatch); `.crdownload`, `.part`, `.tmp`, `.download` uzantıları her zaman yok sayılır.
--min-boyut   bayt; altındaki dosya (yarım/boş) aday değildir. Boyut 1 sn arayla iki ölçümde aynı olmalı (inme bitmiş).
Çıkış: 0 alındı (satır: ad · boyut · zaman) · 1 süre doldu, yeni uygun dosya yok (eski dosyalara dokunulmadı) · 2 kullanım hatası.
"""
import argparse
import datetime
import fnmatch
import os
import shutil
import sys
import time

YARIM = (".crdownload", ".part", ".tmp", ".download", ".partial")


def baslangic_zamani(s):
    s = s.strip()
    if s.startswith("simdi-"):
        return time.time() - float(s[6:])
    try:
        return float(s)
    except ValueError:
        return datetime.datetime.fromisoformat(s).timestamp()


def zaman(yol):
    st = os.stat(yol)
    return max(st.st_mtime, getattr(st, "st_birthtime", 0) or 0)


def adaylar(kaynak, desen, bas, min_boyut):
    out = []
    for ad in os.listdir(kaynak):
        y = os.path.join(kaynak, ad)
        if not os.path.isfile(y) or ad.lower().endswith(YARIM) or not fnmatch.fnmatch(ad, desen):
            continue
        if zaman(y) < bas or os.path.getsize(y) < min_boyut:
            continue
        out.append(y)
    return sorted(out, key=zaman, reverse=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kaynak", required=True); ap.add_argument("--hedef", required=True)
    ap.add_argument("--baslangic", required=True); ap.add_argument("--ad", required=True)
    ap.add_argument("--min-boyut", type=int, default=1024); ap.add_argument("--bekle", type=float, default=60)
    ap.add_argument("--yeni-ad"); ap.add_argument("--tasi", action="store_true")
    a = ap.parse_args()
    kaynak, hedef = os.path.expanduser(a.kaynak), os.path.expanduser(a.hedef)
    if not os.path.isdir(kaynak):
        print("HATA: kaynak klasör yok: %s" % kaynak, file=sys.stderr)
        return 2
    try:
        bas = baslangic_zamani(a.baslangic)
    except (ValueError, TypeError):
        print("HATA: --baslangic anlaşılamadı: %s" % a.baslangic, file=sys.stderr)
        return 2
    bitis = time.time() + a.bekle
    while True:
        aday = adaylar(kaynak, a.ad, bas, a.min_boyut)
        if aday:
            y = aday[0]
            b1 = os.path.getsize(y)
            time.sleep(1.0)
            if os.path.exists(y) and os.path.getsize(y) == b1 and not os.path.exists(y + ".crdownload"):
                os.makedirs(hedef, exist_ok=True)
                son = os.path.join(hedef, a.yeni_ad or os.path.basename(y))
                if os.path.exists(son):
                    print("HATA: hedefte aynı adlı dosya var, üzerine yazılmaz: %s" % son, file=sys.stderr)
                    return 2
                (shutil.move if a.tasi else shutil.copy2)(y, son)
                print("alındı: %s · %d bayt · %s" % (son, b1, datetime.datetime.fromtimestamp(zaman(y) if os.path.exists(y) else time.time()).isoformat(timespec="seconds")))
                return 0
        if time.time() >= bitis:
            print("YOK: %s içinde %s sonrası, '%s' desenli, ≥ %d bayt yeni dosya yok (eski dosyalara dokunulmadı)"
                  % (kaynak, datetime.datetime.fromtimestamp(bas).isoformat(timespec="seconds"), a.ad, a.min_boyut), file=sys.stderr)
            return 1
        time.sleep(1.0)


if __name__ == "__main__":
    sys.exit(main())
