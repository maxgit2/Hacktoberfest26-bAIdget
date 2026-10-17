---
title: Product scope
status: active
updated: 2026-10-17
---

# Product scope

Current authority: [updated specification, SRC-003](../raw/2026-10-17-updated-specification.md), adopted in [ADR-0004](../decisions/adr-0004-updated-product-baseline.md). The [initial brief](../raw/2026-10-17-project-brief.md) is historical. Requirements below are not implemented: source inspection at `055275e` still shows only the [Flutter counter scaffold](../decisions/adr-0003-flutter-scaffold.md).

## Intended experience

bAIdget is an Android app for recording/classifying expenses through receipt images, manual input, and forwarded payment emails, then reviewing spending by period/category. Personal use remains the working scope, but SRC-003 explicitly questions “for one person”; family groups are optional and sharing is undefined (Q-16).

## Current requirements

Requirement IDs are retained across revisions; updated wording does not imply completion.

| ID | Capability | Updated requirement | Milestone / status |
| --- | --- | --- | --- |
| REQ-01 | Identity | Automatic auth through a smartphone ID/fingerprint stable across logins from that smartphone; replaces Google sign-in | 1.0; mechanism open, absent from scaffold |
| REQ-02 | Category setup | Select four/six-category starting templates or create from scratch; narrative permits rename/add/remove | Selection 1.0; editing listed in 2.0; timing ambiguity Q-10 |
| REQ-03 | Receipt image | Select an existing gallery image; backend OCR reads/classifies using user categories; user reviews/corrects | 1.0; additional camera capture unclear, Q-15 |
| REQ-04 | Manual expense | Always available; same form as OCR review; single/recurring input mentioned | Manual entry 1.0; recurrence semantics open |
| REQ-05 | Email import | Forward to an address generated during user creation; backend periodically synchronizes messages | 3.0; AgentMail to evaluate |
| REQ-06 | Summaries | Weekly/monthly/yearly/category views; category pie chart; current-versus-previous-period comparison; optional category granularity | Summaries 2.0; chart variants 5.0; timing/defaults open |
| REQ-07 | Home | Scan image, import expense, expense summary actions | No separate milestone assigned; navigation details open |
| REQ-08 | Expense fields | Supplied owner/date/category/type/amount/currency/metadata fields | [Domain model](../engineering/domain-model.md); API/validation not final |
| REQ-09 | Budgets/alerts | Create budgets; notify at 25%, 50%, 75%, 100%; per-category alerts optional | 4.0; budget/notification semantics open |

Euro is the default currency; its code/encoding remains open. Category labels, app locale/language, hierarchy, and OCR acceptance criteria are unspecified. Four/six describe starting template sizes, not limits.

## Source milestone sequence

This replaces the wiki's earlier suggested demo ordering. The initiator supplied these labels and contents; they are planned scope, not shipped releases, deadlines, or a guarantee that all stages fit the hackathon.

| Milestone | Planned scope | Repository evidence |
| --- | --- | --- |
| 0.1 | Backend infrastructure, details to define | No backend scaffold/configuration |
| 1.0 | Automatic device identity; template selection; receipt scanning and gallery import; manual entry | Only unrelated counter demo exists |
| 2.0 | Server deployment; category editing after template; summaries | Not implemented |
| 3.0 | Forwarded-email import | Not implemented |
| 4.0 | Budget creation; alerts at 25%, 50%, 75%, 100% | Not implemented |
| 5.0 | Different chart types in summaries | Not implemented |

The detailed scan flow starts in the gallery while 1.0 separately lists scanning and gallery import. The narrative permits onboarding category edits while 2.0 lists editing. Chart examples appear in the narrative while variants are in 5.0. Preserve these tensions until [Q-10, Q-15, Q-17](../open-questions.md) are resolved. Address generation is described at user creation although email import lands in 3.0; provisioning timing is Q-06.

## Optional or unscheduled capabilities

Family groups, speech-to-text, additional currencies, a cron job for `concurrent` records, automatic fixed expenses, optional category granularity, and per-category budget alerts remain suggestions. Budgets/threshold notifications are now explicit 4.0 scope. Recurring input is in the core narrative; automatic occurrence generation is separately optional without a milestone. Storing a recurring definition does not imply a running scheduler.

## Candidate acceptance scenarios

These are proposed cases, not executed tests/finalized contracts; see [flows](user-flows.md), [contracts](../engineering/contracts.md), and [AI/data](../engineering/ai-and-data.md).

- Repeated access from the same smartphone reaches the same owner under the agreed auth mechanism; spoofing an ID/owner does not grant access.
- Template/from-scratch setup works; editing follows the resolved milestone boundary and returning users retain categories.
- A gallery image yields an editable draft; cancellation/failure preserves a manual path; confirmed corrections are saved.
- Manual input uses the same form without OCR; required fields and missing amounts follow agreed validation/accounting rules.
- Summaries/comparisons agree with saved records, period boundaries, optional amounts, deleted records, currencies, and recurrence rules.
- Reprocessing forwarded email avoids duplicates and respects recipient ownership/review rules.
- Budget crossings produce the agreed alerts with defined reset, repeated-processing, category, edit, and deletion behavior.

All expense features, service integrations, platform builds, and these scenarios remain unverified in application code.
