#!/usr/bin/env python3
"""
Daily activity extractor (portable, hook-triggered).

Reads Claude Code CLI logs (~/.claude) and, if present, Cowork desktop-app logs, and
writes ONE Markdown file per calendar day: <out>/activity-<date>.md, keyed by the
activity date it describes. A companion Cowork scheduled task reads these + calendar +
Google Docs and posts a daily standup to Slack.

Cross-platform: auto-detects the Cowork data dir per OS and degrades gracefully if
either source is absent. All throttle/lock/log-cap logic lives here (--hook mode), so
the Claude Code hook is just a single `python … --hook` call — no shell wrapper.

Usage:
  extract-daily-activity.py --hook           # for the SessionStart/Stop hook (throttled+locked)
  extract-daily-activity.py                  # regenerate the last 5 days (manual)
  extract-daily-activity.py --backfill 7     # last N days
  extract-daily-activity.py --date 2026-07-14
Env:
  DAILY_ACTIVITY_OUT   override the output dir (default: ~/Documents/Claude/DailyActivity/out
                       if ~/Documents/Claude exists, else ~/DailyActivity/out)
stdlib only.
"""

import argparse
import datetime as dt
import glob
import json
import os
import platform
import sys
import tempfile
import time

HOME = os.path.expanduser("~")
CLAUDE_DIR = os.path.join(HOME, ".claude")
HISTORY = os.path.join(CLAUDE_DIR, "history.jsonl")
PROJECTS_GLOB = os.path.join(CLAUDE_DIR, "projects", "*", "*.jsonl")


def cowork_base():
    """Per-OS location of the Claude desktop app's data dir."""
    s = platform.system()
    if s == "Darwin":
        return os.path.join(HOME, "Library", "Application Support", "Claude")
    if s == "Windows":
        appdata = os.environ.get("APPDATA") or os.path.join(HOME, "AppData", "Roaming")
        return os.path.join(appdata, "Claude")
    xdg = os.environ.get("XDG_CONFIG_HOME") or os.path.join(HOME, ".config")
    return os.path.join(xdg, "Claude")


COWORK_GLOB = os.path.join(cowork_base(), "local-agent-mode-sessions", "*", "*", "local_*.json")


def default_out_dir():
    docs_claude = os.path.join(HOME, "Documents", "Claude")
    base = docs_claude if os.path.isdir(docs_claude) else HOME
    return os.path.join(base, "DailyActivity", "out")


OUT_DIR = os.environ.get("DAILY_ACTIVITY_OUT") or default_out_dir()
STATE_DIR = os.path.dirname(OUT_DIR)          # the DailyActivity dir
HW = os.path.join(STATE_DIR, ".last-run")
LOCK = os.path.join(STATE_DIR, ".run.lock")
HOOK_LOG = os.path.join(OUT_DIR, "hook.log")

COWORK_PATH_MARKERS = ("local-agent-mode-sessions",)
MAX_PROMPTS_PER_PROJECT = 40
PROMPT_TRIM = 240
DEFAULT_BACKFILL = 5
THROTTLE = 300          # 5 min churn guard (hook mode)
LOG_MAX = 262144        # cap hook.log at ~256 KB
STALE_LOCK = 300        # seconds before a lock is treated as abandoned


