"""Dashboard stylesheet, mirroring Lee's reference layout."""
CSS = """
:root{--navy:#031522;--panel:#04192a;--panel2:#062033;--line:#0f3b57;--text:#edfaff;--muted:#9fc4d6;--cyan:#2BC7FF;--green:#21c97a;--red:#ff4b4b;--violet:#A855F7;--amber:#FF9F1C}
*{box-sizing:border-box}
body{margin:0;background:var(--navy);color:var(--text);font:13px/1.45 Arial,Helvetica,sans-serif;-webkit-text-size-adjust:100%}
a{color:var(--cyan)}
.hero{display:block;padding:0;background:linear-gradient(120deg,#04243a,#031522 62%);border-bottom:1px solid var(--line)}.hero-band{position:relative;width:100%;height:clamp(58px,10vw,120px);overflow:hidden;border-bottom:1px solid var(--line)}.hero-band img{position:absolute;left:0;top:50%;transform:translateY(-50%);width:100%;height:auto;display:block}.hero-txt{padding:9px 14px 11px}
.hero-txt h1{margin:0;font-size:clamp(19px,5vw,34px);font-weight:900;letter-spacing:-.02em;line-height:1;text-shadow:0 0 14px #2bc7ff55}
.hero-txt h1 em{font-style:normal;color:var(--cyan)}
.hero-txt p{margin:0;font-size:clamp(10px,2.3vw,14px);font-weight:900;letter-spacing:.16em;color:#dff4ff}
.hero-txt .strap{margin:5px 0 0;font-size:clamp(8px,1.9vw,11px);font-weight:800;letter-spacing:.2em;color:var(--cyan)}

.metabar{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border-bottom:1px solid var(--line)}
.metabar div{background:#041c2c;padding:7px 11px;font-size:10px;color:var(--muted)}
.metabar b{display:block;color:#fff;font-size:11.5px;margin-top:1px}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--green);margin-left:5px;vertical-align:middle}
.dot.w{background:var(--amber)}
.wrap{padding:11px 10px 22px;max-width:1500px;margin:0 auto}
.panels{display:grid;gap:9px;grid-template-columns:repeat(2,1fr)}
.panel{background:var(--panel);border:1.5px solid var(--line);border-radius:11px;display:flex;flex-direction:column;overflow:hidden}
.panel.bc{border-color:#1c5d8a}.panel.mp{border-color:#1d7a4e}.panel.hh{border-color:#8a2b2b}.panel.ba{border-color:#6a3a9e}
.ph{display:grid;grid-template-columns:auto 1fr;gap:7px;align-items:center;padding:7px 9px;border-bottom:1px solid var(--line)}
.panel.bc .ph{background:linear-gradient(90deg,#08324d,#061f31)}
.panel.mp .ph{background:linear-gradient(90deg,#073d29,#061f31)}
.panel.hh .ph{background:linear-gradient(90deg,#4a1414,#061f31)}
.panel.ba .ph{background:linear-gradient(90deg,#3a1a56,#061f31)}
.ic{width:26px;height:26px;border-radius:7px;display:grid;place-items:center;font-size:14px;background:#0b2b3f}
.panel.bc .ic{color:var(--cyan);background:#0d3d5c}.panel.mp .ic{color:var(--green);background:#0d4530}
.panel.hh .ic{color:var(--red);background:#4d1414}.panel.ba .ic{color:#d8b4fe;background:#3d1a5c}
.panel.bx{border-color:#2b7fa8}
.panel.bx .ph{background:linear-gradient(90deg,#06324c,#061f31)}
.panel.bx .ic{color:var(--cyan);background:#0d3d5c}
.panel.bx .btn{border-color:#2b7fa8;color:#a8e4ff}
.ph h2{margin:0;font-size:11px;letter-spacing:.1em;font-weight:900;line-height:1.15}
.ph p{margin:2px 0 0;font-size:7.5px;letter-spacing:.07em;color:var(--muted);line-height:1.25}
.body{padding:8px;flex:1;display:flex;flex-direction:column}
.pb{padding:0 8px 8px}
.btn{display:block;width:100%;border:1px solid #1a4f6b;border-radius:7px;background:#08283a;color:#fff;font-weight:900;font-size:9px;letter-spacing:.05em;padding:9px 8px;text-align:center;text-decoration:none;cursor:pointer;font-family:inherit}
.panel.bc .btn{border-color:#1c5d8a;color:#a8e4ff}.panel.mp .btn{border-color:#1d7a4e;color:#a8f7cf}
.panel.hh .btn{border-color:#8a2b2b;color:#ffc9c2}.panel.ba .btn{border-color:#6a3a9e;color:#e3ccff}
.bcgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.fig{position:relative;border-radius:8px;overflow:hidden;background:#02101a;border:1px solid #0f3b57}
.fig img{display:block;width:100%;height:clamp(96px,14.5vw,186px);object-fit:cover;object-position:center}
.stats{display:grid;gap:5px}
.stat{display:flex;align-items:baseline;justify-content:space-between;gap:6px;border-bottom:1px solid #0d2f42;padding-bottom:4px}
.stat span{color:var(--muted);font-size:8.5px;letter-spacing:.05em;text-transform:uppercase}
.stat b{font-size:14px;font-weight:900;line-height:1.1}
.tag{display:inline-block;font-size:8px;font-weight:900;letter-spacing:.05em;padding:1px 5px;border-radius:99px;margin-left:4px;vertical-align:middle}
.ok{background:#0f3f2a;color:#5ff0a8}.bad{background:#42201c;color:#ff9b8f}.warn{background:#42331a;color:#ffd479}.absent{background:#152a3a;color:#8fb8cc}
.chips{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin:8px 0 0}
.chip{background:#06263a;border:1px solid #103f59;border-radius:6px;padding:5px 2px;text-align:center;font-size:6.5px;letter-spacing:.03em;color:#9fc4d6;line-height:1.15}
.chip i{display:block;font-style:normal;font-size:12px;color:var(--cyan);margin-bottom:3px}
.herofig{position:relative;height:clamp(72px,10.2vw,136px);margin:0 0 9px;border-radius:8px;overflow:hidden;border:1px solid #14415a;background:#02101a}.herofig img{display:block;width:100%;height:100%;object-fit:cover;object-position:center}.herofig:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(4,25,42,.10),rgba(4,25,42,.42))}.figpair{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px}
.figpair img{width:100%;height:clamp(96px,14.5vw,186px);object-fit:cover;object-position:center;border-radius:7px;border:1px solid #0f3b57;display:block;background:#02101a}
.sil{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin-bottom:8px}
.sil svg{width:100%;height:auto;display:block}
ul.li{list-style:none;margin:0 0 8px;padding:0}
ul.li li{position:relative;padding-left:12px;font-size:9.5px;color:#d6ecf7;margin-bottom:3px;line-height:1.3}
ul.li li:before{content:"\\2022";position:absolute;left:1px;color:var(--green);font-weight:900}
.panel.hh ul.li li:before{color:var(--red)}
.heartwrap{position:relative;margin-bottom:8px}
.heartwrap img{display:block;width:100%;height:clamp(64px,9vw,118px);object-fit:cover;object-position:center;border-radius:7px}
.ecg{position:absolute;left:0;right:0;top:50%;height:34px;transform:translateY(-50%);width:100%}
.ecg polyline{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px}
.tile{border:1px solid #14415a;border-radius:7px;padding:7px 5px;background:#062028;text-align:center}
.tile small{display:block;font-size:7.5px;letter-spacing:.05em;color:var(--muted);text-transform:uppercase}
.tile b{display:block;font-size:15px;font-weight:900;margin:2px 0 3px;line-height:1}
.tile u{display:inline-block;text-decoration:none;font-size:7.5px;font-weight:900;letter-spacing:.04em;padding:2px 6px;border-radius:99px}
.gaugewrap{display:grid;place-items:center;margin:2px 0 8px}
.gauge{position:relative;width:min(124px,100%);aspect-ratio:1}
.gauge svg{display:block;width:100%;height:100%;transform:rotate(-90deg)}
.gauge .ctr{position:absolute;inset:0;display:grid;place-content:center;text-align:center;padding:0 16px}
.gauge .ctr small{font-size:7px;letter-spacing:.08em;color:var(--muted);text-transform:uppercase;line-height:1.2}
.gauge .ctr b{font-size:26px;font-weight:900;line-height:1;display:block;margin:2px 0 1px}
.gauge .ctr em{font-style:normal;font-size:7.5px;letter-spacing:.05em;color:var(--muted);display:block}
.gauge .ctr u{text-decoration:none;display:block;font-size:8px;font-weight:800;color:#fff;margin-top:2px}
.strip{text-align:center;font-size:9.5px;font-weight:900;letter-spacing:.04em;border-radius:6px;padding:6px;margin-bottom:7px}
.strip.good{background:#0f3f2a;color:#5ff0a8}.strip.bad{background:#421c1c;color:#ffb3a8}.strip.warn{background:#42331a;color:#ffd479}
.note{font-style:italic;font-size:8.5px;color:var(--muted);text-align:center;margin:0 0 8px;line-height:1.3}
.mini{display:grid;gap:5px;margin:0 0 8px}
.minirow{display:grid;grid-template-columns:1fr 48px;align-items:center;gap:6px;font-size:8.5px;color:var(--muted)}
.minirow .track{height:7px;border-radius:99px;background:#0d2b3c;overflow:hidden}
.minirow b{font-size:9px;text-align:right;color:#dff2fb}
.bloodrow{display:grid;gap:6px}
.bm{display:grid;grid-template-columns:1fr auto;gap:6px;align-items:center;border:1px solid #0f3b57;border-radius:7px;padding:6px 8px;background:#062028}
.bm span{font-size:9.5px;color:#dff2fb}
.bm small{display:block;font-size:7.5px;color:var(--muted);margin-top:1px}
.bm b{font-size:12px;font-weight:900;text-align:right;white-space:nowrap}
.panel.wide{margin-top:9px}
.two{display:grid;gap:9px;margin-top:9px}
.card{background:var(--panel);border:1.5px solid var(--line);border-radius:11px;padding:10px}
.card h2{margin:0 0 8px;font-size:10.5px;letter-spacing:.1em;font-weight:900;color:#fff}
.steps{display:grid;grid-template-columns:1fr;gap:7px}
.step{display:grid;grid-template-columns:auto 1fr;gap:8px;align-items:center}
.step i{width:24px;height:24px;border-radius:50%;border:1.5px solid var(--cyan);color:var(--cyan);display:grid;place-items:center;font-style:normal;font-weight:900;font-size:10px}
.step b{display:block;font-size:9.5px}
.step small{font-size:8.5px;color:var(--muted)}
.docs{display:grid;gap:5px}
.doc{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:center;border:1px solid #0f3b57;border-radius:7px;padding:6px 8px;font-size:9.5px;background:#062028}
.doc small{display:block;color:var(--muted);font-size:7.5px;margin-top:1px}
.doc em{font-style:normal;font-size:7.5px;font-weight:900;letter-spacing:.04em;color:#8fb8cc;border:1px solid #1a4f6b;border-radius:99px;padding:2px 7px;white-space:nowrap}
footer{border-top:1px solid var(--line);padding:12px;text-align:center;font-size:9.5px;color:#7899a9;background:#020d16;margin-top:12px}
footer .l{font-weight:900;letter-spacing:.07em;color:#cfe9f5}
footer .r{margin-top:3px;letter-spacing:.09em}
.disc{font-size:8.5px;color:#7899a9;margin:6px 0 0;line-height:1.4}
@media(min-width:700px){
 .metabar{grid-template-columns:repeat(4,1fr)}
 .wrap{padding:14px 14px 28px}
 .steps{grid-template-columns:repeat(4,1fr)}
 .bloodrow{grid-template-columns:1fr 1fr}
 .two{grid-template-columns:1.35fr 1fr}
 .fig{max-width:270px;margin:0 auto}
}
@media(min-width:1080px){
 .panels{grid-template-columns:repeat(4,1fr);gap:11px}
 .wrap{padding:16px 18px 34px}
 .ph h2{font-size:11.5px}
 .stat b{font-size:15px}
 .bloodrow{grid-template-columns:repeat(3,1fr)}
 .two{grid-template-columns:1.4fr 1fr}
}
"""
