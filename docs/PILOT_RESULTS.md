# Initial structured-document feasibility result

Run on this Mac on 2026-11-13 with `pypandoc_binary==1.17` bundling **Pandoc 3.9**.

A synthetic DOCX contained two heading-1 chapters, Telugu Unicode text, English text, and an embedded PNG illustration. The local adapter converted it into a 5,913-byte draft EPUB 3. Assertions confirmed both chapter names, the Telugu passage, and one embedded illustration. EPUB container order/MIME content and XML parsing checks passed. Pandoc emitted no warnings.

This establishes a working structured DOCX -> EPUB path without converting Word pages into images first. It does not establish general DOCX fidelity: footnotes, tables, equations, floating drawings, comments, tracked edits, and malformed input need broader fixtures. It also says nothing about difficult scanned PDF accuracy.

EPUBCheck was **not run** because a Java runtime is not installed on this machine. Physical Android testing and editorial review were **not run**. The adapter's output report explicitly records all three as pending; the output is a draft, not a release-ready book. No AWS resources were deployed for this check.

The original two `revive.py` packaging tests also pass. Keep the larger benchmark and device acceptance work in [BENCHMARK_PLAN.md](BENCHMARK_PLAN.md) as the gate for selecting production defaults.
