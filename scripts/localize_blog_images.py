"""Copy artwork to this site's own images directory before publication.

Penny can supply articles containing Marblism artwork URLs. Publication fetches
and verifies the artwork, rewrites every occurrence (including social metadata),
and serves it from agingfthat.com. A failed download never replaces a good URL.
"""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r"https?://cdn\.marblism\.com/[^\s\"'<>\\)]+")
MAX_BYTES = 20 * 1024 * 1024
PORTAL_ARTWORK = ["https://cdn.marblism.com/f4-1J604s_r.webp",
                  "https://cdn.marblism.com/9J9277dyCCt.webp"]


def normalize_root_assets(text, page):
    """Repair shared root assets referenced relatively from article subfolders."""
    def replacement(match):
        value = match.group("asset")
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
            return match.group(0)
        path = unquote(parsed.path)
        if (page.parent / path).is_file():
            return match.group(0)
        candidate = (ROOT / path).resolve()
        if not candidate.is_relative_to(ROOT.resolve()) or not candidate.is_file():
            return match.group(0)
        # Preserve any query string or fragment attached to the asset.
        start, end = match.span("asset")
        offset = match.start()
        return match.group(0)[:start-offset] + "/" + value + match.group(0)[end-offset:]

    text = re.sub(r"url\(\s*['\"]?(?P<asset>[^\s)'\"]+)['\"]?\s*\)", replacement, text)
    return re.sub(r"\bsrc\s*=\s*['\"](?P<asset>[^'\"]+)['\"]", replacement, text)


def localize(pages=None) -> int:
    pages = [ROOT / page for page in pages] if pages is not None else [*sorted(ROOT.glob("*.html")), *sorted((ROOT / "blog").glob("*.html")), *sorted(ROOT.glob("*.css"))]
    contents = {page: page.read_text(encoding="utf-8") for page in pages}
    urls = sorted({*PORTAL_ARTWORK, *[url for text in contents.values() for url in URL.findall(text)]})
    if not urls:
        return 0
    target = ROOT / "assets/site-images"
    target.mkdir(parents=True, exist_ok=True)

    def download(url):
        from PIL import Image
        stem = "artwork-" + sha256(url.encode()).hexdigest()[:20]
        for existing in target.glob(stem + ".*"):
            if existing.suffix not in {".jpg", ".png", ".webp", ".gif"}:
                continue
            with Image.open(existing) as picture:
                picture.verify()
            return url, "/assets/site-images/" + existing.name
        with urlopen(Request(url, headers={"User-Agent": "AFT artwork publisher"}), timeout=45) as reply:
            data = reply.read(MAX_BYTES + 1)
        if not data or len(data) > MAX_BYTES:
            raise ValueError("Empty or oversized artwork")
        with Image.open(BytesIO(data)) as picture:
            picture.verify()
            suffix = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "GIF": ".gif"}.get(picture.format)
            if not suffix:
                raise ValueError("Unsupported artwork format")
        name = stem + suffix
        destination = target / name
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        temporary.write_bytes(data)
        temporary.replace(destination)
        return url, "/assets/site-images/" + name

    replacements = {}
    failures = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs = [(url, pool.submit(download, url)) for url in urls]
        for url, future in jobs:
            try:
                source, path = future.result()
                replacements[source] = path
            except Exception as exc:
                failures.append(url + " (" + type(exc).__name__ + ")")
    # Keep all source HTML intact until every image has been verified.
    if failures:
        raise RuntimeError("Artwork could not be imported; original source URLs retained: " + ", ".join(failures))
    for page, text in contents.items():
        for source, path in replacements.items():
            text = text.replace(source, "https://agingfthat.com" + path)
        text = normalize_root_assets(text, page)
        page.write_text(text, encoding="utf-8")
    print("Verified", len(replacements), "artwork images on this site's own hosting")
    return len(replacements)


if __name__ == "__main__":
    localize()
