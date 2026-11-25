#!/usr/bin/env python3
"""excel_yaz.py kırma testleri. Kullanım: python3 excel_test.py → hepsi geçerse 0, biri tutmazsa 1, openpyxl yoksa 3.

Her red önce bozuk girdiyle ≠ 0 görülür; doğru girdi ayrıca ayrı bir okuyucu (openpyxl) ile yeniden ölçülür.
"""
import os
import subprocess
import sys
import tempfile

try:
    from openpyxl import load_workbook
except ImportError:
    # Sistem Python'unda openpyxl yoksa ayrı, sürümü sabit sanal ortamda (arac-ekle kapısı: openpyxl==3.1.5, yalnız PyPI; global kurulum yok)
    # koşar: test GERÇEKTEN ölçülür. Ortam da yoksa "ölçülemedi" (çıkış 3), geçti sayılmaz.
    _VENV = os.path.join(os.path.expanduser("~"), ".local", "share", "viral-urun-ekibi", "excel-venv", "bin", "python")
    if os.environ.get("EXCEL_TEST_VENV") != "1" and os.path.isfile(_VENV):
        os.environ["EXCEL_TEST_VENV"] = "1"
        sys.exit(subprocess.call([_VENV, os.path.abspath(__file__)] + sys.argv[1:]))
    print("HATA: openpyxl yok (sistem Python'u ve excel-venv). ÖLÇÜLEMEDİ, geçti sayılmaz. Kur (ayrı ortam, sürüm sabit):\n"
          "  python3 -m venv ~/.local/share/viral-urun-ekibi/excel-venv && ~/.local/share/viral-urun-ekibi/excel-venv/bin/python -m pip install --only-binary=:all: openpyxl==3.1.5 et-xmlfile==2.0.0")
    sys.exit(3)

BURADA = os.path.dirname(os.path.abspath(__file__))
BETIK = os.path.join(BURADA, "excel_yaz.py")
BASLIK = "urun\tlink\tilgi\tilgi_sayi\talis\tsatis\tpara\tmarj_kat\tkarar\tneden\tkaynak\ttarih"
SATIR_SAT = "Tırnak makası\thttps://www.trendyol.com/x\t243 yorum · 4,3\t243\t170\t399\tTRY\t2,35\tSAT\tTalep var, viral değil.\tTrendyol\t2026-11-23"
SATIR_IZLE = "Mini ütü\thttps://www.trendyol.com/y\t969 yorum · 4,1\t969\t210\t399,9\tTRY\t\tİZLE\tKanıt eksik.\tTrendyol\t2026-11-23"
SATIR_ELE = "Mantar lamba\thttps://www.trendyol.com/z\t10.314 yorum · 4,5\t10314\t\t\t\t\tELE\tDoygun pazar.\tTrendyol\t2026-11-23"

sonuclar = []


def kos(args, hedef):
    return subprocess.run([sys.executable, BETIK] + args, capture_output=True, text=True, cwd=hedef)


def yaz(klasor, ad, metin):
    p = os.path.join(klasor, ad)
    with open(p, "w", encoding="utf-8") as f:
        f.write(metin)
    return p


def bekle(ad, r, beklenen, parca=None):
    ok = r.returncode == beklenen and (parca is None or parca in (r.stdout + r.stderr))
    sonuclar.append(ok)
    print(("GEÇTİ " if ok else "KALDI ") + "%s → çıkış %d (beklenen %d)%s" % (
        ad, r.returncode, beklenen, "" if ok else " | " + (r.stdout + r.stderr).strip()[:200]))
    return ok


def kontrol(ad, ok, ayrinti=""):
    sonuclar.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad + ("" if ok else " | " + str(ayrinti)))


