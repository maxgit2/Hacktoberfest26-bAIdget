# 03 — Architecture

## System
```mermaid
flowchart LR
  app["Flutter app"] -->|Google sign-in| fauth["Firebase Auth"]
  app -->|"HTTPS + Bearer ID token"| api["FastAPI on Cloud Run (EU)"]
  api -->|"verify token (threadpool)"| fauth
  api -->|"AsyncClient"| fs[("Firestore<br/>users/{uid}/...")]
  api -->|"structured output"| gem["Gemini API"]
  app -. "rules: deny all" .-x fs
```

## Layers (inside the API)
```mermaid
flowchart TB
  r["routers/ — HTTP only: parse, auth dep, call service, map response"] --> s["services/ — business rules, Decimal money, recurrence math, needs_review"]
  s --> repo["repositories/ — ONLY place that imports google.cloud.firestore"]
  s --> llm["llm/ — Gemini client + schema + prompt (mockable)"]
  s --> img["imaging/ — Pillow validate, EXIF strip, resize"]
  core["core/ — config, errors, logging, auth dependency"] -.-> r & s & repo
```

## Request flows
**Scan:** router (multipart) → `imaging` validates and strips the image (in memory only) → rate limit (repository transaction) → `llm.extract()` → schema validation → category mapped to the user's categories, falling back to `Other` → `needs_review` rules → `expenses_repo.create_idempotent`. The image is never persisted or logged.

**Recurring sync:** for each active rule (≤ 20) → one transaction: compute occurrence n from `start` → deterministic id → create if absent → advance `next_index`.

## Package layout (target)
```
app/
  main.py            # app factory, routers, exception handlers
  core/              # config.py, errors.py, logging.py, auth.py, time.py, money.py
  routers/           # health, me, categories, expenses, recurring, summary, scan
  services/          # one per domain
  repositories/      # firestore client + one repo per collection
  llm/               # gemini.py, schema.py, prompt.py
  imaging/           # image.py
  models/            # pydantic API schemas
tests/               # pytest + emulators; fixtures: two users
```
