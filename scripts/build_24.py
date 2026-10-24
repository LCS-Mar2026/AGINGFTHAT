import io, json, os, re, hashlib, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ART = 'https://cdn.marblism.com/Gyx2H1Z8Zgt.webp'
IM1 = 'https://cdn.marblism.com/3PPiw6xJCL3.webp'
IM2 = 'https://cdn.marblism.com/Pd0cvSAOQeu.webp'
IM3 = 'https://cdn.marblism.com/XAq0dV8xTWe.webp'
FONT_URL = 'https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf'
FONT = '/tmp/Montserrat.ttf'
SLUG = 'muscle-full-effect-protein-one-big-meal'
TITLE = 'The Muscle-Full Effect, Revisited: What the 100-Gram Protein Study Actually Found'
DESC = 'How much protein a single meal can really use, what the 100-gram study found, and what it means for muscle after 40. A measured view from a longevity clinic in Brighton & Hove.'
CANON = 'https://agingfthat.com/blog/' + SLUG + '.html'

FAQ = [
 ('Is protein above 30 g in one meal wasted?',
  'No. Trommelen and colleagues\u2019 2023 randomised trial found the anabolic response to 100 g of protein after exercise exceeded 12 hours with no upper limit in magnitude or duration, and the amino acids were not simply oxidised. The open question is how much of a very large dose reaches muscle rather than other tissues.'),
 ('What does 0.4 g/kg per meal mean?',
  'It is a research-derived reference for a substantial protein serving, particularly relevant to older adults, not a fixed requirement for everyone. Multiply body weight in kilograms by 0.4 for a rough per-meal estimate. For example, at 70 kg that is about 28 g. Individual needs depend on health, activity and training.'),
 ('Does leucine alone build muscle?',
  'No. Leucine helps signal muscle protein synthesis, but it is only one essential amino acid. Building new muscle protein requires all essential amino acids, along with a training stimulus and recovery. A complete protein food or a well-planned combination of foods is a stronger foundation than relying on leucine alone.'),
 ('Should all protein be eaten evenly through the day?',
  'Not necessarily. Even distribution is a reasonable way to make breakfast and lunch more substantial, but longer-term research in older adults has not shown an independent benefit for muscle mass or strength. Prioritise adequate total protein, suitable per-meal servings and resistance training; use distribution as a practical tool, not a rule.'),
 ('Is protein timing more important than strength training?',
  'Protein supports repair and adaptation, but it does not replace resistance exercise. Training provides the stimulus; protein supplies the building blocks. For healthspan after 40 both belong in a consistent routine, alongside sleep and recovery. Anyone with a medical condition affecting diet should seek personalised guidance first.'),
]

SRC = [
 'Atherton PJ et al. Muscle full effect after oral protein: time-dependent concordance and discordance between human muscle protein synthesis and mTORC1 signaling. <em>J Nutr</em>. 2010;140(10):2110S-2116S.',
 'Moore DR et al. Protein ingestion to stimulate myofibrillar protein synthesis requires greater relative protein intakes in healthy older versus younger men. <em>J Gerontol A</em>. 2015;70(1):57-62.',
 'Trommelen J et al. The anabolic response to protein ingestion during recovery from exercise has no upper limit in magnitude and duration in vivo in humans. <em>Cell Reports Medicine</em>. 2023;4(12):101324.',
 'Mamerow MM et al. Dietary protein distribution positively influences 24-h muscle protein synthesis in healthy adults. <em>J Nutr</em>. 2014;144(6):876-880.',
 'Kim IY et al. Protein intake distribution pattern does not affect anabolic response, lean body mass, muscle strength or function over 8 weeks in older adults. <em>J Nutr</em>. 2017.',
 'Schoenfeld BJ, Aragon AA. How much protein can the body use in a single meal for muscle-building? <em>J Int Soc Sports Nutr</em>. 2018;15:10.',
]

P = []
def p(t): P.append('<p>' + t + '</p>')
def h2(t): P.append('<h2>' + t + '</h2>')
def h3(t): P.append('<h3>' + t + '</h3>')
def img(src, alt, cap): P.append('<img class="hero" src="' + src + '" alt="' + alt + '">\n<p class="caption">' + cap + '</p>')

p('A generous dinner can hold plenty of protein, and muscle does not turn every extra gram into new tissue on demand. That idea, the so-called muscle-full effect, has shaped protein advice for over a decade.')
p('It is also an idea the newest science has substantially revised. Read carefully, the research does not say a big meal is wasted. It says something more specific about how muscle building behaves in the hours after eating, and about what that means for anyone over 40.')
p('Lee C. Stonehouse treats protein as one of the measured inputs in his 10-Tenet operating system. The amount matters less than knowing what the evidence does and does not say, because a nutrition habit built on a misreading of one study tends to be abandoned just as quickly as it was adopted.')

