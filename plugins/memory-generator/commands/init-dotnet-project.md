---
description: Create a CLAUDE.md file for .NET project
argument-hint: "[directory-path]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
---

## Context

- Target directory: $ARGUMENTS (if empty, use current directory)
- Working directory: Current location
- Project type: .NET

## Your Task

Generate a **concise, focused** CLAUDE.md file for a .NET project following the template structure below.

### Determine Scope

1. **Parse the target directory**:
   - If `$ARGUMENTS` is empty: Generate for current directory (this is a root/standalone project - include ALL sections)
   - If `$ARGUMENTS` contains a path: Generate for that subdirectory (this is a sub-project - SKIP section 8: Teamwork Protocol)

2. **Navigate to target**:
   - Change to the specified directory if provided
   - Verify it's a .NET project (look for .csproj files)

3. **Run discovery commands** to gather actual project information:
   - Find .csproj files
   - Check for .editorconfig, appsettings.json, Program.cs
   - Identify test projects
   - Check for EF Core migrations
   - Scan for TODO/HACK/FIXME comments

### Generation Rules

- **FOCUS ON PROJECT-SPECIFIC INFORMATION** - avoid generic .NET advice that applies to all projects
- Use actual values from the project - no placeholders like [PROJECT_NAME]
- Only include sections that are relevant to the specific project
- **BE CONCISE**: Each section should be focused and actionable
- **SKIP GENERIC CONTENT**: Don't include standard .NET patterns unless they're used uniquely in this project
- **CRITICAL**: If generating in a subdirectory, skip section 8 (Teamwork Protocol) entirely
- Reference actual file paths, commands, and configuration from the project
- **TARGET LENGTH**:
  - Small library (< 50 files): 300-500 lines
  - Medium project (50-200 files): 500-800 lines
  - Large application (200+ files): 800-1,200 lines

## Template

# CLAUDE.md Template - Section Guide

Simple outline showing what goes in each section. Use this as a quick reference when generating CLAUDE.md files.

---

## 1. Architecture

