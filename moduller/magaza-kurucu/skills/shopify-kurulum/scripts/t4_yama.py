# -*- coding: utf-8 -*-
"""T4.5 şablon yaması: Ana Tema JSON şablonunda YALNIZ verilen ayarları değiştirir.

Yalnız standart kütüphane (json, re, argparse). ChatGPT/Claude kod aracında çalışır.

Kullanım
  python t4_yama.py --sablon index.json --yama yama.json --cikti out.json
  python t4_yama.py --sablon index.json --yama yama.json --cikti out.json --haric faq
  python t4_yama.py --kontrol sunucudan.json --taban index.json --yama yama.json   # yazdıktan sonra
  python t4_yama.py --sozluk-uret <tema_kok> --cikti ayar-sozlugu.json             # yönetici

yama.json biçimi (ikisi de olur):
  [{"yol": "e-serit/c1/i.icon", "deger": "truck"}, {"yol": "e-kars.disabled", "deger": true}]
  {"degisiklikler": [...], "haric": ["faq"], "bloklar": [ {blok ekleme, yalnız haric bölümde} ]}
  blok ekleme: {"bolum": "faq", "id": "q7", "type": "question", "settings": {...}, "sonra": "q6"}
  yol: "<bölüm>[/<blok>/<alt blok>...].<ayar>"; ayar "disabled" ise bölüm/blok açılır-kapanır.
  config/settings_data.json için yol yalnız ayar adıdır ("type_body_font"); etkin preset'e yazılır.

Durdurulan hatalar (çıkış kodu 1, çıktı dosyası YAZILMAZ):
  - bölüm ya da blok yok; ayar adı ne şablonda ne tema şemasında (ayar-sozlugu.json) var;
  - değer şemadaki tipe uymuyor (checkbox, range sınırı, select seçeneği, richtext etiketi, görsel adresi);
  - aynı yol iki kez; yama sonrası bölüm/blok sayısı, sırası ya da tipi değişti.
Çıkış kodu: 0 = geçti, 1 = YAZMA, 2 = kullanım hatası.
"""
import argparse
import copy
import glob
import hashlib
import json
import os
import re
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
SOZLUK_ADI = "ayar-sozlugu.json"


class YamaHatasi(Exception):
    pass


# ------------------------------------------------------------------ okuma
def oku_metin(metin):
    """Baştaki /* ... */ yorumunu atıp JSON ayrıştırır (Shopify şablonlarının başında yorum olabilir)."""
    metin = metin.lstrip("﻿")
    metin = re.sub(r"^\s*/\*.*?\*/", "", metin, count=1, flags=re.S)
    return json.loads(metin)


def oku_dosya(yol):
    with open(yol, encoding="utf-8") as f:
        return oku_metin(f.read())


def sozluk_yukle(yol=None):
    adaylar = [yol] if yol else [os.path.join(BURADA, SOZLUK_ADI),
                                 os.path.join(BURADA, "..", "references", SOZLUK_ADI)]
    for p in adaylar:
        if p and os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return json.load(f), p
    if yol:
        raise YamaHatasi("sözlük bulunamadı: %s" % yol)
    return None, None


# ------------------------------------------------------------------ şema
def ayar_tanimlari(sozluk, tur, tip, kok_bolum_tipi=None):
    """tur: 'bolum' | 'blok' | 'genel'. Döner: {ayar_id: tanım} ya da None (bilinmiyor)."""
    if not sozluk:
        return None
    if tur == "genel":
        return sozluk.get("genel")
    if tur == "bolum":
        b = sozluk.get("bolumler", {}).get(tip)
        return None if b is None else b.get("a", {})
    yerel = sozluk.get("bolumler", {}).get(kok_bolum_tipi or "", {}).get("b", {})
    if tip in yerel:
        return yerel[tip]
    return sozluk.get("bloklar", {}).get(tip)


