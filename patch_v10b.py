# -*- coding: utf-8 -*-
"""Make the chart key show the current value, not the projected end."""
import ast
import pathlib

g = pathlib.Path("dashboard_src/gen.py")
s = g.read_text(encoding="utf-8")
OLD = """def trend_legend(series):
    return '<div class="tlegend">'+"".join(
        '<span><i style="background:%s"></i>%s <b>%s</b></span>'%(x['c'],x['n'],x['vals'][-1])
        for x in series)+'</div>'"""
NEW = """def trend_legend(series):
    def cur(x):
        nh = x.get('nh', len(x['vals']))
        return x['vals'][nh-1]
    return '<div class="tlegend">'+"".join(
        '<span><i style="background:%s"></i>%s <b>%s</b></span>'%(x['c'],x['n'],cur(x))
        for x in series)+'</div>'"""
if "def cur(x)" not in s:
    assert s.count(OLD) == 1
    s = s.replace(OLD, NEW, 1)
    ast.parse(s)
    g.write_text(s, encoding="utf-8")
    print("legend patched")
else:
    print("legend already current")