def main():
    with tempfile.TemporaryDirectory(prefix="excel_test_") as d:
        cikti = os.path.join(d, "o.xlsx")

        def calistir(ad, metin, beklenen, ek=None, parca=None, kaynak="trendyol"):
            if os.path.exists(cikti):
                os.remove(cikti)
            tsv = yaz(d, "u.tsv", metin)
            r = kos(["--urunler", tsv, "--kaynak", kaynak, "--cikti", cikti] + (ek or []), d)
            bekle(ad, r, beklenen, parca)
            if beklenen != 0:
                kontrol("  ↳ %s: reddedilince dosya yazılmadı" % ad, not os.path.exists(cikti))
            return r

        iyi = BASLIK + "\n" + "\n".join([SATIR_ELE, SATIR_IZLE, SATIR_SAT]) + "\n"

        # --- redler (önce kırmızı) ---
        calistir("geçersiz karar (AL)", BASLIK + "\n" + SATIR_SAT.replace("\tSAT\t", "\tAL\t") + "\n", 1, parca="karar")
        calistir("11 alanlı başlık", BASLIK.rsplit("\t", 1)[0] + "\n" + SATIR_SAT + "\n", 1, parca="başlık")
        calistir("başlık sırası değişik", BASLIK.replace("urun\tlink", "link\turun") + "\n" + SATIR_SAT + "\n", 1, parca="başlık")
        calistir("141 karakterlik neden", BASLIK + "\n" + SATIR_SAT.replace("Talep var, viral değil.", "x" * 141) + "\n", 1, parca="141")
        calistir("bozuk tarih (23.11.2026)", BASLIK + "\n" + SATIR_SAT.replace("2026-11-23", "23.11.2026") + "\n", 1, parca="tarih")
        calistir("olmayan gün (2026-13-45)", BASLIK + "\n" + SATIR_SAT.replace("2026-11-23", "2026-13-45") + "\n", 1, parca="tarih")
        calistir("boş girdi (yalnız başlık, 0 ürün)", BASLIK + "\n", 1, parca="0 ürün")
        calistir("tamamen boş dosya", "", 1)
        calistir("geçersiz para (TL)", BASLIK + "\n" + SATIR_SAT.replace("\tTRY\t", "\tTL\t") + "\n", 1, parca="para")
        calistir("link http ile başlamıyor", BASLIK + "\n" + SATIR_SAT.replace("https://www.trendyol.com/x", "www.trendyol.com/x") + "\n", 1, parca="link")
        calistir("sayı olmayan alış", BASLIK + "\n" + SATIR_SAT.replace("\t170\t", "\tonyetmis\t") + "\n", 1, parca="alis")
        calistir("boş ürün adı", BASLIK + "\n" + SATIR_SAT.replace("Tırnak makası", "") + "\n", 1, parca="urun")

        # kullanım hatası
        r = kos(["--urunler", os.path.join(d, "yok.tsv"), "--kaynak", "yanlis", "--cikti", cikti], d)
        bekle("geçersiz --kaynak → kullanım hatası", r, 2)
        r = kos(["--urunler", os.path.join(d, "yok.tsv"), "--kaynak", "trendyol", "--cikti", cikti], d)
        bekle("olmayan girdi dosyası", r, 1, "yok")

        # openpyxl yok → 3 (içe aktarma engellenerek)
        tsv = yaz(d, "u.tsv", iyi)
        kod = ("import sys, runpy; sys.modules['openpyxl'] = None; "
               "sys.argv = ['excel_yaz.py', '--urunler', %r, '--kaynak', 'trendyol', '--cikti', %r]; "
               "runpy.run_path(%r, run_name='__main__')") % (tsv, cikti, BETIK)
        r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True)
        bekle("openpyxl yok → çıkış 3 ve kurulum komutu", r, 3, "pip install")

        # --- doğru girdi: çıkış 0 ve 6 ölçüm (ayrı okuyucuyla) ---
        r = calistir("doğru girdi (3 ürün)", iyi, 0, parca="TAMAM", kaynak="radar")
        kontrol("  ↳ özet satırı: 3 ürün (SAT 1 / İZLE 1 / ELE 1)", "3 ürün (SAT 1 / İZLE 1 / ELE 1)" in r.stdout, r.stdout)
        wb = load_workbook(cikti)
        ws = wb["Ürünler"]
        kontrol("  ↳ ölçüm 1: sayfa adları tam", wb.sheetnames == ["Ürünler", "Ayrıntı", "Nasıl okunur"], wb.sheetnames)
        kontrol("  ↳ ölçüm 2: Ürünler max_column == 10", ws.max_column == 10, ws.max_column)
        kontrol("  ↳ ölçüm 3: veri satırı = girdi satırı (3)", ws.max_row - 1 == 3, ws.max_row)
        kontrol("  ↳ ölçüm 4: birleştirilmiş hücre 0", sum(len(w.merged_cells.ranges) for w in wb.worksheets) == 0)
        kontrol("  ↳ ölçüm 5: freeze_panes == A2", ws.freeze_panes == "A2", ws.freeze_panes)
        kontrol("  ↳ ölçüm 6: auto_filter dolu (A1:J4)", ws.auto_filter.ref == "A1:J4", ws.auto_filter.ref)
        kontrol("  ↳ sıralama SAT, İZLE, ELE", [ws.cell(i, 7).value for i in (2, 3, 4)] == ["SAT", "İZLE", "ELE"],
                [ws.cell(i, 7).value for i in (2, 3, 4)])
        kontrol("  ↳ karar renkleri C6EFCE / FFEB9C / FFC7CE",
                [ws.cell(i, 7).fill.fgColor.rgb[-6:] for i in (2, 3, 4)] == ["C6EFCE", "FFEB9C", "FFC7CE"],
                [ws.cell(i, 7).fill.fgColor.rgb for i in (2, 3, 4)])
        kontrol("  ↳ link: hücre metni 'aç', köprü tam URL", ws.cell(2, 2).value == "aç" and ws.cell(2, 2).hyperlink.target == "https://www.trendyol.com/x")
        kontrol("  ↳ başlık satırı kalın, beyaz yazı, zemin 1F2937",
                ws.cell(1, 1).font.bold and ws.cell(1, 1).fill.fgColor.rgb[-6:] == "1F2937")
        kontrol("  ↳ Nasıl okunur ≤ 12 satır + başlık", wb["Nasıl okunur"].max_row <= 13, wb["Nasıl okunur"].max_row)
        kontrol("  ↳ para biçimi TRY (₺) ve marj biçimi ×", "₺" in ws.cell(2, 4).number_format and ws.cell(2, 6).number_format == '0.0"×"',
                (ws.cell(2, 4).number_format, ws.cell(2, 6).number_format))

        # ondalık virgül
        kontrol("  ↳ ondalık virgül: marj '2,35' → 2.35", abs(ws.cell(2, 6).value - 2.35) < 1e-9, ws.cell(2, 6).value)
        kontrol("  ↳ ondalık virgül: satış '399,9' → 399.9", abs(ws.cell(3, 5).value - 399.9) < 1e-9, ws.cell(3, 5).value)
        kontrol("  ↳ boş alış/satış hücresi boş kaldı (ELE satırı)", ws.cell(4, 4).value is None and ws.cell(4, 5).value is None)

        # sınır: tam 140 karakter kabul
        calistir("140 karakterlik neden kabul", BASLIK + "\n" + SATIR_SAT.replace("Talep var, viral değil.", "x" * 140) + "\n", 0)

        # ayrıntı .md (ilk Markdown tablosu)
        md = yaz(d, "ham.md", "Önsöz\n\n| ad | puan |\n|---|---|\n| a | 1 |\n| b | 2 |\n\nSonra\n\n| baska | tablo |\n|---|---|\n| x | y |\n")
        calistir("ayrıntı .md → ilk tablo", iyi, 0, ek=["--ayrinti", md])
        wa = load_workbook(cikti)["Ayrıntı"]
        kontrol("  ↳ Ayrıntı: ilk tablo (3 satır × 2 sütun), ikinci tablo yok",
                [[c.value for c in r] for r in wa.iter_rows()] == [["ad", "puan"], ["a", "1"], ["b", "2"]],
                [[c.value for c in r] for r in wa.iter_rows()])
        kontrol("  ↳ Ayrıntı dondurulmuş ve filtreli", wa.freeze_panes == "A2" and bool(wa.auto_filter.ref))

        # ayrıntı .tsv ve birden çok ham dosya uyarısı
        ham_tsv = yaz(d, "ham.tsv", "a\tb\n1\t2\n")
        ham2 = yaz(d, "ham2.tsv", "c\n9\n")
        r = calistir("iki ham tablo → ilki yazılır, uyarı basılır", iyi, 0, ek=["--ayrinti", ham_tsv, "--ayrinti", ham2], parca="UYARI")
        wa = load_workbook(cikti)["Ayrıntı"]
        kontrol("  ↳ yalnız ilk ham tablo yazıldı", [[c.value for c in r] for r in wa.iter_rows()] == [["a", "b"], ["1", "2"]])

        # --kopya
        kopya = os.path.join(d, "masaustu")
        calistir("--kopya klasörü", iyi, 0, ek=["--kopya", kopya])
        kontrol("  ↳ kopya dosyası yazıldı", os.path.isfile(os.path.join(kopya, "o.xlsx")))

        # SAT (koşullu) ayrı sınıf DEĞİL (kurucu kararı 2026-11-25): girdide görülürse SAT olur, eksik kanıt "Kontrol et" notu
        kosullu = BASLIK + "\n" + SATIR_SAT.replace("\tSAT\t", "\tSAT (koşullu)\t") + "\n"
        calistir("SAT (koşullu) eski yazımı kabul", kosullu, 0)
        kontrol("  ↳ Ürünler: karar hücresi 'SAT' (koşullu sınıfı yok)",
                any(c.value == "SAT" for r in load_workbook(cikti)["Ürünler"].iter_rows() for c in r)
                and not any(c.value == "SAT (koşullu)" for r in load_workbook(cikti)["Ürünler"].iter_rows() for c in r))

        # skeptic eski yazımı `SAT-KOŞULLU: <eksik>` SAT + "Kontrol et" notu olur; uydurma değer reddedilir
        alias = BASLIK + "\n" + SATIR_SAT.replace("\tSAT\t", "\tSAT-KOŞULLU: numune\t").replace("Talep var, viral değil.", "") + "\n"
        calistir("SAT-KOŞULLU: numune (eski yazım)", alias, 0)
        kontrol("  ↳ Ürünler: karar 'SAT', neden 'Kontrol et: numune'",
                any(c.value == "SAT" for r in load_workbook(cikti)["Ürünler"].iter_rows() for c in r)
                and any(c.value == "Kontrol et: numune" for r in load_workbook(cikti)["Ürünler"].iter_rows() for c in r))
        calistir("kırma: karar 'SAT-KOŞUL' (uydurma) -> 1", BASLIK + "\n" + SATIR_SAT.replace("\tSAT\t", "\tSAT-KOŞUL\t") + "\n", 1)

        # --kopya DOSYA yolu: klasör değil dosya olarak yazılmalı (0.4.x hatası: dosya adıyla klasör açıyordu)
        kopya_dosya = os.path.join(d, "masaustu2", "Teslim Listesi.xlsx")
        calistir("--kopya dosya yolu", iyi, 0, ek=["--kopya", kopya_dosya])
        kontrol("  ↳ kopya bir DOSYA (klasör değil)", os.path.isfile(kopya_dosya))

        # her kaynak adı çalışır
        for k in ("radar", "spy", "aliexpress", "trendyol"):
            calistir("kaynak %s" % k, iyi, 0, kaynak=k)
            kontrol("  ↳ %s: Nasıl okunur 'İlgi tanımı' satırı var" % k,
                    any(row[0].value == "İlgi tanımı (bu dosya)" for row in load_workbook(cikti)["Nasıl okunur"].iter_rows()))

        # yalnız SAT kullanıcı sayfası: gizli Ayrıntı + boş Ürünler (hunter: aliexpress/trendyol)
        ham = yaz(d, "ham2.tsv", "ad\tkarar\nx\tELE\n")
        calistir("hunter: --ayrinti-gizli → Ayrıntı gizli", BASLIK + "\n" + SATIR_SAT + "\n", 0, ek=["--ayrinti", ham, "--ayrinti-gizli"], kaynak="aliexpress")
        wb = load_workbook(cikti)
        kontrol("  ↳ Ayrıntı sayfası gizli, Ürünler görünür", wb["Ayrıntı"].sheet_state == "hidden" and wb["Ürünler"].sheet_state == "visible",
                (wb["Ayrıntı"].sheet_state, wb["Ürünler"].sheet_state))
        r = calistir("hunter özet satırı: '1 SAT' (İZLE/ELE sayısı yok)", BASLIK + "\n" + SATIR_SAT + "\n", 0, parca="1 SAT", kaynak="aliexpress")
        kontrol("  ↳ hunter özetinde İZLE/ELE yok", "İZLE" not in r.stdout and "ELE" not in r.stdout, r.stdout)
        calistir("0 SAT: --bos-izinli olmadan reddedilir", BASLIK + "\n", 1, parca="0 ürün", kaynak="trendyol")
        calistir("0 SAT: --bos-izinli ile Ürünler boş yazılır", BASLIK + "\n", 0, ek=["--bos-izinli", "--ayrinti-gizli"], parca="0 SAT", kaynak="trendyol")
        kontrol("  ↳ Ürünler yalnız başlık satırı", load_workbook(cikti)["Ürünler"].max_row == 1, load_workbook(cikti)["Ürünler"].max_row)

    kalan = sonuclar.count(False)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuclar), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