RICHTEXT_KOK = re.compile(r"^\s*<(p|ul|ol|h[1-6])[\s>]", re.I)
SAYI = (int, float)
METIN_TIPLER = {"text", "textarea", "richtext", "inline_richtext", "html", "liquid", "url", "image_picker",
                "video", "video_url", "color", "color_background", "font_picker", "product", "collection",
                "page", "blog", "article", "link_list", "metaobject", "color_scheme"}


def deger_kontrol(yol, tanim, deger):
    """Şemadaki tipe göre değer kontrolü. tanim: "checkbox" ya da {"t": "...", ...}."""
    if isinstance(tanim, str):
        tanim = {"t": tanim}
    t = tanim.get("t")
    if t == "checkbox":
        if not isinstance(deger, bool):
            raise YamaHatasi("%s: checkbox true/false olmalı, gelen %r" % (yol, deger))
    elif t in ("range", "number"):
        if deger is None and t == "number":
            return
        if isinstance(deger, bool) or not isinstance(deger, SAYI):
            raise YamaHatasi("%s: %s sayı olmalı, gelen %r" % (yol, t, deger))
        if "min" in tanim and deger < tanim["min"]:
            raise YamaHatasi("%s: %r < min %r" % (yol, deger, tanim["min"]))
        if "max" in tanim and deger > tanim["max"]:
            raise YamaHatasi("%s: %r > max %r" % (yol, deger, tanim["max"]))
    elif t in ("select", "radio", "text_alignment"):
        secenek = tanim.get("o")
        if secenek is not None and deger not in secenek:
            raise YamaHatasi("%s: %r seçeneklerde yok %s" % (yol, deger, secenek))
    elif t in ("product_list", "collection_list", "metaobject_list"):
        if not isinstance(deger, list):
            raise YamaHatasi("%s: %s liste olmalı" % (yol, t))
    elif t in METIN_TIPLER:
        if not isinstance(deger, str):
            raise YamaHatasi("%s: %s metin olmalı, gelen %r" % (yol, t, deger))
        if deger.lstrip().startswith("{{"):   # dinamik kaynak ({{ closest.product... }}, palet referansı)
            return
        if t == "richtext" and deger and not RICHTEXT_KOK.match(deger):
            raise YamaHatasi("%s: richtext <p>, <ul>, <ol> ya da <h1-6> ile başlamalı" % yol)
        if t == "image_picker" and deger and not deger.startswith("shopify://shop_images/"):
            raise YamaHatasi("%s: görsel değeri shopify://shop_images/<dosya-adı> olmalı" % yol)
        if t == "color" and deger and not re.fullmatch(r"#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)", deger.strip()):
            raise YamaHatasi("%s: renk #rrggbb olmalı, gelen %r" % (yol, deger))


# ------------------------------------------------------------------ şablon (sections + order)
def dugum(t, parca):
    """'bolum/blok/alt' -> (düğüm, tur, tip, kök bölüm tipi)."""
    adim = parca.split("/")
    bolumler = t.get("sections") or {}
    if adim[0] not in bolumler:
        raise YamaHatasi("bölüm yok: %s (var olanlar: %s)" % (adim[0], ", ".join(bolumler)))
    d = bolumler[adim[0]]
    kok_tip = d.get("type")
    for i, a in enumerate(adim[1:], 1):
        bloklar = d.get("blocks") or {}
        if a not in bloklar:
            raise YamaHatasi("blok yok: %s (%s altında var olanlar: %s)" % (
                "/".join(adim[:i + 1]), "/".join(adim[:i]), ", ".join(bloklar) or "-"))
        d = bloklar[a]
    tur = "bolum" if len(adim) == 1 else "blok"
    return d, tur, d.get("type"), kok_tip


