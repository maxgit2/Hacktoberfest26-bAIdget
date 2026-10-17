---
title: Repository reconciliation audit
status: active
updated: 2026-10-17
---

# Repository reconciliation audit

Requested by the project initiator to reconcile the wiki after the dev merge. Baseline: `b6d984e`; initial working tree clean. Documentation only; source findings do not imply live deployment or human acceptance of every implementation choice.

## Resume protocol

Read this page, current state, and the diff first. Each tracked file below must be accounted for. Text files are inspected directly; generated assets are assessed as groups, not executed or interpreted as business behavior. Preserve raw records and historical log entries. Update canonical topics, questions, decisions and all three trackers, then run the wiki checker. Do not publish secrets or personal data.

## Progress

- [x] Read shared policies, maintenance, current state, index and questions.
- [x] Capture baseline and full tracked-file inventory.
- [x] Initial graph discovery/query/impact failed (repo not registered/runner absent); retried after user indexing. Named context/impact/process trace available at b6d984e; concept search degraded by missing FTS. No application symbols edited.
- [x] Inspect backend source/models/repositories/services/routers.
- [x] Inspect frontend source/platforms/tests and all manifests.
- [x] Inspect infrastructure, deployment, secrets boundaries and test/eval artifacts.
- [x] Reconcile canonical engineering/product pages and source/decision registers.
- [x] Reconcile questions, trackers, setup, policy summary and current state.
- [x] Run available checks, inspect final consistency/diff and append log.

## Verification ledger

