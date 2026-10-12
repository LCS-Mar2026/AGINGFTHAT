# -*- coding: utf-8 -*-
"""Emits the restricted AFT Elite Bioage Model Logic reference page into _site during deploy."""
import pathlib, os

HASH = "f29d7b120048b9344d52b30c9864a378ab9bee78ebc4e461fd07627d4bf844d8"
OUT = "_site/aft-elite-bioage-model-logic-121026.html"

MARKERS = [
 ("DEXA",[("Body fat","%",8),("Lean mass","kg",9),("Bone density T-score","T-score",8),("Visceral fat area","cm&#178;",9)]),
 ("Fitness",[("VO2max","mL/kg/min",10)]),
 ("Blood &amp; hormones",[("HbA1c","% (converts from mmol/mol)",10),("hsCRP","mg/L",9),
   ("Homocysteine","&#181;mol/L",9),("Total testosterone","nmol/L",7),("Free testosterone","nmol/L (converts from pmol/L)",7)]),
 ("Vital signs",[("Systolic blood pressure","mmHg",8),("Resting heart rate","bpm",6)]),
]
SUPPORT = ["Posture","Old Man Test","Diastolic pressure","Body weight","ALMI","Bone Z-score","Additional laboratory results"]
NOWEIGHT = ["Sleep","Photos and video"]
DOM = [("DEXA",34),("Fitness",10),("Blood &amp; hormones",42),("Vital signs",14)]

CSS = ("":root{--n:#031522;--p:#061d2c;--l:#123c52;--t:#edfaff;--m:#a9c8d8;--c:#2BC7FF;--v:#A855F7;--a:#FF9F1C;--r:#ff4b4b}"
"*{box-sizing:border-box}body{margin:0;background:var(--n);color:var(--t);font:15px/1.6 Arial,Helvetica,sans-serif}"
"body::before{content:'';position:fixed;inset:0;z-index:-2;background:url('https://cdn.marblism.com/-_Hu2UKtvyM.webp') center/cover;opacity:.16}"
"body::after{content:'';position:fixed;inset:0;z-index:-1;pointer-events:none;background:linear-gradient(180deg,rgba(3,21,34,.86),rgba(2,11,18,.92))}"
"a{color:var(--c)}.wrap{max-width:1000px;margin:0 auto;padding:24px 16px 60px}"
".hd{display:grid;grid-template-columns:1fr auto;gap:12px;align-items:center;border-bottom:1px solid var(--l);padding-bottom:16px;margin-bottom:22px}"
"h1{margin:0;font-size:clamp(20px,4.6vw,34px);font-weight:900;letter-spacing:-.02em}h1 em{font-style:normal;color:var(--c)}"
".sub{margin:6px 0 0;font-size:11px;font-weight:900;letter-spacing:.2em;color:var(--v)}"
"h2{font-size:13px;letter-spacing:.14em;font-weight:900;margin:26px 0 10px;color:#fff;text-transform:uppercase}"
".card{background:rgba(6,29,44,.72);border:1px solid var(--l);border-radius:12px;padding:14px}"
"table{width:100%;border-collapse:collapse;font-size:13.5px}"
"th{font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--m);text-align:left;padding:8px;border-bottom:1px solid var(--l)}"
"td{padding:9px 8px;border-bottom:1px solid #0d2b3c;vertical-align:middle}"
"td.d{color:var(--v);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;font-weight:900;white-space:nowrap}"
"td.u{color:var(--m);font-size:12px}td.w{white-space:nowrap;font-weight:900;text-align:right;width:120px}"
".bar{display:inline-block;width:56px;height:6px;border-radius:99px;background:#0d2b3c;margin-right:8px;overflow:hidden;vertical-align:middle}"
".bar i{display:block;height:100%;background:linear-gradient(90deg,#2BC7FF,#7d5cf6)}"
".dts{display:grid;grid-template-columns:repeat(2,1fr);gap:9px;margin-top:12px}"
".dt{border:1px solid var(--l);border-radius:10px;padding:11px;background:#052030;text-align:center}"
".dt b{display:block;font-size:22px;font-weight:900;color:var(--c)}.dt span{font-size:10.5px;color:var(--m)}"
".formula{background:#04202e;border:1px solid #14415a;border-radius:10px;padding:14px;font-size:14.5px;line-height:1.7}"
".formula code{display:block;font-size:13px;color:#a8e4ff;background:#02101a;border:1px solid #14415a;border-radius:7px;padding:11px;margin-top:8px;overflow-x:auto}"
".tiers{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:10px}"
".tier{border:1px solid var(--l);border-radius:9px;padding:10px 8px;text-align:center;background:#062028}"
".tier b{display:block;font-size:20px;font-weight:900}.tier span{font-size:9.5px;color:var(--m)}"
"ul.li{list-style:none;margin:0;padding:0}ul.li li{position:relative;padding-left:14px;margin-bottom:5px;font-size:13.5px;color:#d6ecf7}"
"ul.li li:before{content:'2022';position:absolute;left:2px;color:var(--c);font-weight:900}"
".warn{border-left:3px solid var(--a);background:#3a2a12;border-radius:8px;padding:12px;font-size:13.5px;margin-top:12px}"
".stop{border-left:3px solid var(--r);background:#3a1615;border-radius:8px;padding:12px;font-size:13.5px;margin-top:12px}"
"footer{border-top:1px solid var(--l);padding:18px 0 0;margin-top:28px;text-align:center;color:#7899a9;font-size:11px}"
"@media(min-width:700px){.dts{grid-template-columns:repeat(4,1fr)}}")

rows=[]
for dom,items in MARKERS:
    for i,(nm,un,w) in enumerate(items):
        rows.append('<tr><td class="d">%s</td><td><b>%s</b></td><td class="u">%s</td><td class="w"><span class="bar"><i style="width:%d%%"></i></span>%d%%</td></tr>'
                    % (dom if i==0 else "", nm, un, w*10, w))
body = ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\">"
"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><meta name=\"robots\" content=\"noindex,nofollow\">"
"<title>AFT Elite Bioage Model Logic 121026 | AGING?F***THAT!</title>"
"<style>"+CSS+"</style></head><body>"
"<div id=\"c\" style=\"display:none\"><div class=\"wrap\">"
"<div class=\"hd\"><div><h1>AGING?<em>F***</em>THAT!</h1><p class=\"sub\">AFT_ELITE_BIOAGE_MODEL_LOGIC_121026</p></div>"
"<a href=\"admin.html\">BACK TO ADMIN</a></div>"
"<h2>The model</h2><div class=\"card\"><p>Twelve weighted markers across four domains. The composite is a weighted average. 100 model weight points in total.</p></div>"
"<h2>Marker weights</h2><div class=\"card\"><table>"+"".join(rows)+"</table>"
"<div class=\"dts\">"+"".join('<div class=\"dt\"><b>%d%%</b><span>%s</span></div>'%(v,k) for k,v in DOM)+"</div></div>"
"<h2>Marker scoring</h2><div class=\"card\"><p>Each marker receives 100, 75, 40 or 10 points according to its defined model band. The composite is the weighted average.</p></div>"
"<h2>Age calculation</h2><div class=\"card\"><div class=\"formula\">Biometric age = actual age minus [ (composite score minus 50) divided by 50, times 20 ]. Adjustment capped at plus or minus 20 years. A composite of 75 gives an age 10 years younger.</div></div>"
"<h2>Missing inputs</h2><div class=\"card\"><p>Available weights are recalculated proportionally and the result is labelled provisional. All 12 valid markers are required for a complete assessment.</p>"
"<div class=\"warn\">A Level 1 assessment has no DEXA, no VO2max and no bloods, so it can never produce a complete score. It is always provisional.</div></div>"
"<h2>Supporting information, no additional weight</h2><div class=\"card\"><ul class=\"li\">"+"".join("<li>%s</li>"%x for x in SUPPORT)+"</ul></div>"
"<h2>No weighting in this version</h2><div class=\"card\"><ul class=\"li\">"+"".join("<li>%s</li>"%x for x in NOWEIGHT)+"</ul></div>"
"<h2>Implementation limits</h2><div class=\"card\"><ul class=\"li\"><li>Male reference bands in this version.</li>"
"<li>A proprietary AFT scoring model, not a validated clinical aging clock.</li></ul>"
"<div class=\"stop\">DEXA visceral area must never be replaced with a smart-scale rating.</div></div>"
"<footer>Internal document. Admin access only. Not medical advice.</footer></div></div>")

