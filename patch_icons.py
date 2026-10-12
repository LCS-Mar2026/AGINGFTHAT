"""Adds the blood and biometric age panel figures to the dashboard template."""
import ast, pathlib

p = pathlib.Path("dashboard_src/gen.py")
s = p.read_text(encoding="utf-8")
before = len(s.encode())

art = 'POS_S    = "https://cdn.marblism.com/QBo1eqeRDxl.webp"'
newart = art + '\nBLOOD_ART = "https://cdn.marblism.com/X-G7nSsrtUc.webp"' + '\nBA_ART    = "https://cdn.marblism.com/f4-1J604s_r.webp"'
assert s.count(art) == 1, "art anchor"
s = s.replace(art, newart, 1)

blood_old = "P('<div class=\"body\"><div class=\"bloodrow\">')"
blood_new = "P('<div class=\"body\"><div class=\"herofig\"><img src=\"%s\" alt=\"3D render of red blood cells, plasma and molecular chains representing a blood and hormone panel\"></div>'%BLOOD_ART)\n    " + blood_old
assert s.count(blood_old) == 1, "blood anchor"
s = s.replace(blood_old, blood_new, 1)

ba_old = "P('<div class=\"body\"><div class=\"gaugewrap\"><div class=\"gauge\">'+ring(a['pct'],a['col'])"
ba_new = "P('<div class=\"body\"><div class=\"herofig\"><img src=\"%s\" alt=\"3D render of a DNA helix dissolving into an hourglass, representing biological age\"></div>'%BA_ART)\n    " + ba_old
assert s.count(ba_old) == 1, "ba anchor"
s = s.replace(ba_old, ba_new, 1)

ast.parse(s)
p.write_text(s, encoding="utf-8")
print("patched", before, "->", len(s.encode()), "bytes")
print("BLOOD_ART:", s.count("BLOOD_ART"), "BA_ART:", s.count("BA_ART"), "herofig:", s.count("herofig"))
