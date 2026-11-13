# Select defaults with evidence

The recommendation is architectural, not a claim that a particular OCR engine is best on this collection.

## Corpus

Use permissioned/private test files with known provenance. Include a structured DOCX with headings, lists, footnotes, tables and inline artwork; a legacy DOC; a simple digital PDF; a multi-column illustrated PDF; a mixed scan/text PDF; a rotated/degraded scan; Telugu conjuncts and old typography; a large file; malformed and encrypted inputs. Keep private books out of Git. Synthetic fixtures may be committed separately.

Choose at least 20 representative pages stratified across source quality and decades for native-speaker transcription. Expand the sample if a pipeline fails unevenly. A single clean English page cannot validate old Telugu magazines.

## Candidate runs

- Pandoc directly on DOCX; compare with LibreOffice EPUB output and Calibre.
- DOC normalized through isolated LibreOffice, then Pandoc.
- Docling PDF -> structured book representation -> EPUB.
- Tesseract/OCRmyPDF baseline and Docling+Tesseract configuration for scanned pages.
- Marker as an optional comparator only after the exact model terms are accepted for the intended use.
- Existing `revive.py` as a page-preserving baseline, not the expected final product.

## Measurements

Record tool/model versions, licenses, source hash, configuration, wall time, peak memory, page count, output size, word/character count, illustrations retained, ordered-block coverage, missing/corrupt glyphs and warnings. Use native-speaker ground truth for character error rate; separately score reading order, headings, captions and omissions. Compare output against the source rather than comparing OCR engines only to each other.

Run EPUBCheck on every EPUB, resolve errors, and retain the validation report. Check structure/navigation and source links. Conduct physical Android and desktop reading tests. An EPUBCheck pass cannot establish correct text or comfortable reading.

## Ship decision

Select defaults by input class. Do not force one engine on everything. Establish error/coverage thresholds from pilot results, publish known limitations, and route uncertain jobs to review. A zero-error validation report is required for a Ready download, but editorial uncertainty may still be shown. Never fabricate a single quality score that blends unrelated metrics.

The optional `experiments/docx_to_epub.py` is a local adapter feasibility check. It does not establish public-upload isolation or PDF restoration quality.
