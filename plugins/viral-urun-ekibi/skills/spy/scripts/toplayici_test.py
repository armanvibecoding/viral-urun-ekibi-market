#!/usr/bin/env python3
"""Shopify reklam toplayıcı kırma testleri + pilot uçtan uca (sahte veri: ../tests/).

  python3 toplayici_test.py            [REKLAMAVI_ANALIZ_MODUL=<proje>/veri/db.py ile adaptör de sınanır]

Her kapı önce BOZUK girdiyle çıkış ≠ 0 vermeli, sonra doğru girdiyle geçmeli (kendini_test.py kalıbı).
 1 kuyruk üretimi (tekrar güvenli, ELE yok, IT/NL EN-yedek)   2 günlük tavan + bekleme (yükseltme reddi)
 3 bozuk JSON → hata + gün kilidi, ertesi gün devam           4 engel izi → çıkış 3 + kilit, ertesi gün devam
 5 kayıtsız çağrı reddi + reklam id tekilleştirme             6 Shopify: alan başına tek istek, önbellek, 429 erteleme, 3×429 dur
 7 puan: Shopify olmayan/bilinmeyen derin kuyruğa girmez       8 adaptör: modül yoksa çıkış 4; varsa geçici DB'ye yazar
 9 pilot uçtan uca: US/DE/TR × evcil/mutfak (6 MCP) + Chrome dökümü → işle → alan → Shopify → puan → derin kuyruk
Çıkış: hepsi geçerse 0, biri düşerse 1 (ATLANDI geçti sayılmaz ama düşürmez).
"""
import http.server
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading

BURASI = os.path.dirname(os.path.abspath(__file__))
VERI = os.path.join(os.path.dirname(BURASI), "tests")
PY = sys.executable
SONUC = []
SAYAC = {}


