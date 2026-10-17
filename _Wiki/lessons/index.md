---
title: Lessons register
status: active
updated: 2026-10-17
---

# Lessons register

The following repository/test workflow issues have verified local evidence; client runtime repairs are separately marked unrun in the integration review:

- [Git commit requires an explicit author identity](git-author-identity.md): missing name/email prevented committing; command-local verified identity resolved author metadata without changing global settings.
- [Backend emulator test isolation](backend-emulator-test-isolation.md): missing host variables now fail before a database client starts; observed negative probe and correct exec setup.
- [Firestore profile contention](firestore-profile-contention.md): commit retry exhaustion reproduced and repaired with one bounded jittered round; regression and real concurrency checks pass.

When a reproducible issue is solved, use the [lesson template](../templates/lesson.md). Record the symptom/error signature, affected component/version, cause and supporting evidence, solution, actual verification, and limits. Link the relevant topic page, source file or commit, and [log](../log.md) entry.

If the cause remains uncertain, say so. A workaround is not a verified root-cause fix. During later debugging, consult this register and search the wiki after the first plausible explanation or fix fails, as required by [maintenance](../maintenance.md).
