#!/usr/bin/env python3
"""Kurgu ön-kontrol kapısı: hizli_kurgu ayar dosyasını (ve verilirse çıktı videoyu) eleştirmenden ÖNCE ölçer.

Kullanım:
  python3 kurgu_kontrol.py AYAR.json [AYAR2.json ...] [--video VIDEO.mp4] [--drop 3.429] [--etiket klip_etiket.json]
                           [--esik ad=deger ...] [--gevset KURAL ...] [--json]
Çıkış: herhangi bir ayarda HATA varsa 1, yoksa 0. UYARI çıkışı değiştirmez.

Klip etiketi: her klibin ekranda ne gösterdiği ayar dosyasından okunamaz; `klip_etiket.json`dan gelir. Varsayılan:
kullanılan kliplerin klasöründeki `klip_etiket.json` (birden fazla klasör varsa hepsi birleşir). Biçim dosyanın
`_bicim` alanında: klipler[ad] = {arac, rol, tur, icerik, plan, secim, secim_sn, arac_renk, kusur, kaynak}.
tur: urun · stok · arac_stok · urun_elde · sokum · telefon · bilinmiyor.  Etiketsiz klip = UYARI (ölçülemedi).

Kurallar (SKILL.md "Viral kurgu" + eleştiri turları; eşikler ESIK sözlüğünde, --esik ile değişir):
 stok      durağan stok rozet (tur=stok) toplamı; ilk ya da son plan stok olamaz. Ayarda "meme": true ise atlanır.
 urun      değişmiş ekran (tur=urun) ilk 0,9 sn içinde başlar.
 kanca     ilk yazı ≤ 2 satır (hizli_kurgu satır kırması + font ölçüsü); ilk 1,71 sn'de telefon/stok plan üstünde değil.
 yazi_yeri yakın planda (kirp ≥ 1,3) yazı konumu > 0,15 ise kırpılmış öznenin (rozet) bandıyla çakışma = HATA, yoksa UYARI.
 telefon   telefonda seçilen içerik aracın içeriklerinden olmalı; sonraki ilk ürün planı ve kapanış aynı içerik;
           araya başka ikon girmez (stok/geniş stok = UYARI).
 tekrar    aynı klipte ≥ %50 örtüşen aralık (UYARI); etiketteki kusur aralığı kullanılırsa HATA;
           araçla uyumsuz ortak klip ilk plan ya da > 0,9 sn ise HATA.
 okunma    yazı ekranda ≥ 0,5 + 0,25 × kelime sn (hizli_kurgu ile aynı hesap) — ihlal HATA.
 plan      plan ≥ 2 vuruş (0,857 sn − tolerans); toplam 10–15 sn.
 dongu     son planın ekran içeriği ilk planınkiyle aynı (son plan ilk kareye bağlanır).
 ses       (--video) ses_olc.py: drop_artis ≥ 6 dB, ≥ 0,3 sn −28 dB altı delik yok, −14 ± 1 LUFS.
Betik eleştirmenin yerini almaz: kanca gücü, gerçekçilik, ritim yargısı eleştirmende kalır.
"""
import argparse
import json
import os
import subprocess
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)
from hizli_kurgu import font_yukle, okunma_gerek, satirlara_bol, H  # noqa: E402

ESIK = {
    "stok_uyari_sn": 0.86,     # SKILL: durağan stok plan ≤ 0,86 sn
    "stok_hata_sn": 1.75,      # ilk turda geçen 09/12'de stok toplamı 1,71 sn → HATA sınırı 2 vuruş (bkz. rapor)
    "urun_ilk_sn": 0.9,
    "kanca_sn": 1.714,
    "kanca_satir": 2,
    "yakin_kirp": 1.3,
    "yazi_ust_konum": 0.15,
    "ozne_bant": 0.12,         # kırpılmış öznenin merkezinden ± bu oran (kare yüksekliği) = rozet/plaka bandı
    "ortak_uyumsuz_sn": 0.9,
    "tekrar_orani": 0.5,
    "min_plan_sn": 0.80,       # 2 vuruş = 0,857 sn; 0,83'lük ızgara kayması tolere
    "toplam_min": 10.0,
    "toplam_max": 15.0,
    "drop_db": 6.0,
    "delik_db": -28.0,
    "delik_sn": 0.3,
    "lufs": -14.0,
    "lufs_tol": 1.0,
}
STOKLU = ("stok", "arac_stok")


