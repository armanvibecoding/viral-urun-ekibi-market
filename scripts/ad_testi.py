#!/usr/bin/env python3
"""Ad sistemi kapısı (0.4.0). Tek kaynak: plugins/viral-urun-ekibi/ortak/ad-haritasi.tsv

  python3 scripts/ad_testi.py                 → kapıları koşar (çıkış 0 temiz · 1 hata)
  python3 scripts/ad_testi.py --kendini-sina  → her kapıyı geçici kopyada kırar; kırılmayan kapı yeşil sayılmaz

Kapılar: a) beceri klasör adı = name = haritadaki yeni ad (alias hariç) · b) agents/ = haritadaki 17 ajan ·
c) beceri ve ajan adları tek havuzda benzersiz · d) her eski beceri adı için yalnız SKILL.md içeren alias klasörü ·
e) eski kimlikler izinli yerler dışında geçmiyor · f) description "<Kod adı> (" ile başlar ·
g) birleşen ajanın her modu için ortak/roller/<kod>/<mod>.md var.
"""
import os
import re
import shutil
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUG = os.path.join("plugins", "viral-urun-ekibi")
HARITA = os.path.join(PLUG, "ortak", "ad-haritasi.tsv")
UCUNCU = {"hyperframes", "hyperframes-cli", "hyperframes-registry", "media-use"}
METIN = (".md", ".py", ".sh", ".js", ".mjs", ".json", ".yml", ".yaml", ".tsv", ".csv", ".txt", ".swift", ".gitattributes")
ATLA_DIZIN = {".git", "dist", "node_modules", "__pycache__", ".pytest_cache", "licenses"}
ALIAS_ISARET = re.compile(r"<!--\s*alias:\s*([a-z]+)\s*-->")
YOL_KORU = "moduller/magaza-kurucu"


def oku(yol):
    with open(yol, encoding="utf-8") as f:
        return f.read()


def harita(kok):
    satirlar = oku(os.path.join(kok, HARITA)).splitlines()
    baslik = satirlar[0].split("\t")
    return [dict(zip(baslik, s.split("\t"))) for s in satirlar[1:] if s.strip()]


def on_yazi(yol):
    t = oku(yol)
    m = re.match(r"---\n(.*?)\n---\n", t, re.S)
    alanlar = {}
    if m:
        for s in m.group(1).splitlines():
            if ":" in s and not s.startswith(" "):
                k, v = s.split(":", 1)
                alanlar[k.strip()] = v.strip().strip('"').strip("'")
    return alanlar, t


