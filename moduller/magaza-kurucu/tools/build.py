# -*- coding: utf-8 -*-
"""Mağaza Kurucu paketleyici.

Tek kaynak: skills/ (her skill'in kendi dosyaları) + src/ortak/ (birden çok skill'in
paylaştığı references) + config/tema.json.

  python tools/build.py           # ortak kopyaları eşitle, kontrol et, dist/ zip'lerini üret
  python tools/build.py --check   # hiçbir şey yazmadan doğrula (kopyalar kaynakla aynı mı,
                                  # SKILL.md boyut/frontmatter, references linkleri, manifest sürümleri,
                                  # tek paket yapısı bellekte kurularak)

Derleme hedefleri (hepsi TEK paket düzeni: src/tek/SKILL.md sıralayıcısı + 5 aşama klasörü; aşama SKILL.md'leri
<aşama>/ASAMA.md olarak, frontmatter'sız girer: iç içe SKILL.md tek skill'de yanlış tetiklenebilir):
  1) BİRLEŞİK beceri klasörü (Viral Ürün Ekibi eklentisinin içinde; depoya girer, elle düzenlenmez):
       ../../plugins/viral-urun-ekibi/skills/builder/
     --check bu klasörün kaynakla bayt bayt aynı olduğunu da doğrular (eksik, farklı, fazla dosya = hata).
  2) Tek başına zip'ler (depoya girmez):
       dist/chatgpt/builder.zip      (agents/openai.yaml dahil)
       dist/claude/magaza-kurucu-tek.zip   (agents/ hariç)
Ayrı 5 skill zip'i ve ayrı plugin zip'i ÜRETİLMEZ: ekibin tek girişi vardır (captain).

Çıkış kodu: 0 = geçti, 1 = hata.
"""
import argparse
import io
import json
import os
import re
import stat
import sys
import zipfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLER = ["urun-analiz", "marka", "gorseller", "metinler", "shopify-kurulum"]  # akış sırası
TUM = SKILLER
SKILL_MAX_BAYT = 5120          # SKILL.md ≤ 5 KB
DESC_MAX = 1024                # frontmatter description
REF_UYARI_BAYT = 10 * 1024     # reference ~10 KB üstü: uyarı (hata değil)

# kaynak (repo köküne göre) -> hangi skill'lerin references/ klasörüne kopyalanır
KOPYALAR = {
    "src/ortak/00-calisma-tarzi.md": TUM,
    "src/ortak/01-kurallar.md": TUM,
    "src/ortak/tema-haritasi-t4.md": ["metinler", "shopify-kurulum"],
    "src/ortak/yasal-sayfalar-t7-t8.md": ["metinler", "shopify-kurulum"],
    "src/ortak/gorsel-dosya-adlari-t3.md": ["gorseller", "shopify-kurulum"],
    "src/ortak/tasarim-dili.md": ["gorseller", "marka"],
    "src/ortak/arayuz-sozlesmesi.md": ["urun-analiz", "shopify-kurulum"],
    "src/ortak/site-denetimi.md": ["shopify-kurulum", "metinler"],
    "src/ortak/ekip-koprusu.md": ["urun-analiz", "metinler", "shopify-kurulum"],
    "config/tema.json": ["shopify-kurulum"],
}
MANIFESTLER = ["surum.json"]       # modül sürümü; eklenti manifesti plugins/viral-urun-ekibi/.claude-plugin/plugin.json
JSONLAR = MANIFESTLER + ["config/tema.json"]
BIRLESIK = os.path.normpath(os.path.join(KOK, "..", "..", "plugins", "viral-urun-ekibi", "skills", "builder"))
YASAK_UZANTI = (".webp", ".jpg", ".jpeg", ".png", ".gif", ".zip")   # başka mağaza görseli pakete girmez
# İstisna: kullanıcının onayladığı kendi üretimimiz stil çapası kareleri (G3). Yalnız bu klasör, yalnız jpg/png.
GORSEL_IZINLI_KLASOR = "skills/gorseller/assets/stil-capasi/"
GORSEL_IZINLI_UZANTI = (".jpg", ".jpeg", ".png")
GORSEL_MAX_BAYT = 250 * 1024
ATLA = ("__pycache__", ".pyc", ".DS_Store")
ZIP_TARIH = (2026, 1, 1, 0, 0, 0)   # tekrarlanabilir zip