h2('THE MEAL-SIZE QUESTION')
h3('Where the old idea came from')
p('In a small 2010 study, Atherton and colleagues gave eight young men 48 g of whey protein and traced what happened in their leg muscle. Muscle protein synthesis, the process by which muscle builds new protein, rose sharply and then settled back towards baseline, even though amino acids from the drink were still elevated in the blood. The researchers named this time-limited response the muscle-full effect.')
p('The image it produced was simple: muscle fills up like a glass, and anything poured in after the rim is reached runs to waste. That image travelled further than the study itself, which was small, involved young men, and measured only a few hours. It was never intended to establish an exact meal limit for people over 40.')
img(IM1, 'A luminous muscle-building pulse rising and settling while the amino-acid stream continues past it, illustrating that the anabolic response to a large dose extends beyond the early pulse', 'The early muscle-building pulse eases within hours. The 2023 evidence shows the response to a large dose continues well beyond it.')
p('The 2023 follow-up is where the picture changed. Trommelen and colleagues published a randomised trial in <em>Cell Reports Medicine</em> comparing 25 g with 100 g of protein after resistance exercise. The 100 g dose produced a greater and more prolonged anabolic response, exceeding 12 hours, with no detectable upper limit in magnitude or duration. The amino acids were not simply burned off. The paper\u2019s title says it plainly: the anabolic response to protein ingestion has no upper limit in vivo in humans.')
p('Two further trials point the same way. Kim and colleagues found in healthy young adults that the anabolic response to a meal was not limited by the maximal stimulation of protein synthesis, and a 2021 randomised crossover trial reached the same conclusion in healthy older adults. A large meal is not automatically capped at some fixed number of grams.')
p('What remains genuinely uncertain is how much of a very large single dose ends up in muscle rather than other tissues, and whether distributing protein across the day produces measurably better long-term outcomes. The honest position for healthspan after 40 is that spreading protein is a sensible, evidence-informed habit, but it is a strategy for convenience and consistency rather than a rescue mission for protein that would otherwise be wasted.')

h2('THE OVER-40 DOSE')
h3('Anabolic resistance changes the response')
p('With aging, muscle can become less responsive to smaller meals and other anabolic signals. This is called anabolic resistance. It is not an on-off switch and it does not mean muscle stops responding. It means the stimulus may need to be more deliberate.')
p('In a dose-response analysis, Moore and colleagues estimated that the protein intake associated with a maximal resting muscle protein synthesis response was around 0.24 g per kilogram of body weight per meal in younger men and 0.40 g/kg per meal in older men. The estimate for older adults was variable, so 0.40 g/kg is best treated as a useful guide with a wide margin, not a universal biological cutoff.')
p('As a rough illustration, 0.40 g/kg works out to about 28 g for a person weighing 70 kg, or 32 g for someone at 80 kg. A practical meal might therefore provide roughly 25 to 40 g of quality protein, adjusted to body size, training, appetite and health needs.')
img(IM2, 'A single radiant signal particle approaching a gate in a wall of interwoven light strands, illustrating leucine as the start signal for muscle protein synthesis', 'Leucine helps signal the start of muscle protein synthesis. The other essential amino acids supply the building material.')
p('Resistance exercise shifts the picture further. Yang and colleagues studied older men after leg exercise and found that a 40 g whey dose produced a larger muscle protein synthesis response than 20 g in the post-exercise condition. That acute result supports considering a more substantial protein serving around training. It is not a promise of muscle gain from any single meal.')
p('For an over-40 reader, the point is simple: a token amount of protein at breakfast or lunch may not offer the same stimulus as a substantial serving. It can be worth checking what is actually on the plate before adding another supplement.')

h2('LEUCINE: THE SIGNAL NEEDS MATERIAL')
h3('A trigger is not the whole meal')
p('Leucine, one of the essential amino acids, helps signal that muscle protein building can begin. Think of it as a start signal, not the complete set of materials needed to build the structure.')
p('Research on older adults suggests leucine availability can influence the response to a small essential-amino-acid dose. But claims of a precise, universal leucine threshold should be treated cautiously. The effect depends on the person, the whole meal, the protein source and whether exercise has taken place.')
p('A leucine supplement on its own is not a substitute for a complete protein source. Muscle needs all essential amino acids to make new proteins. Dairy, eggs, fish, meat, soy or a well-planned combination of plant foods can supply a broader set of building blocks. Some sources deliver more leucine per serving than others, so food quality and total protein both matter.')

