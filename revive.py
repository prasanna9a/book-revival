"""Local PDF -> draft EPUB 3 conversion. Never silently invent or rewrite text."""
import argparse
import datetime
import hashlib
import html
import json
from pathlib import Path
import subprocess
import tempfile
import unicodedata
import zipfile


def esc(value):
    return html.escape(str(value), quote=True)


def document(title, body, language):
    return ('<?xml version="1.0" encoding="utf-8"?>'
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" '
            f'xml:lang="{esc(language)}" lang="{esc(language)}">'
            f'<head><title>{esc(title)}</title><link rel="stylesheet" '
            'type="text/css" href="style.css"/></head>'
            f'<body>{body}</body></html>')


def write_epub(output, title, language, pages, source_hash):
    """pages: dicts with text, method, and optional PNG bytes. All are drafts."""
    if not pages:
        raise ValueError('Cannot create an empty book')
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    items = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
             '<item id="css" href="style.css" media-type="text/css"/>']
    spine, links = [], []
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        staged = Path(tmp) / 'book.epub'
        with zipfile.ZipFile(staged, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
            z.writestr('META-INF/container.xml', '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
            z.writestr('EPUB/style.css', 'body{line-height:1.65;margin:5%;font-family:serif} p{margin:0 0 1em} img{max-width:100%;height:auto} .notice{border:1px solid;padding:1em} a{overflow-wrap:anywhere}')
            for n, page in enumerate(pages, 1):
                page_id = f'p{n}'
                items.append(f'<item id="{page_id}" href="{page_id}.xhtml" media-type="application/xhtml+xml"/>')
                spine.append(f'<itemref idref="{page_id}"/>')
                links.append(f'<li><a href="{page_id}.xhtml#page{n}">Source PDF page {n}</a></li>')
                text = unicodedata.normalize('NFC', page['text']).strip()
                paragraphs = ''.join(f'<p>{esc(p)}</p>' for p in text.split('\n\n') if p.strip())
                if not paragraphs:
                    paragraphs = '<p>Text extraction unavailable. Please review the source scan.</p>'
                body = f'<section><span epub:type="pagebreak" role="doc-pagebreak" id="page{n}" aria-label="Source PDF page {n}"/><h1>Source PDF page {n}</h1>'
                if n == 1:
                    body += '<p class="notice">Unreviewed draft. Text may contain extraction or OCR errors. Original spelling is preserved; compare against the source scan.</p>'
                body += paragraphs
                if page.get('image'):
                    image = f'scan{n}.png'
                    z.writestr(f'EPUB/{image}', page['image'])
                    items.append(f'<item id="scan{n}" href="{image}" media-type="image/png"/>')
                    body += f'<figure><img src="{image}" alt="Original scanned source PDF page {n}; detailed image description pending review"/><figcaption>Original source PDF page {n}</figcaption></figure>'
                z.writestr(f'EPUB/{page_id}.xhtml', document(f'{title} — page {n}', body + '</section>', language))
            nav = '<h1>Contents</h1><nav epub:type="toc" id="toc"><h2>Source pages</h2><ol>' + ''.join(links) + '</ol></nav>'
            nav += '<nav epub:type="page-list"><h2>Source PDF pages</h2><ol>' + ''.join(links) + '</ol></nav>'
            z.writestr('EPUB/nav.xhtml', document(title, nav, language))
            modified = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            package = ('<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
                       f'<dc:identifier id="book-id">urn:sha256:{esc(source_hash)}</dc:identifier><dc:title>{esc(title)}</dc:title><dc:language>{esc(language)}</dc:language><dc:source>Source PDF SHA-256: {esc(source_hash)}</dc:source><dc:description>Unreviewed conversion draft; source PDF page indices are not printed page numbers.</dc:description><meta property="dcterms:modified">{modified}</meta></metadata><manifest>'
                       + ''.join(items) + '</manifest><spine>' + ''.join(spine) + '</spine></package>')
            z.writestr('EPUB/package.opf', package)
        staged.replace(output)


def convert(source, output, language='te', ocr_language='tel+eng', force_ocr=False, scans=True):
    import fitz
    source, output = Path(source), Path(output)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    pages, report = [], []
    with fitz.open(source) as pdf, tempfile.TemporaryDirectory() as tmp:
        if pdf.needs_pass:
            raise ValueError('Encrypted PDF requires an unlocked source')
        for i, page in enumerate(pdf):
            text = page.get_text('text', sort=True)
            method = 'embedded-text'
            image = None
            needs_ocr = force_ocr or len(text.strip()) < 40
            if scans or needs_ocr:
                image = page.get_pixmap(dpi=180 if not needs_ocr else 300).tobytes('png')
            if needs_ocr:
                image_path = Path(tmp) / 'page.png'
                image_path.write_bytes(image)
                result = subprocess.run(['tesseract', str(image_path), 'stdout', '-l', ocr_language], check=True, capture_output=True, text=True)
                text, method = result.stdout, 'tesseract'
            pages.append({'text': text, 'method': method, 'image': image if scans else None})
            report.append({'source_page': i + 1, 'method': method, 'characters': len(text.strip()), 'review_required': True})
    write_epub(output, source.stem, language, pages, digest)
    output.with_suffix('.report.json').write_text(json.dumps({'source_sha256': digest, 'status': 'unreviewed', 'pages': report}, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--language', default='te')
    parser.add_argument('--ocr-language', default='tel+eng')
    parser.add_argument('--force-ocr', action='store_true')
    parser.add_argument('--no-scans', action='store_true')
    args = parser.parse_args()
    sources = sorted(args.input.rglob('*.pdf')) if args.input.is_dir() else [args.input]
    if not sources:
        parser.error('No lowercase .pdf files found')
    failures = []
    for source in sources:
        target = (args.output / source.relative_to(args.input).with_suffix('.epub')) if args.input.is_dir() else args.output
        try:
            convert(source, target, args.language, args.ocr_language, args.force_ocr, not args.no_scans)
            print(f'Created draft: {target}')
        except Exception as exc:
            failures.append(str(source))
            print(f'FAILED {source}: {exc}')
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
