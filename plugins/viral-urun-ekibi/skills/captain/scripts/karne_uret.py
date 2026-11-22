#!/usr/bin/env python3
"""Haftalık ekip karnesi: rol başına BİR satır, sonuç metriği gerçek kayıtlardan. Veri yoksa "veri yok" yazar, sayı uydurmaz.

  python3 karne_uret.py --proje . [--bugun YYYY-AA-GG] [--yazma]

Çıktı: tablo (stdout) + .ekip/KARNE.md (üzerine yazılır) + .ekip/karne.jsonl (hafta kaydı; --yazma verilirse dosya yazılmaz).
Lider yalnız "Sonraki tek deneme" sütununu doldurur; betik o sütuna veri yoksa hangi dosyanın eksik olduğunu yazar.

| Rol | Sonuç metriği | Kaynak (proje klasöründe) |
|---|---|---|
| Fırsat avcısı | izleme ölçümünde büyüyen aday oranı (reklam sayısı t0 → t7/t30 arttı) | is/firsat/ivme.csv |
| Kanıt savcısı | SAT kararının 30. günde ayakta kalma oranı | is/firsat/kanit/*.md içinde `sonuc_30gun: ayakta|birakildi` |
| Kreatif analisti | ayrı tutulan videolarda yönü tutan desen oranı | is/kesfet/desen-test.tsv (desen, tuttu: evet|hayir) |
| İçerik stratejisti | 48. saat paylaşım/izlenme medyanı (izlenme ≥ 2000) | is/*/yayin/olcum.csv |
| Kör jüri | jüri sırası ↔ gerçek performans (Spearman ρ, son kalibrasyon) | .ekip/juri-kalibrasyon.jsonl |
| Direktör | kalan videolardan ≤ 3 turda geçenlerin oranı | is/*/elestiri/juri.jsonl |
| Ses tasarımcısı | ses kapısından İLK koşuda geçen video oranı | .ekip/kapi.jsonl (`ses@V`) |
| Kurgu | teknik + kurgu + görüntü kapılarından İLK koşuda geçen video oranı | .ekip/kapi.jsonl |
| Ekip lideri | ilk koşuda geçen geçiş oranı (aşım sayısı ayrıca) | .ekip/kapi.jsonl |
| Mağaza kolu | sepete ekleme oranı (sepete ekleme / oturum) | is/*/magaza/analitik.csv (tarih, oturum, sepete_ekleme, siparis; Shopify analitiğinden yalnız okunur) |

"Bu hafta" = son 7 gün, "Değişim" = önceki 7 güne göre fark; tarih taşımayan kaynakta (olcum.csv, kanıt dosyası) bütün
kayıt kullanılır ve değişim "—" yazılır. Örnek sayısı küçükse (n < 5) değer yine yazılır ama "az örnek" notu düşülür.
Bir rol 3 hafta üst üste "veri yok" kalırsa satıra uyarı eklenir: o rolün gelişim işi durur, kullanıcıya tek soru gider.
Çıkış 0 = karne basıldı · 2 = proje klasörü yok.
"""
import argparse
import csv
import datetime
import glob
import json
import os
import re
import statistics
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

YOK = "veri yok"


def sayi(x):
    try:
        return float(str(x).strip().replace("%", "").replace(",", "."))
    except (TypeError, ValueError):
        return None


def tarih(x):
    m = re.match(r"(\d{4}-\d{2}-\d{2})", str(x or ""))
    try:
        return datetime.date.fromisoformat(m.group(1)) if m else None
    except ValueError:
        return None


def jsonl(yol):
    if not os.path.exists(yol):
        return None
    out = []
    with open(yol, encoding="utf-8") as f:
        for s in f:
            try:
                if s.strip():
                    out.append(json.loads(s))
            except ValueError:
                pass
    return out


def tablo(yol, ayrac=","):
    if not os.path.exists(yol):
        return None
    with open(yol, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader((s for s in f if not s.startswith("#")), delimiter=ayrac)]


def oran(pay, payda):
    return None if not payda else pay / payda


def yuzde(x, basamak=0):
    return YOK if x is None else ("%%%.*f" % (basamak, 100 * x)).replace(".", ",")


