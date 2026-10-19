---
title: Infrastructure activity and milestone tracker
status: active
updated: 2026-10-19
owner: unassigned
---

# Infrastructure activity and milestone tracker

Freshness checked at `3b4cee3` on 2026-10-19. [SRC-007](../raw/2026-10-19-post-hackathon-update.md) records reported cloud/GCP shutdown; resource deletion was not independently inspected. Earlier failed probes remain historical, and restoration is optional future work rather than an assumed active incident. Owners remain unassigned.

Source baseline main `b6d984e`. Deployment is now represented by concrete bootstrap/workflow/image definitions and a documented Cloud Run URL. The 2026-10-17 availability checks failed; hosting is now reported shut down, and live resource/account/IAM/rules/provider state is not established. Configuration/secrets details are canonical in [infrastructure](../engineering/infrastructure.md). Owners unassigned; [maintenance](../maintenance.md) evidence rules apply.

| Milestone | Gate | Current state |
| --- | --- | --- |
| INF-M0 | Traceable repo/wiki baseline | Reconciliation/source/inventory present; no new publication requested |
| INF-M1 | Compatible tools and real Firebase client/server setup | Backend source manifests exist; this host only has Python/Node in checked PATH; mobile setup missing |
| INF-M2 | Healthy deployed API/data/extraction | Definitions/old URL exist; cloud shutdown reported, fresh hosting acceptance deferred |
| INF-M3 | Reproducible full operational/access/limit handoff | Expanded tests/metadata/health smoke definitions present; execution/integration gates open |

| ID | Milestone | Status | Owner | Activity / completion gate | Evidence / dependency |
| --- | --- | --- | --- | --- | --- |
| INF-01 | INF-M0 | done | Unassigned | Tracked wiki/source/history/checker and audit record | 307 baseline tracked files inventoried; prior raw sources retained; ADR-0007/SRC-006; no commit/push in audit |
| INF-02 | INF-M1 | in-progress | Unassigned | Locate compatible tools and execute Flutter/backend/device checks | Audit Python 3.13.0/Node found; pytest/FastAPI/Firebase/Pillow/tzdata absent; Flutter/Java/Firebase/Conda/Ruff absent from checked PATH; prior host provisioning not current proof |
| INF-03 | INF-M1 | blocked | Unassigned | Real same-project Firebase Google/Android registration/signing | Backend project/URL declared; no client Firebase platform files/options or Google Services plugin committed; provider/app/SHA setup unverified |
| INF-04 | INF-M2 | in-progress | Unassigned | Source/start/schema/container/CI/deploy/address delivery and healthy runtime | Complete source/snapshot, deploy.yml/bootstrap/Dockerfile supplied;21 route operations matched; runtime/build/hosted run unverified; INF-10 |
| INF-05 | INF-M2 | unverified | Unassigned | Deployed deny-all client rules and scoped Admin IAM access | deny-all file, four indexes and deploy step exist; live policy/index readiness and combined queries unverified; INF-11 |
| INF-06 | INF-M2 | unverified | Unassigned | Real Gemini secret/model/runtime/limits and retention evidence | Async extraction exists; Secret Manager injection defined, model alias configured; one historical live scan reported in SRC-007; secret-version/retention/region evidence unverified |
| INF-07 | INF-M3 | in-progress | Unassigned | Current health/auth/isolation/retry/provider/recurrence/Android acceptance | 72 backend test functions and25 Flutter declarations; earlier14 auth/profile passes historical; full current suites unrun, service probe fails |
| INF-08 | INF-M3 | in-progress | Unassigned | Safe secrets/logs/reproducible CI/image/deployment | WIF/keyless flow, runtime secret, non-root image, log minimization and ignores; no complete secret-history audit, image/runtime success or all log-retention validation |
| INF-09 | Future | deferred | Unassigned | Inbox/workers/budget notifications/offline/optional cron | No source implementation; recurrence request-driven |
| INF-10 | INF-M2 | deferred | Unassigned | If hosting resumes, provision/configure runtime and record healthy revision | SRC-007: shutdown reported for 2026-10-17; earlier /health500 and me/schema503 remain unexplained historical observations, not proof of deletion or current incident |
| INF-11 | INF-M2 | todo | Unassigned | Validate all supported Firestore filter/usage query indexes | Four index definitions only; combined expense filters and active-rule category usage need deployed coverage; emulator success insufficient |
| INF-12 | INF-M3 | todo | Unassigned | Review deploy manual/ref entry points and WIF protection | Repository-only WIF condition; manual dispatch bypasses CI predicate; no explicit triggering-event/ref guard; live branch/environment IAM protections unverified |

Bootstrap's1USD budget is an alert, not a cap; it does not create all Firebase/app/API prerequisites. Deployment rolls out service before indexes finish provisioning. No cloud mutation, provider call, credential read or installation was performed during audit. The old Windows Android installation report is preserved as [historical setup](contributing.md#historical-local-android-provisioning-2026-10-17); do not describe its process as still alive without observing it. Track [backend](backend-tracker.md)/[frontend](frontend-tracker.md) gates alongside these rows and append [log](../log.md).
