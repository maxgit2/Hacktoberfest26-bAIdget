---
title: Wiki index
status: active
updated: 2026-10-17
---

# bAIdget shared knowledge

This is the entry point for developers, designers, Codex, and Claude. It captures the team's current understanding while the product evolves during the hackathon. Read [current state](current-state.md) first; consult topic pages before choosing interfaces or technologies.

## Orientation and coordination

- [Current state](current-state.md): updated specification versus existing Flutter scaffold, verification limits, and next steps.
- [Maintenance workflow](maintenance.md): schema, evidence, ingest/query/lint, and update rules.
- [Activity log](log.md): append-only chronology of work and verification.
- [Open questions](open-questions.md): unresolved choices, impact, and resolution links.
- [Contributing and setup](development/contributing.md): team workflow and actual command registry.

## Product and engineering

- [Product scope](product/scope.md): current requirements, milestones 0.1–5.0, optional features, and acceptance scenarios.
- [User flows](product/user-flows.md): device identity, categories, gallery/OCR and manual shared form, email, comparisons, budgets/alerts.
- [Architecture and technology registry](engineering/architecture.md): observed counter execution flow, dependency/build-tool versions, and proposed product boundaries.
- [Domain model](engineering/domain-model.md): supplied expense fields, optional float amount, timestamps, recurrence/deletion, and unresolved encoding.
- [Integration contracts](engineering/contracts.md): client/backend handoff checklist and AI extraction boundary.
- [AI, data, and trust boundaries](engineering/ai-and-data.md): receipt/email processing, validation, privacy, and verification scenarios.

## Decisions and lessons

- [Decision register](decisions/index.md): accepted, proposed, rejected, and superseded choices.
- [ADR-0001: Shared project wiki](decisions/adr-0001-shared-project-wiki.md): accepted knowledge workflow and English convention.
- [ADR-0002: Initial application stack](decisions/adr-0002-initial-stack.md): superseded initial proposal, preserved for history.
- [ADR-0003: Flutter client scaffold](decisions/adr-0003-flutter-scaffold.md): observed implementation choice, root package, generated platforms, and limits.
- [ADR-0004: Updated product and stack baseline](decisions/adr-0004-updated-product-baseline.md): updated human requirements, supersession, and open contracts.
- [Lessons register](lessons/index.md): reproducible problems and verified fixes; no application fixes yet.
- [Git author identity](lessons/git-author-identity.md): observed commit failure and verified command-local author setup.

## Sources

- [Source register and methodology](sources/index.md): provenance and the adaptation of the reference discussion.
- [Initial project brief](raw/2026-10-17-project-brief.md): English source note from the project initiator's initial message.
- [Updated specification](raw/2026-10-17-updated-specification.md): SRC-003 English translation/transcription, fields, flows, milestones, stack, and unresolved wording.
- [Karpathy reference record](raw/2026-10-17-karpathy-reference.md): external URL, retrieval scope, and limitations.

## Reusable templates and tooling

- [Topic template](templates/topic.md): a focused page with evidence and open questions.
- [Decision template](templates/decision.md): a compact architecture or product decision record.
- [Lesson template](templates/lesson.md): symptom, diagnosis, fix, and observed verification.
- [Source template](templates/source.md): an immutable English source note with provenance.
- [Wiki checker](tools/check_wiki.py): dependency-free local link, index coverage, and metadata check.

Repository entry points: [README](../README.md), [AGENTS.md](../AGENTS.md), and [CLAUDE.md](../CLAUDE.md).
