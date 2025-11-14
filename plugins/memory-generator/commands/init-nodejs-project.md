---
description: Create a CLAUDE.md file for Node.js project
argument-hint: "[directory-path]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
---

## Context

- Target directory: $ARGUMENTS (if empty, use current directory)
- Working directory: Current location
- Project type: Node.js/JavaScript/TypeScript

## Your Task

Generate a **concise, focused** CLAUDE.md file for a Node.js/JavaScript/TypeScript project following the template structure below.

### Determine Scope

1. **Parse the target directory**:
   - If `$ARGUMENTS` is empty: Generate for current directory (this is a root/standalone project - include ALL sections)
   - If `$ARGUMENTS` contains a path: Generate for that subdirectory (this is a sub-project - SKIP section 8: Teamwork Protocol)

2. **Navigate to target**:
   - Change to the specified directory if provided
   - Verify it's a Node.js project (look for package.json)

3. **Run discovery commands** to gather actual project information:
   - Read package.json for scripts, dependencies, engines
   - Check for tsconfig.json (TypeScript)
   - Check for .eslintrc, .prettierrc, jest.config.js
   - Identify test framework and structure
   - Check for Dockerfile, docker-compose.yml
   - Scan for TODO/FIXME/HACK/XXX comments

### Generation Rules

- **FOCUS ON PROJECT-SPECIFIC INFORMATION** - avoid generic Node.js/JavaScript advice that applies to all projects
- Use actual values from the project - no placeholders like [PROJECT_NAME]
- Only include sections that are relevant to the specific project
- **BE CONCISE**: Each section should be focused and actionable
- **SKIP GENERIC CONTENT**: Don't include standard patterns unless they're used uniquely in this project
- **CRITICAL**: If generating in a subdirectory, skip section 8 (Teamwork Protocol) entirely
- Reference actual npm scripts, file paths, and configuration from the project
- **TARGET LENGTH**:
  - Small library/package (< 50 files): 300-500 lines
  - Medium project (50-200 files): 500-800 lines
  - Large application (200+ files): 800-1,200 lines

## Template

# CLAUDE.md Template - Section Guide (Node.js/JavaScript/TypeScript)

Simple outline showing what goes in each section. Use this as a quick reference when generating CLAUDE.md files for Node.js projects.

---

## 1. Architecture

**What to include:**
- Node.js version (e.g., Node 20.x)
- Language (JavaScript or TypeScript, with version)
- Application type (REST API, GraphQL API, Web App, CLI tool, Library, Microservice)
- Framework (Express, Fastify, NestJS, Next.js, Koa, Hapi, etc.)
- Architecture pattern (MVC, Layered, Clean Architecture, Hexagonal, Microservices)
- Key technologies (web framework, database/ORM, validation, logging, authentication, testing)
- Project structure (folder tree: src/, dist/, tests/, config/, etc.)
- Design patterns used (Repository, Service Layer, Middleware, Dependency Injection, Factory, Strategy)

---

## 2. Commands

**What to include:**
- **Install commands:** npm install, yarn install, pnpm install
- **Build commands:** build (if TypeScript), compile, bundle
- **Run commands:** start, dev (with hot reload), watch
- **Test commands:** test, test:watch, test:coverage, test:unit, test:integration, test:e2e
- **Code quality:** lint, lint:fix, format, type-check (TypeScript)
- **Database (if applicable):** migrate, migrate:rollback, seed, db:reset
- **Development tools:** dev server, debug mode
- **Package management:** add/remove packages, check outdated, check vulnerabilities (npm audit)
- **Environment setup:** Prerequisites (Node version, package manager, database, Docker), environment variables setup
- **Initial setup steps:** Clone, install Node, install dependencies, copy .env.example, configure database, run migrations, start dev server
- **Scripts reference:** List of all npm scripts from package.json with descriptions

---

## 3. Style Guide

**KEEP IT SHORT** - Only include project-specific patterns, not generic JavaScript/TypeScript style advice.

**What to include:**
- **Project-specific naming conventions** (if different from standard JavaScript)
- **Key patterns from actual code** (2-3 examples with line numbers showing unique patterns)
- **Project-specific ESLint/Prettier/TypeScript rules** (only if non-standard)
- **Unique features used** (only if project uses them in special ways)

**What to SKIP:**
- Generic naming conventions (everyone knows camelCase for functions)
- Standard async/await patterns (covered in every JavaScript tutorial)
- Generic module patterns
- Standard error handling (unless project has unique approach)

**Target length**: 30-50 lines, not 100+

---

## 4. Test Bench

**KEEP IT BRIEF** - Focus on what's unique about testing THIS project.

**What to include:**
- **Where tests are** (test directory structure)
- **How to run tests** (npm scripts only)
- **Project-specific test patterns** (if any unique approaches)
- **What to focus on testing** (critical paths for this project)

**What to SKIP:**
- Generic testing advice (describe/it patterns, AAA)
- Standard Jest/Mocha usage
- Generic mocking patterns
- Only include testing frameworks if project actually has tests

**Target length**: 20-40 lines, not 100+

---

## 5. Error Handling

**FOCUS ON PROJECT-SPECIFIC** - Not generic try-catch advice.

**What to include:**
- **Project-specific error patterns** (custom error classes, error middleware)
- **Domain-specific errors** (business rule violations, validation errors)
- **Critical logging points** (what to log in this project)

**What to SKIP:**
- Generic exception handling advice
- Standard logging patterns
- Generic promise error handling
- Only include if project has custom error handling

**Target length**: 30-50 lines, not 100+

---

## 6. Clean Code

**SKIP GENERIC ADVICE** - Don't explain SOLID principles or basic patterns.

