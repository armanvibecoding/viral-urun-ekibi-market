#!/usr/bin/env python3
"""Talimat bütçesi ve tek-kaynak kapısı (geliştirici betiği; eklentiye yüklenmez). Commit öncesi koşulur.

  python3 scripts/butce_kontrol.py            → çıkış 0 temiz · 1 ihlal
  python3 scripts/butce_kontrol.py --kendini-sina   → kapının kendisini kırarak sınar (geçici kopyada)

Kapılar (HATA → çıkış 1):
  1. Çekirdek beceri SKILL.md: ≤ 120 satır VE ≤ 12 000 bayt (satır sınırı uzun satırla aşılmasın diye ikisi birlikte).
     Kapsam dışı: hyperframes*, media-use (üçüncü taraf, imzalı) ve magaza-kurucu (modülün kendi 5 120 bayt sınırı var).
  2. Ajan dosyası ≤ 7 000 bayt.
  3. Tek kaynak: aşağıdaki kuralların tam metni yalnız `ortak/kurallar.md`'de yaşar; izinli dosyalar dışında parmak izi
     görülürse HATA (diğer dosyalar kimliğe atıf yapar: SES-01, ICE-01 …). Kimlik `kurallar.md`'de tanımlı olmalı.
  4. Atıf yapılan her kural kimliği (`ABC-01`) `ortak/kurallar.md`'de tanımlı.
  5. SKILL.md ve ajan dosyalarında tarihli anlatı yok ("2026-11-17 kurucu: …"); kuralın hikâyesi `ortak/bilgi/dersler.md`'de durur.
  6. Kadro: `ortak/ekip.md`'deki model sütunu = ajan dosyasındaki `model:` (her ajan için).
UYARI (çıkışı değiştirmez): referans dosyalarındaki tarihli anlatı sayısı; ≥ 10 KB referans dosyaları.
"""
import glob
import os
import re
import shutil
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SATIR, BAYT, AJAN_BAYT = 120, 12000, 7000
DISARIDA = ("hyperframes", "hyperframes-cli", "hyperframes-registry", "media-use", "magaza-kurucu")
# kimlik → (parmak izi, izinli yol parçaları)
TEK_KAYNAK = {
    "SES-01": (re.compile(r"[−-] ?30 dB"), ("ortak/kurallar.md", "/scripts/", "ortak/bilgi/", "referans/ses-tasarimi.md", "ekler/")),
    "ICE-01": (re.compile(r"organik[^.|\n]{0,40}fiyat (yok|yazıl)|organikte fiyat", re.I),
               ("ortak/kurallar.md", "/scripts/", "ortak/bilgi/", "ortak/paket.py", "ekler/", "referans/agir-kusurlar.md")),
}
KIMLIK = re.compile(r"\b(?:IDD|PLT|SES|ICE|URE)-\d{2}\b")
ANLATI = re.compile(r"20\d\d-\d\d-\d\d[^|\n]{0,25}kurucu|kurucu[^|\n]{0,25}20\d\d-\d\d-\d\d")


def oku(y):
    with open(y, encoding="utf-8", errors="replace") as f:
        return f.read()


def denetle(kok):
    e = os.path.join(kok, "plugins", "viral-urun-ekibi")
    hata, uyari = [], []
    goreli = lambda y: os.path.relpath(y, e).replace(os.sep, "/")
    beceriler = [y for y in sorted(glob.glob(os.path.join(e, "skills", "*", "SKILL.md")))
                 if os.path.basename(os.path.dirname(y)) not in DISARIDA]
    if len(beceriler) < 5:
        hata.append("çekirdek beceri sayısı %d (< 5): kapı ölçecek dosya bulamadı" % len(beceriler))
    for y in beceriler:
        t = oku(y)
        n, b = t.count("\n"), len(t.encode("utf-8"))
        if n > SATIR or b > BAYT:
            hata.append("%s: %d satır / %d bayt (sınır %d satır ve %d bayt) → ayrıntıyı referans dosyasına taşı" % (goreli(y), n, b, SATIR, BAYT))
    ajanlar = sorted(glob.glob(os.path.join(e, "agents", "*.md")))
    for y in ajanlar:
        b = len(oku(y).encode("utf-8"))
        if b > AJAN_BAYT:
            hata.append("%s: %d bayt (sınır %d)" % (goreli(y), b, AJAN_BAYT))
    kurallar_yol = os.path.join(e, "ortak", "kurallar.md")
    kurallar = oku(kurallar_yol) if os.path.exists(kurallar_yol) else ""
    tanimli = set(re.findall(r"^\| ((?:IDD|PLT|SES|ICE|URE)-\d{2}) \|", kurallar, re.M))
    for k in TEK_KAYNAK:
        if k not in tanimli:
            hata.append("ortak/kurallar.md: %s tanımlı değil (tek kaynak satırı yok)" % k)
    metinler = [y for y in glob.glob(os.path.join(e, "**", "*"), recursive=True)
                if os.path.isfile(y) and y.endswith((".md", ".tsv")) and not any("/skills/%s/" % d in y.replace(os.sep, "/") for d in DISARIDA)]
    for y in metinler:
        g, t = goreli(y), oku(y)
        for k, (iz, izinli) in TEK_KAYNAK.items():
            if not any(p in "/" + g or g == p for p in izinli):
                for no, s in enumerate(t.splitlines(), 1):
                    if iz.search(s):
                        hata.append("%s:%d: %s kuralının metni tekrar yazılmış → kimliğe atıf yap (tek kaynak ortak/kurallar.md)" % (g, no, k))
        if not g.startswith("ortak/bilgi/") and not g.startswith("ekler/proje-paketi/yuklenecek/"):
            for kim in set(KIMLIK.findall(t)) - tanimli:
                hata.append("%s: %s kimliğine atıf var ama ortak/kurallar.md'de tanımlı değil" % (g, kim))
    for y in beceriler + ajanlar:
        for no, s in enumerate(oku(y).splitlines(), 1):
            if ANLATI.search(s):
                hata.append("%s:%d: tarihli anlatı (kuralın hikâyesi ortak/bilgi/dersler.md'de durur)" % (goreli(y), no))
    kadro_yol = os.path.join(e, "ortak", "ekip.md")
    kadro = oku(kadro_yol) if os.path.exists(kadro_yol) else ""
    for y in ajanlar:
        ad = os.path.basename(y)[:-3]
        m = re.search(r"^model: (\w+)$", oku(y), re.M)
        satir = [l for l in kadro.splitlines() if "`%s`" % ad in l and l.startswith("|")]
        if not m:
            hata.append("agents/%s.md: model alanı yok" % ad)
        elif not satir:
            hata.append("ortak/ekip.md: `%s` satırı yok" % ad)
        elif "| %s |" % m.group(1) not in satir[0] and "| %s (" % m.group(1) not in satir[0]:
            hata.append("ortak/ekip.md: `%s` modeli ajan dosyasıyla aynı değil (dosya: %s)" % (ad, m.group(1)))
    anlati = sum(len(ANLATI.findall(oku(y))) for y in metinler if "/referans/" in y.replace(os.sep, "/"))
    if anlati:
        uyari.append("referans dosyalarında %d tarihli anlatı cümlesi (sonraki budamada dersler.md'ye taşınır)" % anlati)
    buyuk = [(goreli(y), os.path.getsize(y)) for y in metinler if "/referans/" in y.replace(os.sep, "/") and os.path.getsize(y) >= 10240]
    if buyuk:
        uyari.append("≥ 10 KB referans: " + ", ".join("%s (%d)" % b for b in sorted(buyuk, key=lambda x: -x[1])[:8]))
    return hata, uyari, len(beceriler), len(ajanlar)


