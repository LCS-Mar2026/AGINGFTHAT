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

GREEN="#21c97a"; AMBER="#FF9F1C"; RED="#ff4b4b"; CYAN="#2BC7FF"; VIOLET="#A855F7"

def ring(pct,col):
    r=64.0; circ=2*math.pi*r; dash=circ*pct/100.0
    return ('<svg viewBox="0 0 150 150">'
            '<circle cx="75" cy="75" r="%.0f" fill="none" stroke="#0d2b3c" stroke-width="12"/>'
            '<circle cx="75" cy="75" r="%.0f" fill="none" stroke="%s" stroke-width="12" stroke-linecap="round" '
            'stroke-dasharray="%.1f %.1f"/></svg>')%(r,r,col,dash,circ-dash)

def trend_chart(series, labels, note="", top=None):
    """Three-point trend chart. Series order matches the legend."""
    W,H = 300,118; padL,padR,padT,padB = 30,10,10,20
    iw=W-padL-padR; ih=H-padT-padB
    lo=min(min(x['vals']) for x in series) if not top else 0; hi=max(max(x['vals']) for x in series) if not top else top
    if hi==lo: hi=lo+1
    pad=(hi-lo)*0.18; lo-=pad; hi+=pad
    X=lambda i: padL+iw*(i/(len(labels)-1))
    Y=lambda v: padT+ih*(1-(v-lo)/(hi-lo))
    p=['<svg viewBox="0 0 %d %d">'%(W,H)]
    for k in range(4):
        y=padT+ih*k/3.0
        p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#12405a" stroke-width="1"/>'%(padL,y,W-padR,y))
    for i,lb in enumerate(labels):
        p.append('<text x="%.1f" y="%d" text-anchor="middle" fill="#8fb8cc" font-size="8">%s</text>'%(X(i),H-3,lb))
    for x in series:
        pts=" ".join("%.1f,%.1f"%(X(i),Y(v)) for i,v in enumerate(x['vals']))
        p.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'%(pts,x['c']))
        for i,v in enumerate(x['vals']):
            p.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>'%(X(i),Y(v),x['c']))
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
      '<p>CHIROPRACTIC ANALYSIS &#183; MOVEMENT &#183; ALIGNMENT &#183; POSTURE</p></div></div>')
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
    P('<div class="body"><div class="herofig"><img src="%s" alt="3D render of red blood cells, plasma and molecular chains representing a blood and hormone panel"></div>'%BLOOD_ART)
    P('<div class="bloodrow">')
    for lbl,val,ref,tagcls,tagt in x['rows']:
        P('<div class="bm"><span>%s<small>ref %s</small></span><b>%s<span class="tag %s">%s</span></b></div>'%(lbl,ref,val,tagcls,tagt))
    P('</div><p class="disc">%s</p></div>'%x['note'])
    P('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%x['btn'])

    a=c['ba']
    P('<section class="panel ba wide"><div class="ph"><span class="ic">&#128202;</span><div><h2>BIOMETRIC AGE</h2><p>%s</p></div></div>'%a['sub'])
    P('<div class="body"><div class="herofig"><img src="%s" alt="3D anatomical scan figure representing a biometric age assessment"></div>'%HERO_ART)
    P('<div class="gaugewrap"><div class="gauge">'+ring(a['pct'],a['col'])+'<div class="ctr"><small>Your Biometric Age</small><b>%s</b><em>years</em><u>Chronological Age %s</u></div></div></div>'%(a['bio'],a['chrono']))
    P('</div><div class="ba-chart"><div class="chart">'+trend_chart(a["trend"],a["trend_labels"],top=a.get("trend_max"))+trend_legend(a["trend"])+'</div>')
    if a.get("trend_note"): P('<p class="disc">%s</p>'%a["trend_note"])
    P('</div></div>')
    if a.get('btn'):
        P('<div class="pb"><a class="btn" href="#">%s</a></div>'%a['btn'])
    P('</section>')

    P('<div class="two"><section class="card"><h2>NEXT STEPS</h2><div class="steps">')
    for i,(t,s) in enumerate(c['steps'],1):
        P('<div class="step"><i>%d</i><div><b>%s</b><small>%s</small></div></div>'%(i,t,s))
    P('</div></section><section class="card"><h2>SOURCE DOCUMENTS</h2><div class="docs">')
    for n,d in c['docs']:
        P('<div class="doc"><span>%s<small>%s</small></span><em>ON FILE</em></div>'%(n,d))
    P('</div><p class="disc">Documents are listed for reference. Source files are held securely and not downloadable from this page.</p></section></div>')
    P('</div><footer><div class="l">AGING?F***THAT! &#124; LONGER. STRONGER. HEALTHIER.</div><div class="r">WWW.AGINGFTHAT.COM</div></footer>')
    P('<script>(function(){document.querySelectorAll("a.btn[href=\\u0022#\\u0022]").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();});});})();</script></body></html>')
    return "\n".join(A)

STEPS=[("Review Your Results","Read what each panel measures."),
       ("Book a Consultation","Go through the findings with Lee."),
       ("Personalised Plan","Interventions across the 10 tenets."),
       ("Track Progress","Re-measure and confirm the change.")]
DOCS=[("DEXA Scan Report","14 Oct 2024, 21 Dec 2024, 25 Apr 2025"),
      ("Chiropractic Assessment","Posture, alignment and movement"),
      ("AFT Bespoke Panel 2","Sussex Pathology &#183; 7 markers scored"),
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
   btn="FULL BIOMECHANICAL REPORT"),
 hh=dict(ecg=RED,
   tiles=[("Blood Pressure","140/98","mmHg","bad","ELEVATED"),("Resting Heart Rate","76","bpm","warn","ABOVE OPTIMAL")],
   bullets=["Blood pressure above optimal range","Resting heart rate elevated","May benefit from improved fitness","Supports cardiovascular health focus"],
   mini=[("Systolic",("140",78),RED),("Diastolic",("98",72),RED),("Resting HR",("76",58),AMBER)],
   btn="EDIT READINGS"),
 ba=dict(sub="YOUR ESTIMATED BIOLOGICAL AGE &#183; PROVISIONAL",pct=88,col=RED,
   trend=[dict(n="DEXA domain",c="#2BC7FF",vals=[52,57,61]),
          dict(n="Fitness domain",c="#21c97a",vals=[40,45,48]),
          dict(n="Blood &amp; hormones",c="#FF9F1C",vals=[58,61,64]),
          dict(n="Vital signs domain",c="#A855F7",vals=[30,35,38])],
   trend_labels=["T1","T2","T3"],
   trend_max=100,
   trend_note="Each line is one of the four model domains, scored out of its own points and scaled to 100. Together the four domains are the composite that sets the biometric age.",
   bio="77",chrono="62",
   btn=None),
 blood=dict(name="BLOOD WORK",sub="7 MARKERS SCORED IN THE MODEL &#183; PLUS CORTISOL, NOT SCORED",
   rows=[("<b>1. HbA1c</b> mmol/mol","41","&lt;42","warn","WATCH"),
         ("<b>2. HbA1c</b> %HbA1c","5.9","&lt;6.0","warn","WATCH"),
         ("<b>3. Homocysteine</b>","20.4 &#181;mol/L","3.7&#8211;13.9","bad","ELEVATED"),
         ("<b>4. Albumin</b>","42 g/L","32&#8211;48","ok","WITHIN"),
         ("<b>5. SHBG</b>","36 nmol/L","17.33&#8211;71.5","ok","WITHIN"),
         ("<b>6. Testosterone</b>","19.8 nmol/L","6.51&#8211;23.74","ok","WITHIN"),
         ("<b>7. Free Testosterone</b>","330 pmol/L","170&#8211;660","ok","WITHIN"),
         ("<b>hs-CRP</b>","1.8 mg/L","&lt;1.0","warn","SLIGHTLY HIGH"),
         ("<b>Cortisol</b> &#8212; not scored","398 nmol/L","145.4&#8211;619.4","ok","WITHIN")],
   note="Illustrative sample figures in the Bespoke Panel 2 format. Markers 1 to 7 feed the model; cortisol is reported but not scored; hs-CRP here is an illustrative figure; the laboratory does not currently test for it.",
   btn="EDIT READINGS"),
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
   btn="FULL BIOMECHANICAL REPORT"),
 hh=dict(ecg=GREEN,
   tiles=[("Blood Pressure","120/78","mmHg","ok","GOOD"),("Resting Heart Rate","47","bpm","ok","EXCEPTIONAL")],
   bullets=["Blood pressure within range","Resting heart rate exceptional","Supports cardiovascular health focus","Track and monitor progress"],
   mini=[("Systolic",("120",95),GREEN),("Diastolic",("78",90),GREEN),("Resting HR",("47",98),GREEN)],
   btn="EDIT READINGS"),
 ba=dict(sub="YOUR BIOLOGICAL AGE &#183; BASED ON ASSESSMENT METRICS",pct=75,col=GREEN,
   trend=[dict(n="DEXA domain",c="#2BC7FF",vals=[81,86,90]),
          dict(n="Fitness domain",c="#21c97a",vals=[88,92,95]),
          dict(n="Blood &amp; hormones",c="#FF9F1C",vals=[68,74,79]),
          dict(n="Vital signs domain",c="#A855F7",vals=[93,96,98])],
   trend_labels=["T1","T2","T3"],
   trend_max=100,
   trend_note="Each line is one of the four model domains, scored out of its own points and scaled to 100. Together the four domains are the composite that sets the biometric age.",
   bio="47",chrono="63",
   btn=None),
 blood=dict(name="BLOOD WORK",sub="SUSSEX PATHOLOGY &#183; 08 OCT 2026 &#183; 7 MARKERS SCORED, PLUS CORTISOL",
   rows=[("<b>1. HbA1c</b> mmol/mol","32","&lt;42","ok","NORMAL"),
         ("<b>2. HbA1c</b> %HbA1c","5.08","&lt;6.0","ok","NORMAL"),
         ("<b>3. Homocysteine</b>","22.46 &#181;mol/L","3.7&#8211;13.9","bad","FLAGGED"),
         ("<b>4. Albumin</b>","45 g/L","32&#8211;48","ok","WITHIN"),
         ("<b>5. SHBG</b>","48.41 nmol/L","17.33&#8211;71.5","ok","WITHIN"),
         ("<b>6. Testosterone</b>","43.58 nmol/L","6.51&#8211;23.74","bad","FLAGGED"),
         ("<b>7. Free Testosterone</b>","976.35 pmol/L","170&#8211;660","bad","FLAGGED"),
         ("<b>hs-CRP</b>","not tested","&lt;1.0","absent","NO RESULT"),
         ("<b>Cortisol</b> &#8212; not scored","261.69 nmol/L","145.4&#8211;619.4","ok","WITHIN")],
   note="Results as reported by Sussex Pathology, 08 Oct 2026. Markers 1 to 7 feed the biometric age model; cortisol is reported but not scored; hs-CRP is a model input this panel does not currently test for, so it scores neutral. Automated report, not reviewed by a physician.",
   btn="EDIT READINGS"),
 steps=STEPS,docs=DOCS)

open("dashboard.html","w",encoding="utf-8").write(page(ex))
open("example-report.html","w",encoding="utf-8").write(page(rl))
print("dashboard.html", len(page(ex).encode()))
print("example-report.html", len(page(rl).encode()))
