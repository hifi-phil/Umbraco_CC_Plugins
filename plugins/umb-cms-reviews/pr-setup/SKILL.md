---
name: pr-setup
description: Set up an Umbraco CMS pull request for local exploration. Checks out the PR into a git worktree, optionally installs a starter kit from the Umbraco Marketplace, builds the solution, and starts a running Umbraco instance — ready for manual exploration or automated testing with /pr-test. Use this skill when the user explicitly asks to set up, build, check out, or start a PR instance. Trigger phrases include "set up PR", "check out PR", "build PR", "start PR", "get PR running", "spin up PR", "get this PR ready". Do NOT use this skill when the user wants to test, verify, or validate a PR (use /pr-test instead) or when they want to see what PRs are available (use /pr-classify instead).
---

# PR Setup

You set up an Umbraco CMS pull request in an isolated worktree with a running instance, ready for the developer to explore manually or test with `/pr-test`.

## Arguments

Required: A PR number (e.g., `21887`)

## Overview

The setup follows this pipeline:
1. **Fetch PR info** — get the PR description and changed files
2. **Create worktree** — isolated checkout of the PR branch
3. **Choose starter kit** — ask the user which starter kit to install (or none)
4. **Configure unattended install** — no wizard, auto-creates database and admin user
5. **Build** — compile the solution (detect if frontend build needed)
6. **Start Umbraco** — run on a unique port

The instance is **left running** so the developer can explore it manually or run `/pr-test` for automated browser testing.

## Step 1: Fetch PR Info

```bash
gh pr view {PR_NUMBER} --repo umbraco/Umbraco-CMS --json number,title,body,headRefName,baseRefName,changedFiles,additions,deletions,labels
```

Read the PR body to understand what the PR does. See `references/pr-test-extraction.md` for how to parse the description structure.

Store a brief summary:
- **What the PR does** — one-sentence description
- **Changed areas** — which parts of the codebase are affected
- **Has test plan** — whether the PR description includes test steps (useful for suggesting `/pr-test` later)

## Step 2: Create Worktree

First, ensure `.claude/worktrees` is in `.gitignore` so worktree directories aren't accidentally committed:

```bash
grep -q '.claude/worktrees' .gitignore || echo '.claude/worktrees' >> .gitignore
```

Then create the worktree:

```bash
cd /Users/philw/Projects/Umbraco-CMS
git fetch origin pull/{PR_NUMBER}/head:pr-{PR_NUMBER}
git worktree add .claude/worktrees/pr-{PR_NUMBER} pr-{PR_NUMBER}
```

If the worktree already exists, ask the user if they want to reuse it or recreate it.

## Step 3: Choose and Install Starter Kit

Ask the user which starter kit to install. Only present packages that are **free**, **not themes**, and **compatible with the target Umbraco major version**.

### 3a: Get compatible starter kits

Run the script that fetches starter kits from the Umbraco Marketplace, checks each against NuGet for version compatibility, and filters out themes and incompatible packages. Results are cached for 24 hours.

```bash
/Users/philw/Projects/Umbraco-CMS/.claude/skills/pr-setup/scripts/get-compatible-starter-kits.sh {TARGET_MAJOR_VERSION}
```

Where `{TARGET_MAJOR_VERSION}` is the Umbraco major version (e.g., `17` for PRs targeting `main`). Read `version.json` in the repository root if needed.

The script returns a JSON array like:
```json
[
  {"packageId": "Clean", "title": "Clean Starter Kit for Umbraco", "version": "7.0.5"},
  {"packageId": "Umbraco.Community.Templates.UmBootstrap", "title": "Templates UmBootstrap", "version": "17.1.0"}
]
```

### 3b: Present choices to the user

Use `AskUserQuestion` to present each package from the script output as an option, plus **"None — no starter kit"** as the last option. Include the version in each option's description.

Recommended default: **Clean Starter Kit** (`Clean`) — it's lightweight, widely used, and provides blog content types, templates, sample content, and media out of the box.

### 3c: Install the selected starter kit

If the user selected a starter kit (not "None"):

```bash
cd /Users/philw/Projects/Umbraco-CMS/.claude/worktrees/pr-{PR_NUMBER}
dotnet add src/Umbraco.Web.UI/Umbraco.Web.UI.csproj package {PACKAGE_ID} --version {VERSION}
```

