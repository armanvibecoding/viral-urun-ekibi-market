#!/usr/bin/env python3
"""Kırma testleri — her kapı önce BOZUK girdiyle çıkış ≠ 0 vermeli, sonra doğru girdiyle geçmeli.

  python3 kendini_test.py [--gercek-ozet <eski-ozet.tsv>]

1 gerçek veriyle geri test (özet yoksa ATLANDI — geçti sayılmaz) · 2 tekilleştirme · 3 eksik alan = görünmüyor ·
4 sessiz sınırlama (çıkış 3) · 5 kota/tekrar/hız/kontrol kapısı · 6 elle etiket · 7 yanlış veri → çıkış ≠ 0 (her betik).
Çıkış: tüm testler geçerse 0, biri bile düşerse 1.
"""
import argparse
import os
import subprocess
import sys
import tempfile

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)
import ortak as o  # noqa: E402
import geri_test as gt  # noqa: E402

PY = sys.executable
SONUC = []


def kos(betik, *arg, saat="10:00:00", tarih="2026-11-07"):
    env = dict(os.environ, REKLAMAVI_SIMDI="%sT%s" % (tarih, saat))
    p = subprocess.run([PY, os.path.join(BURASI, betik)] + list(arg), env=env, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def kayit(no, ad, kirma, gecis, not_=""):
    """kirma/gecis: (beklenen_aciklama, gorulen_kod, tamam_mi)"""
    ok = kirma[2] and gecis[2]
    SONUC.append((no, ad, "%s → %s" % (kirma[0], kirma[1]), "%s → %s" % (gecis[0], gecis[1]), "GEÇTİ" if ok else "DÜŞTÜ", not_))


def kok_hazir(kontrol_kart="30"):
    kok = tempfile.mkdtemp(prefix="reklamavi-test-")
    assert kos("nis_kelime.py", "kaydet", "--kok", kok, "--ulke", "TR", "--aile", "KONTROL", "--sorgu", "trendyol", saat="09:00:00")[0] == 0
    kos("nis_kelime.py", "sonuc", "--kok", kok, "--ulke", "TR", "--sorgu", "trendyol", "--kart", kontrol_kart, saat="09:00:05")
    return kok


META = {"ulke": "TR", "sorgu": "kedi yatağı", "nis": "evcil", "aile": "U", "siralama": "gosterim", "baslangic": "2026-11-07T10:00"}


def kart(kod, tarih="2026-09-01", kopya=1, tam="1", link="https://l.facebook.com/l.php?u=https%3A%2F%2Fornek-dukkan.com%2Fproducts%2Fkedi-yatagi"):
    return [str(kod), "Örnek Dükkan", gt.tr_tarih(tarih) if tam == "1" else "",
            ("%d reklam bu kreatifi ve metni kullanıyor" % kopya) if kopya > 1 else "", tam, link, "Şimdi Alışveriş Yap", "video",
            "Kediniz bu yatağa bayılacak kapıda ödeme"]


def sorgu_ac(kok, sorgu="kedi yatağı", aile="U", nis="evcil", saat="10:00:00"):
    return kos("nis_kelime.py", "kaydet", "--kok", kok, "--ulke", "TR", "--aile", aile, "--nis", nis, "--sorgu", sorgu, saat=saat)


def test1(ozet):
    if not ozet:
        SONUC.append((1, "Gerçek veriyle geri test", "—", "—", "ATLANDI", "--gercek-ozet verilmedi; geçti SAYILMAZ"))
        return
    print("[1] kırma (bir kart düşürülmüş):")
    k1, _ = gt.calistir(ozet, boz=True)
    print("[1] geçiş (tam ham):")
    k2, _ = gt.calistir(ozet, boz=False)
    kayit(1, "Gerçek veriyle geri test", ("1 kart düşür → tutmamalı", k1, k1 != 0), ("tam ham → hepsi tutmalı", k2, k2 == 0),
          "çıktıda en çok reklamlı satır yazılı")


def test2():
    kok = kok_hazir()
    sorgu_ac(kok)
    y = gt.ham_yaz(os.path.join(kok, "ham2"), META, [kart(111, kopya=2), kart(111, kopya=3), kart(222, kopya=3)])
    g, _ = kos("meta_kayit.py", "kaydet", "--kok", kok, *y)
    rs = o.oku(kok, "reklam")
    dogru = g == 0 and len(rs) == 2 and {r["kutuphane_kodu"]: r["kopya"] for r in rs} == {"111": "3", "222": "3"}
    m2 = dict(META, sorgu="kedi annesi", aile="K")
    sorgu_ac(kok, "kedi annesi", "K", saat="10:00:30")
    y2 = gt.ham_yaz(os.path.join(kok, "ham2b"), dict(m2, baslangic="2026-11-07T10:01"), [kart(111, kopya=3)])
    g2, _ = kos("meta_kayit.py", "kaydet", "--kok", kok, *y2)
    rs = o.oku(kok, "reklam")
    dogru = dogru and g2 == 0 and len(rs) == 2 and o.oku(kok, "birim")[0]["reklam_sayisi"] == "2"
    d0, _ = kos("kayit_denetle.py", "--kok", kok)
    with open(o.dosya_yolu(kok, "reklam"), "a", encoding="utf-8") as f:     # kır: aynı kod elle ikinci kez
        f.write("\t".join(rs[0][c] for c in o.REKLAM_SUTUN) + "\n")
    d1, _ = kos("kayit_denetle.py", "--kok", kok)
    kayit(2, "Tekilleştirme", ("aynı kod 2 satır → denetle", d1, d1 != 0),
          ("aynı kod 2× + başka sorgu → 1 satır; farklı kod ayrı, kopya 3 korunur", "%s/%s" % (g, d0), dogru and d0 == 0))


def test3():
    kok = kok_hazir()
    sorgu_ac(kok)
    y = gt.ham_yaz(os.path.join(kok, "ham3"), META, [kart(301, tam="0"), kart(302)])
    g, _ = kos("meta_kayit.py", "kaydet", "--kok", kok, *y)
    rs = {r["kutuphane_kodu"]: r for r in o.oku(kok, "reklam")}
    a = rs.get("301", {})
    dogru = g == 0 and a.get("ilk_yayin") == o.GORUNMUYOR and a.get("aktif_gun") == o.GORUNMUYOR and \
        a.get("kopya") == o.GORUNMUYOR and a.get("etiket") == "BILINMIYOR" and rs.get("302", {}).get("kopya") == "1"
    d0, _ = kos("kayit_denetle.py", "--kok", kok)
    satirlar = o.oku(kok, "reklam")
    for r in satirlar:
        if r["kutuphane_kodu"] == "301":
            r["kopya"] = "0"; r["aktif_gun"] = "67"          # kır: okunamayanı 0 / uydurma gün yaz
    o.yaz(kok, "reklam", satirlar)
    d1, cikti = kos("kayit_denetle.py", "--kok", kok)
    kayit(3, "Eksik alan = görünmüyor", ("kopya=0 + uydurma aktif_gun → denetle", d1, d1 != 0 and "0 yazılmaz" in cikti),
          ("yaprak yok → 3 alan 'görünmüyor', etiket BILINMIYOR", "%s/%s" % (g, d0), dogru and d0 == 0))


def test4():
    kok = kok_hazir()
    sorgu_ac(kok)
    y = gt.ham_yaz(os.path.join(kok, "ham4"), META, [])
    g_kontrolsuz, _ = kos("meta_kayit.py", "kaydet", "--kok", kok, *y, saat="10:01:00")
    kos("nis_kelime.py", "kaydet", "--kok", kok, "--ulke", "TR", "--aile", "KONTROL", "--sorgu", "trendyol", saat="10:01:30")
    s0, _ = kos("nis_kelime.py", "sonuc", "--kok", kok, "--ulke", "TR", "--sorgu", "trendyol", "--kart", "0", saat="10:01:40")
    g3, cikti3 = kos("meta_kayit.py", "kaydet", "--kok", kok, *y, saat="10:02:00")
    sonra, _ = sorgu_ac(kok, "kedi oyuncağı", saat="10:03:00")      # sınırlamadan sonra yeni sorgu reddedilmeli
    kok2 = kok_hazir()
    sorgu_ac(kok2)
    y2 = gt.ham_yaz(os.path.join(kok2, "ham4b"), META, [])
    kos("nis_kelime.py", "kaydet", "--kok", kok2, "--ulke", "TR", "--aile", "KONTROL", "--sorgu", "trendyol", saat="10:01:30")
    kos("nis_kelime.py", "sonuc", "--kok", kok2, "--ulke", "TR", "--sorgu", "trendyol", "--kart", "25", saat="10:01:40")
    g0, _ = kos("meta_kayit.py", "kaydet", "--kok", kok2, *y2, saat="10:02:00")
    durum = [a["durum"] for a in o.oku(kok2, "arama") if a["aile"] == "U"]
    kayit(4, "Sessiz sınırlama", ("0 kart + kontrol 0 → 3; kontrolsüz 0 kart → 2; sonra yeni sorgu → 1",
                                  "%s/%s/%s/%s" % (g3, g_kontrolsuz, s0, sonra),
                                  g3 == 3 and "SINIRLAMA" in cikti3 and g_kontrolsuz == 2 and s0 == 3 and sonra == 1),
          ("0 kart + kontrol dolu → GERCEK-SIFIR", g0, g0 == 0 and durum == ["GERCEK-SIFIR"]))


def test5():
    kok = tempfile.mkdtemp(prefix="reklamavi-test-")
    kontrolsuz, _ = sorgu_ac(kok, saat="08:00:00")
    kok = kok_hazir()
    kodlar = []
    for i in range(1, 29):                                   # kontrol 1 + 28 sorgu = 29
        kodlar.append(sorgu_ac(kok, "sorgu %d" % i, saat="10:%02d:%02d" % ((i * 20) // 60, (i * 20) % 60))[0])
    otuzuncu, _ = sorgu_ac(kok, "sorgu 30", saat="10:20:00")     # kontrol + 29 sorgu = 30: kabul
    tekrar, _ = sorgu_ac(kok, "sorgu 1", saat="10:30:00")
    otuzbir, cikti = sorgu_ac(kok, "sorgu 31", saat="10:31:00")
    kok3 = kok_hazir()
    sorgu_ac(kok3, "a", saat="10:00:00")
    cok_hizli, _ = sorgu_ac(kok3, "b", saat="10:00:05")
    n = len(o.oku(kok, "arama"))
    kayit(5, "Kota (≤30, tekrar, ≥15 sn, önce kontrol)",
          ("31. sorgu / aynı sorgu / 5 sn / kontrolsüz", "%s/%s/%s/%s" % (otuzbir, tekrar, cok_hizli, kontrolsuz),
           otuzbir == 1 and "KOTA" in cikti and tekrar == 1 and cok_hizli == 1 and kontrolsuz == 1),
          ("1–30. sorgu kabul", "30 satır" if n == 30 else "%d satır" % n, all(k == 0 for k in kodlar) and otuzuncu == 0 and n == 30))


def test6():
    kok = kok_hazir()
    sorgu_ac(kok)
    y = gt.ham_yaz(os.path.join(kok, "ham6"), META, [kart(601), kart(602, kopya=4)])
    kos("meta_kayit.py", "kaydet", "--kok", kok, *y)
    d0, _ = kos("meta_kayit.py", "denetle", "--kok", kok)
    bs = o.oku(kok, "birim")
    bs[0]["etiket"] = "OLCEKLENIYOR" if bs[0]["etiket"] != "OLCEKLENIYOR" else "TEST"
    o.yaz(kok, "birim", bs)
    d1, cikti = kos("meta_kayit.py", "denetle", "--kok", kok)
    rs = o.oku(kok, "reklam")
    rs[0]["etiket"] = "ESKI-KAZANAN"
    o.yaz(kok, "reklam", rs)
    d2, _ = kos("kazanan_puan.py", "--kok", kok, "--denetle")
    kayit(6, "Elle etiket", ("sayfalar / reklamlar etiketi elle değişti → denetle", "%s/%s" % (d1, d2), d1 == 1 and d2 == 1),
          ("betiğin yazdığı etiket → denetle", d0, d0 == 0))


def test7():
    """Yanlış veri → çıkış ≠ 0 (her betik) + doğru veriyle uçtan uca duman testi."""
    kok = kok_hazir()
    sorgu_ac(kok)
    bozuklar = []

    def yaz(ad, metin):
        p = os.path.join(kok, ad)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(metin)
        return p

    ham = gt.ham_yaz(os.path.join(kok, "iyi"), META, [kart(701), kart(702, kopya=5, tarih="2026-08-01")], parca=2)
    b = "\t".join(["#REKLAMAVI v1", "ulke=TR", "sorgu=kedi yatağı", "nis=evcil", "aile=U", "siralama=gosterim", "baslangic=2026-11-07T10:00"])
    bozuklar.append(("başlık yok", kos("meta_kayit.py", "kaydet", "--kok", kok, yaz("b1.txt", "701\tx\n"))[0]))
    bozuklar.append(("kart sayısı tutmuyor", kos("meta_kayit.py", "kaydet", "--kok", kok, yaz("b2.txt", b + "\tkart=3\tparca=1/1\n" + "\t".join(kart(701)) + "\n"))[0]))
    bozuklar.append(("parça eksik", kos("meta_kayit.py", "kaydet", "--kok", kok, ham[0])[0]))
    bozuklar.append(("kod sayı değil", kos("meta_kayit.py", "kaydet", "--kok", kok, yaz("b3.txt", b + "\tkart=1\tparca=1/1\n" + "\t".join(["ABC"] + kart(1)[1:]) + "\n"))[0]))
    bozuklar.append(("alan sayısı yanlış", kos("meta_kayit.py", "kaydet", "--kok", kok, yaz("b4.txt", b + "\tkart=1\tparca=1/1\n701\tx\ty\n"))[0]))
    bozuklar.append(("ülke geçersiz", kos("meta_kayit.py", "kaydet", "--kok", kok, yaz("b5.txt", b.replace("ulke=TR", "ulke=XX") + "\tkart=0\tparca=1/1\n"))[0]))
    bozuklar.append(("kota dışı sorgu", kos("meta_kayit.py", "kaydet", "--kok", kok, yaz("b6.txt", b.replace("kedi yatağı", "kayıtsız sorgu") + "\tkart=0\tparca=1/1\n"))[0]))
    bozuklar.append(("TSV başlığı bozuk", (lambda: (yaz("x/reklamlar.tsv", "yanlis\tbaslik\n"), kos("kayit_denetle.py", "--kok", os.path.join(kok, "x"))[0])[1])()))
    bozuklar.append(("niş bilinmiyor", kos("nis_kelime.py", "gun", "--kok", kok, "--ulke", "TR", "--nis", "yok-nis")[0]))
    bozuklar.append(("ELE nişi planlanamaz", kos("nis_kelime.py", "gun", "--kok", kok, "--ulke", "TR", "--nis", "kozmetik-saglik")[0]))
    bozuklar.append(("mağaza dökümü adet tutmuyor", kos("magaza_gecis.py", "aktar", "--kok", kok, yaz("m1.txt", "#REKLAMAVI-MAGAZA v1\tokuma=2026-11-07\tadet=2\tparca=1/1\nornek-dukkan.com\tOK\t1\t2026-08-01\t2026-08-01\t499\tKedi yatağı\t2026-08-01\t499\t899\tkedi-yatagi\n"))[0]))
    bozuklar.append(("mağaza OK ama tarih yok", kos("magaza_gecis.py", "aktar", "--kok", kok, yaz("m2.txt", "#REKLAMAVI-MAGAZA v1\tokuma=2026-11-07\tadet=1\tparca=1/1\nornek-dukkan.com\tOK\t1\t\t\t499\tKedi\t\t499\t\tk\n"))[0]))
    desen_baslik = "id,kaynak,hesap,pazar,reklam_gun,kopya,izlenme,hesap_medyan,paylasim,begeni,kazanan," + ",".join(
        ["kanca_ailesi", "giris_turu", "format", "ses", "cta", "duygu", "mizah", "mekanizma"]) + "\n"
    bozuklar.append(("desen: yalnız kazanan", kos("desen_say.py", yaz("d1.csv", desen_baslik + "1,META-reklam,a,TR,40,5,,,,,,K1,İ1,AI,müzik,yok,merak,yok,M2\n"))[0]))
    bozuklar.append(("desen: elle kazanan çelişkili", kos("desen_say.py", yaz("d2.csv", desen_baslik + "1,META-reklam,a,TR,40,5,,,,,H,K1,İ1,AI,müzik,yok,merak,yok,M2\n2,META-reklam,b,TR,5,1,,,,,,K2,İ1,AI,müzik,yok,merak,yok,M2\n"))[0]))
    bozuklar.append(("desen: sütun eksik", kos("desen_say.py", yaz("d3.csv", "id,kaynak\n1,META-reklam\n"))[0]))
    bozuklar.append(("rapor: kayıt yok", kos("haftalik_rapor.py", "--kok", tempfile.mkdtemp())[0]))
    hepsi_red = all(k != 0 for _, k in bozuklar)
    # doğru veriyle uçtan uca
    g1, _ = kos("meta_kayit.py", "kaydet", "--kok", kok, *ham)
    g2, liste = kos("magaza_gecis.py", "liste", "--kok", kok)
    g3, _ = kos("magaza_gecis.py", "aktar", "--kok", kok, yaz("m3.txt", "#REKLAMAVI-MAGAZA v1\tokuma=2026-11-07\tadet=1\tparca=1/1\nornek-dukkan.com\tOK\t1\t2026-07-01\t2026-07-01\t499\tKedi yatağı\t2026-07-01\t499\t899\tkedi-yatagi\n"))
    g4, _ = kos("magaza_gecis.py", "esleme", "--kok", kok)
    satirlar = desen_baslik + "".join("%d,META-reklam,h%d,TR,%d,%d,,,,,,%s,İ1,AI,müzik,yok,merak,yok,M2\n" % (
        i, i, 40 if i <= 4 else 5, 4 if i <= 4 else 1, "K1" if i <= 4 else "K2") for i in range(1, 9))
    g5, desen = kos("desen_say.py", yaz("d4.csv", satirlar))
    g6, _ = kos("haftalik_rapor.py", "--kok", kok)
    g7, _ = kos("kayit_denetle.py", "--kok", kok)
    esleme = open(os.path.join(kok, "aliexpress-esleme.md"), encoding="utf-8").read()
    uctan = [g1, g2, g3, g4, g5, g6, g7]
    dogru = all(k == 0 for k in uctan) and "META-702" in esleme and "__REKLAMAVI_MAGAZALAR" in liste and \
        "| kanca_ailesi | K1 | 4/4 | 0/4 |" in desen and "AYIRT EDİYOR" in desen
    reddetmeyen = [a for a, k in bozuklar if k == 0]
    kayit(7, "Yanlış veri → çıkış≠0 (her betik) + uçtan uca",
          ("%d bozuk girdi" % len(bozuklar), "hepsi ≠0" if hepsi_red else "reddetmeyen: " + ", ".join(reddetmeyen), hepsi_red),
          ("kaydet→liste→aktar→esleme→desen→rapor→denetle", "/".join(str(k) for k in uctan), dogru),
          "1–6'nın her birinde kırma adımı ayrıca ≠0 görüldü (tablo 'Kırma' sütunu)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gercek-ozet")
    a = ap.parse_args()
    test1(a.gercek_ozet)
    for t in (test2, test3, test4, test5, test6, test7):
        try:
            t()
        except Exception as e:  # test kendi hatası da DÜŞTÜ sayılır
            SONUC.append((t.__name__[-1], t.__name__, "—", "—", "DÜŞTÜ", "istisna: %r" % e))
    print("\n| # | Test | Kırma (beklenen → görülen çıkış) | Geçiş (beklenen → görülen) | Sonuç | Not |")
    print("|---|---|---|---|---|---|")
    for s in SONUC:
        print("| %s | %s | %s | %s | %s | %s |" % s)
    dusen = [s for s in SONUC if s[4] == "DÜŞTÜ"]
    print("\n%d test · geçti %d · düştü %d · atlandı %d" % (len(SONUC), sum(1 for s in SONUC if s[4] == "GEÇTİ"),
                                                          len(dusen), sum(1 for s in SONUC if s[4] == "ATLANDI")))
    sys.exit(1 if dusen else 0)


if __name__ == "__main__":
    main()
