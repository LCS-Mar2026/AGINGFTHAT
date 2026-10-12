# -*- coding: utf-8 -*-
"""Dashboard generator. ONE template, data sets per client.
dashboard.html      = example client (sample data, Elite, DEXA, Bespoke Panel 2)
example-report.html = Lee Stonehouse, real verified data
All colour-coding derives from the data. No photographs. SVG charts only."""
import math

CSS = "<style>\n" + open("dashboard.css", encoding="utf-8").read() + "\n</style>"

EXTRA_CSS = """<style>
.gaugewrap{display:grid;place-items:center;margin:4px 0 10px}
.gauge{position:relative;width:158px;height:158px}
.gauge svg{display:block;width:158px;height:158px;transform:rotate(-90deg)}
.gauge .ctr{position:absolute;inset:0;display:grid;place-content:center;text-align:center;padding:0 14px}
.gauge .ctr small{font-size:8px;letter-spacing:.1em;color:var(--muted);text-transform:uppercase;line-height:1.25}
.gauge .ctr b{font-size:30px;font-weight:900;line-height:1;display:block;margin:3px 0 2px}
.gauge .ctr em{font-style:normal;font-size:8.5px;letter-spacing:.07em;color:var(--muted);display:block}
.gauge .ctr u{text-decoration:none;display:block;font-size:9px;font-weight:800;color:#fff;margin-top:3px}
.ecg{display:block;width:100%;height:46px;margin:0 0 8px}
.ecg polyline{fill:none;stroke-width:2.4;stroke-linejoin:round;stroke-linecap:round}
.chart{background:#04202e;border:1px solid #14415a;border-radius:9px;padding:10px 9px 6px;margin-bottom:10px}
.chart svg{display:block;width:100%;height:152px}
.chart .gl{stroke:#12405a;stroke-width:1}
.chart .ax{fill:#8fb8cc;font-size:8.5px;letter-spacing:.04em}
.chart .lg{display:flex;flex-wrap:wrap;gap:4px 12px;margin-top:6px}
.chart .lg span{font-size:9px;color:var(--muted);display:flex;align-items:center;gap:5px}
.chart .lg i{width:12px;height:3px;border-radius:2px;display:inline-block}
.figpair{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:9px}
.figpair img{width:100%;height:auto;border-radius:8px;border:1px solid #14415a;display:block;background:#02101a}
.mini{display:grid;gap:6px;margin:0 0 10px}
.minirow{display:grid;grid-template-columns:1fr 62px;align-items:center;gap:8px;font-size:10.5px;color:var(--muted)}
.minirow .track{height:8px;border-radius:99px;background:#0d2b3c;overflow:hidden}
.minirow b{font-size:10.5px;text-align:right;color:#dff2fb}
.note2{font-size:9.5px;color:#7899a9;margin:6px 0 0;line-height:1.45}
.absent{background:#152a3a;color:#8fb8cc}
</style>"""

GREEN="#21c97a"; AMBER="#FF9F1C"; RED="#ff4b4b"; CYAN="#2BC7FF"; VIOLET="#A855F7"

def ring(pct, colour):
    r=66.0; circ=2*math.pi*r; dash=circ*pct/100.0
    return ('<svg viewBox="0 0 158 158">'
            '<circle cx="79" cy="79" r="%.0f" fill="none" stroke="#0d2b3c" stroke-width="13"/>'
            '<circle cx="79" cy="79" r="%.0f" fill="none" stroke="%s" stroke-width="13" '
            'stroke-linecap="round" stroke-dasharray="%.1f %.1f"/></svg>')%(r,r,colour,dash,circ-dash)

def line_chart(series, labels, unit_hint=""):
    W,H=300,152; padL,padR,padT,padB=34,8,10,20
    iw=W-padL-padR; ih=H-padT-padB
    lo=min(min(s['vals']) for s in series); hi=max(max(s['vals']) for s in series)
    if hi==lo: hi=lo+1
    pad=(hi-lo)*0.16; lo-=pad; hi+=pad
    X=lambda i: padL+iw*(i/(len(labels)-1))
    Y=lambda v: padT+ih*(1-(v-lo)/(hi-lo))
    p=['<svg viewBox="0 0 %d %d">'%(W,H)]
    for k in range(4):
        y=padT+ih*k/3.0
        p.append('<line class="gl" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'%(padL,y,W-padR,y))
        p.append('<text class="ax" x="2" y="%.1f">%.0f</text>'%(y+3, hi-(hi-lo)*k/3.0))
    for i,lb in enumerate(labels):
        p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>'%(X(i),H-4,lb))
    for s in series:
        pts=" ".join("%.1f,%.1f"%(X(i),Y(v)) for i,v in enumerate(s['vals']))
        p.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>'%(pts,s['c']))
        for i,v in enumerate(s['vals']):
            p.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>'%(X(i),Y(v),s['c']))
    p.append('</svg>')
    return "".join(p)