def ayarla_sablon(t, yol, deger, sozluk):
    if "." not in yol:
        raise YamaHatasi("yol biçimi '<bölüm>[/<blok>].<ayar>' olmalı: %s" % yol)
    parca, ayar = yol.rsplit(".", 1)
    d, tur, tip, kok_tip = dugum(t, parca)
    if ayar == "disabled":
        if not isinstance(deger, bool):
            raise YamaHatasi("%s: disabled true/false olmalı" % yol)
        eski = d.get("disabled", False)
        if deger:
            d["disabled"] = True
        else:
            d.pop("disabled", None)
        return eski
    tanimlar = ayar_tanimlari(sozluk, tur, tip, kok_tip)
    mevcut = d.get("settings") or {}
    if tanimlar is not None:
        if ayar not in tanimlar:
            yakin = [k for k in tanimlar if ayar.split("_")[0] in k][:8]
            raise YamaHatasi("ayar yok: %s ('%s' tipinin şemasında '%s' yok%s)" % (
                yol, tip, ayar, "; benzer: " + ", ".join(yakin) if yakin else ""))
        deger_kontrol(yol, tanimlar[ayar], deger)
    elif ayar not in mevcut:
        raise YamaHatasi("ayar yok: %s (şablonda yok ve '%s' tipinin şeması sözlükte yok)" % (yol, tip))
    eski = mevcut.get(ayar, "<yok>")
    d.setdefault("settings", {})[ayar] = deger
    return eski


def blok_ekle(t, islem, haric, sozluk):
    bolum = islem.get("bolum")
    if bolum not in haric:
        raise YamaHatasi("blok ekleme yalnız --haric ile verilen bölümde olur (%s)" % bolum)
    s = (t.get("sections") or {}).get(bolum)
    if s is None:
        raise YamaHatasi("bölüm yok: %s" % bolum)
    bid, btip = islem.get("id"), islem.get("type")
    if not bid or not btip:
        raise YamaHatasi("blok eklemede id ve type gerekli: %r" % islem)
    bloklar = s.setdefault("blocks", {})
    if bid in bloklar:
        raise YamaHatasi("blok zaten var: %s/%s" % (bolum, bid))
    var_olan_tipler = {b.get("type") for b in bloklar.values()}
    tanimlar = ayar_tanimlari(sozluk, "blok", btip, s.get("type"))
    if btip not in var_olan_tipler and tanimlar is None:
        raise YamaHatasi("blok tipi bu bölümde yok: %s (%s)" % (btip, ", ".join(sorted(var_olan_tipler))))
    ayarlar = islem.get("settings") or {}
    ornek = next((b.get("settings") or {} for b in bloklar.values() if b.get("type") == btip), {})
    for k, v in ayarlar.items():
        if tanimlar is not None:
            if k not in tanimlar:
                raise YamaHatasi("ayar yok: %s/%s.%s" % (bolum, bid, k))
            deger_kontrol("%s/%s.%s" % (bolum, bid, k), tanimlar[k], v)
        elif k not in ornek:
            raise YamaHatasi("ayar yok: %s/%s.%s (aynı tipteki bloklarda yok)" % (bolum, bid, k))
    bloklar[bid] = {"type": btip, "settings": ayarlar}
    sira = s.setdefault("block_order", [])
    sonra = islem.get("sonra")
    if sonra is not None:
        if sonra not in sira:
            raise YamaHatasi("'sonra' bloğu yok: %s/%s" % (bolum, sonra))
        sira.insert(sira.index(sonra) + 1, bid)
    else:
        sira.append(bid)


def harita(t, haric=()):
    def gez(b, yol):
        out = []
        for k, v in (b.get("blocks") or {}).items():
            out.append((yol + k, v.get("type"), tuple(v.get("block_order") or [])))
            out += gez(v, yol + k + "/")
        return out
    return {"order": list(t.get("order") or []),
            "bolumler": {k: (s.get("type"), tuple(s.get("block_order") or []), tuple(sorted(gez(s, ""))))
                         for k, s in (t.get("sections") or {}).items() if k not in haric},
            "haric_tip": {k: s.get("type") for k, s in (t.get("sections") or {}).items() if k in haric}}


