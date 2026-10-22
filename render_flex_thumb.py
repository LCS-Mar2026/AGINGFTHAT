import requests, io, hashlib
from PIL import Image
r = requests.get("https://cdn.marblism.com/Un19Z5bSjMl.webp", timeout=60)
r.raise_for_status()
im = Image.open(io.BytesIO(r.content)).convert("RGB")
ratio = 3/2
hig = int(im.width / ratio)
if hig < im.height:
    yt = (im.height - hig) // 2
    im = im.crop((0, yt, im.width, yt + hig))
im = im.resize((1200, 675), Image.LANCZOS)
path = "blog/images/flexibility-score-flexindex-healthspan.jpg"
im.save(path, "JPEG", quality=90)
b = open(path, "rb").read()
print("thumb written", len(b), hashlib.sha256(b).hexdigest()[:16])
