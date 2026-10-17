---
name: firestore-patterns
description: bAIdget Firestore rules — explicit deleted_at null, composite indexes, AsyncClient transactions, idempotent create, cursor pagination. Use when specifying or reviewing repository code.
---
- Create: always write `deleted_at: None` (categories also `archived_at: None`). Queries: `.where(filter=FieldFilter("deleted_at", "==", None))` — missing field ≠ null, so explicit write is mandatory.
- Every new query shape → entry in `firestore.indexes.json` (`deleted_at` equality first, then other equalities, then `date DESC`). Emulator does not enforce indexes: review manually.
- Transactions (`@firestore.async_transactional`): reads before writes; used for get-or-create, idempotent create (`get` → exists? return 200 : `create`), name uniqueness, rate-limit counter, one recurring rule per transaction. Verify signatures in official docs before relying on them.
- Idempotent ids: client UUID for expenses, `uuid5(NS, f"{rule_id}:{n}")` for occurrences; soft-deleted doc still exists → never recreated.
- Pagination: `order_by(date DESC).order_by(__name__ DESC).start_after(snapshot-like dict)`; cursor = urlsafe base64 JSON `{date, id}`; validate on decode.
- Money in `amount_cents: int`.
