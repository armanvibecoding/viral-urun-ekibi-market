#!/usr/bin/env python3
"""Eleştirmen puan kaydı: her eleştiri is/NN/elestiri/puanlar.jsonl dosyasına bir satır (cetvel: referans/puan-cetveli.md).

Kullanım:
  python3 puan_kaydet.py is/NN/elestiri/puanlar.jsonl --video 26 --tur 2 --mod teslim \
      --kanca 6 --gercekcilik 3 --yazi 5 --ritim 6 --ses 8 \
      --kusur "yazi: 6,8 sn 'Heart mode' alev seçim planında" \
      --agir "secilen!=gorunen: alev seçiliyor, video kalple bitiyor" \
      --yeni_kural "ritim: aynı aracın 3 videosu aynı yapı" [--gerekce "..."] [--cagri 3]

Toplam = beş alanın düz ortalaması, en yakın 0,5'e (ön-üretimde verilen alanların ortalaması).
Ağır kusur (--agir) varsa toplam en fazla 5 ve geçti=false.
Teslim geçer: toplam >= 7, hiçbir alan < 5, ağır kusur yok. Ön-üretim geçer: toplam >= 6, gerçekçilik >= 7, ağır yok.
--yeni_kural "alan: metin": kontrat dışı kusur; yalnız toplam_yeni'de o alanı en fazla 1 düşürür, geçti'yi etkilemez.
Aynı video+mod için önceki satırdan |Δtoplam| > 1,5 ise --gerekce zorunlu; yoksa yazmaz, çıkış 2.
Çıkış 0 = satır yazıldı (satır stdout'a JSON).
"""
import argparse, datetime, json, math, os, sys

ALANLAR = ["kanca", "gercekcilik", "yazi", "ritim", "ses"]


def yuvarla(x):
    return math.floor(x * 2 + 0.5) / 2


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya")
    ap.add_argument("--video", required=True)
    ap.add_argument("--tur", type=int, required=True)
    ap.add_argument("--mod", choices=["teslim", "onuretim"], default="teslim")
    for a in ALANLAR:
        ap.add_argument("--" + a, type=float)
    ap.add_argument("--kusur", action="append", default=[])
    ap.add_argument("--agir", action="append", default=[])
    ap.add_argument("--yeni_kural", action="append", default=[])
    ap.add_argument("--gerekce", default="")
    ap.add_argument("--cagri", type=int, help="eleştirmen çağrı no")
    a = ap.parse_args()

    puan = {k: getattr(a, k) for k in ALANLAR}
    for k, v in puan.items():
        if v is not None and not 1 <= v <= 10:
            sys.exit(f"{k} 1–10 arası olmalı: {v}")
    gerekli = ALANLAR if a.mod == "teslim" else ["kanca", "gercekcilik"]
    eksik = [k for k in gerekli if puan[k] is None]
    if eksik:
        sys.exit(f"{a.mod} modunda eksik alan: {', '.join(eksik)}")
    verilen = {k: v for k, v in puan.items() if v is not None}

    yeni = dict(verilen)
    for y in a.yeni_kural:
        alan = y.split(":", 1)[0].strip()
        if alan not in verilen:
            sys.exit(f"--yeni_kural 'alan: metin' biçiminde olmalı (alan: {', '.join(ALANLAR)}): {y}")
        yeni[alan] = max(verilen[alan] - 1, 1) if yeni[alan] == verilen[alan] else yeni[alan]  # alan başına en fazla 1

    def toplamla(d):
        t = yuvarla(sum(d.values()) / len(d))
        return min(t, 5.0) if a.agir else t

    toplam, toplam_yeni = toplamla(verilen), toplamla(yeni)
    if a.mod == "teslim":
        gecti = toplam >= 7 and min(verilen.values()) >= 5 and not a.agir
    else:
        gecti = toplam >= 6 and verilen["gercekcilik"] >= 7 and not a.agir

    onceki = None
    if os.path.exists(a.dosya):
        with open(a.dosya, encoding="utf-8") as f:
            for satir in f:
                if satir.strip():
                    r = json.loads(satir)
                    if str(r.get("video")) == str(a.video) and r.get("mod") == a.mod:
                        onceki = r
    fark = None if onceki is None else round(toplam - onceki["toplam"], 2)
    if fark is not None and abs(fark) > 1.5 and not a.gerekce.strip():
        print(f"KAYDEDİLMEDİ: video {a.video} önceki tur {onceki['tur']} toplam {onceki['toplam']} → {toplam} "
              f"(Δ {fark:+}). > 1,5 oynama için --gerekce zorunlu (hangi değişiklik/kanıt).", file=sys.stderr)
        sys.exit(2)

    kayit = {"video": a.video, "tur": a.tur, "mod": a.mod, "puanlar": puan, "toplam": toplam,
             "toplam_yeni": toplam_yeni, "gecti": gecti, "kusurlar": a.kusur, "agir_kusurlar": a.agir,
             "yeni_kural": a.yeni_kural, "onceki_fark": fark, "gerekce": a.gerekce, "cagri": a.cagri,
             "tarih": datetime.datetime.now().isoformat(timespec="seconds")}
    os.makedirs(os.path.dirname(os.path.abspath(a.dosya)), exist_ok=True)
    with open(a.dosya, "a", encoding="utf-8") as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
    print(json.dumps(kayit, ensure_ascii=False))


if __name__ == "__main__":
    main()