def harita_kontrol(taban, yeni, haric):
    a, b = harita(taban, haric), harita(yeni, haric)
    if a["order"] != b["order"]:
        raise YamaHatasi("BÖLÜM SIRASI/SAYISI DEĞİŞTİ: %d -> %d bölüm" % (len(a["order"]), len(b["order"])))
    if set(a["bolumler"]) != set(b["bolumler"]) or a["haric_tip"] != b["haric_tip"]:
        eksik = sorted(set(a["bolumler"]) - set(b["bolumler"]))
        raise YamaHatasi("BÖLÜM KAYBI ya da EKİ: eksik %s, yeni %s" % (
            eksik, sorted(set(b["bolumler"]) - set(a["bolumler"]))))
    for k in a["bolumler"]:
        if a["bolumler"][k] != b["bolumler"][k]:
            ta, tb = a["bolumler"][k], b["bolumler"][k]
            neden = "tip %s -> %s" % (ta[0], tb[0]) if ta[0] != tb[0] else \
                "blok sayısı %d -> %d" % (len(ta[2]), len(tb[2])) if len(ta[2]) != len(tb[2]) else "blok sırası/tipi"
            raise YamaHatasi("BLOK KAYBI/DEĞİŞİMİ: %s (%s)" % (k, neden))
    # hariç bölüm: eski bloklar aynen durmalı (yalnız ekleme serbest)
    for k in haric:
        sa = (taban.get("sections") or {}).get(k)
        sb = (yeni.get("sections") or {}).get(k)
        if sa is None:
            continue
        ba, bb = sa.get("blocks") or {}, sb.get("blocks") or {}
        for bid, blok in ba.items():
            if bid not in bb or bb[bid].get("type") != blok.get("type"):
                raise YamaHatasi("BLOK KAYBI: %s/%s" % (k, bid))
        sira_b = [x for x in (sb.get("block_order") or []) if x in ba]
        if sira_b != list(sa.get("block_order") or []):
            raise YamaHatasi("BLOK SIRASI DEĞİŞTİ: %s" % k)


def deger_al(t, yol, ayarlar_modu):
    if ayarlar_modu:
        return etkin_preset(t).get(yol, "<yok>")
    parca, ayar = yol.rsplit(".", 1)
    d = dugum(t, parca)[0]
    return d.get("disabled", False) if ayar == "disabled" else (d.get("settings") or {}).get(ayar, "<yok>")


# ------------------------------------------------------------------ config/settings_data.json
def etkin_preset(t):
    cur = t.get("current")
    if isinstance(cur, dict):
        return cur
    p = (t.get("presets") or {}).get(cur)
    if p is None:
        raise YamaHatasi("settings_data: etkin preset '%s' yok" % cur)
    return p


def ayarla_genel(t, yol, deger, sozluk):
    if "." in yol or "/" in yol:
        raise YamaHatasi("settings_data yolu yalnız ayar adıdır: %s" % yol)
    p = etkin_preset(t)
    tanimlar = ayar_tanimlari(sozluk, "genel", None)
    if tanimlar is not None:
        if yol not in tanimlar:
            raise YamaHatasi("ayar yok: %s (settings_schema.json'da yok)" % yol)
        deger_kontrol(yol, tanimlar[yol], deger)
    elif yol not in p:
        raise YamaHatasi("ayar yok: %s (etkin preset'te yok, sözlük yok)" % yol)
    eski = p.get(yol, "<yok>")
    p[yol] = deger
    return eski


def ayarlar_kontrol(taban, yeni):
    if sorted(taban) != sorted(yeni):
        raise YamaHatasi("settings_data üst düzey anahtarları değişti")
    if taban.get("current") != yeni.get("current"):
        raise YamaHatasi("settings_data current değişti")
    pa, pb = taban.get("presets") or {}, yeni.get("presets") or {}
    if sorted(pa) != sorted(pb):
        raise YamaHatasi("settings_data preset adları değişti")
    for k in pa:
        if sorted((pa[k].get("sections") or {})) != sorted((pb[k].get("sections") or {})):
            raise YamaHatasi("settings_data %s bölüm anahtarları değişti" % k)


