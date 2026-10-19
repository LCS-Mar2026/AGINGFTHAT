import re
p = "scripts/build_public.py"
w = open(p, encoding="utf-8").read()
for name in ["social/seed-oils-food-supply-healthspan.jpg", "social/seed-oils-food-supply-healthspan-1440.jpg", "social/seed-oils-food-supply-healthspan-story.jpg"]:
    for pat in ('"' + name + '", ', ', "' + name + '"', '"' + name + '"'):
        w = w.replace(pat, "", 1)
open(p, "w", encoding="utf-8").write(w)
print("whitelist cleaned")