# Tek paket
TEK_KOK = "builder"            # zip kök klasörü = router name
TEK_ASAMA_DOSYA = "ASAMA.md"         # aşama SKILL.md'lerinin paket içi adı
TEK_ZIPLER = {"chatgpt": "dist/chatgpt/builder.zip", "claude": "dist/claude/magaza-kurucu-tek.zip"}
TEK_MAX_BAYT = 25 * 1024 * 1024      # Skills Upload sınırı ölçülmedi; güvenli tavan
METIN_UZANTI = (".md", ".py", ".json", ".yaml", ".yml", ".txt")


def yol(*p):
    return os.path.join(KOK, *p)


def oku_bayt(p):
    with open(p, "rb") as f:
        return f.read()


def hedefler():
    for kaynak, skiller in KOPYALAR.items():
        for s in skiller:
            yield kaynak, "skills/%s/references/%s" % (s, os.path.basename(kaynak))


# ------------------------------------------------------------------ kopyalar
def esitle():
    n = 0
    for kaynak, hedef in hedefler():
        b = oku_bayt(yol(kaynak))
        h = yol(hedef)
        if not os.path.exists(h) or oku_bayt(h) != b:
            os.makedirs(os.path.dirname(h), exist_ok=True)
            with open(h, "wb") as f:
                f.write(b)
            n += 1
    return n


def kontrol_kopyalar(hatalar):
    for kaynak, hedef in hedefler():
        if not os.path.exists(yol(hedef)):
            hatalar.append("KOPYA YOK: %s (kaynak %s)" % (hedef, kaynak))
        elif oku_bayt(yol(hedef)) != oku_bayt(yol(kaynak)):
            hatalar.append("KOPYA FARKLI: %s != %s" % (hedef, kaynak))


# ------------------------------------------------------------------ skill kuralları
def frontmatter(metin):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", metin, re.S)
    if not m:
        return None
    # Gerçek YAML ayrıştırıcısı: ChatGPT/agent skills doğrulaması YAML'a göre yapar.
    # (2026-11-17: tırnaksız description içindeki ": " 4 skill'i bozuyordu; basit ayrıştırıcı yakalamadı.)
    import yaml
    try:
        alan = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return {"__yaml_hata__": str(e).splitlines()[0]}
    return {k: ("" if v is None else str(v)) for k, v in (alan or {}).items()}


def izinli_gorsel(rel):
    """rel: repo köküne göre '/' ayraçlı yol (ya da zip içi 'skills/...' / '<skill>/...' adı)."""
    rel = rel.replace("\\", "/")
    kisa = GORSEL_IZINLI_KLASOR[len("skills/"):]          # gorseller/assets/stil-capasi/
    return ((rel.startswith(GORSEL_IZINLI_KLASOR) or rel.startswith(kisa))
            and rel.lower().endswith(GORSEL_IZINLI_UZANTI))


def kontrol_stil_capasi(hatalar):
    d = yol(*GORSEL_IZINLI_KLASOR.strip("/").split("/"))
    if not os.path.isdir(d):
        hatalar.append("stil çapası klasörü yok: %s" % GORSEL_IZINLI_KLASOR)
        return 0
    anilan = ""
    refs = [os.path.join(k, x) for k, _, fs in os.walk(yol("skills", "gorseller", "references")) for x in sorted(fs)]
    for f in [yol("skills", "gorseller", "SKILL.md")] + refs:
        anilan += open(f, encoding="utf-8").read()
    n = 0
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if not f.lower().endswith(GORSEL_IZINLI_UZANTI):
            hatalar.append("stil çapası: izinsiz dosya %s" % f)
            continue
        n += 1
        if os.path.getsize(p) > GORSEL_MAX_BAYT:
            hatalar.append("stil çapası: %s %d bayt > %d" % (f, os.path.getsize(p), GORSEL_MAX_BAYT))
        if f not in anilan:
            hatalar.append("stil çapası: %s gorseller references'ta anılmıyor (model kullanmaz)" % f)
    if n == 0:
        hatalar.append("stil çapası klasörü boş")
    return n


