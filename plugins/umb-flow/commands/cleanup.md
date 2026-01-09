---
description: Clean up git worktrees
allowed-tools: Bash
---

## Context

You are helping the user clean up git worktrees. This command manages worktrees created by the `/umb-flow:branch` command when using worktree mode.

**Reference the `git-worktree` skill for worktree operations.**

## Your Task

Clean up worktrees by following these steps:

### Step 1: List Worktrees

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list
```

### Step 2: Clean Up

If there are inactive worktrees, run the cleanup:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

The script will:
1. List all inactive worktrees
2. Ask for confirmation before removing
3. Skip the currently active worktree
4. Clean up empty directories

## Important Notes

- NEVER remove worktrees without user confirmation
- The script won't remove the current worktree (must cd out first)
- Worktrees with uncommitted changes require `--force` to remove
