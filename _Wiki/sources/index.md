---
title: Source register and methodology
status: active
updated: 2026-10-17
---

# Source register and methodology

## Sources

| ID | Record | Role |
| --- | --- | --- |
| SRC-001 | [Initial project brief](../raw/2026-10-17-project-brief.md) | Product requirements and the explicit English/wiki instructions; normalized English source note |
| SRC-002 | [Karpathy reference](../raw/2026-10-17-karpathy-reference.md) | External methodological inspiration; bibliographic pointer with retrieval limitations |
| SRC-003 | [Updated base specification](../raw/2026-10-17-updated-specification.md) | Initiator's complete pasted update translated/transcribed into English; current requirements/fields/flows/milestones/stack, superseding changed parts of SRC-001 |

SRC-001 and SRC-002 remain immutable historical records. SRC-003 is synthesized in [scope](../product/scope.md), [flows](../product/user-flows.md), [model](../engineering/domain-model.md), [contracts](../engineering/contracts.md), [architecture](../engineering/architecture.md), [AI/data](../engineering/ai-and-data.md), and [ADR-0004](../decisions/adr-0004-updated-product-baseline.md). Google sign-in and camera-first assumptions from SRC-001 no longer define the current baseline; camera scope, category editing/chart timing, fingerprint, and monetary/recurrence details remain explicit [questions](../open-questions.md). Its linked AgentMail homepage and OCR ranking were opened for reference intake only; evaluation limits are in AI/data. No external benchmark or provider claim became a project requirement.

Repository inspection is separately recorded in [current state](../current-state.md) and [log](../log.md). The Flutter integration observations are tied to fetched `origin/main` commit `055275e513a6690489d8712e20011913f42ec555` on 2026-10-17, then inspected locally. They do not guarantee the contents of later remote commits; repository implementation evidence is kept distinct from the immutable brief/reference records above.

## Reference interpretation

[Karpathy's idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) separates source material, maintained synthesis, and operating instructions, with ingest/query/lint operations and distinct index/history files.

Discussion contributions informed the adaptation:

| Discussion point | Reference | Project response |
| --- | --- | --- |
| Team writes and conflicting knowledge | [huachen-wang](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f#gistcomment-6316883) | Merge shared-file edits carefully and preserve unresolved contradictions |
| Unsupported certainty and stale claims | [antondzi-legacy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f#gistcomment-6285217) | Require evidence and separate proposals from implementation |
| Operational evidence can contradict documentation | [pollockchris083-arch](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f#gistcomment-6312158) | Inspect running behavior and record discrepancies |
| Lookup must happen during work | [orcosto-lab](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f#gistcomment-6381418) | Search lessons after the first unsuccessful diagnosis/fix |
| Duplicate concepts and summaries | [HagaiHen](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f#gistcomment-6414983) | Extend canonical pages and maintain current summaries |
| Structural checks have limits | [alfabarisl18-ops](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f#gistcomment-6406888) | Use a local checker plus factual review |

These comments are experience reports or arguments, not validated benchmarks or project requirements. The adaptation and its tradeoffs are the team's reviewable documentation; no advertised tool is installed or endorsed.

## Review coverage

The main gist was read in full. The browser loaded 780 comment entries, from `gistcomment-6089247` through `gistcomment-6431021`, and still exposed an earlier-comments control. Batch screening used excerpts, with the six comments cited above read in full. Some batch output was truncated. A complete reading of every comment was **not achieved or verified**: further pagination encountered browser timeouts and a detached connection, and GitHub API retrieval failed as well. This explicitly falls short of the requested all-comments review.

Follow-up: when access works again, retrieve and read the remaining older entries and the full text of entries only screened so far, then add a dated source/review record and reconcile any material findings. Do not infer that loading an entry means its complete text was read. External linked repositories, papers, demos, and promotional feature claims are outside this source review. See the bootstrap [verification entry](../log.md).

## Future intake

Use the [source template](../templates/source.md) for new briefs, design handoffs, meeting outcomes, or external references. Keep raw notes immutable, integrate conclusions into the canonical topic, and record source-to-topic links here. A source record that has not yet been synthesized should be explicitly marked pending in this register. Source trust and agent instructions are distinct; see [maintenance](../maintenance.md).
