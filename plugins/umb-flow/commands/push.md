---
description: Push commits to remote repository
allowed-tools: Bash
---

## Context

You are helping the user push their commits to the remote repository.

## Your Task

Push commits by following these steps:

### Step 1: Gather Information

Run these commands in parallel:

1. `git status -sb` - Check branch and tracking status
2. `git log @{u}..HEAD --oneline 2>/dev/null || git log --oneline -5` - See commits to be pushed

### Step 2: Check Prerequisites

1. **Uncommitted changes?** - Warn if there are uncommitted changes (they won't be pushed)
2. **Upstream set?** - If no upstream tracking branch, use `git push -u origin <branch>`
3. **Commits to push?** - If no commits ahead, inform the user there's nothing to push

### Step 3: Push

```bash
git push
```

Or if no upstream is set:

```bash
git push -u origin <branch-name>
```

### Step 4: Verify

Run `git status` to confirm the push succeeded.

## Important Notes

- NEVER use `--force` or `--force-with-lease` unless explicitly requested
- NEVER push to a protected branch without user confirmation
- If push fails due to remote changes, suggest `git pull --rebase` first
