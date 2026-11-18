# -*- coding: utf-8 -*-
"""0.3.4 görsel metin + tipografi kuralları pakette duruyor mu (ilk gerçek ChatGPT koşusundan)."""
import os

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = ("skills", "gorseller", "references")


def oku(*p):
    with open(os.path.join(KOK, *p), encoding="utf-8") as f:
        return f.read()


def test_gorsele_lojistik_yazisi_yasak():
    k = oku("src", "ortak", "01-kurallar.md")
    blok = k[k.index("- Görsel metni (0.3.4"):k.index("- Bilgi notu (kullanıcının sorumluluğu; engel değil)")]
    for parca in ("ASLA yazılmaz", '"Ücretsiz kargo"', '"Kapıda ödeme"', '"%20 indirim"', '"2 yıl garanti"',
                  "kampanya", "teslimat", "DEVAM KARTI'ndaki onaylı metinlerden",
                  "[DOĞRULA] işaretli bilgi görsele yazılmaz"):
        assert parca in blok, parca
    # kural her skill'e kopyalanır (metinler dahil)
    for s in ("gorseller", "metinler", "marka"):
        assert "- Görsel metni (0.3.4" in oku("skills", s, "references", "01-kurallar.md"), s
    # prompt YASAKLAR bloğu ve kabul listesi
    p = oku(*G, "uretim-promptlari.md")
    yasak = p[p.index("**YASAKLAR.**"):p.index("**ÇIKTI (kare).**")]
    assert "'Ücretsiz kargo'" in yasak and "garanti" in yasak
    assert "Onaysız vaat" in oku(*G, "kabul-kontrolu.md")
    # eski izin geri gelmesin: görsel şablonlarında kargo güven satırı yok
    assert "Ücretsiz kargo · 14 gün iade" not in p
    assert "güven satırı" not in p.lower() and "GUVEN_SATIRI" not in p
    assert "yalnız mağaza kuralıysa" not in oku(*G, "adim-4-fotograf-plani.md")
    assert "Görsel metni" in oku("skills", "metinler", "references", "adim-6-shopify-plani.md")


def test_baslik_somut_fayda():
    k = oku("src", "ortak", "01-kurallar.md")
    for parca in ("G1 başlığı ürünün somut faydasıdır", "2–5 kelime", "Soyut sıfat yığını yok",
                  '"Kontrollü form."', '"chunker"', "o görselin gösterdiği tek şeyi söyler"):
        assert parca in k, parca
    assert "somut fayda = alıcının sonucu, 2–5 kelime" in oku(*G, "uretim-promptlari.md")


def test_hex_ve_yazi_tipi_once():
    t = oku("src", "ortak", "tasarim-dili.md")
    b = t[t.index("## 9. "):]
    assert "5 HEX" in b and "başlık yazı tipi tarifi" in b and "görsel ÜRETİLMEZ" in b
    assert "Her görsel promptunda HEX'ler" in b
    assert "Tek hiyerarşi" in b and "en fazla 1 kısa alt satır" in b
    assert "5 HEX" in oku(*G, "adim-4-fotograf-plani.md").split("4.1 Referans")[0]
    assert "5 HEX + başlık yazı tipi tarifi" in oku(*G, "adim-5-gorsel-uretimi.md")
    assert "5 HEX + başlık yazı tipi tarifi yoksa görsel üretme" in oku("skills", "gorseller", "SKILL.md")
    assert "Görsel kilidi (0.3.4)" in oku("skills", "marka", "references", "logo-renk-font.md")


def test_tek_zemin_hex():
    t = oku("src", "ortak", "tasarim-dili.md")
    b = t[t.index("## 9. "):]
    for parca in ("Tek zemin HEX'i", "TEK ve AYNI zemin HEX'ini", "`scripts/duzelt.py zemin`", "Farklı zeminli görsel RED"):
        assert parca in b, parca
    p = oku(*G, "uretim-promptlari.md")
    assert "Zemin düz {RENK_ZEMIN} (galeriyle aynı HEX)" in p          # B1 artık koyu değil
    assert "Zemin düz {RENK_METIN}. Kartlar" not in p                    # G2 koyu durak kapandı
    assert "yalnız M2 kullanılır" in p
    k = oku(*G, "kabul-kontrolu.md")
    assert "Tek zemin HEX'i (0.3.4)" in k and "farklı zemin" in k


