---
title: Frontend main and backend dev integration source record
status: active
updated: 2026-10-17
---

# Frontend main and backend dev integration source record

- Source ID: SRC-005.
- Origin: fetched repository commits, source/configuration inspection, and the initiator's merge/publication request in this conversation.
- Source/access date: 2026-10-17.
- Record type: English repository observation and normalized summary of human authorization, not a copy of another agent's undocumented conversation.
- Human request: download dev, verify its full contents, merge it to main and update the wiki; subsequent message explicitly authorizes commit and push.
- Main frontend commit: 6d9baea8e66ca2eb4f49e8c6b22d2bfa30d2a185.
- Dev backend commit: 18c0d1946136db94a30983eb91e5f377b3a07678.
- Merge base: ec8a3b5b4ac0480113d97c2f993e514014c1bf2c. Local main previously contained shared wiki commit 3994609.

## Initial integration observations

Main had advanced with the frontend while local wiki/API trackers were still uncommitted. Those local files were backed up in stash 9046be8c1d830584d8a3fe4028cd5e5689011cb8, excluding personal Obsidian state. Fast-forward to main plus non-fast-forward dev integration produced no textual conflicts; the local wiki was restored for reconciliation.

Frontend source contains auth/profile gates, category onboarding, gallery scan upload, read-only detail/settings and synthetic in-memory mocks. [docs/frontend-handoff.md](../../docs/frontend-handoff.md) adds English UI and gallery-only decisions to the handoff.

Backend source contains scaffold and auth/profile slices only: health, Firebase dependency, transactional user repository, tests, emulator rules/config, CI and Dockerfile. [Backend data/architecture/questions](../../backend/specs/open-questions.md) describe future choices as internally adopted proposals; independent evidence of their claimed previous human approval is not provided here. Future endpoint task documents are plans, not implemented services.

The first local full emulator suite observed 11 passes and one concurrent-profile failure; runtime diagnosis/final results belong in [integration review](../development/integration-review.md). No live provider/deployment or Flutter build was evaluated by this source record.

## Integration

See [ADR-0006](../decisions/adr-0006-integrated-client-and-backend.md), [architecture](../engineering/architecture.md), [current state](../current-state.md), [source register](../sources/index.md), and [activity log](../log.md). Preserve prior raw sources; this record updates source observations without rewriting them.
