"""Only reviewed public marketing files may enter the Pages artifact."""
from pathlib import Path
import shutil, re, html, posixpath

PUBLIC = [".nojekyll", "AFT_Book_Cover.jpg", "After_Gym1_1.jpg", "Aiden1.jpg", "Before39c.jpg", "Before_19.jpeg", "CNAME", "Family_Afterat63.jpg", "Family_Beforeat50.jpg", "Gracie1.jpeg", "Lee&Maria_63.jpeg", "Lee_AFT_Headshot.jpg", "Sophie1.jpg", "aft-logo.png", "android-chrome-192.png", "android-chrome-512.png", "anterior-posture-view.jpg", "apple-touch-icon.png", "blog.html", "blog/age-reversal-brighton-hove.html", "blog/biological-age-test-vs-calculator.html", "blog/healthspan-after-40.html", "blog/healthspan-vs-lifespan.html", "blog/how-to-reverse-biological-age-5-steps.html", "brand-guidelines-assets-v01-011026.html", "dexa-scan-21-dec-2024.jpg", "dexa-scan-25-apr-2025.jpg", "elite-a-program-details.html", "example-report.html", "favicon.ico", "favicon.svg", "index.html", "lab-partners.html", "lateral-posture-view.jpg", "new-bio-age-model.html", "programme-b-details.html", "programme-c-details.html", "programs-offered.html", "report-part-1.html", "report-part-2.html", "report-part-3.html", "report-part-4.html", "report-part-5.html", "report.css", "report.html", "robots.txt", "site.webmanifest", "sitemap.xml"]

root = Path(__file__).resolve().parents[1]
stage = root / "_site"
if stage.exists(): shutil.rmtree(stage)
stage.mkdir()
for name in PUBLIC:
    source = root / name
    if not source.is_file() or source.is_symlink():
        raise SystemExit("Missing or unsafe public file: " + name)
    if source.suffix == ".html":
        text = source.read_text()
        if re.search(r"sessionStorage|localStorage|SHA-256|higgsfield\.app|data:image|<iframe", text, re.I):
            raise SystemExit("Forbidden content in public HTML: " + name)
        base = posixpath.dirname(name)
        for match in re.finditer(r"(?:href|src)=[\"\']([^\"\']+)", text, re.I):
            url = html.unescape(match[1])
            if re.match(r"https?://|mailto:|tel:#", url): continue
            ref = url.split("#")[0].split("?")[0]
            target = ref.lstrip("/") if ref.startswith("/") else posixpath.normpath(posixpath.join(base, ref))
            if target in ("", "."): continue
            if target.startswith(".."):
                continue
            if target not in PUBLIC:
                raise SystemExit("Unreviewed local reference in " + name + ": " + target)
    (stage / name).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, stage / name)
print("PASS: public artifact contains only", len(PUBLIC), "reviewed marketing files")
