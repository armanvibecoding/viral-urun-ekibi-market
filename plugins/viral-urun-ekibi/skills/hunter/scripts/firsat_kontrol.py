#!/usr/bin/env python3
"""hunter yardimcisi (yalniz Python 3 standart kutuphanesi; macOS / Windows / Linux).

Alt komutlar:
  tekrar  KLASOR TERIM...      Aday daha once is/firsat/ altinda gecmis mi? (AliExpress linki, urun no veya kelime)
  denetle ADAYLAR.md           Aday tablosunu kurallara gore denetler, DNA ve sira puanini hesaplar.
                               YALNIZ SAT (kurucu karari 2026-11-25): oneri SAT adayi ya da ELE. ELE yalniz KANITLI engel:
                               veto, kanitli negatif marj, zaten viral kaniti, DNA<4, olculmus sira puani < 8. dogrulanamadi/bos
                               olcut engel DEGIL: "kontrol et" notu olur (SAT kartinda "ilk testte kontrol et")
  ozet    ADAYLAR.md [--hedef N] [--proje DIR]
                               Kullanici ozeti: YALNIZ SAT (kanit dosyasi olanlar); N varsayilan 5; N'e ulasilamazsa
                               tek satir "k SAT buldum, sebep: ..."
  sinama  ADAYLAR.md [--n 3] [--tohum N]
                               Dogrulama icin rastgele N satir secer (sayi kaynagindan acilip kontrol edilir)

Cikis kodu: 0 = sorun yok, 1 = denetimde hata var / tekrar bulundu, 2 = kullanim hatasi.
"""
import os
import random
import re
import sys

# Eski yazım `SAT-KOŞULLU: <eksik>` artık ayrı sınıf DEĞİL: SAT'tır, eksik kanıt SAT kartında "ilk testte kontrol et" notudur (kurucu kararı 2026-11-25)
KOSULLU_RE = re.compile(r"^\s*SAT\s*[-–]?\s*\(?\s*KO[SŞ]ULLU\s*\)?\s*(?:[:：]\s*(?P<eksik>[^—–]*?))?\s*(?:[—–].*)?$", re.I)
ITEM_RE = re.compile(r"(?:item/|/i/|productId=)(\d{9,20})")
DNA_ESIK = 4
SAT_ESIK = 8
OLUMSUZ_VETO = ("", "yok", "-", "hayir", "hayır", "temiz")
KANIT_RE = re.compile(r"(is/firsat/kanit/\S+?\.md)")


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


def ve_say(eksik):
    """'numune ve alıcı videosu' → 2 (tek eksik kanıt kuralı)."""
    return len([x for x in re.split(r"\s(?:ve|ile|and)\s|[;+&]|,\s", eksik.strip(), flags=re.I) if x.strip()])


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
        oneri, ele, kontrol, sira, dna = oneri_hesapla(k)
        metin = " ".join(v for a, v in k.items() if not a.startswith("_"))
        kosullu = KOSULLU_RE.match(sutun(k, "durum"))
        if durum.startswith("SAT") and not KANIT_RE.search(metin) and not re.search(r"kanit/|kanıt/", metin):
            sorunlar.append("SAT ama kanit dosyasi yolu yok")
        if (durum.startswith("SAT") or kosullu) and ele:
            sorunlar.append("durum SAT ama kanitli engel var (%s): SAT yazilamaz" % "; ".join(ele))
        if "trendyol" in fiyat.lower():
            sorunlar.append("fiyat Trendyol perakende fiyati: tedarikci (AliExpress) normal fiyati yazilmali; Trendyol fiyati hedef satis/rakip fiyatidir, alis degil")
        if durum.startswith("IZLE") or durum.startswith("İZLE"):
            print(f"   UYARI {etiket}: durum IZLE eski sinif (yalniz SAT ve ELE); denetim kaydinda kalir, kullaniciya gitmez")
        print(f"{etiket} | {urun} | DNA {dna}/7 | sira {sira if sira is not None else '?'}/11 | oneri: {oneri}")
        if kontrol:
            print("   ~ ilk testte kontrol et: " + "; ".join(kontrol))
        for x in sorunlar:
            print(f"   ! {x}")
        hata += len(sorunlar)
    print(f"TOPLAM: {len([k for k in kayitlar if '_hata' not in k])} aday, {hata} sorun")
    return 1 if hata else 0


