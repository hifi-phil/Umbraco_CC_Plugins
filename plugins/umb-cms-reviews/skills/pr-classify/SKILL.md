---
name: pr-classify
description: Classify open PRs on the Umbraco-CMS repo by testability and help pick which PR(s) to test with /pr-test. Use this skill whenever the user mentions PRs, pull requests, reviewing PRs, triaging PRs, wants to see what's open, wants to pick a PR, or asks "what should I test?" — even if they don't explicitly say "classify". Also triggers for questions like "which PRs can be automated?", "show me testable PRs", or "what's open?".
---

# PR Classifier

You help the developer understand which open PRs on the Umbraco-CMS repository can be automatically tested via browser automation, and which ones aren't suitable. Your tone is conversational — you're a colleague helping triage PR reviews.

## Arguments

- No arguments: classify all open PRs
- A PR number (e.g., `21887`): classify and extract test plan for just that PR

## Step 1: Fetch Open PRs

Use the fetch script to download all PR data in one shot. It fetches PR metadata and changed file lists in parallel (up to 8 at a time), caches results for 5 minutes, and returns a single JSON array with everything needed for classification.

All open PRs:
```bash
scripts/fetch-open-prs.sh
```

A specific PR:
```bash
scripts/fetch-open-prs.sh {PR_NUMBER}
```

Limit the number of PRs:
```bash
scripts/fetch-open-prs.sh --limit 20
```

The script returns a JSON array where each PR object includes all the standard `gh` fields plus a `files` array containing the changed file paths. This means you have everything needed for classification without making additional API calls.

**If the script isn't available** (e.g. running outside the plugin directory), fall back to:
```bash
gh pr list --repo umbraco/Umbraco-CMS --state open --limit 50 --json number,title,labels,body,headRefName,baseRefName,changedFiles,additions,deletions,isDraft
```

## Step 2: Classify Each PR

Read `references/pr-classification-heuristics.md` for the detailed classification rules.

Classify each PR into one of three categories:

### BROWSER_TESTABLE
The PR has changes that can be verified by navigating the Umbraco backoffice and interacting with the UI. Indicators:
- Has explicit UI test steps in the description (checkbox items with action words like "Go to", "Click", "Verify", "Navigate")
- Changed files include frontend code (`.ts`, `.js` files in `src/Umbraco.Web.UI.Client/`)
- Changed files include controllers or views
- Labels include `area/frontend` or `area/backoffice`

### API_TESTABLE
The PR modifies backend behavior that can be verified through API calls but has no UI test plan. Indicators:
- Changes to API controllers, services, or repositories
- Has behavioral expectations described in the PR body
- No UI test steps but has clear before/after behavior

### NOT_TESTABLE
The PR has no user-facing behavioral change that can be tested. Indicators:
- Dependency bumps (title starts with "Bump", labels include `dependencies`)
- Draft or WIP PRs
- Pure test infrastructure changes (files only in `tests/`)
- Static asset changes with no behavioral impact
- Build/template fixes
- Pure refactoring with no behavioral change

## Step 3: Extract Test Plans

For each BROWSER_TESTABLE PR, read `references/pr-test-extraction.md` and extract:

1. **Preconditions** — what needs to exist before testing (document types, content, media, users, languages, specific configuration)
2. **Test Steps** — the specific actions to perform in the browser
3. **Expected Outcomes** — what should be visible or verifiable after each step
4. **Complexity** — rate as LOW / MEDIUM / HIGH based on how much setup and how many steps are involved

## Step 4: Present Results

Sort the table so the best candidates for testing appear at the bottom (easiest to spot). Use this sort order:

1. **NOT_TESTABLE** first (least interesting — skim past these)
2. **API_TESTABLE** next
3. **BROWSER_TESTABLE HIGH** complexity
4. **BROWSER_TESTABLE MEDIUM** complexity
5. **BROWSER_TESTABLE LOW** complexity last (best candidates — right at the bottom)

Present a summary table like this:

```
| # | Title | Classification | Complexity | Notes |
|---|-------|---------------|------------|-------|
| 21860 | Dependencies: Update server-side deps | NOT_TESTABLE | - | NuGet package updates only |
| ... | ... | ... | ... | ... |
| 21900 | Elements: Workspace split view | BROWSER_TESTABLE | HIGH | Complex multi-view setup |
| 21875 | Doc Type: "Allowed in library" toggle | BROWSER_TESTABLE | MEDIUM | New toggle, some setup needed |
| 21887 | Upload Field: Show filename after upload | BROWSER_TESTABLE | LOW | Simple UI change, clear test steps |
```

Then for each BROWSER_TESTABLE PR (in the same order — LOW complexity last), provide a brief summary:

```
### PR #21887: Upload Field: Show filename after file upload
**Classification:** BROWSER_TESTABLE | **Complexity:** LOW
**What it does:** After uploading a file, the filename now appears as plain text (pre-save) or as a clickable link (post-save).
**Test steps:** Upload a file → verify filename shows → save → verify filename is now a link
**Preconditions:** Need a document type with an upload field property
```

## Step 5: Help Pick

After presenting the results, ask the developer which PR(s) they'd like to test. Suggest starting with LOW complexity PRs if this is their first time using the system. Mention they can run `/pr-test {number}` to test a specific PR.

If there are particularly interesting or important PRs (high impact, many changed files, or critical bugfixes), call those out specifically.
