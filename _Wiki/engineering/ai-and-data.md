---
title: AI data and trust boundaries
status: active
updated: 2026-10-17
---

# AI, data and trust boundaries

Source baseline `b6d984e`; [scan service](../../backend/app/services/scan.py), [Gemini client](../../backend/app/llm/gemini.py), [prompt](../../backend/app/llm/prompt.py), [image processing](../../backend/app/imaging/image.py), [auth](../../backend/app/core/auth.py). Full extraction code and mocked tests now exist; live model accuracy/retention and production isolation remain unverified.

## Identity and storage

Every domain route derives UID from Firebase token verification in a threadpool (`check_revoked=False`) and scopes repositories below users/{uid}. No model text/client owner can select another user. Deny-all Firestore rules protect direct clients if deployed, while backend Admin SDK relies on IAM plus application scoping. Two-user emulator test sources cover profile/category/expense/rules/summary and scan category allowlisting; they do not prove production rules or Google provider configuration. Email/display name are persisted on initial provisioning, not refreshed from each token.

Client defaults are fake authentication and synthetic memory data. They are independent of real backend URL selection: fake-token requests to a live API fail. SDK initialization/platform config, same-project tokens, provider enablement and Android signing remain integration gates.

## Extraction boundary and saved review

Only gallery image selection is exposed. Client resizes/re-encodes JPEG, keeps a UUID across retries and sends multipart with 45s receive timeout. Server reads up to 10,485,760 bytes, Pillow validates JPEG/PNG/WebP by content, rejects excessive/decompression-bomb images, applies EXIF orientation, strips metadata, flattens transparency and re-encodes quality 85/long side2048. CPU work is offloaded. No durable image object/store is written by app code; framework multipart UploadFile may spool temporary data, so a strict guarantee that bytes never touch disk is not established.

Firestore quota is consumed before provider success, default 30 per user/fixed UTC hour;429 has Retry-After. Existing live UUID retries bypass provider/quota after request parsing. Concurrent first uploads can still make multiple paid calls despite idempotent final persistence. Deleted-ID retry can call the provider before returning404. These are billing/retry limitations, not demonstrated data duplication.

Gemini uses async google-genai, environment key/model, JSON response_schema and timeout 30s. Missing key/provider API errors→503, timeout→504, invalid parsed output→422. Prompt includes only active category IDs/names plus image and says embedded instructions are data. Pydantic validates declared fields; extra fields are ignored following b6d984e's schema fix. Category allowlisting/fallback is enforced after extraction. There is no tool execution, arbitrary action dispatcher or email ingestion.

Amounts/quantities arrive as strings and are parsed separately; unreadable values become null/review. Missing/invalid date falls back to now; naive extracted date assumes TZ_NAME. If both seller and valid total are absent, no expense is created. Otherwise save immediately with source=scan, metadata and computed needs_review; no pre-save confirmation. Item mismatch tolerance is one cent per item. Human correction requires PATCH and explicit needs_review=false, which the backend supports but the current Flutter detail cannot send. Missing amount is excluded from totals, not treated as a zero purchase.

Known validation gaps: extracted currency is ignored and labeled EUR; quantities inherit two-decimal/positive money limits; zero VAT becomes null/review. Ordinary expense reads expose stored scan money keys, unlike scan response. Record these as limitations in [contracts](contracts.md)/[review](../development/integration-review.md#post-merge-audit-at-b6d984e), not accepted model behavior.

## Privacy, secrets and evidence

Provider credentials stay backend-side; Cloud Run Secret Manager injection and WIF avoid committed keys. Request middleware logs only method/status/request ID/timestamp; SDK logger behavior and cloud request logging/retention are not audited. Images and user category names are sent to Gemini; configured model alias does not establish provider processing region/retention. Expense scan_details stores extracted text, amounts, VAT/payment metadata. No purge/TTL/account deletion/export policy, sensitive-data filter or retention schedule is implemented. See [infrastructure](infrastructure.md).

Ten synthetic text/expected-JSON evaluation cases and an offline comparator exist under [tests/eval](../../backend/tests/eval/evaluate.py); **there are no image fixtures or captured model results in this set**. The script compares flattened expected fields, skips missing result files and has no minimum-accuracy exit threshold (returns 0 if any fields compared). It is not in CI. This is evaluation scaffolding, not measured OCR accuracy or a prompt-injection defense benchmark. The mocked injection test only shows extracted instruction-like strings are stored as data.

No real receipt, account/secret, authenticated business request or live Gemini call was used during this audit. Public service probes failed500/503; no claim of production extraction success. Older DeepSeek-OCR/AgentMail references remain historical, not current provider implementations.

## Verification still needed

Run full emulator suites and configured Android flows with synthetic input: cross-user operations, direct Firestore denial, same-ID concurrent/retry/deleted scans, image bounds/temporary cleanup, provider errors/quotas, non-EUR/weighted items, saved correction and later reads, summary null/delete/DST behavior, recurrence caps/overlap/resume. Validate retention/region/logging and live IAM separately. No formal security audit is claimed. [Trackers](../development/backend-tracker.md) and [questions](../open-questions.md) hold the remaining work; email/budgets/family/bulk/voice/other currencies/offline remain excluded.
