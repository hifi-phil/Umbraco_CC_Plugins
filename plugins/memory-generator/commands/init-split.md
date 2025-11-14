---
description: Split large CLAUDE.md into organized docs/ structure
argument-hint: "[directory-path]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

## Context

- Target directory: $ARGUMENTS (if empty, use current directory)
- This command splits an EXISTING large CLAUDE.md file into organized topic-specific files
- Content templates are defined in /init-nodejs-project and /init-dotnet-project commands

## Your Task

Split an existing CLAUDE.md file into a navigation index + separate topic docs in `docs/` folder.

### Output Structure

**Standalone Projects**: 11 files
- `CLAUDE.md` - Navigation index (~120-180 lines)
- `docs/` - 10 topic files including `workflow.md`

**Sub-Projects**: 10 files
- `CLAUDE.md` - Navigation index with monorepo note (~120-180 lines)
- `docs/` - 9 topic files (NO `workflow.md`)

### Process

1. **Check for existing CLAUDE.md** in target directory
   - If not found, suggest using `/init-nodejs-project` or `/init-dotnet-project` first

2. **Detect if sub-project or standalone**:
   - Check parent directory for package.json/.sln → Sub-project
   - Check if in `src/`, `packages/`, `apps/` folder → Sub-project
   - Check for `../../CLAUDE.md` → Sub-project
   - Otherwise → Standalone project

3. **Create backup**: Save `CLAUDE.md` to `CLAUDE.md.backup`

4. **Create `docs/` folder**

5. **Split existing CLAUDE.md into topic files**:
   - Extract sections to separate files in `docs/`
   - Sub-projects: Skip workflow section entirely
   - Standalone: Include workflow.md

6. **Update main CLAUDE.md**:
   - Keep only: overview, doc structure, quick start, quick reference, getting help
   - Remove detailed content (now in topic files)
   - Add monorepo note for sub-projects

### Topic Files to Create

**9-10 topic files** (content structure defined in /init-nodejs-project and /init-dotnet-project):
- `architecture.md` - System design and tech stack
- `commands.md` - All build/dev/test commands
- `workflow.md` - Git workflow, CI/CD (SKIP for sub-projects)
- `style-guide.md` - Naming and formatting
- `clean-code.md` - Best practices and SOLID
- `testing.md` - Testing strategies
- `error-handling.md` - Error patterns
- `edge-cases.md` - Common pitfalls
- `security.md` - Security practices
- `agentic-workflow.md` - AI assistant guide

### File Headers

**Topic docs** get simple headers:
```markdown
# [Topic Name]

Part of the [Project Name Documentation](../CLAUDE.md)

**Note**: [Sub-projects only] For Git workflow and CI/CD, see [monorepo root](../../CLAUDE.md).

---
```

**Main CLAUDE.md** structure:
- Project overview (brief, with metadata)
- Documentation Structure (categorized links to docs/)
- Quick Start (prerequisites, setup, 4-5 common commands + link to full Commands doc)
- Quick Reference (key dirs, files, conventions)
- Getting Help (links)

### Key Rules

1. **No duplication**: CLAUDE.md is navigation only, details go in topic docs
2. **Sub-projects**: NO workflow.md, add monorepo note to CLAUDE.md and topic headers
3. **Standalone**: Include workflow.md
4. **Simple headers**: No redundant doc lists in topic files
5. **Size**: CLAUDE.md ~120-180 lines, topic docs vary by content

### Example Usage

```bash
/init-split                              # Current directory
/init-split /src/Umbraco.Web.UI.Client  # Specific path
```

## Success Criteria

✅ CLAUDE.md reduced to navigation index (~120-180 lines)
✅ `docs/` folder with 9-10 topic files (no workflow.md for sub-projects)
✅ No duplication between CLAUDE.md and topic docs
✅ Simple headers in topic files (no redundant navigation lists)
✅ Sub-projects have monorepo notes, no workflow.md
✅ Backup created (CLAUDE.md.backup)

## Final Step: Automatic Quality Review

**REQUIRED**: After splitting documentation, you MUST proactively use the `claude-md-optimizer` agent (without waiting for user to ask) to review for:
- Remaining duplication between files
- Proper split structure validation
- Token efficiency analysis
- Sub-project scoping correctness

Say to the user: "Documentation split complete. Now running automatic quality review with the claude-md-optimizer agent..."

Then immediately invoke the claude-md-optimizer agent.
