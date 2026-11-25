#!/usr/bin/env python3
"""hooks/durum-yukle.sh kırma testi: oturum başında 'Eklenti sürümü: <plugin.json sürümü>' yazılır; plugin.json yoksa 'bilinmiyor';
eski '0.4.0 AD DEĞİŞİKLİĞİ' satırı artık yok. Çıkış 0 = hepsi geçti."""
import json
import os
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EKLENTI = os.path.join(KOK, "plugins", "viral-urun-ekibi")
HOOK = os.path.join(EKLENTI, "hooks", "durum-yukle.sh")
sonuc = []


def t(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad + ("" if ok else " | " + str(ayrinti)[:300]))


def kos(kok, proje):
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=kok, CLAUDE_PROJECT_DIR=proje)
    return subprocess.run(["sh", HOOK], capture_output=True, text=True, env=env).stdout


with tempfile.TemporaryDirectory() as d:
    surum = json.load(open(os.path.join(EKLENTI, ".claude-plugin", "plugin.json"), encoding="utf-8"))["version"]
    c = kos(EKLENTI, d)
    t("sürüm satırı plugin.json sürümünü (%s) yazar" % surum, "Eklenti sürümü: %s " % surum in c, c)
    t("güncelleme uyarısı: ChatGPT zip'i elle güncellenir", "ChatGPT zip" in c and "elle" in c, c)
    t("eski '0.4.0' AD DEĞİŞİKLİĞİ satırı kalktı", "AD DEĞİŞİKLİĞİ" not in c and "0.4.0" not in c, c)
    # kırma: sürüm dosyası farklıysa çıktı değişir (sabit metin değil, dosyadan okur)
    sahte = os.path.join(d, "sahte")
    os.makedirs(os.path.join(sahte, ".claude-plugin"))
    json.dump({"name": "x", "version": "9.8.7"}, open(os.path.join(sahte, ".claude-plugin", "plugin.json"), "w"))
    t("KIRMA sürüm dosyadan okunur (sahte 9.8.7)", "Eklenti sürümü: 9.8.7 " in kos(sahte, d))
    t("KIRMA plugin.json yoksa 'bilinmiyor' (uydurma sürüm yok)", "Eklenti sürümü: bilinmiyor " in kos(os.path.join(d, "yok"), d))
kalan = sonuc.count(False)
print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
sys.exit(1 if kalan else 0)
