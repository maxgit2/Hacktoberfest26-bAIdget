---
title: ADR-0004 Updated product and stack baseline
status: superseded
updated: 2026-10-17
---

# ADR-0004: Updated product and stack baseline

- Decision status: **superseded as the current integration baseline by [ADR-0005](adr-0005-api-handoff-baseline.md)**. Previously accepted at requirements/direction level; historical adoption below is preserved. Earlier future milestones remain deferred scope, not implemented behavior.
- Date: 2026-10-17.
- Authority: project initiator supplied the updated specification and explicitly requested wiki reconciliation; [SRC-003](../raw/2026-10-17-updated-specification.md) records it in English. No separate teammate approval is asserted.
- Replaces: [ADR-0002](adr-0002-initial-stack.md) as the current direction. [ADR-0003](adr-0003-flutter-scaffold.md) remains evidence of the existing scaffold.

## Changes from the initial brief

Use automatic smartphone-based identity (stable ID/fingerprint) in place of Google sign-in. Backend proof/session, ID generation/storage, reinstall/device recovery, and what fingerprint means technically remain open. A device ID alone is not a verified backend credential; ownership must not trust a client-supplied field.

Use gallery image selection for receipt extraction and a shared form for OCR review/manual entry. Additional camera capture remains open because the milestone list separately names scanning and gallery import. Category editing timing remains open: setup narrative permits edits while milestone 2.0 lists them.

Adopt the supplied [expense field list](../engineering/domain-model.md) as the documentation baseline, including optional `amount: float`, default euro, timestamps, and literal `concurrent` with unspecified `info`. This is not an executable API/database schema. Earlier exact-money advice remains an engineering concern requiring agreement, not permission to rewrite the supplied type.

Record the [0.1–5.0 milestones](../product/scope.md) as intended scope/sequence: infrastructure; core auth/input; server deployment/categories/summaries; email; budgets/alerts; chart variants. Weekly summaries and previous-period comparisons extend the initial direction. No completion, deadline, or commitment that all stages fit the hackathon is inferred.

The stack direction is Android + Flutter + FastAPI + Firebase. Firebase services, backend layout/runtime, and workers are undefined; workers remain tentative. DeepSeek-OCR is the named OCR direction, with exact model/deployment/contract/evaluation open. AgentMail remains an evaluation candidate for 3.0.

## Rationale and consequences

The authority is the updated human specification; no framework/provider comparison was supplied. Preserve [SRC-001](../raw/2026-10-17-project-brief.md) and the superseded ADR for history. Old Google/camera assumptions must not remain active requirements.

No application code, dependency, provider account, or deployment was changed. At ingestion the app remains the counter scaffold. Resolve the [questions](../open-questions.md) before independently implementing shared contracts, particularly identity, optional amounts, recurrence, timestamps, categories, and summary accounting.