def kontrol_skill(ad, hatalar, uyarilar, tablo):
    d = yol("skills", ad)
    p = os.path.join(d, "SKILL.md")
    if not os.path.exists(p):
        hatalar.append("%s: SKILL.md yok" % ad)
        return
    bayt = os.path.getsize(p)
    metin = open(p, encoding="utf-8").read()
    fm = frontmatter(metin)
    durum = []
    if bayt > SKILL_MAX_BAYT:
        hatalar.append("%s: SKILL.md %d bayt > %d" % (ad, bayt, SKILL_MAX_BAYT))
        durum.append("BOYUT")
    if fm is None:
        hatalar.append("%s: frontmatter yok" % ad)
        durum.append("FM")
    elif "__yaml_hata__" in fm:
        hatalar.append("%s: frontmatter geçerli YAML değil: %s" % (ad, fm["__yaml_hata__"]))
        durum.append("YAML")
    else:
        if fm.get("name") != ad:
            hatalar.append("%s: name '%s' klasör adıyla aynı değil" % (ad, fm.get("name")))
            durum.append("NAME")
        if not re.fullmatch(r"[a-z0-9-]{1,64}", fm.get("name", "")):
            hatalar.append("%s: name biçimi geçersiz" % ad)
        desc = fm.get("description", "")
        if not desc:
            hatalar.append("%s: description yok" % ad)
            durum.append("DESC")
        elif len(desc) > DESC_MAX:
            hatalar.append("%s: description %d karakter > %d" % (ad, len(desc), DESC_MAX))
            durum.append("DESC")
        ekstra = set(fm) - {"name", "description"}
        if ekstra:
            uyarilar.append("%s: frontmatter'da ek alan %s" % (ad, sorted(ekstra)))
    # references: SKILL.md'de anılan her dosya var mı, var olan her dosya anılıyor mu
    rdir = os.path.join(d, "references")
    mevcut = sorted(os.listdir(rdir)) if os.path.isdir(rdir) else []
    anilan = set(re.findall(r"references/([A-Za-z0-9_.\-]+)", metin))
    for f in sorted(anilan - set(mevcut)):
        hatalar.append("%s: SKILL.md'de anılan references/%s yok" % (ad, f))
    for f in mevcut:
        if f not in anilan and f not in metin:
            hatalar.append("%s: references/%s SKILL.md'de anılmıyor (model okumaz)" % (ad, f))
        b = os.path.getsize(os.path.join(rdir, f))
        if b > REF_UYARI_BAYT:
            uyarilar.append("%s: references/%s %d bayt (~10 KB üstü)" % (ad, f, b))
    # pakete girmemesi gerekenler
    for kok, _, dosyalar in os.walk(d):
        for f in dosyalar:
            rel = os.path.relpath(os.path.join(kok, f), KOK).replace("\\", "/")
            if f.lower().endswith(YASAK_UZANTI) and not izinli_gorsel(rel):
                hatalar.append("%s: görsel/arsiv dosyası pakette: %s" % (ad, os.path.relpath(os.path.join(kok, f), KOK)))
    if not os.path.exists(os.path.join(d, "agents", "openai.yaml")):
        hatalar.append("%s: agents/openai.yaml yok" % ad)
    tablo.append((ad, bayt, len(fm.get("description", "")) if fm else 0, len(mevcut), "OK" if not durum else ",".join(durum)))


