"""Shopify reklam toplayıcı — ortak SQLite deposu (yalnız stdlib).

Tek dosya: `reklam.db` (varsayılan `is/meta/reklam.db`). Tablolar:
  kuyruk   — niş × pazar sorgusu ve durumu (bekliyor/acik/tamam/engel/hata)
  cagri    — her alınan sorgu (günlük tavan + bekleme bu tablodan sayılır)
  kilit    — gün + yol (mcp/chrome) kilidi: engel/hata görülünce o gün o yol DURUR
  reklam   — reklam (ad_id ile tekil)
  sayfa_alan — Facebook sayfası → hedef alan adı (Chrome dökümünden ya da elle)
  magaza   — alan adı başına TEK Shopify kontrolü (önbellek)
  puan     — basari_puani.py çıktısı; derin=1 olanlar derin analiz kuyruğu
Alan adları kullanıcı projesindeki analiz veritabanı modülüyle (`<proje>/veri/db.py`) uyumlu tutulur (pazar, nis, okuma_tarihi, yayin_tarihi, kaynak_ref);
o veritabanına yazmak `analiz_db_aktar.py` adaptörünün işidir.
"""
import datetime as dt
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

PAZARLAR = ["US", "TR", "GB", "DE", "FR", "ES", "IT", "NL"]
# proje analiz veritabanı pazar sözlüğü: TR/ABD/AB/UK
PAZAR_ANALIZ = {"US": "ABD", "TR": "TR", "GB": "UK", "DE": "AB", "FR": "AB", "ES": "AB", "IT": "AB", "NL": "AB"}
YOLLAR = ["mcp", "chrome"]

# ---- Hız kuralları (varsayılan; --tavan / --bekle ile DÜŞÜRÜLEBİLİR, yükseltme kurucu kararıdır) ----
TAVAN = {"mcp": 150, "chrome": 30}         # günlük sorgu tavanı
BEKLE_SN = {"mcp": 20, "chrome": 15}       # iki sorgu arası en az
HATA_DENEME = 3                             # aynı sorgu en çok 3 kez 'hata' alır, sonra elle bakılır
SHOPIFY_BEKLE_SN = 10                       # iki alan adı isteği arası en az
SHOPIFY_ERTELE_SAAT = 24                    # 429 / zaman aşımı → bu kadar ertele (Retry-After daha uzunsa o)
SHOPIFY_429_DUR = 3                         # bir koşuda bu kadar 429 → koşu DURUR (çıkış 3)

SEMA = """
CREATE TABLE IF NOT EXISTS kuyruk(
  id INTEGER PRIMARY KEY,
  pazar TEXT NOT NULL, nis TEXT NOT NULL, aile TEXT NOT NULL, sorgu TEXT NOT NULL, yol TEXT NOT NULL,
  dil TEXT NOT NULL DEFAULT 'yerel',
  oncelik INTEGER NOT NULL DEFAULT 100,
  durum TEXT NOT NULL DEFAULT 'bekliyor' CHECK(durum IN ('bekliyor','acik','tamam','engel','hata')),
  deneme INTEGER NOT NULL DEFAULT 0,
  son_tarih TEXT, tahmini_toplam INTEGER, gelen INTEGER, dosya TEXT, notlar TEXT,
  UNIQUE(pazar, nis, aile, sorgu, yol)
);
CREATE TABLE IF NOT EXISTS cagri(
  id INTEGER PRIMARY KEY, tarih TEXT NOT NULL, zaman TEXT NOT NULL, yol TEXT NOT NULL, kuyruk_id INTEGER
);
CREATE TABLE IF NOT EXISTS kilit(
  tarih TEXT NOT NULL, yol TEXT NOT NULL, sebep TEXT NOT NULL, zaman TEXT NOT NULL, PRIMARY KEY(tarih, yol)
);
CREATE TABLE IF NOT EXISTS reklam(
  ad_id TEXT PRIMARY KEY,
  page_id TEXT, page_name TEXT, pazar TEXT NOT NULL, nis TEXT, sorgu TEXT,
  baslik TEXT, govde TEXT,
  olusturma TEXT, yayin_tarihi TEXT, snapshot_url TEXT,
  hedef_alan TEXT, hedef_yol TEXT, kopya INTEGER,
  kaynak TEXT NOT NULL, kuyruk_id INTEGER,
  ilk_gorulme TEXT NOT NULL, okuma_tarihi TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_reklam_page ON reklam(pazar, page_id);
CREATE INDEX IF NOT EXISTS ix_reklam_alan ON reklam(hedef_alan);
CREATE TABLE IF NOT EXISTS sayfa_alan(
  page_id TEXT PRIMARY KEY, alan TEXT NOT NULL, kaynak TEXT NOT NULL, tarih TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS magaza(
  alan TEXT PRIMARY KEY,
  durum TEXT NOT NULL CHECK(durum IN ('bekliyor','tamam','ertelendi','hata')),
  shopify INTEGER,              -- 1 / 0 / NULL (bilinmiyor)
  kanit TEXT, http_kodu INTEGER, urun_sayisi INTEGER, en_eski_urun TEXT, yas_gun INTEGER,
  istek_sayisi INTEGER NOT NULL DEFAULT 0, son_istek TEXT, ertele_bitis TEXT, nihai_alan TEXT
);
CREATE TABLE IF NOT EXISTS puan(
  pazar TEXT NOT NULL, birim TEXT NOT NULL, page_name TEXT, alan TEXT, nis TEXT,
  puan INTEGER NOT NULL, gerekce TEXT NOT NULL, shopify INTEGER, derin INTEGER NOT NULL DEFAULT 0,
  sira INTEGER, tarih TEXT NOT NULL,
  PRIMARY KEY(pazar, birim)
);
"""


def simdi():
    return o.bugun()


def bugun_str():
    return simdi().date().isoformat()


def baglan(yol):
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    c = sqlite3.connect(yol)
    c.row_factory = sqlite3.Row
    c.executescript(SEMA)
    return c


def kilitli_mi(c, yol, tarih=None):
    r = c.execute("SELECT sebep FROM kilit WHERE tarih=? AND yol=?", (tarih or bugun_str(), yol)).fetchone()
    return r["sebep"] if r else None


def kilitle(c, yol, sebep):
    c.execute("INSERT OR IGNORE INTO kilit VALUES (?,?,?,?)", (bugun_str(), yol, sebep[:300], simdi().isoformat()))
    c.commit()


def epoch_tarih(v):
    """Meta MCP epoch saniyesi → ISO tarih. Sayı değilse ISO tarih kabul edilir; çözülemezse None."""
    if v is None or v == "":
        return None
    try:
        return dt.datetime.utcfromtimestamp(int(v)).date().isoformat()
    except (TypeError, ValueError, OverflowError, OSError):
        s = str(v)[:10]
        return s if o.iso_mu(s) else None


def baslik_norm(s):
    """Aynı ürün/başlığın farklı sayfalarda geçişini saymak için kaba normal form."""
    import re
    t = o.norm(s or "")
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\d+", " ", t)
    return " ".join(t.split())[:80]
