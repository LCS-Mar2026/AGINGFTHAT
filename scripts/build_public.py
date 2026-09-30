"""Only reviewed public marketing files may enter the Pages artifact."""
from pathlib import Path
import shutil, re, html
PUBLIC = ['index.html', 'programs-offered.html', 'elite-a-program-details.html', 'programme-b-details.html', 'programme-c-details.html', 'lab-partners.html', '.nojekyll', 'CNAME', 'favicon.svg', 'AFT_Book_Cover.jpg', 'Lee_AFT_Headshot.jpg', 'Gracie1.jpeg', 'Aiden1.jpg', 'Sophie1.jpg', 'Family_Beforeat50.jpg', 'Family_Afterat63.jpg', 'Before39c.jpg', 'Lee&Maria_63.jpeg', 'Before_19.jpeg', 'After_Gym1_1.jpg']
root = Path(__file__).resolve().parents[1]
stage = root / '_site'
if stage.exists(): shutil.rmtree(stage)
stage.mkdir()
for name in PUBLIC:
    source = root / name
    if not source.is_file() or source.is_symlink():
        raise SystemExit('Missing or unsafe public file: ' + name)
    if source.suffix == '.html':
        text = source.read_text()
        if re.search(r'sessionStorage|localStorage|SHA-256|higgsfield\.app|data:image|<iframe', text, re.I):
            raise SystemExit('Forbidden content in public HTML: ' + name)
        for match in re.finditer(r'(?:href|src)=["\']([^"\']+)', text, re.I):
            url = html.unescape(match[1])
            if re.match(r'https?://|mailto:|tel:|#', url): continue
            target = url.split('#')[0].split('?')[0]
            if target and target not in PUBLIC:
                raise SystemExit('Unreviewed local reference in ' + name)
    shutil.copyfile(source, stage / name)
print('PASS: public artifact contains only', len(PUBLIC), 'reviewed marketing files')