def kos(betik, *arg, zaman="2026-11-18T10:00:00", env_ek=None):
    env = dict(os.environ, REKLAMAVI_SIMDI=zaman)
    env.update(env_ek or {})
    p = subprocess.run([PY, os.path.join(BURASI, betik)] + [str(a) for a in arg], env=env, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def kayit(no, ad, kirma, gecis, not_=""):
    ok = kirma[2] and gecis[2]
    SONUC.append((no, ad, "%s → %s" % (kirma[0], kirma[1]), "%s → %s" % (gecis[0], gecis[1]), "GEÇTİ" if ok else "DÜŞTÜ", not_))


def yeni_db():
    return os.path.join(tempfile.mkdtemp(prefix="toplayici-test-"), "reklam.db")


def sorgu(db, sql, *a):
    c = sqlite3.connect(db)
    try:
        return c.execute(sql, a).fetchall()
    finally:
        c.close()


def v(ad):
    return os.path.join(VERI, ad)


def al_isle(db, dosya, zaman):
    k, out = kos("kuyruk.py", "al", "--db", db, "--yol", "mcp", zaman=zaman)
    if k != 0:
        return k, out, None
    kid = json.loads(out)["id"]
    k2, out2 = kos("toplanan_isle.py", "mcp", "--db", db, "--id", kid, dosya, zaman=zaman)
    return k2, out2, kid


# ------------------------------------------------------------------ testler
def test1():
    db = yeni_db()
    k1, _ = kos("kuyruk.py", "uret", "--db", db, "--pazar", "US,XX")
    k2, _ = kos("kuyruk.py", "uret", "--db", db, "--pazar", "US", "--nis", "kozmetik-saglik")
    g1, _ = kos("kuyruk.py", "uret", "--db", db, "--pazar", "US,IT,TR")
    n1 = sorgu(db, "SELECT COUNT(*) FROM kuyruk")[0][0]
    g2, _ = kos("kuyruk.py", "uret", "--db", db, "--pazar", "US,IT,TR")
    n2 = sorgu(db, "SELECT COUNT(*) FROM kuyruk")[0][0]
    ele = sorgu(db, "SELECT COUNT(*) FROM kuyruk WHERE nis='kozmetik-saglik'")[0][0]
    it = sorgu(db, "SELECT DISTINCT dil FROM kuyruk WHERE pazar='IT'")
    nis_sayi = sorgu(db, "SELECT COUNT(DISTINCT nis) FROM kuyruk")[0][0]
    ok = g1 == g2 == 0 and n1 == n2 == 3 * nis_sayi and ele == 0 and it == [("EN-yedek",)]
    kayit(1, "Kuyruk üretimi", ("geçersiz pazar / ELE nişi", "%d/%d" % (k1, k2), k1 != 0 and k2 != 0),
          ("2× üret → aynı %d satır, ELE 0, IT=EN-yedek" % n1, "%d/%d · %s" % (g1, g2, it), ok),
          "mcp: niş başına 1 sorgu × pazar")


def test2():
    db = yeni_db()
    kos("kuyruk.py", "uret", "--db", db, "--pazar", "US,DE,TR", "--nis", "evcil,mutfak")
    ky, _ = kos("kuyruk.py", "al", "--db", db, "--yol", "mcp", "--tavan", "500")
    kb, _ = kos("kuyruk.py", "al", "--db", db, "--yol", "mcp", "--bekle", "1")
    a1, o1, _ = al_isle(db, v("ornek_mcp_US_evcil.json"), "2026-11-18T10:00:00")
    hizli, oh = kos("kuyruk.py", "al", "--db", db, "--yol", "mcp", "--tavan", "2", zaman="2026-11-18T10:00:05")
    a2, _, _ = al_isle(db, v("ornek_mcp_US_mutfak.json"), "2026-11-18T10:00:30")
    tavan, ot = kos("kuyruk.py", "al", "--db", db, "--yol", "mcp", "--tavan", "2", zaman="2026-11-18T10:01:30")
    ertesi, _ = kos("kuyruk.py", "al", "--db", db, "--yol", "mcp", "--tavan", "2", zaman="2026-11-19T09:00:00")
    kayit(2, "Günlük tavan + bekleme",
          ("tavan 500 / bekleme 1 sn / 5 sn sonra / tavan 2'de 3. çağrı", "%d/%d/%d/%d" % (ky, kb, hizli, tavan),
           ky == 1 and kb == 1 and hizli == 5 and tavan == 4 and "bekle_sn" in oh),
          ("1. ve 2. çağrı, ertesi gün sayaç sıfır", "%d/%d/%d" % (a1, a2, ertesi), a1 == a2 == ertesi == 0))


def test3():
    db = yeni_db()
    kos("kuyruk.py", "uret", "--db", db, "--pazar", "US", "--nis", "evcil,mutfak")
    b, ob, kid = al_isle(db, v("ornek_mcp_bozuk.json"), "2026-11-18T10:00:00")
    durum = sorgu(db, "SELECT durum, deneme FROM kuyruk WHERE id=?", kid)[0]
    kilit, _ = kos("kuyruk.py", "al", "--db", db, "--yol", "mcp", zaman="2026-11-18T11:00:00")
    yok, _ = kos("toplanan_isle.py", "mcp", "--db", db, "--id", kid, v("yok.json"), zaman="2026-11-18T11:00:00")
    e, _, kid2 = al_isle(db, v("ornek_mcp_US_evcil.json"), "2026-11-19T09:00:00")
    kayit(3, "Bozuk JSON → hata + gün kilidi",
          ("yarım JSON / aynı gün al / yok dosya", "%d/%d/%d · kuyruk=%s" % (b, kilit, yok, tuple(durum)),
           b == 1 and kilit == 3 and yok != 0 and tuple(durum) == ("hata", 1)),
          ("ertesi gün kaldığı yerden", "%d (id %s)" % (e, kid2), e == 0))


def test4():
    db = yeni_db()
    kos("kuyruk.py", "uret", "--db", db, "--pazar", "US,DE", "--nis", "evcil")
    e1, o1, kid = al_isle(db, v("ornek_mcp_engel.json"), "2026-11-18T10:00:00")
    kilit, _ = kos("kuyruk.py", "al", "--db", db, "--yol", "mcp", zaman="2026-11-18T12:00:00")
    db2 = yeni_db()
    kos("kuyruk.py", "uret", "--db", db2, "--pazar", "US", "--nis", "evcil")
    e2, _, _ = al_isle(db2, v("ornek_mcp_engel_metin.json"), "2026-11-18T10:00:00")
    db3 = yeni_db()
    kos("kuyruk.py", "uret", "--db", db3, "--pazar", "US", "--nis", "evcil")
    kos("kuyruk.py", "al", "--db", db3, "--yol", "mcp")
    elle, _ = kos("kuyruk.py", "engel", "--db", db3, "--yol", "mcp", "--id", "1", "--sebep", "ekranda sınır uyarısı")
    k3, _ = kos("kuyruk.py", "al", "--db", db3, "--yol", "mcp", zaman="2026-11-18T13:00:00")
    g, og, kid2 = al_isle(db, v("ornek_mcp_US_evcil.json"), "2026-11-19T09:00:00")
    ayni = kid2 == kid
    kayit(4, "Engel izi → çıkış 3 + kilit",
          ("error(#613) / metin 'Too many' / elle engel → sonra al", "%d/%d/%d→%d · aynı gün al %d" % (e1, e2, elle, k3, kilit),
           e1 == 3 and e2 == 3 and elle == 3 and k3 == 3 and kilit == 3),
          ("ertesi gün engelli sorgu yeniden denenir", "%d · aynı id=%s" % (g, ayni), g == 0 and ayni))


def test5():
    db = yeni_db()
    kos("kuyruk.py", "uret", "--db", db, "--pazar", "US", "--nis", "evcil,mutfak")
    kayitsiz, _ = kos("toplanan_isle.py", "mcp", "--db", db, "--id", "1", v("ornek_mcp_US_evcil.json"))
    a1, _, _ = al_isle(db, v("ornek_mcp_US_evcil.json"), "2026-11-18T10:00:00")
    a2, _, _ = al_isle(db, v("ornek_mcp_US_mutfak.json"), "2026-11-18T10:00:30")
    tekrar, _ = kos("toplanan_isle.py", "mcp", "--db", db, "--id", "1", v("ornek_mcp_US_evcil.json"), zaman="2026-11-18T10:01:00")
    n = sorgu(db, "SELECT COUNT(*) FROM reklam")[0][0]
    gun = sorgu(db, "SELECT yayin_tarihi FROM reklam WHERE ad_id='900000000000001'")[0][0]
    kayit(5, "Kayıtsız çağrı reddi + tekilleştirme",
          ("açılmamış sorgu / tamamlanmış sorguyu yeniden işle", "%d/%d" % (kayitsiz, tekrar), kayitsiz == 1 and tekrar == 1),
          ("6+4 reklam, 1 ortak id → 9 tekil, epoch→ISO", "%d/%d · %d · %s" % (a1, a2, n, gun), a1 == a2 == 0 and n == 9 and gun == "2026-08-01"))


class _Sunucu(http.server.BaseHTTPRequestHandler):
    yanit = {}

    def do_GET(self):  # noqa: N802
        alan = self.path.strip("/").split("/")[0]
        SAYAC[alan] = SAYAC.get(alan, 0) + 1
        kod, bas, govde = self.yanit.get(alan, [404, {}, "yok"])
        self.send_response(kod)
        for k, x in bas.items():
            self.send_header(k, x)
        self.end_headers()
        self.wfile.write(govde.encode("utf-8"))

    def log_message(self, *a):
        pass


def sunucu_ac():
    with open(v("ornek_shopify_yanitlari.json"), encoding="utf-8") as f:
        _Sunucu.yanit = json.load(f)
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Sunucu)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s, {"REKLAMAVI_SHOPIFY_TABAN": "http://127.0.0.1:%d/{alan}" % s.server_address[1]}


