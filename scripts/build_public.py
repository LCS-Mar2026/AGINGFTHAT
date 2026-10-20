"""Only reviewed public marketing files may enter the Pages artifact."""
from pathlib import Path
import shutil, re, html, posixpath
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from localize_blog_images import localize

PUBLIC = ['.nojekyll', 'AFT_Book_Cover.jpg', 'After_Gym1_1.jpg', 'Aiden1.jpg', 'Before39c.jpg', 'Before_19.jpeg', 'CNAME', 'Family_Afterat63.jpg', 'Family_Beforeat50.jpg', 'Gracie1.jpeg', 'Lee&Maria_63.jpeg', 'Lee_AFT_Headshot.jpg', 'Sophie1.jpg', 'aft-logo.png', 'android-chrome-192.png', 'android-chrome-512.png', 'anterior-posture-view.jpg', 'apple-touch-icon.png', 'blog.html', 'brand-guidelines.html', 'dashboard.html', 'elite-a-program-details.html', 'example-report.html', 'favicon.ico', 'favicon.svg', 'index.html', 'lab-partners.html', 'lateral-posture-view.jpg', 'new-bio-age-model.html', 'programs-offered.html', 'report-part-1.html', 'report-part-2.html', 'report-part-3.html', 'report.html', 'site.webmanifest', 'sitemap.xml', 'admin.html', 'bio-age-level-1-model.html', 'level1-section05-mockup.html', 'brand-guidelines-assets-v01-011026.html', 'client-blood-panel.html', 'client-progress.html', 'client-report.html', 'client-scan-history.html', 'programme-b-details.html', 'programme-c-details.html', 'report.css', 'report-part-4.html', 'report-part-5.html', 'social/balance-after-40-one-legged-stance.jpg', 'social/balance-after-40-one-legged-stance-1440.jpg', 'social/balance-after-40-one-legged-stance-story.jpg', 'social/how-to-read-biological-age-results.jpg', 'social/how-to-read-biological-age-results-1440.jpg', 'social/how-to-read-biological-age-results-story.jpg', 'social/butyrate-fibre-biological-age.jpg', 'social/butyrate-fibre-biological-age-1440.jpg', 'social/butyrate-fibre-biological-age-story.jpg', 'social/creatine-brain-phosphate-buffer.jpg', 'social/creatine-brain-phosphate-buffer-1440.jpg', 'social/creatine-brain-phosphate-buffer-story.jpg', 'social/sodium-to-potassium-ratio-healthspan.jpg', 'social/sodium-to-potassium-ratio-healthspan-1440.jpg', 'social/sodium-to-potassium-ratio-healthspan-story.jpg', 'client-login.html']

DEST = Path("_site")


def allowed(p: str) -> bool:
    return p in public_files()


def public_files():
    # New daily articles and their assets do not require a code-list edit.
    articles = [str(p) for p in Path("blog").glob("*.html") if not p.is_symlink()]
    images = [str(p) for p in Path("blog/images").rglob("*")
              if p.is_file() and not p.is_symlink()
              and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif"}]
    artwork = [str(p) for p in Path("assets/site-images").glob("*") if p.is_file() and not p.is_symlink()
               and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}]
    return sorted(set(PUBLIC + articles + images + artwork))


class BlogImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "img" and attrs.get("src"):
            self.sources.append(attrs["src"])
        if tag in {"img", "source"} and attrs.get("srcset"):
            self.sources.extend(part.strip().split()[0] for part in attrs["srcset"].split(",") if part.strip())
        if tag == "meta" and attrs.get("property", attrs.get("name", "")) in {"og:image", "twitter:image"}:
            self.sources.append(attrs.get("content", ""))


def check_blog_assets(files):
    published = set(files)
    for page in ["blog.html", *[p for p in files if p.startswith("blog/") and p.endswith(".html")]]:
        parser = BlogImages()
        text = Path(page).read_text(encoding="utf-8")
        parser.feed(text)
        parser.sources.extend(re.findall(r"url\(['\"]?([^)'\"]+)", text))
        for source in parser.sources:
            url = urlsplit(html.unescape(source))
            if url.scheme == "data":
                continue
            if url.netloc and url.hostname not in {"agingfthat.com", "www.agingfthat.com"}:
                continue
            path = unquote(url.path)
            path = path.lstrip("/") if path.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(page), path))
            if path not in published:
                raise SystemExit("Missing published blog image: " + page + " -> " + source)


def main() -> int:
    localize([p for p in public_files() if p.endswith((".html", ".css"))])
    files = public_files()
    check_blog_assets(files)
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    missing = []
    copied = 0
    for rel in files:
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
    for rel in files:
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
