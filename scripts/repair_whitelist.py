# -*- coding: utf-8 -*-
import ast
import pathlib
import re

p = pathlib.Path('scripts/build_public.py')
src = p.read_text(encoding='utf-8')
PUB = None
for node in ast.parse(src).body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'PUBLIC':
        PUB = ast.literal_eval(node.value)
assert PUB is not None
assert 'admin.html' in PUB
allow = list(PUB)
for name in ('bio-age-level-1-model.html', 'level1-section05-mockup.html'):
    if name not in allow:
        allow.insert(allow.index('admin.html') + 1, name)
lit = 'PUBLIC = [\n' + ''.join('    "%s",\n' % x for x in allow) + ']'
first = re.search(r'PUBLIC = \[.*?\]', src, re.S)
assert first
out = src[:first.start()] + lit + src[first.end():]
ast.parse(out)
p.write_text(out, encoding='utf-8')
print('PUBLIC rebuilt', len(allow))
