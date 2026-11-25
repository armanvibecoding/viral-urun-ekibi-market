#!/usr/bin/env python3
"""Rol fikstürlerinin dosya/şema testi (ajan koşturmaz, kredi harcamaz).

Doğrular: her ajan dosyasının (agents/*.md) bir fikstür klasörü var; her modun en az
bir sabit girdisi ve bir "eksik girdi" vakası var; eksik girdi vakası `dur` bekler;
modlar ajan tanımındaki mod tablosuyla aynı; ortak sözleşme eksik girdide durmayı yazıyor.
Çıkış: 0 hepsi tamam · 1 hata.
"""
import json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]          # eklenti kökü
ROLLER = Path(__file__).resolve().parent
hatalar = []

def hata(m):
    hatalar.append(m)

ajanlar = sorted(p.stem for p in (KOK / "agents").glob("*.md"))
klasorler = sorted(p.name for p in ROLLER.iterdir() if p.is_dir())
if ajanlar != klasorler:
    hata(f"ajan/klasör farkı: yalnız ajanda {sorted(set(ajanlar)-set(klasorler))} · yalnız klasörde {sorted(set(klasorler)-set(ajanlar))}")

def ajan_modlari(rol):
    govde = (KOK / "agents" / f"{rol}.md").read_text(encoding="utf-8")
    modlar = re.findall(r"^\| (\w+) \| `[^`]*ortak/roller/", govde, flags=re.M)
    if modlar:
        return set(modlar)
    if re.search(r"`mod:`|mod: gorsel|`gorsel`", govde) and rol == "copy":
        return {"gorsel", "site"}
    return {None}

for rol in klasorler:
    f = ROLLER / rol / "vaka.json"
    if not f.exists():
        hata(f"{rol}: vaka.json yok"); continue
    ham = f.read_text(encoding="utf-8")
    if re.search("/" + "Users/|/" + "home/", ham):
        hata(f"{rol}: mutlak ev yolu")
    try:
        d = json.loads(ham)
    except Exception as e:
        hata(f"{rol}: JSON bozuk ({e})"); continue
    if d.get("rol") != rol:
        hata(f"{rol}: rol alanı yanlış")
    if not {"vaka", "urun", "pazar"} <= set(d.get("sabit_urun", {})):
        hata(f"{rol}: sabit_urun eksik")
    moduller = d.get("moduller") or []
    if not moduller:
        hata(f"{rol}: sabit girdi yok")
    for m in moduller:
        b = m.get("beklenen", {})
        if not m.get("brief") or not b.get("cikti_dosyasi") or not b.get("zorunlu_bolumler"):
            hata(f"{rol}/{m.get('mod')}: brief/çıktı/zorunlu bölüm eksik")
    eksikler = d.get("eksik_girdi") or []
    for e in eksikler:
        if e.get("beklenen") != "dur" or "dur" not in (e.get("ilk_satir_icerir") or []):
            hata(f"{rol}/{e.get('mod')}: eksik girdi vakası `dur` beklemiyor")
        if not e.get("yasak"):
            hata(f"{rol}/{e.get('mod')}: yasak (uydurma) listesi boş")
    kume = lambda l: {x.get("mod") for x in l}
    if kume(moduller) != kume(eksikler):
        hata(f"{rol}: sabit girdi modları {kume(moduller)} ≠ eksik girdi modları {kume(eksikler)}")
    beklenen = ajan_modlari(rol)
    if kume(moduller) != beklenen:
        hata(f"{rol}: fikstür modları {kume(moduller)} ≠ ajan tanımı {beklenen}")

sozlesme = (KOK / "ortak" / "sozlesme-rol.md").read_text(encoding="utf-8")
if "Girdi eksikse dur" not in sozlesme:
    hata("ortak/sozlesme-rol.md: 'Girdi eksikse dur' kuralı yok")

if hatalar:
    print("KALDI")
    for h in hatalar:
        print(" -", h)
    sys.exit(1)
vaka = sum(len(json.loads((ROLLER / r / 'vaka.json').read_text(encoding='utf-8'))['moduller']) for r in klasorler)
print(f"GEÇTİ: {len(klasorler)} rol · {vaka} sabit girdi · {vaka} eksik girdi vakası")