class Karne:
    def __init__(self, proje, bugun):
        self.p, self.bugun = proje, bugun
        self.h0 = bugun - datetime.timedelta(days=7)
        self.h1 = bugun - datetime.timedelta(days=14)

    def pencere(self, satirlar, anahtar):
        """(bu hafta, önceki hafta) satır listeleri."""
        bu, once = [], []
        for r in satirlar:
            t = tarih(anahtar(r))
            if t is None:
                continue
            if self.h0 < t <= self.bugun:
                bu.append(r)
            elif self.h1 < t <= self.h0:
                once.append(r)
        return bu, once

    # --- her fonksiyon: (değer metni, değişim metni, örnek metni, eksik kaynak ya da None, ham değer)
    def avci(self):
        yol = os.path.join(self.p, "is", "firsat", "ivme.csv")
        t = tablo(yol)
        if not t:
            return YOK, "—", "0 aday", "is/firsat/ivme.csv (t0 + t7 ölçümü)", None
        urun = {}
        for r in t:
            urun.setdefault((r.get("urun"), r.get("pazar")), {})[(r.get("olcum") or "").lower()] = sayi(r.get("reklam_sayisi"))
        izlenen = {k: v for k, v in urun.items() if v.get("t0") is not None and any(v.get(x) is not None for x in ("t7", "t30"))}
        if not izlenen:
            return YOK, "—", "0 / %d aday yeniden okundu" % len(urun), "ivme.csv'de t7 satırı yok (ivme_olc.py bekleyen)", None
        buyuyen = sum(1 for v in izlenen.values() if (v.get("t30") if v.get("t30") is not None else v["t7"]) > v["t0"])
        x = oran(buyuyen, len(izlenen))
        return yuzde(x), "—", "%d / %d aday yeniden okundu" % (len(izlenen), len(urun)), None, x

    def savci(self):
        dosyalar = glob.glob(os.path.join(self.p, "is", "firsat", "kanit", "*.md"))
        sonuc = []
        for y in dosyalar:
            m = re.search(r"^sonuc_30gun:\s*(\w+)", open(y, encoding="utf-8", errors="replace").read(), re.M | re.I)
            if m:
                sonuc.append(m.group(1).lower())
        if not sonuc:
            return YOK, "—", "%d kanıt dosyası, 0 sonuç" % len(dosyalar), "kanıt dosyasında `sonuc_30gun: ayakta` ya da `birakildi` satırı", None
        x = oran(sum(s.startswith("ayakta") for s in sonuc), len(sonuc))
        return yuzde(x), "—", "%d / %d SAT kararı sonuçlandı" % (len(sonuc), len(dosyalar)), None, x

    def analist(self):
        t = tablo(os.path.join(self.p, "is", "kesfet", "desen-test.tsv"), "\t")
        if not t:
            return YOK, "—", "0 desen sınandı", "is/kesfet/desen-test.tsv (kazanan–kaybeden karşılaştırması)", None
        x = oran(sum((r.get("tuttu") or "").strip().lower().startswith("e") for r in t), len(t))
        return yuzde(x), "—", "%d desen" % len(t), None, x

    def stratejist(self):
        oranlar = []
        dosyalar = glob.glob(os.path.join(self.p, "is", "*", "yayin", "olcum.csv"))
        for y in dosyalar:
            for r in tablo(y) or []:
                iz, pay, saat = sayi(r.get("izlenme")), sayi(r.get("paylasim")), sayi(r.get("saat"))
                if iz and iz >= 2000 and pay is not None and saat in (None, 48.0):
                    oranlar.append(pay / iz)
        if not oranlar:
            return YOK, "—", "0 ölçülmüş yayın", "is/NN/yayin/olcum.csv (48. saat; izlenme ≥ 2000)", None
        x = statistics.median(oranlar)
        return yuzde(x, 2), "—", "%d video (eşik %%0,61)" % len(oranlar), None, x

    def juri(self):
        k = jsonl(os.path.join(self.p, ".ekip", "juri-kalibrasyon.jsonl"))
        if not k:
            return YOK, "—", "0 kalibrasyon", ".ekip/juri-kalibrasyon.jsonl (juri.py kalibrasyon)", None
        son = k[-1]
        if son.get("rho") is None:
            return YOK, "—", "n = %s (%s)" % (son.get("n"), son.get("hukum")), "kalibrasyon seti n ≥ 8 ve performans ölçütü dolu olmalı", None
        once = k[-2].get("rho") if len(k) > 1 and k[-2].get("rho") is not None else None
        degisim = "—" if once is None else ("%+.2f" % (son["rho"] - once)).replace(".", ",")
        return ("ρ %.2f (%s)" % (son["rho"], son.get("hukum"))).replace(".", ","), degisim, "n = %s, %s kopya" % (son.get("n"), son.get("kopya")), None, son["rho"]

    def _juri_satirlari(self):
        out = []
        for y in glob.glob(os.path.join(self.p, "is", "*", "elestiri", "juri.jsonl")):
            for r in jsonl(y) or []:
                r["_is"] = os.path.basename(os.path.dirname(os.path.dirname(y)))
                out.append(r)
        return out

    def direktor(self):
        s = [r for r in self._juri_satirlari() if r.get("mod") == "teslim"]
        if not s:
            return YOK, "—", "0 teslim hükmü", "is/NN/elestiri/juri.jsonl (juri.py birlestir --kayit)", None
        video = {}
        for r in s:
            video.setdefault((r["_is"], str(r.get("video"))), []).append(r)
        kalanlar = {k: v for k, v in video.items() if any(x.get("gecti") is not True for x in v)}
        if not kalanlar:
            return YOK, "—", "%d video, hiçbiri kalmadı" % len(video), "kalan video yok (direktör çağrılmadı)", None
        duzelen = sum(1 for v in kalanlar.values() if any(x.get("gecti") is True and (x.get("tur") or 99) <= 3 for x in v))
        x = oran(duzelen, len(kalanlar))
        return yuzde(x), "—", "%d kalan video" % len(kalanlar), None, x

    def _ilk_kosular(self):
        k = jsonl(os.path.join(self.p, ".ekip", "kapi.jsonl"))
        if k is None:
            return None
        ilk = {}
        for r in k:
            ilk.setdefault((r.get("gecis"), r.get("is")), r)
        return k, ilk

    def _kapi_orani(self, onekler, ad):
        v = self._ilk_kosular()
        if v is None:
            return YOK, "—", "0 kapı koşusu", ".ekip/kapi.jsonl (kapi.py yayin)", None
        k, ilk = v
        durum = {}
        for (gecis, is_), r in ilk.items():
            if gecis != "yayin":
                continue
            for x in r.get("kapilar", []):
                on, _, vid = x["kapi"].partition("@")
                if on in onekler and vid and vid != "V" and x["durum"] != "UYGULANMAZ":
                    durum.setdefault((is_, vid), []).append(x["durum"] == "GEÇTİ")
        if not durum:
            return YOK, "—", "0 video kapıdan geçti", "kapi.py yayin koşusu (%s)" % ad, None
        x = oran(sum(all(d) for d in durum.values()), len(durum))
        return yuzde(x), "—", "%d video" % len(durum), None, x

    def ses(self):
        return self._kapi_orani(("ses",), "ses@V")

    def kurgu(self):
        return self._kapi_orani(("teknik", "kurgu", "goruntu"), "teknik/kurgu/goruntu@V")

    def lider(self):
        v = self._ilk_kosular()
        if v is None:
            return YOK, "—", "0 kapı koşusu", ".ekip/kapi.jsonl (kapi.py kredi / yayin)", None
        k, ilk = v
        bu, once = self.pencere(list(ilk.values()), lambda r: r.get("tarih"))
        asim = sum(1 for r in k if r.get("sonuc") == "AŞIMLA GEÇTİ")
        hesap = lambda rr: oran(sum(r.get("sonuc") == "GEÇTİ" for r in rr), len(rr))
        x, o = hesap(bu), hesap(once)
        if x is None:
            tum = hesap(list(ilk.values()))
            return (yuzde(tum) + " (tüm zaman)") if tum is not None else YOK, "—", "bu hafta 0 geçiş · toplam %d · aşım %d" % (len(ilk), asim), None, tum
        degisim = "—" if o is None else ("%+d puan" % round(100 * (x - o)))
        return yuzde(x), degisim, "%d geçiş · aşım %d" % (len(bu), asim), None, x

    def magaza(self):
        satirlar = []
        for y in glob.glob(os.path.join(self.p, "is", "*", "magaza", "analitik.csv")):
            satirlar += tablo(y) or []
        gecerli = [r for r in satirlar if sayi(r.get("oturum")) and sayi(r.get("sepete_ekleme")) is not None]
        if not gecerli:
            return YOK, "—", "0 gün", "is/NN/magaza/analitik.csv (tarih, oturum, sepete_ekleme, siparis)", None
        bu, once = self.pencere(gecerli, lambda r: r.get("tarih"))
        hesap = lambda rr: oran(sum(sayi(r["sepete_ekleme"]) for r in rr), sum(sayi(r["oturum"]) for r in rr))
        x, o = hesap(bu), hesap(once)
        if x is None:
            return YOK, "—", "son 7 günde 0 gün (toplam %d gün)" % len(gecerli), "analitik.csv'de son 7 günün satırı", None
        degisim = "—" if o is None else ("%+.1f puan" % (100 * (x - o))).replace(".", ",")
        return yuzde(x, 1), degisim, "%d gün · %d oturum" % (len(bu), sum(sayi(r["oturum"]) for r in bu)), None, x


