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
| ADR-0004 | [Updated product and stack baseline](adr-0004-updated-product-baseline.md) | Accepted as supplied requirements/direction; implementation contracts open | Project initiator's updated specification SRC-003: device identity, gallery/shared form, expense fields, milestones, stack |

DeepSeek-OCR is named without an exact variant/host; AgentMail is only to evaluate. No finalized auth, API/persistence schema, Firebase service, worker, or deployment target is established. See [open questions](../open-questions.md).
