---
name: pr-test
description: Test an Umbraco CMS pull request using browser automation. Logs into the backoffice via Playwright MCP, executes the test steps from the PR description, captures screenshots as evidence, and posts results to the PR. If the instance isn't running yet, it tells the user to run /pr-setup first. Use this skill whenever the user wants to test, verify, try, check, or explore a PR — even if the instance isn't set up yet. Trigger phrases include "test PR", "verify PR", "check PR works", "does this PR work?", "try PR", "run the tests", "check if the fix works", "run browser tests". Also triggers when the user provides a PR number and wants to interact with it in any testing or exploratory capacity, such as "can you build and test PR 21913" or "get PR 21900 running and check if it works". Use /pr-classify first to pick a good candidate.
---

# PR Test Runner

You test an already-running Umbraco CMS pull request by driving the backoffice UI with browser automation and verifying it against the PR description.

## Arguments

Required: A PR number (e.g., `21887`)

## Prerequisites

The PR instance must already be running. If it isn't, tell the user to run `/pr-setup {PR_NUMBER}` first.

Check if the instance is running:
```bash
PORT=$((10000 + {PR_NUMBER} % 10000))
lsof -ti:${PORT} 2>/dev/null && echo "Instance running on port ${PORT}" || echo "No instance on port ${PORT} — run /pr-setup {PR_NUMBER} first"
```

If not running, stop and tell the user. Do not set up the instance yourself.

## Overview

The test follows this pipeline:
1. **Fetch PR info** — get the PR description and extract test steps
2. **Confirm Playwright** — verify browser is ready
3. **Login via browser** — authenticate using Playwright MCP
4. **Execute test steps** — translate PR description into browser actions, retrying up to 3 times per step
5. **Report results** — pass/fail per step, upload evidence to the PR

## Step 1: Fetch PR Info

```bash
gh pr view {PR_NUMBER} --repo umbraco/Umbraco-CMS --json number,title,body,headRefName,baseRefName,changedFiles,additions,deletions,labels
```

Read the PR body and extract the test plan. See `references/pr-test-extraction.md` for how to parse the test steps.

Store the extracted data:
- **Test steps** — ordered list of actions and verifications
- **Preconditions** — what content/config needs to exist
- **Expected outcomes** — what each step should produce

## Step 2: Confirm Playwright is Ready

First, read `.mcp.json` in the repository root and verify the Playwright MCP server is configured correctly. The `playwright` entry must have these args:

- `--headless` — no visible browser window
- `--save-video=1920x1080` — auto-record video evidence
- `--viewport-size=1920x1080` — consistent viewport for screenshots
- `--save-trace` — capture trace for debugging
- `--isolated` — fresh browser context each session
- `--output-dir=.playwright-mcp` — all evidence goes to `.playwright-mcp/`

Expected config:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--headless",
        "--save-video=1920x1080",
        "--viewport-size=1920x1080",
        "--save-trace",
        "--isolated",
        "--output-dir=.playwright-mcp"
      ]
    }
  }
}
```

**If the config is missing or wrong**: Tell the user what needs to change, update the file, and then **stop** — tell them to restart Claude Code for the MCP changes to take effect, then re-run `/pr-test`. Do NOT continue testing with a misconfigured Playwright, as video and traces won't be captured.

**If the config is correct**: Continue to the browser check.

Confirm the browser is ready:

```
browser_snapshot
```

If the snapshot succeeds, the browser is running and ready for navigation. Video recording and trace capture are happening automatically in the background — evidence will be saved to `.playwright-mcp/` when the session ends.

See `references/playwright-config.md` for retry strategy and timeout details.

## Step 3: Login via Playwright MCP

Calculate port: `PORT = 10000 + ({PR_NUMBER} % 10000)`

Navigate to the backoffice and login:

1. `browser_navigate` to `http://localhost:{PORT}/umbraco`
2. Wait for the login page to load (`browser_wait_for` text "Login" or look for email field)
3. `browser_snapshot` to see the login form
4. `browser_fill_form` or `browser_type` to enter:
   - Email: `admin@test.com`
   - Password: `TestPassword1234!`
5. Click the login/sign-in button
6. `browser_wait_for` the dashboard to load (look for "Content" in the sidebar)
7. Take a screenshot to confirm login succeeded

Read `references/umbraco-navigation.md` for how to navigate the backoffice.

## Step 4: Execute Test Steps

For each test step extracted from the PR:

1. **Take a "before" screenshot** if this is a verification step
2. **Translate the step to browser actions** using the patterns in `references/umbraco-navigation.md`
3. **Execute the browser actions** using Playwright MCP tools
4. **Verify the outcome** using the patterns in `references/verification-patterns.md`
5. **Take an "after" screenshot** as evidence
6. **Record pass/fail** for this step

Read `references/evidence-capture.md` for screenshot and video recording guidance.

### Retry logic

The Umbraco backoffice is a SPA with async loading — elements may not appear immediately after navigation or actions. To give each step a fair chance:

- **Retry each action up to 3 times** before marking it as FAIL
- **Wait 2-3 seconds between retries** to allow async operations to complete
- **Re-snapshot before each retry** — the DOM may have changed
- Only mark a step as FAIL after all 3 attempts have been exhausted

This is especially important for:
- Clicking elements that appear after async loading (modals, pickers, tree expansion)
- Verifying text that renders after an API call completes
- Form submissions that trigger server-side processing

### Screenshot file paths:

