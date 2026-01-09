---
name: git-worktree
description: This skill manages Git worktrees for isolated parallel development. It handles creating, listing, switching, and cleaning up worktrees with a simple interactive interface, following KISS principles.
---

# Git Worktree Manager

This skill provides a unified interface for managing Git worktrees across your development workflow. Whether you're reviewing PRs in isolation or working on features in parallel, this skill handles all the complexity.

## What This Skill Does

- **Create worktrees** from main branch with clear branch names
- **List worktrees** with current status
- **Switch between worktrees** for parallel work
- **Clean up completed worktrees** automatically
- **Interactive confirmations** at each step
- **Automatic .gitignore management** for worktree directory
- **Automatic .env file copying** from main repo to new worktrees

## CRITICAL: Always Use the Manager Script

**NEVER call `git worktree add` directly.** Always use the `worktree-manager.sh` script.

The script handles critical setup that raw git commands don't:
1. Copies `.env`, `.env.local`, `.env.test`, etc. from main repo
2. Ensures `.worktrees` is in `.gitignore`
3. Creates consistent directory structure

```bash
# ✅ CORRECT - Always use the script
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-name

# ❌ WRONG - Never do this directly
git worktree add .worktrees/feature-name -b feature-name main
```

## When to Use This Skill

Use this skill in these scenarios:

1. **Branch Creation (`/umb-flow:branch`)**: When creating a new branch, offers choice between traditional branch or worktree
2. **Parallel Development**: When working on multiple features simultaneously
3. **Cleanup (`/umb-flow:cleanup`)**: After completing work in a worktree

## How to Use

### In umb-flow Commands

The skill is automatically called from `/umb-flow:branch` and `/umb-flow:cleanup` commands:

```
# /umb-flow:branch asks: new branch (switch) or worktree (parallel)?
# /umb-flow:cleanup lists and removes inactive worktrees
```

### Manual Usage

You can also invoke the skill directly from bash:

```bash
# Create a new worktree (copies .env files automatically)
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-login

# List all worktrees
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list

# Switch to a worktree
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch feature-login

# Copy .env files to an existing worktree (if they weren't copied)
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh copy-env feature-login

# Clean up completed worktrees
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

## Commands

### `create <branch-name> [from-branch]`

Creates a new worktree with the given branch name.

**Options:**
- `branch-name` (required): The name for the new branch and worktree
- `from-branch` (optional): Base branch to create from (defaults to `main`)

**Example:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-login
```

**What happens:**
1. Checks if worktree already exists
2. Updates the base branch from remote
3. Creates new worktree and branch
4. **Copies all .env files from main repo** (.env, .env.local, .env.test, etc.)
5. Shows path for cd-ing to the worktree

### `list` or `ls`

Lists all available worktrees with their branches and current status.

**Example:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list
```

**Output shows:**
- Worktree name
- Branch name
- Which is current (marked with ✓)
- Main repo status

### `switch <name>` or `go <name>`

Switches to an existing worktree and cd's into it.

**Example:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch feature-login
```

**Optional:**
- If name not provided, lists available worktrees and prompts for selection

### `cleanup` or `clean`

Interactively cleans up inactive worktrees with confirmation.

**Example:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

**What happens:**
1. Lists all inactive worktrees
2. Asks for confirmation
3. Removes selected worktrees
4. Cleans up empty directories

## Workflow Examples

### Creating a Feature Branch with Worktree

```bash
# User runs /umb-flow:branch feature-login
# Command asks: "How do you want to work?"
# User chooses: "Worktree (parallel development)"

# Script runs (copies .env files automatically):
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-login

# You're now in isolated worktree with all env vars
cd .worktrees/feature-login

# After work is complete, return to main and cleanup:
cd ../..
# Run /umb-flow:cleanup
```

### Parallel Feature Development

```bash
# Create first feature via /umb-flow:branch (choose worktree):
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-login

# Later, create second feature via /umb-flow:branch (choose worktree):
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-notifications

# List what you have:
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list

# Switch between them as needed:
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch feature-login

# When done, run /umb-flow:cleanup from main repo:
cd /path/to/main/repo
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

## Key Design Principles

### KISS (Keep It Simple, Stupid)

- **One manager script** handles all worktree operations
- **Simple commands** with sensible defaults
- **Interactive prompts** prevent accidental operations
- **Clear naming** using branch names directly

### Opinionated Defaults

- Worktrees always created from **main** (unless specified)
- Worktrees stored in **.worktrees/** directory
- Branch name becomes worktree name
- **.gitignore** automatically managed

### Safety First

- **Confirms before creating** worktrees
- **Confirms before cleanup** to prevent accidental removal
- **Won't remove current worktree**
- **Clear error messages** for issues

## Integration with umb-flow Commands

### `/umb-flow:branch`

The branch command integrates worktree support at Step 4:

```
1. User runs: /umb-flow:branch feature-name
2. Command gathers state (current branch, uncommitted changes, existing worktrees)
3. Checks prerequisites (base branch, valid name)
4. Asks: "How do you want to work?
   1. New branch (switch to it) - Traditional branch
   2. Worktree (parallel development) - Isolated in .worktrees/"

5. If worktree chosen → calls worktree-manager.sh create
6. If traditional → creates branch with git checkout -b
```

### `/umb-flow:cleanup`

Dedicated command for worktree cleanup:

```
1. Lists all worktrees via worktree-manager.sh list
2. Runs worktree-manager.sh cleanup
3. Confirms before removing each inactive worktree
```

## Troubleshooting

### "Worktree already exists"

If you see this, the script will ask if you want to switch to it instead.

### "Cannot remove worktree: it is the current worktree"

Switch out of the worktree first (to main repo), then cleanup:

```bash
cd $(git rev-parse --show-toplevel)
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

### Lost in a worktree?

See where you are:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list
```

### .env files missing in worktree?

If a worktree was created without .env files (e.g., via raw `git worktree add`), copy them:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh copy-env feature-name
```

Navigate back to main:

```bash
cd $(git rev-parse --show-toplevel)
```

## Technical Details

### Directory Structure

```
.worktrees/
├── feature-login/          # Worktree 1
│   ├── .git
│   ├── app/
│   └── ...
├── feature-notifications/  # Worktree 2
│   ├── .git
│   ├── app/
│   └── ...
└── ...

.gitignore (updated to include .worktrees)
```

### How It Works

- Uses `git worktree add` for isolated environments
- Each worktree has its own branch
- Changes in one worktree don't affect others
- Share git history with main repo
- Can push from any worktree

### Performance

- Worktrees are lightweight (just file system links)
- No repository duplication
- Shared git objects for efficiency
- Much faster than cloning or stashing/switching
