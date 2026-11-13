# Structured Word conversion pilot

Install `pip install -r experiments/requirements.txt` inside the project virtual environment. This package bundles Pandoc; inspect its engine license and notices before packaging a service image.

```sh
.venv/bin/python experiments/docx_to_epub.py input.docx build/book.epub --language te
```

The adapter preserves Pandoc's structured DOCX path, creates an EPUB 3 with a TOC, checks container/XML syntax, and emits a report that explicitly says EPUBCheck, Android and editorial review were not run. It uses a subprocess timeout and Pandoc's sandbox; those are not a complete public-upload isolation design. It has not implemented the proposed quality-review UI or PDF/DOC routes.

For EPUBCheck, use the pinned current upstream release and retain its report. For DOC use a separate LibreOffice normalization stage. For PDF use the layout/OCR benchmark in `docs/BENCHMARK_PLAN.md`.
