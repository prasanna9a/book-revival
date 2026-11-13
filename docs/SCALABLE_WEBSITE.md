# Website-first scaling requirements

Book Revival is a responsive website for Android and desktop browsers. Users upload PDF, DOCX or DOC, choose reading options, preview the conversion, and download an EPUB. Native mobile apps are optional future clients of the same API.

## Starting architecture

Use the resource design in AWS_ARCHITECTURE.md: CDN-served frontend, stateless authenticated API, direct private object-storage uploads, durable job state, and queued disposable conversion workers. Files do not pass through a long-running web request. The user can close the page and return to their job.

## Growth without a rewrite

- Scale the frontend, API, and conversion workers independently.
- Keep durable state and files outside application processes.
- Version the job API and conversion pipeline; record tool/model versions per result.
- Split fast structured-document jobs from expensive scan/OCR jobs so large books do not block all users.
- Use queue depth and oldest-job age to guide worker capacity, with explicit concurrency and cost limits.
- Apply per-user quotas and fair scheduling; preserve idempotency under retries.
- Isolate failed jobs, bound retries, and support cancellation, deletion, and recovery.
- Measure upload success, conversion success by input type/language, queue wait, processing time per page, download success, and cost per completed book.
- Cache static website assets globally. Keep private user books out of public caches.
- Start in one AWS region. Add other regions only when measured latency, residency requirements, or recovery goals justify the added complexity.

## Phased delivery

1. Private pilot: responsive upload/status/download flow, one region, capped CPU workers, representative documents and physical Android tests.
2. Public beta: user accounts, quotas, abuse controls, load testing, job fairness, operational dashboards and a tested recovery procedure.
3. Growth: independently tuned worker pools, optional GPU tier, resumable uploads for larger files, richer review tools and optional subscription/account plans.
4. Further expansion: additional regions, organization accounts and native mobile clients when demand warrants them.

No numerical throughput or availability promise is established yet. Benchmark realistic book sizes and OCR workloads, then set measurable service objectives and run a load test before publishing capacity claims. Autoscaling must remain bounded by the chosen operating budget.

This is a design requirement, not an assertion that the website or autoscaling infrastructure is deployed.
