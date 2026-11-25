#!/usr/bin/env python3
"""profil.py: danışanın işletme profili (yalnız Python 3 standart kütüphanesi). Tek dosya: <proje>/.ekip/isletme-profili.tsv

Kullanım:
  profil.py goster [--profil DOSYA]                         profildeki değerleri yazar (dosya yoksa "profil yok", çıkış 0)
  profil.py yaz anahtar=deger [anahtar=deger ...] [--profil DOSYA]   doğrulayıp dosyaya yazar (aynı anahtar güncellenir)
  profil.py yol                                              profil dosyasının aranan yolunu yazar

Anahtarlar (hepsi isteğe bağlı; yazılmayan anahtar için eklenti varsayılanı kullanılır):
  kapida_odeme_orani_yuzde  satışların yüzde kaçı kapıda ödeme (0-100; kapıda ödeme yoksa 0)
  kapida_ek_ucret           kapıda ödeme başına ek ücret (TL, >= 0)
  kat_min                   hedef satış / alış katı alt sınırı (>= 1)
  satis_tl_min              en düşük satış fiyatı (TL, >= 0)
  marka_roas                markanın kendi reklam hesabındaki gerçek ROAS (> 0; bilmiyorsan yazma)
  kanal                     shopify | pazar-yeri

Dosya yolu önceliği: --profil > VUE_PROFIL ortam değişkeni > $CLAUDE_PROJECT_DIR/.ekip/isletme-profili.tsv > ./.ekip/isletme-profili.tsv.
Bozuk değer (sayı değil, aralık dışı, bilinmeyen anahtar) sessiz geçilmez: ProfilHatasi / çıkış 1.
Çıkış: 0 tamam · 1 profil hatası · 2 kullanım.
"""
import csv
import datetime
import os
import sys

DOSYA_ADI = "isletme-profili.tsv"
BASLIK = ["anahtar", "deger", "tarih"]
# anahtar -> (alt, üst, alt_dahil)  None = sınır yok
SAYISAL = {
    "kapida_odeme_orani_yuzde": (0.0, 100.0, True),
    "kapida_ek_ucret": (0.0, None, True),
    "kat_min": (1.0, None, True),
    "satis_tl_min": (0.0, None, True),
    "marka_roas": (0.0, None, False),
}
KANALLAR = ("shopify", "pazar-yeri")
ANAHTARLAR = tuple(SAYISAL) + ("kanal",)


class ProfilHatasi(ValueError):
    pass


def yol_bul(acik=None):
    if acik:
        return acik
    if os.environ.get("VUE_PROFIL"):
        return os.environ["VUE_PROFIL"]
    kok = os.environ.get("CLAUDE_PROJECT_DIR") or "."
    return os.path.join(kok, ".ekip", DOSYA_ADI)


def dogrula(anahtar, deger):
    """Doğru değeri (float ya da kanal metni) döner; bozuksa ProfilHatasi."""
    d = (deger or "").strip().replace(",", ".")
    if anahtar == "kanal":
        if d.lower() not in KANALLAR:
            raise ProfilHatasi("kanal %r geçersiz; izinli: %s" % (deger, ", ".join(KANALLAR)))
        return d.lower()
    if anahtar not in SAYISAL:
        raise ProfilHatasi("bilinmeyen profil anahtarı %r; izinli: %s" % (anahtar, ", ".join(ANAHTARLAR)))
    try:
        v = float(d)
    except ValueError:
        raise ProfilHatasi("%s sayı değil: %r" % (anahtar, deger))
    alt, ust, alt_dahil = SAYISAL[anahtar]
    if v != v or v in (float("inf"), float("-inf")):
        raise ProfilHatasi("%s geçersiz sayı: %r" % (anahtar, deger))
    if (v < alt) or (v == alt and not alt_dahil) or (ust is not None and v > ust):
        raise ProfilHatasi("%s aralık dışı: %g" % (anahtar, v))
    return v


def oku(yol=None):
    """{anahtar: değer}. Dosya yoksa {} (varsayılan eklenti değerleri geçerli). Satır bozuksa ProfilHatasi."""
    yol = yol_bul(yol)
    if not os.path.isfile(yol):
        return {}
    out = {}
    with open(yol, encoding="utf-8-sig", newline="") as f:
        for no, r in enumerate(csv.reader(f, delimiter="\t"), 1):
            if not any(h.strip() for h in r) or r[0].strip().startswith("#"):
                continue
            if no == 1 and r[0].strip() == "anahtar":
                continue
            r = r + [""] * 3
            a, d = r[0].strip(), r[1].strip()
            if d == "":
                continue  # boş = "bilmiyorum": varsayılan kullanılır
            try:
                out[a] = dogrula(a, d)
            except ProfilHatasi as e:
                raise ProfilHatasi("%s:%d: %s" % (yol, no, e))
    return out


def yaz(degerler, yol=None):
    yol = yol_bul(yol)
    mevcut = {}
    if os.path.isfile(yol):
        mevcut = oku(yol)
    for a, d in degerler.items():
        mevcut[a] = dogrula(a, str(d))
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    bugun = datetime.date.today().isoformat()
    with open(yol, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(BASLIK)
        for a in ANAHTARLAR:
            if a in mevcut:
                v = mevcut[a]
                w.writerow([a, ("%g" % v) if isinstance(v, float) else v, bugun])
    return yol


def ozet(p):
    return ", ".join("%s=%s" % (a, ("%g" % v) if isinstance(v, float) else v) for a, v in p.items())


def main(argv):
    args = argv[1:]
    yol = None
    if "--profil" in args:
        i = args.index("--profil")
        yol = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    try:
        if args[0] == "yol":
            print(yol_bul(yol))
            return 0
        if args[0] == "goster":
            p = oku(yol)
            print("profil: " + (ozet(p) if p else "yok (eklenti varsayılanları kullanılır)"))
            return 0
        if args[0] == "yaz" and len(args) > 1:
            d = {}
            for kv in args[1:]:
                if "=" not in kv:
                    raise ProfilHatasi("anahtar=deger biçimi bekleniyor: %r" % kv)
                a, v = kv.split("=", 1)
                d[a.strip()] = v
            print("yazıldı: %s" % yaz(d, yol))
            return 0
    except (ProfilHatasi, OSError) as e:
        print("HATA: %s" % e)
        return 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
