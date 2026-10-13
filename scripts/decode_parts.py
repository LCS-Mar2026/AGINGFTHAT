import base64
import pathlib

PAIRS = [
    ("p1.b64", "dashboard_src/gen_p1.txt"),
    ("p2.b64", "dashboard_src/gen_p2.txt"),
    ("dash.b64", "dashboard.html"),
    ("ex.b64", "example-report.html"),
    ("css.b64", "dashboard_src/css.py"),
]
for src, dst in PAIRS:
    data = base64.b64decode(pathlib.Path(src).read_text())
    pathlib.Path(dst).write_bytes(data)
    print(dst, len(data), "bytes")
