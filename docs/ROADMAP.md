# Delivery roadmap

## 1. Inventory and preservation

- Copy the source collection into owned Drive storage, preserving year folders.
- Keep a private mapping of source and destination IDs, sizes, checksums when available, and copy failures.
- Distinguish story issues from auxiliary newsletters; deduplicate by content hash without deleting originals.
- Download via authenticated Drive access, never commit access tokens or source material.

Done when every discovered PDF is verified in the destination and all exclusions are explicit.

## 2. One excellent issue

- Pick representative pages: cover, multi-column prose, illustration, damaged scan, and contents.
- Compare embedded text versus Tesseract Telugu OCR against native-speaker transcription.
- Add segmentation into columns, paragraphs, captions, illustrations, and story boundaries.
- Keep raw OCR, bounding boxes, confidence, reviewed text, and edits as distinct artifacts.
- Build source-page and story navigation, editorial image descriptions, licensed fonts, and metadata.
- Run EPUBCheck and test on Apple Books, a mobile EPUB reader, and an e-ink device; record actual versions and results.

Done when a reviewer signs off on fidelity and reading order and unresolved errors remain visible. The current prototype does not satisfy this milestone yet.

## 3. Reliable batch conversion

- Persistent job ledger keyed by input hash + pipeline version + configuration.
- Resume after interruption; atomic outputs; retry only failed stages; bounded memory and worker count.
- Per-page coverage checks; OCR review queues; provenance and correction history.
- Benchmark runtime/storage before processing the whole collection.

## 4. Reader and restoration workbench

- Offline-first web reader with bookmarks, local progress, comfortable Telugu typography.
- Side-by-side scan and text review with exact coordinate anchors.
- Curated story catalog, series continuity, glossary, and accessibility testing.

## 5. Public library

- Document rights clearance per edition and asset, approved territories, attribution, and license.
- Release only reviewed, validated, cleared editions; archive versioned provenance.
- Add opt-in narration and reviewed translations as separate derivatives.
- Maintain corrections and takedown contact procedures.

## Recommended architecture

Private Drive originals -> authenticated local ingest -> checksummed immutable masters -> page render/layout analysis -> OCR blocks -> human review -> canonical story JSON -> EPUB/web reader -> validation -> rights-cleared release.

Canonical story JSON should include stable IDs, language, issue/date, source hash, page indices and bounding boxes, ordered blocks, illustrations, raw OCR, reviewed text, reviewer history, rights evidence, and derivative links. A page-based prototype is only the first adapter into that model.