def kontrol_manifest(hatalar):
    surumler = {}
    for j in JSONLAR:
        try:
            veri = json.load(open(yol(j), encoding="utf-8"))
        except Exception as e:   # noqa: BLE001
            hatalar.append("JSON okunamadı: %s (%s)" % (j, e))
            continue
        if j in MANIFESTLER:
            surumler[j] = veri.get("version")
            if veri.get("name") != "builder":
                hatalar.append("%s: name builder değil" % j)
        if j == ".claude-plugin/marketplace.json":
            for p in veri.get("plugins", []):
                surumler[j + " → " + p.get("name", "?")] = p.get("version")
    if len(set(surumler.values())) != 1:
        hatalar.append("Sürümler farklı: %s" % surumler)
    return next(iter(surumler.values()), None)


# ------------------------------------------------------------------ zip
def dosyalar(kok, haric_klasor=()):
    for k, klasorler, fs in os.walk(kok):
        klasorler[:] = sorted(x for x in klasorler if x not in ATLA and x not in haric_klasor)
        for f in sorted(fs):
            if f.endswith(ATLA) or f in ATLA:
                continue
            yield os.path.join(k, f)


def _zip_bilgi(ad, klasor=False):
    """Unix (create_system=3) girdisi: dosya 0644, klasör 0755."""
    zi = zipfile.ZipInfo(ad, ZIP_TARIH)
    zi.create_system = 3
    if klasor:
        zi.external_attr = ((stat.S_IFDIR | 0o755) << 16) | 0x10
        zi.compress_type = zipfile.ZIP_STORED
    else:
        zi.external_attr = (stat.S_IFREG | 0o644) << 16
        zi.compress_type = zipfile.ZIP_DEFLATED
    return zi


def zip_bayt(girdiler):
    """girdiler: [(disk_yolu ya da bayt, arsiv_adi)] -> zip baytları (üst klasör girdileri eklenir)."""
    tampon = io.BytesIO()
    yazilan_klasor = set()
    with zipfile.ZipFile(tampon, "w", zipfile.ZIP_DEFLATED) as z:
        for kaynak, ad in girdiler:
            ad = ad.replace("\\", "/")
            parcalar = ad.split("/")[:-1]
            for i in range(1, len(parcalar) + 1):
                k = "/".join(parcalar[:i]) + "/"
                if k not in yazilan_klasor:
                    yazilan_klasor.add(k)
                    z.writestr(_zip_bilgi(k, klasor=True), b"")
            veri = kaynak if isinstance(kaynak, bytes) else oku_bayt(kaynak)
            z.writestr(_zip_bilgi(ad), veri)
    return tampon.getvalue()


def zip_yaz(hedef, girdiler):
    """girdiler: [(disk_yolu ya da bayt, arsiv_adi)]"""
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    with open(hedef, "wb") as f:
        f.write(zip_bayt(girdiler))
    return hedef


def skill_girdileri(ad, haric_klasor=()):
    d = yol("skills", ad)
    return [(p, ad + "/" + os.path.relpath(p, d).replace("\\", "/")) for p in dosyalar(d, haric_klasor)]


def plugin_girdileri(kok_dosyalar, haric_klasor=()):
    g = [(yol(f), f) for f in kok_dosyalar]
    for ad in SKILLER:
        g += [(p, "skills/" + a) for p, a in skill_girdileri(ad, haric_klasor)]
    return g


def frontmatter_sil(b):
    m = re.match(rb"^---\r?\n.*?\r?\n---\r?\n+", b, re.S)
    return b[m.end():] if m else b


def tek_girdileri(chatgpt):
    """Tek paket: builder/SKILL.md (router) + [agents/openai.yaml] + <aşama>/ASAMA.md + references/scripts/assets."""
    k = TEK_KOK + "/"
    g = [(yol("src", "tek", "SKILL.md"), k + "SKILL.md")]
    if chatgpt:
        g.append((yol("src", "tek", "agents", "openai.yaml"), k + "agents/openai.yaml"))
    for ad in SKILLER:
        for p, a in skill_girdileri(ad, ("agents",)):
            if a == ad + "/SKILL.md":
                g.append((frontmatter_sil(oku_bayt(p)), k + ad + "/" + TEK_ASAMA_DOSYA))
            else:
                g.append((p, k + a))
    return g


