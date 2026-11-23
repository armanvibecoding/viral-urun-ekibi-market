#!/usr/bin/env python3
"""Ön-üretim kartı kapısı: video üretimine (hikâye kurucu, kutulu kurgu) başlamadan kart dosyası geçerli olmalı.

  python3 on_uretim_karti.py sablon [--pazar US]      → örnek kart JSON'u basar
  python3 on_uretim_karti.py kontrol KART.json        → çıkış 0 geçerli · 1 HATA (neden satır satır)

Kart (JSON) bilgiyi KOPYALAMAZ, kütüphaneye işaret eder; betik işareti kütüphanede doğrular:
  pazar            US | UK | DE | FR | ES | TR   (pazar-kartlari/<P>.md var olmalı)
  kanca_ailesi     K1…K15 (kanca-kutuphanesi.md'de "### K<n>." başlığı olmalı; yazısız = K13)
  kanca_metni      ekrana yazılacak kanca (TR: ≤ 8 kelime)
  kanit            kütüphanede geçen kanıt numaraları ["[037]", "[S24-G1x04]"] (en az 1; her biri kanca-kutuphanesi.md'de bulunmalı)
  sahne_sablonu    S1…S10 (sahne-sablonlari.md'de "## S<n> " başlığı olmalı)
  format           dongu (7–10 sn, başa saran) | hikaye (25 sn)
  tatmin_ani       dongu için zorunlu: tek tatmin/kanıt anının tarifi
  muzik            {"karar": "...", "dayanak": "kural-rampa|muzik-kutuphanesi|kullanici-dosyasi"}; müzik verisi ölçülmedi, rampa kuralı geçerli (SES-01)
  ilk_1sn          ilk 1 saniyede ekranda ne görünecek
  esik             AB/UK pazarında "abd-yarisi" (paylaşım beklentisi ABD'nin yarısı; ABD eşiğiyle öldürme yok)
  tr_veri_zayif    TR pazarında true ("TR verisi zayıf, ilk testten sonra kalibre")
"""
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # eklenti kökü
REF = os.path.join(KOK, "skills", "studio", "referans")
PAZARLAR = ("US", "UK", "DE", "FR", "ES", "TR")
AB = ("UK", "DE", "FR", "ES")
DAYANAK = ("kural-rampa", "muzik-kutuphanesi", "kullanici-dosyasi")


def oku(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def dogrula(kart, ref=REF):
    h = []
    pz = kart.get("pazar")
    if pz not in PAZARLAR:
        h.append("pazar %r; izinli: %s" % (pz, ", ".join(PAZARLAR)))
    elif not os.path.isfile(os.path.join(ref, "pazar-kartlari", pz + ".md")):
        h.append("pazar kartı dosyası yok: pazar-kartlari/%s.md" % pz)
    kut = oku(os.path.join(ref, "kanca-kutuphanesi.md"))
    fam = str(kart.get("kanca_ailesi", ""))
    if not re.fullmatch(r"K\d{1,2}", fam) or not re.search(r"^### %s\. " % re.escape(fam), kut, re.M):
        h.append("kanca_ailesi %r kanca-kutuphanesi.md'de başlık olarak yok (K1…K15; yazısız = K13)" % fam)
    metin = str(kart.get("kanca_metni", "")).strip()
    if not metin and fam != "K13":
        h.append("kanca_metni boş (yalnız yazısız K13'te boş olabilir; o zaman ilk_1sn görüntüyü tarif eder)")
    if pz == "TR" and len(metin.split()) > 8:
        h.append("TR kancası %d kelime (≤ 8)" % len(metin.split()))
    kanit = kart.get("kanit")
    if not isinstance(kanit, list) or not kanit:
        h.append("kanit boş: kütüphaneden en az 1 kanıt numarası (ör. \"[037]\", \"[S24-G1x04]\")")
    else:
        for k in kanit:
            if not str(k).strip("[] ") or str(k) not in kut:
                h.append("kanıt %r kanca-kutuphanesi.md'de geçmiyor (uydurma kanıt numarası olmaz)" % k)
    sab = str(kart.get("sahne_sablonu", ""))
    if not re.fullmatch(r"S\d{1,2}", sab) or not re.search(r"^## %s\b" % re.escape(sab), oku(os.path.join(ref, "sahne-sablonlari.md")), re.M):
        h.append("sahne_sablonu %r sahne-sablonlari.md'de yok (S1…S10)" % sab)
    fmt = kart.get("format")
    if fmt not in ("dongu", "hikaye"):
        h.append("format %r; izinli: dongu | hikaye" % fmt)
    if fmt == "dongu" and not str(kart.get("tatmin_ani", "")).strip():
        h.append("dongu formatında tatmin_ani zorunlu (tek tatmin/kanıt anı)")
    m = kart.get("muzik") or {}
    if not str(m.get("karar", "")).strip() or m.get("dayanak") not in DAYANAK:
        h.append("muzik.karar dolu ve muzik.dayanak %s olmalı (müzik verisi ölçülmedi; kural = rampa + tarif)" % "|".join(DAYANAK))
    if not str(kart.get("ilk_1sn", "")).strip():
        h.append("ilk_1sn boş: ilk saniyede ne görünecek yazılmalı")
    if pz in AB and kart.get("esik") != "abd-yarisi":
        h.append("AB/UK pazarında esik = \"abd-yarisi\" yazılmalı (paylaşım beklentisi ABD'nin yarısı; ABD eşiğiyle öldürme yok)")
    if pz == "TR" and kart.get("tr_veri_zayif") is not True:
        h.append("TR pazarında tr_veri_zayif = true yazılmalı (TR verisi zayıf, ilk testten sonra kalibre)")
    return h


def kart_kapisi(yol):
    """Diğer betikler için: (tamam, [hatalar]). Dosya yok/bozuk = kapı KAPALI."""
    if not yol or not os.path.isfile(yol):
        return False, ["ön-üretim kartı yok: %s (üretimden önce `on_uretim_karti.py sablon` ile yaz)" % yol]
    try:
        kart = json.loads(oku(yol))
    except ValueError as e:
        return False, ["ön-üretim kartı JSON değil: %s" % e]
    h = dogrula(kart)
    return (not h), h


def sablon(pazar):
    return {"pazar": pazar, "kanca_ailesi": "K1", "kanca_metni": "DO NOT show this to a DOG MOM", "kanit": ["[037]"],
            "sahne_sablonu": "S1", "format": "dongu", "tatmin_ani": "tek hamlede temizlenen yüzey",
            "muzik": {"karar": "açık lisanslı parça, 1,5–2 sn rampa", "dayanak": "kural-rampa"},
            "ilk_1sn": "ürün elde, sonuç ilk karede", **({"esik": "abd-yarisi"} if pazar in AB else {}), **({"tr_veri_zayif": True} if pazar == "TR" else {})}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "sablon":
        pz = sys.argv[sys.argv.index("--pazar") + 1] if "--pazar" in sys.argv else "US"
        print(json.dumps(sablon(pz), ensure_ascii=False, indent=2))
        return 0
    if sys.argv[1] == "kontrol" and len(sys.argv) > 2:
        ok, h = kart_kapisi(sys.argv[2])
        for x in h:
            print("HATA:", x)
        print("ön-üretim kartı: %s" % ("GEÇTİ" if ok else "KALDI"))
        return 0 if ok else 1
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