**What to include:**
- **Key design patterns actually used** (Middleware, Factory, Repository - with file references)
- **Project-specific architectural decisions** (why certain patterns were chosen)
- **Code smells to watch for in THIS project** (based on actual codebase analysis)

**What to SKIP:**
- SOLID principles explanations
- Generic function/module design advice
- Standard dependency injection patterns
- Generic code smells

**Target length**: 40-60 lines, not 200+

---

## 7. Security

**What to include:**
- Input validation (use validation libraries: Joi, Yup, Zod, express-validator; validate all user input, sanitize HTML, validate types and formats, set limits on input size)
- Authentication & authorization (detected method: JWT, Passport.js, Auth0, OAuth2; token validation, refresh tokens, session management, password hashing with bcrypt/argon2, authorization middleware, role-based access control RBAC)
- API security (rate limiting with express-rate-limit, CORS configuration properly, helmet.js for security headers, request size limits, input sanitization, prevent injection attacks)
- Database security (SQL injection prevention: use parameterized queries, ORMs with prepared statements; NoSQL injection prevention: validate input, use ODM properly; least privilege database users)
- Secrets management (environment variables with dotenv, never commit .env files, use secrets managers: AWS Secrets Manager, Azure Key Vault, Vault; rotate secrets regularly)
- Dependencies security (npm audit regularly, Snyk or Dependabot, update dependencies, avoid known vulnerable packages, review package permissions)
- Common vulnerabilities (XSS prevention: escape output, Content Security Policy; CSRF protection: tokens, SameSite cookies; open redirect prevention; prototype pollution prevention; ReDoS prevention: validate regex)
- HTTPS enforcement (force HTTPS in production, HSTS headers, secure cookies with httpOnly/secure flags)
- Data protection (encrypt sensitive data at rest, hash passwords never plain text, secure communication between services, sanitize logs)
- Security headers (Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security via helmet.js)
- Security anti-patterns to avoid (eval(), Function constructor, executing user input, trusting client data, exposing stack traces in production, using == instead of ===, weak cryptography)

---

## 8. Teamwork and Workflow

**⚠️ SKIP THIS SECTION if a directory parameter was provided (subdirectory project). Include only for root/standalone projects.**

**What to include:**
- Version control (repository hosting: GitHub/GitLab/Bitbucket from git config, branching strategy: Git Flow/GitHub Flow/Trunk Based from CONTRIBUTING.md or inferred, branch naming convention, protected branches main/master)
- Commit message format (from CONTRIBUTING.md if exists, otherwise Conventional Commits format: feat/fix/docs/style/refactor/test/chore with scope and description)
- Pull request process (PR title format, **PR description template - USE VERBATIM if found at .github/pull_request_template.md**, code review checklist, review guidelines, merge requirements: approvals, tests pass, no conflicts)
- Build & CI/CD (platform detected: GitHub Actions/GitLab CI/CircleCI/Travis; pipeline stages: install, lint, test, build, deploy; quality gates: all tests pass, linting passes, coverage threshold, no vulnerabilities; environments: development, staging, production)
- Code quality gates (ESLint passing, Prettier formatting, tests passing, coverage thresholds, TypeScript compilation if applicable, no console.log in production code)
- Documentation (when to update: API changes, architecture changes, new features, configuration changes, deployment changes; documentation locations: README.md, docs/, JSDoc/TSDoc comments, OpenAPI/Swagger specs, CHANGELOG.md)
- Package.json scripts (document all custom scripts and their purpose)
- Release process (versioning: semantic versioning, changelog generation, git tags, npm publish if library, deployment steps, rollback procedure)

---

## 9. Edge Cases

**ONLY PROJECT-SPECIFIC EDGE CASES** - Not generic JavaScript edge cases.

**What to include:**
- **Domain-specific edge cases** (unique to this project's business logic)
- **Known gotchas** (from TODO comments, issues, or code comments)
- **Integration edge cases** (external API failures, database constraints)

**What to SKIP:**
- Generic null/undefined handling (standard JavaScript)
- Generic array/string/number edge cases
- Generic async patterns
- Generic event loop advice
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
- **Performance considerations** (caching, clustering, bottlenecks)
- **Deployment specifics** (Docker, cloud, PM2, configuration)
- **Technical debt** (TODO/FIXME/HACK with file:line references, top 5-10 only)

**What to emphasize:**
- Information that's NOT in the code
- Decisions and tradeoffs
- "Gotchas" and non-obvious behaviors

**Target length**: 100-200 lines (this section can be detailed)

---

## Quick Reference (Always Include)

**What to include:**
- Essential commands (start dev server, run tests, build, with actual npm script names)
- Key directories (src/, dist/, tests/, config/ with brief descriptions)
- Important files (package.json, main entry point, config files, .env.example)
- Environment variables (list critical ones with descriptions)
- API endpoints (if web API: list main routes or link to API docs)
- Configuration (how to configure for development/staging/production)
- Getting help (documentation location, maintainer contact, repository issues link)

This section needs to be as simple as possible and ONLY include the basics

---

## Usage

When generating CLAUDE.md:

1. **Run discovery commands** (check package.json, tsconfig.json, .eslintrc, file structure)

2. **Fill in each section** using the guidance above

3. **Only include sections** that are relevant:
   - Skip Database for static sites
   - Skip Testing if no tests exist
   - **Skip Teamwork Protocol (section 8) if this is a subdirectory project**

4. **Use actual values** - real script names from package.json, real file paths, real dependency versions

5. **Keep it concise** - this is a guide, include what's actually present in the project

6. **Verify completeness** - all relevant sections present, all placeholders replaced

---

## Suggested Length by Project Size

- **Small library/package (< 50 files):** 300-500 lines total
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
❌ Explains generic JavaScript/Node.js concepts (async/await, promises)
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
