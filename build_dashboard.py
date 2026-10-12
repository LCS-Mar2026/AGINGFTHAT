# -*- coding: utf-8 -*-
"""Rebuild both dashboard pages from the shared template in dashboard_src/."""
import os, shutil, subprocess, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "dashboard_src"

for f in ("dashboard.html", "example-report.html"):
    p = SRC / f
    if p.exists():
        p.unlink()

r = subprocess.run([sys.executable, "gen.py"], cwd=str(SRC), capture_output=True, text=True)
print(r.stdout)
print(r.stderr)
if r.returncode != 0:
    raise SystemExit("generator failed")

for f in ("dashboard.html", "example-report.html"):
    src = SRC / f
    if not src.is_file():
        raise SystemExit("missing output: " + f)
    b = src.read_bytes()
    if len(b) < 12000:
        raise SystemExit("output too small: " + f)
    (HERE / f).write_bytes(b)
    print("%-22s %6d bytes" % (f, len(b)))