def test_detay_etiketi_buyutec_ve_sus_cizgisi_yasak():
    k = oku("src", "ortak", "01-kurallar.md")
    assert '"DETAY 01"' in k and '"detay" kelimesi' in k and "büyüteç dairesi" in k
    p = oku(*G, "uretim-promptlari.md")
    yasak = p[p.index("**YASAKLAR.**"):p.index("**ÇIKTI (kare).**")]
    for parca in ("'DETAY 01'", "'detay' kelimesi", "büyüteç dairesi", "süs çizgisi"):
        assert parca in yasak, parca
    # şablonlarda başlık altı vurgu çizgisi kalmadı
    assert "48×4" not in p and "başlık altı kısa çizgi" not in p
    assert "büyüteç dairesi" in oku(*G, "kabul-kontrolu.md")


def test_urun_kadraji_doldurur_ve_kayma_kontrolu():
    t = oku("src", "ortak", "tasarim-dili.md")
    b = t[t.index("## 9. "):]
    for parca in ("≥ %55", "%6 kenar payı korunur", "çapraz konmaz", "en az bir değer ayrıntısı",
                  "tedarikçi fotoğrafıyla (Ref 1)", "Fark varsa RED", "kullanıcıya tek soru"):
        assert parca in b, parca
    k = oku(*G, "kabul-kontrolu.md")
    assert "%55" in k and "renk kayması" in k and "tedarikçi fotoğrafı" in k
    assert "%55" in oku(*G, "uretim-promptlari.md")
    assert "tedarikçi fotoğrafıyla (Ref 1)" in oku(*G, "adim-5-gorsel-uretimi.md")


def test_onayli_fiyat_degismez_ve_hukuk_kisiti_eklenmedi():
    c = oku("src", "ortak", "00-calisma-tarzi.md")
    assert "ONAYLI DEĞER DEĞİŞMEZ" in c and "onaylanan fiyat" in c
    # 0.3.4 kuralları kalite kuralıdır; sağlık/hukuk yasağı eklenmedi
    t = oku("src", "ortak", "tasarim-dili.md")
    b = t[t.index("## 9. "):]
    for kelime in ("sağlık", "mevzuat", "hukuk"):
        assert kelime not in b.lower(), kelime


# ---------------------------------------------------------------- 0.3.5 (test12 dersleri + Lufella sohbet incelemesi)
def test_ortak_istem_bloklari_dosyasi():
    o = oku(*G, "ortak-istem-bloklari.md")
    for parca in ("ÜRÜN KİLİDİ:", "RENK (yalnız bunlar):", "TİPOGRAFİ (bir marka sistemi", "YASAKLAR:",
                  "karakter karakter aynıdır", "{ZEMİN_HEX}", "gravürü SİL", "en az 5 parça",
                  "transparent background PNG, alfa kanallı", "32 pikselde bile okunur"):
        assert parca in o, parca
    # teste özgü ürün bloğa sızmadı (genel şablon)
    s3 = o[o.index("## 3. Blok 2"):o.index("## 4. Blok 3")]
    assert "#0F2B2E" not in s3 and "makas" not in s3
    assert "ortak-istem-bloklari.md" in oku("skills", "gorseller", "SKILL.md")
    assert "\r" not in o


def test_g1_once_ve_stil_eki():
    o = oku(*G, "ortak-istem-bloklari.md")
    assert "Önce yalnız G1 üret" in o and "Ek 2 onaylı G1" in o
    assert "Onay gelmeden başka görsel üretme" in o
    assert "ÖNCE yalnız G1 üret" in oku(*G, "adim-5-gorsel-uretimi.md")
    assert "Önce yalnız G1" in oku("skills", "gorseller", "SKILL.md")
    t = oku("src", "ortak", "tasarim-dili.md")
    assert "**G1 önce:**" in t and "ürün fotoğrafı + onaylı G1" in t
    # çapadan yalnız tipografi hiyerarşisi/boşluk; renk DEVAM KARTI'ndan
    p = oku(*G, "uretim-promptlari.md")
    assert "rengi ve ürünü ALMA: renk DEVAM KARTI'ndan" in p and "rengi ve ürünü ALMA" in o.replace("Rengi", "rengi")
    assert "kargo/iade satırını" not in p      # eski açık zeminli SESSA çapası gitti


