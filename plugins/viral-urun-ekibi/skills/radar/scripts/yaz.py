#!/usr/bin/env python3
"""yaz.py METIN — iPhone Yansıtma'ya klavye TUŞ KODLARIYLA yazar (macOS).

iPhone Yansıtma unicode klavye olaylarını yok sayıyor; tuş kodlarını ise iPhone'un klavye düzenine göre
yorumluyor ve bu düzen değişebiliyor. Düzen, bu dosyanın yanındaki `klavye` dosyasından okunur: us (varsayılan) | tr.
Yazdıktan sonra arama kutusundaki metni ekran görüntüsünde kontrol et; bozuksa `klavye` dosyasını değiştir.
Yalnız a-z, 0-9, nokta, tire, alt çizgi ve boşluk yazılır (kullanıcı adı aramak için yeterli).
"""
import os
import subprocess
import sys

K = dict(a=0, s=1, d=2, f=3, h=4, g=5, z=6, x=7, c=8, v=9, b=11, q=12, w=13, e=14, r=15, y=16, t=17,
         o=31, u=32, i=34, p=35, l=37, j=38, k=40, n=45, m=46)
K.update({'1': 18, '2': 19, '3': 20, '4': 21, '6': 22, '5': 23, '9': 25, '7': 26, '8': 28, '0': 29,
          '.': 47, '-': 27, ' ': 49})

D = os.path.dirname(os.path.abspath(__file__))
try:
    duzen = open(os.path.join(D, 'klavye'), encoding='utf-8').read().strip()
except OSError:
    duzen = 'us'
if duzen == 'tr':  # iPhone TR-Q düzeni: i = US ' (39), . = US / (44), - = US = (24)
    K.update({'i': 39, '.': 44, '-': 24})

if len(sys.argv) < 2:
    sys.exit('kullanım: yaz.py METIN')
cmd = []
for ch in sys.argv[1].lower():
    if ch == '_':
        cmd.append('key code %d using shift down' % (24 if duzen == 'tr' else 27))
    elif ch in K:
        cmd.append(f'key code {K[ch]}')
    else:
        print('atlandı:', ch, file=sys.stderr)
script = 'tell application "System Events"\n' + '\ndelay 0.03\n'.join(cmd) + '\nend tell'
sys.exit(subprocess.run(['osascript', '-e', script]).returncode)