# ------------------------------------------------------------------ yama
def yama_oku(yol):
    with open(yol, encoding="utf-8") as f:
        veri = json.load(f)
    if isinstance(veri, list):
        veri = {"degisiklikler": veri}
    if not isinstance(veri, dict):
        raise YamaHatasi("yama JSON liste ya da nesne olmalı")
    deg = []
    for i, d in enumerate(veri.get("degisiklikler") or []):
        if isinstance(d, (list, tuple)) and len(d) == 2:
            deg.append((d[0], d[1]))
        elif isinstance(d, dict) and "yol" in d and "deger" in d:
            deg.append((d["yol"], d["deger"]))
        else:
            raise YamaHatasi("yama satırı %d geçersiz: %r (beklenen {\"yol\":..,\"deger\":..})" % (i + 1, d))
    goruldu = set()
    for y, _ in deg:
        if not isinstance(y, str) or not y:
            raise YamaHatasi("yol metin olmalı: %r" % (y,))
        if y in goruldu:
            raise YamaHatasi("aynı yol iki kez: %s" % y)
        goruldu.add(y)
    return deg, list(veri.get("haric") or []), list(veri.get("bloklar") or [])


def uygula(taban, degisiklikler, haric=(), bloklar=(), sozluk=None):
    """Yamayı uygular, bütün kontrolleri yapar. Döner: (yeni, rapor satırları). Hata: YamaHatasi."""
    ayarlar_modu = "presets" in taban and "sections" not in taban
    if not ayarlar_modu and not isinstance(taban.get("sections"), dict):
        raise YamaHatasi("şablon değil: 'sections' yok")
    if not degisiklikler and not bloklar:
        raise YamaHatasi("yama boş")
    yeni = copy.deepcopy(taban)
    rapor = []
    if ayarlar_modu and (haric or bloklar):
        raise YamaHatasi("settings_data için --haric ve blok ekleme kullanılmaz")
    for islem in bloklar:
        blok_ekle(yeni, islem, haric, sozluk)
        rapor.append("+ blok %s/%s (%s)" % (islem.get("bolum"), islem.get("id"), islem.get("type")))
    for yol, deger in degisiklikler:
        eski = ayarla_genel(yeni, yol, deger, sozluk) if ayarlar_modu else ayarla_sablon(yeni, yol, deger, sozluk)
        rapor.append("%s: %s -> %s" % (yol, kisalt(eski), kisalt(deger)))
    if ayarlar_modu:
        ayarlar_kontrol(taban, yeni)
    else:
        harita_kontrol(taban, yeni, haric)
    for yol, deger in degisiklikler:   # yazılan değer gerçekten yerinde mi
        if deger_al(yeni, yol, ayarlar_modu) != deger:
            raise YamaHatasi("değer yerine oturmadı: %s" % yol)
    return yeni, rapor


def kisalt(v, n=60):
    s = json.dumps(v, ensure_ascii=False) if not (isinstance(v, str) and v == "<yok>") else v
    return s if len(s) <= n else s[:n - 1] + "…"


def sikistir(t):
    return json.dumps(t, ensure_ascii=False, separators=(",", ":"))


def sayim(t):
    if "sections" not in t:
        return "settings_data"
    bloklar = 0

    def gez(b):
        nonlocal bloklar
        for v in (b.get("blocks") or {}).values():
            bloklar += 1
            gez(v)
    for s in t["sections"].values():
        gez(s)
    return "%d bölüm | %d blok" % (len(t.get("order") or t["sections"]), bloklar)


# ------------------------------------------------------------------ sözlük üretimi (yönetici)
SCHEMA_RE = re.compile(r"{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}", re.S)
ID_SIZ = ("header", "paragraph")


