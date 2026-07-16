---
description: Provision a scheduled cloud routine that runs /dependabot-rollup for a single GitHub repo. Clones a per-repo routine (correct source, base branch, marketplace + enabled plugin, weekly cron) so adding a repo is a one-liner. One routine per repo by design — isolation, per-repo auth scope, and the drive-to-green loop are inherently per-PR.
argument-hint: "<owner/repo> [base-branch] [--cron '0 8 * * 1'] [--env <environment_id>]"
---

# /new-dependabot-routine

Create a scheduled **cloud routine** that runs `/dependabot-rollup` for one repository. Use this to stamp out a per-repo routine without hand-editing the routine config each time. The rollup logic lives in the `dependabot-rollup` plugin (delivered to the worker via the marketplace), so this command only produces the thin per-repo wiring.

**Why one routine per repo (not one routine sweeping many):** the `/dependabot-rollup` drive-to-green-CI step keeps working across turns until a single PR is green — that's inherently per-PR. Per-repo routines give failure isolation, repo-scoped auth, independent cadence/base-branch, and clean per-repo run history. This command makes that cheap.

ARGUMENTS: $ARGUMENTS
- `<owner/repo>` — **required**, e.g. `umbraco/Umbraco-CMS-MCP-Editor`.
- `[base-branch]` — optional. Default: `dev` if it exists on the target repo, else the repo's default branch.
- `--cron '<expr>'` — optional 5-field UTC cron. Default `0 8 * * 1` (Mon 09:00 Europe/London = 08:00 UTC). Minimum interval is 1 hour.
- `--env <environment_id>` — optional cloud environment id. If omitted, reuse the env of an existing Dependabot rollup routine (see step 2), else ask the user.

## Procedure

### 1. Resolve inputs

- Parse `<owner/repo>`; fail early if missing.
- **Base branch:** if not given, check `gh api repos/<owner/repo>/branches/dev` — if it exists use `dev`, else `gh repo view <owner/repo> --json defaultBranchRef --jq .defaultBranchRef.name`.
- **Cron:** default `0 8 * * 1` unless `--cron` given.
- Confirm the resolved repo URL (`https://github.com/<owner/repo>`), base branch, and cron back to the user before creating.

### 2. Resolve the cloud environment

Load the trigger tool first: `ToolSearch select:RemoteTrigger`.

- If `--env` was given, use it.
- Otherwise `RemoteTrigger {action:"list"}` and reuse the `job_config.ccr.environment_id` from an existing routine whose name starts with "Dependabot security rollup" (keeps all rollup routines on the same env). 
- If none exists and no `--env` was given, ask the user which environment to use — do not guess an id.

### 3. Build the routine body

Generate a fresh lowercase v4 UUID for `events[].data.uuid` (e.g. via `python3 -c "import uuid;print(uuid.uuid4())"`). Assemble:

```json
{
  "name": "Dependabot security rollup → <owner/repo> (<base>)",
  "cron_expression": "<cron>",
  "enabled": true,
  "enabled_plugins": ["dependabot-rollup@umbraco-cc-plugins"],
  "extra_marketplaces": ["hifi-phil/Umbraco_CC_Plugins"],
  "job_config": {
    "ccr": {
      "environment_id": "<env>",
      "session_context": {
        "model": "claude-sonnet-5",
        "sources": [{"git_repository": {"url": "https://github.com/<owner/repo>"}}],
        "allowed_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Skill"]
      },
      "events": [{"data": {
        "uuid": "<fresh-uuid>",
        "session_id": "",
        "type": "user",
        "parent_tool_use_id": null,
        "message": {"role": "user", "content": "<prompt below>"}
      }}]
    }
  }
}
```

**Event prompt content** (keep it short — the plugin ships the full playbook):

> Run the `/dependabot-rollup <base>` command for the repo `<owner/repo>`. That command is provided by the enabled `dependabot-rollup` plugin — follow it exactly. Contract reminder: SECURITY-ONLY (must map to an open Dependabot alert); EXCLUDE semver-major bumps (report them, never merge); roll all in-scope security bumps into ONE `chore/` branch + PR against `<base>`; drive the PR to fully-green CI via `/goal`; close superseded Dependabot PRs ONLY after CI is green; be a QUIET no-op if nothing is in scope; NOTIFY the human exactly once, at the end. If the Dependabot alerts API returns 403 (missing `security_events` scope), STOP and report that limitation rather than guessing.

### 4. Create and verify

- `RemoteTrigger {action:"create", body:{…}}`.
- **The exact field names/format for attaching a marketplace + plugin to a CCR routine are not yet confirmed.** After creating, `RemoteTrigger {action:"get", trigger_id:"…"}` and check that `enabled_plugins` and `extra_marketplaces` came back populated (not empty `[]`). If they were dropped or the call errored, try these variants and re-verify:
  - `extra_marketplaces` as full git URL `https://github.com/hifi-phil/Umbraco_CC_Plugins` instead of `owner/repo`.
  - `enabled_plugins` as just `dependabot-rollup`, or as an object map `{"dependabot-rollup@umbraco-cc-plugins": true}` (mirroring `settings.json` `enabledPlugins`).
  - Placing `enabled_plugins`/`extra_marketplaces` inside `job_config.ccr.session_context` if the top-level fields don't stick.
  Report which format worked so the next run is deterministic.
- Report the routine name, schedule (human-readable), resolved base branch, and the routine URL: `https://claude.ai/code/routines/<trigger_id>`.

### 5. Offer a smoke test

Offer to `RemoteTrigger {action:"run", trigger_id:"…"}` once to confirm the worker loads the plugin and the command runs end-to-end for that repo. Note it will act for real (open a PR, and close superseded PRs if CI goes green), so a first run should be supervised.

## Notes

- **Auth:** the routine's identity needs push + PR + branch-delete on the target repo, and `security_events` read for the Dependabot alerts API. If any run no-ops with a permissions report, that scope is missing for that repo.
- **No CI on the target repo:** `/dependabot-rollup`'s green-CI goal is vacuously met when a repo has no PR checks — the rollup then ships unverified. Only schedule repos you're comfortable auto-merging security bumps into, or ensure they run PR CI.