h2('DISTRIBUTION: A HABIT, NOT A RESCUE')
h3('More than one opportunity, without pretending dinner is wasted')
p('If most daily protein is saved for dinner, breakfast and lunch may be relatively low in the amino acids needed to stimulate muscle protein synthesis. A more even pattern gives muscle several opportunities across the day rather than concentrating the largest serving in one sitting.')
p('In a small crossover study, Mamerow and colleagues compared similar daily protein totals eaten either more evenly across three meals or heavily weighted towards dinner. The even pattern was associated with higher 24-hour muscle protein synthesis. The sample was only eight healthy adults, so the finding is suggestive, not proof that meal distribution alone produces more muscle over the long term.')
img(IM3, 'A curved daily timeline with four evenly spaced glowing nodes, each emitting a pulse, illustrating protein distribution across the day as a practical habit', 'Spreading substantial protein servings through the day is a practical habit, not a proven advantage over a dinner-heavy pattern.')
p('The longer-term evidence in older adults is less clear. In an eight-week randomised trial, Kim and colleagues found no significant difference in muscle mass, strength or function between older participants assigned an even or dinner-heavy protein pattern. The trial was small, and both groups consumed a planned daily protein intake.')
p('A 2018 review by Schoenfeld and Aragon put the position carefully: a true upper limit to the anabolic response per meal has not been established, and while spreading protein is a defensible strategy, the evidence does not show that a large single meal squanders protein. Read together with the 2023 trial, the honest summary is that distribution is a reasonable habit with a plausible mechanism, not a proven advantage over a dinner-heavy pattern.')

h2('A SIMPLE HEALTHSPAN PROTEIN METHOD')
p('The research supports a measured routine, not a rigid eating schedule. Record a few days of meals and estimate how much protein each contains, because a dinner-heavy pattern is easy to miss. Build a protein source into breakfast and lunch as well as dinner, choosing foods that fit appetite and preference.')
p('Use body size as a guide: around 0.4 g/kg per meal is a research-derived reference from the Moore analysis, with a broad confidence band rather than a prescription. Pair the habit with progressive resistance training, which gives muscle a reason to adapt. The guidance on <a href="https://agingfthat.com/blog/eccentric-lowering-strength-training-over-50.html">strength training over 50</a> is a practical place to start.')
p('Total daily intake still matters, as do energy intake, sleep, illness, digestion and the ability to follow the plan consistently. People with kidney disease or other relevant medical conditions should discuss protein targets with a healthcare professional before making substantial changes.')
p('A <a href="https://agingfthat.com/blog/how-to-read-biological-age-results.html">biological age test</a> can contribute broader context to a health plan, but no single biomarker or food choice explains muscle health on its own. The <a href="https://agingfthat.com/blog/healthspan-after-40.html">healthspan framework</a> treats muscle as part of a wider picture of physical capability.')
p('Lee became a personal trainer at 21 in California after competing as a bodybuilder. He wrote <em>The Healthspan Extension Manual</em> and built the 10-Tenet operating system he now practises. For readers <strong>within a 10 mile radius of Brighton &amp; Hove city centre</strong>, a conversation with Lee can explore how protein and strength training fit into a measured plan. Contact is by <a href="https://wa.me/447935903549">WhatsApp</a>, by text, voice note or voice call.')

h2('THREE STEPS TO START')
p('<strong>Check the whole day, not the evening.</strong> Record meals for a few days and estimate the protein in each. A pattern that looks adequate on paper often delivers most of its total in one sitting.')
p('<strong>Give breakfast and lunch a real serving.</strong> Aim for roughly 0.4 g per kilogram of body weight per meal as a research-derived guide, adjusted for body size and appetite. Whole-food sources that supply all essential amino acids beat a leucine tablet.')
p('<strong>Train, then feed the training.</strong> A more substantial protein serving around resistance exercise has acute evidence behind it in older men. Repeat for four weeks before judging whether the routine works.')

h2('FREQUENTLY ASKED QUESTIONS')
for q, a in FAQ:
    h3(q); p(a)

h2('THE NEXT STEP')
p('The muscle-full effect is not a reason to fear a large meal, and the newest research makes that case more strongly than ever. A 100 g dose after exercise drove muscle building for more than twelve hours without hitting a ceiling in one randomised trial. Build substantial protein into more than one meal if it suits the day. Train muscle consistently. Track the routine and adjust it deliberately.')
p('None of it is a guarantee. All of it beats guessing.')
p('To make healthspan measurable, contact Lee directly on <a href="https://wa.me/447935903549">WhatsApp</a> by text, voice note or voice call.')