def oneri_hesapla(k):
    """(oneri, ELE sebepleri, kontrol notlari, sira, dna). ELE yalniz kanitli engel; olculemeyen olcut not olur."""
    ele, kontrol = [], []
    dna = dna_say(sutun(k, "dna"))
    abcd = [sayi(k.get(x, "")) for x in ("a", "b", "c", "d")]
    sira = int(sum(abcd)) if all(x is not None for x in abcd) else None
    if not sutun(k, "dna").strip():
        kontrol.append("DNA puanı eksik")
    elif dna < DNA_ESIK:
        ele.append("DNA<4")
    if sira is None:
        kontrol.append("sıra puanı (A-D) eksik")
    elif sira < SAT_ESIK:
        ele.append("sıra puanı %d (SAT için ≥%d)" % (sira, SAT_ESIK))
    veto = sutun(k, "veto").strip()
    if veto.lower() not in OLUMSUZ_VETO:
        ele.append("veto: %s" % veto)
    marj = sutun(k, "marj").strip().lower()
    if marj:
        mv = sayi(marj)
        if "zarar" in marj or "negatif" in marj or (mv is not None and mv <= 1.0):
            ele.append("marj: kanıtlı negatif katkı")
    else:
        kontrol.append("marj hesaplanmadı")
    zv = sutun(k, "zaten").strip().lower()
    if zv.startswith("zaten viral"):
        ele.append("aynı ürün zaten viral")
    elif not zv.startswith("tutmam"):
        kontrol.append("zaten viral doğrulanamadı (vekil: Meta reklam sayısı + satıcı sayısı)")
    sat = sutun(k, "satış", "satis").strip().lower()
    if not sat or sat.startswith("doğrulanamadı") or sat.startswith("dogrulanamadi"):
        kontrol.append("ürün satışı doğrulanamadı")
    return ("ELE (%s)" % "; ".join(ele)) if ele else "SAT adayi (kanit dosyasi sart)", ele, kontrol, sira, dna


def nihai(k, proje):
    """Kullaniciya gidecek tek hukum: SAT | KANIT-BEKLIYOR | ELE | DISI."""
    durum = sutun(k, "durum").strip().upper().replace("İ", "I")
    _, ele, _, _, _ = oneri_hesapla(k)
    if durum.startswith("ELE") or ele:
        return "ELE"
    if not durum.startswith("SAT"):
        return "DISI"
    m = KANIT_RE.search(" ".join(v for a, v in k.items() if not a.startswith("_")))
    return "SAT" if m and os.path.isfile(os.path.join(proje, m.group(1))) else "KANIT-BEKLIYOR"


def ozet(yol, hedef, proje):
    baslik, kayitlar = tablo_oku(yol)
    kayitlar = [k for k in kayitlar if "_hata" not in k]
    sat, bekleyen, sebepler = [], 0, {}
    for k in kayitlar:
        h = nihai(k, proje)
        oneri, ele, kontrol, sira, _ = oneri_hesapla(k)
        if h == "SAT":
            sat.append((k, kontrol, sira))
        elif h == "KANIT-BEKLIYOR":
            bekleyen += 1
        elif h == "ELE":
            for e in ele or ["yazılı karar eşiği geçmedi"]:
                anahtar = re.split(r"\s[\d(]", e)[0].split(":")[0].strip()
                sebepler[anahtar] = sebepler.get(anahtar, 0) + 1
    print(f"SAT {len(sat)}/{hedef} · {len(kayitlar)} aday tarandı")
    for n, (k, kontrol, sira) in enumerate(sat[:8], 1):
        parca = [f"{n}. {sutun(k, 'ürün', 'urun')[:60]}", f"AliExpress satış {sutun(k, 'satış', 'satis')[:40]}", f"fiyat {sutun(k, 'fiyat')[:30]}"]
        if sira is not None:
            parca.append(f"sıra {sira}/11")
        if kontrol:
            parca.append("ilk testte kontrol et: " + "; ".join(kontrol))
        print(" · ".join(parca))
    if len(sat) > 8:
        print(f"+{len(sat) - 8} SAT daha: firsat-urunler.xlsx")
    if bekleyen:
        print(f"{bekleyen} aday kanıt dosyası bekliyor (kanıt yazılınca SAT olarak görünür)")
    if len(sat) < hedef:
        sebep = (", ".join(a for a, _ in sorted(sebepler.items(), key=lambda x: -x[1])[:2]) + " eşiği geçmedi") if sebepler else "tarama sınırı ya da engel sinyali"
        print(f"{len(sat)} SAT buldum, sebep: {sebep}")
    return 0


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
    if komut == "ozet" and len(argv) >= 3:
        hedef = int(argv[argv.index("--hedef") + 1]) if "--hedef" in argv else 5
        yol = os.path.abspath(argv[2])
        proje = argv[argv.index("--proje") + 1] if "--proje" in argv else os.path.dirname(os.path.dirname(os.path.dirname(yol)))
        return ozet(yol, hedef, proje)
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
