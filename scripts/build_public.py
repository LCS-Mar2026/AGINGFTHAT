"""Only reviewed public marketing files may enter the Pages artifact."""
from pathlib import Path
import shutil, re, html, posixpath

PUBLIC = [".nojekyll", "AFT_Book_Cover.jpg", "After_Gym1_1.jpg", "Aiden1.jpg", "Before39c.jpg", "Before_19.jpeg", "CNAME", "Family_Afterat63.jpg", "Family_Beforeat50.jpg", "Gracie1.jpeg", "Lee&Maria_63.jpeg", "Lee_AFT_Headshot.jpg", "Sophie1.jpg", "aft-logo.png", "android-chrome-192.png", "android-chrome-512.png", "anterior-posture-view.jpg", "apple-touch-icon.png", "blog.html", "blog/age-reversal-brighton-hove.html", "blog/balance-after-40-one-legged-stance.html", "blog/biological-age-test-vs-calculator.html", "blog/healthspan-after-40.html", "blog/healthspan-vs-lifespan.html", "blog/how-to-read-biological-age-results.html", "blog/how-to-reverse-biological-age-5-steps.html", "blog/fibre-the-most-ignored-number-in-healthspan.html", "blog/heart-rate-variability-after-40-vagal-tone.html", "blog/muscle-as-an-endocrine-organ-myokines-strength-training-over-50.html", "blog/vo2max-after-40.html", "brand-guidelines.html", "dashboard.html", "elite-a-program-details.html", "example-report.html", "favicon.ico", "favicon.svg", "index.html", "lab-partners.html", "lateral-posture-view.jpg", "new-bio-age-model.html", "programs-offered.html", "report-part-1.html", "report-part-2.html", "report-part-3.html", "report.html", "site.webmanifest", "sitemap.xml", "admin.html", "brand-guidelines-assets-v01-011026.html", "client-blood-panel.html", "client-progress.html", "client-report.html", "client-scan-history.html", "programme-b-details.html", "programme-c-details.html", "report.css", "report-part-4.html", "report-part-5.html", "social/balance-after-40-one-legged-stance.jpg", "social/balance-after-40-one-legged-stance-1440.jpg", "social/balance-after-40-one-legged-stance-story.jpg", "social/how-to-read-biological-age-results.jpg", "social/how-to-read-biological-age-results-1440.jpg", "social/how-to-read-biological-age-results-story.jpg"]

DEST = Path("_site")


def allowed(p: str) -> bool:
    return p in PUBLIC


def main() -> int:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    missing = []
    copied = 0
    for rel in PUBLIC:
        src = Path(rel)
        if not src.is_file():
            missing.append(rel)
            continue
        out = DEST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
        copied += 1
    if missing:
        raise SystemExit("Missing or unsafe public file: " + ", ".join(missing))
    for rel in PUBLIC:
        if not rel.endswith(".html"):
            continue
        f = DEST / rel
        t = f.read_text(encoding="utf-8")
        depth = len(Path(rel).parts) - 1
        prefix = "../" * depth
        t = re.sub(r'href="(?!/|\.\./|https?:|mailto:|tel:|#)', 'href="' + prefix, t)
        f.write_text(t, encoding="utf-8")
    print("copied", copied, "files to _site")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
