"""Build the 9:16 Instagram story image for the day's article. CI-safe."""
import os, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W,H = 1080,1920
NAVY=(3,21,34); ICE=(169,205,234); CYAN=(43,199,255); WHITE=(237,250,255)
FONT="/tmp/Montserrat.ttf"

def font(sz,w=900):
    f=ImageFont.truetype(FONT,sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f

def wrap(d,t,f,maxw):
    out=[];cur=""
    for word in t.split():
        s=(cur+" "+word).strip()
        if d.textlength(s,font=f)<=maxw: cur=s
        else:
            if cur: out.append(cur)
            cur=word
    if cur: out.append(cur)
    return out

STATEMENT=("A biometric assessment brings biological signals together to create a "
           "more useful picture of healthspan than chronological age alone.")
EYEBROW="BIO AGE \u00b7 BLOOD MARKERS"
PILL="BLOG \u00b7 LINK IN BIO"
OUT="social/how-to-read-biological-age-results-story"

art=Image.open("/tmp/art-story.webp").convert("RGB")
r=max(W/art.width,H/art.height)
art=art.resize((int(art.width*r),int(art.height*r)),Image.LANCZOS)
l=(art.width-W)//2; t=(art.height-H)//2
art=art.crop((l,t,l+W,t+H))
art=ImageEnhance.Contrast(art).enhance(1.05)
art=ImageEnhance.Brightness(art).enhance(0.92)

c=art.copy()
d=ImageDraw.Draw(c,"RGBA")
for i in range(760):
    a=int(190*(1-(i/760))**1.15)
    d.line([(0,i),(W,i)],fill=(3,21,34,a))
for i in range(700):
    a=int(225*((i/700))**1.05)
    d.line([(0,H-700+i),(W,H-700+i)],fill=(3,21,34,a))

PAD=76
logo=Image.open("aft-logo.png").convert("RGBA")
logo=logo.crop(logo.split()[-1].getbbox())
LW=300; LH=int(logo.height*(LW/logo.width))
logo=logo.resize((LW,LH),Image.LANCZOS)
c.paste(logo,(PAD,132),logo)
d.line([(PAD,132+LH+34),(W-PAD,132+LH+34)],fill=CYAN,width=3)
d.text((PAD,132+LH+70),EYEBROW,font=font(26,700),fill=CYAN)

f=font(56,800); lh=int(56*1.34)
lines=wrap(d,STATEMENT,f,W-2*PAD)
while len(lines)*lh>620 and f.size>40:
    f=font(f.size-2,800); lh=int(f.size*1.34); lines=wrap(d,STATEMENT,f,W-2*PAD)
y=H-700+70
for ln in lines:
    d.text((PAD,y),ln,font=f,fill=WHITE); y+=lh

fp=font(30,800)
tw=d.textlength(PILL,font=fp)
pill_h=76; pill_y=H-160
d.rounded_rectangle([PAD,pill_y,PAD+tw+60,pill_y+pill_h],radius=pill_h//2,fill=CYAN)
d.text((PAD+30,pill_y+(pill_h-int(fp.size*1.2))//2+2),PILL,font=fp,fill=NAVY)

os.makedirs("social", exist_ok=True)
c.convert("RGB").save(OUT+".jpg",quality=90,subsampling=0,optimize=True,progressive=False)
b=open(OUT+".jpg","rb").read()
print("story OK", c.size, "bytes", len(b), "sha256", hashlib.sha256(b).hexdigest())
