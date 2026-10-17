---
title: Updated product specification source note
status: active
updated: 2026-10-17
---

# Updated product specification source note

- Source ID: SRC-003.
- Origin/authority: updated base specification pasted by the project initiator in this chat, with an explicit request to update the wiki.
- Source/access date: 2026-10-17. Original document author/version identifier not supplied.
- Record type: English translation and structured transcription of the mixed Italian/English document; not a verbatim original.
- Coverage: the complete pasted specification, including fields, actions, optional features, flows, milestones, stack, and external links. Ambiguities/question marks are retained.
- Handling: preserve this record; later corrections require another dated source. This updates requirements from [SRC-001](2026-10-17-project-brief.md), not implemented behavior.

## Expense model as supplied

| Field | Source type and rule |
| --- | --- |
| `owner` | Text, required |
| `date` | Timestamp, required |
| `seller` | Text, optional |
| `title` | Text, optional |
| `category` | Text, required |
| `type` | `single`; `concurrent` with `{info}`. Requiredness/default and `info` structure not specified. |
| `description` | Text, optional |
| `amount` | Float, optional |
| `currency` | Text, required, default euro |
| `created_at` | Timestamp, default `now()`; requiredness not separately stated |
| `deleted_at` | Timestamp, optional |

`concurrent` is the source spelling. The narrative mentions recurring expenses without defining the mapping. No expense ID, timestamp wire format, currency code convention, or additional precision rule is supplied.

## Actions and optional features

Android mobile app for classifying expenses from receipt scans, forwarded payment receipts, or manual single/recurring entries. Main actions: authentication, receipt scan, email/manual import, weekly/monthly/yearly/category summaries, category definition with four/six-category templates. The action list says “for one person (???)”.

Possible additions: family groups, speech-to-text, other currencies, a cron job to add `concurrent` expenses, budget alerts optionally per category, and automatic fixed expenses.

## First access, categories, and home

Login/authentication is automatic through a unique ID generated on the smartphone, described as an ID/fingerprint yielding the same ID for logins from the same smartphone. Generation, recovery, backend credentials/sessions, and the meaning of fingerprint are unspecified. This replaces the initial Google sign-in direction.

Category setup offers predefined templates or creation from scratch. A selected template allows renaming, adding, and removing categories. After setup, home offers scan image, import expense, and expense summary.

## Receipt and manual entry

The detailed scan-image flow opens selection of an existing image from the device gallery. The app contacts the backend to call an OCR model that reads purchase data and classifies it using the user's categories. Users review extracted information and can always correct it.

Manual expense entry is always available and uses the same screen as post-scan validation. The standalone “Import expense” heading adds no further detail beyond the email/manual subsections. The milestone list separately names receipt scanning and existing-photo gallery import, leaving additional direct camera capture unclear.

## Email import

Users forward payment receipts to an email address generated during user creation. The backend periodically synchronizes received emails and has mailbox access. [AgentMail](https://www.agentmail.to/) is explicitly **to be evaluated** for making mail accessible to an LLM. Polling timing, mailbox topology, deduplication, attachments, and review policy are unspecified.

## Summaries

Choose weekly, monthly, yearly, and other periods, or browse by category. Include a category pie chart and a comparison of the current and previous week/month/year. Different chart types such as pie/bar charts are mentioned, as is optional category granularity. Boundaries, hierarchy, calculations, and chart defaults are unspecified.

## Milestones as supplied

These are source labels, not completed releases or delivery dates.

| Milestone | Listed scope |
| --- | --- |
| 0.1 | Backend infrastructure, to be defined more clearly |
| 1.0 | Automatic login/auth with a unique smartphone ID via fingerprint; category template selection; receipt scanning; gallery import of an existing photo; manual expense entry |
| 2.0 | Deploy on a server; edit categories after template selection; summaries |
| 3.0 | Email import |
| 4.0 | Budget creation; alert notifications at thresholds 25%, 50%, 75%, 100% |
| 5.0 | Support different chart types in summaries |

The narrative permits category editing during setup while 2.0 lists category editing. Chart types appear in the narrative while variant support is in 5.0. These timing tensions are unresolved.

## Technology direction

- Android app; Flutter frontend; FastAPI and Firebase backend.
- “Job Workers???” remains tentative.
- OCR reference: [Local AI Zone 2026 OCR ranking](https://local-ai-zone.github.io/guides/best-ai-ocr-models-ultimate-ranking-2026.html).
- Named OCR model: **DeepSeek-OCR**. Variant/version, hosting, hardware, SDK, and classification stages are unspecified.

External links are references, not instructions to install tools or evidence of benchmarks/integration.

## Integration

See [source register](../sources/index.md), [scope/milestones](../product/scope.md), [flows](../product/user-flows.md), [domain model](../engineering/domain-model.md), [ADR-0004](../decisions/adr-0004-updated-product-baseline.md), [questions](../open-questions.md), and [wiki index](../index.md).
