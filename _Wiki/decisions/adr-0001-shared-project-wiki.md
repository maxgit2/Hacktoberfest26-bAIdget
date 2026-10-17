---
title: ADR-0001 Shared project wiki
status: active
updated: 2026-10-17
---

# ADR-0001: Shared project wiki and agent workflow

- Decision status: **accepted**.
- Date: 2026-10-17.
- Authority: project initiator's explicit bootstrap request, recorded in the [initial brief](../raw/2026-10-17-project-brief.md).

## Context and choice

Several developers, designers, and AI agents need a common technical understanding during a rapidly evolving one-day hackathon. The user requests a wiki inspired by Karpathy's pattern and continuous capture of work, discoveries, problems, and solutions.

Maintain the shared wiki under `_Wiki`, with English documentation and code comments. Provide conventional root `AGENTS.md` and `CLAUDE.md` entry points that share a single policy. Keep sources, current synthesis, decisions, lessons, and chronological activity distinct and linked. The concrete file layout and lightweight templates are this bootstrap's implementation of the requested workflow.

## Alternatives and rationale

Chat history or separate agent notes fragment knowledge across contributors. A large documentation service or retrieval platform would require additional setup during the hackathon. Repository Markdown provides a reviewable, accessible starting point alongside the code.

## Consequences

Every implementation/discovery/fix task includes proportionate wiki maintenance and a log entry. Preserve sources and superseded reasoning; update current summaries instead of accumulating conflicting accounts. Humans retain authority over scope and consequential decisions. No automatic hook or external service is installed; compliance depends on contributor behavior and review.

See [maintenance](../maintenance.md), [index](../index.md), and [agent policy](../../AGENTS.md). This choice can evolve through a replacement decision with explicit links.
