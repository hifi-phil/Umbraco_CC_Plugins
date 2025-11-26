---
description: Create a structured git commit following project conventions
allowed-tools: Bash, Read, Glob, Grep
---

## Context

You are helping the user create a well-structured git commit following the project's commit message conventions.

## Your Task

Create a git commit by following these steps:

### Step 1: Gather Information

Run these commands in parallel to understand the current state:

1. `git status` - See all staged/unstaged changes and untracked files
2. `git diff --cached` - See staged changes (what will be committed)
3. `git diff` - See unstaged changes
4. `git branch --show-current` - Get current branch name
5. Identify protected branches:
   - `gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null` - Get default branch
   - `gh api repos/{owner}/{repo}/branches --jq '.[] | select(.protected) | .name' 2>/dev/null` - Get GitHub protected branches
   - Also consider common protected branches: `main`, `master`, `dev`, `develop`, `release/*`

### Step 2: Check for Commit Message Conventions

Look for commit message guidelines in these locations (in priority order):

1. **CLAUDE.md / .claude/docs/** - Check for commit message section or guidelines
2. **CONTRIBUTING.md** - Often contains commit message format
3. **.github/COMMIT_CONVENTION.md** - Dedicated commit convention file
4. **.gitmessage** or **.git-commit-template** - Git commit template
5. **package.json** - Check for commitlint config or commitizen config
6. **.commitlintrc** / **commitlint.config.js** - Commitlint rules
7. **git log --oneline -5** - Infer style from recent commits

Use the first convention found. If a specific format is defined, follow it exactly. Only fall back to conventional commits if no project-specific convention exists.

### Step 3: Check Branch

Check if the current branch is a protected branch (from Step 1). If it is:

1. **Stop and warn the user** - Committing directly to protected branches is not recommended
2. **Suggest using `/branch`** - Tell the user to run `/branch` to create a new branch first
3. **Ask how to proceed**:
   - Create a new branch now (use `/branch`)
   - Continue committing anyway (if they confirm)

Only proceed with the commit if the user explicitly confirms, or if they're already on a non-protected branch.

### Step 4: Analyze Changes

Based on the diff output, understand:

1. **What changed** - Files modified, functions added/removed, etc.
2. **Why it changed** - The purpose behind the changes
3. **Scope** - What area of the codebase is affected
4. **Impact** - Does this break existing functionality?

### Step 5: Check Changes Match Branch Purpose

Compare what the changes are about vs what the branch name suggests:

- Parse the branch name to understand its purpose (e.g., `feature/user-authentication` is about user auth)
- Look at the actual changes - what feature/area do they relate to?

If the changes don't seem related to the branch name:
1. **Warn the user** - e.g., "You're on `feature/user-auth` but these changes appear to be about payment processing"
2. **Ask if they're on the correct branch** - They may have meant to branch from main/dev first
3. **Offer options**:
   - Continue anyway (if intentional)
   - Use `/branch` to create a new branch from the default branch for this work

### Step 6: Stage Files (if needed)

If there are unstaged changes the user wants to commit:
- Ask which files to stage
- Run `git add <files>` for the specified files

### Step 7: Create Commit Message

Use the commit message convention discovered in Step 2.

If a project convention was found, follow it exactly.

If no convention was found, write a clear commit message that:
- Has a concise subject line (under 72 characters)
- Uses imperative mood ("add" not "added")
- Explains the "why" in the body if the change isn't obvious
- Matches the style of recent commits in the project

### Step 8: Execute Commit

Run the commit with a HEREDOC to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
<subject line>

<body if needed>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 9: Verify

Run `git status` and `git log -1` to confirm the commit was created successfully.

### Step 10: Offer to Push

After a successful commit, ask the user if they want to push:

- If yes, push to remote (use `git push -u origin <branch>` if no upstream is set)
- If no, inform them they can use `/push` later

## Important Notes

- NEVER use `--amend` unless explicitly requested
- NEVER push unless explicitly requested
- NEVER skip hooks unless explicitly requested
- If pre-commit hooks modify files, you may retry the commit ONCE
- Do NOT commit files that look like secrets (.env, credentials, tokens)
- Ask the user for clarification if the change type is ambiguous