STYLE = '<style>body{margin:0;background:radial-gradient(circle at 50% 0,#0a3550 0,#031522 38%,#020b12 100%);color:#edfaff;font:17px/1.65 Arial,sans-serif}.wrap{max-width:840px;margin:auto;padding:24px 20px 70px}.eyebrow{font-size:13px;letter-spacing:.25em;color:#75ddff;font-weight:700;margin:26px 0 18px}img.hero{width:100%;border-radius:22px;border:1.5px solid #2bc7ff;box-shadow:0 0 24px #16bfff55;margin:8px 0 10px}p.caption{font-size:14px;color:#a9c8d8;margin:0 0 34px}h1{font-size:clamp(32px,5vw,52px);line-height:1.05;letter-spacing:-.02em;margin:0 0 26px}h2{font-size:clamp(24px,3vw,34px);line-height:1.1;margin:38px 0 14px;color:#8CE2F3}h3{font-size:19px;margin:26px 0 8px;color:#c9e5ef}p{margin:0 0 20px;color:#e7f5fb}a{color:#2bc7ff}.sources{padding-left:20px;font-size:14px;color:#c9e5ef}.sources li{margin-bottom:14px}.footer{margin-top:50px;padding-top:20px;border-top:1px solid #19bff5;font-size:13px;color:#a9c8d8}strong{color:#fff}</style>'

ld = {'@context':'https://schema.org','@graph':[
 {'@type':'Article','image':[ART,IM1,IM2,IM3],'author':{'name':'Lee C. Stonehouse','@type':'Person'},'headline':TITLE,
  'keywords':['healthspan','protein per meal','muscle protein synthesis','leucine','anabolic resistance','biological age'],
  'publisher':{'url':'https://agingfthat.com','name':'AGING?F*** THAT!','@type':'Organization'},
  'description':DESC,'dateModified':'2026-10-24','datePublished':'2026-10-24',
  'articleSection':['Nutrition','Healthspan'],'mainEntityOfPage':{'@id':CANON,'@type':'WebPage'}},
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
 '<main class="wrap">\n<div class="eyebrow">24 OCTOBER 2026 \u00b7 LEE C. STONEHOUSE</div>\n'
 '<img class="hero" src="' + ART + '" alt="Amber amino-acid particles flowing into glowing violet muscle-fibre strands on a deep indigo background, illustrating the muscle-full effect and protein per meal">\n'
 '<p class="caption">Muscle protein synthesis responds to a meal in pulses. The newest evidence shows a large dose keeps working well beyond the early pulse.</p>\n\n<h1>' + TITLE + '</h1>\n\n')

TAIL = '\n<ol class="sources">' + ''.join('<li>' + s + '</li>' for s in SRC) + '</ol>\n'
TAIL += ('<div class="footer">AGING?F***THAT! operates a longevity clinic in Hove and works with clients within a 10 mile radius of Brighton &amp; Hove city centre. '
 'Articles are educational and are not medical advice. Contact is by WhatsApp only: <a href="https://wa.me/447935903549">wa.me/447935903549</a></div>\n</main></body></html>\n')

html = HEAD + BODY + TAIL
assert 'ageing' not in html.lower()
assert 'Marbella' not in html
assert 'within a 10 mile radius of Brighton &amp; Hove city centre' in html
assert html.count('wa.me/447935903549') >= 3
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
            '          <p class="muted">A 100 g dose drove muscle building for over 12 hours with no ceiling. Spreading protein is still a good habit, just not a rescue mission.</p>\n'
            '          <span class="date">24 October 2026</span>\n        </a>\n      </article>\n')
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
    entry = '<url><loc>' + CANON + '</loc><lastmod>2026-10-24</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
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

# 24 October colour scheme: indigo band, violet accents, amber pill
NAVY = (8, 12, 34); ICE = (196, 190, 240); CYAN = (196, 150, 255); WHITE = (245, 243, 255)
PILL = (255, 176, 59)
W, H = 1440, 1800
K = W / 1080.0
BAND = int(H * 0.472)
c = Image.new('RGB', (W, H), NAVY)
c.paste(ImageEnhance.Sharpness(ImageEnhance.Contrast(crop_band(art, W, BAND, 0.34)).enhance(1.05)).enhance(1.25), (0, 0))
d = ImageDraw.Draw(c, 'RGBA')
g = int(220 * K)
for y in range(BAND - g, BAND):
    a = int(255 * ((y - (BAND - g)) / g) ** 1.4)
    d.line([(0, y), (W, y)], fill=(8, 12, 34, a))
