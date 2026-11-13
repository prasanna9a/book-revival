# Open-source research and recommended foundation

Reviewed 2026-11-13. This is a source-based engineering recommendation, not a measured quality ranking. Repository defaults and model licenses can change; pin the selected revisions and retain their notices before shipping.

## Decision

Build Book Revival as an orchestration, quality-review, and reading-experience layer around existing engines. Use Pandoc for structured Word documents and EPUB packaging; evaluate Docling plus Tesseract for PDF layout and OCR. Validate every downloadable EPUB with EPUBCheck. Offer standard EPUB downloads first, then an optional mobile web reader built with foliate-js. Use Readest as an Android interoperability target and Readium if a native Android app becomes worthwhile.

The differentiator is faithful reconstruction, inspectable corrections, attractive typography, and an honest quality report. An upload form wrapped around a generic PDF converter will not reliably restore illustrated, multi-column Telugu books.

## Candidates

| Repository | Observed license / scope | Best role | Decision and limitation |
|---|---|---|---|
| [Docling](https://github.com/docling-project/docling) | MIT code; model licenses separate | PDF layout, reading order, tables, structured JSON/HTML | Preferred PDF candidate. Benchmark on our Telugu scans; do not assume model language coverage or accuracy. EPUB is listed as input, not a reason to assume a complete EPUB authoring pipeline. |
| [Pandoc](https://github.com/jgm/pandoc) | GPL-2.0-or-later | DOCX -> EPUB, semantic HTML -> EPUB | Preferred structured-document and packaging engine. PDF is not its general-purpose input parser. Retain headings, footnotes, lists, and media through the intermediate representation. |
| [LibreOffice](https://www.libreoffice.org/about-us/licenses/) | MPL/LGPL licensing described upstream; distribution includes other components | Legacy binary DOC -> DOCX normalization | Separate isolated compatibility worker. DOC and DOCX are different formats; Pandoc's DOCX support does not imply DOC support. |
| [Tesseract](https://github.com/tesseract-ocr/tesseract) | Apache-2.0 code; inspect selected language data | Local OCR with explicit language selection | CPU baseline, including Telugu `tel`. Keep word boxes and uncertainty; measure errors with native speakers. |
| [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) | MPL-2.0 code; dependency licenses separate | Searchable PDF derivative, rotation/deskew/OCR workflow | Useful scan preprocessing and optional searchable-PDF output. It does not create a finished reflowable EPUB. |
| [Calibre](https://github.com/kovidgoyal/calibre) | GPL-3.0 | Format compatibility, metadata, alternative conversion baseline | Keep as a fallback/baseline. Its PDF documentation identifies limitations with multi-column, image-based, and complex-language material. Do not make it our only restoration engine. |
| [Calibre-Web-Automated](https://github.com/crocodilestick/Calibre-Web-Automated) | GPL-3.0 license file | Fast self-hosted personal library and automated ingest/conversion | Best ready-made personal-library option among those reviewed. It inherits Calibre's conversion limitations and is a different starting point from a public, isolated per-user conversion service. |
| [EPUBCheck](https://github.com/w3c/epubcheck) | BSD-3-Clause | EPUB conformance validation | Required release gate. Conformance does not prove OCR accuracy or accessibility. |
| [foliate-js](https://github.com/johnfactotum/foliate-js) | MIT; vendored libraries have their own notices | In-browser EPUB rendering | Preferred modular web-reader candidate. Upstream warns its API is unstable; pin a commit and test upgrades. Its demo is not a complete product. |
| [Readest](https://github.com/readest/readest) | AGPL-3.0-or-later | Existing Android/iOS/desktop/web reader | Test our downloads here; useful UX reference. Forking the whole app is a larger commitment and brings its license obligations. |
| [Readium Kotlin Toolkit](https://github.com/readium/kotlin-toolkit) | BSD-3-Clause | Native Android EPUB reader | Preferred future Android-native foundation; defer native development until downloads and mobile web work well. |
| [epub.js](https://github.com/futurepress/epub.js) | BSD-2-Clause as shown upstream | Alternative browser EPUB renderer | Benchmark alongside foliate-js if browser compatibility or integration simplicity wins. |
| [Marker](https://github.com/datalab-to/marker) | Current README: Apache-2.0 code; modified OpenRAIL-M weights with usage/commercial conditions | Alternative layout/OCR benchmark | Evaluate separately. Model weights are not an unrestricted substitute for a fully open dependency stack. Do not infer licenses from older blog posts. |
| [PyMuPDF](https://github.com/pymupdf/PyMuPDF) | AGPL-3.0 or commercial license | Existing local `revive.py` prototype | Keep the prototype available, but make the product's licensing choice explicit before carrying this dependency into a hosted release. |

These are declared upstream licenses, not a completed dependency or model-license audit. Free/open-source engines still have hosting costs. No third-party source has been vendored into this repository by this research.

## Build versus reuse

- For a private family library quickly: evaluate Calibre-Web-Automated plus an OCR/restoration preprocessing stage.
- For a public upload -> reviewed enhanced EPUB service: build the small Book Revival product layer around the recommended engines. Keep library publishing separate from private conversion.
- For a branded Android reader: start with interoperable EPUB downloads; later use Readium rather than implementing EPUB rendering from scratch.

## Format-aware conversion

1. DOCX: preserve the Word document's structure and images; use Pandoc directly. Avoid rasterizing a structured Word file to PDF first.
2. DOC: normalize with a disposable LibreOffice process/profile; treat macros, embedded objects, and external links as untrusted and disable/remove them.
3. Born-digital PDF: reconstruct blocks, columns, headings, captions, links, and figures. Retain source coordinates and embedded text when it is sound.
4. Scanned/mixed PDF: rotate/deskew a derivative, OCR only where needed, merge with layout analysis, retain raw and reviewed text separately.
5. Canonical book model: ordered semantic blocks, source anchors, media, language, metadata, and review history. Do not use lossy Markdown as the only archival representation.
6. Export: standard EPUB with semantic XHTML, CSS, metadata, navigation, illustrations and reviewed alternatives; optional archival PDF and HTML reading package. Calibre can provide additional formats later.

## Why not promise perfect automatic conversion?

[Calibre's own PDF guidance](https://manual.calibre-ebook.com/conversion.html#pdfconversion) identifies difficult input classes. A parser can also return syntactically valid but incorrectly ordered text. Confidence scores and a successful exit code are insufficient. Compare actual output with source pages and tell the user where review is needed.

## Reference details

- [Docling formats](https://docling-project.github.io/docling/usage/supported_formats/) and [license/model note](https://github.com/docling-project/docling#license).
- [Pandoc manual](https://pandoc.org/MANUAL.html): EPUB settings, DOCX input, sandbox and untrusted-input guidance.
- [LibreOffice conversion filters](https://help.libreoffice.org/latest/en-US/text/shared/guide/convertfilters.html): legacy Word and DOCX formats.
- [Tesseract language data](https://github.com/tesseract-ocr/tessdoc/blob/main/Data-Files.md).
- [foliate-js status and API](https://github.com/johnfactotum/foliate-js#current-status).
- [Marker commercial/model terms](https://github.com/datalab-to/marker#commercial-usage).

No corpus benchmark or actual Android device test has been completed by this research. See [BENCHMARK_PLAN.md](BENCHMARK_PLAN.md) before choosing final defaults.
