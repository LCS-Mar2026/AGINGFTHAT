# -*- coding: utf-8 -*-
"""Build the dashboard pages from the shared template."""
import math
from css import CSS

HERO_ART = "https://cdn.marblism.com/v87Uu3kUSV9.webp"
BC_FIG   = "https://cdn.marblism.com/9J9277dyCCt.webp"
HEART    = "https://cdn.marblism.com/zZxd4bJ1qSt.webp"
POS_F    = "https://cdn.marblism.com/9J9277dyCCt.webp"
POS_S    = "https://cdn.marblism.com/9J9277dyCCt.webp"
BLOOD_ART = "https://cdn.marblism.com/X-G7nSsrtUc.webp"
BA_ART    = "https://cdn.marblism.com/f4-1J604s_r.webp"

GREEN="#7CFF1F"; AMBER="#FFB020"; RED="#FF1744"; CYAN="#2BC7FF"; VIOLET="#A855F7"

def ring(pct,col):
    """Three-band arc. The score lands visibly inside red, neutral or green."""
    import math
    r=64.0; circ=2*math.pi*r
    bands=[(0,40,'#8a2b2b'),(40,70,'#7a5a1e'),(70,100,'#1d7a4e')]
    out=['<svg viewBox="0 0 150 150">']
    out.append('<circle cx="75" cy="75" r="%.0f" fill="none" stroke="#0d2b3c" stroke-width="11"/>'%r)
    for lo,hi,c in bands:
        a0=circ*lo/100.0; a1=circ*(hi-lo)/100.0
        out.append('<circle cx="75" cy="75" r="%.0f" fill="none" stroke="%s" stroke-width="11" '
                   'stroke-dasharray="%.1f %.1f" stroke-dashoffset="%.1f" opacity="0.85"/>'
                   %(r,c,a1,circ-a1,-a0))
    dash=circ*pct/100.0
    out.append('<circle cx="75" cy="75" r="%.0f" fill="none" stroke="%s" stroke-width="11" '
               'stroke-linecap="round" stroke-dasharray="%.1f %.1f"/>'%(r,col,dash,circ-dash))
    ang=-90+360*pct/100.0; rad=math.radians(ang)
    out.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="#04202e" stroke-width="2"/>'
               %(75+(r-0)*math.cos(rad),75+(r-0)*math.sin(rad),col))
    out.append('</svg>')
    return "".join(out)

def _svg_open(W,H):
    return '<svg viewBox="0 0 %d %d">'%(W,H)

def _grid(p, W, H, padL, padR, padT, ih, lo, hi, ticks=4):
    for k in range(ticks):
        y = padT + ih*k/(ticks-1.0)
        p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#12405a" stroke-width="1"/>'%(padL,y,W-padR,y))
        p.append('<text x="%d" y="%.1f" text-anchor="end" fill="#9fc4d6" font-size="12">%.0f</text>'%(padL-6,y+4, hi-(hi-lo)*k/(ticks-1.0)))

def _axis_labels(p, labels, X, H):
    for i,lb in enumerate(labels):
        p.append('<text x="%.1f" y="%d" text-anchor="middle" fill="#9fc4d6" font-size="12">%s</text>'%(X(i),H-6,lb))

def trend_chart(series, labels, note="", top=None):
    """Three-point trend chart. Fixed viewBox so type stays legible. Series are right-aligned."""
    W,H = 560,200; padL,padR,padT,padB = 40,14,14,30
    iw=W-padL-padR; ih=H-padT-padB
    flat=[v for x in series for v in x['vals']]
    lo=0 if top else min(flat); hi=top if top else max(flat)
    if hi==lo: hi=lo+1
    pad=(hi-lo)*0.16; lo=(lo-pad) if not top else 0; hi=hi+pad
    def X(i): return padL+iw*(i/(len(labels)-1))
    def Y(v): return padT+ih*(1-(v-lo)/(hi-lo))
    p=[_svg_open(W,H)]
    _grid(p, W, H, padL, padR, padT, ih, lo, hi)
    _axis_labels(p, labels, X, H)
    for x in series:
        vals=x['vals']; off=len(labels)-len(vals)
        idx=list(range(off,off+len(vals)))
        pts=" ".join("%.1f,%.1f"%(X(i),Y(v)) for i,v in zip(idx,vals))
        p.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>'%(pts,x['c']))
        for i,v in zip(idx,vals):
            p.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>'%(X(i),Y(v),x['c']))
    p.append('</svg>')
    return "".join(p)