def denetle(kok):
    hata = []
    h = harita(kok)
    beceri = [r for r in h if r["tur"] == "beceri"]
    ajan = [r for r in h if r["tur"] == "ajan"]
    b_yeni = {r["yeni"] for r in beceri}
    a_yeni = {r["yeni"] for r in ajan}
    kod = {r["yeni"]: r["kod_adi"] for r in h}
    skills = os.path.join(kok, PLUG, "skills")
    agents = os.path.join(kok, PLUG, "agents")

    # a) + f(beceri)
    gercek = set()
    for ad in sorted(os.listdir(skills)):
        y = os.path.join(skills, ad, "SKILL.md")
        if not os.path.isfile(y):
            continue
        alanlar, t = on_yazi(y)
        if ALIAS_ISARET.search(t):
            continue
        if ad in UCUNCU:
            continue
        gercek.add(ad)
        if alanlar.get("name") != ad:
            hata.append("a) skills/%s: frontmatter name (%s) klasör adıyla aynı değil" % (ad, alanlar.get("name")))
        if ad not in b_yeni:
            hata.append("a) skills/%s: haritada yeni beceri adı değil" % ad)
        elif not alanlar.get("description", "").startswith(kod[ad] + " ("):
            hata.append("f) skills/%s: description '%s (' ile başlamıyor" % (ad, kod[ad]))
    for ad in sorted(b_yeni - gercek):
        hata.append("a) haritadaki beceri skills/%s/ yok" % ad)

    # b) + f(ajan)
    dosyalar = {f[:-3] for f in os.listdir(agents) if f.endswith(".md")}
    if dosyalar != a_yeni:
        hata.append("b) agents/ kümesi haritayla aynı değil: fazla=%s eksik=%s" % (sorted(dosyalar - a_yeni), sorted(a_yeni - dosyalar)))
    for ad in sorted(dosyalar & a_yeni):
        alanlar, _ = on_yazi(os.path.join(agents, ad + ".md"))
        if alanlar.get("name") != ad:
            hata.append("b) agents/%s.md: name (%s) dosya adıyla aynı değil" % (ad, alanlar.get("name")))
        if not alanlar.get("description", "").startswith(kod[ad] + " ("):
            hata.append("f) agents/%s.md: description '%s (' ile başlamıyor" % (ad, kod[ad]))

    # c)
    for ad in sorted(b_yeni | a_yeni):
        if not re.fullmatch(r"[a-z]+", ad):
            hata.append("c) kimlik [a-z]+ değil: " + ad)
    for ad in sorted(b_yeni & a_yeni):
        hata.append("c) beceri ve ajan havuzunda çakışan ad: " + ad)

    # d)
    for r in beceri:
        if r["eski"] == "-":
            continue
        d = os.path.join(skills, r["eski"])
        if not os.path.isdir(d):
            hata.append("d) alias klasörü yok: skills/" + r["eski"])
            continue
        if os.listdir(d) != ["SKILL.md"]:
            hata.append("d) alias klasöründe SKILL.md dışında dosya var: skills/%s → %s" % (r["eski"], sorted(os.listdir(d))))
        y = os.path.join(d, "SKILL.md")
        if os.path.isfile(y):
            m = ALIAS_ISARET.search(oku(y))
            if not m:
                hata.append("d) alias işareti yok: skills/%s/SKILL.md" % r["eski"])
            elif m.group(1) != r["yeni"] or not os.path.isfile(os.path.join(skills, m.group(1), "SKILL.md")):
                hata.append("d) alias hedefi bozuk: skills/%s → %s" % (r["eski"], m.group(1)))

    # e)
    eskiler = sorted({r["eski"] for r in h if r["eski"] != "-"}, key=len, reverse=True)
    desen = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(e) for e in eskiler))
    alias_dizin = {os.path.join(skills, r["eski"]) for r in beceri if r["eski"] != "-"}
    for dizin, altlar, dosyalar_ in os.walk(kok):
        altlar[:] = [a for a in altlar if a not in ATLA_DIZIN]
        goreli_d = os.path.relpath(dizin, kok).replace(os.sep, "/")
        if goreli_d == "docs/gelistirici" or goreli_d.startswith("docs/gelistirici/"):
            continue
        if dizin in alias_dizin:
            continue
        for f in dosyalar_:
            if not f.endswith(METIN):
                continue
            yol = os.path.join(dizin, f)
            goreli = os.path.relpath(yol, kok).replace(os.sep, "/")
            if goreli in (HARITA.replace(os.sep, "/"), "CHANGELOG.md"):
                continue
            if "/skills/hyperframes" in "/" + goreli or "/skills/media-use/" in "/" + goreli:
                continue
            try:
                satirlar = oku(yol).splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            for i, s in enumerate(satirlar, 1):
                s2 = s.replace(YOL_KORU, "\x00").replace('"moduller", "magaza-kurucu"', "\x00")
                if goreli.endswith("analiz_db_aktar.py") and '"kaynak"' in s:
                    continue
                if i == 1 and "/ortak/roller/" in "/" + goreli and "(eski:" in s:
                    continue
                for m in desen.finditer(s2):
                    hata.append("e) eski kimlik '%s': %s:%d" % (m.group(1), goreli, i))
                    break

    # g)
    modlu = {}
    for r in ajan:
        if r["mod"]:
            modlu.setdefault(r["yeni"], []).append(r["mod"])
    for k, modlar in sorted(modlu.items()):
        for m in modlar:
            if not os.path.isfile(os.path.join(kok, PLUG, "ortak", "roller", k, m + ".md")):
                hata.append("g) ortak/roller/%s/%s.md yok" % (k, m))
    return hata


