import requests, io, os
from PIL import Image
pairs = [
    ("creatine-brain-phosphate-buffer", "https://cdn.marblism.com/VCezZc1RB9N.webp"),
    ("multivitamin-myth-blood-test-first", "https://cdn.marblism.com/KwizQuc3ZPz.webp"),
]
os.makedirs("blog/images", exist_ok=True)
for slug, url in pairs:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    im = Image.open(io.BytesIO(r.content)).convert("RGB")
    if im.width > 1200:
        im = im.resize((1200, int(im.height * 1200 / im.width)), Image.LANCZOS)
    path = "blog/images/" + slug + ".jpg"
    im.save(path, "JPEG", quality=92)
    print(slug, im.size, os.path.getsize(path))
