---
description: Create a pull request following project conventions
allowed-tools: Bash, Read, Glob, Grep
---

## Context

You are helping the user create a well-structured pull request using the GitHub CLI (`gh`).

## Your Task

Create a pull request by following these steps:

### Step 1: Gather Information

Run these commands in parallel to understand the current state:

1. `git status` - Check for uncommitted changes and current branch
2. `git branch --show-current` - Get current branch name
3. `git remote -v` - Check remote configuration
4. Identify target branch and protected branches:
   - `gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null` - Get default branch
   - `gh api repos/{owner}/{repo}/branches --jq '.[] | select(.protected) | .name' 2>/dev/null` - Get GitHub protected branches
   - Check for common development branches: `dev`, `develop`, `development`
   - If `dev`/`develop` exists, that's likely the PR target (gitflow). Otherwise use the default branch.

### Step 2: Check for PR Conventions

Look for PR guidelines in these locations (in priority order):

1. **CLAUDE.md / .claude/docs/** - Check for PR description section or guidelines
2. **CONTRIBUTING.md** - Often contains PR format requirements
3. **.github/pull_request_template.md** or **.github/PULL_REQUEST_TEMPLATE.md** - PR template
4. **.github/PULL_REQUEST_TEMPLATE/** - Directory of multiple templates
5. **Recent merged PRs** - `gh pr list --state merged --limit 5` to infer style

Use the first convention/template found. If a specific format is defined, follow it exactly.

### Step 3: Check Prerequisites

Before creating the PR:

1. **Uncommitted changes?** - Warn the user if there are uncommitted changes
2. **Branch pushed?** - Check if branch is pushed to remote with `git status -sb`
3. **On protected branch?** - Warn if trying to create PR from a protected branch

If the branch isn't pushed:
```bash
git push -u origin <branch-name>
```

### Step 4: Analyze Changes

Get the commits and changes for this PR:

```bash
git log --oneline origin/<target-branch>..HEAD
git diff origin/<target-branch>...HEAD --stat
```

Review to understand:

1. **What changed** - Files modified, added, deleted
2. **Why it changed** - Purpose of the changes based on commit messages and code
3. **Impact** - What areas of the codebase are affected
4. **Testing needed** - What should be tested to verify the changes

### Step 5: Create PR Title

Use the convention discovered in Step 2. If none was found, create a clear title that:
- Summarises the change concisely
- Matches the style of recent PRs in the project
- Stays under 72 characters

### Step 6: Create PR Body

Use the template/convention discovered in Step 2.

If no template was found, write a clear PR description that:
- Summarises what the PR does
- Explains why the change was made
- Lists key changes
- Describes how to test
- Matches the style of recent PRs in the project

### Step 7: Execute PR Creation

Use a HEREDOC to preserve formatting:

```bash
gh pr create --base <target-branch> --title "<title>" --body "$(cat <<'EOF'
<PR body following project convention or template>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 8: Return PR URL

After creation, display the PR URL so the user can review it.

## Important Notes

- NEVER force push or modify git history
- NEVER create PRs from protected branches
- If `gh` is not installed, inform the user to install it from https://cli.github.com/
- If not authenticated, inform user to run: `gh auth login`
- Ask for clarification if the purpose of the changes is unclear
- Include any linked issues using `Fixes #123` or `Closes #123` syntax if applicable