body += ("<div id=\"g\" style=\"max-width:420px;margin:14vh auto 0;padding:0 18px;text-align:center\">"
"<div style=\"font-weight:900;letter-spacing:.14em;font-size:12px;color:#e9fbff;padding:6px 0 16px\">INTERNAL DOCUMENT, RESTRICTED</div>"
"<div style=\"border:1px solid #168cc0;border-radius:18px;padding:26px 22px;background:rgba(6,29,44,.78)\">"
"<label for=\"pw\">Admin password</label>"
"<input id=\"pw\" type=\"password\"/>"
"<button id=\"btn\">OPEN</button>"
"<div id=\"err\"></div></div></div>")

body += ("<script>(function(){var H='"+HASH+"';var K='agnf_admin_v2';"
"var g=document.getElementById('g'),c=document.getElementById('c');"
"function d(s){return crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)).then(function(b){return [...new Uint8Array(b)].map(function(x){return x.toString(16).padStart(2,'0')}).join('')})}"
"function v(){try{return Number(localStorage.getItem(K)||0)>Date.now()}catch(e){return false}}"
"function w(){try{localStorage.setItem(K,String(Date.now()+90*24*60*60*1000))}catch(e){}}"
"function sh(){g.style.display='none';c.style.display='block'}"
"function go(){d(document.getElementById('pw').value).then(function(h){if(h===H){w();sh()}else{document.getElementById('err').textContent='Password not recognised.'}})}"
"document.getElementById('btn').addEventListener('click',go);"
"document.getElementById('pw').addEventListener('keydown',function(e){if(e.key==='Enter')go()});"
"if(v())sh();})();</script></body></html>")

os.makedirs("_site", exist_ok=True)
pathlib.Path(OUT).write_text(body, encoding="utf-8")
print(OUT, len(body.encode()), "bytes")
