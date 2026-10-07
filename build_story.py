"""9:16 Instagram story with the blog snapshot AND the caption baked in.
Artwork = THE ARTICLE'S OWN HERO so the social post matches the blog.
One image, nothing to copy. Lee adds music and posts."""
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

EYEBROW="BIO AGE \u00b7 BLOOD MARKERS"
STATEMENT=("A biometric assessment brings biological signals together to create a "
           "more useful picture of healthspan than chronological age alone.")
CAPTION=("Chronological age tells you how many birthdays have passed. It does not tell you "
         "how well you move, recover or regulate blood sugar. A biological age test turns "
         "vague concern into a measurement you can act on.")
FOOTER="New articles daily at agingfthat.com/blog"
TAGS="#healthspan  #longevity"
PILL="BLOG \u00b7 LINK IN BIO"
OUT="social/how-to-read-biological-age-results-story"

ART_H=int(H*0.44)
art=Image.open("/tmp/hero.webp").convert("RGB")
r=max(W/art.width,ART_H/art.height)
art=art.resize((int(art.width*r),int(art.height*r)),Image.LANCZOS)
l=(art.width-W)//2; t=int((art.height-ART_H)*0.34)
art=art.crop((l,t,l+W,t+ART_H))
art=ImageEnhance.Contrast(art).enhance(1.06)
art=ImageEnhance.Brightness(art).enhance(0.94)

c=Image.new("RGB",(W,H),NAVY); c.paste(art,(0,0))
d=ImageDraw.Draw(c,"RGBA")
g=340
for y in range(ART_H-g,ART_H):
    a=int(255*((y-(ART_H-g))/g)**1.35)
    d.line([(0,y),(W,y)],fill=(3,21,34,a))
d.rectangle([0,ART_H,W,H],fill=NAVY)

PAD=72
logo=Image.open("aft-logo.png").convert("RGBA")
logo=logo.crop(logo.split()[-1].getbbox())
LW=286; LH=int(logo.height*(LW/logo.width))
logo=logo.resize((LW,LH),Image.LANCZOS)
c.paste(logo,(PAD,ART_H+44),logo)

ry=ART_H+44+LH+30
d.line([(PAD,ry),(W-PAD,ry)],fill=CYAN,width=3)
d.text((PAD,ry+34),EYEBROW,font=font(25,700),fill=CYAN)

f=font(50,900); lh=int(50*1.26)
lines=wrap(d,STATEMENT,f,W-2*PAD)
y=ry+34+58
for ln in lines:
    d.text((PAD,y),ln,font=f,fill=WHITE); y+=lh

y+=18
f2=font(32,500); lh2=int(32*1.52)
cap=wrap(d,CAPTION,f2,W-2*PAD)
for ln in cap:
    d.text((PAD,y),ln,font=f2,fill=ICE); y+=lh2

y+=30
d.text((PAD,y),FOOTER,font=font(29,700),fill=CYAN)
y+=44
d.text((PAD,y),TAGS,font=font(28,700),fill=ICE)

fp=font(30,800)
tw=d.textlength(PILL,font=fp)
pill_h=78; pill_y=H-158
d.rounded_rectangle([PAD,pill_y,PAD+tw+60,pill_y+pill_h],radius=pill_h//2,fill=CYAN)
d.text((PAD+30,pill_y+(pill_h-int(fp.size*1.2))//2+2),PILL,font=fp,fill=NAVY)

print("content ends y:",y,"| pill top:",pill_y,"| gap:",pill_y-y,"| fits:", y < pill_y-40)
os.makedirs("social", exist_ok=True)
c.convert("RGB").save(OUT+".jpg",quality=90,subsampling=0,optimize=True,progressive=False)
b=open(OUT+".jpg","rb").read()
print("story OK",c.size,"bytes",len(b),"sha256",hashlib.sha256(b).hexdigest())
