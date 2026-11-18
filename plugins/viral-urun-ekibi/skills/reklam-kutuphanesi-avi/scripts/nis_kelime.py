#!/usr/bin/env python3
"""Niş → sorgu planı ve günlük kota bekçisi.

  python3 nis_kelime.py gun    --kok is/meta --ulke US,TR,GB --nis evcil [--nis-basi 4] [--ivme]
        Günün sorgu listesini ve Meta URL'lerini basar (yazmaz). Kalan kotayı aşmaz; son 7 günde
        yapılmış sorgu tekrar önerilmez (--ivme: yalnız 7+ gün önce yapılanları tekrar önerir).
  python3 nis_kelime.py kaydet --kok is/meta --ulke TR --aile U --nis evcil --sorgu "kedi yatağı" [--siralama gosterim]
        Sorguyu AÇMADAN HEMEN ÖNCE çalıştır. Reddeder (çıkış 1): günün 31. sorgusu · aynı gün aynı ülke+sorgu ·
        son kayıttan <15 sn · bugün dolu bir KONTROL kaydı yokken U/S/K/ALAN sorgusu.
  python3 nis_kelime.py sonuc  --kok is/meta --ulke US --sorgu nike --kart 25
        Kontrol sorgusunun ekranda görülen kart sayısını yazar. 0 ise çıkış 3 (SINIRLAMA — bugün dur).
  python3 nis_kelime.py nisler                      # niş kodlarını ve pazar başına terim sayısını basar
"""
import argparse
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

VARSAYILAN_NISLER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "referans", "nisler.md")
AB_INGILIZCE_YEDEK = {"GB", "DE", "FR", "ES", "IT", "NL"}   # AB'de İngilizce reklam da döner → US süzgeç terimleri yedek


def nisler_oku(yol=VARSAYILAN_NISLER):
    """{nis: {"ad": str, "ele": bool, "terim": {(ulke, aile): [ifade, ...]}}}"""
    if not os.path.exists(yol):
        raise o.VeriHatasi("nisler.md yok: %s" % yol)
    sonuc, guncel = {}, None
    with open(yol, encoding="utf-8") as f:
        for no, s in enumerate(f, start=1):
            m = re.match(r"^## (\S+)\s+—\s+(.*)$", s.strip())
            if m:
                guncel = m.group(1)
                if guncel in sonuc:
                    raise o.VeriHatasi("nisler.md:%d niş iki kez: %s" % (no, guncel))
                sonuc[guncel] = {"ad": m.group(2), "ele": "ELE KAPISI" in m.group(2), "terim": {}}
                continue
            m = re.match(r"^\|\s*([A-Z]{2})\s*\|\s*(U|S|K|F|KONTROL)\s*\|(.*)\|\s*$", s.strip())
            if m and guncel:
                if m.group(1) not in o.ULKELER:
                    raise o.VeriHatasi("nisler.md:%d bilinmeyen pazar %s" % (no, m.group(1)))
                terimler = [t.strip() for t in m.group(3).split(";") if t.strip()]
                if not terimler:
                    raise o.VeriHatasi("nisler.md:%d boş terim listesi" % no)
                sonuc[guncel]["terim"].setdefault((m.group(1), m.group(2)), []).extend(terimler)
    if not sonuc:
        raise o.VeriHatasi("nisler.md içinde '## kod — ad' başlığı yok")
    return sonuc


norm = o.norm


def nis_bul(sozluk, ulke, metin):
    """S (dropship sinyali) sorgusundan gelen kartın nişi: gövde+yolda en çok eşleşen niş (Ü + F terimleri)."""
    t = norm(metin).replace("-", " ")
    en, en_puan = "belirsiz", 0
    for nis, v in sozluk.items():
        if nis.startswith("_"):
            continue
        terimler = v["terim"].get((ulke, "U"), []) + v["terim"].get((ulke, "F"), [])
        if ulke in AB_INGILIZCE_YEDEK:
            terimler += v["terim"].get(("US", "U"), []) + v["terim"].get(("US", "F"), [])
        puan = sum(1 for x in set(terimler) if re.search(r"(?<!\w)" + re.escape(norm(x)), t))
        if puan > en_puan:
            en, en_puan = nis, puan
    return en


def meta_url(ulke, sorgu, aile, siralama):
    if aile in ("KONTROL", "ALAN"):
        p = [("active_status", "active"), ("ad_type", "all"), ("country", ulke), ("q", sorgu),
             ("search_type", "keyword_unordered"), ("media_type", "all")]
    else:
        p = [("active_status", "active"), ("ad_type", "all"), ("country", ulke), ("q", '"%s"' % sorgu),
             ("search_type", "keyword_exact_phrase"), ("media_type", "video"),
             ("sort_data[mode]", o.SIRALAMALAR[siralama]), ("sort_data[direction]", "desc")]
    return "https://www.facebook.com/ads/library/?" + urllib.parse.urlencode(p, safe="[]", quote_via=urllib.parse.quote)