def router_yollari(metin):
    """Router'da `...` içinde anılan paket içi yollar (aşama klasörüyle başlayan; yer tutucular hariç)."""
    out = []
    for t in re.findall(r"`([^`\s]+)`", metin):
        if any(c in t for c in "<>*…"):
            continue
        if "/" in t and t.split("/")[0] in SKILLER + ["agents"]:
            out.append(t)
    return out


def kontrol_tek(bayt, chatgpt, hatalar, etiket="tek"):
    """Tek paket zip'ini doğrular. Döner: (dosya sayısı, açık toplam bayt, router SKILL.md bayt)."""
    k = TEK_KOK + "/"
    try:
        z = zipfile.ZipFile(io.BytesIO(bayt))
    except zipfile.BadZipFile as e:
        hatalar.append("%s: zip okunamadı (%s)" % (etiket, e))
        return 0, 0, 0
    router_bayt = 0
    with z:
        bilgiler = z.infolist()
        adlar = [i.filename for i in bilgiler]
        dosya_adlari = [n for n in adlar if not n.endswith("/")]
        kume = set(adlar)
        acik = sum(i.file_size for i in bilgiler)
        if not all(n.startswith(k) for n in adlar):
            hatalar.append("%s: girdiler '%s' ile başlamıyor" % (etiket, k))
        for i in bilgiler:
            izin = (i.external_attr >> 16) & 0o777
            if i.create_system != 3 or izin != (0o755 if i.is_dir() else 0o644):
                hatalar.append("%s: %s create_system=%d izin=%o (3 / 644, klasör 755 olmalı)"
                               % (etiket, i.filename, i.create_system, izin))
                break
        skill_md = [n for n in dosya_adlari if n.rsplit("/", 1)[-1] == "SKILL.md"]
        if skill_md != [k + "SKILL.md"]:
            hatalar.append("%s: yalnız kökte tek SKILL.md olmalı, bulunan: %s" % (etiket, skill_md))
        if k + "SKILL.md" in kume:
            router_b = z.read(k + "SKILL.md")
            router_bayt = len(router_b)
            router = router_b.decode("utf-8")
            if router_bayt > SKILL_MAX_BAYT:
                hatalar.append("%s: router SKILL.md %d bayt > %d" % (etiket, router_bayt, SKILL_MAX_BAYT))
            fm = frontmatter(router)
            if fm is None or "__yaml_hata__" in fm:
                hatalar.append("%s: router frontmatter geçersiz: %s"
                               % (etiket, (fm or {}).get("__yaml_hata__", "yok")))
            else:
                if fm.get("name") != TEK_KOK:
                    hatalar.append("%s: router name '%s' != %s" % (etiket, fm.get("name"), TEK_KOK))
                d = fm.get("description", "")
                if not d or len(d) > DESC_MAX:
                    hatalar.append("%s: router description boş ya da > %d karakter" % (etiket, DESC_MAX))
            yollar = router_yollari(router)
            for ad in SKILLER:
                if "%s/%s" % (ad, TEK_ASAMA_DOSYA) not in yollar:
                    hatalar.append("%s: router %s/%s'yi anmıyor" % (etiket, ad, TEK_ASAMA_DOSYA))
            for t in yollar:
                t2 = t.rstrip("/")
                if k + t2 not in kume and not any(n.startswith(k + t2 + "/") for n in adlar):
                    hatalar.append("%s: router'da anılan yol pakette yok: %s" % (etiket, t))
        # aşama dosyaları: frontmatter yok; andıkları references/scripts dosyaları aşama klasöründe var
        for ad in SKILLER:
            p = k + ad + "/" + TEK_ASAMA_DOSYA
            if p not in kume:
                hatalar.append("%s: %s yok" % (etiket, p))
                continue
            m = z.read(p).decode("utf-8")
            if m.startswith("---"):
                hatalar.append("%s: %s frontmatter içeriyor" % (etiket, p))
            for klasor in ("references", "scripts"):
                for f in sorted(set(re.findall(klasor + r"/([A-Za-z0-9_.\-]+\.[a-z]+)", m))):
                    if "%s%s/%s/%s" % (k, ad, klasor, f) not in kume:
                        hatalar.append("%s: %s'nin andığı %s/%s yok" % (etiket, p, klasor, f))
        ajan = k + "agents/openai.yaml"
        if chatgpt:
            if ajan not in kume:
                hatalar.append("%s: agents/openai.yaml yok" % etiket)
            else:
                import yaml
                try:
                    y = yaml.safe_load(z.read(ajan).decode("utf-8")) or {}
                    if (y.get("interface") or {}).get("display_name") != "Mağaza Kurucu":
                        hatalar.append("%s: openai.yaml display_name 'Mağaza Kurucu' değil" % etiket)
                except yaml.YAMLError as e:
                    hatalar.append("%s: openai.yaml geçersiz YAML (%s)" % (etiket, e))
        elif any(n.startswith(k + "agents/") for n in adlar):
            hatalar.append("%s: Claude paketinde agents/ var" % etiket)
        for n in dosya_adlari:
            ic = n[len(k):]
            if ic.lower().endswith(YASAK_UZANTI) and not izinli_gorsel(ic):
                hatalar.append("%s: görsel/arsiv dosyası var: %s" % (etiket, n))
            if ic.lower().endswith(METIN_UZANTI) and b"\r" in z.read(n):
                hatalar.append("%s: CRLF satır sonu: %s" % (etiket, n))
    if len(bayt) > TEK_MAX_BAYT:
        hatalar.append("%s: zip %d bayt > %d" % (etiket, len(bayt), TEK_MAX_BAYT))
    return len(dosya_adlari), acik, router_bayt


