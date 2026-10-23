import io, json, os, re, hashlib, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ART = 'https://cdn.marblism.com/smTOTZEjGAx.webp'
IM1 = 'https://cdn.marblism.com/GYYtfQP6Dau.webp'
IM2 = 'https://cdn.marblism.com/QN0Z25KkuQp.webp'
IM3 = 'https://cdn.marblism.com/8klV5n3Ewv_.webp'
FONT_URL = 'https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf'
FONT = '/tmp/Montserrat.ttf'
SLUG = 'twenty-minute-dose-nature-cortisol'
TITLE = 'The Twenty-Minute Dose: Why Nature Works Like a Prescription, and Why Sitting Still Beats Walking Past It'
DESC = 'The 21-30 minute cortisol window, the sitting-versus-walking finding and the 120-minute weekly floor: what the nature research shows for healthspan after 40. A measured view from a longevity clinic in Hove.'
CANON = 'https://agingfthat.com/blog/' + SLUG + '.html'

FAQ = [
 ('How long should a nature break be to reduce stress?',
  'In Hunter, Gillespie and Chen\u2019s 2019 study of 36 urban adults, the most efficient modelled cortisol window was 21 to 30 minutes, with no significant effect under 20 minutes and continued but slower benefits beyond 30. It is a modelled estimate from a small sample, not a guaranteed personal response or a clinical prescription.'),
 ('Is sitting in nature better than walking?',
  'Not for every measure. In that study, cortisol response was the same whether participants sat or walked. The alpha-amylase result differed: an adjusted decline appeared among those sitting or sitting with some walking, but not among those who walked throughout. Participants chose their activity, so this was not a randomised posture test.'),
 ('How much time in nature should I aim for each week?',
  'White and colleagues analysed survey data from 19,806 adults in England and found that 120 minutes or more in nature per week was associated with higher odds of good self-reported health and wellbeing, with the relationship levelling off at higher totals. It was observational, so it cannot prove cause. Treat 120 minutes as a practical target.'),
 ('Can a short walk in nature stop rumination?',
  'Bratman and colleagues randomly assigned 38 healthy adults to a 90-minute nature or urban walk in 2015 and found less self-reported rumination and reduced subgenual prefrontal cortex activity after the nature walk. It measured short-term changes in a small sample. It does not establish whether a shorter walk has the same effect.'),
 ('Do I need a forest for a nature break?',
  'The research does not establish that a forest is essential. Hunter and colleagues let participants choose any outdoor place that gave them a sense of contact with nature, and most chose urban green space near where they lived. A nearby park, a green route or a riverside path can all count as the input.'),
]

SRC = [
 'Hunter MR, Gillespie BW, Chen SYP. Urban nature experiences reduce stress in the context of daily life based on salivary biomarkers. <em>Frontiers in Psychology</em>. 2019;10:722.',
 'Bratman GN, Hamilton JP, Hahn KS, Daily GC, Gross JJ. Nature experience reduces rumination and subgenual prefrontal cortex activation. <em>PNAS</em>. 2015;112(28):8567-8572.',
 'White MP, Alcock I, Grellier J, et al. Spending at least 120 minutes a week in nature is associated with good health and wellbeing. <em>Scientific Reports</em>. 2019;9:7730.',
]

P = []
def p(t): P.append('<p>' + t + '</p>')
def h2(t): P.append('<h2>' + t + '</h2>')
def h3(t): P.append('<h3>' + t + '</h3>')
def img(src, alt, cap): P.append('<img class="hero" src="' + src + '" alt="' + alt + '">\n<p class="caption">' + cap + '</p>')

p('A walk past the park is not the same as a break in it. That distinction sounds small, and it is the sort of detail that gets lost when advice collapses into a single instruction to get outside more.')
p('The research behind that instruction is more specific than most people realise, and also more modest. It looks at how long a break needs to last, what is being measured, and in one finding, whether the person sat down or kept walking. Read carefully, it is not a wellness slogan. It is a dose question.')
p('Lee C. Stonehouse treats time outdoors as one of the cheapest inputs in his 10-Tenet operating system, and the one most easily skipped, because nothing hurts when it is missed. That is exactly why the numbers matter. A behaviour that produces no pain when neglected needs a schedule, not good intentions.')