def bugunku(aramalar, tarih):
    return [a for a in aramalar if a["tarih"] == tarih]


def gun_plani(kok, ulkeler, nisler, nis_basi, ivme, sozluk):
    simdi = o.bugun()
    tarih = simdi.date().isoformat()
    aramalar = o.oku(kok, "arama")
    kalan = o.GUNLUK_KOTA - len(bugunku(aramalar, tarih))
    yakin = {}
    for a in aramalar:
        yakin.setdefault((a["ulke"], a["sorgu"]), []).append(o.gun_farki(tarih, a["tarih"]))
    plan = []
    if not any(a["aile"] == "KONTROL" and o.sayi_mi(a["kart"]) and int(a["kart"]) > 0 for a in bugunku(aramalar, tarih)):
        u0 = ulkeler[0]
        k = sozluk["_kontrol"]["terim"].get((u0, "KONTROL"), ["nike"])[0]
        plan.append((u0, "-", "KONTROL", k, "gosterim"))
    for ulke in ulkeler:
        s_terim = sozluk["_sinyal"]["terim"].get((ulke, "S"), [])
        adaylar = []
        for nis in nisler:
            t = sozluk[nis]["terim"]
            us, ks = t.get((ulke, "U"), []), t.get((ulke, "K"), [])
            sira = [("U", x) for x in us[:max(1, nis_basi - 2)]] + [("K", x) for x in ks[:1]]
            adaylar += [(ulke, nis, aile, x, "gosterim") for aile, x in sira]
        adaylar += [(ulke, "-", "S", x, "yeni") for x in s_terim[:1]]
        for c in adaylar:
            gecmis = yakin.get((c[0], c[3]), [])
            if ivme:
                if gecmis and min(gecmis) >= 7:
                    plan.append(c)
            elif not gecmis or min(gecmis) >= 7:
                plan.append(c)
    return tarih, kalan, plan[:max(0, kalan)], len(plan)


def kaydet(kok, ulke, aile, nis, sorgu, siralama, sozluk):
    if ulke not in o.ULKELER:
        raise o.VeriHatasi("ülke geçersiz: %s (%s)" % (ulke, ",".join(o.ULKELER)))
    if aile not in o.AILELER:
        raise o.VeriHatasi("aile geçersiz: %s (%s)" % (aile, ",".join(o.AILELER)))
    if siralama not in o.SIRALAMALAR:
        raise o.VeriHatasi("sıralama geçersiz: %s" % siralama)
    if aile in ("U", "K") and nis not in sozluk:
        raise o.VeriHatasi("niş bilinmiyor: %s (nisler.md)" % nis)
    if aile in ("U", "K") and sozluk[nis]["ele"]:
        raise o.VeriHatasi("%s ELE KAPISI nişi: yalnız süzgeç/sinyal, sorgu planına girmez" % nis)
    if not sorgu.strip():
        raise o.VeriHatasi("sorgu boş")
    simdi = o.bugun()
    tarih, saat = simdi.date().isoformat(), simdi.strftime("%H:%M:%S")
    aramalar = o.oku(kok, "arama")
    bugun = bugunku(aramalar, tarih)
    if len(bugun) >= o.GUNLUK_KOTA:
        raise o.VeriHatasi("KOTA: bugün %d sorgu yapıldı (sınır %d). Yarın devam." % (len(bugun), o.GUNLUK_KOTA))
    if aile != "KONTROL" and any(a["ulke"] == ulke and a["sorgu"] == sorgu and a["aile"] != "KONTROL" for a in bugun):
        raise o.VeriHatasi("TEKRAR: %s / %r bugün zaten yapıldı" % (ulke, sorgu))
    if bugun:
        son = max(a["saat"] for a in bugun)
        h, m, s = [int(x) for x in son.split(":")]
        fark = (simdi.hour * 3600 + simdi.minute * 60 + simdi.second) - (h * 3600 + m * 60 + s)
        if fark < o.MIN_ARALIK_SN:
            raise o.VeriHatasi("ÇOK HIZLI: son sorgudan %d sn geçti (en az %d). Bekle." % (fark, o.MIN_ARALIK_SN))
    if aile != "KONTROL":
        k = [a for a in bugun if a["aile"] == "KONTROL"]
        if not k or not o.sayi_mi(k[-1]["kart"]) or int(k[-1]["kart"]) == 0:
            raise o.VeriHatasi("KONTROL YOK: önce dolu bir kontrol sorgusu (`--aile KONTROL`, sonra `sonuc --kart N`). "
                               "Son kontrol 0 ya da yazılmamışsa bugün tarama yok.")
    aramalar.append({"tarih": tarih, "saat": saat, "ulke": ulke, "nis": nis if aile in ("U", "K") else "-",
                     "aile": aile, "sorgu": sorgu, "siralama": siralama, "kart": "", "durum": "ACIK", "ham_dosya": ""})
    o.yaz(kok, "arama", aramalar)
    print("kaydedildi (%d/%d): %s" % (len(bugun) + 1, o.GUNLUK_KOTA, meta_url(ulke, sorgu, aile, siralama)))


