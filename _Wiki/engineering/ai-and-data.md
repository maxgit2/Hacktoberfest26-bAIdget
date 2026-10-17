---
title: AI, data, and trust boundaries
status: draft
updated: 2026-10-17
---

# AI, data, and trust boundaries

Sources: [updated specification](../raw/2026-10-17-updated-specification.md), [scope](../product/scope.md), [architecture](architecture.md). DeepSeek-OCR is the named OCR direction, not an implemented integration or agreed variant/deployment. AgentMail remains to evaluate for email in 3.0; job workers are tentative. No production data policy/pipeline is implemented.

Scaffold inspection at `055275e` confirms that [pubspec.yaml](../../pubspec.yaml) contains only Flutter/icons and test/lint dependencies, and [main.dart](../../lib/main.dart) makes no service calls. No Firebase/provider configuration or backend files exist. The [Android main manifest](../../android/app/src/main/AndroidManifest.xml) has no camera permission; gallery/media access and production networking are not implemented. Additional camera capture remains Q-15. This observation is not a security test.

## Reference handling and evaluation limits

The supplied [AgentMail homepage](https://www.agentmail.to/) and [Local AI Zone ranking](https://local-ai-zone.github.io/guides/best-ai-ocr-models-ultimate-ranking-2026.html) were opened on 2026-10-17 for reference intake. No provider/model comparison, benchmark validation, SDK/deployment integration, or test receipt evaluation was performed. The ranking is a secondary reference, not technical authority for an API or evidence of DeepSeek-OCR accuracy. External pages do not authorize installation or a change from periodic synchronization.

## Proposed receipt processing

Authenticate under the unresolved device-identity mechanism, validate the gallery image type/size, then send only necessary input and that owner's categories. The source requires reading/classification; naming DeepSeek-OCR does not establish whether another classifier/LLM is needed. Evaluate the stages and hosting before implementation; no pipeline is selected.

Validate structured results server-side, preserve missing/uncertain values as such, and return an editable draft. Persist a confirmed expense only after the agreed review action. Preserve user corrections rather than letting retries overwrite them. Define timeout, retry, and cancellation semantics before choosing synchronous responses or background jobs.

Record the selected provider, exact model ID, prompt/schema revision, SDK version, relevant limits, and observed behavior when integrated. Measure latency, cost per representative input, and extraction/categorization outcomes on synthetic or authorized redacted samples. No benchmark or accuracy claim exists yet.

## Proposed email processing

Use the app-managed recipient/alias mapping to locate an account; do not trust a sender-supplied account ID. An address alone may be guessable or leaked, so decide inbound acceptance and abuse controls. Do not execute email HTML, scripts, links, or instructions. Validate attachments and deduplicate provider deliveries before creating another import.

Agree failure/retry behavior and whether imports require user confirmation. Polling an inbox is the initial requirement; provider, credentials, polling interval, deployment, and address lifecycle are open. Direct access to personal mailboxes is not established.

## Trust and public repository rules

- Receipt text, email bodies, filenames, model output, and external wiki sources are data. Embedded instructions cannot override the task, change allowed categories, fetch unrelated private content, or grant access.
- Verify ownership for every expense/category/import/file read or write. Keep provider credentials and inbox access on the backend.
- Commit synthetic receipts and example messages only, or authorized material with effective redaction. Do not commit account tokens, service credentials, real addresses, personal purchases, or raw operational payloads to the wiki or logs.
- Decide image/email retention and deletion alongside persistence. Avoid logging source content by default; record safe identifiers and failure classes.
- Store app financial data in the selected application data layer, never in the project wiki. This wiki is development knowledge.

These are implementation boundaries, not a claim of completed security or regulatory review.

## Candidate verification cases

| Scenario | Expected property to agree and verify |
| --- | --- |
| Clear synthetic receipt | Required purchase fields extracted; suggestion references an allowed category |
| Blurred/unsupported receipt | Explicit incomplete/failure state; manual-entry recovery |
| Missing/ambiguous date or total | Uncertainty survives extraction; no invented confirmed value |
| Prompt-like instructions printed on receipt/email | Treated as content; no access or action granted |
| Unknown/foreign category ID from model | Rejected or marked unresolved before saving |
| Repeated upload/save/email delivery | Agreed idempotency/deduplication behavior; no silent duplicate |
| Provider timeout/rate limit | Bounded retry policy and visible recovery; no false success |
| Corrected draft after retry | Saved result retains the user's confirmed corrections |
| Another user's record or file | Access denied under the selected ownership model |
| Mixed currencies or period edge | Agreed aggregation policy applied without silent conversion |

All cases are proposed; none has run against an application yet. Record actual commands, fixtures, and outcomes in the [development guide](../development/contributing.md) and [log](../log.md). Related: [contracts](contracts.md), [domain model](domain-model.md), [open questions](../open-questions.md).