h2('THE DAILY DOSE')
h3('Twenty to thirty minutes is the cortisol window')
p('In 2019, Hunter, Gillespie and Chen published a study in <em>Frontiers in Psychology</em> that followed 36 urban adults across eight weeks. Participants chose when, where and for how long to take a nature break, defined as any outdoor place that gave them a sense of contact with nature. Saliva was sampled immediately before and after selected breaks, and the samples were used to measure cortisol, a stress-related hormone, and alpha-amylase, a marker linked to sympathetic nervous system activity.')
p('The design dealt with an obvious problem. Cortisol falls through the day anyway, so a lower reading after a break proves nothing on its own. Using the pre-break samples to establish the normal daytime trajectory, the researchers found that in this group cortisol declined about 11.7% per hour as an ordinary diurnal effect. A nature break was associated with a further decline of 21.3% per hour on top of that.')
p('That is a modelled rate, not a promise that a single break drops anyone\u2019s cortisol by 21.3%. It describes the slope of the relationship across 110 breaks in 36 people.')
p('The more useful part came from a step model that split the breaks by duration. The most efficient window for the additional cortisol response was <strong>21 to 30 minutes</strong>, at an estimated 18.5% per hour beyond the daytime decline. Breaks longer than 30 minutes continued to show benefit, but at a lower modelled rate of 11.4% per hour. Under 20 minutes, the model found no significant effect.')
img(IM1, 'Abstract 3D visualization of a nature exposure dose-response curve rising to a luminous optimum then flattening, illustrating the 21 to 30 minute cortisol window', 'The duration model in the 2019 study put the most efficient cortisol response at 21 to 30 minutes, with slower gains after that.')
p('Keep the limits in view. The sample was small and self-selected, 92% of participants were women, and the mean age was 45.8. Participants picked their own settings and schedules, which is what makes the result realistic for daily life and also what makes it weaker than a large randomised trial. This is evidence about a pattern in a group, not a personal prescription.')

h2('THE POSTURE FINDING')
h3('Sitting still matters for one marker, not both')
p('The same study measured salivary alpha-amylase. Its ordinary daytime pattern runs upward at roughly 3.5% per hour, the opposite of cortisol. After accounting for that rise, the model estimated a 28.1% per hour decline during nature breaks, but only among participants who spent the break sitting, or sitting with some walking.')
p('For participants who walked throughout, alpha-amylase changed by about 4% per hour, indistinguishable from ordinary daytime drift. The walking nature break did not move that marker.')
p('Cortisol behaved differently again. Its response was the same whether people sat or walked. The regression slope for the low exertion and high exertion groups was effectively identical.')
img(IM2, 'Abstract 3D render contrasting a still suspended glass sphere with a moving tangled cyan ribbon, illustrating the difference between sitting and walking during a nature break', 'In the same study, sitting was linked to the alpha-amylase finding, while the cortisol response did not depend on posture.')
p('So sit still is not a rule for the twenty-to-thirty-minute cortisol window. It is a careful reading of one result in one marker. The activity groups were not assigned at random either, which means the posture comparison cannot show that sitting caused the difference. People who chose to sit may have differed in other ways.')
p('There is a practical lesson underneath the caveat, and it is not about posture at all. A nature break does not have to become a training session. The deliberate version of the habit is to stop, sit, and let attention rest on what is actually there. Walking remains a legitimate way to get the time in. It simply should not be described as equivalent to sitting for every measure in this study.')