def birlesik_beklenen():
    """Birleşik beceri klasörünün olması gereken içeriği: {göreli yol: bayt} (tek paketin Claude düzeni, kök öneksiz)."""
    k = TEK_KOK + "/"
    out = {}
    for kaynak, ad in tek_girdileri(False):
        out[ad[len(k):]] = kaynak if isinstance(kaynak, bytes) else oku_bayt(kaynak)
    return out


def birlesik_mevcut():
    out = {}
    for kok, _, ds in os.walk(BIRLESIK):
        for f in ds:
            if any(a in f or a in kok for a in ATLA):
                continue
            p = os.path.join(kok, f)
            out[os.path.relpath(p, BIRLESIK).replace("\\", "/")] = oku_bayt(p)
    return out


def kontrol_birlesik(hatalar):
    bek, mev = birlesik_beklenen(), birlesik_mevcut()
    for ad in sorted(set(bek) - set(mev)):
        hatalar.append("BİRLEŞİK EKSİK: skills/builder/%s (build.py çalıştır)" % ad)
    for ad in sorted(set(mev) - set(bek)):
        hatalar.append("BİRLEŞİK FAZLA: skills/builder/%s (kaynakta karşılığı yok; elle eklenmiş)" % ad)
    for ad in sorted(set(bek) & set(mev)):
        if bek[ad] != mev[ad]:
            hatalar.append("BİRLEŞİK FARKLI: skills/builder/%s (elle düzenlenmiş ya da build.py çalıştırılmamış)" % ad)
    return len(bek)


def birlesik_yaz():
    bek, mev = birlesik_beklenen(), birlesik_mevcut()
    for ad in set(mev) - set(bek):
        os.remove(os.path.join(BIRLESIK, ad))
    n = 0
    for ad, b in bek.items():
        if mev.get(ad) != b:
            h = os.path.join(BIRLESIK, ad)
            os.makedirs(os.path.dirname(h), exist_ok=True)
            with open(h, "wb") as f:
                f.write(b)
            n += 1
    for kok, ds, fs in os.walk(BIRLESIK, topdown=False):
        if not ds and not fs:
            os.rmdir(kok)
    return n


def zipleri_uret(surum):
    return []   # ayrı skill/plugin zip'i yok (tek giriş); tek paket zip'leri main() içinde yazılır


