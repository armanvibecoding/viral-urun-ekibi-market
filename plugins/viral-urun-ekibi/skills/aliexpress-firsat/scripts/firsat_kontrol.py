#!/usr/bin/env python3
"""aliexpress-firsat yardimcisi (yalniz Python 3 standart kutuphanesi; macOS / Windows / Linux).

Alt komutlar:
  tekrar  KLASOR TERIM...      Aday daha once is/firsat/ altinda gecmis mi? (AliExpress linki, urun no veya kelime)
  denetle ADAYLAR.md           Aday tablosunu kurallara gore denetler, DNA ve sira puanini hesaplar
  sinama  ADAYLAR.md [--n 3] [--tohum N]
                               Dogrulama icin rastgele N satir secer (sayi kaynagindan acilip kontrol edilir)

Cikis kodu: 0 = sorun yok, 1 = denetimde hata var / tekrar bulundu, 2 = kullanim hatasi.
"""
import os
import random
import re
import sys

ITEM_RE = re.compile(r"(?:item/|/i/|productId=)(\d{9,20})")
DNA_ESIK = 4
SAT_ESIK = 8
IZLE_ESIK = 6


def urun_no(metin):
    m = ITEM_RE.search(metin)
    if m:
        return m.group(1)
    if re.fullmatch(r"\d{9,20}", metin.strip()):
        return metin.strip()
    return None


def md_dosyalari(klasor):
    for kok, _, dosyalar in os.walk(klasor):
        for d in sorted(dosyalar):
            if d.lower().endswith((".md", ".txt", ".tsv", ".csv")):
                yield os.path.join(kok, d)


def tekrar(klasor, terimler):
    if not os.path.isdir(klasor):
        print(f"KLASOR YOK: {klasor} -> ilk tur, tekrar kontrolu bos gecti.")
        return 0
    bulundu = False
    for terim in terimler:
        no = urun_no(terim)
        aranan = no if no else terim.lower()
        eslesme = []
        for yol in md_dosyalari(klasor):
            with open(yol, encoding="utf-8", errors="replace") as f:
                for i, satir in enumerate(f, 1):
                    hedef = satir if no else satir.lower()
                    if aranan in hedef:
                        eslesme.append(f"  {yol}:{i}: {satir.strip()[:160]}")
        if eslesme:
            bulundu = True
            print(f"DAHA ONCE GORULDU: {terim}")
            print("\n".join(eslesme[:10]))
        else:
            print(f"YENI: {terim}")
    return 1 if bulundu else 0