def delta_chart(series, labels):
    """Chronological against biometric age. Solid history, dashed projection."""
    W,H = 560,220; padL,padR,padT,padB = 40,14,14,32
    iw=W-padL-padR; ih=H-padT-padB
    flat=[v for x in series for v in x['vals']]
    lo=min(flat); hi=max(flat); pad=(hi-lo)*0.14 or 1
    lo-=pad; hi+=pad
    def X(i): return padL+iw*(i/(len(labels)-1))
    def Y(v): return padT+ih*(1-(v-lo)/(hi-lo))
    p=[_svg_open(W,H)]
    _grid(p, W, H, padL, padR, padT, ih, lo, hi)
    for i,lb in enumerate(labels):
        dash = ' stroke-dasharray="4 4"' if i>=3 else ''
        if i>=3:
            p.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#3d5c72" stroke-width="1" stroke-dasharray="4 4"/>'%(X(i),padT,X(i),H-padB))
    _axis_labels(p, labels, X, H)
    for x in series:
        vals=x['vals']; nh=x.get('nh',len(vals))
        hist=vals[:nh]; proj=vals[nh-1:] if nh<len(vals) else []
        pts=" ".join("%.1f,%.1f"%(X(i),Y(v)) for i,v in enumerate(hist))
        p.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round"/>'%(pts,x['c']))
        if proj:
            po=" ".join("%.1f,%.1f"%(X(nh-1+i),Y(v)) for i,v in enumerate(proj))
            p.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.8" stroke-dasharray="7 5" stroke-linejoin="round" stroke-linecap="round"/>'%(po,x['c']))
        for i,v in enumerate(vals):
            p.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"%s/>'%(X(i),Y(v),x['c'],' stroke="#04202e" stroke-width="1.6"' if i>=nh else ''))
    p.append('</svg>')
    return "".join(p)

def trend_legend(series):
    return '<div class="tlegend">'+"".join(
        '<span><i style="background:%s"></i>%s <b>%s</b></span>'%(x['c'],x['n'],x['vals'][-1])
        for x in series)+'</div>'

def mini(rows):
    h=['<div class="mini">']
    for lbl,(val,pct),cls in rows:
        h.append('<div class="minirow"><span>%s</span><span class="track"><i style="background:%s;width:%d%%"></i></span><b>%s</b></div>'%(lbl,cls,pct,val))
    h.append('</div>')
    return "".join(h)

def silo(colours):
    h=['<div class="sil">']
    for c in colours:
        h.append('<svg viewBox="0 0 40 76"><g fill="%s"><circle cx="20" cy="8" r="6"/>'
                 '<rect x="15" y="15" width="10" height="20" rx="4"/>'
                 '<rect x="6" y="17" width="7" height="18" rx="3"/>'
                 '<rect x="27" y="17" width="7" height="18" rx="3"/>'
                 '<rect x="15" y="36" width="4.5" height="30" rx="2"/>'
                 '<rect x="20.5" y="36" width="4.5" height="30" rx="2"/></g></svg>'%c)
    h.append('</div>')
    return "".join(h)

