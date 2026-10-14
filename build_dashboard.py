"""Validate committed dashboards without overwriting them at deployment."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for name in ("dashboard.html", "example-report.html", "client-report.html"):
    path = ROOT / name
    content = path.read_text(encoding="utf-8")
    if len(content.encode("utf-8")) < 12000 or "<html" not in content.lower() or "</html>" not in content.lower():
        raise SystemExit("Invalid or incomplete dashboard: " + name)
    print(name, len(content.encode("utf-8")), "bytes; committed content retained")
