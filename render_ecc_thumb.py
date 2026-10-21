import requests, io, os, hashlib
from PIL import Image
rs = requests.get("https://cdn.marblism.com/6L-QusN7eqq.webp", timeout=60)
rs.raise_for_status()
im = Image.open(io.BytesIO(rs.content)).convert("RGB")
if im.width > 1200:
    im = im.resize((1200, int(im.height*1200/im.width)), Image.LANCZOS)
ratio = 3/2
hig = int(im.width / ratio)
if hig < im.height:
    yt = (im.height - hig) // 2
    im = im.crop((0, yt, im.width, yt + hig))
im = im.resize((1200, 675), Image.LANCZOS)
path = "blog/images/eccentric-lowering-strength-training-over-50.jpg"
im.save(path, "JPEG", quality=92)
b = open(path, "rb").read()
print("thumb written", len(b), "sha", hashlib.sha256(b).hexdigest())
