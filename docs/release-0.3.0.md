# Release 0.3.0: yayın notu taslağı

> Taslak: GitHub Releases sayfasına yapıştırılır. Etiket: `v0.3.0` · Başlık: `0.3.0: tek kapı, kör jüri, sade depo`
> Eklenecek dosya: `viral-urun-ekibi-chatgpt.zip` (`sh scripts/chatgpt_paketi_yap.sh` ile `dist/` altında üretilir; depoda tutulmaz).

---

## Bu sürümde neler var?

**Daha sıkı kapılar.** Tek zorlayıcı kapı (`kapi.py`) ön-üretimden krediye ve tesliminden yayına geçişi kapatır; aşım yalnızca
kullanıcının `KARARLAR.md` içine yazdığı satırla mümkündür. Eleştirmen üçe bölündü: mekanik kontroller betiğe, zevk yargısı
performansa göre kalibre edilen kör video jürisine, kök neden ve düzeltme emri direktöre gitti.

**Daha kısa talimatlar.** Beceri ve ajan dosyaları budandı; tekrar eden kurallar `ortak/kurallar.md` içindeki kimlikli tek kaynağa indi,
ayrıntılar `referans/` dosyalarına taşındı. Hiçbir kapı ya da test kaldırılmadı. Yeni talimat bütçesi kapısı (`scripts/butce_kontrol.py`) bunu korur.

**Rol başına sonuç ölçümü.** Haftalık karne betiği (`karne_uret.py`) hangi rolün işe yaradığını sayıyla gösterir.

**Profesyonel depo.** README yeniden yazıldı (tek cümle, rozetler, akış diyagramı, 3 adımlık kurulum), İngilizce özet (`README.en.md`),
`CHANGELOG.md`, `SECURITY.md`, `PRIVACY.md`, `CODE_OF_CONDUCT.md`, issue ve PR şablonları, GitHub Actions CI, eklenti ikonu.
İç plan ve analiz belgeleri `docs/gelistirici/`, betikler `scripts/` altına taşındı.

## Dikkat: değişenler
- ChatGPT ZIP'i artık depoda yok; aşağıdaki dosyadan indir.
- Betik yolları değişti: `docs/*.sh|py` → `scripts/`. Kendi komutlarında ya da CI'nda eski yolu kullanıyorsan güncelle.
- Sağlık ve sonuç dili artık yasak değil, uyarı ve bilgi notu üretir; uydurma veri kapıları aynen duruyor.

## Kurulum

Claude Code:
```
/plugin marketplace add armanvibecoding/viral-urun-ekibi-market
/plugin install viral-urun-ekibi@viral-urun-market
```
Mevcut kullanıcılar: `/plugin` → Marketplaces → viral-urun-market → Update.

ChatGPT: aşağıdaki `viral-urun-ekibi-chatgpt.zip` dosyasını indir, açmadan ChatGPT → Plugins → yükle.

## Doğrulama
`claude plugin validate plugins/viral-urun-ekibi` uyarısız geçer; arayüz sözleşmesi 49/49, mağaza kolu testleri, kurgu, kapı, toplayıcı ve kırma testleri geçer.

Tam liste: [CHANGELOG.md](../CHANGELOG.md).
