## Ne değişti ve neden?
<!-- Tek paragraf. Hangi beceri/ajan/betik, hangi sorun. -->

## Nasıl denedim?
<!-- Çalıştırdığın komut ve çıktısı (çıkış kodu). -->

## Kontrol listesi
- [ ] `claude plugin validate plugins/viral-urun-ekibi` ve `claude plugin validate .` geçti
- [ ] `python3 scripts/sozlesme_test.py` çıkış 0
- [ ] `python3 scripts/butce_kontrol.py` çıkış 0
- [ ] Mağaza kolu değiştiyse: `python3 moduller/magaza-kurucu/tools/build.py` + `python3 -m pytest -q moduller/magaza-kurucu/tests`
- [ ] `sh scripts/anonim_kontrol.sh` temiz (kara listen varsa) ve metinde kişisel bilgi, mutlak yol, anahtar yok
- [ ] Davranış değiştiyse `plugin.json` içindeki `version` arttı ve `CHANGELOG.md` güncellendi
- [ ] Kullanıcıya görünen metin Türkçe
