---
title: Open questions
status: active
updated: 2026-10-17
---

# Open questions

Current authority: [SRC-003](raw/2026-10-17-updated-specification.md), [ADR-0004](decisions/adr-0004-updated-product-baseline.md). IDs are retained as answers evolve; “partially answered” is not a finalized integration contract. Owners remain **unassigned**; coordination roles are suggestions. Priority is proposed: **P0** blocks affected integration, **P1** must be resolved before that feature.

| ID | Priority | Current answer and remaining question | Suggested coordination |
| --- | --- | --- | --- |
| Q-01 | P0 | Updated source supplies milestone scope 0.1–5.0, replacing the wiki's suggested sequence. Which stages fit the one-day demo, with which owners and acceptance criteria? No deadline/completion inferred. | Whole team |
| Q-02 | P0 | Direction answered: Android/Flutter/FastAPI/Firebase (ADR-0004); only Flutter scaffold exists. Which Firebase services, database access boundary, backend location/runtime, and server/deployment target? Workers remain tentative. | Frontend + backend |
| Q-03 | P0 | Google sign-in is superseded by automatic smartphone ID/fingerprint. What does fingerprint mean, how is ID generated/stored, how does backend authenticate/prove possession, and what are reinstall/reset/device-change recovery rules? An ID string alone must not authorize access. | Frontend + backend |
| Q-04 | P0 | Expense has one required text `category`, but is it a stable ID or label? Whole purchase versus item/category allocation is not settled. Does optional category granularity require hierarchy? | Product/design + frontend + backend |
| Q-05 | P0 | DeepSeek-OCR is named. Which variant/version/host/hardware, OCR/classification stages, output schema, image limits, upload/timing/errors, and synthetic-sample acceptance criteria? | AI/backend + frontend |
| Q-06 | P1 before 3.0; P0 if email demonstrated | Email import is 3.0; AgentMail remains to evaluate. Address generation is described at user creation: provision in 1.0 or defer to 3.0? Which mailbox/provider/mapping, polling, deduplication, attachments, review, retries? | Backend + product/design |
| Q-07 | P0 for manual contract | Manual and post-OCR review share a form. Source required fields are recorded in the model. How does home reach manual input, which incomplete values can be saved, and how are `single`/`concurrent {info}` encoded? Requiredness/default of `type`, recurrence fields/occurrences/scheduling remain undefined. | Design + frontend + backend |
| Q-08 | P0 | Source says optional float `amount` and text `currency` default euro. What are precision/rounding, null/save/summary behavior, refunds/range, currency code, and unsupported-currency policy? Reconcile prior exact-money advice explicitly. | Frontend + backend |
| Q-09 | P0 for summaries | Source specifies timestamp `date`, `created_at` default now, optional `deleted_at`. Which wire format, timezone/clock authority, week start, period boundaries, and partial-period comparison rules? | Frontend + backend |
| Q-10 | P0 for 1.0 categories | What are template labels, empty-set rules, and category rename/delete semantics? Narrative permits onboarding edits but 2.0 lists editing after template: are initial customization and later edits distinct milestones? | Product/design + backend |
| Q-11 | P1 | Are images/emails retained, where/for how long, with which access/deletion rules? What goes to OCR/LLM? Device identity data handling also needs definition. | Backend + team |
| Q-12 | P1 | Root Flutter layout, Dart constraint/pub lockfile, `setState`, widget test/lints are known. Which exact SDK and verified Android toolchain, backend runtime/dependencies, product state/router/network libraries, CI, and workers? | Frontend + backend |
| Q-13 | P1 | What is the app's initial display language/locale? English docs and generated demo strings do not settle localization. | Design + frontend |
| Q-14 | P1 | Which Android demo device/emulator/API level and fallback? SDK levels currently delegate to Flutter; example application ID/debug release signing require review before identity/provider integration. | Frontend + demo coordinator |
| Q-15 | P0 for receipt UI | Detailed scanning starts with gallery selection, while 1.0 separately lists scanning and gallery import. Is direct camera capture also required in 1.0? Which picker/media/access behavior? | Design + frontend |
| Q-16 | P1 | Source marks “for one person (???)” and lists family groups as optional. Confirm personal-only ownership scope; shared/family roles are undefined. | Product + backend |
| Q-17 | P1 before 2.0 | Which default charts/comparisons ship in 2.0, versus selectable chart types in 5.0? Category pie chart/bar chart examples and optional granularity are recorded; chart defaults/hierarchy and comparison presentation are undefined. | Design + frontend + backend |
| Q-18 | P1 before 4.0 | Budget creation and alerts at 25/50/75/100% are specified; per-category alerts optional. What budget fields/period/currency, configurable thresholds, crossing/reset/deduplication, delivery channel, and edit/delete/recurrence effects? | Product + frontend + backend |
| Q-19 | P0 before expense mutations | No expense ID is supplied. How are records identified and `deleted_at` applied? Define soft-delete visibility, restore/purge, summaries/budget effects, and who assigns creation/deletion timestamps. | Frontend + backend |

## Resolution workflow

Keep answers in [scope](product/scope.md), [architecture](engineering/architecture.md), [model](engineering/domain-model.md), or [contracts](engineering/contracts.md), with source/authority/date and decision links. Preserve question IDs and history through source/decision records; append resolutions to [log](log.md). Open details do not block documentation intake, but shared runtime contracts need agreement before incompatible implementations.
