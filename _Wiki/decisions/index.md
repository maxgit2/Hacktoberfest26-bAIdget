---
title: Decision register
status: active
updated: 2026-10-17
---

# Decision register

This register tracks both product and technical decisions. Use the [decision template](../templates/decision.md) and [maintenance workflow](../maintenance.md). Accepted means an evidenced choice, not implemented behavior.

| ID | Decision | Decision status | Authority / evidence |
| --- | --- | --- | --- |
| ADR-0001 | [Shared project wiki and agent workflow](adr-0001-shared-project-wiki.md) | Accepted | Project initiator explicitly requested `_Wiki`, Codex/Claude instructions, continuous knowledge capture, and English documentation/comments |
| ADR-0002 | [Initial Flutter / FastAPI / Firebase direction](adr-0002-initial-stack.md) | Superseded by ADR-0004 | Initial proposal retained for history; updated source supplies current direction |
| ADR-0003 | [Flutter client scaffold at the repository root](adr-0003-flutter-scaffold.md) | Accepted scaffold implementation choice; no product features implied | Francesca De Luca's commit `055275e` on `origin/main`; root manifest, counter demo, test, and generated runners |
| ADR-0004 | [Updated product and stack baseline](adr-0004-updated-product-baseline.md) | Superseded by ADR-0005 for current integration | SRC-003 adoption retained as history/future roadmap |
| ADR-0005 | [API handoff integration baseline](adr-0005-api-handoff-baseline.md) | Accepted as supplied documentation/integration baseline; runtime unverified | Initiator supplied SRC-004 and requested reconciliation plus maintained frontend/backend/infrastructure trackers |
| ADR-0006 | [Integrated client/backend choices](adr-0006-integrated-client-and-backend.md) | Accepted for committed implementation choices; future backend proposals not independently approved | Main6d9baea frontend plus dev18c0d19 scaffold/auth; requested merge/review/publication |

Firebase Google Auth, backend-only Firestore, API ownership, EUR and persisted scan review are now declared in SRC-004. Referenced OpenAPI/source/config/addresses and runtime proof are absent; model/provider/deployment remain unverified. Earlier DeepSeek-OCR/AgentMail names do not establish current adoption. See [open questions](../open-questions.md).
