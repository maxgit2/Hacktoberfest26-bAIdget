---
title: Git commit requires an explicit author identity
status: active
updated: 2026-10-17
---

# Git commit requires an explicit author identity

## Symptom and verified cause

During the documentation publication task, `git commit` failed with `Author identity unknown` and `fatal: unable to auto-detect email address`. `git config --show-origin --get user.name` and the corresponding `user.email` lookup returned no values. Fetch access had succeeded; missing commit metadata was the observed failure, not a GitHub authentication failure.

## Resolution

Verify the intended author's identity before assigning it. In this task, the connected GitHub profile matched the initial repository commit's author/login and public noreply address. Reused that existing identity through command-local `-c user.name=... -c user.email=...` arguments, without changing local/global Git settings or using another contributor's identity.

```sh
git show -s --format='%an <%ae>' ec8a3b5
git -c user.name=VERIFIED_NAME -c user.email=VERIFIED_EMAIL var GIT_AUTHOR_IDENT
git -c user.name=VERIFIED_NAME -c user.email=VERIFIED_EMAIL commit -m "Commit message"
```

Replace placeholders with verified values; an arbitrary earlier author's identity is not authorization to reuse it. The command-local `var GIT_AUTHOR_IDENT` check successfully resolved the verified identity here. Commit/push results are checked separately during the publication handoff; author metadata does not establish remote write access. Future commits need the same command-local arguments or deliberately configured repository settings.

Evidence and task context: [activity log](../log.md), [development guide](../development/contributing.md).
