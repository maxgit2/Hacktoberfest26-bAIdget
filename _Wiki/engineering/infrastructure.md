---
title: Infrastructure deployment and secrets
status: active
updated: 2026-10-19
---

# Infrastructure, deployment and secrets

Baseline `b6d984e`; evidence: [deploy workflow](../../.github/workflows/deploy.yml), [bootstrap](../../backend/deploy/bootstrap-gcp.sh), [CI](../../.github/workflows/ci.yml), [backend README](../../backend/README.md), [config](../../backend/app/core/config.py). This page describes code/configuration and observed probes, not an audit of live IAM or cloud resources.

## Post-hackathon operational status

The merged [README](../../README.md) reports cloud deployment shutdown on 2026-10-17; the 2026-10-19 wiki log also reports GCP project shutdown. [SRC-007](../raw/2026-10-19-post-hackathon-update.md) preserves provenance. Resource deletion and exact shutdown scope were not inspected. Treat the old URL as historical and use local emulators for development; hosted integration requires explicit reprovisioning/configuration and fresh evidence if work resumes. Reported CI/live-scan successes are historical, not checks rerun here.

Root [.gitignore](../../.gitignore) now excludes ten specific Obsidian settings/plugin files, not the entire .obsidian directory.

## Historical delivery and runtime definitions

Backend handoff supplies `https://baidget-api-voiguesqbq-ew.a.run.app/v1` in europe-west1. Root `/health` is separate from `/v1`. The frontend handoff still says TBD, and AppConfig defaults to empty; the address is not automatically enabled in Flutter. During the 2026-10-17 audit, Python urllib HTTPS GETs returned health **500**, me **503**, OpenAPI **503**, as HTML service errors. Those probes did not establish healthy startup/routing/schema/auth; they do not establish the shutdown's timing or cause. Cause is unknown without runtime/revision logs. No private data or authenticated operation was requested.

CI runs on pushes and PRs, creates the Conda environment, installs Java 21/Node 22/firebase-tools, runs Ruff check/format and pytest through local Auth/Firestore emulators. It has no Flutter, Docker-build, model-evaluation or wiki-check job. Dependencies and Firebase CLI in CI are not fully pinned.

Deploy uses successful CI `workflow_run` on main or manual `workflow_dispatch`, checks out the corresponding SHA, uses GitHub OIDC/WIF, builds/pushes the Docker image to Artifact Registry, deploys Cloud Run, deploys Firestore rules/indexes and probes health plus unauthenticated `/v1/me`=401. Image tags use the triggering SHA. Manual dispatch bypasses the CI-success predicate. The workflow does not explicitly test the triggering CI event type or pin manual dispatch to main; review repository environment/ref protections and WIF policy before treating every entry path as main-only.

Cloud Run configuration: public network access (`--allow-unauthenticated`), runtime account `baidget-api`, 0–2 instances, CPU 1/memory 512Mi, concurrency 40, timeout 60s, environment project/model, Secret Manager `gemini-api-key:latest`. Public network access lets Firebase-authenticated clients call directly; domain routers enforce bearer auth. Docs/redoc/OpenAPI are also public in source, despite the workflow comment saying only health is public. Health only returns static OK; it is not a Firestore/Gemini readiness check.

[Dockerfile](../../backend/Dockerfile) installs every pip dependency from environment.yml (including tests/lint tools), copies app code, runs as non-root and respects PORT (8080 default). No Conda runtime, image digest pin, container healthcheck or separate production requirements lock is supplied. Workflow files do not prove a successful build/run.

## Bootstrap and permissions

The Bash script configures Artifact Registry cleanup (keep three recent versions/delete older than one day), runtime/deployer service accounts, runtime datastore.user, secret-level secretAccessor, deployer Cloud Run/admin/artifact-writer/rules-admin/index-admin/serviceusage roles and actAs on runtime. It creates a GitHub OIDC provider restricted to the repository and binds workloadIdentityUser; the condition is repository-based, not branch-based. GitHub variables are GCP_PROJECT_ID, GCP_REGION, WIF_PROVIDER and DEPLOY_SA. Identifiers/defaults are environment-specific, not credentials; do not copy the committed billing-account identifier into new examples.

