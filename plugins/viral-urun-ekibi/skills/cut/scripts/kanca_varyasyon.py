#!/usr/bin/env python3
"""Kanca varyasyon testi: AYNI çekimden N (≥10) kanca sürümü üretir (tek ayardan N ayar + N video) ve yayın/ölçüm kaydını yazar.

  python3 kanca_varyasyon.py AYAR.json KANCALAR.json [--render] [--en-az 10] [--sira-saat 24]
AYAR.json   hizli_kurgu ayarı (kutulu stil + ön-üretim kartı dahil); ilk yazı (yazilar[0] ya da planlar[0].yazi) kanca yerine geçer.
KANCALAR.json  [{"id": "V01", "aile": "K1", "yazi": "DO NOT show this to a DOG MOM", "vurgu": "DOG MOM", "kanit": ["[037]"]}, …]
Çıktı: AYAR yanında varyasyon_V01.json … · varyasyon/yayin-plani.md · varyasyon/kayit.tsv (olcum-ve-test-plani.md §4 sütunları).
Kapılar (HATA → çıkış 1): ≥ --en-az (10) kanca · kimlikler ve kanca yazıları benzersiz · her aile K<n> ve kanıt numarası kanca-kutuphanesi.md'de ·
  TR ayarında kanca ≤ 8 kelime · yalnız KANCA değişir (diğer her alan aynı çekimden gelir).
--render: her varyasyonu hizli_kurgu.py ile üretir (kart kapısı orada da işler).
Karar eşikleri ve 48. saat kuralı: studio/referans/olcum-ve-test-plani.md §3.
"""
import argparse
import copy
import json
import os
import re
import subprocess
import sys

B = os.path.dirname(os.path.abspath(__file__))
KUT = os.path.join(B, "..", "..", "studio", "referans", "kanca-kutuphanesi.md")


def dogrula(kancalar, pazar, en_az):
    h = []
    if len(kancalar) < en_az:
        h.append("%d kanca var, en az %d gerekli (drop-marka hesapları aynı çekimle 10–25 kanca dener; hit oranı ~1/25)" % (len(kancalar), en_az))
    kut = open(KUT, encoding="utf-8").read()
    idler, yazilar = set(), set()
    for k in kancalar:
        i, y = k.get("id"), (k.get("yazi") or "").strip()
        if not i or i in idler:
            h.append("kimlik boş ya da tekrar: %r" % i)
        idler.add(i)
        if y.lower() in yazilar:
            h.append("%s: kanca yazısı başka varyasyonla aynı" % i)
        yazilar.add(y.lower())
        fam = str(k.get("aile", ""))
        if not re.fullmatch(r"K\d{1,2}", fam) or not re.search(r"^### %s\. " % fam, kut, re.M):
            h.append("%s: aile %r kütüphanede yok" % (i, fam))
        if not k.get("kanit") or any(str(x) not in kut for x in k["kanit"]):
            h.append("%s: kanıt numarası kütüphanede yok/boş" % i)
        if not y and fam != "K13":
            h.append("%s: kanca yazısı boş (yalnız K13 yazısızdır)" % i)
        if pazar == "TR" and len(y.split()) > 8:
            h.append("%s: TR kancası %d kelime (≤ 8)" % (i, len(y.split())))
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ayar")
    ap.add_argument("kancalar")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--en-az", type=int, default=10)
    ap.add_argument("--sira-saat", type=int, default=24, help="iki yayın arası saat (varsayılan 24)")
    a = ap.parse_args()
    kok = os.path.dirname(os.path.abspath(a.ayar))
    ayar = json.load(open(a.ayar, encoding="utf-8"))
    kancalar = json.load(open(a.kancalar, encoding="utf-8"))
    pazar = ayar.get("pazar")
    if not pazar and ayar.get("on_uretim_karti"):
        try:
            pazar = json.load(open(os.path.join(kok, ayar["on_uretim_karti"]), encoding="utf-8")).get("pazar")
        except (OSError, ValueError):
            pass
    h = dogrula(kancalar, pazar, a.en_az)
    if h:
        for x in h:
            print("HATA:", x)
        return 1
    out = os.path.join(kok, "varyasyon")
    os.makedirs(out, exist_ok=True)
    satirlar = []
    for n, k in enumerate(kancalar):
        v = copy.deepcopy(ayar)
        if v.get("yazilar"):
            v["yazilar"][0]["yazi"] = k["yazi"]
            v["yazilar"][0]["vurgu"] = k.get("vurgu", "")
        elif v.get("planlar"):
            v["planlar"][0]["yazi"] = k["yazi"]
            v["planlar"][0]["vurgu"] = k.get("vurgu", "")
        v["cikti"] = "varyasyon/%s.mp4" % k["id"]
        # ayar kök klasöre göre göreli yollar: varyasyon/ içinden bir üst klasöre göre çözülsün diye ayarı kökte yaz
        yol = os.path.join(kok, "varyasyon_%s.json" % k["id"])
        json.dump(v, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if a.render:
            r = subprocess.run([sys.executable, os.path.join(B, "hizli_kurgu.py"), yol], capture_output=True, text=True)
            if r.returncode:
                print("HATA: %s render çıkış %d: %s" % (k["id"], r.returncode, (r.stdout + r.stderr)[-300:]))
                return 1
        satirlar.append((k, n))
    with open(os.path.join(out, "yayin-plani.md"), "w", encoding="utf-8") as f:
        f.write("# Yayın planı (%d varyasyon, aynı çekim)\n\nAralık: %d saat. Ölçüm: yayından 24 s / 48 s / 7 gün (`studio/referans/olcum-ve-test-plani.md` §3–4). Karar 48. saatte, ≥ 2.000 izlenmede.\n\n| Sıra | Video | Aile | Kanca | Kanıt | Yayın (gün/saat) |\n|---|---|---|---|---|---|\n" % (len(kancalar), a.sira_saat))
        for k, n in satirlar:
            f.write("| %d | %s | %s | %s | %s | T+%d sa |\n" % (n + 1, k["id"], k["aile"], k.get("yazi", "").replace("|", "/"), " ".join(k["kanit"]), n * a.sira_saat))
        f.write("\nParti kararı: hiçbiri DEVAM değilse görüntüyü değiştir (kancayı değil), yeni klip setiyle 2. parti. Kazanan: aynı kanca + yeni sahne ya da aynı görüntü + 3 yeni kanca.\n")
    with open(os.path.join(out, "kayit.tsv"), "w", encoding="utf-8") as f:
        f.write("\t".join(["Video", "Değişken", "Şablon", "Kanca (aile)", "Süre", "CTA", "Format", "Pazar", "Yayın tarihi/saat", "Takipçi (yayında)", "24s izlenme", "48s izlenme", "48s beğeni", "48s yorum", "48s paylaşım", "48s repost", "Ses etiketi", "7g izlenme", "pay/iz", "beğ/iz", "hesap-içi kat", "Karar"]) + "\n")
        for k, n in satirlar:
            f.write("\t".join([k["id"], "kanca", "", "%s (%s)" % (k.get("yazi", ""), k["aile"])] + [""] * 18) + "\n")
    print("TAMAM %d varyasyon → %s (yayin-plani.md, kayit.tsv)%s" % (len(satirlar), out, " + videolar" if a.render else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