def etiketleri_yukle(ayar_yol, a, ek):
    kok = os.path.dirname(ayar_yol)
    yollar = list(ek or [])
    for p in a["planlar"]:
        y = os.path.join(os.path.dirname(os.path.join(kok, p["klip"])), "klip_etiket.json")
        if os.path.exists(y) and os.path.abspath(y) not in map(os.path.abspath, yollar):
            yollar.append(y)
    klipler, araclar = {}, {}
    for y in yollar:
        d = json.load(open(y, encoding="utf-8"))
        klipler.update(d.get("klipler", {}))
        araclar.update(d.get("araclar", {}))
    return klipler, araclar, yollar


def zaman_cizelgesi(a, klipler):
    t, planlar = 0.0, []
    for i, p in enumerate(a["planlar"]):
        sure = (p["bit"] - p["bas"]) / p.get("hiz", 1.0)
        ad = os.path.splitext(os.path.basename(p["klip"]))[0]
        planlar.append({"i": i, "t0": t, "t1": t + sure, "sure": sure, "ad": ad, "p": p, "e": klipler.get(ad)})
        t += sure
    return planlar


def ekran(pl):
    """Planın araç ekranında görünen içerik (telefon planında araç görünüyorsa arac_icerik)."""
    e = pl["e"] or {}
    if e.get("tur") == "telefon":
        return e.get("arac_icerik")
    return e.get("icerik")


def yazi_listesi(a, planlar):
    """(bas, bit, yazı sözlüğü, kaynak) — zaman çizelgesi yazıları + plan yazıları + CTA."""
    out = [(y["bas"], y["bit"], y, "yazilar") for y in a.get("yazilar", [])]
    for pl in planlar:
        p = pl["p"]
        if p.get("yazi"):
            out.append((pl["t0"], pl["t1"], {"yazi": p["yazi"], "boyut": p.get("boyut", 112), "konum": p.get("konum", 0.16)}, "plan"))
    cta = a.get("cta")
    if cta:
        for pl in planlar[cta["plan"]:]:
            out.append((pl["t0"], pl["t1"], {"yazi": cta["satir1"], "boyut": 100, "satir2": cta["satir2"], "boyut2": 58,
                                             "konum": cta.get("konum", 0.16)}, "cta"))
    return out


def satir_sayisi(y, font_yol, agirlik):
    from PIL import Image, ImageDraw
    d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    n = len(satirlara_bol(d, y["yazi"], font_yukle(font_yol, y.get("boyut", 96), agirlik)))
    n2 = len(satirlara_bol(d, y["satir2"], font_yukle(font_yol, y.get("boyut2", 60), agirlik))) if y.get("satir2") else 0
    return n, n2


def ortusme(a0, a1, b0, b1):
    return max(0.0, min(a1, b1) - max(a0, b0))