def tanim_sikistir(st):
    t = st.get("type")
    if t in ("select", "radio", "text_alignment") and st.get("options"):
        return {"t": t, "o": [o.get("value") for o in st["options"]]}
    if t in ("select", "radio", "text_alignment"):
        return {"t": t, "o": ["left", "center", "right"]} if t == "text_alignment" else t
    if t == "range":
        return {"t": t, "min": st.get("min"), "max": st.get("max")}
    if t == "number":
        d = {"t": t}
        for k in ("min", "max"):
            if k in st:
                d[k] = st[k]
        return d if len(d) > 1 else t
    return t


def ayar_listesi(settings):
    return {st["id"]: tanim_sikistir(st) for st in settings or [] if st.get("id") and st.get("type") not in ID_SIZ}


def sema_oku(dosya):
    with open(dosya, encoding="utf-8") as f:
        m = SCHEMA_RE.search(f.read())
    return json.loads(m.group(1)) if m else None


def sozluk_uret(tema_kok):
    tema = os.path.join(tema_kok, "theme") if os.path.isdir(os.path.join(tema_kok, "theme", "sections")) else tema_kok
    if not os.path.isdir(os.path.join(tema, "sections")):
        raise YamaHatasi("tema klasörü bulunamadı (sections/ yok): %s" % tema_kok)
    soz = {"aciklama": "Ana Tema bölüm/blok ayar adları ve tipleri; t4_yama.py ayar adı ve değer kontrolünde "
                       "kullanır. Elle düzenleme: tema değişince 't4_yama.py --sozluk-uret <tema>' ile yeniden üret.",
           "bolumler": {}, "bloklar": {}, "genel": {}}
    for f in sorted(glob.glob(os.path.join(tema, "sections", "*.liquid"))):
        j = sema_oku(f)
        if j is None:
            continue
        yerel = {b["type"]: ayar_listesi(b.get("settings")) for b in j.get("blocks") or []
                 if b.get("type") and not b["type"].startswith("@") and "settings" in b}
        kayit = {"a": ayar_listesi(j.get("settings"))}
        if yerel:
            kayit["b"] = yerel
        soz["bolumler"][os.path.basename(f)[:-len(".liquid")]] = kayit
    for f in sorted(glob.glob(os.path.join(tema, "blocks", "*.liquid"))):
        j = sema_oku(f)
        if j is not None:
            soz["bloklar"][os.path.basename(f)[:-len(".liquid")]] = ayar_listesi(j.get("settings"))
    ss = os.path.join(tema, "config", "settings_schema.json")
    if os.path.exists(ss):
        with open(ss, encoding="utf-8") as f:
            for grup in json.load(f):
                soz["genel"].update(ayar_listesi(grup.get("settings")))
    return soz


