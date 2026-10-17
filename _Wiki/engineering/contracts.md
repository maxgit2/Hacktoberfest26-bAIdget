---
title: Integration contracts
status: draft
updated: 2026-10-17
---

# Integration contracts

At scaffold commit `055275e`, no product routes, runtime schemas, status codes, or event formats are present. [lib/main.dart](../../lib/main.dart) is a counter demo with no API calls; [pubspec.yaml](../../pubspec.yaml) has no auth/network/provider dependencies. No backend manifest/routes exist. [SRC-003](../raw/2026-10-17-updated-specification.md) now supplies field names and flows, adopted in [ADR-0004](../decisions/adr-0004-updated-product-baseline.md); these are requirements, not an executable API.

## Source-defined contract inputs

- **Identity:** automatic smartphone ID/fingerprint replaces Google sign-in; backend proof/session and recovery remain unresolved. Do not authorize from a device ID or `owner` payload alone.
- **Expense fields:** the [model](domain-model.md) preserves all 11 source fields, optional float amount, default euro, timestamps, and `single` / `concurrent {info}`. ID, timestamp/union encoding, precision/null policy, and deletion semantics remain open. Do not silently normalize source literals into a different schema.
- **Input:** gallery image to backend OCR/classification, then correction in the same form used for manual input; additional camera capture remains open. OCR review is required; the explicit save protocol is proposed.
- **Summaries:** weekly/monthly/yearly/category views and current-versus-previous-period comparisons; agree optional amount, deletion, currency, recurrence, and time boundaries before aggregation.
- **Delivery:** auth/input 1.0, deployment/categories/summaries 2.0, email 3.0, budgets/alerts 4.0, chart variants 5.0. These labels are planned scope, not deployed API versions.

## Contract checklist before parallel implementation

| Area | Agree and record | Current status |
| --- | --- | --- |
| Identity | Device ID/fingerprint generation/storage, backend credential/session/proof, account provisioning/recovery | Direction supplied; mechanism open |
| Categories | Template payload, stable IDs, customization operations, validation, category deletion behavior | Open |
| Expenses | Source fields in model; ID, encoding, precision/nulls, category reference, mutations/deletion | Source list supplied; wire/validation open |
| Receipt upload | Payload format, supported media, size limit, authentication, response timing, retry behavior | Open |
| Extraction | Structured draft schema, nullable/missing fields, category ID validation, failure representation | Open |
| Confirmation | Create vs update semantics, concurrency/repeated taps, ownership, idempotency | Open |
| Email import | Address provisioning, recipient mapping, polling, delivery deduplication, pending review visibility | Open |
| Summaries | Weekly/monthly/yearly/current-previous boundaries, category totals, currency/null/deletion/draft/recurrence treatment | Views supplied; aggregation open |
| Budgets/alerts | Budget fields/period, 25/50/75/100% thresholds, category option, notification/reset/deduplication | 4.0 scope supplied; contract open |
| Errors | Stable machine-readable error code, safe message, field errors, retryability; app recovery state | Open |

## Proposed AI extraction boundary

The backend should provide input content and the allowed categories for the authenticated user. The provider should return **candidate** purchase information in a constrained structure. The backend validates the result before exposing a draft to the app.

DeepSeek-OCR is named, but variant/host, output format, and classification stages are not agreed. Discuss mapping to `seller`, `date`, `title`, `category`, `amount`, and `currency`, keeping missing/uncertain values explicit. These are source domain fields, not a complete extraction response. Required saved-expense fields may be missing in a draft; ownership/creation metadata must not come from model output. Line items remain conditional on allocation decisions. Self-reported model confidence is not calibrated accuracy.

Agree what the app receives when data is partial, the provider times out, categories changed during extraction, or the model returns an unknown category. Provider output never supplies trusted ownership, backend instructions, SQL, or executable code.

## Recording the first real contract

1. Resolve the relevant [questions](../open-questions.md) and record the decision and affected roles.
2. Add a small synthetic request/response example with exact field names, encoding, and expected failure cases.
3. Link the actual schema/routes and any generated OpenAPI file once they exist. Inspect implementation rather than maintaining a second competing full API specification.
4. Record how mocks differ from the real contract and verify one agreed request across client/backend.
5. Update [flows](../product/user-flows.md), [domain model](domain-model.md), and [current state](../current-state.md).

The first integrator should replace open rows with links to actual contracts and evidence. Until then, do not describe this page as a working API reference.
