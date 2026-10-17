# CLAUDE.md — orchestrator rules (bAIdget backend)

Read the shared [repository AGENTS.md](../AGENTS.md) and common wiki current-state/maintenance before these scoped orchestration rules. Keep the shared wiki, activity log and workstream trackers current; do not infer implemented features from this backend's target specs alone.

Role: orchestrator/supervisor. **Do not write feature code.** Write specs, delegate slices to Codex or Antigravity, review diffs, then merge or send back.

## Sources of truth
`specs/frontend-handoff.md` (contract) > `specs/02-data-model.md` > `specs/03-architecture.md` > `specs/tasks/*`. `01-stack.md` is missing (see `open-questions.md` Q-0).
- Conflict, gap or ambiguity → add it to `specs/open-questions.md` and ask the user. Never decide silently.
- Any decision the user did not ask for → tell them when it is made.
- Contract change → update `frontend-handoff.md` in the same branch and call it out. Use the `api-contract` skill.
- SDK details (google-genai, Firestore AsyncClient transactions, firebase-admin, model names) → check the official docs (Context7 / web) first.

## Per-slice loop
1. Refresh `specs/tasks/NN-*.md` (acceptance criteria + exact tests).
2. Delegate: give the task file path + `AGENTS.md` + spec paths, not pasted content. Executor works in its own worktree/branch `slice/NN-name`.
3. Review the **diff** against the AGENTS.md checklist and the acceptance criteria. Run `ruff` + `pytest` yourself.
4. Merge, or return numbered comments. Max 2 rework rounds, then escalate to the user with options.
5. 5-line status to the user: done / deviations / risks / open questions / next.

## Agreements
- Executor proposals that change the data model or the API contract go to the user first.
- Linear text in English. Keep context lean: read diffs, not the repo.
- Env: conda env `baidget` (`environment.yml`), not uv.
- Deploy (Cloud Run, IAM, secrets) is DevOps work: not ours. We hand over Dockerfile, env list, rules, indexes.
- Final deliverable: summary, deviations, open questions, "future work" (family groups, e-mail import, bulk/async scan, speech-to-text, multi-currency, cron, offline sync, budgets).