def kendini_sina():
    """Kopya yalnız gereken dosyaları taşır; her kırma ilgili harf kodunda HATA üretmeli."""
    gecici = tempfile.mkdtemp(prefix="ad_test_")
    atla = shutil.ignore_patterns(".git", "dist", "node_modules", "__pycache__", ".pytest_cache", "*.ttf", "*.woff2", "*.mp3",
                                  "*.jpg", "*.png", "hyperframes*", "media-use")
    shutil.copytree(KOK, gecici, dirs_exist_ok=True, ignore=atla)
    sonuc = []
    temiz = denetle(gecici)
    sonuc.append(("temiz kopya → 0 hata", not temiz))
    h = harita(gecici)
    b0 = next(r for r in h if r["tur"] == "beceri" and r["eski"] != "-" and r["eski"] != r["yeni"] and r["mod"] == "")
    a0 = next(r for r in h if r["tur"] == "ajan" and not r["mod"])
    am = next(r for r in h if r["tur"] == "ajan" and r["mod"])
    skills = os.path.join(gecici, PLUG, "skills")
    agents = os.path.join(gecici, PLUG, "agents")

    def kir(ad, yol, degistir, harf):
        eski = oku(yol) if os.path.isfile(yol) else None
        yeni = degistir(eski)
        klasor = os.path.dirname(yol)
        yeni_klasor = not os.path.isdir(klasor)
        os.makedirs(klasor, exist_ok=True)
        with open(yol, "w", encoding="utf-8") as f:
            f.write(yeni)
        bulunan = denetle(gecici)
        sonuc.append((ad, any(x.startswith(harf + ")") for x in bulunan)))
        if eski is None:
            os.remove(yol)
            if yeni_klasor:
                os.rmdir(klasor)
        else:
            with open(yol, "w", encoding="utf-8") as f:
                f.write(eski)

    kir("a) name klasör adından farklı → HATA", os.path.join(skills, b0["yeni"], "SKILL.md"),
        lambda t: re.sub(r"^name: .*$", "name: yanlis", t, count=1, flags=re.M), "a")
    kir("b) fazladan ajan dosyası → HATA", os.path.join(agents, "fazlalik.md"), lambda t: "---\nname: fazlalik\n---\n", "b")
    b1 = next(r for r in h if r["tur"] == "beceri")
    kir("c) beceri adı ajan havuzunda da → HATA", os.path.join(gecici, HARITA),
        lambda t: t.replace("\t%s\t%s\t" % (a0["yeni"], a0["kod_adi"]), "\t%s\t%s\t" % (b1["yeni"], a0["kod_adi"])), "c")
    kir("d) alias klasörüne ikinci dosya → HATA", os.path.join(skills, b0["eski"], "EKSTRA.md"), lambda t: "x\n", "d")
    kir("e) eski kimlik serbest metinde → HATA", os.path.join(gecici, "README.md"),
        lambda t: t + "\nBkz. %s becerisi.\n" % b0["eski"], "e")
    kir("f) description kod adıyla başlamıyor → HATA", os.path.join(agents, a0["yeni"] + ".md"),
        lambda t: re.sub(r"^description: .*$", "description: Başka bir şey.", t, count=1, flags=re.M), "f")
    modyol = os.path.join(gecici, PLUG, "ortak", "roller", am["yeni"], am["mod"] + ".md")
    gizli = modyol + ".gizli"
    if os.path.isfile(modyol):
        os.rename(modyol, gizli)
        sonuc.append(("g) mod dosyası yok → HATA", any(x.startswith("g)") for x in denetle(gecici))))
        os.rename(gizli, modyol)
    else:
        sonuc.append(("g) mod dosyası yok → HATA (dosya zaten yok)", any(x.startswith("g)") for x in denetle(gecici))))
    sonuc.append(("geri alınca yine temiz", not denetle(gecici)))
    shutil.rmtree(gecici, ignore_errors=True)
    for ad, ok in sonuc:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    kalan = sum(1 for _, ok in sonuc if not ok)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
    return 1 if kalan else 0


def main():
    if "--kendini-sina" in sys.argv:
        return kendini_sina()
    hata = denetle(KOK)
    for x in hata:
        print("HATA  " + x)
    print("ad kapısı: %d hata → %s" % (len(hata), "KALDI" if hata else "GEÇTİ"))
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