h2('THE BRAIN AND RUMINATION')
h3('A separate study, a separate question')
p('Stress hormones are only one way to describe what a nature break does. The other strand of evidence looks at repetitive negative thinking, the loop where the mind returns to the same worry without resolving it.')
p('In a 2015 <em>PNAS</em> experiment, Bratman and colleagues randomly assigned 38 healthy urban adults to a 90-minute walk in either a natural or an urban setting. Participants were young on average, around 26.6 years old, so the result should not be assumed to transfer unchanged to a reader over 40. After the nature walk, participants reported less rumination and showed reduced activity in the subgenual prefrontal cortex, a region associated with withdrawal-related rumination. The urban walkers did not show the same changes.')
p('That is a controlled comparison, which the cortisol study was not, but it is also small and it measured short-term outcomes after a single walk. It does not show that a nature walk prevents depression, and it does not settle the ideal daily dose. Its value is different: it identifies a mechanism that a stress hormone reading cannot capture.')
p('The two studies should sit side by side rather than blend into one sweeping claim. One explored stress biomarkers across self-timed short breaks in ordinary life. The other examined rumination and a brain measure after a longer, controlled walk.')

h2('THE WEEKLY FLOOR')
h3('Build the dose across the week')
p('A third study moves from the single break to the total. In 2019, White and colleagues analysed survey data from 19,806 adults in England. People who had spent at least 120 minutes in nature during the previous week were more likely to report good health and high wellbeing than those who reported none. The association appeared to level off beyond roughly 200 to 300 minutes, and it held whether the time was taken in one long visit or several shorter ones.')
img(IM3, 'Abstract 3D visualization of a calm cyan centre connected by copper time nodes and open orbital rings, representing a weekly 120 minute nature target', 'A survey of 19,806 adults in England linked 120 minutes or more of weekly nature contact with better self-reported health and wellbeing.')
p('This is self-reported and observational. People reported their own visits and their own health, so the study cannot show that the time outdoors caused the difference. Healthier or happier people may simply be more likely to spend time outside, and the authors called for prospective and intervention research before firm guidelines are drawn. Treat 120 minutes as a practical weekly floor to test, not an official prescription.')
p('For anyone <strong>within a 10 mile radius of Brighton &amp; Hove city centre</strong>, the arithmetic is forgiving. Twenty minutes on four days clears the total, with a longer stretch at the weekend. The Downs, the seafront and the city\u2019s parks all sit inside that radius, and none of them requires a special trip.')

h2('MAKE IT MEASURABLE')
h3('A nature break is an input, not a vibe')
p('A structured healthspan programme should record time outdoors the way it records training load, sleep and protein: as a behaviour with a number attached, not a feeling to be recalled later. The record is simple. Minutes per visit, days per week, and whether the time was mostly sitting, walking or a mix.')
p('The clinic\u2019s version of this is deliberately unglamorous. A short reset is logged separately from a longer walk, because they are different inputs and because the research treats them differently. Neither is counted as a substitute for strength training, sleep or recovery. The point is not to inflate one behaviour into a cure. It is to know whether the cheapest intervention in the framework is actually happening.')
p('It also has to be read alongside other measures rather than instead of them. <a href="https://agingfthat.com/blog/heart-rate-variability-after-40-vagal-tone.html">Heart rate variability and vagal tone</a> give context on physiological regulation, <a href="https://agingfthat.com/blog/how-to-read-biological-age-results.html">how to read biological age results</a> explains why no single marker should stand in for a full assessment, and the <a href="https://agingfthat.com/blog/balance-after-40-one-legged-stance.html">10-second balance test</a> covers a different part of physical capability altogether.')
p('Lee became a personal trainer at 21 in California after competing as a bodybuilder. He wrote <em>The Healthspan Extension Manual</em> and built the 10-Tenet operating system he now practices. His own biological age was assessed at 47 against a chronological age of 63. That result came from a measured programme, and it is not a promise of the same outcome for anyone else.')

