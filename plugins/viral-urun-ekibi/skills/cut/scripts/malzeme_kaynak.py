#!/usr/bin/env python3
"""Malzeme kaynağı ve lisans kaydı (KAYNAK.tsv): klip ↔ kaynak eşleşmesi ve lisans durumu. Kapılar bu modülü kullanır
(kurgu_kontrol `malzeme` kuralı · kapi.py yayin `lisans@V`). Kayıt kurucunun/lider­in elindedir; karar kurucuda, kayıt kapıdadır.

KAYNAK.tsv (sekmeyle ayrılmış, ilk satır başlık; `#` ile başlayan satır yok sayılır). Sütunlar:
  vaka · dosya · kaynak · cekim · kullanilacak_aralik · not          (eski sütunlar; `dosya` eşleşme anahtarıdır)
  lisans    kurucu (kurucunun kendi çekimi) | uretim (bizim ürettiğimiz: Flow/ChatGPT) | stok (lisanslı stok, LISANS.md) |
            yazili (satıcı/tedarikçi yazılı ticari izin) | boş/yok/sinav-ici = lisanssız
  kullanim  sinav | yayin   (yalnız `yayin` olan malzeme yayına girer)
  yapay_mi  evet | hayir    (tedarikçi videosu yapay zekâ üretimi mi; `evet` + lisans ≠ uretim = gerçek ürün görüntüsü değil)
  bakildi   YYYY-AA-GG      (kaynağın var olduğuna ve lisans metnine en son bakılan gün)
Boş sütun = KALDI (yayın kapısında). Eski dosyada bu sütunlar hiç yoksa hepsi boş sayılır.
"""
import csv
import os
import re

URUN_TURLERI = ("urun", "urun_elde", "telefon", "sokum")   # ürünün kendisini gösteren klip türleri (klip_etiket.json `tur`)
LISANS_TAMAM = ("kurucu", "uretim", "stok", "yazili")


def bul(baslangic, acik=None):
    """KAYNAK.tsv yolu: açıkça verilen, yoksa başlangıç klasöründen yukarı (en çok 6 üst) KAYNAK.tsv · tedarikci/ · malzeme/. Yoksa None."""
    if acik:
        return acik if os.path.isfile(acik) else None
    d = os.path.abspath(baslangic if os.path.isdir(baslangic) else os.path.dirname(baslangic))
    for _ in range(7):
        for alt in ("", "tedarikci", "malzeme"):
            y = os.path.join(d, alt, "KAYNAK.tsv")
            if os.path.isfile(y):
                return y
        ust = os.path.dirname(d)
        if ust == d:
            break
        d = ust
    return None


def oku(yol):
    with open(yol, encoding="utf-8-sig", newline="") as f:
        satirlar = [s for s in f if s.strip() and not s.lstrip().startswith("#")]
    return [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(satirlar, delimiter="\t")]


def esle(satirlar, metin, vaka=None):
    """Etiketin kaynak metnini (ör. "tedarikçi ilan videosu ae-3256812808567181.mp4 17.6s") KAYNAK.tsv satırlarına bağlar.
    Satır `dosya` adı (uzantılı ya da uzantısız) metinde geçiyorsa eşleşir. `vaka` KAYNAK.tsv'deki bir vaka adıysa yalnız o vakanın
    satırları sayılır (başka vakanın klibi = yanlış ürün)."""
    m = (metin or "").lower()
    vakalar = {s.get("vaka", "") for s in satirlar}
    havuz = [s for s in satirlar if not (vaka and vaka in vakalar) or s.get("vaka") == vaka]
    out = []
    for s in havuz:
        d = s.get("dosya", "").lower()
        if d and (d in m or os.path.splitext(d)[0] in m):
            out.append(s)
    return out


def kullanilabilir(satir):
    return not re.match(r"\s*kullanma", satir.get("kullanilacak_aralik", ""), re.I)


def lisans_sorunu(satir):
    """Yayın için lisans eksiği (boş liste = tamam)."""
    s = []
    if satir.get("lisans", "").lower() not in LISANS_TAMAM:
        s.append("lisans %s (kurucu|uretim|stok|yazili olmalı)" % (satir.get("lisans") or "boş"))
    if satir.get("kullanim", "").lower() != "yayin":
        s.append("kullanim %s (yayin olmalı)" % (satir.get("kullanim") or "boş"))
    if satir.get("yapay_mi", "").lower() not in ("evet", "hayir", "hayır"):
        s.append("yapay_mi boş")
    if not satir.get("bakildi"):
        s.append("bakildi boş")
    return s


def klip_kaynaklari(ayar, etiketler, klasor_vaka=None, satirlar=None):
    """[(klip adı, tür, kaynak metni, [eşleşen satırlar])] — yalnız ürün türündeki klipler. ayar: hizli_kurgu ayarı (dict)."""
    out, gorulen = [], set()
    for p in ayar.get("planlar", []):
        if not isinstance(p, dict):
            continue
        ad = os.path.splitext(os.path.basename(p["klip"]))[0]
        if ad in gorulen:
            continue
        gorulen.add(ad)
        e = etiketler.get(ad) or {}
        if e.get("tur") in URUN_TURLERI:
            metin = e.get("malzeme") or e.get("kaynak") or ""
            out.append((ad, e["tur"], metin, esle(satirlar or [], metin, klasor_vaka)))
    return out