def test_tipografi_tarifi_ve_baslik_boyu():
    for metin in (oku(*G, "ortak-istem-bloklari.md"), oku(*G, "uretim-promptlari.md")):
        for parca in ("DAR (condensed) grotesk, BÜYÜK HARF, SemiBold", "Barlow Condensed / Oswald",
                      "satır aralığı 0,95", "harf aralığı geniş (+%12)", "büyük harfte i → İ, ı → I", "serif YOK"):
            assert parca in metin, parca
    o = oku(*G, "ortak-istem-bloklari.md")
    assert "harf yüksekliği tuvalin yaklaşık %10'u" in o and "satır satır" in o
    assert "dikeyden 8–12° eğik; boyu tuval yüksekliğinin %80'i" in o
    assert "ürünün renginden OLMAZ" in o
    p = oku(*G, "uretim-promptlari.md")
    assert "cap 76 px" not in p and "Başlık küçük ve ince" not in p     # ince/küçük başlık kökü
    assert "metinsiz; metni site yazar" not in p and "sakin alan: web sitesi" not in p   # boş sol yarı kökü


def test_g2_makro_kart_ve_gosterilen_teslim():
    p = oku(*G, "uretim-promptlari.md")
    g2 = p[p.index("### G2 "):p.index("### G3 ")]
    assert "İKON YOK" in g2 and "MAKRO FOTOĞRAFI" in g2 and "üst %60" in g2
    o = oku(*G, "ortak-istem-bloklari.md")
    assert "Gösterilen görsel = teslim edilen dosya" in o and "en fazla 4 görsel" in o
    assert "YALNIZ soruyu cevapla" in o


def test_stil_capasi_yeni_kareler():
    d = os.path.join(KOK, "skills", "gorseller", "assets", "stil-capasi")
    assert sorted(os.listdir(d)) == ["b1-masaustu.jpg", "b2-mobil.jpg", "g1-poster.jpg",
                                     "g2-makro-kartlar.jpg", "g3-isaret-cizgileri.jpg"]


# ---------------------------------------------------------------- 0.3.6 (hazır istem modu; test13 = 0.3.5'in gerçek ChatGPT koşusu)
ISTEM = G + ("istemler",)
URUN_SABLONLARI = ("g0-feed.md", "g1.md", "g2.md", "g2-makro.md", "g3.md", "g4.md", "g5.md", "b1-masaustu.md", "b2-mobil.md")
GRAVUR = "gravür, üretici logosu, amblem, kazıma yazı, harf ya da rakam YOK (Ek 1'de üründe görünen küçük gravürü SİL, kopyalama)"
KILIT_SON = "Ek 1'deki yazıları, logoyu, zemin rengini, düzeni ve açıyı YOK SAY ve KOPYALAMA"


def istem_govdesi(metin):
    return metin[metin.index("=== İSTEM BAŞI ===") + len("=== İSTEM BAŞI ==="):metin.index("=== İSTEM SONU ===")]


def test_hazir_istem_sablonlari_var():
    d = os.path.join(KOK, *ISTEM)
    assert sorted(os.listdir(d)) == sorted(URUN_SABLONLARI + ("logo-ikon.md", "bos-kart.md"))
    for f in os.listdir(d):
        ham = open(os.path.join(d, f), "rb").read()
        assert b"\r" not in ham, f
        m = ham.decode("utf-8")
        assert "İstemi sen YAZMAZSIN" in m and "KELİMESİ KELİMESİNE" in m, f
        assert "Kısaltma, özetleme, yeniden yazma" in m and "YASAK" in m, f
        assert m.count("=== İSTEM BAŞI ===") == 1 and m.count("=== İSTEM SONU ===") == 1, f
        # teste özgü ürün şablona sızmadı: istem gövdesinde somut HEX ve "makas" yok
        g = istem_govdesi(m)
        assert "#0F2B2E" not in g and "makas" not in g.lower(), f