h2('THREE STEPS TO START')
p('<strong>Schedule one 20 to 30 minute break.</strong> Put it in the diary rather than waiting for a gap. Choose a place that genuinely feels like contact with nature. Sit, walk or combine the two, knowing that the posture finding applies to alpha-amylase and not to the cortisol response.')
p('<strong>Log the week, not the outing.</strong> Note the minutes and the activity type for each visit and add them up. Work toward 120 minutes across the week, which is a target suggested by observational evidence rather than a guaranteed threshold.')
p('<strong>Repeat for a month before judging it.</strong> One unusually good or bad day tells you nothing. Four weeks of logged minutes tells you whether the habit exists, and that is the only question worth asking first.')

h2('FREQUENTLY ASKED QUESTIONS')
for q, a in FAQ:
    h3(q); p(a)

h2('THE NEXT STEP')
p('Healthspan is built from repeated inputs, not one dramatic gesture. The nature evidence gives a starting structure that is unusual for its honesty: a daily window of 20 to 30 minutes linked to one stress marker, a weekly total of 120 minutes associated with better self-reported health in a large survey, and a separate brain finding that does not pretend to be the same thing.')
p('None of it is a guarantee. All of it beats guessing.')
p('To make healthspan measurable, contact Lee directly on <a href="https://wa.me/447935903549">WhatsApp</a> by text, voice note or voice call.')

STYLE = '<style>body{margin:0;background:radial-gradient(circle at 50% 0,#0a3550 0,#031522 38%,#020b12 100%);color:#edfaff;font:17px/1.65 Arial,sans-serif}.wrap{max-width:840px;margin:auto;padding:24px 20px 70px}.eyebrow{font-size:13px;letter-spacing:.25em;color:#75ddff;font-weight:700;margin:26px 0 18px}img.hero{width:100%;border-radius:22px;border:1.5px solid #2bc7ff;box-shadow:0 0 24px #16bfff55;margin:8px 0 10px}p.caption{font-size:14px;color:#a9c8d8;margin:0 0 34px}h1{font-size:clamp(32px,5vw,52px);line-height:1.05;letter-spacing:-.02em;margin:0 0 26px}h2{font-size:clamp(24px,3vw,34px);line-height:1.1;margin:38px 0 14px;color:#8CE2F3}h3{font-size:19px;margin:26px 0 8px;color:#c9e5ef}p{margin:0 0 20px;color:#e7f5fb}a{color:#2bc7ff}.sources{padding-left:20px;font-size:14px;color:#c9e5ef}.sources li{margin-bottom:14px}.footer{margin-top:50px;padding-top:20px;border-top:1px solid #19bff5;font-size:13px;color:#a9c8d8}strong{color:#fff}</style>'

ld = {'@context':'https://schema.org','@graph':[
 {'@type':'Article','image':[ART,IM1,IM2,IM3],'author':{'name':'Lee C. Stonehouse','@type':'Person'},'headline':TITLE,
  'keywords':['healthspan','cortisol','nature','biological age','longevity clinic'],
  'publisher':{'url':'https://agingfthat.com','name':'AGING?F*** THAT!','@type':'Organization'},
  'description':DESC,'dateModified':'2026-10-23','datePublished':'2026-10-23',
  'articleSection':['Healthspan','Longevity'],'mainEntityOfPage':{'@id':CANON,'@type':'WebPage'}},
 {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQ]},
]}
LDS = json.dumps(ld, indent=1, ensure_ascii=False)
json.loads(LDS)

BODY = '\n'.join(P)
words = len(re.sub(r'<[^>]+>',' ',BODY).split())
assert words >= 1200, words

