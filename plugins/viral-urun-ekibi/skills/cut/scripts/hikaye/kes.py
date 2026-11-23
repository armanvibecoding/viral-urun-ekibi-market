"""kes.py <kaynak.png> <çıktı.png> x0 y0 x1 y1 [alt üst] — düz (tek renkli) zeminli ürün fotoğrafından ürünü keser (zemin rengine uzaklık → alfa).
Gerçek ürün fotoğrafı yoksa kesme yapılmaz; AI görseli yalnız son çaredir (tarif 02)."""
import sys, numpy as np
from PIL import Image, ImageFilter
s, o = sys.argv[1:3]; x0, y0, x1, y1 = map(int, sys.argv[3:7])
im = np.asarray(Image.open(s).convert("RGB").crop((x0, y0, x1, y1))).astype(float)
# zemin: kenar pikselleri medyanı (yerel: satır bazlı sol/sağ kenar ortalaması ile gradyan izlenir)
kenar = np.concatenate([im[:6].reshape(-1, 3), im[-6:].reshape(-1, 3), im[:, :6].reshape(-1, 3), im[:, -6:].reshape(-1, 3)])
bg = np.median(kenar, 0)
d = np.sqrt(((im - bg) ** 2).sum(2))
lo, hi = float(sys.argv[7]) if len(sys.argv) > 7 else 22, float(sys.argv[8]) if len(sys.argv) > 8 else 60
a = np.clip((d - lo) / (hi - lo), 0, 1)
A = Image.fromarray((a * 255).astype("uint8")).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
# en büyük bileşen dışındaki küçük parçaları (yazı kırıntısı) at
from PIL import ImageChops
import numpy as np
m = (np.asarray(A) > 90).astype(np.uint8)
try:
    from scipy import ndimage as nd
    lab, n = nd.label(m)
    if n > 1:
        big = 1 + np.argmax(nd.sum(m, lab, range(1, n + 1))); keep = nd.binary_dilation(lab == big, iterations=6)
        A = Image.fromarray((np.asarray(A) * keep).astype("uint8"))
except ImportError: pass
out = Image.fromarray(im.astype("uint8")).convert("RGBA"); out.putalpha(A); out.save(o); print(o, out.size, "bg", bg.round())
