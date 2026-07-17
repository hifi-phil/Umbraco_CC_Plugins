---
name: setup-daily-standup
description: Finish setting up the daily-standup routine — the Cowork scheduled task that reads the plugin's activity extracts, adds Google Calendar + new Google Docs, and posts a 7am weekday summary to Slack. Use after installing the daily-standup plugin. Trigger on "set up my daily standup", "configure the standup routine", "finish daily-standup setup".
---

# Set up the daily standup (Cowork half)

The `daily-standup` plugin already handles the **Claude Code CLI half**: its `SessionStart`/`Stop`
hooks run a bundled extractor that writes one activity file per day to
`~/Documents/Claude/DailyActivity/out/activity-<date>.md` (Claude Code CLI + Cowork sessions,
precise dates). That happens automatically whenever the user runs Claude Code — nothing to configure.

This skill finishes the **Cowork half**: the 7am scheduled task that reads those files, adds
calendar + Google Docs context, and posts to Slack. That part lives in the Claude **desktop app**
(Cowork) and can't be automated by a plugin, so guide the user through it.

**You are Claude Code on the user's machine. Do the file creation yourself; guide the user through
the desktop-app steps. Adapt paths to their OS.**

## Why a Cowork task (not another script)
Cowork has the Google/Slack connectors and its own scheduler; a plain script does not. But Cowork
can't read `~/.claude`, so it relies on the plugin's extract files (which is why the plugin exists).

## Prerequisites (verify first)
1. **daily-standup plugin installed + enabled** (its hook must be active — check `/hooks` or that
   `~/Documents/Claude/DailyActivity/out/` has recent `activity-*.md` files; if empty, run the
   extractor once manually: `python3 <plugin>/scripts/extract-daily-activity.py --backfill 3`).
2. **Claude desktop app** with **Cowork scheduled tasks enabled**, signed into a **claude.ai account**.
3. **Connectors** connected at https://claude.ai/customize/connectors: **Google Calendar**,
   **Google Drive**, **Slack**.
4. A **Slack channel** to post to + its **channel ID** (`C0…`, from the channel's details).

## Step 1 — Ask the user for their Slack channel name + ID.

## Step 2 — Create the Cowork task skill file
Write `~/Documents/Claude/Scheduled/personal-standup-summary/SKILL.md`, substituting the user's
`CHANNEL_NAME` and `CHANNEL_ID`:

````markdown
---
name: personal-standup-summary
description: Every weekday at 7am, summarize my previous-day activity — Claude Code + Cowork work (from the daily-standup plugin's per-day extract), calendar events, and newly-created Google Docs — and post it to CHANNEL_NAME.
---

You are generating my personal daily activity summary and posting it to Slack. Run these steps fully; the run has no memory of prior conversations.

STEP 1 — Determine the reporting period (a list of calendar dates).
- If today is Monday: LAST FRIDAY, SATURDAY and SUNDAY (today−3, −2, −1). Otherwise: YESTERDAY (today−1).
- Write the exact date(s) as YYYY-MM-DD.

STEP 2 — Read the activity extract (primary source for Claude work).
- Files live in the connected folder DailyActivity, in out/, named activity-<date>.md, one per calendar day. Full path: ~/Documents/Claude/DailyActivity/out/activity-<date>.md.
- For EACH date in the period, open its file. Each has a "Claude Code (CLI)" section (projects, branches, session topics, prompts) and a "Cowork" section.
- Write a concise, grouped summary across the period — group by theme/project, not by day. Cover both sections.
- FALLBACK: if a day's file is missing/empty, note it and use session_info tools (mcp__session_info__list_sessions, mcp__session_info__read_transcript) to recover Cowork activity, with a one-line note that that day is approximate. (session_info sees Cowork only, no CLI, no reliable dates — prefer the files.)

STEP 3 — Calendar.
- Google Calendar connector (list_calendars, list_events): the period's events + today's agenda.
- Optional preference: to cut noise, drop any event whose title contains "standup"/"stand-up" (case-insensitive). Remove this line to keep them.
- Skip gracefully with a one-line note if the connector errors.

STEP 4 — New Google Docs / Drive files created in the period.
- Google Drive connector (search_files / list_recent_files): files CREATED (not merely edited) in the period. List title + link. Skip gracefully if none/unavailable.

STEP 5 — Post to Slack.
- Post to the PRIVATE channel CHANNEL_NAME (channel ID: CHANNEL_ID).
- Format scannable: a short date/period header; **What I worked on** (grouped bullets, note Claude Code vs Cowork where useful); **Calendar** with EACH event on its OWN line (one bullet per event, never joined with "·"), grouped under "Yesterday (<date>)" and "Today (<date>)" lines as `• <time> <title>`, any heads-up on its own line; **New docs** (one per line, omit if none).
- If there was no activity, still post a brief note and include Calendar + New docs.
````

## Step 3 — Create the scheduled task in Cowork (user does this in the app)
1. Cowork → **Scheduled** → **New scheduled task**.
2. Point it at `~/Documents/Claude/Scheduled/personal-standup-summary/SKILL.md`.
3. Schedule: **`0 7 * * 1-5`**.
4. Ensure **Google Calendar, Google Drive, Slack** connectors are available to the task.
5. **Grant it the folder** `~/Documents/Claude/DailyActivity` (edit task → add folder) so it can read the extracts.

## Step 4 — Test
1. Confirm `~/Documents/Claude/DailyActivity/out/` has a fresh `activity-<today>.md` (use Claude Code once, or run the extractor manually).
2. In Cowork, **Run now** on the task.
3. Check Slack: the post should include a **What I worked on** section with the user's Claude Code CLI projects/branches — proving it read the extract files (not just the session_info fallback). If the CLI section is missing, re-check the folder grant.

## Notes
- The extract refreshes only when the user runs Claude Code (that's what the plugin hook is for). A day spent only in Cowork falls back to session_info (approximate) for the Cowork section.
- The folder grant lives in the Cowork app's own config — if the user recreates the task via the UI, they may need to re-add the folder.
- **Windows:** the plugin hook calls `python3`; if only `python` is on PATH, edit the plugin's `hooks/hooks.json` accordingly (the hook is async and failure is silent, so a missing `python3` just means no auto-refresh).