# ------------------------------------------------------------------ CLI
def yaz(yol, metin):
    with open(yol, "w", encoding="utf-8", newline="") as f:
        f.write(metin)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="T4.5 şablon yaması (yalnız verilen ayarlar).")
    ap.add_argument("--sablon", help="sunucudan okunan şablon (ham metin, baştaki yorum olabilir)")
    ap.add_argument("--yama", help="yama JSON dosyası")
    ap.add_argument("--cikti", help="yazılacak sıkıştırılmış JSON (yalnız bütün kontroller geçerse yazılır)")
    ap.add_argument("--haric", action="append", default=[], help="harita kontrolünden muaf bölüm (ör. faq); tekrar edilebilir")
    ap.add_argument("--sozluk", help="ayar-sozlugu.json yolu (varsayılan: betiğin yanında)")
    ap.add_argument("--kontrol", help="yazdıktan sonra sunucudan tekrar okunan dosya")
    ap.add_argument("--taban", help="--kontrol için yamadan önceki şablon")
    ap.add_argument("--sozluk-uret", metavar="TEMA_KOK", help="tema klasöründen ayar sözlüğü üret (--cikti ile)")
    ap.add_argument("--boyut", type=int, help="sunucunun bildirdiği dosya boyutu (bayt; files { size }): okunan metin eksikse durur")
    ap.add_argument("--bolum-sayisi", type=int, help="T4.0 haritasındaki bölüm sayısı: okunan şablon farklıysa durur")
    a = ap.parse_args(argv)

    try:
        if a.sozluk_uret:
            if not a.cikti:
                ap.error("--sozluk-uret için --cikti gerekli")
            soz = sozluk_uret(a.sozluk_uret)
            metin = json.dumps(soz, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
            yaz(a.cikti, metin)
            print("SÖZLÜK: %d bölüm, %d blok, %d genel ayar, %d bayt -> %s" % (
                len(soz["bolumler"]), len(soz["bloklar"]), len(soz["genel"]), len(metin.encode("utf-8")), a.cikti))
            return 0

        sozluk, sozluk_yolu = sozluk_yukle(a.sozluk)
        sozluk_notu = "sözlük: %s" % (os.path.basename(sozluk_yolu) if sozluk_yolu else
                                      "YOK (yalnız şablonda zaten bulunan ayarlar yazılabilir)")

        if a.kontrol:
            if not (a.taban and a.yama):
                ap.error("--kontrol için --taban ve --yama gerekli")
            taban = oku_dosya(a.taban)
            tekrar = oku_dosya(a.kontrol)
            deg, haric, bloklar = yama_oku(a.yama)
            haric = list(dict.fromkeys(haric + a.haric))
            beklenen, _ = uygula(taban, deg, haric, bloklar, sozluk)
            ayarlar_modu = "presets" in taban and "sections" not in taban
            if ayarlar_modu:
                ayarlar_kontrol(taban, tekrar)
            else:
                harita_kontrol(taban, tekrar, haric)
            for yol, deger in deg:
                if deger_al(tekrar, yol, ayarlar_modu) != deger:
                    raise YamaHatasi("sunucudaki değer farklı: %s" % yol)
            ayni = tekrar == beklenen
            print("KONTROL GEÇTİ | %s | %d değişiklik yerinde | beklenenle %s" % (
                sayim(tekrar), len(deg), "BİREBİR AYNI" if ayni else "harita+değer aynı, başka farklar var"))
            return 0

        if not (a.sablon and a.yama and a.cikti):
            ap.error("--sablon, --yama ve --cikti gerekli")
        if a.boyut is not None:
            okunan = os.path.getsize(a.sablon)
            if abs(okunan - a.boyut) > 2:   # sondaki satır sonu farkı tolere edilir; daha küçük kesik JSON'u zaten bozar
                raise YamaHatasi("okunan şablon %d bayt, sunucu %d bayt diyor: okuma eksik/bozuk, tekrar oku" % (
                    okunan, a.boyut))
        taban = oku_dosya(a.sablon)
        if a.bolum_sayisi is not None and "sections" in taban and len(taban.get("order") or []) != a.bolum_sayisi:
            raise YamaHatasi("şablonda %d bölüm var, T4.0 haritası %d diyor" % (
                len(taban.get("order") or []), a.bolum_sayisi))
        deg, haric, bloklar = yama_oku(a.yama)
        haric = list(dict.fromkeys(haric + a.haric))
        yeni, rapor = uygula(taban, deg, haric, bloklar, sozluk)
        cikti = sikistir(yeni)
        json.loads(cikti)   # geçerli JSON
        yaz(a.cikti, cikti)
        for r in rapor:
            print("  " + r)
        print("GEÇTİ | %d değişiklik | %s | %d karakter | sha256 %s | %s -> %s" % (
            len(deg) + len(bloklar), sayim(yeni), len(cikti),
            hashlib.sha256(cikti.encode("utf-8")).hexdigest()[:12], sozluk_notu, a.cikti))
        return 0
    except YamaHatasi as e:
        print("YAZMA: %s" % e)
        return 1
    except (OSError, json.JSONDecodeError) as e:
        print("YAZMA: dosya okunamadı/ayrıştırılamadı: %s" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