Bootstrap creates the secret container and permissions; its value/version must be added separately. It configures a **1 USD budget alert** at 50/90/100 percent. This is alerting, not a spending cap. It does not provision the Firebase Google provider/mobile registration, Firestore database/location, all required API enablement, signing or secret value. No Terraform/state-managed infrastructure, scheduled worker, rollback automation or alert dashboard is committed. Script execution/live resource state were not verified here.

## Configuration and credentials

| Setting | Source default / use |
| --- | --- |
| GOOGLE_CLOUD_PROJECT | demo-baidget locally; workflow sets target project |
| FIRESTORE_EMULATOR_HOST / FIREBASE_AUTH_EMULATOR_HOST | Unset by default; Firebase exec exports them to child processes; never set in production |
| GEMINI_API_KEY | Unset; missing key → extraction_unavailable; workflow injects secret version at runtime |
| GEMINI_MODEL | gemini-flash-latest; mutable provider alias, not a reproducible model version |
| GEMINI_TIMEOUT_SECONDS | 30; Flutter scan receive timeout 45, Cloud Run timeout 60 |
| SCAN_RATE_LIMIT_PER_HOUR | 30; transactional fixed UTC-hour counter per user |
| MAX_IMAGE_BYTES | 10,485,760 compressed upload bytes read by service; multipart parsing occurs before this service check |
| TZ_NAME | Europe/Rome for scan/reporting; recurrence actually hardcodes Europe/Rome |
| API_BASE_URL / USE_FIREBASE | Flutter build definitions; persisted Settings URL wins, auth mode remains independently selected |

Settings uses environment variables and does **not** automatically load `.env`; use Uvicorn `--env-file .env` locally. Runtime Firebase Admin/Firestore uses application default credentials; Cloud Run supplies service-account identity. No service-account JSON key is required by this workflow. Tests require both emulator hosts and create synthetic emulator users; never run them against a live database or provider.

Tracked `.env.example` has placeholders. Backend ignore excludes `.env`, caches and logs; root ignores Flutter/build/editor artifacts but has no general service-account/keystore exclusion. The Docker build context is backend-only; `.dockerignore` excludes `.env`, tests/specs/caches, and Dockerfile copies only app plus the manifest. Ignore rules are not a secret scanner. Inspection found no private-key/service-account JSON/token credential file in tracked paths; this is not a full Git history or remote-secret audit. Project/billing identifiers are not secret values. No provider key was read or printed.

## Data access, indexes and operations

Client Firestore rules deny all documents; Admin SDK access is controlled by IAM and UID-scoped repository code, not those client rules. Production rules, Google provider, IAM bindings, secret versions, Firestore region, backups/TTL and deletion policy remain unverified. Only Firestore/Auth emulator ports8080/9099 are supplied; they are not the FastAPI API port.

Four committed expense composite indexes cover deleted_at plus date/name, category/date, type/date, needs_review/date. Multiple simultaneous equality filters and active-rule category usage queries need production index validation; passing emulators would not establish index coverage. The deploy runs Firestore rules/indexes **after** rolling out the service, so newly required indexes may not be ready when the revision begins serving.

Request logs deliberately contain request ID, method, status and timestamp, without route body, token or receipt content. Root config leaves other SDK loggers enabled, so end-to-end sensitive-log handling is not independently established. Uploaded files are not saved to an application image collection or object store; UploadFile/framework may use temporary spooling, and provider retention is unspecified. See [AI/data](ai-and-data.md).

If hosting is resumed, collect fresh healthy-service evidence, validate deployment-entry trust and IAM, test combined indexes, configure Android Firebase/signing, define retention and run real auth/owner checks with synthetic data before closing [infrastructure gates](../development/infrastructure-tracker.md). No cloud configuration was changed by this audit.
