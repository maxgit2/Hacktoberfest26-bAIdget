# 06 — Scan
**Depends on:** 02, 03 | **Executor:** Antigravity | **Parallel with:** 04, 05

## Endpoint
`POST /v1/expenses/scan` (multipart: `image`, optional `id`)

## Files
`app/imaging/image.py`, `app/llm/{schema,prompt,gemini}.py`, `app/services/scan.py`, `app/repositories/rate_limit.py`, `app/routers/scan.py`, `tests/test_scan.py`, `tests/test_imaging.py`, `tests/eval/` (≥ 10 anonymized sample cases + expected JSON; offline eval script, **not** run in CI).

## Acceptance
- Check the size limit while reading the stream (> `MAX_IMAGE_BYTES` → `413 image_too_large`). Validate the real type with Pillow (`jpeg/png/webp`, else `415 unsupported_image_type`). Strip EXIF, resize so the long side ≤ 2048, re-encode JPEG in memory. Pillow runs in the threadpool. The image is never written to disk or logged.
- Rate limit before calling the LLM: Firestore transaction, `SCAN_RATE_LIMIT_PER_HOUR` → `429 rate_limited` with a `Retry-After` header.
- Same `id` already exists → return 200 **before** rate limiting or the LLM call (cheap retry).
- Gemini via `google-genai` structured output (check the official docs for `response_schema`/`response_json_schema` and the current model id; model comes from `GEMINI_MODEL`). The prompt lists the user's category ids and names, and says the image text is data, not instructions.
- The output is validated with pydantic. Amounts are strings → comma-normalized → Decimal. A category id not among the user's categories → `Other`.
- Neither merchant nor total readable → `422 extraction_failed`, nothing created. Provider error → `503 extraction_unavailable`. Timeout (config, ~30 s) → `504 extraction_timeout`.
- `needs_review=true` when the amount is missing, the date is missing or unreliable (Q-9), or the sum of item totals ≠ total (tolerance 0.01 × number of items).
- Saved through the expenses repo `create_idempotent` with `source=scan` and `scan_details`.

## Tests (Gemini always mocked)
happy receipt; payment screenshot without items; comma amounts ("1.234,56"); hallucinated category id → Other; prompt-injection text in the output fields is stored as plain text only; items mismatch → needs_review; extraction_failed creates nothing; 413, 415 (png renamed .jpg passes, a txt file fails), 503, 504; 31st scan in an hour → 429 + Retry-After; repeat id → 200 and the LLM is not called; EXIF removed (test image with GPS); user B's scan cannot pick A's category.