def tablo_oku(yol):
    """Markdown tablosundaki satirlari {baslik: deger} sozlugu olarak dondurur (ilk tablo basligina gore)."""
    with open(yol, encoding="utf-8", errors="replace") as f:
        satirlar = [s.rstrip("\n") for s in f]
    baslik, kayitlar = None, []
    for no, s in enumerate(satirlar, 1):
        if not s.strip().startswith("|"):
            continue
        hucre = [h.strip() for h in s.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", h) for h in hucre if h):
            continue
        if baslik is None:
            baslik = [h.lower() for h in hucre]
            continue
        if len(hucre) != len(baslik):
            kayitlar.append({"_satir": no, "_hata": f"sutun sayisi {len(hucre)} (baslik {len(baslik)})"})
            continue
        k = dict(zip(baslik, hucre))
        k["_satir"] = no
        kayitlar.append(k)
    return baslik or [], kayitlar


def sutun(k, *adlar):
    for anahtar, deger in k.items():
        if anahtar.startswith("_"):
            continue
        if any(a in anahtar for a in adlar):
            return deger
    return ""


def sayi(metin):
    m = re.search(r"-?\d+(?:[.,]\d+)?", metin or "")
    return float(m.group(0).replace(",", ".")) if m else None


def dna_say(metin):
    metin = (metin or "").upper()
    if re.fullmatch(r"[01]{7}", metin.replace(" ", "")):
        return metin.replace(" ", "").count("1")
    return len(set(re.findall(r"V([1-7])", metin)))


def denetle(yol):
    baslik, kayitlar = tablo_oku(yol)
    if not kayitlar:
        print(f"TABLO BULUNAMADI: {yol}")
        return 1
    hata = 0
    gorulen = {}
    for k in kayitlar:
        etiket = f"satir {k['_satir']}"
        if "_hata" in k:
            print(f"HATA {etiket}: {k['_hata']}")
            hata += 1
            continue
        urun = sutun(k, "ürün", "urun")[:50]
        link = sutun(k, "link")
        satis = sutun(k, "satış", "satis")
        fiyat = sutun(k, "fiyat")
        durum = sutun(k, "durum").upper()
        sorunlar = []
        no = urun_no(link)
        if not no and "doğrulanamadı" not in link.lower() and "dogrulanamadi" not in link.lower():
            sorunlar.append("AliExpress urun linki yok")
        if no:
            if no in gorulen:
                sorunlar.append(f"ayni urun no {gorulen[no]} satirinda da var")
            gorulen[no] = k["_satir"]
        s = satis.lower()
        if "kart" in s:
            sorunlar.append("satis arama kartindan: urun sayfasindan okunmali")
        if ("mağaza" in s or "magaza" in s or "store" in s) and "sayfa" not in s:
            sorunlar.append("magaza toplami urun satisi degildir")
        if not satis:
            sorunlar.append("satis bos: sayi ya da 'doğrulanamadı' yazilmali")
        f_ = fiyat.lower()
        if ("yeni müşteri" in f_ or "yeni musteri" in f_ or "new user" in f_) and "normal" not in f_:
            sorunlar.append("yalniz yeni-musteri fiyati var: normal fiyat yazilmali")
        dna = dna_say(sutun(k, "dna"))
        abcd = [sayi(k.get(x, "")) for x in ("a", "b", "c", "d")]
        sira = int(sum(abcd)) if all(x is not None for x in abcd) else None
        oneri = "-"
        if dna < DNA_ESIK:
            oneri = "ELE (DNA<4)"
        elif sira is not None:
            oneri = "SAT adayi (kanit dosyasi sart)" if sira >= SAT_ESIK else ("IZLE" if sira >= IZLE_ESIK else "ELE (sira<=5)")
        metin = " ".join(v for a, v in k.items() if not a.startswith("_"))
        if durum.startswith("SAT") and not re.search(r"kanit/|kanıt/", metin):
            sorunlar.append("SAT ama kanit dosyasi yolu yok")
        print(f"{etiket} | {urun} | DNA {dna}/7 | sira {sira if sira is not None else '?'}/11 | oneri: {oneri}")
        for x in sorunlar:
            print(f"   ! {x}")
        hata += len(sorunlar)
    print(f"TOPLAM: {len([k for k in kayitlar if '_hata' not in k])} aday, {hata} sorun")
    return 1 if hata else 0


def sinama(yol, n, tohum):
    _, kayitlar = tablo_oku(yol)
    adaylar = [k for k in kayitlar if "_hata" not in k and sayi(sutun(k, "satış", "satis")) is not None]
    if not adaylar:
        print("Sayi iceren satir yok; sinama yapilamadi.")
        return 1
    rnd = random.Random(tohum)
    secim = rnd.sample(adaylar, min(n, len(adaylar)))
    print(f"SINAMA: {len(secim)} satir secildi (tohum={tohum}). Her birini urun sayfasindan ac ve karsilastir:")
    for k in secim:
        print(f"- satir {k['_satir']}: {sutun(k, 'ürün', 'urun')[:60]}")
        print(f"    link : {sutun(k, 'link')}")
        print(f"    satis: {sutun(k, 'satış', 'satis')}   fiyat: {sutun(k, 'fiyat')}")
    print("Biri bile tutmazsa tablonun tamami 'supheli' sayilir.")
    return 0


def main(argv):
    try:  # Windows konsolunda Turkce karakter hatasini onler
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    komut = argv[1]
    if komut == "tekrar" and len(argv) >= 4:
        return tekrar(argv[2], argv[3:])
    if komut == "denetle" and len(argv) == 3:
        return denetle(argv[2])
    if komut == "sinama" and len(argv) >= 3:
        n, tohum = 3, None
        if "--n" in argv:
            n = int(argv[argv.index("--n") + 1])
        if "--tohum" in argv:
            tohum = int(argv[argv.index("--tohum") + 1])
        if tohum is None:
            tohum = random.SystemRandom().randint(1, 10**6)
        return sinama(argv[2], n, tohum)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
