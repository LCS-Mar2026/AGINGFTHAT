"""Render the daily AFT Instagram POST (1440x1800 master + 1080x1350) for the
current article. Artwork and font are fetched into /tmp by the workflow."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H = 1440, 1800
K = W / 1080.0
NAVY = (3, 21, 34); ICE = (169, 205, 234); CYAN = (43, 199, 255); WHITE = (237, 250, 255)
FONT = "/tmp/Montserrat.ttf"

def font(sz, w=900):
    f = ImageFont.truetype(FONT, int(round(sz * K)))
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f

def wrap(d, t, f, maxw):
    out = []; cur = ""
    for word in t.split():
        s = (cur + " " + word).strip()
        if d.textlength(s, font=f) <= maxw: cur = s
        else:
            if cur: out.append(cur)
            cur = word
    if cur: out.append(cur)
    return out

TITLE = "How to Read Your Biological Age Results: Turning Blood Markers Into a Healthspan Plan"
EYEBROW = "BIO AGE \u00b7 BLOOD MARKERS"
LINE = "New articles daily at agingfthat.com/blog"
PILL = "BLOG \u00b7 LINK IN BIO"
OUT = "social/how-to-read-biological-age-results"

art = Image.open("/tmp/art.webp").convert("RGB")
BAND = int(H * 0.472)
r = max(W / art.width, BAND / art.height)
art = art.resize((int(art.width * r), int(art.height * r)), Image.LANCZOS)
l = (art.width - W) // 2; t = int((art.height - BAND) * 0.30)
art = art.crop((l, t, l + W, t + BAND))
art = ImageEnhance.Contrast(art).enhance(1.05)
art = ImageEnhance.Sharpness(art).enhance(1.25)

c = Image.new("RGB", (W, H), NAVY); c.paste(art, (0, 0))
d = ImageDraw.Draw(c, "RGBA")
g = int(220 * K)
for y in range(BAND - g, BAND):
    a = int(255 * ((y - (BAND - g)) / g) ** 1.4)
    d.line([(0, y), (W, y)], fill=(3, 21, 34, a))
d.rectangle([0, BAND, W, H], fill=NAVY)

PAD = int(70 * K)
logo = Image.open("aft-logo.png").convert("RGBA")
logo = logo.crop(logo.split()[-1].getbbox())
LW = int(300 * K); LH = int(logo.height * (LW / logo.width))
logo = logo.resize((LW, LH), Image.LANCZOS)
ly = BAND + int(40 * K)
c.paste(logo, (PAD, ly), logo)

ry = ly + LH + int(34 * K)
d.line([(PAD, ry), (W - PAD, ry)], fill=CYAN, width=int(3 * K))
ey = ry + int(36 * K)
d.text((PAD, ey), EYEBROW, font=font(26, 700), fill=CYAN)

fp = font(27, 800); pill_h = int(70 * K); pill_y = H - int(46 * K) - pill_h
f2 = font(29, 600)
body_lines = wrap(d, LINE, f2, W - 2 * PAD)
body_y = pill_y - int(22 * K) - len(body_lines) * int(38 * K)

f = font(54, 900); lh = int(f.size * 1.16)
lines = wrap(d, TITLE, f, W - 2 * PAD)
hy = ey + int(40 * K) + int(20 * K)
need = len(lines) * lh; avail = body_y - int(22 * K) - hy
while need > avail and f.size > int(38 * K):
    f = font(f.size / K - 2, 900); lh = int(f.size * 1.16)
    lines = wrap(d, TITLE, f, W - 2 * PAD); need = len(lines) * lh
y = hy
for ln in lines:
    d.text((PAD, y), ln, font=f, fill=WHITE); y += lh
y = body_y
for ln in body_lines:
    d.text((PAD, y), ln, font=f2, fill=ICE); y += int(38 * K)

tw = d.textlength(PILL, font=fp)
d.rounded_rectangle([PAD, pill_y, PAD + tw + int(56 * K), pill_y + pill_h], radius=pill_h // 2, fill=CYAN)
d.text((PAD + int(28 * K), pill_y + (pill_h - int(fp.size * 1.2)) // 2 + 2), PILL, font=fp, fill=NAVY)

c.convert("RGB").save(OUT + ".jpg", quality=95, subsampling=0, optimize=True)
c.resize((1080, 1350), Image.LANCZOS).convert("RGB").save(OUT + "-1080.jpg", quality=95, subsampling=0, optimize=True)
print("rendered", c.size, "headline", f.size, "lines", len(lines))