def test6():
    SAYAC.clear()
    s, env = sunucu_ac()
    try:
        db = yeni_db()
        kos("kuyruk.py", "uret", "--db", db, "--pazar", "US", "--nis", "evcil,mutfak")
        al_isle(db, v("ornek_mcp_US_evcil.json"), "2026-11-18T10:00:00")
        al_isle(db, v("ornek_mcp_US_mutfak.json"), "2026-11-18T10:00:30")
        bozuk_alan, _ = kos("shopify_kontrol.py", "alan-ekle", "--db", db, "--page-id", "1", "--alan", "bu bir alan değil")
        bozuk_pid, _ = kos("shopify_kontrol.py", "alan-ekle", "--db", db, "--page-id", "abc", "--alan", "a.example")
        kos("shopify_kontrol.py", "alan-ekle", "--db", db, "--dosya", v("ornek_sayfa_alan.tsv"))
        k1, o1 = kos("shopify_kontrol.py", "kontrol", "--db", db, "--bekle", "0", env_ek=env)
        ilk = dict(SAYAC)
        k2, o2 = kos("shopify_kontrol.py", "kontrol", "--db", db, "--bekle", "0", env_ek=env)
        ikinci_ek = {a: SAYAC[a] - ilk.get(a, 0) for a in SAYAC if SAYAC[a] - ilk.get(a, 0)}
        er = sorgu(db, "SELECT durum, ertele_bitis FROM magaza WHERE alan='mutfaktr-ornek.example'")
        amazon = sorgu(db, "SELECT shopify, istek_sayisi FROM magaza WHERE alan='amazon.com'")
        shp = dict(sorgu(db, "SELECT alan, shopify FROM magaza"))
        yas = sorgu(db, "SELECT yas_gun, urun_sayisi FROM magaza WHERE alan='patili-ornek.example'")[0]
        # 3× 429 → koşu durur
        db2 = yeni_db()
        for i, a in enumerate(["korumali-ornek.example", "sinir1-ornek.example", "sinir2-ornek.example",
                               "sinir3-ornek.example", "zz-son-ornek.example"]):
            kos("shopify_kontrol.py", "alan-ekle", "--db", db2, "--page-id", str(500 + i), "--alan", a)
        k3, o3 = kos("shopify_kontrol.py", "kontrol", "--db", db2, "--bekle", "0", env_ek=env)
        son = SAYAC.get("zz-son-ornek.example", 0)
        korumali = sorgu(db2, "SELECT durum FROM magaza WHERE alan='korumali-ornek.example'")
        kirma_ok = bozuk_alan == 1 and bozuk_pid == 1 and k3 == 3 and son == 0 and korumali == [("hata",)]
        gecis_ok = (k1 == 0 and k2 == 0 and not ikinci_ek and all(x == 1 for x in ilk.values()) and
                    er and er[0][0] == "ertelendi" and er[0][1] > "2026-11-19" and amazon == [(0, 0)] and
                    shp.get("patili-ornek.example") == 1 and shp.get("blog-ornek.example") == 0 and
                    shp.get("yasli-ornek.example") == 1 and yas == (121, 2))
        kayit(6, "Shopify: tek istek + önbellek + 429",
              ("bozuk alan / bozuk page_id / 403 + 3×429 → dur (sonraki alana istek?)", "%d/%d/%d · 403=%s · sonraki istek=%d" % (bozuk_alan, bozuk_pid, k3, korumali, son), kirma_ok),
              ("1. koşu her alana 1 istek, 2. koşu 0 istek, 429 ertelendi, amazon istek yok, yaş 121 gün",
               "%d/%d · 2. koşu ek istek=%s · %s" % (k1, k2, ikinci_ek or 0, yas), gecis_ok))
    finally:
        s.shutdown()