HEAD = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
 '<title>' + TITLE + ' | AGING?F***THAT!</title><meta name="description" content="' + DESC + '"><link rel="canonical" href="' + CANON + '">\n'
 '<link rel="icon" href="../favicon.ico" sizes="any">\n<link rel="icon" href="../favicon.svg" type="image/svg+xml">\n'
 '<link rel="apple-touch-icon" href="../apple-touch-icon.png">\n<link rel="icon" sizes="32x32" type="image/png" href="../android-chrome-192.png">\n'
 '<meta property="og:type" content="article"><meta property="og:title" content="' + TITLE + '"><meta property="og:description" content="' + DESC + '">'
 '<meta property="og:image" content="' + ART + '"><meta property="og:url" content="' + CANON + '"><meta name="twitter:card" content="summary_large_image">'
 '<meta name="twitter:title" content="' + TITLE + '"><meta name="twitter:description" content="' + DESC + '"><meta name="twitter:image" content="' + ART + '">\n'
 + STYLE + '\n<script type="application/ld+json">\n' + LDS + '\n</script>\n'
 '<!-- Metricool tracker -->\n<script>window.metricool=window.metricool||function(){(window.metricool.q=window.metricool.q||[]).push(arguments)};</script>\n'
 '<script async src="https://tracker.metricool.com/resources/be.js"></script>\n</head><body>\n'
 '<header style="padding:14px 0;text-align:center"><a href="../index.html"><img src="../aft-logo.png" alt="AGING?F***THAT!" style="width:min(760px,92%)"></a></header>\n'
 '<main class="wrap">\n<div class="eyebrow">23 OCTOBER 2026 \u00b7 LEE C. STONEHOUSE</div>\n'
 '<img class="hero" src="' + ART + '" alt="A luminous ring timer above a geometric forest form on a dark navy background, illustrating the twenty minute nature dose for healthspan">\n'
 '<p class="caption">A nature break has a duration, and the research suggests the duration changes the result.</p>\n\n<h1>' + TITLE + '</h1>\n\n')

TAIL = '\n<ol class="sources">' + ''.join('<li>' + s + '</li>' for s in SRC) + '</ol>\n'
TAIL += ('<div class="footer">AGING?F***THAT! operates a longevity clinic in Hove and works with clients within a 10 mile radius of Brighton &amp; Hove city centre. '
 'Articles are educational and are not medical advice. Contact is by WhatsApp only: <a href="https://wa.me/447935903549">wa.me/447935903549</a></div>\n</main></body></html>\n')

html = HEAD + BODY + TAIL
assert 'ageing' not in html.lower()
assert 'Marbella' not in html
assert 'within a 10 mile radius of Brighton &amp; Hove city centre' in html
assert 'wa.me/447935903549' in html
assert html.count('class="hero"') == 4
assert html.count('<link rel="icon"') + html.count('apple-touch-icon') >= 4
for bad in ['Wall Street','CEO','wealth than health','FCIPD','MBA','mailto:']:
    assert bad.lower() not in html.lower(), bad

os.makedirs('blog', exist_ok=True)
open('blog/' + SLUG + '.html', 'w').write(html)
print('article words', words, 'bytes', len(html.encode()))

# ---- blog listing card ----
list_html = open('blog.html').read()
if SLUG not in list_html:
    anchor = '<section class="grid">'
    i = list_html.find(anchor)
    assert i > 0
    i = list_html.find('>', i) + 1
    card = ('\n      <article class="card">\n        <a href="blog/' + SLUG + '.html"><img class="thumb" src="blog/images/' + SLUG + '.jpg" alt="' + TITLE + '" loading="lazy" decoding="async"/>\n'
            '          <h3>' + TITLE + '</h3>\n'
            '          <p class="muted">Twenty to thirty minutes was the most efficient cortisol window in a small 2019 study. The 120 minute week does the rest.</p>\n'
            '          <span class="date">23 October 2026</span>\n        </a>\n      </article>\n')
    list_html = list_html[:i] + card + list_html[i:]
    open('blog.html', 'w').write(list_html)
    print('listing card added')
else:
    print('listing card already present')

# ---- sitemap ----
sm = open('sitemap.xml').read()
if SLUG not in sm:
    i = sm.find('<url>')
    assert i > 0
    entry = '<url><loc>' + CANON + '</loc><lastmod>2026-10-23</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
    sm = sm[:i] + entry + sm[i:]
    open('sitemap.xml', 'w').write(sm)
    print('sitemap entry added')
else:
    print('sitemap entry already present')

# ---- images ----
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'AFT-render/1.0'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()

if not os.path.exists(FONT):
    open(FONT, 'wb').write(get(FONT_URL))