def sonuc(kok, ulke, sorgu, kart):
    if not o.sayi_mi(kart):
        raise o.VeriHatasi("kart sayı olmalı")
    tarih = o.bugun().date().isoformat()
    aramalar = o.oku(kok, "arama")
    hedef = [a for a in aramalar if a["tarih"] == tarih and a["ulke"] == ulke and a["sorgu"] == sorgu and a["aile"] == "KONTROL"]
    if not hedef:
        raise o.VeriHatasi("bugün %s / %r KONTROL kaydı yok" % (ulke, sorgu))
    hedef[-1].update(kart=kart, durum="TAMAM" if int(kart) > 0 else "SINIRLAMA")
    o.yaz(kok, "arama", aramalar)
    if int(kart) == 0:
        print("SINIRLAMA — bugün dur. Kontrol sorgusu 0 kart: Meta bugün sonuç vermiyor; sonuç 'doğrulanamadı'.")
        sys.exit(3)
    print("kontrol dolu (%s kart) — tarama serbest." % kart)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nisler", default=VARSAYILAN_NISLER)
    alt = ap.add_subparsers(dest="komut")
    g = alt.add_parser("gun")
    g.add_argument("--kok", default="is/meta")
    g.add_argument("--ulke", required=True)
    g.add_argument("--nis", required=True)
    g.add_argument("--nis-basi", type=int, default=4)
    g.add_argument("--ivme", action="store_true")
    k = alt.add_parser("kaydet")
    k.add_argument("--kok", default="is/meta")
    k.add_argument("--ulke", required=True)
    k.add_argument("--aile", required=True)
    k.add_argument("--nis", default="-")
    k.add_argument("--sorgu", required=True)
    k.add_argument("--siralama", default="gosterim")
    s = alt.add_parser("sonuc")
    s.add_argument("--kok", default="is/meta")
    s.add_argument("--ulke", required=True)
    s.add_argument("--sorgu", required=True)
    s.add_argument("--kart", required=True)
    alt.add_parser("nisler")
    x = ap.parse_args()
    try:
        sozluk = nisler_oku(x.nisler)
        if x.komut == "gun":
            ulkeler = [u.strip().upper() for u in x.ulke.split(",") if u.strip()]
            nisler = [n.strip() for n in x.nis.split(",") if n.strip()]
            for u in ulkeler:
                if u not in o.ULKELER:
                    raise o.VeriHatasi("ülke geçersiz: %s" % u)
            for n in nisler:
                if n not in sozluk or n.startswith("_"):
                    raise o.VeriHatasi("niş bilinmiyor: %s" % n)
                if sozluk[n]["ele"]:
                    raise o.VeriHatasi("%s ELE KAPISI nişi, sorgu planına girmez" % n)
            tarih, kalan, plan, toplam = gun_plani(x.kok, ulkeler, nisler, x.nis_basi, x.ivme, sozluk)
            print("# %s · kalan kota %d/%d · plan %d sorgu%s" % (tarih, max(kalan, 0), o.GUNLUK_KOTA, len(plan),
                  " (kota yüzünden %d kesildi)" % (toplam - len(plan)) if toplam > len(plan) else ""))
            print("# sıra: önce KONTROL; her sorgudan önce `kaydet`, aralar ≥15 sn")
            for ulke, nis, aile, sorgu, sir in plan:
                print("%s\t%s\t%s\t%s\t%s\t%s" % (ulke, nis, aile, sir, sorgu, meta_url(ulke, sorgu, aile, sir)))
        elif x.komut == "kaydet":
            kaydet(x.kok, x.ulke.upper(), x.aile.upper(), x.nis, x.sorgu.strip(), x.siralama, sozluk)
        elif x.komut == "sonuc":
            sonuc(x.kok, x.ulke.upper(), x.sorgu.strip(), x.kart)
        elif x.komut == "nisler":
            for n, v in sozluk.items():
                say = {u: sum(len(v["terim"].get((u, a), [])) for a in ("U", "K", "F", "S", "KONTROL")) for u in o.ULKELER}
                print("%-14s %s %s" % (n, "ELE" if v["ele"] else "   ", " ".join("%s:%d" % kv for kv in say.items())))
        else:
            ap.print_help()
            sys.exit(1)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))


if __name__ == "__main__":
    main()