All screenshots must be saved into the Playwright MCP evidence directory so they live alongside the auto-recorded video and traces:

```
.playwright-mcp/screenshots/pr-{PR_NUMBER}-step-{N}-{short-description}.png
```

For example:
- `.playwright-mcp/screenshots/pr-22034-step-1-validation-error-empty.png`
- `.playwright-mcp/screenshots/pr-22034-step-3-save-publish-success.png`

When calling `browser_take_screenshot`, always pass the `filename` parameter with the full relative path above. Do NOT use the default filename or save to the working directory root.

### Key Playwright MCP patterns:

- **Always use `browser_snapshot`** before clicking — it gives you the accessibility tree with element refs
- **Use `browser_take_screenshot`** at key moments for evidence — always with an explicit `filename` in `.playwright-mcp/screenshots/`
- **Check `browser_console_messages` with level "error"** after each major action to catch JS errors
- **Use `browser_wait_for`** after navigation or actions that cause page loads

### Handling preconditions:

If the test needs content that doesn't exist:
- **Navigate the backoffice UI** to create it — click through menus, fill forms, save
- The Clean Starter Kit provides blog content types, templates, and media — use these when possible
- If you can't create something via the UI after retries, mark the step as NEEDS_HUMAN_REVIEW

**IMPORTANT — UI only:**
- **Do NOT** use `browser_evaluate` to call the Management API directly
- **Do NOT** modify the database or make direct API calls to set up test data
- **Do NOT** bypass the UI to work around problems — if the UI doesn't work, that's a finding
- All actions must go through the backoffice UI, the same way a real user would

## Step 5: Report Results and Post to PR

After all test steps are complete, do two things: tell the user the results locally, and post evidence to the PR as a comment.

### Evidence directory

All evidence lives in `.playwright-mcp/`:
- **Videos** — recorded automatically to `.playwright-mcp/videos/` by Playwright MCP
- **Traces** — saved automatically to `.playwright-mcp/traces/`
- **Screenshots** — taken manually during test steps, saved to `.playwright-mcp/screenshots/` (see "Screenshot file paths" above)

### Rename the video

Playwright MCP saves videos with random hash filenames (e.g., `285b39eb6b353f4831ca80fb029562d1.webm`). After all test steps are complete, rename the most recent video to a descriptive name:

```bash
# Find the most recent .webm file and rename it
LATEST_VIDEO=$(ls -t .playwright-mcp/videos/*.webm 2>/dev/null | head -1)
if [ -n "$LATEST_VIDEO" ]; then
  mv "$LATEST_VIDEO" ".playwright-mcp/videos/pr-{PR_NUMBER}-{short-kebab-description}.webm"
fi
```

The `{short-kebab-description}` should be a few words summarising the PR, e.g.:
- `pr-22034-multi-url-picker-validation.webm`
- `pr-21887-upload-field-filename.webm`

### Local report

Present this to the user in the conversation:

```
## PR #{NUMBER}: {TITLE}
**Branch:** {headRefName}
**Status:** PASS / FAIL / PARTIAL

### Test Results
| Step | Action | Expected | Result |
|------|--------|----------|--------|
| 1 | Navigate to Settings > Data Types | Page loads | PASS |
| 2 | Create upload field data type | Data type created | PASS |
| 3 | Upload image, verify filename | Filename as text | FAIL |

### Console Errors
{list any JS console errors found, or "None"}

### Network Errors
{list any failed API calls, or "None"}

### Notes
{any observations, edge cases found, or areas that need human review}

### Evidence
**Video:** .playwright-mcp/videos/pr-{NUMBER}-{short-kebab-description}.webm
**Screenshots:**
- .playwright-mcp/screenshots/pr-{NUMBER}-step-1-{description}.png
- .playwright-mcp/screenshots/pr-{NUMBER}-step-2-{description}.png
- .playwright-mcp/screenshots/pr-{NUMBER}-step-3-{description}.png
**Traces:** .playwright-mcp/traces/

### Instance Still Running
The Umbraco instance is running at http://localhost:{PORT}/umbraco
Login: admin@test.com / TestPassword1234!
Run /pr-cleanup {PR_NUMBER} when done exploring.
```

The video will already have been renamed (see "Rename the video" above). List all screenshot files matching the PR number pattern from `.playwright-mcp/screenshots/`.

### Post evidence to the PR

Read `references/pr-comment-evidence.md` for the full process. In short:

1. **Post a text-only comment** on the PR via `gh pr comment` with:
   - Pass/fail summary table
   - Console/network error summary
   - Notes on edge cases or issues found
2. **Ask the user before posting** — confirm they want the comment added to the PR
3. **Tell the user where local evidence is** — all evidence is in `.playwright-mcp/` (screenshots, videos, traces)
4. **Do NOT attempt to upload images via gists** — `gh gist create` corrupts binary files. If the user wants images on the PR, they can edit the comment on GitHub and drag-drop the screenshot files in.

## Important Notes

- **Leave the instance running** — the developer may want to explore
- **Be thorough with edge cases** — if the PR fixes a specific bug, try to trigger the original bug too
- **Check console errors** — even if the UI looks correct, JS errors indicate problems
- **Take screenshots liberally** — evidence is cheap, reviewers appreciate seeing the actual UI
- **If a step fails, continue testing** — report all results, not just the first failure
- **If you can't figure out how to test something**, mark it as NEEDS_HUMAN_REVIEW rather than skipping silently