def fnt(sz, w=900):
    f = ImageFont.truetype(FONT, sz)
    try:
        f.set_variation_by_axes([w])
    except Exception:
        pass
    return f

def wrap(d, t, f, maxw):
    out, cur = [], ''
    for word in t.split():
        s = (cur + ' ' + word).strip()
        if d.textlength(s, font=f) <= maxw:
            cur = s
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out

def crop_band(art, W, H, focus=0.42):
    r = max(W / art.width, H / art.height)
    a = art.resize((int(art.width * r), int(art.height * r)), Image.LANCZOS)
    l = (a.width - W) // 2
    t = int((a.height - H) * focus)
    return a.crop((l, t, l + W, t + H))

art = Image.open(io.BytesIO(get(ART))).convert('RGB')
lg0 = Image.open('aft-logo.png').convert('RGBA')
LGO = lg0.crop(lg0.split()[-1].getbbox())

os.makedirs('blog/images', exist_ok=True)
thumb = ImageEnhance.Contrast(crop_band(art, 1200, 675, 0.45)).enhance(1.05)
thumb.save('blog/images/' + SLUG + '.jpg', 'JPEG', quality=90, subsampling=0, optimize=True)
print('thumb', len(open('blog/images/' + SLUG + '.jpg', 'rb').read()))

NAVY = (3, 21, 34); ICE = (169, 205, 234); CYAN = (43, 199, 255); WHITE = (237, 250, 255)
W, H = 1440, 1800
K = W / 1080.0
BAND = int(H * 0.472)
c = Image.new('RGB', (W, H), NAVY)
c.paste(ImageEnhance.Sharpness(ImageEnhance.Contrast(crop_band(art, W, BAND, 0.34)).enhance(1.05)).enhance(1.25), (0, 0))
d = ImageDraw.Draw(c, 'RGBA')
g = int(220 * K)
for y in range(BAND - g, BAND):
    a = int(255 * ((y - (BAND - g)) / g) ** 1.4)
    d.line([(0, y), (W, y)], fill=(3, 21, 34, a))
d.rectangle([0, BAND, W, H], fill=NAVY)
PAD = int(70 * K)
LW = int(300 * K); LH = int(LGO.height * (LW / LGO.width))
lg = LGO.resize((LW, LH), Image.LANCZOS)
ly = BAND + int(40 * K)
c.paste(lg, (PAD, ly), lg)
ry = ly + LH + int(34 * K)
d.line([(PAD, ry), (W - PAD, ry)], fill=CYAN, width=int(3 * K))
ey = ry + int(36 * K)
d.text((PAD, ey), 'STRESS CONTROL & HEALTHSPAN', font=fnt(int(26 * K), 700), fill=CYAN)
fp = fnt(int(27 * K), 800); pill_h = int(70 * K); pill_y = H - int(46 * K) - pill_h
f2 = fnt(int(29 * K), 600)
body_lines = wrap(d, 'Twenty to thirty minutes moves one stress marker. The 120 minute week moves the rest.', f2, W - 2 * PAD)
body_y = pill_y - int(22 * K) - len(body_lines) * int(38 * K)
f = fnt(int(54 * K), 900); lh = int(f.size * 1.16)
lines = wrap(d, TITLE, f, W - 2 * PAD)
hy = ey + int(60 * K)
while len(lines) * lh > body_y - int(22 * K) - hy and f.size > int(34 * K):
    f = fnt(f.size - 2, 900); lh = int(f.size * 1.16)
    lines = wrap(d, TITLE, f, W - 2 * PAD)
y = hy
for ln in lines:
    d.text((PAD, y), ln, font=f, fill=WHITE); y += lh
y = body_y
for ln in body_lines:
    d.text((PAD, y), ln, font=f2, fill=ICE); y += int(38 * K)
