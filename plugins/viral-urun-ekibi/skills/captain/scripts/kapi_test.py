#!/usr/bin/env python3
"""kapi.py kırma testi: her kapı önce GEÇEN bir projede ölçülür, sonra tek tek kırılır (kırılmayan kapı yeşil sayılmaz).

Kullanım: python3 kapi_test.py [--klasor <çıktı>] [--hizli]   → hepsi geçerse 0, biri tutmazsa 1.
--hizli: video üreten yayın testlerini atlar (ffmpeg/numpy yoksa da koşar); atlanan test "ATLANDI" yazılır, geçti sayılmaz.
Kredi harcamaz, internet gerekmez. Sentetik proje geçici klasörde kurulur.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile

BURASI = os.path.dirname(os.path.abspath(__file__))
EKLENTI = os.path.abspath(os.path.join(BURASI, "..", "..", ".."))
KAPI = os.path.join(BURASI, "kapi.py")
BUGUN = datetime.date.today().isoformat()
SONUC = []

DEFTER = """# GERİ BİLDİRİM DEFTERİ
| # | Tarih | Kaynak | Anahtar | Geri bildirim / kusur | İşlenen dosya:bölüm | Durum | Bildirildi |
|---|---|---|---|---|---|---|---|
| 1 | 2000-01-01 | kurucu | ani-muzik | "müzik bir anda açılıyor" | is/01-urun/kurgu/KURALLAR.md:K3 | İŞLENDİ | evet |
"""


def yaz(yol, icerik):
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik if isinstance(icerik, str) else json.dumps(icerik, ensure_ascii=False, indent=1))
    return yol


def senaryolar(bozuk=False):
    def v(no, ozne, an, giris, ortam, eylemler, aile, kanca):
        return {"no": no, "mekanizma": "M8", "sablon": "S2", "an": an, "kanca": kanca, "aile": aile, "kimlik": False,
                "giris": giris, "ortam": ortam, "ozne": ozne,
                "sahneler": [{"eylem": e} for e in eylemler], "etkilesim_sahne": 3 if bozuk and no == 1 else 2,
                "sonuc_sahne": 2, "cta": "Yorumlara RAMPA yaz", "neden": "test"}
    return {"urun": "Test rampası", "pazar": "TR", "videolar": [
        v(1, "tekir", "Gece mama saati", "gece kamerası", "gece yatak odası",
          ["Kedi sahibinin omzuna dokunur", "Kedi tuşa basar ve mama düşer", "Kedi mamayı yer"], "K7", "Gece 3'te uyandırmıyor"),
        v(2, "siyah köpek", "Sabah kapı önü", "kapı zili yakın plan", "sabah koridor",
          ["Köpek kapıya koşar", "Sahibi rampayı açar ve köpek çıkar", "Köpek koltukta oturur"], "K12", "Bunu neden kimse söylemedi"),
        v(3, "gri tavşan", "Öğlen bahçe", "bahçe geniş plan", "öğlen bahçe",
          ["Tavşan çimde durur", "Çocuk havucu uzatır ve tavşan yaklaşır", "Tavşan havucu kemirir"], "K9", "Üç günde alıştı"),
    ]}


def proje_kur(kok):
    """Bütün kredi kapılarını GEÇEN en küçük proje. Dönen: (proje, iş klasörü)."""
    is_ = os.path.join(kok, "is", "01-urun")
    yaz(os.path.join(kok, ".ekip", "KARARLAR.md"), "# KARARLAR\n- 2000-01-01 | pazar | Türkiye\n- 2000-01-01 | kredi | Flow için en fazla 120 kredi\n")
    yaz(os.path.join(kok, ".ekip", "GERI-BILDIRIM.md"), DEFTER)
    yaz(os.path.join(is_, "senaryolar.json"), senaryolar())
    yaz(os.path.join(is_, "kurgu", "KURALLAR.md"), "# KURALLAR\nK1 süre 12–15 sn\nK2 kanca ilk karede\nK3 müzik rampayla\nK4 fiyat yok\nK5 döngü\n")
    hukum(is_, "onuretim", "V01", True)
    return kok, is_


def hukum(is_, mod, video, gecti, dosya="juri.jsonl", recete=None):
    yol = os.path.join(is_, "elestiri", dosya)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "a", encoding="utf-8") as f:
        f.write(json.dumps({"video": video, "tur": 1, "mod": mod, "gecti": gecti, "toplam": 7.5 if gecti else 5.5,
                            "recete": recete or []}, ensure_ascii=False) + "\n")


def kos(*args):
    r = subprocess.run([sys.executable, KAPI] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def bekle(ad, sonuc, kod, icermeli=(), icermemeli=()):
    k, c = sonuc
    tamam = k == kod and all(x in c for x in icermeli) and not any(x in c for x in icermemeli)
    SONUC.append((ad, tamam))
    if not tamam:
        print("--- %s (çıkış %s, beklenen %s):\n%s" % (ad, k, kod, c))


def taze(kok, ad):
    hedef = os.path.join(kok, ad)
    shutil.rmtree(hedef, ignore_errors=True)
    return proje_kur(hedef)


def kredi_testleri(kok):
    p, i = taze(kok, "k0")
    bekle("kredi: eksiksiz proje -> 0, 5 kapı GEÇTİ", kos("kredi", i, "--proje", p), 0, ["SONUÇ: GEÇTİ — geçen 5 · kalan 0"])
    kayit = [json.loads(s) for s in open(os.path.join(p, ".ekip", "kapi.jsonl"), encoding="utf-8")]
    SONUC.append(("kredi: koşu .ekip/kapi.jsonl'a yazıldı (5 kapı)", len(kayit) == 1 and len(kayit[0]["kapilar"]) == 5 and kayit[0]["sonuc"] == "GEÇTİ"))

    p, i = taze(kok, "k1"); yaz(os.path.join(i, "senaryolar.json"), senaryolar(bozuk=True))
    bekle("kırma: senaryo sebep→sonuç ihlali -> 1", kos("kredi", i, "--proje", p), 1, ["KALDI      senaryo"])
    p, i = taze(kok, "k2"); os.remove(os.path.join(i, "senaryolar.json"))
    bekle("kırma: senaryolar.json yok -> 1 (temiz demez)", kos("kredi", i, "--proje", p), 1, ["dosya yok: senaryolar.json"])
    p, i = taze(kok, "k3"); os.remove(os.path.join(i, "kurgu", "KURALLAR.md"))
    bekle("kırma: kontrat yok -> 1", kos("kredi", i, "--proje", p), 1, ["KALDI      kontrat"])
    p, i = taze(kok, "k4"); shutil.rmtree(os.path.join(i, "elestiri"))
    bekle("kırma: hüküm kaydı yok -> 1 (temiz demez)", kos("kredi", i, "--proje", p), 1, ["KALDI      hukum", "hüküm kaydı yok"])
    p, i = taze(kok, "k5"); hukum(i, "onuretim", "V02", False)
    bekle("kırma: bir videonun son ön-üretim hükmü KALDI -> 1 (kaldı ama üretildi durumu)", kos("kredi", i, "--proje", p), 1,
          ["KALDI      hukum", "V02"])
    p, i = taze(kok, "k6"); hukum(i, "onuretim", "V01", False)
    bekle("kırma: önce geçti, SON hüküm kaldı -> 1 (son satır geçerli)", kos("kredi", i, "--proje", p), 1, ["KALDI      hukum"])
    p, i = taze(kok, "k7"); yaz(os.path.join(p, ".ekip", "KARARLAR.md"), "# KARARLAR\n- 2000-01-01 | pazar | Türkiye\n")
    bekle("kırma: kredi tavanı onayı yok -> 1", kos("kredi", i, "--proje", p), 1, ["KALDI      kredi-onayi"])
    p, i = taze(kok, "k8"); os.remove(os.path.join(p, ".ekip", "GERI-BILDIRIM.md"))
    bekle("kırma: defter yok -> 1 (yok = temiz değil)", kos("kredi", i, "--proje", p), 1, ["KALDI      defter", "defter yok"])
    p, i = taze(kok, "k9"); os.remove(os.path.join(p, ".ekip", "GERI-BILDIRIM.md"))
    hukum(i, "onuretim", "V01", True, dosya="puanlar.jsonl", recete=["KALICI: müzik rampası -> skills/cut/SKILL.md:Ses"])
    bekle("kırma: KALICI reçete var, defter yok -> 1", kos("kredi", i, "--proje", p), 1, ["KALICI reçete var, hiçbiri deftere girmemiş"])
    p, i = taze(kok, "k10")
    yaz(os.path.join(p, ".ekip", "GERI-BILDIRIM.md"), DEFTER + "| 2 | 2000-01-02 | elestirmen | fiyat | organikte fiyat | — | AÇIK | hayır |\n")
    bekle("kırma: defterde AÇIK satır -> 1", kos("kredi", i, "--proje", p), 1, ["KALDI      defter"])

    # kural terfisi iki basamak (URE-02): ilk örnek ürün kontratına, eklentiye ancak ikinci örnekte
    BAS = DEFTER.split("| 1 |")[0]
    def defterli(ad, satirlar):
        p, i = taze(kok, ad)
        yaz(os.path.join(p, ".ekip", "GERI-BILDIRIM.md"), BAS + "".join(satirlar))
        return kos("kredi", i, "--proje", p)
    ILK_URUN = "| 1 | 2000-01-01 | kullanıcı | ani-muzik | müzik ani | is/01-urun/kurgu/KURALLAR.md:K3 | İŞLENDİ | evet |\n"
    bekle("kırma: ilk örnekte eklenti dosyasına kural -> 1 (tek örnekten eklenti kuralı)",
          defterli("t1", ["| 1 | 2000-01-01 | kullanıcı | ani-muzik | müzik ani | skills/cut/SKILL.md:Ses | İŞLENDİ | evet |\n"]), 1,
          ["tek örnekten eklenti kuralı"])
    bekle("terfi: ilk örnek kontrata, ikinci örnek üretici dosyaya (TEKRAR-DÜZELTİLDİ) -> 0",
          defterli("t2", [ILK_URUN, "| 2 | 2000-01-05 | direktör | ani-muzik | yine ani | agents/ses-tasarimcisi.md:Kurallar | TEKRAR-DÜZELTİLDİ | evet |\n"]), 0,
          ["GEÇTİ      defter"])
    bekle("kırma: ikinci örnek yine yalnız kontrata yazılmış -> 1 (üretici düzeltilmemiş)",
          defterli("t3", [ILK_URUN, "| 2 | 2000-01-05 | direktör | ani-muzik | yine ani | is/01-urun/kurgu/KURALLAR.md:K3 | İŞLENDİ | evet |\n"]), 1,
          ["TEKRAR-DÜZELTİLDİ olmalı"])
    bekle("kırma: işlendi ama kullanıcıya bildirilmedi -> 1",
          defterli("t4", [ILK_URUN.replace("| evet |", "| hayır |")]), 1, ["bildirilmedi"])

    # aşım: yalnız KARARLAR'da tarihli kurucu satırıyla, kapı başına
    def asimli(ad, satir):
        p, i = taze(kok, ad); hukum(i, "onuretim", "V01", False)
        with open(os.path.join(p, ".ekip", "KARARLAR.md"), "a", encoding="utf-8") as f:
            f.write(satir + "\n")
        return kos("kredi", i, "--proje", p)
    bekle("aşım: tarihli kurucu satırı -> 0, AŞILDI görünür", asimli("a1", '- %s | kapi-asimi | kredi 01-urun hukum: "gerçekçilik 6 kalsın, üretelim"' % BUGUN),
          0, ["AŞILDI", "AŞIMLA GEÇTİ", "gerçekçilik 6 kalsın"])
    bekle("kırma: başka kapıya yazılmış aşım -> 1", asimli("a2", '- %s | kapi-asimi | kredi 01-urun senaryo: "senaryo böyle kalsın"' % BUGUN), 1, ["KALDI      hukum"])
    bekle("kırma: başka işe yazılmış aşım -> 1", asimli("a3", '- %s | kapi-asimi | kredi 02-baska hukum: "üretelim gitsin"' % BUGUN), 1, ["KALDI      hukum"])
    bekle("kırma: başka geçişe yazılmış aşım -> 1", asimli("a4", '- %s | kapi-asimi | yayin 01-urun hukum: "üretelim gitsin"' % BUGUN), 1, ["KALDI      hukum"])
    bekle("kırma: ileri tarihli aşım -> 1", asimli("a5", '- 2999-01-01 | kapi-asimi | kredi 01-urun hukum: "üretelim gitsin"'), 1, ["ileri tarihli"])
    bekle("kırma: kurucu cümlesi olmayan aşım -> 1", asimli("a6", "- %s | kapi-asimi | kredi 01-urun hukum" % BUGUN), 1, ["biçim tutmuyor"])
    bekle("kırma: 'hepsi' diye toplu aşım -> 1", asimli("a7", '- %s | kapi-asimi | kredi 01-urun hepsi: "hepsini geç, üretelim"' % BUGUN), 1, ["KALDI      hukum"])

    bekle("kullanım: iş klasörü yok -> 2", kos("kredi", os.path.join(kok, "yok"), "--proje", kok), 2)
    k, c = kos("liste")
    SONUC.append(("liste: kredi 5 kapı, yayin 8 kapı (kapının kendisi sayılır)", k == 0 and "kredi (5)" in c and "yayin (8)" in c))


def video_uret(is_, ad, delik=False):
    """6 sn 1080×1920 video + müzik stem'i; müzik −30 dB'den 1,75 sn rampa, açılışta diegetik tık, −14 LUFS."""
    import wave
    import numpy as np
    sys.path.insert(0, os.path.join(EKLENTI, "skills", "cut", "scripts"))
    import ffaraclar as F
    ff, sr = F.ffmpeg_bul(), 48000
    t = np.arange(int(6 * sr)) / sr
    muz = 0.3 * np.sin(2 * np.pi * 220 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 2 * t))
    muz = muz * np.where(t < 1.75, 10 ** ((-30 + 30 * t / 1.75) / 20), 1.0)
    tik = np.where(t < 0.25, 0.25 * np.sin(2 * np.pi * 900 * t), 0.0)
    karisim = muz + tik
    if delik:
        karisim[(t > 3.0) & (t < 3.6)] = 0.0

    def wav(yol, x):
        os.makedirs(os.path.dirname(yol), exist_ok=True)
        with wave.open(yol, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
    video = os.path.join(is_, "kurgu", ad + ".mp4")
    os.makedirs(os.path.dirname(video), exist_ok=True)
    gecici = os.path.join(is_, "kurgu", "_" + ad + ".wav")
    kazanc = 1.0
    for _ in range(3):  # ölç-düzelt: −14 LUFS
        wav(gecici, karisim * kazanc)
        F.calistir([ff, "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x2a6f97:s=1080x1920:r=30:d=6,noise=alls=8:allf=t",
                    "-i", gecici, "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", video])
        fark = -14.0 - F.lufs_olc(video)
        if abs(fark) < 0.3:
            break
        kazanc *= 10 ** (fark / 20)
    os.remove(gecici)
    wav(os.path.join(is_, "ses", "stem_" + ad, "muz.wav"), muz * kazanc)
    yaz(os.path.join(is_, "kurgu", ad + ".json"), {"planlar": [["../klipler/%s_S1.mp4" % ad, 0, 6.0]], "kanca": "Bunu izle", "cikti": "kurgu/%s.mp4" % ad})
    return video


def yayin_testleri(kok):
    p, i = taze(kok, "y0")
    video_uret(i, "V01")
    hukum(i, "teslim", "V01", True)
    bekle("yayin: eksiksiz video -> 0 (teknik, görüntü, ses, hüküm, defter geçti)", kos("yayin", i, "--proje", p, "--kopyala"), 0,
          ["GEÇTİ      teknik@V01", "GEÇTİ      goruntu@V01", "GEÇTİ      ses@V01", "GEÇTİ      hukum@V01", "GEÇTİ      defter",
           "UYGULANMAZ kurgu@V01", "UYGULANMAZ sozlesme", "kalan 0"])
    SONUC.append(("yayin: geçince --kopyala teslim/V01.mp4 üretti", os.path.exists(os.path.join(i, "teslim", "V01.mp4"))))
    temiz = os.path.join(kok, "y0")

    def kopya(ad):
        hedef = os.path.join(kok, ad)
        shutil.rmtree(hedef, ignore_errors=True)
        shutil.copytree(temiz, hedef)
        shutil.rmtree(os.path.join(hedef, "is", "01-urun", "teslim"), ignore_errors=True)
        return hedef, os.path.join(hedef, "is", "01-urun")

    p, i = kopya("y1"); hukum(i, "teslim", "V01", False)
    bekle("kırma: son teslim hükmü KALDI -> 1, teslim klasörüne kopyalanmaz", kos("yayin", i, "--proje", p, "--kopyala"), 1,
          ["KALDI      hukum@V01", "KOPYALANMADI"])
    SONUC.append(("kırma: kaldıysa teslim/V01.mp4 YOK", not os.path.exists(os.path.join(i, "teslim", "V01.mp4"))))
    p, i = kopya("y2"); shutil.rmtree(os.path.join(i, "ses"))
    bekle("kırma: müzik stem'i yok -> 1 (ölçülemeyen = kaldı)", kos("yayin", i, "--proje", p), 1, ["KALDI      ses@V01", "stem"])
    p, i = kopya("y3"); os.remove(os.path.join(i, "kurgu", "V01.json"))
    bekle("kırma: ayar dosyası yok -> 1", kos("yayin", i, "--proje", p), 1, ["KALDI      goruntu@V01", "ayar dosyası yok"])
    p, i = kopya("y4"); os.remove(os.path.join(i, "kurgu", "V01.mp4"))
    bekle("kırma: teslim videosu yok -> 1 (temiz demez)", kos("yayin", i, "--proje", p), 1, ["teslim videosu yok", "kapı koşmadı"])
    p, i = kopya("y5"); video_uret(i, "V01", delik=True)
    bekle("kırma: 0,6 sn ses deliği -> 1", kos("yayin", i, "--proje", p), 1, ["KALDI      ses@V01"])
    p, i = kopya("y6"); os.remove(os.path.join(p, ".ekip", "GERI-BILDIRIM.md"))
    bekle("kırma: yayında defter yok -> 1", kos("yayin", i, "--proje", p), 1, ["KALDI      defter"])
    # mağaza paketi varsa iddia + sözleşme kapıları devreye girer (örnek paket: ortak/sozlesme/ornek)
    ornek = os.path.join(EKLENTI, "ortak", "sozlesme", "ornek", "magaza-paketi.json")
    p, i = kopya("y7"); os.makedirs(os.path.join(i, "magaza")); shutil.copy(ornek, os.path.join(i, "magaza", "magaza-paketi.json"))
    bekle("yayin: mağaza paketi + iddiasız yazı -> 0 (iddia ve sözleşme kapısı koştu)", kos("yayin", i, "--proje", p), 0,
          ["GEÇTİ      iddia@V01", "GEÇTİ      sozlesme"])
    d = json.load(open(os.path.join(i, "kurgu", "V01.json"), encoding="utf-8")); d["yazilar"] = [{"bas": 0, "bit": 2, "yazi": "%97 müşteri memnun"}]
    yaz(os.path.join(i, "kurgu", "V01.json"), d)
    bekle("kırma: ekranda uydurma istatistik -> 1", kos("yayin", i, "--proje", p), 1, ["KALDI      iddia@V01"])
    d["yazilar"] = [{"bas": 0, "bit": 2, "yazi": "Bel ağrısını geçirir"}]; yaz(os.path.join(i, "kurgu", "V01.json"), d)
    bekle("yayin: ekranda sağlık cümlesi -> 0 (engel değil, bilgi notu)", kos("yayin", i, "--proje", p), 0, ["GEÇTİ      iddia@V01"])
    yaz(os.path.join(i, "magaza", "magaza-paketi.json"), {"surum": "1"})
    bekle("kırma: bozuk mağaza paketi -> 1", kos("yayin", i, "--proje", p), 1, ["KALDI      sozlesme"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--klasor")
    ap.add_argument("--hizli", action="store_true")
    a = ap.parse_args()
    kok = os.path.abspath(a.klasor or tempfile.mkdtemp(prefix="kapi_test_"))
    os.makedirs(kok, exist_ok=True)
    kredi_testleri(kok)
    atlanan = 0
    if a.hizli:
        atlanan = 1
        print("ATLANDI yayın testleri (--hizli): video üretilmedi, bu kapılar bu koşuda ÖLÇÜLMEDİ")
    else:
        yayin_testleri(kok)
    for ad, ok in SONUC:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    kalan = sum(1 for _, ok in SONUC if not ok)
    print("klasör:", kok)
    print("TOPLAM: %d test, %d kaldı%s" % (len(SONUC), kalan, ", yayın grubu atlandı" if atlanan else ""))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
