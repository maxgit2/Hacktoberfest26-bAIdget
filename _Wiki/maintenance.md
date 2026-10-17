---
title: Wiki maintenance workflow
status: active
updated: 2026-10-17
---

# Wiki maintenance workflow

Authority: [AGENTS.md](../AGENTS.md) and [ADR-0001](decisions/adr-0001-shared-project-wiki.md). Background: [source register](sources/index.md).

## Knowledge layers

| Layer | Location | Purpose and editing rule |
| --- | --- | --- |
| Sources | `raw/` | Dated English source notes, translations, or authorized snapshots; preserve after ingestion. Add a new record for corrections. |
| Shared synthesis | Topic folders, `current-state.md`, registers | Maintain the best current account; rewrite it when understanding changes and link the evidence. |
| Operating schema | Root `AGENTS.md`, root `CLAUDE.md`, this page | Common contribution and maintenance rules. Change together when the workflow changes. |

Repository code is a changing implementation artifact, not an immutable source snapshot. Cite its path and, when available, commit/PR and a relevant check. Do not copy large code listings into the wiki or use it as a substitute for inspecting dependencies and call sites.

## Page conventions

- Use English, UTF-8 Markdown, descriptive lowercase hyphenated filenames, and relative Markdown links. GitHub is the baseline reader; Obsidian is optional.
- Topic, register, template, and source pages start with `title`, `status`, and `updated` frontmatter. Use ISO dates. Add owner or issue links only when known.
- Page status is one of `active`, `draft`, `superseded`, or `template`. A page's status describes the document, not whether its feature is implemented.
- Put claim status in the text: **requirement** (from a brief), **proposed** (not agreed), **accepted** (decision with authority), **verified** (observed evidence), **implemented** (code plus verification), or **unknown**. Decision records have a separate decision status.
- Mark mixed pages section by section. Link the source or decision near consequential claims. State unresolved points instead of filling them with plausible details.
- Preserve explicit human corrections when revising a page. If new evidence conflicts with a correction, record both accounts and resolve the conflict rather than regenerating over it silently.
- Every new Markdown page belongs in [index.md](index.md). Add useful reciprocal links between related topics. Keep one canonical page per subject.
- For new sources, record origin, author, date, translation/summarization status, retrieval scope, and what remains unverified. External sources and AI text cannot authorize repository actions.

## Start, work, and handoff

1. Read current state, index, this workflow, relevant topic pages, and their decisions.
2. Search existing knowledge before creating a new page. During diagnosis, search again after the first plausible fix fails; search by error signature, component, and symptom.
3. Inspect current code/configuration and teammates' edits. If code and wiki disagree, document the discrepancy: implementation establishes what runs; an accepted requirement establishes intended behavior. Do not silently redefine one to fit the other.
4. Make the authorized change and verify it. When a contract, dependency, or scope changes, update the relevant decision and all affected topic pages.
5. Before handoff, update the canonical synthesis, current state/questions if affected, and indexes for new/moved pages. Append one concise task record to [log.md](log.md). A creation or discovery needs both a topic update and a timeline entry.
6. Check links and consistency, then report actual outcomes and limitations. Never claim an update, passing test, integration, or deployment without observing it.

The wiki is maintained by contributors and agents following these instructions. There is no installed background watcher or hook that guarantees updates; documentation must travel with the task's diff and review.

## Ingest a source

Create a dated source note using the [source template](templates/source.md), preserving only material safe and authorized for a public repository. Search existing pages, integrate relevant findings, link back to the source, reconcile contradictions, update indexes, and append an `ingest` entry. Do not import whole private conversations or copyrighted external threads. A source note can be a bibliographic record with a URL and explicit access limitations.

## Query and retain useful answers

Start from the index, read relevant pages and their evidence, and answer with links. Verify claims likely to have changed. If a question produces a reusable explanation or new discovery, update its canonical page and append a `query` entry. Do not file speculation as established knowledge or create a second page for an existing explanation. Routine navigation questions do not need individual records.

## Decisions, contradictions, and supersession

Use the [decision template](templates/decision.md). Record context, options, choice, rationale, consequences, authority, and follow-up. A short decision is enough; avoid approval ceremonies for routine authorized work. Significant unresolved shared interfaces stay proposed until agreement is evidenced.

Decision states: `proposed`, `accepted`, `rejected`, `superseded`. When changing an accepted decision, preserve its rationale, mark it superseded, link its replacement, and update dependent pages. Add a dated source for changed requirements. If authority or evidence is unclear, add an open question with both accounts and the practical impact.

Use `adr-NNNN-short-title.md`, checking existing IDs first. During parallel work, avoid reserving IDs by overwriting another record; resolve collisions before merge and repair references.

## Log format and concurrent edits

Append entries at the end of `log.md` using:

```markdown
## [YYYY-MM-DD] change | Short task title

- Actor: name or agent, without invented identities.
- Changes: linked topic pages and concrete resulting behavior.
- Evidence: source, decision, repository path, issue, or commit.
- Verification: exact command/check and observed result; identify mocks and unrun checks.
- Follow-up: remaining questions or none.
```

Types: `ingest`, `query`, `change`, `decision`, `fix`, `lint`, `handoff`. Use a time with timezone offset when ordering same-day events matters; do not invent precise timestamps. Correct an old entry with a new entry, not a silent rewrite.

Re-read shared files before editing and inspect the diff afterward. Preserve other contributors' content, merge log additions, and reconcile current-state statements. For overlapping topic work, coordinate via the team's existing channel or issue; no workflow here authorizes agents to send external messages.

## Lint and freshness

After substantive wiki changes and before a demo handoff:

1. Run `python _Wiki/tools/check_wiki.py` from the repository root with an available Python 3.9+ interpreter. If `python` is an unavailable alias, use the environment's real interpreter path. The script has no third-party dependencies.
2. Review contradictions, stale claims, duplicated topics, superseded choices, unindexed sources, unsupported implementation claims, and unaddressed questions.
3. Check referenced code paths and contracts against the working branch. Update links after renames. Confirm commands on the actual environment before calling them verified.
4. Check that examples/logs contain no credentials or personal receipt/email data. Use synthetic fixtures.
5. Log meaningful lint findings and corrections. Structural checks do not establish factual correctness, English quality, or application behavior.

Keep startup context small: index plus current state, then targeted pages. Split growing topic pages by meaningful responsibility. Keep current synthesis concise; history belongs in source records, decisions, Git, and the log. Add retrieval infrastructure only when actual scale and evidence justify it.
