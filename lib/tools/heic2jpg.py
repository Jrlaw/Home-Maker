"""HEIC -> JPEG next to each input (see heic2jpg.sh)."""
import sys

import pillow_heif
from PIL import Image, ImageOps

pillow_heif.register_heif_opener()
for p in sys.argv[1:]:
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    im.thumbnail((1600, 1600))
    out = p.rsplit(".", 1)[0] + ".jpg"
    im.save(out, quality=88)
    print(out)