Current results are detailed in the [review](integration-review.md#post-merge-audit-at-b6d984e); earlier-session results remain historical.

| Executed check | Observed result |
| --- | --- |
| Initial `git status --short`; `git log -6 --oneline`; `git ls-files` | Clean at b6d984e,307 tracked files; inventory below |
| `python -` stdlib AST/JSON/route comparison | Python 3.13.0;57 tracked Python files parse;15 schema paths/21 operations;20 handoff operations included; router methods/paths exactly match snapshot |
| `python -` direct money and isolated actual-function probes | Exact cents, separator/rejection cases passed; UTC month/leap/UUID checks passed; generic scan serializer drift and21-rule false backlog reproduced with explicit stubs |
| `python -m pytest --collect-only -q` | Cannot start: No module named pytest. FastAPI/Firebase/Firestore/Pillow/tzdata also absent; no emulator/Flutter/Ruff/container/hosted/provider success claimed |
| Python urllib public HTTPS GETs | /health500; /v1/me503; /v1/openapi.json503, HTML service errors; no token/business mutation; cause unknown |
| GitNexus after user indexing | Fresh source commit b6d984e,250 indexed files/2,004 nodes/4,037 edges/115 flows. FTS-degraded concept queries empty; named contexts and named scan quota trace corroborated source. current_user empty incoming misses Depends usage; source confirms it |
| Documentation impact | current-state/root AGENTS/README MEDIUM; trackers/questions/review HIGH due18–21 direct document references,44 reachable files; warned before those edits, keep IDs/paths coherent; no File process membership |

Final wiki/diff/inventory/hash checks and graph result are recorded below after execution. No application code, dependency, provider configuration or Git branch/commit was changed. The user-generated GitNexus policy count changes in root AGENTS/CLAUDE are preserved.

## File inventory

Legend: `read` application/test/spec/wiki text inspected; `role` generated/native scaffold or instruction asset reviewed structurally for its role (not line-by-line native correctness); `asset` binary icon/launch image inventoried by type/size, not visually audited; `preserved` source/history inspected and retained. This is repository coverage, not an assertion that every generated native runner is tested or supported. Group conclusions belong in canonical pages.

| File | Review | Notes |
| --- | --- | --- |
| `.claude/skills/gitnexus-cli/SKILL.md` | role | Local graph workflow instructions, no product implementation |
| `.claude/skills/gitnexus-debugging/SKILL.md` | role | Local graph workflow instructions, no product implementation |
| `.claude/skills/gitnexus-exploring/SKILL.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `.claude/skills/gitnexus-guide/SKILL.md` | role | Local graph workflow instructions, no product implementation |
| `.claude/skills/gitnexus-impact-analysis/SKILL.md` | role | Local graph workflow instructions, no product implementation |
| `.claude/skills/gitnexus-refactoring/SKILL.md` | role | Local graph workflow instructions, no product implementation |
| `.github/workflows/ci.yml` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `.github/workflows/deploy.yml` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `.gitignore` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `.metadata` | role | License or Flutter generated metadata; no feature completion inferred |
| `AGENTS.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `CLAUDE.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `LICENSE` | role | License or Flutter generated metadata; no feature completion inferred |
| `README.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/current-state.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/decisions/adr-0001-shared-project-wiki.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/decisions/adr-0002-initial-stack.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/decisions/adr-0003-flutter-scaffold.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/decisions/adr-0004-updated-product-baseline.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/decisions/adr-0005-api-handoff-baseline.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/decisions/adr-0006-integrated-client-and-backend.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/decisions/index.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/development/backend-tracker.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/development/contributing.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/development/frontend-tracker.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/development/infrastructure-tracker.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/development/integration-review.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/engineering/ai-and-data.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/engineering/architecture.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/engineering/contracts.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/engineering/domain-model.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/index.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/lessons/backend-emulator-test-isolation.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/lessons/firestore-profile-contention.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/lessons/git-author-identity.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/lessons/index.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/log.md` | preserved | Prior history retained; append audit evidence only |
| `_Wiki/maintenance.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/open-questions.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/product/scope.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/product/user-flows.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/raw/2026-10-17-frontend-handoff.md` | preserved | Historical source retained; current implementation corrected through SRC-006 |
| `_Wiki/raw/2026-10-17-integration-source-record.md` | preserved | Historical source retained; current implementation corrected through SRC-006 |
| `_Wiki/raw/2026-10-17-karpathy-reference.md` | preserved | Historical source retained; current implementation corrected through SRC-006 |
| `_Wiki/raw/2026-10-17-project-brief.md` | preserved | Historical source retained; current implementation corrected through SRC-006 |
| `_Wiki/raw/2026-10-17-updated-specification.md` | preserved | Historical source retained; current implementation corrected through SRC-006 |
| `_Wiki/sources/index.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/templates/decision.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/templates/lesson.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/templates/source.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/templates/topic.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `_Wiki/tools/check_wiki.py` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `analysis_options.yaml` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `android/.gitignore` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/app/build.gradle.kts` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/app/src/debug/AndroidManifest.xml` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/app/src/main/AndroidManifest.xml` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/app/src/main/kotlin/com/example/baidget/MainActivity.kt` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/app/src/main/res/drawable-v21/launch_background.xml` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/app/src/main/res/drawable/launch_background.xml` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/app/src/main/res/mipmap-hdpi/ic_launcher.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `android/app/src/main/res/mipmap-mdpi/ic_launcher.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `android/app/src/main/res/mipmap-xhdpi/ic_launcher.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `android/app/src/main/res/values-night/styles.xml` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/app/src/main/res/values/styles.xml` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/app/src/profile/AndroidManifest.xml` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/build.gradle.kts` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/gradle.properties` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/gradle/wrapper/gradle-wrapper.properties` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `android/settings.gradle.kts` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `backend/.agents/rules/agents.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/.claude/skills/api-contract/SKILL.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/.claude/skills/fastapi-layering/SKILL.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/.claude/skills/firestore-patterns/SKILL.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/.claude/skills/llm-structured-extraction/SKILL.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/.dockerignore` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/.env.example` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/.gitignore` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/AGENTS.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/CLAUDE.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/CONTRACT-REPORT.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/Dockerfile` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/GEMINI.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/README.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/app/core/auth.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/core/config.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/core/errors.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/core/logging.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/core/money.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/core/time.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/imaging/image.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/llm/gemini.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/llm/prompt.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/llm/schema.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/main.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/models/category.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/models/errors.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/models/expense.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/models/recurring.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/models/summary.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/models/user.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/repositories/categories.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/repositories/client.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/repositories/expenses.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/repositories/rate_limit.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/repositories/rules.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/repositories/users.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/routers/categories.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/routers/expenses.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/routers/health.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/routers/me.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/routers/recurring.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/routers/scan.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/routers/summary.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/services/catalog.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/services/categories.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/services/expenses.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/services/recurrence.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/services/recurring.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/services/scan.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/services/summary.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/app/services/users.py` | read | Domain/control/data path reviewed; findings in current integration review |
| `backend/deploy/bootstrap-gcp.sh` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/environment.yml` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/firebase.json` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/firestore.indexes.json` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/firestore.rules` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/openapi.json` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/pyproject.toml` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/scripts/export_openapi.py` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `backend/specs/02-data-model.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/03-architecture.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/frontend-handoff.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/open-questions.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/tasks/00-scaffold.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/tasks/01-auth-me.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/tasks/02-categories.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/tasks/03-expenses.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/tasks/04-summaries.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/tasks/05-recurring.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/tasks/06-scan.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/specs/tasks/07-hardening.md` | read | Target specification compared with code; protected source left unchanged |
| `backend/tests/conftest.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/01_grocery_receipt.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/02_restaurant_receipt.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/03_payment_screenshot.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/04_comma_amount.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/05_invoice.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/06_missing_date.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/07_missing_seller.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/08_weighted_item.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/09_prompt_injection.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/cases/10_unreadable_total.json` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/eval/evaluate.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_auth.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_categories.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_contract.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_errors.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_expenses.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_health.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_imaging.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_llm_schema.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_me.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_money.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_openapi_snapshot.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_recurrence_math.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_recurring.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_scan.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `backend/tests/test_summary.py` | read | Assertions/fixtures inspected; synthetic/mock evidence, suite unrun here |
| `docs/frontend-handoff.md` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `ios/.gitignore` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Flutter/AppFrameworkInfo.plist` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Flutter/Debug.xcconfig` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Flutter/Release.xcconfig` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner.xcodeproj/project.pbxproj` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner.xcodeproj/project.xcworkspace/contents.xcworkspacedata` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner.xcodeproj/project.xcworkspace/xcshareddata/IDEWorkspaceChecks.plist` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner.xcodeproj/project.xcworkspace/xcshareddata/WorkspaceSettings.xcsettings` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner.xcworkspace/contents.xcworkspacedata` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner.xcworkspace/xcshareddata/IDEWorkspaceChecks.plist` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner.xcworkspace/xcshareddata/WorkspaceSettings.xcsettings` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner/AppDelegate.swift` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-1024x1024@1x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-20x20@1x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-20x20@2x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-20x20@3x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-29x29@1x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-29x29@2x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-29x29@3x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-40x40@1x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-40x40@2x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-40x40@3x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-60x60@2x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-60x60@3x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-76x76@1x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-76x76@2x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-83.5x83.5@2x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/LaunchImage.imageset/Contents.json` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner/Assets.xcassets/LaunchImage.imageset/LaunchImage.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/LaunchImage.imageset/LaunchImage@2x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/LaunchImage.imageset/LaunchImage@3x.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `ios/Runner/Assets.xcassets/LaunchImage.imageset/README.md` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner/Base.lproj/LaunchScreen.storyboard` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner/Base.lproj/Main.storyboard` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner/Info.plist` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner/Runner-Bridging-Header.h` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/Runner/SceneDelegate.swift` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `ios/RunnerTests/RunnerTests.swift` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `lib/app.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/auth/auth_providers.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/auth/auth_service.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/auth/firebase_auth_service.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/config/app_config.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/format/formatters.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/network/api_client.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/network/api_error_messages.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/network/api_exception.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/network/auth_interceptor.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/network/mock_backend.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/settings/api_base_url.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/theme/design_tokens.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/core/widgets/status_views.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/account/data/account_repository.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/account/domain/user_profile.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/auth/presentation/sign_in_screen.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/categories/data/categories_repository.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/categories/domain/category.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/categories/presentation/category_style.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/expenses/data/expenses_repository.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/expenses/domain/expense.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/expenses/presentation/expense_detail_screen.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/onboarding/presentation/onboarding_screen.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/settings/presentation/settings_screen.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/upload/data/receipt_image_picker.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/features/upload/presentation/upload_screen.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `lib/main.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `linux/.gitignore` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `linux/CMakeLists.txt` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `linux/flutter/CMakeLists.txt` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `linux/flutter/generated_plugin_registrant.cc` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `linux/flutter/generated_plugin_registrant.h` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `linux/flutter/generated_plugins.cmake` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `linux/runner/CMakeLists.txt` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `linux/runner/main.cc` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `linux/runner/my_application.cc` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `linux/runner/my_application.h` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/.gitignore` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Flutter/Flutter-Debug.xcconfig` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Flutter/Flutter-Release.xcconfig` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Flutter/GeneratedPluginRegistrant.swift` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner.xcodeproj/project.pbxproj` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner.xcodeproj/project.xcworkspace/xcshareddata/IDEWorkspaceChecks.plist` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner.xcworkspace/contents.xcworkspacedata` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner.xcworkspace/xcshareddata/IDEWorkspaceChecks.plist` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/AppDelegate.swift` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/Assets.xcassets/AppIcon.appiconset/app_icon_1024.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `macos/Runner/Assets.xcassets/AppIcon.appiconset/app_icon_128.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `macos/Runner/Assets.xcassets/AppIcon.appiconset/app_icon_16.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `macos/Runner/Assets.xcassets/AppIcon.appiconset/app_icon_256.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `macos/Runner/Assets.xcassets/AppIcon.appiconset/app_icon_32.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `macos/Runner/Assets.xcassets/AppIcon.appiconset/app_icon_512.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `macos/Runner/Assets.xcassets/AppIcon.appiconset/app_icon_64.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `macos/Runner/Base.lproj/MainMenu.xib` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/Configs/AppInfo.xcconfig` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/Configs/Debug.xcconfig` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/Configs/Release.xcconfig` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/Configs/Warnings.xcconfig` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/DebugProfile.entitlements` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/Info.plist` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/MainFlutterWindow.swift` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/Runner/Release.entitlements` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `macos/RunnerTests/RunnerTests.swift` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `pubspec.lock` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `pubspec.yaml` | read | Reviewed as documentation/configuration/policy; historical claims reconciled where applicable |
| `test/api_test.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `test/app_flow_test.dart` | read | Client feature/mode/parser/test behavior inspected; Flutter execution unavailable |
| `web/favicon.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `web/icons/Icon-192.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `web/icons/Icon-512.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `web/icons/Icon-maskable-192.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `web/icons/Icon-maskable-512.png` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `web/index.html` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `web/manifest.json` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/.gitignore` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/CMakeLists.txt` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/flutter/CMakeLists.txt` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/flutter/generated_plugin_registrant.cc` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/flutter/generated_plugin_registrant.h` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/flutter/generated_plugins.cmake` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/CMakeLists.txt` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/Runner.rc` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/flutter_window.cpp` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/flutter_window.h` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/main.cpp` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/resource.h` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/resources/app_icon.ico` | asset | Platform icon/launch image; no business behavior or visual QA claim |
| `windows/runner/runner.exe.manifest` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/utils.cpp` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/utils.h` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/win32_window.cpp` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |
| `windows/runner/win32_window.h` | role | Runner/build/plugin/permission/resource role inspected; no native build; key configs covered in architecture/setup |

## Audit-created pages

All four pages are inspected and indexed: this ledger, [infrastructure](../engineering/infrastructure.md), [ADR-0007](../decisions/adr-0007-merged-backend-baseline.md) and [SRC-006](../raw/2026-10-17-post-merge-audit.md). The307-row baseline includes neither these new pages nor local GitNexus database/cache artifacts. The user generated `.gitnexus/` during the audit; it is local analysis infrastructure, not a product feature or a source file to publish.

## Reproduce the bounded static checks

From repository root, run this Python block with `python -` or an equivalent UTF-8 script runner. It requires only the standard library. It checks syntax and static API topology, **not runtime schema equality or application behavior**.

```python
import ast
import json
import re
import subprocess
from pathlib import Path

files = subprocess.check_output(["git", "ls-files"], text=True).splitlines()
for name in files:
    if name.endswith(".py"):
        ast.parse(Path(name).read_text(encoding="utf-8"), filename=name)
schema = json.loads(Path("backend/openapi.json").read_text(encoding="utf-8"))
actual = {(method, path) for path, ops in schema["paths"].items() for method in ops}
text = Path("backend/specs/frontend-handoff.md").read_text(encoding="utf-8")
section = text.split("## 5. Endpoints", 1)[1].split("## 6.", 1)[0]
expected = {(method.lower(), "/v1" + path.split("?", 1)[0])
            for method, path in re.findall(r"^### `([A-Z]+) ([^`]+)`$", section, re.M)}
assert expected <= actual
registered = set()
for path in Path("backend/app/routers").glob("*.py"):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    prefix = ""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "APIRouter":
            prefix = next((ast.literal_eval(k.value) for k in node.keywords if k.arg == "prefix"), "")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute) and dec.func.attr in {"get", "post", "patch", "delete", "put"}:
                    registered.add((dec.func.attr, prefix + ast.literal_eval(dec.args[0])))
