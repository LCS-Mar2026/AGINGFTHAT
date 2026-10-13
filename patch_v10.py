# -*- coding: utf-8 -*-
"""v10: blood rows no longer clip, gauge 3x bigger and brighter, chart labels
removed in favour of the key beneath, vendor names gone, biomechanical not chiropractic."""
import ast, pathlib, re

# ---------------- gen.py ----------------
g = pathlib.Path("dashboard_src/gen.py")
s = g.read_text(encoding="utf-8")

# 1. brighter red and lime green
s = s.replace('GREEN="#21c97a"; AMBER="#FF9F1C"; RED="#ff4b4b"',
              'GREEN="#7CFF1F"; AMBER="#FFB020"; RED="#FF1744"', 1)
assert 'GREEN="#7CFF1F"' in s

# 2. chart functions: drop the right-hand value labels, reclaim the gutter
s = s.replace('    W,H = 560,200; padL,padR,padT,padB = 40,66,14,30',
              '    W,H = 560,200; padL,padR,padT,padB = 40,14,14,30', 1)
s = s.replace('    W,H = 560,220; padL,padR,padT,padB = 40,66,14,32',
              '    W,H = 560,220; padL,padR,padT,padB = 40,14,14,32', 1)
label_block = """        p.append('<text x="%.1f" y="%.1f" fill="%s" font-size="12" font-weight="700">%s</text>'
                 %(X(idx[-1])+9, Y(vals[-1])+4, x['c'], x.get('lbl', vals[-1])))
"""
assert s.count(label_block) == 1
s = s.replace(label_block, "", 1)
label_block2 = """        if x.get('lbl'):
            p.append('<text x="%.1f" y="%.1f" fill="%s" font-size="12" font-weight="700">%s</text>'
                     %(X(len(vals)-1)+9, Y(vals[-1])+4, x['c'], x['lbl']))
"""
assert s.count(label_block2) == 1, s.count(label_block2)
s = s.replace(label_block2, "", 1)
assert "font-weight=\"700\">%s</text>" not in s.split("def _grid")[1].split("def page")[0]

# 3. legend keeps the current value, so the key carries the numbers
s = s.replace("""def trend_legend(series):
    return '<div class="tlegend">'+"".join(
        '<span><i style="background:%s"></i>%s <b>%s</b></span>'%(x['c'],x['n'],x['vals'][-1])
        for x in series)+'</div>'""",
"""def trend_legend(series):
    return '<div class="tlegend">'+"".join(
        '<span><i style="background:%s"></i>%s <b>%s</b></span>'%(x['c'],x['n'],x['vals'][-1])
        for x in series)+'</div>'""", 1)

# 4. no vendor names, and chiropractic becomes biomechanical
s = s.replace('("Chiropractic Assessment","Posture, alignment and movement")',
              '("Biomechanical Assessment","Posture, alignment and movement")', 1)
s = s.replace('("AFT Bespoke Panel 2","Sussex Pathology &#183; 7 markers scored")',
              '("AFT Bespoke Blood Panel","Drawn 08 Oct 2026 &#183; 5 markers scored")', 1)
s = s.replace('note="Results as reported by Sussex Pathology, 08 Oct 2026.',
              'note="Results from the AFT Bespoke Blood Panel, drawn 08 Oct 2026.', 1)
assert "Chiropractic" not in s and "Sussex" not in s, "vendor text remains"
ast.parse(s)
g.write_text(s, encoding="utf-8")
print("gen.py", len(s.encode()), "| chart labels removed | vendors cleared")

# ---------------- css.py ----------------
c = pathlib.Path("dashboard_src/css.py")
t = c.read_text(encoding="utf-8")

# one wide column for the blood markers: they were clipping in narrow tracks
t = t.replace(' .bloodrow{grid-template-columns:1fr 1fr}\n', '')
t = t.replace(' .bloodrow{grid-template-columns:repeat(3,1fr)}\n', '')
t = t.replace('.bloodrow{display:grid;gap:6px}',
              '.bloodrow{display:grid;grid-template-columns:1fr;gap:6px}', 1)
t = t.replace('.bm{display:grid;grid-template-columns:1fr auto;gap:6px;align-items:center;'
              'border:1px solid #0f3b57;border-radius:7px;padding:6px 8px;background:#062028}',
              '.bm{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px;align-items:center;'
              'border:1px solid #0f3b57;border-radius:7px;padding:6px 8px;background:#062028;min-width:0}', 1)
t = t.replace('.bm b{font-size:15px;font-weight:900;text-align:right;white-space:nowrap;letter-spacing:-.01em;text-transform:none}',
              '.bm b{font-size:14px;font-weight:900;text-align:right;letter-spacing:-.01em;text-transform:none;min-width:0}', 1)
t = t.replace('.bm span{font-size:9px;', '.bm span{min-width:0;font-size:9px;', 1)
t = t.replace('.panel{background:var(--panel);border:1.5px solid var(--line);border-radius:11px;display:flex;flex-direction:column;'
              'overflow:hidden;min-width:0;width:100%}',
              '.panel{background:var(--panel);border:1.5px solid var(--line);border-radius:11px;display:flex;flex-direction:column;'
              'min-width:0;width:100%}', 1)

# gauge three times bigger
t = t.replace('.gauge{position:relative;width:min(124px,100%);aspect-ratio:1}',
              '.gauge{position:relative;width:min(330px,100%);aspect-ratio:1}', 1)
t = t.replace('.gauge .ctr small{font-size:8px;', '.gauge .ctr small{font-size:11px;', 1)
t = t.replace('.gauge .ctr b{font-size:30px;', '.gauge .ctr b{font-size:62px;', 1)
t = t.replace('.gauge .ctr em{font-style:normal;font-size:7.5px;', '.gauge .ctr em{font-style:normal;font-size:12px;', 1)
t = t.replace('.gauge .ctr u{text-decoration:none;display:block;font-size:8px;',
              '.gauge .ctr u{text-decoration:none;display:block;font-size:12px;', 1)
# thicker ring stroke
c.write_text(t, encoding="utf-8")
print("css.py", len(t.encode()))

# ring stroke a touch thicker to suit the larger gauge
s2 = g.read_text(encoding="utf-8")
s2 = s2.replace('stroke="#0d2b3c" stroke-width="13"', 'stroke="#0d2b3c" stroke-width="11"')
s2 = s2.replace('stroke-width="13" ', 'stroke-width="11" ')
ast.parse(s2)
g.write_text(s2, encoding="utf-8")
print("ring stroke adjusted")
