---
name: fastapi-layering
description: Review or specify bAIdget FastAPI code layering — routers/services/repositories split, auth dependency, threadpool for blocking SDKs, error mapping. Use when writing a task spec or reviewing a slice diff.
---
- Router: parse input (pydantic), `user = Depends(current_user)`, call ONE service function, return a `response_model`. No `if` on business rules, no Firestore.
- Service: business rules, Decimal money, raises `AppError(code, status, msg, details)` with codes from `frontend-handoff.md` §3 only.
- Repository: only module importing `google.cloud.firestore`; takes `uid` as first arg; builds paths from `users/{uid}`.
- Blocking calls (`firebase_admin.auth.verify_id_token`, Pillow, sync Gemini client) → `await run_in_threadpool(...)`.
- Review grep: `grep -rn "google.cloud" app/ | grep -v repositories/` must be empty; `grep -rn "float(" app/services` suspicious.
- Every route: explicit `operation_id`, `response_model`, `status_code`.