def kontrol_zip(p, hatalar):
    with zipfile.ZipFile(p) as z:
        adlar = z.namelist()
    base = os.path.basename(p)
    if base.startswith("skill-"):
        ad = base[len("skill-"):-len(".zip")]
        if not all(n.startswith(ad + "/") for n in adlar):
            hatalar.append("%s: girdiler '%s/' ile başlamıyor" % (base, ad))
        if ad + "/SKILL.md" not in adlar:
            hatalar.append("%s: SKILL.md yok" % base)
    else:
        for ad in SKILLER:
            if "skills/%s/SKILL.md" % ad not in adlar:
                hatalar.append("%s: skills/%s/SKILL.md yok" % (base, ad))
    if any(n.lower().endswith(YASAK_UZANTI) and not izinli_gorsel(n[len("skills/"):] if n.startswith("skills/") else n)
           for n in adlar):
        hatalar.append("%s: görsel/arsiv dosyası var" % base)
    return len([n for n in adlar if not n.endswith("/")])


# ------------------------------------------------------------------ ana
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="yazmadan doğrula")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if not a.check:
        n = esitle()
        print("Ortak kopyalar eşitlendi: %d dosya güncellendi" % n)

    hatalar, uyarilar, tablo = [], [], []
    kontrol_kopyalar(hatalar)
    for ad in SKILLER:
        kontrol_skill(ad, hatalar, uyarilar, tablo)
    surum = kontrol_manifest(hatalar)
    n_capa = kontrol_stil_capasi(hatalar)

    print("Sürüm: %s" % surum)
    print("%-16s %10s %10s %6s  %s" % ("skill", "SKILL.md B", "desc kar.", "refs", "durum"))
    for r in tablo:
        print("%-16s %10d %10d %6d  %s" % r)
    print("Stil çapası: %d görsel (%s)" % (n_capa, GORSEL_IZINLI_KLASOR))
    print("Ortak kopya: %d hedef, kaynakla %s" % (
        len(list(hedefler())), "AYNI" if not any(h.startswith("KOPYA") for h in hatalar) else "FARKLI"))

    # Tek paket: her iki modda bellekte kurulur ve doğrulanır; yazma yalnız derlemede
    tek_bayt = {}
    for hedef, rel in TEK_ZIPLER.items():
        b = zip_bayt(tek_girdileri(hedef == "chatgpt"))
        tek_bayt[rel] = b
        n, acik, rb = kontrol_tek(b, hedef == "chatgpt", hatalar, etiket=os.path.basename(rel))
        print("tek  %-40s %4d dosya %9d B zip (%.2f MB), açık %d B, router SKILL.md %d B"
              % (rel, n, len(b), len(b) / 1048576.0, acik, rb))

    if not a.check and not hatalar:
        print("Birleşik beceri: %d dosya yazıldı/güncellendi → %s" % (birlesik_yaz(), os.path.relpath(BIRLESIK, KOK)))
    n_bir = kontrol_birlesik(hatalar)
    print("Birleşik beceri: %d dosya, kaynakla %s" % (n_bir, "AYNI" if not any(h.startswith("BİRLEŞİK") for h in hatalar) else "FARKLI"))

    if not a.check and not hatalar:
        for p in zipleri_uret(surum):
            n = kontrol_zip(p, hatalar)
            print("zip  %-48s %4d dosya %8d B" % (os.path.relpath(p, KOK), n, os.path.getsize(p)))
        for rel, b in tek_bayt.items():
            h = yol(*rel.split("/"))
            os.makedirs(os.path.dirname(h), exist_ok=True)
            with open(h, "wb") as f:
                f.write(b)
            print("yaz  %s (%d B)" % (rel, len(b)))

    for u in uyarilar:
        print("UYARI:", u)
    for h in hatalar:
        print("HATA:", h)
    print("SONUÇ:", "GEÇTİ" if not hatalar else "KALDI (%d hata)" % len(hatalar))
    sys.exit(0 if not hatalar else 1)


if __name__ == "__main__":
    main()