def test_her_urun_sablonunda_yer_tutucu_ve_sabit_kilit():
    import re
    bloklar = {}
    for f in URUN_SABLONLARI:
        g = istem_govdesi(oku(*ISTEM, f))
        for yt in ("{ÜRÜN_ADI_VE_ÖLÇÜ}", "{ÜRÜN_KİLİDİ_PARÇALARI}", "{ZEMİN_HEX}", "{METİN_HEX}", "{İKİNCİL_HEX}",
                   "{VURGU_HEX}", "{ÜRÜN_RENGİ}", "{DÜZELTME}"):
            assert yt in g, (f, yt)
        if f == "g0-feed.md":  # feed karesi yazısız (Merchant Center image_link kuralı, 0.4.0)
            assert "BU KAREDE HİÇBİR YAZI YOK" in g and "{BAŞLIK" not in g, f
        else:
            assert "{BAŞLIK_SATIRLARI}" in g or "{SATIR_METİNLERİ}" in g or "{BAŞLIK}" in g, f
        # sabit cümleler: tek görsel, girdi fotoğrafı yok sayılır, gravür silme, kilit, font, tek renk başlık, kenar payı
        for sabit in ("YALNIZ 1 görsel üret: kolaj, ızgara, yan yana varyasyon, çok panel",
                      "içindeki yazı, logo, zemin ve düzen YOK SAYILIR", "ÜRÜN KİLİDİ: Ek 1 ürünün TEK doğru kaynağıdır",
                      GRAVUR, KILIT_SON, "parça sayısı", "Barlow Condensed SemiBold ya da Oswald benzeri dar grotesk",
                      "Poppins, Montserrat ve benzeri geniş geometrik yazı tipi = RED", "Başlık TEK renk",
                      "markanın tek başlık ailesidir", "büyük harfte i → İ, ı → I",
                      "her kenarda tuvalin en az %7'si boş zemin", "çizgi ikon", "METİNLER (yalnız bunlar, birebir):",
                      "ÇIKTI: tek görsel"):
            assert sabit in g, (f, sabit)
        # doldurulmamış yer tutucu dışındaki her şey sabit: üç blok bütün şablonlarda karakter karakter aynı
        for ad, bas, son in (("kilit", "ÜRÜN KİLİDİ:", "RENK (yalnız bunlar):"), ("sistem", "RENK (yalnız bunlar):", "DÜZEN ("),
                             ("yasak", "YASAKLAR:", "{DÜZELTME}")):
            bloklar.setdefault(ad, set()).add(g[g.index(bas):g.index(son)].strip())
        # yer tutucu adları yalnız BÜYÜK HARF + alt çizgi
        assert all(re.fullmatch(r"[A-ZÇĞİÖŞÜ0-9_]+", x) for x in re.findall(r"\{([^}]+)\}", g)), f
    assert all(len(v) == 1 for v in bloklar.values()), {k: len(v) for k, v in bloklar.items()}
    # G1 dışındakilerde Ek 2 onaylı G1; başlık boyu G1 ve bannerlarda %9–11
    for f in URUN_SABLONLARI:
        g = istem_govdesi(oku(*ISTEM, f))
        assert ("Ek 2 = aynı markanın onaylı galeri karesi" in g) == (f != "g1.md"), f
    for f in ("g1.md", "b1-masaustu.md", "b2-mobil.md"):
        assert "%9–11'i" in istem_govdesi(oku(*ISTEM, f)), f
    # ortak dosyadaki bloklar şablonlardakiyle aynı
    o = oku(*G, "ortak-istem-bloklari.md")
    for v in bloklar.values():
        assert list(v)[0] in o
    assert "İstemi sen YAZMAZSIN" in o and "istemler/g2-makro.md" in o and "istemler/b2-mobil.md" in o


def test_skill_md_en_ustte_tek_gorsel_kurali():
    s = oku("skills", "gorseller", "SKILL.md")
    ilk = "\n".join(s.split("\n")[:15])
    for parca in ("TEK ÇAĞRI = TEK GÖRSEL", "Kolaj, ızgara, çok panel = RED", "kırpıp dosya yapmak YASAK",
                  "ürün fotoğrafı + onaylı G1 YENİDEN eklenir", '"düzenlenmez"', "HAZIR İSTEM", "KELİMESİ KELİMESİNE",
                  "references/istemler/", "duzelt.py zemin", "onaya sunmadan 1 kez yeniden üret"):
        assert parca in ilk, parca
    assert len(s.encode("utf-8")) <= 5120
    a5 = oku(*G, "adim-5-gorsel-uretimi.md")
    assert "0.3.6 HAZIR İSTEM" in a5 and "panel kırpma RED" in a5


