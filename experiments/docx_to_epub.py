"""Local DOCX/Pandoc feasibility adapter. Not a public-upload sandbox."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from xml.etree import ElementTree as ET
import zipfile


def convert(source, output, title=None, language='en', timeout=120):
    import pypandoc
    source, output = Path(source).resolve(), Path(output).resolve()
    if source.suffix.lower() != '.docx':
        raise ValueError('This feasibility adapter accepts DOCX only; DOC and PDF need other routes')
    if source.stat().st_size > 50 * 1024 * 1024:
        raise ValueError('DOCX exceeds the pilot 50 MiB limit')
    with zipfile.ZipFile(source) as z:
        names = z.namelist()
        if 'word/document.xml' not in names:
            raise ValueError('Missing Word document part')
        if sum(i.file_size for i in z.infolist()) > 100 * 1024 * 1024:
            raise ValueError('Expanded DOCX exceeds 100 MiB')
        if any('vbaproject' in n.lower() for n in names):
            raise ValueError('Macro content is not supported')
    output.parent.mkdir(parents=True, exist_ok=True)
    pandoc = pypandoc.get_pandoc_path()
    version = subprocess.run([pandoc, '--version'], check=True, capture_output=True, text=True, timeout=10).stdout.splitlines()[0]
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        staged = Path(tmp) / 'book.epub'
        result = subprocess.run([
            pandoc, str(source), '--from=docx', '--to=epub3', '--standalone',
            '--sandbox', '--toc', '--metadata', f'title={title or source.stem}',
            '--metadata', f'lang={language}', '--output', str(staged),
        ], check=True, capture_output=True, text=True, timeout=timeout)
        with zipfile.ZipFile(staged) as z:
            if z.namelist()[0] != 'mimetype' or z.read('mimetype') != b'application/epub+zip':
                raise ValueError('Invalid EPUB container')
            for name in z.namelist():
                if name.endswith(('.xml', '.opf', '.xhtml')):
                    ET.fromstring(z.read(name))
            images = [n for n in z.namelist() if n.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))]
        staged.replace(output)
    report = {
        'adapter': 'docx-pandoc-feasibility', 'engine': version,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'language': language, 'output_bytes': output.stat().st_size,
        'embedded_images': len(images), 'engine_warnings': result.stderr.strip(),
        'checks': {'container_and_xml': 'passed', 'epubcheck': 'not_run',
                   'android_device': 'not_run', 'editorial_review': 'not_run'},
        'status': 'draft',
    }
    output.with_suffix('.report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--title')
    parser.add_argument('--language', default='en')
    args = parser.parse_args()
    print(json.dumps(convert(args.source, args.output, args.title, args.language), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