tw = d.textlength('SEE CAPTION FOR MORE', font=fp)
d.rounded_rectangle([PAD, pill_y, PAD + tw + int(56 * K), pill_y + pill_h], radius=pill_h // 2, fill=CYAN)
d.text((PAD + int(28 * K), pill_y + (pill_h - int(fp.size * 1.2)) // 2 + 2), 'SEE CAPTION FOR MORE', font=fp, fill=NAVY)
print('post fits', y < pill_y - int(20 * K))
os.makedirs('social', exist_ok=True)
c.convert('RGB').save('social/' + SLUG + '.jpg', 'JPEG', quality=95, subsampling=0, optimize=True)
c.resize((1080, 1350), Image.LANCZOS).convert('RGB').save('/tmp/post1080.jpg', 'JPEG', quality=95, subsampling=0, optimize=True)

SW, SH = 1080, 1920
ART_H = int(SH * 0.40)
s = Image.new('RGB', (SW, SH), NAVY)
st = ImageEnhance.Brightness(ImageEnhance.Contrast(crop_band(art, SW, ART_H, 0.34)).enhance(1.06)).enhance(0.94)
s.paste(st, (0, 0))
sd = ImageDraw.Draw(s, 'RGBA')
gg = 340
for yy in range(ART_H - gg, ART_H):
    a = int(255 * ((yy - (ART_H - gg)) / gg) ** 1.35)
    sd.line([(0, yy), (SW, yy)], fill=(3, 21, 34, a))
sd.rectangle([0, ART_H, SW, SH], fill=NAVY)
SPAD = 72
SLW = 286; SLH = int(LGO.height * (SLW / LGO.width))
s.paste(LGO.resize((SLW, SLH), Image.LANCZOS), (SPAD, ART_H + 40), LGO.resize((SLW, SLH), Image.LANCZOS))
sry = ART_H + 40 + SLH + 28
sd.line([(SPAD, sry), (SW - SPAD, sry)], fill=CYAN, width=3)
sd.text((SPAD, sry + 32), 'STRESS CONTROL & HEALTHSPAN', font=fnt(24, 700), fill=CYAN)
sf = fnt(42, 900); sstep = int(42 * 1.24)
slines = wrap(sd, TITLE, sf, SW - 2 * SPAD)
sy = sry + 32 + 54
for ln in slines:
    sd.text((SPAD, sy), ln, font=sf, fill=WHITE); sy += sstep
sy += 16
CAP = ('Twenty-one to thirty minutes was the most efficient cortisol window in a 2019 study of 36 adults. '
       'Cortisol fell 21.3% an hour beyond the normal daytime decline. Small study, useful dose. Then build 120 minutes across the week.')
sf2 = fnt(28, 500)
for ln in wrap(sd, CAP, sf2, SW - 2 * SPAD):
    sd.text((SPAD, sy), ln, font=sf2, fill=ICE); sy += int(28 * 1.5)
sy += 20
sd.text((SPAD, sy), 'Read the full blog at www.agingfthat.com!', font=fnt(27, 800), fill=CYAN); sy += 40
sd.text((SPAD, sy), 'New articles daily at agingfthat.com/blog', font=fnt(25, 600), fill=ICE); sy += 36
sd.text((SPAD, sy), '#healthspan #longevity', font=fnt(26, 700), fill=ICE)
sfp = fnt(29, 800)
stw = sd.textlength('BLOG \u00b7 LINK IN BIO', font=sfp)
sph = 76; spy = SH - 150
sd.rounded_rectangle([SPAD, spy, SPAD + stw + 58, spy + sph], radius=sph // 2, fill=CYAN)
sd.text((SPAD + 29, spy + (sph - int(sfp.size * 1.2)) // 2 + 2), 'BLOG \u00b7 LINK IN BIO', font=sfp, fill=NAVY)
print('story fits', sy < spy - 30)
s.save('social/' + SLUG + '-story.jpg', 'JPEG', quality=92, subsampling=0, optimize=True)
print('social written', os.path.getsize('social/' + SLUG + '.jpg'), os.path.getsize('social/' + SLUG + '-story.jpg'))
print('DONE')
