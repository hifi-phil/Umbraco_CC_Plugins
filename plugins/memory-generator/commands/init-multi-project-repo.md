---
description: Create a CLAUDE.md file for multi-project repo root
---

## Overview
Create a **concise, focused** CLAUDE.md file in the root of a multi-project repository.

## Rules

- **FOCUS ON REPO-LEVEL INFORMATION** - Structure, collaboration, and how projects relate
- **BE CONCISE** - This is a high-level overview, not project-specific details
- **LINK to project-specific CLAUDE.md files** - Don't duplicate what's in subdirectories
- Do not deviate from this template structure
- **TARGET LENGTH: 300-500 lines** (root should be shorter than individual projects)
- **DO NOT ADD "Getting Started" sections** - Skip basic clone/build commands that developers already know
- **DO NOT ADD "Quick Start" or "Installation" sections** - These are assumed knowledge

## Template

# CLAUDE.md Template - Multi Project Root

Simple outline for generating CLAUDE.md at the root of a repo of multiple projects. Focuses on structure and collaboration.

---

## 1. Overview

**What to include:**
- What this project contains (list of main applications/packages/services)
- Technologies used across projects (Node.js, .NET, Python, Go, etc.)
- Shared dependencies or common libraries
- Overall architecture (microservices, packages, apps + libs, frontend + backend, etc.)

---

## 2. Repository Structure

**What to include:**
- Top-level directory structure with descriptions
  ```
  /apps          - Applications (deployable services)
  /packages      - Shared libraries/packages
  /libs          - Common utilities
  /tools         - Build tools, scripts
  /docs          - Documentation
  /config        - Shared configuration
  ```
- List of main applications with brief description
  - `apps/web` - Customer-facing web app (Next.js)
  - `apps/api` - Backend API (Express)
  - `apps/admin` - Admin dashboard (React)
- Dependencies between projects (which apps use which packages)
- Build output locations (dist/, build/, out/)

---

## 3. Teamwork & Collaboration

**KEEP IT HIGH-LEVEL** - Link to CONTRIBUTING.md for details.

**What to include:**
- **Branching strategy:** (from CONTRIBUTING.md or git config)
  - Main branch name
  - Branch naming convention
  - Protected branches

- **Commit message format:** (ONLY if non-standard, otherwise reference CONTRIBUTING.md)

- **Pull request process:**
  - PR template location: `.github/pull_request_template.md` (if exists - USE VERBATIM)
  - Required CI checks
  - Merge strategy

- **Code owners:**
  - `.github/CODEOWNERS` file location (if exists)
  - Who owns which parts of the repo

**What to SKIP:**
- Generic commit message examples (everyone knows conventional commits)
- Detailed code review guidelines (link to CONTRIBUTING.md instead)
- Generic workflow advice

---

## Quick Reference

**What to include:**

- **Key directories:**
  - `/apps` - Applications
  - `/packages` - Shared packages
  - `/docs` - Documentation

- **Projects in this repo:**
  | Project | Type | Description | Port |
  |---------|------|-------------|------|
  | apps/web | Next.js | Customer web app | 3000 |
  | apps/api | Express | Backend API | 3001 |
  | apps/admin | React | Admin dashboard | 3002 |
  | packages/ui | React | Component library | - |

DO NOT create anything else in this section, only the above

---

## Usage

When generating CLAUDE.md for a project root:

1. **Focus on the big picture** - don't duplicate project-specific details
2. **Link to project-specific docs** - each app/package can have its own CLAUDE.md
3. **Emphasize structure and workflow** - how the repo works as a whole
4. **Keep it practical** - commands someone needs to get started
5. **Be concise** - root documentation should be shorter than individual projects
6. **Target length:** 300-500 lines

---

## When to Use This Template

Use this template at the **root level** of a repo that contains many project. For individual projects within the repo:
- Create separate CLAUDE.md files in each project directory using the specific Claude template
- Use the language-specific templates (Node.js or .NET) for those
- Link from root CLAUDE.md to project-specific ones

**Example structure:**
```
/root
  ├── CLAUDE.md                    # Use this template
  ├── apps/
  │   ├── web/
  │   │   └── CLAUDE.md           # Use Node.js template
  │   └── api/
  │       └── CLAUDE.md           # Use Node.js template
  └── packages/
      └── shared-lib/
          └── CLAUDE.md           # Use Node.js template
```

---

## Writing Philosophy

**Good multi-project CLAUDE.md:**
✅ Explains how projects relate to each other
✅ Links to individual project CLAUDE.md files
✅ Documents repo-level decisions (monorepo strategy, shared tooling)
✅ Shows dependency graph between projects
✅ Provides getting started commands for the entire repo

**Bad multi-project CLAUDE.md:**
❌ Duplicates content from individual project docs
❌ Includes generic Git/PR advice
❌ Exceeds 500 lines (should be shortest doc)
❌ Contains project-specific implementation details
❌ Reads like a tutorial instead of a navigation guide
❌ Includes "Getting Started" sections with basic `git clone` and build commands
❌ Contains "Prerequisites" sections listing obvious requirements like SDKs

---

**This template provides essential context for working with a multi-project repo without duplicating project-specific details.**

**Remember: The root CLAUDE.md is for NAVIGATION and STRUCTURE. Project-specific details belong in subdirectory CLAUDE.md files.**