assert registered == actual
print("PASS: Python syntax and static route/snapshot/handoff inventory", len(actual))
```

The defect probes execute AST-selected actual function bodies with an identity response model stub and a fake repository of 21 non-due rules respectively. They corroborate the source findings A-01/A-03 without bypassing the emulator test safety fixture. For full acceptance use the commands in [contributing](contributing.md), with compatible dependencies and local emulators.

## Reconciliation outcomes

Canonical architecture/contracts/model/AI-data/infrastructure/product pages now match backend source and partial client boundaries. All existing task/question IDs retained; backend02–07 tasks changed from absent/todo to source-present but gate-unverified, and new findings have BE-13–16, FE-15, INF-10–12 and Q-25–32 follow-ups. No unresolved contract was silently accepted. Raw sources/log history remain intact; historical integration/provisioning/ADR inventories are labeled by their original baseline.

Final graph check (before log append): MCP detect_changes(scope=all) reported 23 tracked changed files,74 documentation sections,0 affected execution processes and low change risk. The response did not expose partial/truncated flags; no application safety conclusion is drawn from an empty process list. It excludes four untracked new wiki pages; those are covered by inventory/link/content checks. No commit requested/performed.

## Final handoff checks

- Wiki structural check passed:41 pages, three entry points, local links/metadata/index coverage valid; final command rerun after log append.
- `git diff --check` and separate task Markdown UTF-8/newline/whitespace/conflict checks passed. Five prior raw records and the old log prefix preserved (Git-normalized line endings).
- Inventory has307 unique baseline paths with review states; all task IDs preserved,16 backend/15 frontend/12 infrastructure rows have valid statuses/owners/evidence,32 question IDs retained/extended.
- Re-executed the reproducible static-check block from this file successfully. Source/test/config paths unchanged; no commit/push. The user's concurrent root `.obsidian/` files remain untouched and excluded from deliverable checks.
- Full application verification remains explicitly pending for environment/deployment reasons recorded above; audit/reconciliation itself is complete, not blocked on implementing the findings.