def pilot(env):
    """US/DE/TR × evcil/mutfak — 6 MCP sorgusu + 1 Chrome dökümü."""
    db = yeni_db()
    kos("kuyruk.py", "uret", "--db", db, "--pazar", "US,DE,TR", "--nis", "evcil,mutfak")
    dosya = {("US", "evcil"): "US_evcil", ("US", "mutfak"): "US_mutfak", ("DE", "evcil"): "DE_evcil",
             ("DE", "mutfak"): "DE_mutfak", ("TR", "evcil"): "TR_evcil", ("TR", "mutfak"): "TR_mutfak"}
    kodlar = []
    for i in range(6):
        zaman = "2026-11-18T10:%02d:%02d" % (i // 2, (i % 2) * 30)
        k, out = kos("kuyruk.py", "al", "--db", db, "--yol", "mcp", zaman=zaman)
        if k != 0:
            kodlar.append(k)
            continue
        q = json.loads(out)
        k2, _ = kos("toplanan_isle.py", "mcp", "--db", db, "--id", q["id"],
                    v("ornek_mcp_%s.json" % dosya[(q["pazar"], q["nis"])]), zaman=zaman)
        kodlar.append(k2)
    kodlar.append(kos("toplanan_isle.py", "chrome", "--db", db, v("ornek_chrome_TR_evcil-1.txt"))[0])
    kodlar.append(kos("shopify_kontrol.py", "alan-ekle", "--db", db, "--dosya", v("ornek_sayfa_alan.tsv"))[0])
    kodlar.append(kos("shopify_kontrol.py", "kontrol", "--db", db, "--bekle", "0", env_ek=env)[0])
    cikti = os.path.dirname(db)
    kp, op = kos("basari_puani.py", "hesapla", "--db", db, "--pazar", "US,DE,TR", "--en-iyi", "300", "--cikti", cikti)
    kodlar.append(kp)
    return db, cikti, kodlar, op


def test7_9():
    SAYAC.clear()
    s, env = sunucu_ac()
    try:
        bozuk, _ = kos("basari_puani.py", "hesapla", "--db", yeni_db(), "--pazar", "XX")
        bozuk2, _ = kos("basari_puani.py", "hesapla", "--db", yeni_db(), "--en-iyi", "0")
        db, cikti, kodlar, op = pilot(env)
        derin = sorgu(db, "SELECT pazar, alan, puan, sira FROM puan WHERE derin=1 ORDER BY pazar, sira")
        derin_alan = {d[1] for d in derin}
        disari = sorgu(db, "SELECT COUNT(*) FROM puan WHERE derin=1 AND (shopify IS NULL OR shopify<>1)")[0][0]
        ust_us = [d for d in derin if d[0] == "US"][:1]
        tsv = os.path.exists(os.path.join(cikti, "derin-analiz-US.tsv"))
        ok7 = (disari == 0 and "blog-ornek.example" not in derin_alan and "amazon.com" not in derin_alan and
               "mutfaktr-ornek.example" not in derin_alan and ust_us and ust_us[0][1] == "patili-ornek.example" and tsv)
        kayit(7, "Puan: Shopify kapısı", ("geçersiz pazar / en-iyi 0", "%d/%d" % (bozuk, bozuk2), bozuk == 1 and bozuk2 == 1),
              ("derin kuyrukta yalnız shopify=1; US 1. = genç küçük mağaza", "%d dışı · US1=%s" % (disari, ust_us[0][1] if ust_us else "-"), ok7))
        n_reklam = sorgu(db, "SELECT COUNT(*) FROM reklam")[0][0]
        k_durum = sorgu(db, "SELECT durum, COUNT(*) FROM kuyruk GROUP BY durum")
        ok9 = all(k == 0 for k in kodlar) and n_reklam == 16 and dict(k_durum).get("tamam") == 6
        SONUC.append((9, "Pilot uçtan uca (6 MCP + 1 Chrome)", "—",
                      "al/işle×6 → chrome → alan → kontrol → puan: %s · %d reklam · kuyruk %s · derin %d"
                      % ("/".join(str(k) for k in kodlar), n_reklam, dict(k_durum), len(derin)),
                      "GEÇTİ" if ok9 else "DÜŞTÜ", op.replace("\n", " | ")[:300]))
        test8(db)
    finally:
        s.shutdown()


def test8(db):
    yok, _ = kos("analiz_db_aktar.py", "--db", db, "--analiz-modul", "/yok/db.py", "--analiz-db", os.path.join(os.path.dirname(db), "a.db"))
    modul = os.environ.get("REKLAMAVI_ANALIZ_MODUL")
    if not modul or not os.path.exists(modul):
        SONUC.append((8, "Adaptör (analiz DB)", "modül yok → %d" % yok, "—", "ATLANDI" if yok == 4 else "DÜŞTÜ",
                      "REKLAMAVI_ANALIZ_MODUL verilmedi; yazma sınanmadı"))
        return
    hedef = os.path.join(os.path.dirname(db), "analiz-test.db")
    d, od = kos("analiz_db_aktar.py", "--db", db, "--analiz-modul", modul, "--analiz-db", hedef, "--deneme")
    g, og = kos("analiz_db_aktar.py", "--db", db, "--analiz-modul", modul, "--analiz-db", hedef)
    g2, _ = kos("analiz_db_aktar.py", "--db", db, "--analiz-modul", modul, "--analiz-db", hedef)
    n = sorgu(hedef, "SELECT COUNT(*) FROM video WHERE kaynak_yontemi='meta-reklam-kutuphanesi'")[0][0] if os.path.exists(hedef) else -1
    h = sorgu(hedef, "SELECT COUNT(*) FROM hesap WHERE platform='facebook'")[0][0] if os.path.exists(hedef) else -1
    beklenen = sorgu(db, "SELECT COUNT(*) FROM puan WHERE derin=1")[0][0]
    kayit(8, "Adaptör (analiz DB)", ("modül yok", yok, yok == 4),
          ("deneme → yaz → tekrar yaz (idempotent)", "%d/%d/%d · %d hesap · %d video" % (d, g, g2, h, n),
           d == 0 and g == 0 and g2 == 0 and h == beklenen and n > 0), og[:120])


def main():
    for tt in (test1, test2, test3, test4, test5, test6, test7_9):
        try:
            tt()
        except Exception as e:
            SONUC.append((tt.__name__, tt.__name__, "—", "—", "DÜŞTÜ", "istisna: %r" % e))
    SONUC.sort(key=lambda s: str(s[0]))
    print("| # | Test | Kırma (beklenen → görülen) | Geçiş (beklenen → görülen) | Sonuç | Not |")
    print("|---|---|---|---|---|---|")
    for s in SONUC:
        print("| %s | %s | %s | %s | %s | %s |" % s)
    dusen = [s for s in SONUC if s[4] == "DÜŞTÜ"]
    print("\n%d test · geçti %d · düştü %d · atlandı %d" % (len(SONUC), sum(1 for s in SONUC if s[4] == "GEÇTİ"),
                                                          len(dusen), sum(1 for s in SONUC if s[4] == "ATLANDI")))
    sys.exit(1 if dusen else 0)


if __name__ == "__main__":
    main()