# --------------------------------------------------------------------------- #
def to_ms(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip()
    if not s:
        return None
    if s.isdigit():
        return int(s)
    try:
        return int(dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000)
    except Exception:
        return None


def iter_jsonl(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception:
                    continue
    except Exception:
        return


def is_cowork_path(p):
    return bool(p) and any(m in p for m in COWORK_PATH_MARKERS)


def new_project():
    return {"prompts": [], "branches": set(), "titles": set(), "count": 0}


def collect(day_set):
    data = {d: {"projects": {}, "cowork": []} for d in day_set}

    def day_of(ms):
        if ms is None:
            return None
        try:
            return dt.datetime.fromtimestamp(ms / 1000).date()
        except Exception:
            return None

    def proj_bucket(day, path):
        return data[day]["projects"].setdefault(path, new_project())

    for rec in iter_jsonl(HISTORY):
        day = day_of(to_ms(rec.get("timestamp")))
        if day not in day_set:
            continue
        proj = rec.get("project") or "(unknown)"
        if is_cowork_path(proj):
            continue
        b = proj_bucket(day, proj)
        b["count"] += 1
        text = (rec.get("display") or "").strip()
        if text and len(b["prompts"]) < MAX_PROMPTS_PER_PROJECT:
            t = text.replace("\n", " ")
            if len(t) > PROMPT_TRIM:
                t = t[:PROMPT_TRIM] + "…"
            if not b["prompts"] or b["prompts"][-1] != t:
                b["prompts"].append(t)

    for path in glob.glob(PROJECTS_GLOB):
        session_cwd = None
        ai_title = None
        per_day_branches = {}
        for rec in iter_jsonl(path):
            t = rec.get("type")
            if t == "user":
                if rec.get("isSidechain"):
                    continue
                day = day_of(to_ms(rec.get("timestamp")))
                if day not in day_set:
                    continue
                session_cwd = session_cwd or rec.get("cwd")
                per_day_branches.setdefault(day, set())
                if rec.get("gitBranch"):
                    per_day_branches[day].add(rec["gitBranch"])
            elif t == "ai-title":
                ai_title = rec.get("aiTitle") or ai_title
        if is_cowork_path(session_cwd):
            continue
        for day, branches in per_day_branches.items():
            b = proj_bucket(day, session_cwd or "(unknown)")
            b["branches"].update(branches)
            if ai_title:
                b["titles"].add(ai_title)

    for path in glob.glob(COWORK_GLOB):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                d = json.load(fh)
        except Exception:
            continue
        if d.get("scheduledTaskId") == "personal-standup-summary":
            continue
        created = to_ms(d.get("createdAt"))
        last = to_ms(d.get("lastActivityAt")) or created
        start_day = day_of(created) or day_of(last)
        end_day = day_of(last) or start_day
        if start_day is None:
            continue
        entry = {
            "title": (d.get("title") or "(untitled)").strip(),
            "initial": (d.get("initialMessage") or "").strip(),
            "kind": d.get("sessionType") or "interactive",
            "ms": created or last or 0,
        }
        for day in day_set:
            if start_day <= day <= end_day:
                data[day]["cowork"].append(dict(entry))

    for d in data:
        data[d]["cowork"].sort(key=lambda s: s["ms"])
    return data


# --------------------------------------------------------------------------- #
def project_name(path):
    if not path or path == "(unknown)":
        return "(unknown)"
    return os.path.basename(path.rstrip("/")) or path


def render(day, projects, cowork):
    lines = [f"# Activity — {day.strftime('%A %d %b %Y')} ({day.isoformat()})", ""]
    lines.append("_Host-generated from ~/.claude + Cowork logs; one file per calendar day._")
    lines.append("")

    lines.append("## Claude Code (CLI)")
    lines.append("")
    active = {p: v for p, v in projects.items()
              if v["count"] or v["prompts"] or v["titles"] or v["branches"]}
    if not active:
        lines.append("_No Claude Code CLI activity._")
        lines.append("")
    else:
        for path in sorted(active, key=lambda p: -active[p]["count"]):
            v = active[path]
            meta = []
            if v["branches"]:
                meta.append("branch: " + ", ".join(sorted(v["branches"])))
            meta.append(f"{v['count']} prompt(s)")
            lines.append(f"### {project_name(path)}  _(" + " · ".join(meta) + ")_")
            lines.append(f"`{path}`")
            if v["titles"]:
                lines.append("")
                lines.append("Session topics:")
                for t in sorted(v["titles"]):
                    lines.append(f"- {t}")
            if v["prompts"]:
                lines.append("")
                lines.append("Prompts:")
                for p in v["prompts"]:
                    lines.append(f"- {p}")
            lines.append("")

    lines.append("## Cowork")
    lines.append("")
    if not cowork:
        lines.append("_No Cowork activity._")
        lines.append("")
    else:
        for s in cowork:
            tag = " _(scheduled)_" if s["kind"] == "scheduled" else ""
            lines.append(f"### {s['title']}{tag}")
            if s["initial"]:
                gist = s["initial"].replace("\n", " ")
                if len(gist) > PROMPT_TRIM:
                    gist = gist[:PROMPT_TRIM] + "…"
                lines.append(f"- opened with: {gist}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_atomic(path, content):
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp-activity-", suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def generate(days):
    data = collect(set(days))
    out = []
    for day in sorted(days, reverse=True):
        b = data[day]
        path = os.path.join(OUT_DIR, f"activity-{day.isoformat()}.md")
        write_atomic(path, render(day, b["projects"], b["cowork"]))
        out.append((path, len(b["projects"]), len(b["cowork"])))
    return out


# --------------------------------------------------------------------------- #
def cap_log():
    try:
        if os.path.getsize(HOOK_LOG) > LOG_MAX:
            with open(HOOK_LOG, "r", encoding="utf-8", errors="replace") as fh:
                tail = fh.read().splitlines()[-200:]
            with open(HOOK_LOG, "w", encoding="utf-8") as fh:
                fh.write("\n".join(tail) + "\n")
    except OSError:
        pass


def run_hook():
    """Throttled + locked run for the SessionStart/Stop hook. Never raises."""
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
        now = int(time.time())
        last = 0
        try:
            last = int(open(HW).read().strip())
        except Exception:
            last = 0
        if now - last < THROTTLE:
            return 0
        # clear a stale lock left by a crashed run
        try:
            if now - os.stat(LOCK).st_mtime > STALE_LOCK:
                os.rmdir(LOCK)
        except OSError:
            pass
        # atomic lock: exactly one racer proceeds
        try:
            os.mkdir(LOCK)
        except OSError:
            return 0
        try:
            with open(HW, "w") as fh:
                fh.write(str(now))
            cap_log()
            days = [dt.date.today() - dt.timedelta(days=i) for i in range(DEFAULT_BACKFILL)]
            stamp = dt.datetime.now().isoformat(timespec="seconds")
            with open(HOOK_LOG, "a", encoding="utf-8") as lg:
                for path, np_, nc in generate(days):
                    lg.write(f"[{stamp}] {os.path.basename(path)} — {np_} project(s), {nc} cowork\n")
        finally:
            try:
                os.rmdir(LOCK)
            except OSError:
                pass
    except Exception:
        pass
    return 0


def main():
    ap = argparse.ArgumentParser(description="Extract per-day Claude/Cowork activity.")
    ap.add_argument("--hook", action="store_true", help="Throttled+locked run for the CC hook.")
    ap.add_argument("--date", help="A single day, YYYY-MM-DD.")
    ap.add_argument("--backfill", type=int, default=DEFAULT_BACKFILL,
                    help=f"Regenerate the last N calendar days (default {DEFAULT_BACKFILL}).")
    args = ap.parse_args()

    if args.hook:
        return run_hook()

    if args.date:
        try:
            days = [dt.datetime.strptime(args.date, "%Y-%m-%d").date()]
        except ValueError:
            print(f"error: --date must be YYYY-MM-DD (got {args.date!r})", file=sys.stderr)
            return 2
    else:
        today = dt.date.today()
        days = [today - dt.timedelta(days=i) for i in range(max(1, args.backfill))]

    stamp = dt.datetime.now().isoformat(timespec="seconds")
    for path, np_, nc in generate(days):
        print(f"[{stamp}] {os.path.basename(path)} — {np_} project(s), {nc} cowork session(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
