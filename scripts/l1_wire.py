# -*- coding: utf-8 -*-
"""Whitelist the Level 1 model page and the section 05 mockup, and verify both files."""
import pathlib

H = "88fd5b3c36c67f85583f1ca1b411c84351a4890e887b2d7b9e8fec304550201e"
PAGES = ["bio-age-level-1-model.html", "level1-section05-mockup.html"]

for name in PAGES:
    t = pathlib.Path(name).read_text(encoding="utf-8")
    assert len(t) > 8000, name
    assert "<html" in t and "</html>" in t, name
    print(name, len(t.encode()), "bytes")
assert H in pathlib.Path("bio-age-level-1-model.html").read_text(encoding="utf-8")

f = pathlib.Path("scripts/build_public.py")
s = f.read_text(encoding="utf-8")
for name in PAGES:
    if name not in s:
        marker = "admin.html"
        i = s.index(marker) + len(marker)
        s = s[:i] + ', "' + name + '"' + s[i:]
        f.write_text(s, encoding="utf-8")
out = f.read_text(encoding="utf-8")
for name in PAGES:
    assert name in out, name
    print("whitelisted:", name)
