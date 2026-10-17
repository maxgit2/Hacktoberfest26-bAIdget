# API contract comparison

Compared `openapi.json` and the implemented request/response models with `specs/frontend-handoff.md` section 5.

## Matches

- Every method and path listed in section 5 exists under `/v1`.
- Documented primary status codes match, including `200` for idempotent expense and scan retries.
- All error codes in section 3 exist in the application, and the API emits the documented error envelope.
- `/health` remains at the root, as adopted in Q-12.

## Mismatches

| Area | Frontend handoff | Real API / OpenAPI |
|---|---|---|
| `POST /expenses` request | Calls `currency` required while also giving it a default of `EUR`. | `currency` is optional in OpenAPI and defaults to `EUR`. |
| `Expense.scan_details` | Documents a fixed object with `document_type`, `items`, `vat_total`, `vat_number`, and `payment_method`. | Runtime returns those fields, but OpenAPI exposes `scan_details` as an arbitrary object because the response model is `dict[str, object]`. |
| `POST /expenses` errors | Endpoint lists `category_not_found` and `validation_error`. | It can also return `404 not_found` when an id belongs to a soft-deleted expense, as adopted in Q-2. |
| `POST /expenses/scan` errors | Endpoint lists image, extraction, rate-limit, and provider errors. | It can also return `404 not_found` for a soft-deleted id, `category_not_found` when no active Other category exists, and `validation_error` for malformed multipart fields. |
| Endpoint error lists | Some endpoint sections list only selected errors. | OpenAPI also documents authentication, request validation, resource-not-found, and internal errors wherever the route can emit them. The section 3 global error table contains all of these codes. |

No runtime contract behavior was changed to resolve these discrepancies.
