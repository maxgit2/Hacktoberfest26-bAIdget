---
title: Initial project brief source note
status: active
updated: 2026-10-17
---

# Initial project brief source note

- Source ID: SRC-001.
- Origin: project initiator's initial message in the repository bootstrap conversation, 2026-10-17.
- Original language: Italian.
- Record type: English translation and structured normalization of the supplied brief, not a verbatim transcript. The original remains in the conversation; there is no public message URL.
- Handling: preserve this record after ingestion. Add a new dated source note for later corrections or requirements.

## Project and collaboration

bAIdget is an expense categorization/tracking app used from mobile, initially Android. A team of backend/frontend programmers, designers, and other contributors is building it during a one-day hackathon. Specifications are early and will evolve quickly during the next hours.

All project documentation and comments must always be English, regardless of the language used to talk with agents, because the repository is open source on GitHub and intended for international contributors.

## Requested shared knowledge system

Initialize a flexible LLM-assisted wiki in `_Wiki`, based on [Karpathy's LLM Wiki idea and its comments](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), adapted for software development. Track decisions, flows, choices, structure, technical frameworks/libraries, discoveries, created work, and solved problems. Provide instruction files for both Codex and Claude so agents maintain the same shared knowledge as work evolves.

## Main capabilities

- Authentication; first access offers Google sign-in.
- Configure categories after sign-in: choose a prepared template or create categories from scratch. Templates initially have four or six categories; users can rename, add, or remove categories.
- Home offers receipt scanning, expense import, and spending summaries.
- Receipt scanning opens the camera. The app contacts the backend, which calls an OCR/model integration to read data and classify using the user's configured categories. The user reviews extracted information and can correct it.
- Manual purchase entry, with one-off and recurring expenses mentioned.
- Forward payment emails to a generated email address created during account creation. The backend periodically synchronizes received emails and has access to the receiving mailboxes.
- Expense summaries by month, year, and category, for a single individual.

## Possible additions

Family groups, speech-to-text, and additional currencies are listed as possible extra features.

## Initial technical direction

- Android app.
- Backend: FastAPI and Firebase; no specific Firebase services or versions supplied.
- Frontend: Flutter.

The message does not select the AI provider/model, email provider, exact database schema, API contracts, deployment target, category labels, default currency, app display language, or final hackathon scope. Product pages distinguish these unknowns from requirements. See [source register](../sources/index.md) and [scope](../product/scope.md).