def legend(series):
    return '<div class="lg">'+"".join('<span><i style="background:%s"></i>%s</span>'%(s['c'],s['n']) for s in series)+'</div>'

def page(cfg):
    P=[]
    A=P.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
    A('<title>%s</title>'%cfg['title'])
    A('<meta name="description" content="%s">'%cfg['desc'])
    A('<link rel="canonical" href="https://agingfthat.com/%s">'%cfg['slug'])
    A('<meta name="robots" content="%s">'%cfg['robots'])
    A('<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">')
    A(CSS); A(EXTRA_CSS); A('</head><body>')

    A('<header class="hero"><h1 class="wm">AGING?<em>F***</em>THAT!</h1><p class="sub">%s</p>'
      '<p class="strap">MEASURE &#124; ANALYSE &#124; OPTIMISE &#124; TRACK STATUS</p></header>'%cfg['sub'])
    m=cfg['meta']
    A('<div class="metabar"><div>Name<b>%s</b></div><div>Assessment Date<b>%s</b></div>'
      '<div>Program<b>%s</b></div><div>Status<b>%s<span class="dot %s"></span></b></div></div>'
      %(m['name'],m['date'],m['program'],m['status'],m['dot']))
    A('<div class="wrap">')
    if cfg.get('banner'): A('<p class="disc" style="margin:0 0 12px">%s</p>'%cfg['banner'])
    A('<div class="panels">')

    bc=cfg['bc']
    A('<section class="panel bc"><div class="ph"><span class="ic">&#128100;</span><div><h2>BODY COMPOSITION</h2><p>%s</p></div></div>'%bc['src'])
    A('<div class="rows">')
    for lbl,val,tag in bc['rows']:
        A('<div class="row"><span>%s</span><b>%s%s</b></div>'%(lbl,val,tag))
    A('</div>')
    A('<div class="chart">'+line_chart(bc['series'],['T1','T2','T3'])+legend(bc['series'])+'</div>')
    A('<p class="note2">%s</p>'%bc['note'])
    A('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%bc['btn'])

    mp=cfg['mp']
    A('<section class="panel mp"><div class="ph"><span class="ic">&#128694;</span><div><h2>MOVEMENT &amp; POSTURE</h2><p>CHIROPRACTIC ANALYSIS &#183; MOVEMENT &#183; ALIGNMENT &#183; POSTURE</p></div></div>')
    A('<div class="figpair"><img src="%s" alt="3D anatomical posture figure, front view, with a vertical alignment axis and offset markers at head, shoulders, ribcage, pelvis and knees" loading="lazy">'
      '<img src="%s" alt="3D anatomical posture figure, side view, with a vertical plumb line and angle markers at the cervical spine, thoracic curve, lumbar and pelvis" loading="lazy"></div>'%(mp['img1'],mp['img2']))
    A('<ul class="li">'+''.join('<li>%s</li>'%x for x in mp['bullets'])+'</ul>')
    A('<div class="mini">')
    for lbl,val,cls in mp['offsets']:
        A('<div class="minirow"><span>%s</span><span class="track"><i class="%s" style="width:%d%%"></i></span><b>%s</b></div>'%(lbl,cls,val[1],val[0]))
    A('</div>')
    A('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%mp['btn'])

    hh=cfg['hh']
    A('<section class="panel hh"><div class="ph"><span class="ic">&#10084;&#65039;</span><div><h2>HEART HEALTH</h2><p>BLOOD PRESSURE &amp; RESTING HEART RATE &#183; CURRENT MEASUREMENTS</p></div></div>')
    A('<svg class="ecg" viewBox="0 0 300 46" preserveAspectRatio="none"><polyline points="0,26 34,26 42,26 46,10 50,40 54,20 58,26 96,26 104,26 108,12 112,38 116,22 120,26 170,26 178,26 182,11 186,39 190,21 194,26 240,26 248,26 252,12 256,38 260,22 264,26 300,26" stroke="%s"/></svg>'%hh['ecg'])
    A('<div class="tiles">')
    for lbl,val,unit,tagcls,tagt in hh['tiles']:
        A('<div class="tile"><small>%s</small><b>%s</b><small>%s</small><u class="tag %s">%s</u></div>'%(lbl,val,unit,tagcls,tagt))
    A('</div>')
    A('<ul class="li">'+''.join('<li>%s</li>'%x for x in hh['bullets'])+'</ul>')
    A('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%hh['btn'])

    ba=cfg['ba']
    A('<section class="panel ba"><div class="ph"><span class="ic">&#128202;</span><div><h2>BIOMETRIC AGE</h2><p id="baSub">%s</p></div></div>'%ba['sub'])
    A('<div class="gaugewrap"><div class="gauge">'+ring(ba['pct'],ba['colour'])+
      '<div class="ctr"><small>Your Biometric Age</small><b>%s</b><em>years</em><u>Chronological Age %s</u></div></div></div>'%(ba['bio'],ba['chrono']))
    A('<div class="strip %s">%s</div>'%('good' if ba['colour']==GREEN else ('bad' if ba['colour']==RED else 'warn'), ba['strip']))
    A('<p class="note">A healthier, stronger longer life is within your control.</p>')
    A('<div class="mini">')
    for lbl,val,cls in ba['rows']:
        A('<div class="minirow"><span>%s</span><span class="track"><i class="%s" style="width:%d%%"></i></span><b>%s</b></div>'%(lbl,cls,val[1],val[0]))
    A('</div>')
    A('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%ba['btn'])
    A('</div>')

    bx=cfg['blood']
    A('<section class="panel bx bloods" style="margin-top:12px"><div class="ph"><span class="ic">&#129514;</span><div><h2>%s</h2><p>%s</p></div></div>'%(bx['name'],bx['sub']))
    A('<table class="mk"><tr><th>Marker</th><th>Result</th><th>Reference</th><th>Status</th></tr>')
    for r in bx['rows']:
        A('<tr><td>%s</td><td class="n">%s</td><td>%s</td><td><span class="tag %s">%s</span></td></tr>'%r)
    A('</table>')
    A('<p class="disc">%s</p>'%bx['note'])
    A('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%bx['btn'])

    A('<div class="two"><section class="card"><h2>NEXT STEPS</h2><div class="steps">')
    for i,(t,s) in enumerate(cfg['steps'],1):
        A('<div class="step"><i>%d</i><div><b>%s</b><span>%s</span></div></div>'%(i,t,s))
    A('</div></section>')
    A('<section class="card"><h2>SOURCE DOCUMENTS</h2><div class="docs">')
    for name,detail in cfg['docs']:
        A('<div class="doc"><span>%s<small>%s</small></span><em>ON FILE</em></div>'%(name,detail))
    A('</div><p class="disc">Documents are listed for reference. Source files are held securely and are not downloadable from this page.</p></section></div>')
    A('</div>')
    A('<footer><div class="l">AGING?F***THAT! &#124; LONGER. STRONGER. HEALTHIER.</div><div class="r">WWW.AGINGFTHAT.COM</div></footer>')
    A('<script>(function(){document.querySelectorAll("a.btn[href=\\u0022#\\u0022]").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();});});})();</script>')
    A('</body></html>')
    return "\n".join(P)

STEPS=[("Review Your Results","Read what each panel measures and what it means."),
       ("Book a Consultation to Discuss","Go through the findings with Lee."),
       ("Personalised Plan &amp; Recommendations","Interventions across the 10 tenets."),
       ("Take Action &amp; Track Progress","Re-measure and confirm the change.")]
P1="https://cdn.marblism.com/5BmFVv925aB.webp"
P2="https://cdn.marblism.com/QBo1eqeRDxl.webp"

docs_common=[
 ("DEXA scan","14 Oct 2024, 21 Dec 2024 and 25 Apr 2025 &#183; body composition and bone density"),
 ("Chiropractic assessment report","Posture, alignment and movement findings, with front and side imagery"),
 ("AFT Bespoke Panel 2","Sussex Pathology &#183; 7 scored markers plus cortisol"),
 ("Heart rate and blood pressure log","Home and in-clinic readings"),
 ("Biometric age summary","Composite model output, by assessment date")]

# ================================================== EXAMPLE (sample data)
ex_bc=dict(src="DEXA SCAN &#183; T1 / T2 / T3",
 rows=[("Weight","90.0 kg",""),
       ("Muscle Mass","31.4 kg",'<span class="tag bad">LOW</span>'),
       ("Body Fat","28.0%",'<span class="tag bad">HIGH</span>'),
       ("Visceral Fat","14",'<span class="tag bad">HIGH</span>'),
       ("BMI","28.9",'<span class="tag warn">OVERWEIGHT</span>')],
 series=[dict(n="Muscle mass (kg)",c=CYAN,vals=[32.8,32.1,31.4]),
         dict(n="Body fat (%)",c=RED,vals=[25.4,26.7,28.0]),
         dict(n="Visceral fat",c=AMBER,vals=[11,12.5,14]),
         dict(n="BMI",c=VIOLET,vals=[27.6,28.2,28.9])],
 note="Three DEXA assessments at 12-month intervals. Muscle mass falling while body fat and visceral fat rise is the classic midlife pattern.",
 btn="VIEW FULL DEXA SCAN REPORT")

ex_mp=dict(img1=P1,img2=P2,
 bullets=["Forward head posture","Anterior pelvic tilt","Reduced spinal alignment","Postural imbalance detected","Personalised recommendations"],
 offsets=[("Head shift",("1.90cm L",78),RED),("Shoulders",("1.30cm R",62),AMBER),
          ("Ribcage",("1.10cm L",55),AMBER),("Pelvis",("2.90cm L",86),RED),
          ("Knees",("1.20cm L",58),AMBER)],
 btn="EDIT READINGS")

ex_hh=dict(ecg=RED,
 tiles=[("Blood Pressure","140/98","mmHg","bad","ELEVATED"),("Resting Heart Rate","76","bpm","warn","ABOVE OPTIMAL")],
 bullets=["Blood pressure above optimal range","Resting heart rate elevated","May benefit from improved fitness","Supports cardiovascular health focus","Track and monitor progress"],
 btn="EDIT READINGS")

ex_ba=dict(sub="YOUR ESTIMATED BIOLOGICAL AGE &#183; BASED ON LEVEL 1 METRICS",pct=88,colour=RED,
 bio="77",chrono="62",strip="15 YEARS OLDER THAN YOUR ACTUAL AGE",
 rows=[("Biometric vs chronological",("+15 yrs",88),RED),("Model confidence",("High",80),GREEN),("Markers scored",("6 of 7",86),AMBER)],
 btn="EDIT READINGS")

ex_blood=dict(name="AFT BESPOKE PANEL 2",sub="7 MARKERS SCORED IN THE MODEL &#183; PLUS CORTISOL, NOT SCORED",
 rows=[("HbA1c (mmol/mol)","41","&lt;42 normal","warn","WATCH"),
       ("HbA1c %HbA1c (%)","5.9","&lt;6.0 normal","warn","WATCH"),
       ("Homocysteine","20.4 &#181;mol/L","3.7&#8211;13.9","bad","ELEVATED"),
       ("Albumin","42 g/L","32&#8211;48","ok","WITHIN"),
       ("SHBG","36 nmol/L","17.33&#8211;71.5","ok","WITHIN"),
       ("Testosterone","19.8 nmol/L","6.51&#8211;23.74","ok","WITHIN"),
       ("Free Testosterone","330 pmol/L","170&#8211;660","ok","WITHIN"),
       ("hs-CRP","not tested","&lt;1.0","absent","NO RESULT"),
       ("Cortisol &#8212; not scored","398 nmol/L","145.4&#8211;619.4","ok","WITHIN")],
 note="Illustrative sample figures in the Bespoke Panel 2 format. Seven markers feed the model; cortisol is reported but not scored; hs-CRP is a model input that this panel does not currently test for.",
 btn="EDIT READINGS")

ex = page(dict(title="Example Client Report — Biometric Age Assessment Dashboard | AGING?F***THAT!",
 desc="An example biometric age assessment dashboard: body composition, movement and posture, heart health, blood markers and estimated biological age in one view.",
 slug="dashboard.html", sub="BIOMETRIC AGE ASSESSMENT DASHBOARD", robots="index,follow",
 banner="<b>EXAMPLE ONLY.</b> Every figure on this page is illustrative sample data, not a real client record. It shows the format of an AFT assessment dashboard.",
 meta=dict(name="John Smith",date="12 OCT 2026",program="Elite",status="Client",dot=""),
 bc=ex_bc,mp=ex_mp,hh=ex_hh,ba=ex_ba,blood=ex_blood,steps=STEPS,docs=docs_common))

# ================================================== LEE (real, verified)
rl_bc=dict(src="DEXA SCAN &#183; T1 / T2 / T3",
 rows=[("Weight","85.7 kg",""),
       ("Muscle Mass","74.6 kg",'<span class="tag ok">EXCEPTIONAL</span>'),
       ("Body Fat","9.6%",'<span class="tag ok">LEAN</span>'),
       ("Visceral Fat","54.6 cm&#178;",'<span class="tag ok">LOW</span>'),
       ("BMI","22.4",'<span class="tag ok">HEALTHY</span>')],
 series=[dict(n="Muscle mass (kg)",c=CYAN,vals=[71.2,72.9,74.6]),
         dict(n="Body fat (%)",c=GREEN,vals=[13.4,11.5,9.6]),
         dict(n="Visceral fat",c=AMBER,vals=[72.0,63.0,54.6]),
         dict(n="BMI",c=VIOLET,vals=[23.8,23.1,22.4])],
 note="Three DEXA assessments at 12-month intervals. Muscle mass rising while body fat and visceral fat fall is the intended direction of travel.",
 btn="VIEW FULL DEXA SCAN REPORT")

rl_mp=dict(img1=P1,img2=P2,
 bullets=["Forward head posture","Anterior pelvic tilt","Reduced spinal alignment","Measured against the 25 Apr 2025 assessment","Personalised recommendations"],
 offsets=[("Head shift",("1.40cm L",62),AMBER),("Shoulders",("0.77cm R",42),GREEN),
          ("Ribcage",("0.44cm L",30),GREEN),("Pelvis",("2.46cm L",74),AMBER),
          ("Knees",("0.60cm L",32),GREEN)],
 btn="EDIT READINGS")

rl_hh=dict(ecg=GREEN,
 tiles=[("Blood Pressure","120/78","mmHg","ok","GOOD"),("Resting Heart Rate","47","bpm","ok","EXCEPTIONAL")],
 bullets=["Blood pressure within range","Resting heart rate exceptional","Supports cardiovascular health focus","Track and monitor progress"],
 btn="EDIT READINGS")

rl_ba=dict(sub="YOUR BIOLOGICAL AGE &#183; BASED ON ASSESSMENT METRICS",pct=75,colour=GREEN,
 bio="47",chrono="63",strip="16 YEARS YOUNGER THAN YOUR ACTUAL AGE",
 rows=[("Biometric vs chronological",("&#8722;16 yrs",90),GREEN),("Model confidence",("High",85),GREEN),("Markers scored",("6 of 7",86),AMBER)],
 btn="EDIT READINGS")

rl_blood=dict(name="AFT BESPOKE PANEL 2",sub="SUSSEX PATHOLOGY &#183; PANEL DRAWN 08 OCT 2026 &#183; 7 MARKERS SCORED, PLUS CORTISOL",
 rows=[("HbA1c (mmol/mol)","32","&lt;42 normal","ok","NORMAL"),
       ("HbA1c %HbA1c (%)","5.08","&lt;6.0 normal","ok","NORMAL"),
       ("Homocysteine","22.46 &#181;mol/L","3.7&#8211;13.9","bad","FLAGGED"),
       ("Albumin","45 g/L","32&#8211;48","ok","WITHIN"),
       ("SHBG","48.41 nmol/L","17.33&#8211;71.5","ok","WITHIN"),
       ("Testosterone","43.58 nmol/L","6.51&#8211;23.74","bad","FLAGGED"),
       ("Free Testosterone","976.35 pmol/L","170&#8211;660","bad","FLAGGED"),
       ("hs-CRP","not tested","&lt;1.0","absent","NO RESULT"),
       ("Cortisol &#8212; not scored","261.69 nmol/L","145.4&#8211;619.4","ok","WITHIN")],
 note="Results as reported by Sussex Pathology on 08 Oct 2026. Seven markers feed the biometric age model. Cortisol is reported but not scored. hs-CRP is a model input this panel does not currently test for, so it scores neutral. Automated report, not reviewed by a physician; results should be discussed with a qualified practitioner.",
 btn="EDIT READINGS")

rl = page(dict(title="Client Report — Biometric Age Assessment Dashboard | AGING?F***THAT!",
 desc="An AFT biometric age assessment dashboard: body composition, movement and posture, heart health, blood markers and biological age in one view.",
 slug="example-report.html", sub="BIOMETRIC AGE ASSESSMENT DASHBOARD", robots="index,follow",
 banner=None,
 meta=dict(name="Lee C. Stonehouse",date="08 OCT 2026",program="Elite",status="Client",dot=""),
 bc=rl_bc,mp=rl_mp,hh=rl_hh,ba=rl_ba,blood=rl_blood,steps=STEPS,docs=docs_common))

open("dashboard.html","w",encoding="utf-8").write(ex)
open("example-report.html","w",encoding="utf-8").write(rl)
print("dashboard.html      %6d bytes" % len(ex.encode()))
print("example-report.html %6d bytes" % len(rl.encode()))