def test_logo_varsayilani_ikon():
    lg = oku(*ISTEM, "logo-ikon.md")
    for parca in ("Varsayılan logo budur: **yalnız ikon, yazısız, şeffaf PNG.**", "yalnız kullanıcı isterse",
                  "{LOGO_FİKRİ}", "{LOGO_HEX}", "YALNIZ İKONDAN", "transparent background PNG, alfa kanallı",
                  "Ürün fotoğrafı EKLENMEZ"):
        assert parca in lg, parca
    assert "Logo varsayılanı: yalnız ikon, yazısız, şeffaf PNG" in oku("skills", "gorseller", "SKILL.md")
    ms = oku("skills", "marka", "SKILL.md")
    assert "varsayılan **yalnız ikon, yazısız, şeffaf PNG**" in ms and "Canlı metin logo yalnız kullanıcı isterse" in ms
    assert "logo ÜRETİLMEZ" not in ms and "varsayılan: logo yok" not in ms
    assert "**Varsayılan (0.3.6): yalnız ikon, yazısız, şeffaf PNG.**" in oku("skills", "marka", "references", "logo-renk-font.md")
    for f in (("skills", "gorseller", "SKILL.md"), G + ("uretim-promptlari.md",), G + ("adim-5-gorsel-uretimi.md",)):
        assert "varsayılan canlı metin" not in oku(*f).lower(), f
    assert "Logo: ikon (yalnız ikon, şeffaf PNG" in oku("src", "ortak", "00-calisma-tarzi.md")


def test_zemin_vurgu_marka_adiminda_ve_font_adi():
    ms = oku("skills", "marka", "SKILL.md")
    for parca in ("pembe/pastel/açık renkli ürün → KOYU nötr zemin", "petrol, antrasit, lacivert",
                  "vurgu ürünün renginden OLMAZ", "Barlow Condensed SemiBold", "Tek yazı sistemi", "barlow_condensed_n6"):
        assert parca in ms, parca
    lr = oku("skills", "marka", "references", "logo-renk-font.md")
    assert "Görsel kilidi (0.3.6" in lr and "KOYU nötr tek HEX" in lr and "`duzelt.py zemin` her görselde zorunlu" in lr
    assert "Görsel renkleri: zemin #" in oku("src", "ortak", "00-calisma-tarzi.md")
    t = oku("src", "ortak", "tasarim-dili.md")
    b = t[t.index("## 11. 0.3.6"):]
    for parca in ("Tek çağrı = tek görsel", "koyu nötr zemin", "Poppins/Montserrat/geniş geometrik = RED", "TEK renk",
                  "%9–11", "YOK SAYILIR", "≥ %6", "onaya sunmadan 1 kez yeniden üretim"):
        assert parca in b, parca
    for kelime in ("sağlık", "mevzuat", "hukuk"):          # hukuk kısıtı eklenmedi
        assert kelime not in b.lower(), kelime


def test_kontrol_listesi_baglayici_ve_pet_nisi():
    k = oku(*G, "kabul-kontrolu.md")
    b = k[k.index("### 2b. 0.3.6"):k.index("## 3. Kenar ve zemin")]
    for parca in ("GÖSTERİLMEZ", "1 kez yeniden üretilir", "Hatayı görüp yine de onaya sunmak YASAK", "**Yazım:**",
                  "**Ürün kilidi:**", "**Tek zemin:**", "**Font:**", "**Yasak öğe:**", "Poppins/Montserrat", "çizgi ikon"):
        assert parca in b, parca
    kur = oku("src", "ortak", "01-kurallar.md")
    assert "Pet / evcil hayvan ekipmanı" in kur and "`nis-gadget`" in kur and "güzellik (`nis-guzellik`) DEĞİLDİR" in kur
    assert "Pet / evcil hayvan ekipmanı" in oku("skills", "urun-analiz", "references", "01-kurallar.md")

