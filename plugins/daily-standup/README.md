# daily-standup

A personal routine that, **every weekday at 7am**, summarizes your previous day's work —
**Claude Code CLI** activity, **Cowork** sessions, **Google Calendar** events, and **Google Docs
you created** — and posts it to a Slack channel. (Monday covers Friday + the weekend.)

## Why two halves?

Cowork (the Claude desktop app) runs sandboxed: it **can't read `~/.claude`** (your Claude Code CLI
logs) and its session view has **no timestamps**, so it can't report CLI work or filter to a precise
day. A plain script *can* read those logs but has **no access to your Google/Slack connectors**. So
the routine is a hybrid:

```
Claude Code hooks → extractor → ~/Documents/Claude/DailyActivity/out/activity-<date>.md
                                        │ (folder granted to the Cowork task)
7am weekdays  → Cowork scheduled task → reads those files + Calendar + Google Docs → Slack
```

This plugin ships the **Claude Code half** and auto-wires it; a bundled `/setup` skill walks you
through the **Cowork half** (which a plugin can't automate — it lives in the desktop app).

## What the plugin does automatically

- Bundles `scripts/extract-daily-activity.py` (stdlib-only, cross-platform, degrades gracefully).
- Auto-wires it to **`SessionStart` + `Stop`** hooks (`async`, throttled to ~5 min, single-run lock,
  capped log — folded into the script, no shell wrapper). It refreshes the per-day activity files
  whenever you use Claude Code. **No `settings.json` editing.**

## Install

```
/plugin marketplace add hifi-phil/Umbraco_CC_Plugins   # if not already added
/plugin install daily-standup@umbraco-cc-plugins
```

Then finish the Slack/Cowork side:

```
/setup-daily-standup
```

## Requirements

- **Claude Code CLI** + **Python 3** on PATH as `python3` (Windows: see note below) — for the extractor.
- For the 7am post: the **Claude desktop app** with **Cowork scheduled tasks**, a **claude.ai account**,
  connectors (**Google Calendar / Drive / Slack**), and a **Slack channel**. The `/setup` skill covers this.

## Notes & limitations

- Refreshes only when you use Claude Code (that's the hook). A day spent only in Cowork falls back to
  `session_info` (approximate) for the Cowork section — CLI-only requirement is unaffected.
- The Cowork folder grant lives in the desktop app's config; recreating the task via the UI may need
  the folder re-added.
- Everything is cross-platform; only the Cowork *data* location differs per OS and the script
  auto-detects it. **Windows:** the hook calls `python3` — if only `python` is on PATH, edit
  `hooks/hooks.json`. The hook is async and fails silently, so a missing interpreter only means no
  auto-refresh (never a broken session).

## Files

- `scripts/extract-daily-activity.py` — the extractor (`--hook`, `--backfill N`, `--date YYYY-MM-DD`).
- `hooks/hooks.json` — SessionStart/Stop wiring.
- `skills/setup-daily-standup/` — the Cowork-side setup walkthrough (`/setup-daily-standup`).
