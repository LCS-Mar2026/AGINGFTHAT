"""9:16 Instagram story with the blog snapshot AND the caption baked in.
Artwork = the day's FRESH graphic. One image, nothing to copy. Lee adds music and posts."""
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

EYEBROW="NUTRITION & HEALTHSPAN"
STATEMENT=("Butyrate and Biological Age: The Molecule Your Gut Bacteria Make From Fibre")
CAPTION=("Your gut bacteria ferment fibre into butyrate. Colon cells use it as fuel and researchers study it for effects on inflammation, the gut barrier and gene regulation. A new article separates the credible science from the hype, explains why the UK averages 16.4 grams of fibre a day against a 30-gram recommendation, and gives a five-step protocol to build the fibre habit properly.")
FOOTER="Read the full blog at www.agingfthat.com!"
TAGS="#healthspan  #longevity"
PILL="SEE CAPTION FOR MORE"
OUT="social/butyrate-fibre-biological-age-story"

ART_H=int(H*0.40)
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
c.paste(logo,(PAD,ART_H+40),logo)

ry=ART_H+40+LH+28
d.line([(PAD,ry),(W-PAD,ry)],fill=CYAN,width=3)
d.text((PAD,ry+32),EYEBROW,font=font(24,700),fill=CYAN)

f=font(44,900); lh=int(44*1.24)
lines=wrap(d,STATEMENT,f,W-2*PAD)
y=ry+32+54
for ln in lines:
    d.text((PAD,y),ln,font=f,fill=WHITE); y+=lh

y+=16
f2=font(29,500); lh2=int(29*1.50)
cap=wrap(d,CAPTION,f2,W-2*PAD)
for ln in cap:
    d.text((PAD,y),ln,font=f2,fill=ICE); y+=lh2

y+=24
d.text((PAD,y),FOOTER,font=font(28,700),fill=CYAN)
y+=42
d.text((PAD,y),TAGS,font=font(27,700),fill=ICE)

fp=font(30,800)
tw=d.textlength(PILL,font=fp)
pill_h=78; pill_y=H-150
d.rounded_rectangle([PAD,pill_y,PAD+tw+60,pill_y+pill_h],radius=pill_h//2,fill=CYAN)
d.text((PAD+30,pill_y+(pill_h-int(fp.size*1.2))//2+2),PILL,font=fp,fill=NAVY)

print("content ends y:",y,"| pill top:",pill_y,"| gap:",pill_y-y,"| fits:", y < pill_y-30)
os.makedirs("social", exist_ok=True)
c.convert("RGB").save(OUT+".jpg",quality=90,subsampling=0,optimize=True,progressive=False)
b=open(OUT+".jpg","rb").read()
print("story OK",c.size,"bytes",len(b),"sha256",hashlib.sha256(b).hexdigest())
