---
title: Wiki index
status: active
updated: 2026-10-17
---

# bAIdget shared knowledge

This is the entry point for developers, designers, Codex, and Claude. It captures the team's current understanding while the product evolves during the hackathon. Read [current state](current-state.md) first; consult topic pages before choosing interfaces or technologies.

## Orientation and coordination

- [Repository reconciliation audit](development/repository-audit.md): complete file inventory, inspection progress, checks and remaining audit work at main `b6d984e`.
- [Current state](current-state.md): full backend MVP source, partial Flutter client, service availability and verification limits.
- [Maintenance workflow](maintenance.md): schema, evidence, ingest/query/lint, and update rules.
- [Activity log](log.md): append-only chronology of work and verification.
- [Open questions](open-questions.md): unresolved choices, impact, and resolution links.
- [Contributing and setup](development/contributing.md): team workflow and actual command registry.
- [Integration review and verification](development/integration-review.md): historical integration and current main audit findings, actual checks and limits.
- [Frontend activity/milestone tracker](development/frontend-tracker.md): Flutter tasks, owners, status, dependencies and completion gates.
- [Backend activity/milestone tracker](development/backend-tracker.md): declared API delivery versus verified implementation; artifacts and remaining work.
- [Infrastructure activity/milestone tracker](development/infrastructure-tracker.md): tooling, Firebase/access, hosting/extraction and operational checks.

## Product and engineering

- [Product scope](product/scope.md): latest handoff scope, workstream milestones, deferred earlier roadmap and acceptance gates.
- [User flows](product/user-flows.md): Firebase Google login, categories, saved-scan review, manual input, recurring rules and summaries.
- [Architecture and technology registry](engineering/architecture.md): observed client/backend flows, dependency/build-tool versions, and remaining product boundaries.
- [Infrastructure, deployment and secrets](engineering/infrastructure.md): Cloud Run delivery, IAM/WIF, configuration, indexes, credential boundaries and operational evidence.
- [Domain model](engineering/domain-model.md): expense/category/rule fields, server ownership, EUR/nulls, timestamps and persisted review.
- [Integration contracts](engineering/contracts.md): all 21 source operations, Firebase auth, retries/errors, committed OpenAPI and contract drift.
- [AI, data, and trust boundaries](engineering/ai-and-data.md): receipt/email processing, validation, privacy, and verification scenarios.

## Decisions and lessons

- [Decision register](decisions/index.md): accepted, proposed, rejected, and superseded choices.
- [ADR-0001: Shared project wiki](decisions/adr-0001-shared-project-wiki.md): accepted knowledge workflow and English convention.
- [ADR-0002: Initial application stack](decisions/adr-0002-initial-stack.md): superseded initial proposal, preserved for history.
- [ADR-0003: Flutter client scaffold](decisions/adr-0003-flutter-scaffold.md): observed implementation choice, root package, generated platforms, and limits.
- [ADR-0004: Updated product and stack baseline](decisions/adr-0004-updated-product-baseline.md): superseded SRC-003 adoption, retained for history/future scope.
- [ADR-0005: API handoff integration baseline](decisions/adr-0005-api-handoff-baseline.md): current supplied contract, changed boundaries and maintained workstream tracking.
- [ADR-0006: Integrated client/backend](decisions/adr-0006-integrated-client-and-backend.md): historical initial integration choices; extended by ADR-0007.
- [ADR-0007: Merged backend MVP baseline](decisions/adr-0007-merged-backend-baseline.md): observed domain implementation and deployment choices, with explicit acceptance and runtime limits.
- [Lessons register](lessons/index.md): reproducible problems, verified fixes and their limits.
- [Git author identity](lessons/git-author-identity.md): observed commit failure and verified command-local author setup.
- [Backend emulator test isolation](lessons/backend-emulator-test-isolation.md): verified fail-fast guard and correct local emulator setup.
- [Firestore profile contention](lessons/firestore-profile-contention.md): verified bounded retry after SDK commit exhaustion and remaining deadline limits.

## Sources

- [Source register and methodology](sources/index.md): provenance and the adaptation of the reference discussion.
- [Initial project brief](raw/2026-10-17-project-brief.md): English source note from the project initiator's initial message.
- [Updated specification](raw/2026-10-17-updated-specification.md): SRC-003 English translation/transcription, fields, flows, milestones, stack, and unresolved wording.
- [Frontend API handoff source record](raw/2026-10-17-frontend-handoff.md): SRC-004 complete supplied document, provenance, digest and runtime-evidence limits.
- [Frontend/main and backend/dev integration source](raw/2026-10-17-integration-source-record.md): SRC-005 pinned commits, human request and initial observations.
- [Post-merge reconciliation source](raw/2026-10-17-post-merge-audit.md): SRC-006 current human request, pinned source and audit evidence boundaries.
- [Karpathy reference record](raw/2026-10-17-karpathy-reference.md): external URL, retrieval scope, and limitations.

## Reusable templates and tooling

- [Topic template](templates/topic.md): a focused page with evidence and open questions.
- [Decision template](templates/decision.md): a compact architecture or product decision record.
- [Lesson template](templates/lesson.md): symptom, diagnosis, fix, and observed verification.
- [Source template](templates/source.md): an immutable English source note with provenance.
- [Wiki checker](tools/check_wiki.py): dependency-free local link, index coverage, and metadata check.

Repository entry points: [README](../README.md), [AGENTS.md](../AGENTS.md), and [CLAUDE.md](../CLAUDE.md).
