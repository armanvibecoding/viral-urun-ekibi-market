#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""on_ucus.py kırma testleri. Kullanım: python3 on_ucus_test.py → 0 hepsi doğru · 1 bir kapı tutmadı.

Bu gecenin 6 ilk-tur kaybından (V6) ön uçuşun ÜRETİMDEN ÖNCE yakalaması gerekenler (en az 4): 01 malzemesiz · 02 K14/K15 başlığı yok · 07 referans yok ·
07 ölçüm aracı yok · 05 Tesseract yok (K2 TR ölçülemez). Her kapı önce kötü girdiyle ≠ 0 (kırma), sonra iyi girdiyle çıkış 0/3 (GEÇTİ ya da ölçülemez-liste) görülür.
"""
import os
import shutil
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
BETIK = os.path.join(BURADA, "on_ucus.py")
REF = os.path.join(os.path.dirname(BURADA), "skills", "studio", "referans")
sonuclar = []


def kos(args, env=None):
    r = subprocess.run([sys.executable, BETIK] + args, capture_output=True, text=True, env=dict(os.environ, **(env or {})))
    return r.returncode, r.stdout + r.stderr


def bekle(ad, rc, beklenen, cikti, parca=None, yok=None):
    ok = rc in (beklenen if isinstance(beklenen, tuple) else (beklenen,)) and (parca is None or parca in cikti) and (yok is None or yok not in cikti)
    sonuclar.append(ok)
    print("%s %s → çıkış %d%s" % ("GEÇTİ" if ok else "KALDI", ad, rc, "" if ok else "\n    beklenen %s parça=%r yok=%r\n    %s" % (beklenen, parca, yok, cikti.strip().replace("\n", "\n    ")[-500:])))


def yaz(y, m):
    os.makedirs(os.path.dirname(y), exist_ok=True)
    with open(y, "w", encoding="utf-8") as f:
        f.write(m)


def main():
    with tempfile.TemporaryDirectory() as k:
        # --- 01: malzemesiz iş
        bos = os.path.join(k, "is", "01-urun")
        os.makedirs(bos)
        rc, c = kos(["malzeme", bos])
        bekle("malzeme: KAYNAK.tsv yok", rc, 1, c, "KAYNAK.tsv yok")
        iyi = os.path.join(k, "is", "02-urun")
        yaz(os.path.join(iyi, "KAYNAK.tsv"), "vaka\tdosya\tkaynak\tcekim\tkullanilacak_aralik\tnot\tlisans\tkullanim\tyapay_mi\tbakildi\n"
            "a\tklip1.mp4\tkurucu\tel\t0:00-0:10\t-\tkurucu\tyayin\thayir\t2026-11-25\n")
        rc, c = kos(["malzeme", iyi, "--yayin"])
        bekle("malzeme: satır var ama dosya yok", rc, 1, c, "dosya yok")
        yaz(os.path.join(iyi, "klip1.mp4"), "x")
        rc, c = kos(["malzeme", iyi, "--yayin"])
        bekle("malzeme: dosya + lisans tam → hazır", rc, 0, c, "HAZIR")
        yaz(os.path.join(iyi, "KAYNAK.tsv"), "vaka\tdosya\tkaynak\tcekim\tkullanilacak_aralik\tnot\nx\tklip1.mp4\ttedarikçi\t-\t0:00-0:10\t-\n")
        rc, c = kos(["malzeme", iyi, "--yayin"])
        bekle("malzeme: --yayin lisans sütunları boş → EKSİK", rc, 1, c, "lisans/kullanim/yapay_mi/bakildi eksik")
        rc, c = kos(["malzeme", iyi])
        bekle("malzeme: sınav modunda lisans boş → ölçülemez listesi (çıkış 3)", rc, 3, c, "lisans kapısı KALIR")
        # --- 02: kütüphanede K14/K15 başlığı yok
        ref = os.path.join(k, "ref")
        shutil.copytree(REF, ref)
        kut = os.path.join(ref, "kanca-kutuphanesi.md")
        m = open(kut, encoding="utf-8").read()
        import re
        m2 = re.sub(r"^### K1[45]\. .*$", "#### (başlık yok)", m, flags=re.M)
        yaz(kut, m2)
        rc, c = kos(["kutuphane"], env={"ON_UCUS_REF": ref})
        bekle("kütüphane: K14/K15 başlığı silindi", rc, 1, c, "K14, K15")
        rc, c = kos(["kutuphane"])
        bekle("kütüphane: gerçek kütüphane tam", rc, 0, c, "HAZIR")
        # --- 07: referans yok / var
        tsv = os.path.join(k, "referanslar.tsv")
        yaz(tsv, "id\tpazar\thesap\tkaynak_url\tolcum\ttur\tkare_panosu_yolu\tnot\n")
        rc, c = kos(["referans", "--tsv", tsv, "--pazar", "US", "--tur", "site"])
        bekle("referans: TSV boş", rc, 1, c, "0/3")
        satirlar = "".join("R%d\tUS\th\t\t1/1\tsite\tpano%d\t-\n" % (i, i) for i in range(1, 4))
        yaz(tsv, "id\tpazar\thesap\tkaynak_url\tolcum\ttur\tkare_panosu_yolu\tnot\n" + satirlar)
        kok = os.path.join(k, "kok")
        rc, c = kos(["referans", "--tsv", tsv, "--pazar", "US", "--tur", "site", "--referans-kok", kok])
        bekle("referans: satır var ama kare panosu klasörü yok", rc, 1, c, "0/3")
        for i in range(1, 4):
            os.makedirs(os.path.join(kok, "pano%d" % i))
        rc, c = kos(["referans", "--tsv", tsv, "--pazar", "US", "--tur", "site", "--referans-kok", kok])
        bekle("referans: 3 çözülen pano → hazır", rc, 0, c, "HAZIR")
        rc, c = kos(["referans", "--tsv", tsv, "--pazar", "TR", "--tur", "site", "--referans-kok", kok])
        bekle("referans: pazar uyumsuz (TR için yalnız TR sayılır)", rc, 1, c, "0/3")
        # --- 07: ölçüm aracı yok
        rc, c = kos(["arac", "--icin", "site"], env={"WEB_OLCUM_DIZIN": os.path.join(k, "yok")})
        bekle("araç(site): Lighthouse/axe klasörü yok", rc, 1, c, "web-olcum")
        # --- 05: Tesseract yok → K2 TR olculemez (başlanabilir ama listelenir)
        rc, c = kos(["arac", "--icin", "gorsel"], env={"OCR_TESSERACT": os.path.join(k, "tesseract-yok"), "PATH": "/usr/bin:/bin"})
        bekle("araç(gorsel): Tesseract yok → ölçülemez listesi ya da başka eksik", rc, (1, 3), c, "tesseract")
        # --- bütün araç tablosunda bilinmeyen grup / komut hatası
        rc, c = kos(["arac", "--icin", "yok"])
        bekle("kullanım hatası → çıkış 2", rc, 2, c)
    kalan = sonuclar.count(False)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuclar), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
