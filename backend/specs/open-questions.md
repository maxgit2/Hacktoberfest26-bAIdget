# Open questions & decisions to approve

Status: **ADOPTED AS PROPOSED** (2026-10-17, user said "go on" without answering; user may override). Executors still do not resolve new ones.

## Missing input
- **Q-0** `specs/01-stack.md` was not provided. `02-data-model.md` was derived from the handoff, and decisions [D-n] are below. Please send 01-stack.md if it exists, or approve the D-list.

## Contract gaps / ambiguities (handoff)
- **Q-1** Delete category: the handoff says "blocked if used (409)". The brief says "block (409) or archive", and summaries "include archived categories that still have expenses". If delete is blocked whenever the category is used, an archived category can never have expenses. Proposal: delete is blocked while used and archives otherwise (soft). The summary clause then only applies to expenses that were soft-deleted later. Confirm.
- **Q-2** Idempotent `POST /expenses` with an `id` that exists but is **soft-deleted**: return 200 with the deleted doc? Proposal: return `404 not_found`. A retry of a deleted item should not resurrect it, and `deleted_at` is never non-null in responses.
- **Q-3** `POST /expenses` with an `id` that exists but a **different body**: proposal = return the existing expense with 200 and ignore the new body (pure retry semantics).
- **Q-4** `make-recurring` response is `201`. The expense keeps its id and becomes occurrence 0 (`type` → recurring). Confirm the source expense is mutated rather than copied.
- **Q-5** Recurring occurrences: is `needs_review` false, and is `source` "manual"? Proposal: yes, both.
- **Q-6** `PATCH /expenses` on a recurring occurrence with `amount: null`: allowed? Proposal: yes.
- **Q-7** Max 30 counts active categories including `Other`? Onboarding with 30 picks + Other = 31 → reject with `max_categories`? Proposal: limit applies to the total including Other.
- **Q-8** `GET /expenses` filter `category` = archived category id: return its expenses (yes, proposal).
- **Q-9** Scan `needs_review` when the date is missing: which date is used? Proposal: server "now", with `needs_review=true`.
- **Q-10** Error code for `make-recurring` on a soft-deleted expense: `404`.
- **Q-11** `PATCH /recurring-rules` `category` pointing to an archived category → `422 category_not_found` (proposal).

## Decisions taken by the orchestrator (need OK)
- **D-0 Tooling:** **conda** (`environment.yml`, env `baidget`) replaces `uv` from the brief, as the user asked. `pyproject.toml` stays for ruff/pytest config and package metadata.
- **D-1** Money stored as integer cents (`amount_cents`). API stays a number.
- **D-2** Ids: `cat_<8 chars>`, `rule_<8 chars>`.
- **D-3** Category name 1–40 chars, trimmed.
- **D-4** Uniqueness via `name_key = casefold(trimmed name)` among active categories.
- **D-5** The 30 limit counts active categories including Other.
- **D-6** Occurrence id = `uuid5(fixed namespace, "{rule_id}:{n}")`.
- **D-7** `recurrence.index` stored internally only.
- **D-8** Recurrence arithmetic in Europe/Rome local time, with the day clamped to the month length.
- **D-9** `resume_from` implements "no backfill on reactivation".
- **D-10** Sync caps: 50 occurrences per rule and 20 rules per call.
- **D-11** Scan rate limit: fixed hourly window in Firestore (works across Cloud Run instances).
- **D-12** Summaries read the documents and aggregate in Python. Acceptable at MVP volume. Upgrade to a monthly rollup document if it gets slow.
- **D-13** Antigravity instructions: `AGENTS.md` is canonical. It is symlinked as `.agents/rules/agents.md` and `GEMINI.md`, because Antigravity 2.0 documents `.agents/rules` and its AGENTS.md support is unconfirmed.
- **D-14** Gemini model name comes from env `GEMINI_MODEL`. The value is verified against the official docs in slice 06, not hard-coded from memory.
- **Q-12** Is `/health` at the root (not `/v1/health`)? Proposal: both `/health` and the `/v1` prefix for everything else, health at the root only.
- **Q-13** Does summary `count` include expenses with a null amount? Proposal: no; they are reported in `uncounted`.