def kendini_sina():
    """Kapıyı geçici kopyada tek tek kır; her kırma HATA üretmeli (kırılmayan kapı yeşil sayılmaz)."""
    gecici = tempfile.mkdtemp(prefix="butce_test_")
    hedef = os.path.join(gecici, "plugins", "viral-urun-ekibi")
    shutil.copytree(os.path.join(KOK, "plugins", "viral-urun-ekibi"), hedef,
                    ignore=shutil.ignore_patterns("hyperframes*", "media-use", "*.ttf", "*.jpg", "__pycache__"))
    temiz, _, _, _ = denetle(gecici)
    sonuc = [("temiz kopya → 0 hata", not temiz)]

    def kir(ad, yol, degistir, aranan):
        tam = os.path.join(hedef, yol)
        eski = oku(tam)
        with open(tam, "w", encoding="utf-8") as f:
            f.write(degistir(eski))
        h, _, _, _ = denetle(gecici)
        sonuc.append((ad, any(aranan in x for x in h)))
        with open(tam, "w", encoding="utf-8") as f:   # ters değişimle geri al
            f.write(eski)
    kir("SKILL.md 121 satır → HATA", "skills/video-kurgu/SKILL.md", lambda t: t + "\n" * 40, "satır /")
    kir("SKILL.md > 12 000 bayt (uzun satır) → HATA", "skills/teklif-ve-sayfa/SKILL.md", lambda t: t + "x" * 6000, "bayt (sınır")
    kir("ajan > 7 000 bayt → HATA", "agents/video-juri.md", lambda t: t + "x" * 5000, "bayt (sınır 7000)")
    kir("müzik kuralı başka dosyada yeniden yazıldı → HATA", "skills/video-kurgu/SKILL.md",
        lambda t: t + "\nMüzik 0. sn'de −30 dB'den başlar.\n", "SES-01 kuralının metni")
    kir("fiyat kuralı başka dosyada yeniden yazıldı → HATA", "agents/icerik-stratejisti.md",
        lambda t: t + "\nOrganik videoda ekranda fiyat yok.\n", "ICE-01 kuralının metni")
    kir("tanımsız kural kimliğine atıf → HATA", "skills/video-kurgu/SKILL.md", lambda t: t + "\nBkz. SES-99.\n", "SES-99")
    kir("tek kaynak satırı silindi → HATA", "ortak/kurallar.md", lambda t: t.replace("| SES-01 |", "| SES-XX |"), "SES-01 tanımlı değil")
    kir("tarihli anlatı beceriye girdi → HATA", "skills/ekip-lideri/SKILL.md", lambda t: t + "\n(2026-11-17 kurucu: şöyle dedi)\n", "tarihli anlatı")
    kir("kadro modeli ajan dosyasından farklı → HATA", "agents/ses-tasarimcisi.md",
        lambda t: re.sub(r"^model: \w+$", "model: fable", t, flags=re.M), "modeli ajan dosyasıyla aynı değil")
    son, _, _, _ = denetle(gecici)
    sonuc.append(("geri alınca yine temiz", not son))
    shutil.rmtree(gecici, ignore_errors=True)
    for ad, ok in sonuc:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    kalan = sum(1 for _, ok in sonuc if not ok)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
    return 1 if kalan else 0


def main():
    if "--kendini-sina" in sys.argv:
        return kendini_sina()
    hata, uyari, nb, na = denetle(KOK)
    for h in hata:
        print("HATA  " + h)
    for u in uyari:
        print("UYARI " + u)
    print("bütçe: %d beceri, %d ajan denetlendi · %d hata · %d uyarı → %s" % (nb, na, len(hata), len(uyari), "KALDI" if hata else "GEÇTİ"))
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
