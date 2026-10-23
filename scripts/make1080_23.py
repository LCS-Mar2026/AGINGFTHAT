"""Downscale the 23 October master post image to the 1080x1350 delivery size."""
from PIL import Image

SRC = "social/twenty-minute-dose-nature-cortisol.jpg"
OUT = "social/twenty-minute-dose-nature-cortisol-1080.jpg"

im = Image.open(SRC).convert("RGB")
im.resize((1080, 1350), Image.LANCZOS).save(OUT, "JPEG", quality=95, subsampling=0, optimize=True)
print(OUT, Image.open(OUT).size, len(open(OUT, "rb").read()))

p = "scripts/build_public.py"
s = open(p, encoding="utf-8").read()
if OUT not in s:
    anchor = "'client-login.html']"
    assert s.count(anchor) == 1
    s = s.replace(anchor, "'" + OUT + "', " + anchor)
    open(p, "w", encoding="utf-8").write(s)
    print("whitelisted")