**What to include:**
- Target framework (e.g., net8.0)
- Language version (e.g., C# 12)
- Application type (Web API, MVC, Library, Console, Umbraco)
- Architecture pattern (Clean Architecture, Layered, Standard)
- Key technologies (web framework, database, DI, logging, validation, mapping, auth)
- Solution structure (folder tree)
- Design patterns used (Repository, Unit of Work, CQRS, Mediator, Options, Factory)

---

## 2. Commands

**What to include:**
- **Build commands:** build, clean, restore
- **Run commands:** run, watch (with actual project paths)
- **Test commands:** test, test with filters, test with coverage
- **Code quality:** format, build with warnings as errors
- **Database (if EF Core):** migrations add/update/remove/script
- **Publishing:** publish, pack (for libraries)
- **Package management:** add/remove/list packages, check outdated/vulnerable
- **Environment setup:** Prerequisites, SDK version, IDE requirements, database, tools
- **Initial setup steps:** Clone, install SDK, restore, configure, migrate, run
- **User secrets:** init, set, list (for ASP.NET Core)
- **Configuration sources:** Priority order

---

## 3. Style Guide

**KEEP IT SHORT** - Only include project-specific patterns, not generic .NET style advice.

**What to include:**
- **Project-specific naming conventions** (if different from standard .NET)
- **Key patterns from actual code** (2-3 examples with line numbers showing unique patterns)
- **Project-specific .editorconfig rules** (only if non-standard)
- **Unique C# features used** (only if project uses them in special ways)

**What to SKIP:**
- Generic naming conventions (everyone knows PascalCase for classes)
- Standard async/await patterns (covered in every .NET tutorial)
- Generic LINQ advice
- Standard null handling (unless project has unique approach)

**Target length**: 30-50 lines, not 100+

---

## 4. Test Bench

**KEEP IT BRIEF** - Focus on what's unique about testing THIS project.

**What to include:**
- **Where tests are** (test project paths)
- **How to run tests** (commands only)
- **Project-specific test patterns** (if any unique approaches)
- **What to focus on testing** (critical paths for this project)

**What to SKIP:**
- Generic testing advice (AAA pattern, mock best practices)
- Standard xUnit/NUnit usage
- Generic test naming conventions
- Only include testing frameworks if project actually has tests

**Target length**: 20-40 lines, not 100+

---

## 5. Error Handling

**FOCUS ON PROJECT-SPECIFIC** - Not generic try-catch advice.

**What to include:**
- **Project-specific error patterns** (custom exceptions, error handling middleware)
- **Domain-specific errors** (business rule violations, validation errors)
- **Critical logging points** (what to log in this project)

**What to SKIP:**
- Generic exception handling advice (everyone knows not to catch all exceptions)
- Standard logging patterns
- Generic try-catch examples
- Only include if project has custom error handling

**Target length**: 30-50 lines, not 100+

---

## 6. Clean Code

**SKIP GENERIC ADVICE** - Don't explain SOLID principles, everyone knows them.

**What to include:**
- **Key design patterns actually used** (Builder, Strategy, Factory - with file references)
- **Project-specific architectural decisions** (why certain patterns were chosen)
- **Code smells to watch for in THIS project** (based on actual codebase analysis)

**What to SKIP:**
- SOLID principles explanations
- Generic method/class design advice
- Standard DI patterns
- Generic code smells

**Target length**: 40-60 lines, not 200+

---

## 7. Security

**What to include:**
- Input validation (FluentValidation or Data Annotations examples, parameter validation)
- Authentication & authorization (detected method: JWT/Identity/OAuth/Azure AD, token validation, authorization policies, password requirements if Identity, controller authorization examples)
- Data access security (SQL injection prevention: EF Core parameterized, Dapper with parameters, never string concatenation)
- API security (CORS configuration, rate limiting, request size limits, security headers, HTTPS enforcement)
- Secrets management (User Secrets for dev, environment variables/Key Vault for prod, never commit secrets, never log secrets)
- Data protection (Data Protection API for encryption if detected)
- Dependency security (check vulnerable packages, update regularly)
- Security analyzers (if detected, list them)
- Security anti-patterns to avoid (BinaryFormatter, predictable GUIDs, plain text passwords, exposing stack traces in prod, trusting client validation, AllowAnonymous carelessly)

---

## 8. Teamwork and Workflow

**⚠️ SKIP THIS SECTION if a directory parameter was provided (subdirectory project). Include only for root/standalone projects.**

**What to include:**
- Version control (repository hosting: GitHub/Azure DevOps/GitLab from git config, branching strategy from CONTRIBUTING.md or inferred, branch naming convention, protected branches)
- Commit message format (from CONTRIBUTING.md if exists, otherwise Conventional Commits format with types and examples)
- Pull request process (PR title format, **PR description template - USE VERBATIM if found at .github/pull_request_template.md or similar**, code review checklist, review guidelines, merge requirements)
- Build & CI/CD (pipeline platform detected: GitHub Actions/Azure Pipelines/GitLab CI, pipeline stages from config, quality gates, environments and deployment strategy)
- Documentation (when to update: API changes, architecture changes, schema changes, new features, config changes, deployment changes; documentation locations: README, architecture docs, API docs, deployment docs, XML comments; CHANGELOG management if exists)
- Project management (tool: Azure Boards/Jira/GitHub Projects if known, work item types, workflow states, sprint cadence)
- Release process (steps: create branch, update versions, update CHANGELOG, test, deploy staging, merge to main, tag, deploy production, merge back)

---

## 9. Edge Cases

**ONLY PROJECT-SPECIFIC EDGE CASES** - Not generic .NET edge cases.

**What to include:**
- **Domain-specific edge cases** (unique to this project's business logic)
- **Known gotchas** (from TODO comments, issues, or code comments)
- **Integration edge cases** (external API failures, database constraints)

**What to SKIP:**
- Generic null handling (standard .NET)
- Generic collection edge cases
- Generic DateTime/String edge cases
- Generic async patterns
- Only include if project has documented edge cases

**Target length**: 30-50 lines, not 200+

---

## 10. Agentic Workflow

**HIGH-LEVEL GUIDANCE ONLY** - Not step-by-step code examples.

**What to include:**
- **Key decision points** (when to use which pattern, when to consult team)
- **Project-specific workflow** (how to add features to THIS codebase)
- **Quality gates** (what must pass before PR)
- **Common pitfalls** (mistakes to avoid in this project)

**What to SKIP:**
- Generic implementation steps
- Detailed code examples
- Generic error recovery advice
- Verbose "think aloud" examples

**Target length**: 60-100 lines, not 250+

---

## 11. Project-Specific Notes ⭐ **MOST IMPORTANT SECTION**

**THIS IS THE HEART OF THE DOCUMENT** - Everything here should be unique to this project.

**What to include:**
- **Key design decisions** (why things are done a certain way)
- **External integrations** (APIs, SDKs, services with versions)
- **Known limitations** (what doesn't work, what's not supported)
- **Performance considerations** (caching, background jobs, bottlenecks)
- **Deployment specifics** (Docker, cloud, configuration)
- **Technical debt** (TODO/HACK/FIXME with file:line references, top 5-10 only)

**What to emphasize:**
- Information that's NOT in the code
- Decisions and tradeoffs
- "Gotchas" and non-obvious behaviors

**Target length**: 100-200 lines (this section can be detailed)

---

## Quick Reference (Always Include)

**What to include:**
- Essential commands (run application, run tests, build with actual project paths)
- Key projects (list with one-sentence descriptions based on analysis)
- Important files (with full paths: appsettings.json, Program.cs, DbContext if EF, solution file)
- Configuration (development/staging/production approach detected or documented)
- Getting help (documentation paths, team lead from README if present)

---

## Usage

When generating CLAUDE.md:

1. **Determine the target directory**:
   - If no directory parameter provided: Generate in current directory (include all sections)
   - If directory parameter provided: Generate in that subdirectory (skip section 8: Teamwork Protocol)

2. **Run discovery commands** to gather project information from the target directory

3. **Fill in each section** using the guidance above

4. **Only include sections** that are relevant:
   - Skip Security for simple libraries
   - Skip Testing if no tests exist
   - **Skip Teamwork Protocol (section 8) if this is a subdirectory project**

5. **Use actual values** - no placeholders like [PROJECT_NAME]

6. **Keep it concise** - this is a guide, not every detail from above is required

7. **Verify completeness** - all relevant sections present, all placeholders replaced

---

## Suggested Length by Project Size

- **Small library (< 50 files):** 300-500 lines total
  - Focus on: Architecture, Commands, Key Patterns, Project-Specific Notes, Quick Reference

- **Medium project (50-200 files):** 500-800 lines total
  - Add: Testing, Security (if applicable), Agentic Workflow

- **Large application (200+ files):** 800-1,200 lines total
  - Add: More detailed sections, but still avoid generic advice

---

## Writing Philosophy

**Good CLAUDE.md characteristics:**
✅ Answers "Why?" not "What?" (the code shows what)
✅ Explains project-specific decisions and tradeoffs
✅ Points to actual files with line numbers
✅ Focuses on non-obvious information
✅ Highlights gotchas and common mistakes
✅ References actual code patterns from the project

**Bad CLAUDE.md characteristics:**
❌ Explains generic .NET concepts (SOLID, DI, async/await)
❌ Includes extensive code examples of basic patterns
❌ Repeats information from the root CLAUDE.md
❌ Contains advice that applies to all projects
❌ Exceeds 1,200 lines for any project
❌ Reads like a tutorial instead of a reference

---

**Remember: CONCISE and PROJECT-SPECIFIC is better than COMPREHENSIVE and GENERIC.**

## Final Step: Automatic Quality Review

**REQUIRED**: After generating CLAUDE.md, you MUST proactively use the `claude-md-optimizer` agent (without waiting for user to ask) to review for:
- Duplication and token waste
- Project-specific vs generic content
- Proper length targets
- Quality and accuracy

Say to the user: "Documentation generated. Now running automatic quality review with the claude-md-optimizer agent..."

Then immediately invoke the claude-md-optimizer agent.
