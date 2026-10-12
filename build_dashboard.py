# -*- coding: utf-8 -*-
"""Emits two pages from ONE template: dashboard.html (fake example) and
example-report.html (Lee's real data). Same design, different data."""

CSS = "<style>\n" + open("dashboard.css", encoding="utf-8").read() + "\n</style>"

def bars(items):
    h=['<div class="bars">']
    for lbl,pct,cls,val in items:
        h.append('<div class="bar"><span>%s</span><span class="track"><i class="%s" style="width:%s%%"></i></span><b>%s</b></div>'%(lbl,cls,str(pct),val))
    h.append('</div>')
    return "".join(h)

def mk(cells, rows):
    h=['<table class="mk"><tr>'+''.join('<th>%s</th>'%c for c in cells)+'</tr>']
    for r in rows:
        h.append('<tr><td>%s</td><td class="n">%s</td><td>%s</td><td><span class="tag %s">%s</span></td></tr>'%(r[0],r[1],r[2],r[3],r[4]))
    h.append('</table>')
    return "".join(h)

def page(cfg):
    P=[]
    P.append('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>'%cfg['title'])
    P.append('<meta name="description" content="%s">'%cfg['desc'])
    P.append('<link rel="canonical" href="https://agingfthat.com/%s">'%cfg['slug'])
    P.append('<meta name="robots" content="%s">'%cfg.get('robots','index,follow'))
    P.append('<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">')
    P.append(CSS)
    P.append('</head><body>')
    P.append('<header class="hero"><h1 class="wm">AGING?<em>F***</em>THAT!</h1><p class="sub">%s</p><p class="strap">MEASURE &#124; ANALYSE &#124; OPTIMISE &#124; TRACK STATUS</p></header>'%cfg['sub'])
    mb=cfg['meta']
    P.append('<div class="metabar"><div>Name<b>%s</b></div><div>Assessment Date<b>%s</b></div><div>Source<b>%s</b></div><div>Status<b>%s<span class="dot %s"></span></b></div></div>'%(mb[0],mb[1],mb[2],mb[3],mb[4]))
    P.append('<div class="wrap">')
    if cfg.get('banner'): P.append('<p class="disc" style="margin:0 0 12px">%s</p>'%cfg['banner'])
    P.append('<div class="panels">')

    bc=cfg['bc']
    P.append('<section class="panel bc"><div class="ph"><span class="ic">&#128100;</span><div><h2>BODY COMPOSITION</h2><p>RENPHO MORPHO SCAN</p></div></div>')
    P.append('<div class="rows">')
    for lbl,val,tag in bc['rows']:
        P.append('<div class="row"><span>%s</span><b>%s%s</b></div>'%(lbl,val,tag))
    P.append('</div>')
    P.append(bars(bc['bars']))
    P.append('<div class="railtxt"><i>Segmental Analysis</i><i>Muscle Balance</i><i>Body Shape</i><i>Metabolic Age</i></div>')
    P.append('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%bc['btn'])

    mp=cfg['mp']
    P.append('<section class="panel mp"><div class="ph"><span class="ic">&#128694;</span><div><h2>MOVEMENT &amp; POSTURE</h2><p>CHIROPRACTIC ANALYSIS &#183; MOVEMENT &#183; ALIGNMENT &#183; POSTURE</p></div></div>')
    P.append('<div class="shots"><img src="anterior-posture-view.jpg" alt="Anterior posture view from the chiropractic assessment" loading="lazy"><img src="lateral-posture-view.jpg" alt="Lateral posture view from the chiropractic assessment" loading="lazy"></div>')
    P.append('<ul class="li">'+''.join('<li>%s</li>'%x for x in mp['bullets'])+'</ul>')
    P.append(bars(mp['bars']))
    P.append('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%mp['btn'])

    hh=cfg['hh']
    P.append('<section class="panel hh"><div class="ph"><span class="ic">&#10084;&#65039;</span><div><h2>HEART HEALTH</h2><p>BLOOD PRESSURE &amp; RESTING HEART RATE &#183; CURRENT MEASUREMENTS</p></div></div>')
    P.append('<div class="tiles">')
    for lbl,val,unit,tagcls,tagt in hh['tiles']:
        P.append('<div class="tile"><small>%s</small><b>%s</b><small>%s</small><u class="tag %s">%s</u></div>'%(lbl,val,unit,tagcls,tagt))
    P.append('</div>')
    P.append(bars(hh['bars']))
    P.append('<ul class="li">'+''.join('<li>%s</li>'%x for x in hh['bullets'])+'</ul>')
    P.append('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%hh['btn'])

    ba=cfg['ba']
    P.append('<section class="panel ba"><div class="ph"><span class="ic">&#128202;</span><div><h2>BIOMETRIC AGE</h2><p>%s</p></div></div>'%ba['sub'])
    P.append('<div class="donutwrap"><div class="donut" style="background:%s"><div class="inner"><small>Your Biometric Age</small><b>%s</b><em>years</em><u>Chronological Age %s</u></div></div></div>'%(ba['gauge'],ba['bio'],ba['chrono']))
    P.append('<div class="strip %s">%s</div>'%('good' if ba['younger'] else 'bad', ba['strip']))
    P.append('<p class="note">A healthier, stronger longer life is within your control.</p>')
    P.append(bars(ba['bars']))
    P.append('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%ba['btn'])
    P.append('</div>')

    if cfg.get('blood'):
        bx=cfg['blood']
        P.append('<section class="panel bx bloods" style="margin-top:12px"><div class="ph"><span class="ic">&#129514;</span><div><h2>BLOOD &amp; HORMONE MARKERS</h2><p>INDEPENDENT LAB VERIFIED &#183; BLOOD MARKERS OF LONGEVITY</p></div></div>')
        P.append(mk(['Marker','Result','Reference','Status'], bx['rows']))
        P.append('<p class="disc">%s</p>'%bx['note'])
        P.append('<div class="pb"><a class="btn" href="#">%s</a></div></section>'%bx['btn'])

    P.append('<div class="two"><section class="card"><h2>NEXT STEPS</h2><div class="steps">')
    for i,(t,s) in enumerate(cfg['steps'],1):
        P.append('<div class="step"><i>%d</i><div><b>%s</b><span>%s</span></div></div>'%(i,t,s))
    P.append('</div></section>')
    P.append('<section class="card"><h2>SOURCE DOCUMENTS</h2><div class="docs">')
    for name,detail in cfg['docs']:
        P.append('<div class="doc"><span>%s<small>%s</small></span><em>ON FILE</em></div>'%(name,detail))
    P.append('</div><p class="disc">Documents are listed for reference. Source files are held securely and are not downloadable from this page.</p></section></div>')
    P.append('</div>')
    P.append('<footer><div class="l">AGING?F***THAT! &#124; LONGER. STRONGER. HEALTHIER.</div><div class="r">WWW.AGINGFTHAT.COM</div></footer>')
    P.append('<script>(function(){document.querySelectorAll("a.btn[href=\\u0022#\\u0022]").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();});});})();</script>')
    P.append('</body></html>')
    return "\n".join(P)

# ---------------------------------------------------------------- FAKE EXAMPLE
FAKE = dict(
 title="Example Client Report — Biometric Age Assessment Dashboard | AGING?F***THAT!",
 desc="An example biometric age assessment dashboard: body composition, movement and posture, heart health, blood markers and estimated biological age in one view.",
 slug="dashboard.html", sub="BIOMETRIC AGE ASSESSMENT DASHBOARD",
 banner="<b>EXAMPLE ONLY.</b> Every figure on this page is illustrative sample data, not a real client record. It shows the format of an AFT assessment dashboard.",
 meta=("John Smith","12 OCT 2026","Level 1 Offer / Mailer","Applicant","w"),
 bc=dict(
  rows=[("Weight","90.0 kg",""),("Body Fat","21.0%",'<span class="tag warn">ABOVE TARGET</span>'),
        ("Muscle Mass","52.0 kg",'<span class="tag bad">LOW</span>'),("Visceral Fat","11",'<span class="tag bad">HIGH</span>'),
        ("BMI","27.8",'<span class="tag warn">OVERWEIGHT</span>')],
  bars=[("Muscle",58,"mid","52.0"),("Body Fat",74,"hot","21.0"),("Visceral",82,"hot","11"),("BMI",72,"mid","27.8")],
  btn="VIEW FULL MORPHO SCAN REPORT"),
 mp=dict(
  bullets=["Forward head posture","Anterior pelvic tilt","Reduced spinal alignment","Postural imbalance detected","Personalised recommendations"],
  bars=[("Head shift",70,"hot","1.40cm L"),("Shoulders",55,"mid","0.77cm R"),("Ribcage",38,"mid","0.44cm L"),("Hips",80,"hot","2.46cm L")],
  btn="VIEW FULL CHIROPRACTIC REPORT"),
 hh=dict(
  tiles=[("Blood Pressure","140/98","mmHg","bad","ELEVATED"),("Resting Heart Rate","76","bpm","warn","ABOVE OPTIMAL")],
  bars=[("Systolic",78,"hot","140"),("Diastolic",72,"hot","98"),("Resting HR",58,"mid","76")],
  bullets=["Blood pressure above optimal range","Resting heart rate elevated","May benefit from improved fitness","Supports cardiovascular health focus","Track and monitor progress"],
  btn="ADD / EDIT READINGS"),
 ba=dict(sub="YOUR ESTIMATED BIOLOGICAL AGE &#183; BASED ON LEVEL 1 METRICS",
  gauge="conic-gradient(from 200deg,#ff4b4b 0deg,#ff9b7a 120deg,#ffd479 240deg,#ff4b4b 360deg)",
  bio="77", chrono="62", younger=False, strip="15 YEARS OLDER THAN YOUR ACTUAL AGE",
  bars=[("Biometric Age",88,"hot","77"),("Chronological",62,"cy","62"),("Divergence",88,"hot","+15")],
  btn="VIEW YOUR FULL REPORT"),
 blood=dict(
  rows=[("HS-CRP","3.8 mg/L","&lt;1.0","bad","ELEVATED"),("HbA1c","41 mmol/mol","&lt;42","warn","WATCH"),
        ("Total Cholesterol","6.1 mmol/L","&lt;5.0","bad","ELEVATED"),("LDL Cholesterol","4.2 mmol/L","&lt;3.0","bad","ELEVATED"),
        ("HDL Cholesterol","1.0 mmol/L","&gt;1.0","warn","WATCH"),("Triglycerides","2.1 mmol/L","&lt;1.7","bad","ELEVATED"),
        ("ApoB","1.05 g/L","&lt;0.80","bad","ELEVATED"),("Fasting Glucose","5.8 mmol/L","&lt;5.6","warn","WATCH"),
        ("Testosterone","14.1 nmol/L","8.6&#8211;29.0","ok","WITHIN"),("Vitamin D","46 nmol/L","75&#8211;150","bad","LOW"),
        ("Fasting Insulin","62 pmol/L","14&#8211;42","warn","WATCH"),("Ferritin","210 &#181;g/L","30&#8211;300","ok","WITHIN")],
  note="Illustrative sample values only, shown to demonstrate the panel format and status logic.",
  btn="VIEW FULL BLOOD &amp; HORMONE PANEL"),
 steps=[("Review Your Results","Read what each panel measures and what it means."),
        ("Book a Consultation to Discuss","Go through the findings with Lee."),
        ("Personalised Plan &amp; Recommendations","Interventions across the 10 tenets."),
        ("Take Action &amp; Track Progress","Re-measure and confirm the change.")],
 docs=[("Renpho Morpho scan report","Body composition, muscle balance, metabolic age"),
       ("DEXA scan","Body composition and bone density, by assessment date"),
       ("Chiropractic assessment report","Posture, alignment and movement findings"),
       ("Blood and hormone panel","Independent lab panel, by draw date"),
       ("Heart rate and blood pressure log","Home and in-clinic readings"),
       ("Biometric age summary","Composite model output, by assessment date")],
)

# ----------------------------------------------------------------- REAL (LEE)
REAL = dict(
 title="Example Client Report — Biometric Age Assessment Dashboard | AGING?F***THAT!",
 desc="A real AFT biometric age assessment dashboard: body composition, movement and posture, heart health, blood markers and biological age in one view.",
 slug="example-report.html", sub="BIOMETRIC AGE ASSESSMENT DASHBOARD",
 banner=None,
 meta=("Lee C. Stonehouse","10 SEP 2026","Elite Age Reversal Programme","Client",""),
 bc=dict(
  rows=[("Weight","85.7 kg",""),("Body Fat","9.6%",'<span class="tag ok">LEAN</span>'),
        ("Lean Mass","74.60 kg",'<span class="tag ok">EXCEPTIONAL</span>'),("Visceral Fat","54.6 cm&#178;",'<span class="tag ok">LOW</span>'),
        ("BMI","22.4",'<span class="tag ok">HEALTHY</span>')],
  bars=[("Lean mass",92,"good","74.6 kg"),("Body fat",90,"good","9.6%"),("Visceral fat",95,"good","54.6"),("Muscle symm.",94,"good","5.58%")],
  btn="VIEW FULL MORPHO SCAN REPORT"),
 mp=dict(
  bullets=["Forward head posture","Anterior pelvic tilt","Reduced spinal alignment","Measured against the 25 Apr 2025 assessment","Personalised recommendations"],
  bars=[("Head shift",70,"mid","1.40cm L"),("Shoulders",55,"mid","0.77cm R"),("Ribcage",38,"good","0.44cm L"),("Hips",80,"mid","2.46cm L")],
  btn="VIEW FULL CHIROPRACTIC REPORT"),
 hh=dict(
  tiles=[("Blood Pressure","120","mmHg","ok","GOOD"),("Resting Heart Rate","47","bpm","ok","EXCEPTIONAL")],
  bars=[("Systolic",95,"good","120"),("Diastolic",90,"good","78"),("Resting HR",98,"good","47")],
  bullets=["Blood pressure within range","Resting heart rate exceptional","Supports cardiovascular health focus","Track and monitor progress"],
  btn="ADD / EDIT READINGS"),
 ba=dict(sub="YOUR BIOLOGICAL AGE &#183; BASED ON ASSESSMENT METRICS",
  gauge="conic-gradient(from 200deg,#2BC7FF 0deg,#7d5cf6 150deg,#e0409a 250deg,#2BC7FF 330deg)",
  bio="47", chrono="63", younger=True, strip="16 YEARS YOUNGER THAN YOUR ACTUAL AGE",
  bars=[("Biological age",75,"good","47"),("Chronological",63,"cy","63"),("Divergence",90,"good","&#8722;16")],
  btn="VIEW YOUR FULL REPORT"),
 blood=dict(
  rows=[("HbA1c","33 mmol/mol","&lt;42","ok","GOOD"),("HS-CRP","1.5 mg/L","&lt;1.0","warn","ESTIMATED"),
        ("Homocysteine","8.0 &#181;mol/L","&lt;10","ok","GOOD"),("Total Testosterone","19.4 nmol/L","8.6&#8211;29.0","ok","GOOD"),
        ("Free Testosterone","443 pmol/L","200&#8211;600","ok","EXCEPTIONAL"),("SHBG","66 nmol/L","18&#8211;144","ok","GOOD"),
        ("Total Cholesterol","6.2 mmol/L","&lt;5.0","bad","FLAGGED"),("Non-HDL Cholesterol","4.6 mmol/L","&lt;4.0","bad","FLAGGED"),
        ("LDL Cholesterol","4.0 mmol/L","&lt;3.0","bad","FLAGGED"),("HDL Cholesterol","1.6 mmol/L","&gt;1.0","ok","GOOD"),
        ("Triglycerides","1.6 mmol/L","&lt;1.7","warn","OKAY"),("Creatinine","113 &#181;mol/L","60&#8211;105","bad","FLAGGED"),
        ("eGFR (MDRD)","57 mL/min","&gt;90","bad","FLAGGED"),("ALT","37 IU/L","&lt;41","ok","GOOD"),
        ("Haematocrit","0.47 L/L","0.40&#8211;0.52","ok","GOOD"),("Platelets","261 x10&#8313;/L","150&#8211;400","ok","GOOD"),
        ("PSA","3.08 &#181;g/L","&lt;3.5","warn","OKAY"),("Vitamin D","145 nmol/L","75&#8211;150","ok","GOOD")],
  note="Panel dated 10 Sep 2026. Flagged cholesterol, renal and phosphate markers are the current programme focus. Trends across repeat panels are what the programme tracks.",
  btn="VIEW FULL BLOOD &amp; HORMONE PANEL"),
 steps=[("Review Your Results","Read what each panel measures and what it means."),
        ("Book a Consultation to Discuss","Go through the findings with Lee."),
        ("Personalised Plan &amp; Recommendations","Interventions across the 10 tenets."),
        ("Take Action &amp; Track Progress","Re-measure and confirm the change.")],
 docs=[("Renpho Morpho scan report","25 Apr 2025 &#183; latest body composition"),
       ("DEXA scan","14 Oct 2024, 21 Dec 2024 and 25 Apr 2025 &#183; body composition and bone density"),
       ("Chiropractic assessment report","Posture, alignment and movement findings"),
       ("Blood and hormone panel","10 Sep 2026 &#183; independent laboratory panel"),
       ("Heart rate and blood pressure log","120 mmHg systolic &#183; resting heart rate 47 bpm"),
       ("Biometric age summary","Composite model output, by assessment date")],
)

for cfg, name in ((FAKE,"dashboard.html"), (REAL,"example-report.html")):
    h = page(cfg)
    open(name,"w",encoding="utf-8").write(h)
    print("%-22s %6d bytes  panels=%d  tags=%d" % (name, len(h.encode()), h.count('class="panel '), h.count('class="tag ')))
