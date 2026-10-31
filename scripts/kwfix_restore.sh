#!/bin/bash
set -e
: > /tmp/kwfix_joined.txt
for u in \
  "https://cdn.marblism.com/YlXhdBbboAf.txt" \
  "https://cdn.marblism.com/JOYI_Dj_es0.txt" \
  "https://cdn.marblism.com/AWMA-Cxz69A.txt" \
  "https://cdn.marblism.com/mvOFnWwouFL.txt" ; do
  curl -sSL "$u" >> /tmp/kwfix_joined.txt
done
cat /tmp/kwfix_joined.txt > blog/glymphatic-system-brain-waste-clearance.html
python3 -c "
d=open('blog/glymphatic-system-brain-waste-clearance.html','rb').read()
import hashlib
print('restored', len(d), hashlib.sha256(d).hexdigest()[:16])
assert len(d)>19000
assert b'glymphatic system' in d
assert b'perceived age' not in d
"
git config user.name "Penny (Blog Writer)"
git config user.email "penny@agingfthat.com"
git add blog/glymphatic-system-brain-waste-clearance.html
git diff --cached --quiet && echo "nothing to commit" || git commit -m "Restore full glymphatic article with corrected keywords [automated]"
git pull --rebase --autostash origin main
git push