d.rectangle([0, BAND, W, H], fill=NAVY)
PAD = int(70 * K)
LW = int(300 * K); LH = int(LGO.height * (LW / LGO.width))
lg = LGO.resize((LW, LH), Image.LANCZOS)
ly = BAND + int(40 * K)
c.paste(lg, (PAD, ly), lg)
ry = ly + LH + int(34 * K)
d.line([(PAD, ry), (W - PAD, ry)], fill=CYAN, width=int(3 * K))
ey = ry + int(36 * K)
d.text((PAD, ey), 'NUTRITION & HEALTHSPAN', font=fnt(int(26 * K), 700), fill=CYAN)
fp = fnt(int(27 * K), 800); pill_h = int(70 * K); pill_y = H - int(46 * K) - pill_h
f2 = fnt(int(29 * K), 600)
body_lines = wrap(d, 'A 100 g dose drove muscle building for over 12 hours. Distribution is a habit, not a rescue mission.', f2, W - 2 * PAD)
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
tw = d.textlength('BLOG \u00b7 LINK IN BIO', font=fp)
d.rounded_rectangle([PAD, pill_y, PAD + tw + int(56 * K), pill_y + pill_h], radius=pill_h // 2, fill=PILL)
d.text((PAD + int(28 * K), pill_y + (pill_h - int(fp.size * 1.2)) // 2 + 2), 'BLOG \u00b7 LINK IN BIO', font=fp, fill=NAVY)
print('post fits', y < pill_y - int(20 * K))
os.makedirs('social', exist_ok=True)
c.convert('RGB').save('social/' + SLUG + '.jpg', 'JPEG', quality=95, subsampling=0, optimize=True)
print('post', os.path.getsize('social/' + SLUG + '.jpg'))
c.resize((1080, 1350), Image.LANCZOS).convert('RGB').save('social/' + SLUG + '-1080.jpg', 'JPEG', quality=95, subsampling=0, optimize=True)
print('post1080', os.path.getsize('social/' + SLUG + '-1080.jpg'))

SW, SH = 1080, 1920
ART_H = int(SH * 0.40)
s = Image.new('RGB', (SW, SH), NAVY)
st = ImageEnhance.Brightness(ImageEnhance.Contrast(crop_band(art, SW, ART_H, 0.34)).enhance(1.06)).enhance(0.94)
s.paste(st, (0, 0))
sd = ImageDraw.Draw(s, 'RGBA')
gg = 340
for yy in range(ART_H - gg, ART_H):
    a = int(255 * ((yy - (ART_H - gg)) / gg) ** 1.35)
    sd.line([(0, yy), (SW, yy)], fill=(8, 12, 34, a))
sd.rectangle([0, ART_H, SW, SH], fill=NAVY)
SPAD = 72
SLW = 286; SLH = int(LGO.height * (SLW / LGO.width))
slg = LGO.resize((SLW, SLH), Image.LANCZOS)
s.paste(slg, (SPAD, ART_H + 40), slg)
sry = ART_H + 40 + SLH + 28
sd.line([(SPAD, sry), (SW - SPAD, sry)], fill=CYAN, width=3)
sd.text((SPAD, sry + 32), 'NUTRITION & HEALTHSPAN', font=fnt(24, 700), fill=CYAN)
sf = fnt(42, 900); sstep = int(42 * 1.24)
slines = wrap(sd, TITLE, sf, SW - 2 * SPAD)
sy = sry + 32 + 54
for ln in slines:
    sd.text((SPAD, sy), ln, font=sf, fill=WHITE); sy += sstep
sy += 16
CAP = ('A 100 g dose after exercise drove muscle building for more than 12 hours with no ceiling, in a 2023 trial. '
       'The old 30 gram cap is out of date. Spreading protein across the day is still a sensible habit, '
       'aim for roughly 0.4 g per kilogram per meal, and train to give muscle a reason to use it.')
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
sd.rounded_rectangle([SPAD, spy, SPAD + stw + 58, spy + sph], radius=sph // 2, fill=PILL)
sd.text((SPAD + 29, spy + (sph - int(sfp.size * 1.2)) // 2 + 2), 'BLOG \u00b7 LINK IN BIO', font=sfp, fill=NAVY)
print('story fits', sy < spy - 30)
s.save('social/' + SLUG + '-story.jpg', 'JPEG', quality=92, subsampling=0, optimize=True)
print('story', os.path.getsize('social/' + SLUG + '-story.jpg'))
print('DONE')