ROLLER = [
    ("Fırsat avcısı", "büyüyen aday oranı (t0 → t7/t30)", "avci"),
    ("Kanıt savcısı", "SAT ayakta kalma (30. gün)", "savci"),
    ("Kreatif analisti", "tutan desen oranı", "analist"),
    ("İçerik stratejisti", "48. saat paylaşım/izlenme medyanı", "stratejist"),
    ("Kör jüri", "performansla uyum (Spearman ρ)", "juri"),
    ("Direktör", "kalan videodan ≤ 3 turda geçen", "direktor"),
    ("Ses tasarımcısı", "ses kapısından ilk koşuda geçen", "ses"),
    ("Kurgu", "teknik + kurgu + görüntü, ilk koşuda geçen", "kurgu"),
    ("Ekip lideri", "ilk koşuda geçen geçiş", "lider"),
    ("Mağaza kolu", "sepete ekleme oranı", "magaza"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--proje", default=".")
    ap.add_argument("--bugun")
    ap.add_argument("--yazma", action="store_true", help="dosya yazma, yalnız bas")
    a = ap.parse_args()
    proje = os.path.abspath(a.proje)
    if not os.path.isdir(proje):
        print("HATA: proje klasörü yok: %s" % proje, file=sys.stderr)
        return 2
    bugun = datetime.date.fromisoformat(a.bugun) if a.bugun else datetime.date.today()
    k = Karne(proje, bugun)
    gecmis = jsonl(os.path.join(proje, ".ekip", "karne.jsonl")) or []
    satirlar, kayit = [], {"tarih": bugun.isoformat(), "roller": {}}
    for rol, metrik, fn in ROLLER:
        deger, degisim, ornek, eksik, ham = getattr(k, fn)()
        m = re.search(r"\b(\d+)\b", ornek)
        if ham is not None and m and int(m.group(1)) < 5 and "az örnek" not in ornek:
            ornek += " (az örnek)"
        # 3 hafta üst üste veri yok mu (farklı haftalardaki önceki kayıtlar + bu koşu)
        onceki = [g for g in gecmis if g.get("tarih") and (bugun - datetime.date.fromisoformat(g["tarih"])).days >= 6]
        haftalar = {}
        for g in onceki:
            hafta = (bugun - datetime.date.fromisoformat(g["tarih"])).days // 7
            haftalar[hafta] = g.get("roller", {}).get(rol)
        ust_uste = 1 if ham is None else 0
        for h in sorted(haftalar):
            if ham is None and haftalar[h] is None and h == ust_uste:
                ust_uste += 1
        sonraki = ("eksik: " + eksik) if eksik else ""
        if ham is None and ust_uste >= 3:
            sonraki = "3 HAFTA VERİ YOK → kullanıcıya tek soru: veri mi gelecek, rol mü kapanacak · " + sonraki
        satirlar.append("| %s | %s | %s | %s | %s | %s |" % (rol, metrik, deger, degisim, ornek, sonraki))
        kayit["roller"][rol] = ham
    dolu = sum(v is not None for v in kayit["roller"].values())
    metin = ("# Ekip karnesi — %s (son 7 gün)\n\nBetik üretti (`karne_uret.py`); sayılar proje kayıtlarından. \"veri yok\" = kaynak dosya yok ya da boş; "
             "tahmin yazılmaz.\nVerisi olan rol: %d / %d.\n\n| Rol | Sonuç metriği | Bu hafta | Değişim | Örnek | Sonraki tek deneme |\n|---|---|---|---|---|---|\n"
             % (bugun.isoformat(), dolu, len(ROLLER))) + "\n".join(satirlar) + "\n"
    print(metin)
    ekip = os.path.join(proje, ".ekip")
    if not a.yazma and os.path.isdir(ekip):
        with open(os.path.join(ekip, "KARNE.md"), "w", encoding="utf-8") as f:
            f.write(metin)
        with open(os.path.join(ekip, "karne.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