def page(c):
    A=[]; P=A.append
    P('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
    P('<title>%s</title>'%c['title'])
    P('<meta name="description" content="%s">'%c['desc'])
    P('<link rel="canonical" href="https://agingfthat.com/%s">'%c['slug'])
    P('<meta name="robots" content="%s">'%c['robots'])
    P('<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" href="favicon.svg" type="image/svg+xml">'
      '<link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">')
    P('<style>%s</style></head><body>'%CSS)
    P('<header class="hero">'
      '<div class="hero-txt"><p>%s</p>'
      '<p class="strap">MEASURE &#124; ANALYSE &#124; OPTIMISE &#124; TRACK STATUS%s</p></div></header>'
      %(c['sub'], (' <span class="mocknote">%s</span>'%c['notice']) if c.get('notice') else ''))
    m=c['meta']
    P('<div class="metabar"><div>Name<b>%s</b></div><div>Assessment Date<b>%s</b></div>'
      '<div>Program<b>%s</b></div><div>Status<b>%s<span class="dot %s"></span></b></div></div>'
      %(m['name'],m['date'],m['program'],m['status'],m['dot']))
    P('<div class="wrap">')
    if c.get('banner'): P('<p class="disc">%s</p>'%c['banner'])
    P('<div class="panels">')
    b=c['bc']
    P('<section class="panel bc"><div class="ph"><span class="ic">&#128100;</span><div><h2>BODY COMPOSITION</h2><p>%s</p></div></div>'%b['src'])
    P('<div class="body"><div class="bcgrid"><div class="fig"><img src="%s" alt="3D anatomical body composition visualisation showing muscle volume in blue and visceral fat in amber"></div>'%BC_FIG)
    P('<div class="stats">')
    for lbl,val,tag in b['rows']:
        P('<div class="stat"><span>%s</span><b>%s%s</b></div>'%(lbl,val,tag))
    P('</div></div><div class="chips">')
    for i,ch in enumerate(b['chips'],1):
        P('<div class="chip"><i>%d</i>%s</div>'%(i,ch))
    P('</div>'+mini(b['mini']))
    P('</div><div class="pb"><a class="btn" href="#">%s</a></div></section>'%b['btn'])
    mp=c['mp']
    P('<section class="panel mp"><div class="ph"><span class="ic">&#128694;</span><div><h2>MOVEMENT &amp; POSTURE</h2>'
      '<p>MOVEMENT &#183; ALIGNMENT &#183; POSTURE ANALYSIS</p></div></div>')
    P('<div class="body"><div class="figpair">'
      '<img src="%s" alt="Placeholder posture view, front, standing in for the chiropractic biomechanical report image">'
      '<img src="%s" alt="Placeholder posture view, side, standing in for the chiropractic biomechanical report image"></div>'%(POS_F,POS_S))
    P('<ul class="li">'+''.join('<li>%s</li>'%x for x in mp['bullets'])+'</ul>'+mini(mp['mini']))
    P('</div><div class="pb"><a class="btn" href="#">%s</a></div></section>'%mp['btn'])
    h=c['hh']
    P('<section class="panel hh"><div class="ph"><span class="ic">&#10084;&#65039;</span><div><h2>HEART HEALTH</h2>'
      '<p>BLOOD PRESSURE &amp; RESTING HEART RATE &#183; CURRENT MEASUREMENTS</p></div></div>')
    P('<div class="body"><div class="heartwrap"><img src="%s" alt="3D anatomical heart with an ECG trace">'
      '<svg class="ecg" viewBox="0 0 300 34" preserveAspectRatio="none"><polyline points="0,19 30,19 38,19 42,7 46,29 50,14 54,19 90,19 98,19 102,8 106,28 110,15 114,19 165,19 173,19 177,7 181,29 185,14 189,19 235,19 243,19 247,8 251,28 255,15 259,19 300,19" stroke="%s"/></svg></div>'%(HEART,h['ecg']))
    P('<div class="tiles">')
    for lbl,val,unit,tagcls,tagt in h['tiles']:
        P('<div class="tile"><small>%s</small><b>%s</b><small>%s</small><u class="tag %s">%s</u></div>'%(lbl,val,unit,tagcls,tagt))
    P('</div><ul class="li">'+''.join('<li>%s</li>'%x for x in h['bullets'])+'</ul>'+mini(h['mini']))
    P('</div><div class="pb"><a class="btn" href="#">%s</a></div></section>'%h['btn'])
    x=c['blood']
    P('<section class="panel bx"><div class="ph"><span class="ic">&#129514;</span><div><h2>%s</h2><p>%s</p></div></div>'%(x['name'],x['sub']))
    P('<div class="body"><div class="herofig"><img src="%s" alt="3D render of red blood cells, plasma and molecular chains representing the blood and hormone panel"></div>'%BLOOD_ART)
    P('<h3 class="ch-h">MODEL INPUTS &#183; %d MARKERS</h3>'%len(x['model']))
    P('<div class="bloodrow">')
    for lbl,val,ref,tagcls,tagt in x['model']:
        P('<div class="bm"><span>%s<small>ref %s</small></span><b>%s<span class="tag %s">%s</span></b></div>'%(lbl,ref,val,tagcls,tagt))
    P('</div>')
    P('<h3 class="ch-h">REPORTED, NOT SCORED</h3>')
    P('<div class="bloodrow">')
    for lbl,val,ref,tagcls,tagt in x['extra']:
        P('<div class="bm"><span>%s<small>ref %s</small></span><b>%s<span class="tag %s">%s</span></b></div>'%(lbl,ref,val,tagcls,tagt))
    P('</div><p class="disc">%s</p></div>'%x['note'])
    P('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%x['btn'])

    a=c['ba']
    P('<section class="panel ba wide"><div class="ph"><span class="ic">&#128202;</span><div><h2>BIOMETRIC AGE</h2><p>%s</p></div></div>'%a['sub'])
    P('<div class="body">')
    P('<div class="ba-top">')
    P('<div class="gaugewrap"><div class="gauge">'+ring(a['pct'],a['col'])+'<div class="ctr"><small>BIOMETRIC AGE</small><b>%s</b><em>years</em></div></div></div>')
    P('<div class="deltapane %s"><u>CHRONOLOGICAL %s</u><b>%s</b><u>%s</u><span>%s</span><i>%s</i></div>'%(a['dcls'],a['chrono'],a['delta'],a['dlabel'],a['dsub'],c['meta']['date']))
    P('</div>')
    P('<h3 class="ch-h">BIOMETRIC AGE AGAINST CHRONOLOGICAL AGE</h3>')
    P('<div class="chart">'+delta_chart(a['delta_series'],a['delta_labels'])+trend_legend(a['delta_series'])+'</div>')
    if a.get('delta_note'): P('<p class="disc">%s</p>'%a['delta_note'])
    P('<h3 class="ch-h">%s</h3>'%a['prog_head'])
    P('<div class="chart">'+trend_chart(a['trend'],a['trend_labels'])+trend_legend(a['trend'])+'</div>')
    if a.get('trend_note'): P('<p class="disc">%s</p>'%a['trend_note'])
    P('<h3 class="ch-h">SOURCE DOCUMENTS ON FILE</h3>')
    P('<div class="docs">')
    for n,d in c['docs']:
        P('<div class="doc"><span>%s<small>%s</small></span><em>ON FILE</em></div>'%(n,d))
    P('</div><p class="disc">Documents are listed for reference. Source files are held securely and are not downloadable from this page.</p>')
    P('</div>')
    P('</section>')

    P('<div class="two two-single"><section class="card"><h2>NEXT STEPS</h2><div class="steps">')
    for i,(t,s2) in enumerate(c['steps'],1):
        P('<div class="step"><i>%d</i><div><b>%s</b><small>%s</small></div></div>'%(i,t,s2))
    P('</div></section>')

    P('</div><footer><div class="l">AGING?F***THAT! &#124; LONGER. STRONGER. HEALTHIER.</div><div class="r">WWW.AGINGFTHAT.COM</div></footer>')
    P('<script>(function(){document.querySelectorAll("a.btn[href=\\u0022#\\u0022]").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();});});})();</script></body></html>')
    return "\n".join(A)

STEPS=[("Review Your Results","Read what each panel measures."),
       ("Book a Consultation","Go through the findings with Lee."),
       ("Personalised Plan","Interventions across the 10 tenets."),
       ("Track Progress","Re-measure and confirm the change.")]
DOCS=[("DEXA Scan Report","14 Oct 2024, 21 Dec 2024, 25 Apr 2025"),
      ("Biomechanical Assessment","Posture, alignment and movement"),
      ("AFT Bespoke Blood Panel","Drawn 08 Oct 2026 &#183; 5 markers scored"),
      ("Blood Pressure Log","Home and in-clinic readings"),
      ("Biometric Age Summary","Composite model output")]

ex=dict(title="Example Client Report — Biometric Age Assessment | AGING?F***THAT!",
 desc="An example AFT biometric age assessment dashboard: body composition, movement and posture, heart health, blood markers and estimated biological age.",
 slug="dashboard.html",sub="BIOMETRIC AGE ASSESSMENT DASHBOARD",robots="index,follow",
 notice="ILLUSTRATION ONLY &#183; MOCK DATA",
 meta=dict(name="John Smith",date="12 OCT 2026",program="Elite",status="Client",dot=""),
 bc=dict(src="DEXA &#183; 4 MODEL INPUTS &#183; 34% OF THE SCORE",
   rows=[("Body fat %","21.0%",'<span class="tag warn">8% WT</span>'),
         ("Lean mass","52.0 kg",'<span class="tag warn">9% WT</span>'),
         ("Bone density T-score","&#8722;1.4",'<span class="tag warn">8% WT</span>'),
         ("Visceral fat area","142 cm&#178;",'<span class="tag warn">9% WT</span>')],
   chips=["Body fat","Lean mass","Bone density","Visceral area"],
   mini=[("Body fat",("21.0%",74),RED),("Lean mass",("52.0 kg",58),AMBER),("Visceral area",("142",82),RED),("Bone density",("&#8722;1.4",70),AMBER)],
   btn="VIEW FULL DEXA SCAN REPORT"),
 mp=dict(silo=[AMBER,GREEN,GREEN,AMBER],
   bullets=["Forward head posture","Anterior pelvic tilt","Reduced spinal alignment","Postural imbalance detected","Personalised recommendations"],
   mini=[("Head shift",("1.40cm L",62),AMBER),("Shoulders",("0.77cm R",42),GREEN),("Ribcage",("0.44cm L",30),GREEN),("Pelvis",("2.46cm L",74),AMBER),("Knees",("0.60cm L",32),GREEN)],
   btn="FULL REPORT"),
 hh=dict(ecg=RED,
   tiles=[("Blood Pressure","140/98","mmHg","bad","ELEVATED"),("Resting Heart Rate","76","bpm","warn","ABOVE OPTIMAL")],
   bullets=["Blood pressure above optimal range","Resting heart rate elevated","May benefit from improved fitness","Supports cardiovascular health focus"],
   mini=[("Systolic",("140",78),RED),("Diastolic",("98",72),RED),("Resting HR",("76",58),AMBER)],
   btn="FULL REPORT"),
 ba=dict(sub="BIOMETRIC AGE &#183; COMPOSITE OF 12 WEIGHTED MARKERS",pct=72,col=RED,
   bio="72",chrono="62",delta="+10 yrs",dcls="bad",dlabel="OLDER THAN CHRONOLOGICAL",
   dsub="A composite of 72 gives a biometric age 10 years above chronological age.",
   delta_labels=["2Y AGO","1Y AGO","NOW","+1Y","+2Y"],
   delta_series=[dict(n="Chronological",c="#8fb8cc",vals=[60,61,62,63,64],lbl="CHRONO 64"),
                 dict(n="Biometric",c="#ff4b4b",vals=[77,75,72,68,64],nh=3,lbl="BIO 64")],
   delta_note="Solid lines are on file. The dashed section is an extrapolation from the recorded trend, not a measurement or a forecast, and it assumes the current lifestyle continues unchanged.",
   prog_head="THREE-YEAR PROGRESSION &#183; DEXA OUTPUTS AND BIOMETRIC AGE",
   trend=[dict(n="Biometric age",c="#ff4b4b",vals=[77,75,72],lbl="Biometric age"),
          dict(n="Body fat %",c="#FF9F1C",vals=[24.6,22.9,21.0],lbl="Body fat %"),
          dict(n="Lean mass kg",c="#2BC7FF",vals=[50.4,51.2,52.0],lbl="Lean mass kg"),
          dict(n="Visceral area cm&#178;",c="#A855F7",vals=[150,146,142],lbl="Visceral area cm&#178;"),
          dict(n="Bone density T-score",c="#21c97a",vals=[-1.9,-1.65,-1.4],lbl="Bone density T-score")],
   trend_labels=["2Y AGO","1Y AGO","NOW"],
   trend_note="Illustrative. The NOW values match the DEXA figures in Body Composition. Bone density is plotted against its own scale.",
   btn=None),
 blood=dict(name="BLOOD WORK",sub="THE BLOOD &amp; HORMONE DOMAIN &#183; 42% OF THE MODEL",
   model=[("HbA1c mmol/mol","41","&lt;42","warn","WATCH"),
          ("hsCRP","1.8 mg/L","&lt;1.0","warn","SLIGHTLY HIGH"),
          ("Homocysteine","20.4 &#181;mol/L","3.7&#8211;13.9","bad","ELEVATED"),
          ("Total testosterone","19.8 nmol/L","6.51&#8211;23.74","ok","WITHIN"),
          ("Free testosterone","330 pmol/L","170&#8211;660","ok","WITHIN")],
   extra=[("HbA1c %HbA1c","5.9","&lt;6.0","warn","WATCH"),
          ("Albumin","42 g/L","32&#8211;48","ok","WITHIN"),
          ("SHBG","36 nmol/L","17.33&#8211;71.5","ok","WITHIN"),
          ("Cortisol","398 nmol/L","145.4&#8211;619.4","ok","WITHIN")],
   note="Illustrative sample figures. The five model inputs above are the blood and hormone markers the AFT Bio Age Model scores. Cortisol, SHBG, albumin and the percentage HbA1c are reported for context but carry no weight in the model.",
   btn="FULL REPORT"),
 steps=STEPS,docs=DOCS)

rl=dict(title="Client Report — Biometric Age Assessment | AGING?F***THAT!",
 desc="An AFT biometric age assessment dashboard: body composition, movement and posture, heart health, blood markers and biological age.",
 slug="example-report.html",sub="BIOMETRIC AGE ASSESSMENT DASHBOARD",robots="index,follow",
 banner=None,
 meta=dict(name="Lee C. Stonehouse",date="08 OCT 2026",program="Elite",status="Client",dot=""),
 bc=dict(src="DEXA &#183; 4 MODEL INPUTS &#183; 34% OF THE SCORE",
   rows=[("Body fat %","9.6%",'<span class="tag ok">8% WT</span>'),
         ("Lean mass","74.6 kg",'<span class="tag ok">9% WT</span>'),
         ("Bone density T-score","awaiting report",'<span class="tag warn">8% WT</span>'),
         ("Visceral fat area","54.6 cm&#178;",'<span class="tag ok">9% WT</span>')],
   chips=["Body fat","Lean mass","Bone density","Visceral area"],
   mini=[("Body fat",("9.6%",90),GREEN),("Lean mass",("74.6 kg",92),GREEN),("Visceral area",("54.6",95),GREEN),("Bone density",("&#8212;",50),AMBER)],
   btn="VIEW FULL DEXA SCAN REPORT"),
 mp=dict(silo=[AMBER,GREEN,GREEN,AMBER],
   bullets=["Forward head posture","Anterior pelvic tilt","Reduced spinal alignment","Measured against 25 Apr 2025","Personalised recommendations"],
   mini=[("Head shift",("1.40cm L",62),AMBER),("Shoulders",("0.77cm R",42),GREEN),("Ribcage",("0.44cm L",30),GREEN),("Pelvis",("2.46cm L",74),AMBER),("Knees",("0.60cm L",32),GREEN)],
   btn="FULL REPORT"),
 hh=dict(ecg=GREEN,
   tiles=[("Blood Pressure","120/78","mmHg","ok","GOOD"),("Resting Heart Rate","47","bpm","ok","EXCEPTIONAL")],
   bullets=["Blood pressure within range","Resting heart rate exceptional","Supports cardiovascular health focus","Track and monitor progress"],
   mini=[("Systolic",("120",95),GREEN),("Diastolic",("78",90),GREEN),("Resting HR",("47",98),GREEN)],
   btn="FULL REPORT"),
 ba=dict(sub="BIOLOGICAL AGE &#183; COMPOSITE OF 12 WEIGHTED MARKERS",pct=75,col=GREEN,
   bio="47",chrono="63",delta="&#8722;16 yrs",dcls="good",dlabel="YOUNGER THAN CHRONOLOGICAL",
   dsub="A composite of 75 gives a biometric age 16 years below chronological age.",
   delta_labels=["NOW","+1Y","+2Y"],
   delta_series=[dict(n="Chronological",c="#8fb8cc",vals=[63,64,65],lbl="CHRONO 65"),
                 dict(n="Biometric",c="#21c97a",vals=[47,45,43],nh=1,lbl="BIO 43")],
   delta_note="Real data at NOW. Earlier biometric ages are not on file, so nothing is drawn before the current assessment. The dashed section is an extrapolation, not a measurement or a forecast.",
   prog_head="THREE-YEAR PROGRESSION &#183; DEXA OUTPUTS AND BIOMETRIC AGE",
   trend=[dict(n="Biometric age",c="#21c97a",vals=[47],lbl="Biometric age"),
          dict(n="Body fat %",c="#FF9F1C",vals=[13.4,11.5,9.6],lbl="Body fat %"),
          dict(n="Lean mass kg",c="#2BC7FF",vals=[71.2,72.9,74.6],lbl="Lean mass kg"),
          dict(n="Visceral area cm&#178;",c="#A855F7",vals=[72.0,63.0,54.6],lbl="Visceral area cm&#178;")],
   trend_labels=["2Y AGO","1Y AGO","NOW"],
   trend_note="The NOW values match the DEXA figures in Body Composition. Bone density awaits the DEXA bone report. Only one biometric age is on file, so it is shown as a single point.",
   btn=None),
 blood=dict(name="BLOOD WORK",sub="THE BLOOD &amp; HORMONE DOMAIN &#183; 42% OF THE MODEL &#183; 08 OCT 2026",
   model=[("HbA1c mmol/mol","32","&lt;42","ok","NORMAL"),
          ("hsCRP","not tested","&lt;1.0","absent","NO RESULT"),
          ("Homocysteine","22.46 &#181;mol/L","3.7&#8211;13.9","bad","FLAGGED"),
          ("Total testosterone","43.58 nmol/L","6.51&#8211;23.74","bad","FLAGGED"),
          ("Free testosterone","976.35 pmol/L","170&#8211;660","bad","FLAGGED")],
   extra=[("HbA1c %HbA1c","5.08","&lt;6.0","ok","NORMAL"),
          ("Albumin","45 g/L","32&#8211;48","ok","WITHIN"),
          ("SHBG","48.41 nmol/L","17.33&#8211;71.5","ok","WITHIN"),
          ("Cortisol","261.69 nmol/L","145.4&#8211;619.4","ok","WITHIN")],
   note="Results from the AFT Bespoke Blood Panel, drawn 08 Oct 2026. The five model inputs are the blood and hormone markers the AFT Bio Age Model scores; hsCRP is a model input that this panel does not currently test for, so it scores neutral. Cortisol, SHBG, albumin and the percentage HbA1c are reported for context but carry no weight. Automated report, not reviewed by a physician.",
   btn="EDIT READINGS"),
 steps=STEPS,docs=DOCS)

open("dashboard.html","w",encoding="utf-8").write(page(ex))
open("example-report.html","w",encoding="utf-8").write(page(rl))
print("dashboard.html", len(page(ex).encode()))
print("example-report.html", len(page(rl).encode()))