Where `{PACKAGE_ID}` and `{VERSION}` come from the NuGet lookup (e.g., `Clean` and `7.0.5`).

Starter kit package migrations run automatically during unattended install because `PackageMigrationsUnattended` defaults to `true`.

If the user selected **"None"**, skip this step entirely — Umbraco will start with an empty content tree.

## Step 4: Configure Unattended Install

Read `references/appsettings-template.md` for the full configuration template.

Create/overwrite `src/Umbraco.Web.UI/appsettings.Development.json` in the worktree with the unattended install configuration. The key settings are:
- SQLite connection string
- `InstallUnattended: true`
- Admin credentials (email: `admin@test.com`, password: `TestPassword1234!`)

Also ensure the data directory is clean:
```bash
rm -rf .claude/worktrees/pr-{PR_NUMBER}/src/Umbraco.Web.UI/umbraco/Data
```

## Step 5: Build

Read `references/build-detection.md` to determine if a frontend build is needed.

Check if the PR changes frontend files:
```bash
gh pr diff {PR_NUMBER} --repo umbraco/Umbraco-CMS --name-only | grep -c "src/Umbraco.Web.UI.Client/"
```

**Backend only (no frontend changes):**
```bash
cd /Users/philw/Projects/Umbraco-CMS/.claude/worktrees/pr-{PR_NUMBER}
dotnet build src/Umbraco.Web.UI/Umbraco.Web.UI.csproj -c Debug
```

**With frontend changes:**
```bash
cd /Users/philw/Projects/Umbraco-CMS/.claude/worktrees/pr-{PR_NUMBER}/src/Umbraco.Web.UI.Client
npm install
npm run build
cd /Users/philw/Projects/Umbraco-CMS/.claude/worktrees/pr-{PR_NUMBER}
dotnet build src/Umbraco.Web.UI/Umbraco.Web.UI.csproj -c Debug
```

If the build fails, report the error to the user and stop. The PR may have merge conflicts or dependency issues.

## Step 6: Start Umbraco

Calculate port: `PORT = 10000 + ({PR_NUMBER} % 10000)`

Before starting, check the port isn't already in use. If it is, see `references/port-management.md` for how to pick an alternative port or resolve the conflict.

```bash
# Check for port conflict first
lsof -ti:${PORT} 2>/dev/null && echo "WARNING: Port ${PORT} is in use!" || echo "Port ${PORT} is free"
```

```bash
cd /Users/philw/Projects/Umbraco-CMS/.claude/worktrees/pr-{PR_NUMBER}
dotnet run --project src/Umbraco.Web.UI --urls "http://localhost:{PORT}" --no-build &
```

Run this in the background. Then poll until ready:

```bash
for i in $(seq 1 60); do
  status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:{PORT}/umbraco" 2>/dev/null)
  if [ "$status" = "200" ] || [ "$status" = "302" ]; then
    echo "Umbraco is ready on port {PORT}"
    break
  fi
  echo "Waiting for Umbraco to start... (attempt $i/60)"
  sleep 3
done
```

If it doesn't become ready within 3 minutes, check the logs:
```bash
cat .claude/worktrees/pr-{PR_NUMBER}/src/Umbraco.Web.UI/umbraco/Logs/UmbracoTraceLog.*.json | tail -50
```

## Step 7: Report to User

Present this summary:

```
## PR #{NUMBER}: {TITLE}
**Branch:** {headRefName}
**Instance:** http://localhost:{PORT}/umbraco
**Login:** admin@test.com / TestPassword1234!
**Starter Kit:** {selected starter kit name, or "None"}
**Worktree:** .claude/worktrees/pr-{PR_NUMBER}

### PR Description Summary
{Brief summary of what the PR does and its test plan}

### What's Next?
- **Explore manually** — open the URL above in your browser
- **Run automated tests** — use `/pr-test {PR_NUMBER}` to verify the PR with browser automation
- **Clean up when done** — use `/pr-cleanup {PR_NUMBER}` to stop the instance and remove the worktree
```

## Important Notes

- **Leave the instance running** — the developer will either explore or run `/pr-test`
- **Report the port clearly** — `/pr-test` and `/pr-cleanup` need it
- **If the build fails, stop** — don't try to work around build failures
