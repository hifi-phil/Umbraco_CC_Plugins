---
description: Create and set up a new branch
argument-hint: "<branch-name>"
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
---

## Context

You are helping the user create and set up a new branch for development. The branch can be created either as a traditional branch (switching the current worktree) or as a separate git worktree for parallel development.

**Reference the `git-worktree` skill for worktree operations.**

## Your Task

Create a new branch by following these steps:

### Step 1: Parse Arguments

- Branch name: `$ARGUMENTS`
- If no argument provided, ask the user for a branch name

### Step 2: Gather Current State

Run these commands in parallel:

1. `git status` - Check for uncommitted changes
2. `git branch --show-current` - Get current branch
3. `git remote -v` - Check remote configuration
4. `bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list` - Check existing worktrees
5. Identify the base branch to branch from:
   - `gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null` - Get default branch
   - `gh api repos/{owner}/{repo}/branches --jq '.[] | select(.protected) | .name' 2>/dev/null` - Get GitHub protected branches
   - Check for common development branches: `dev`, `develop`, `development`
   - If a `dev`/`develop` branch exists, use that as the base (gitflow). Otherwise use the default branch.

### Step 3: Check Prerequisites

Before creating the branch:

1. **Currently on a feature branch?** - If the current branch is not the base branch (e.g., you're on `feature/user-auth`), warn the user:
   - "You're currently on `feature/user-auth`. New branches are usually created from `dev`/`main`."
   - Ask if they want to:
     - Branch from the base branch (recommended)
     - Branch from the current branch (if intentional, e.g., sub-feature)

2. **Uncommitted changes?** - Note if there are uncommitted changes. These will come along to the new branch automatically, which is usually the desired behaviour (user wants to commit them to the new branch).

3. **Valid branch name?** - Ensure the branch name:
   - Contains no spaces (use hyphens)
   - Is lowercase
   - Follows a sensible pattern

### Step 4: Ask About Worktree Mode

Ask the user how they want to work:

1. **New branch (switch to it)** - Traditional branch, switches current working directory
2. **Worktree (parallel development)** - Creates isolated worktree in `.worktrees/` folder

If user chooses worktree, use the worktree manager script:
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create <branch-name> <base-branch>
```

Then skip to Step 9 (Confirm Setup) - the script handles everything else.

### Step 5: Format Branch Name

If not already formatted, suggest a branch name based on the work type:

```
<type>/<description>
```

Common prefixes:
- `feature/` - New feature
- `fix/` - Bug fix
- `hotfix/` - Urgent production fix
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions
- `chore/` - Maintenance

Examples:
- `feature/user-authentication`
- `fix/login-redirect-loop`
- `chore/update-dependencies`

Don't force a prefix if the user provides a clear branch name without one.

### Step 6: Prepare Source Branch

Based on the user's choice in Step 3:

**If branching from the base branch (default):**
```bash
git fetch origin
git checkout <base-branch>
git pull origin <base-branch>
```

**If branching from the current branch (sub-feature):**
```bash
git fetch origin
# Stay on current branch, just ensure it's up to date with remote if it has one
git pull origin <current-branch> 2>/dev/null || true
```

### Step 7: Create Branch

```bash
git checkout -b <branch-name>
```

### Step 8: Push Branch (Optional)

Ask the user if they want to push the branch to remote now:

```bash
git push -u origin <branch-name>
```

### Step 9: Confirm Setup

Display a summary:

```
✓ Branch created: <branch-name>
✓ Based on: <source-branch> (up to date)
✓ Remote tracking: <status>

Ready to start development!
```

## Important Notes

- NEVER delete or force-modify existing branches
- Uncommitted changes will carry over to the new branch - this is expected
- If the branch name already exists, warn the user and ask how to proceed
- Always fetch latest before branching to ensure up-to-date base
- If `gh` is not available, check for `dev`/`develop` branches first, then fall back to `main`