def kontrol(ayar_yol, args, esik):
    a = json.load(open(ayar_yol, encoding="utf-8"))
    kok = os.path.dirname(os.path.abspath(ayar_yol))
    font = a.get("font", "")
    font = font if os.path.isabs(font) else os.path.join(kok, font)
    klipler, araclar, etiket_yollari = etiketleri_yukle(ayar_yol, a, args.etiket)
    planlar = zaman_cizelgesi(a, klipler)
    hata, uyari = [], []

    def H_(k, m):  # aynı plan iki kez kullanılınca aynı mesaj tekrar yazılmaz
        if {"kural": k, "mesaj": m} not in hata:
            hata.append({"kural": k, "mesaj": m})

    def U_(k, m):
        if {"kural": k, "mesaj": m} not in uyari:
            uyari.append({"kural": k, "mesaj": m})
    f2 = lambda x: f"{x:.2f}"

    for pl in planlar:
        if pl["e"] is None:
            U_("etiket", f"plan {pl['i']} ({pl['ad']}) etiketsiz — içerik kuralları bu planda ölçülemedi")
    sayac = {}
    for pl in planlar:
        c = (pl["e"] or {}).get("arac")
        if c:
            sayac[c] = sayac.get(c, 0) + pl["sure"]
    arac_kod = max(sayac, key=sayac.get) if sayac else None
    arac = araclar.get(arac_kod, {})
    icerikler = set(arac.get("icerikler", []))
    tur = lambda pl: (pl["e"] or {}).get("tur", "bilinmiyor")

    # 1 — stok
    if not a.get("meme"):
        stok = [pl for pl in planlar if tur(pl) == "stok"]
        top = sum(pl["sure"] for pl in stok)
        if top > esik["stok_hata_sn"]:
            H_("stok", f"durağan stok toplamı {f2(top)} sn > {esik['stok_hata_sn']} sn (planlar {[pl['i'] for pl in stok]})")
        elif top > esik["stok_uyari_sn"] + 0.01:
            U_("stok", f"durağan stok toplamı {f2(top)} sn > {esik['stok_uyari_sn']} sn (SKILL hedefi)")
        for pl in stok:
            if pl["sure"] > esik["stok_uyari_sn"] + 0.05:
                U_("stok", f"plan {pl['i']} ({pl['ad']}) tek stok plan {f2(pl['sure'])} sn > {esik['stok_uyari_sn']}")
        if planlar and tur(planlar[0]) == "stok":
            H_("stok", f"ilk plan durağan stok ({planlar[0]['ad']})")
        if planlar and tur(planlar[-1]) in STOKLU:
            H_("stok", f"video stok rozetle bitiyor ({planlar[-1]['ad']})")

    # 2 — ürün ilk 0,9 sn
    ilk_urun = next((pl for pl in planlar if tur(pl) == "urun" or (tur(pl) == "telefon" and ekran(pl) and not str(ekran(pl)).startswith("stok"))), None)
    if ilk_urun is None:
        H_("urun", "videoda değişmiş ekranlı plan yok")
    elif ilk_urun["t0"] >= esik["urun_ilk_sn"]:
        once = [pl["ad"] for pl in planlar if pl["t0"] < ilk_urun["t0"]]
        bilinmez = any(tur(pl) == "bilinmiyor" for pl in planlar if pl["t0"] < ilk_urun["t0"])
        (U_ if bilinmez else H_)("urun", f"değişmiş ekran ilk kez {f2(ilk_urun['t0'])} sn'de (≥ {esik['urun_ilk_sn']}); önce: {once}")

    # 3 — kanca
    ylist = yazi_listesi(a, planlar)
    kanca = next(((b, e, y) for b, e, y, _ in sorted(ylist, key=lambda x: x[0]) if b < 0.05), None)
    if kanca is None:
        H_("kanca", "ilk karede kanca yazısı yok")
    else:
        b, e, y = kanca
        try:
            n, n2 = satir_sayisi(y, font, a.get("font_agirlik"))
            if n + n2 > esik["kanca_satir"]:
                H_("kanca", f"kanca '{y['yazi']}' {n + n2} satır (≤ {esik['kanca_satir']})")
        except OSError as ex:
            U_("kanca", f"font açılamadı, satır sayısı ölçülmedi: {ex}")
        if e - b > esik["kanca_sn"] + 0.01:
            U_("kanca", f"kanca yazısı {f2(e - b)} sn ekranda (> {esik['kanca_sn']}; ilk turda geçen 09/12'de 2,14 sn)")
        for pl in planlar:
            o = ortusme(b, min(e, esik["kanca_sn"]), pl["t0"], pl["t1"])
            if o > 0.05:
                if tur(pl) in ("telefon", "stok"):
                    H_("kanca", f"kanca '{y['yazi']}' {f2(pl['t0'])}–{f2(pl['t1'])} sn'de {tur(pl)} planı üstünde ({pl['ad']}); kanca ürünlü planda olmalı")
                elif tur(pl) in ("arac_stok", "bilinmiyor"):
                    U_("kanca", f"kanca {f2(pl['t0'])}–{f2(pl['t1'])} sn'de {tur(pl)} planı üstünde ({pl['ad']})")

    # 4 — yazı yeri (yakın planda rozet/plaka bandı)
    for b, e, y, kaynak in ylist:
        konum = y.get("konum", 0.16)
        if konum <= esik["yazi_ust_konum"]:
            continue
        try:
            n, n2 = satir_sayisi(y, font, a.get("font_agirlik"))
        except OSError:
            n, n2 = 1, 1 if y.get("satir2") else 0
        yuk = (n * y.get("boyut", 96) * 1.12 + n2 * y.get("boyut2", 60) * 1.12) / H
        for pl in planlar:
            k = pl["p"].get("kirp") or 1.0
            if ortusme(b, e, pl["t0"], pl["t1"]) < 0.05 or k < esik["yakin_kirp"]:
                continue
            fy = pl["p"].get("kirp_merkez", [0.5, 0.5])[1]
            ch = 1.0 / k
            ust = min(max(0.0, fy - ch / 2), 1 - ch)
            ozne = (fy - ust) / ch
            if ortusme(konum, konum + yuk, ozne - esik["ozne_bant"], ozne + esik["ozne_bant"]) > 0:
                H_("yazi_yeri", f"'{y['yazi']}' (konum {konum}) plan {pl['i']} {pl['ad']} kirp {k}: öznenin bandında ({f2(ozne)}±{esik['ozne_bant']}) — rozet/plaka üstünde")
            else:
                U_("yazi_yeri", f"'{y['yazi']}' (konum {konum}) yakın plan {pl['i']} {pl['ad']} kirp {k}: konum > {esik['yazi_ust_konum']}, panoda plaka/ürün çakışmasına bak")

    # 5 — telefon karosu = araç ekranı
    for pl in planlar:
        e = pl["e"] or {}
        if e.get("tur") != "telefon":
            continue
        secim, ssn = e.get("secim"), e.get("secim_sn")
        if secim is None or ssn is None:
            U_("telefon", f"plan {pl['i']} {pl['ad']}: etikette seçim/secim_sn yok")
            continue
        if pl["p"]["bit"] <= ssn:
            U_("telefon", f"plan {pl['i']} {pl['ad']}: kullanılan aralık seçim anından ({ssn} sn) önce bitiyor — seçim görünmüyor")
            continue
        if icerikler and secim not in icerikler:
            H_("telefon", f"plan {pl['i']} {pl['ad']}: telefonda '{secim}' seçiliyor ama {arac.get('ad', arac_kod)} içerikleri {sorted(icerikler)}")
        if e.get("arac_icerik") and e["arac_icerik"] != secim:
            H_("telefon", f"plan {pl['i']} {pl['ad']}: telefonda '{secim}', aynı karede araçta '{e['arac_icerik']}'")
        sonra = [q for q in planlar[pl["i"] + 1:] if tur(q) in ("urun",) + STOKLU or (tur(q) == "telefon" and ekran(q))]
        ilk_urun_sonra = next((q for q in sonra if tur(q) == "urun"), None)
        if ilk_urun_sonra and ekran(ilk_urun_sonra) != secim:
            H_("telefon", f"telefonda '{secim}' seçildi, sonraki ilk ürün planı {ilk_urun_sonra['i']} ({ilk_urun_sonra['ad']}) '{ekran(ilk_urun_sonra)}' gösteriyor")
        for q in sonra:
            if q is ilk_urun_sonra:
                continue
            if tur(q) in STOKLU:
                U_("telefon", f"telefonda '{secim}' seçildikten sonra plan {q['i']} ({q['ad']}) fabrika logosu gösteriyor")
            elif ekran(q) != secim:
                H_("telefon", f"telefonda '{secim}' seçildikten sonra plan {q['i']} ({q['ad']}, {f2(q['t0'])} sn) '{ekran(q)}' gösteriyor")
        if planlar[-1]["i"] > pl["i"] and ekran(planlar[-1]) != secim and tur(planlar[-1]) not in STOKLU:
            H_("telefon", f"telefonda '{secim}' seçildi, video '{ekran(planlar[-1])}' ile bitiyor")

    # 6 — tekrar, kusur aralığı, uyumsuz ortak klip
    for i, p1 in enumerate(planlar):
        for p2 in planlar[i + 1:]:
            if p1["p"]["klip"] != p2["p"]["klip"]:
                continue
            o = ortusme(p1["p"]["bas"], p1["p"]["bit"], p2["p"]["bas"], p2["p"]["bit"])
            kisa = min(p1["p"]["bit"] - p1["p"]["bas"], p2["p"]["bit"] - p2["p"]["bas"])
            if kisa > 0 and o / kisa >= esik["tekrar_orani"]:
                U_("tekrar", f"{p1['ad']} aynı aralık iki kez: plan {p1['i']} [{p1['p']['bas']}–{p1['p']['bit']}] ve plan {p2['i']} [{p2['p']['bas']}–{p2['p']['bit']}] (%{100 * o / kisa:.0f})")
    for pl in planlar:
        for k in (pl["e"] or {}).get("kusur", []):
            if ortusme(pl["p"]["bas"], pl["p"]["bit"], k["bas"], k["bit"]) > 0.02:
                H_("tekrar", f"plan {pl['i']} {pl['ad']} [{pl['p']['bas']}–{pl['p']['bit']}] etiketteki kusur aralığını [{k['bas']}–{k['bit']}] kullanıyor: {k['neden']}")
        e = pl["e"] or {}
        if e and e.get("arac") is None and e.get("tur") in ("urun_elde", "telefon", "sokum"):
            neden = []
            ic = e.get("secim") if e.get("tur") == "telefon" else e.get("icerik")
            if icerikler and ic and not ic.startswith("stok") and ic not in icerikler:
                neden.append(f"ikon '{ic}' bu aracın içeriği değil")
            if e.get("arac_renk") and arac.get("renk") and e["arac_renk"] not in arac["renk"]:
                neden.append(f"araç rengi {e['arac_renk']} ≠ {arac['renk']}")
            yer = "ilk plan" if pl["i"] == 0 else f2(pl["sure"]) + " sn"
            if neden and (pl["i"] == 0 or pl["sure"] > esik["ortak_uyumsuz_sn"]):
                H_("tekrar", f"uyumsuz ortak klip {pl['ad']} ({'; '.join(neden)}) {yer}")
            elif neden:
                U_("tekrar", f"uyumsuz ortak klip {pl['ad']} ({'; '.join(neden)}) {f2(pl['sure'])} sn")

    # 7 — okunma (hizli_kurgu UYARI'sıyla aynı hesap)
    for y in a.get("yazilar", []):
        gerek = okunma_gerek(y)
        if y["bit"] - y["bas"] < gerek - 1e-6:
            H_("okunma", f"'{y['yazi']}' {f2(y['bit'] - y['bas'])} sn ekranda, en az {f2(gerek)} sn gerekir")

    # plan süresi ve toplam
    for pl in planlar:
        if pl["sure"] < esik["min_plan_sn"]:
            H_("plan", f"plan {pl['i']} {pl['ad']} {f2(pl['sure'])} sn < 2 vuruş ({esik['min_plan_sn']})")
    toplam = planlar[-1]["t1"] if planlar else 0
    if not esik["toplam_min"] <= toplam <= esik["toplam_max"]:
        H_("plan", f"toplam {f2(toplam)} sn ({esik['toplam_min']}–{esik['toplam_max']} dışında)")

    # döngü
    if len(planlar) > 1:
        ilk, son = planlar[0], planlar[-1]
        ik = "telefon" if tur(ilk) == "telefon" else ekran(ilk)
        sk = "telefon" if tur(son) == "telefon" else ekran(son)
        if ik is None or sk is None or "bilinmiyor" in (ik, sk):
            U_("dongu", f"ilk/son plan içeriği bilinmiyor ({ilk['ad']} / {son['ad']})")
        elif ik != sk:
            H_("dongu", f"son plan '{sk}' ({son['ad']}) ilk plana '{ik}' ({ilk['ad']}) bağlanmıyor — döngüde içerik değişiyor")

    # 8 — ses
    ses = None
    if args.video:
        drop = args.drop if args.drop is not None else a.get("drop_sn", 3.429)
        r = subprocess.run([sys.executable, os.path.join(BURASI, "ses_olc.py"), args.video, "--drop", str(drop),
                            "--delik_db", str(esik["delik_db"]), "--delik_sn", str(esik["delik_sn"])], capture_output=True, text=True)
        if r.returncode:
            H_("ses", f"ses_olc.py çalışmadı: {r.stderr.strip()[-200:]}")
        else:
            ses = json.loads(r.stdout)
            da = ses.get("drop_artis_db")
            if da is None or da < esik["drop_db"]:
                H_("ses", f"drop artışı {da} dB < {esik['drop_db']} dB ({drop} sn)")
            if ses["delikler"]:
                H_("ses", f"{esik['delik_db']} dB altı ≥ {esik['delik_sn']} sn delik: {ses['delikler']}")
            if abs(ses["I_lufs"] - esik["lufs"]) > esik["lufs_tol"]:
                H_("ses", f"ses {ses['I_lufs']} LUFS (hedef {esik['lufs']} ± {esik['lufs_tol']})")

    for g in args.gevset or []:  # profil: bu kuralın HATA'ları UYARI'ya iner (başka ürün tipi / bilinçli istisna)
        uyari += [dict(h, mesaj="(gevşetildi) " + h["mesaj"]) for h in hata if h["kural"] == g]
        hata = [h for h in hata if h["kural"] != g]
    return {"ayar": ayar_yol, "arac": arac.get("ad", arac_kod), "sure_sn": round(toplam, 2), "etiket": etiket_yollari,
            "hatalar": hata, "uyarilar": uyari, "ses": ses, "gecti": not hata}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ayar", nargs="+")
    ap.add_argument("--video", help="çıktı video (ses kuralları için; tek ayarla)")
    ap.add_argument("--drop", type=float, help="drop'un videodaki sn'si (varsayılan ayar 'drop_sn' ya da 3.429)")
    ap.add_argument("--etiket", action="append", help="ek klip_etiket.json (birden fazla verilebilir)")
    ap.add_argument("--esik", action="append", default=[], help="eşik değiştir: ad=deger (ör. stok_hata_sn=0.86)")
    ap.add_argument("--gevset", action="append", help="bu kuralın HATA'larını UYARI yap (ör. --gevset dongu); raporda yazılır")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.video and len(args.ayar) > 1:
        sys.exit("--video tek ayar dosyasıyla kullanılır")
    esik = dict(ESIK)
    for s in args.esik:
        ad, _, v = s.partition("=")
        if ad not in esik:
            sys.exit(f"bilinmeyen eşik: {ad} (seçenekler: {', '.join(esik)})")
        esik[ad] = float(v)
    sonuclar = [kontrol(y, args, esik) for y in args.ayar]
    if args.json:
        print(json.dumps(sonuclar if len(sonuclar) > 1 else sonuclar[0], ensure_ascii=False, indent=1))
    else:
        for s in sonuclar:
            print(f"== {s['ayar']}  ({s['arac']}, {s['sure_sn']} sn)")
            for h in s["hatalar"]:
                print(f"HATA  [{h['kural']}] {h['mesaj']}")
            for u in s["uyarilar"]:
                print(f"UYARI [{u['kural']}] {u['mesaj']}")
            print(f"özet: {len(s['hatalar'])} hata, {len(s['uyarilar'])} uyarı → {'GEÇTİ' if s['gecti'] else 'KALDI'}")
    sys.exit(0 if all(s["gecti"] for s in sonuclar) else 1)


if __name__ == "__main__":
    main()
