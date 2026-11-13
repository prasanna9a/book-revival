# Book Revival

Old stories, comfortable modern reading. A Telugu-first, local conversion toolkit and restoration roadmap for scanned storybooks.

## Working prototype

`revive.py` converts one PDF or a directory tree into draft EPUB 3 packages. It extracts embedded text, falls back to local Tesseract OCR on sparse pages, preserves Unicode, includes source scans by default, provides source PDF page navigation, and writes a review report. It never uses a remote AI service or rewrites the story.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
# Install Tesseract and the tel + eng language data using your OS package manager.
tesseract --list-langs
python revive.py data/originals build/epub --language te --ocr-language tel+eng
python -m unittest discover -s tests -v
```

Single-file example: `python revive.py data/issue.pdf build/issue.epub`.
Use `--force-ocr` for a corrupt text layer; `--no-scans` makes smaller drafts but removes the in-book facsimile. Existing outputs are replaced. Input PDFs remain unchanged. Folder mode currently selects lowercase `.pdf` extensions.

## Status and limitations

This is a starting implementation, not a finished restoration service. Automated EPUB packaging tests use synthetic text. Actual collection OCR and EPUBCheck validation must be completed before publishing any edition. Install PyMuPDF and Tesseract before PDF conversion. Telugu OCR quality, column reading order, story boundaries, illustrations, captions, printed page labels, and text alternatives need editorial review. Source scans are embedded as whole pages; illustration extraction and layout reconstruction are future work. Sparse-text detection is a heuristic and cannot establish OCR correctness. Scans can make EPUBs large. The converter processes an entire issue in memory; benchmark before large batches.

All output is explicitly marked unreviewed. No accessibility-conformance claim is made. The repository contains software and documentation only; private sources, credentials, and Drive IDs must not be committed.

## Product direction

See [the experience plan](docs/EXPERIENCE.md) and [delivery roadmap](docs/ROADMAP.md). First prove one excellent issue, then scale through a resumable, reviewed pipeline. Worldwide book distribution requires a documented permission or public-domain determination for each edition; age or a shared Drive link does not establish redistribution rights. This project has not determined those rights.

## References

- [W3C EPUB 3.3](https://www.w3.org/TR/epub-33/): package, navigation, page lists.
- [W3C EPUB accessibility guidance for fixed layout](https://www.w3.org/TR/epub-fxl-a11y/): why scan preservation alone is insufficient.
- [Tesseract language data](https://github.com/tesseract-ocr/tessdoc/blob/main/Data-Files.md): Telugu language model availability.

These references inform the design; the prototype has not been certified against them.
