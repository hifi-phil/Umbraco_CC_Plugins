---
description: Create a CLAUDE.md file for .NET RCL with TypeScript
argument-hint: "[directory-path]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
---

## Context

- Target directory: $ARGUMENTS (if empty, use current directory)
- Working directory: Current location
- Project type: .NET Razor Class Library (RCL) with TypeScript frontend

## Your Task

Generate a **concise, focused** CLAUDE.md file for a .NET Razor Class Library (RCL) with TypeScript frontend following the template structure below.

This is a **HYBRID PROJECT** combining .NET and Node.js ecosystems - documentation must cover both sides and their integration points.

### Determine Scope

1. **Parse the target directory**:
   - If `$ARGUMENTS` is empty: Generate for current directory (this is a root/standalone project - include ALL sections)
   - If `$ARGUMENTS` contains a path: Generate for that subdirectory (this is a sub-project - SKIP section 8: Teamwork Protocol)

2. **Navigate to target**:
   - Change to the specified directory if provided
   - Verify it's an RCL with TypeScript frontend

3. **Run discovery commands** to gather actual project information:

   **-.NET Side:**
   - Find .csproj file with `Sdk="Microsoft.NET.Sdk.Razor"` or `Sdk="Microsoft.NET.Sdk.Web"`
   - Check for `StaticWebAssetBasePath` property (indicates RCL)
   - Look for wwwroot/ directory (compiled frontend output)
   - Check for any C# source files and structure
   - Identify Razor components if present

   **Frontend Side:**
   - Locate frontend directory (common names: Client/, src/, frontend/, app/)
   - Read package.json for scripts, dependencies, engines
   - Check for tsconfig.json (TypeScript configuration)
   - Check for build tool config (vite.config.ts, webpack.config.js, etc.)
   - Check for .eslintrc, .prettierrc
   - Identify frontend framework (Lit, React, Vue, Angular, Svelte)
   - Identify component model (Web Components, React components, etc.)
   - Scan for TODO/FIXME/HACK/XXX comments in both C# and TypeScript files

### Generation Rules

- **FOCUS ON HYBRID PROJECT NATURE** - emphasize integration between .NET and frontend
- **FOCUS ON PROJECT-SPECIFIC INFORMATION** - avoid generic .NET or Node.js advice that applies to all projects
- Use actual values from the project - no placeholders like [PROJECT_NAME]
- Only include sections that are relevant to the specific project
- **BE CONCISE**: Each section should be focused and actionable
- **SKIP GENERIC CONTENT**: Don't include standard patterns unless they're used uniquely in this project
- **CRITICAL**: If generating in a subdirectory, skip section 8 (Teamwork Protocol) entirely
- Reference actual file paths, commands, npm scripts, and configuration from the project
- **EMPHASIZE BUILD INTEGRATION**: Document how frontend build integrates with .NET build
- **TARGET LENGTH**:
  - Small RCL (< 50 files): 400-600 lines
  - Medium RCL (50-200 files): 600-900 lines
  - Large RCL (200+ files): 900-1,400 lines
  (Slightly longer than standard templates due to dual .NET + frontend nature)

## Template

# CLAUDE.md Template - Section Guide (RCL with TypeScript)

Simple outline showing what goes in each section for a hybrid .NET RCL + TypeScript project.

---

## 1. Architecture

**What to include:**

**-.NET Side:**
- Target framework (e.g., net9.0, net8.0)
- Language version (e.g., C# 12)
- Project type: Razor Class Library (RCL)
- SDK: Microsoft.NET.Sdk.Razor or Microsoft.NET.Sdk.Web
- StaticWebAssetBasePath configuration
- Key .NET dependencies and libraries
- Razor components structure (if applicable)

**Frontend Side:**
- Node.js version (e.g., Node 22.x)
- TypeScript version
- Frontend framework (Lit, React, Vue, Angular, Svelte, Vanilla)
- Component model (Web Components, React components, etc.)
- Build system (Vite, Webpack, Rollup, esbuild)
- Key frontend libraries (state management, routing, UI libraries)
- Module system (ESM, CommonJS)

**Integration:**
- How frontend assets are served (StaticWebAssetBasePath, wwwroot mapping)
- Build order (frontend → .NET or concurrent)
- Asset bundling strategy
- Development vs production asset handling

**Project Structure:**
```
ProjectRoot/
├── *.csproj                    # RCL project file
├── wwwroot/                    # Compiled frontend output
├── Client/ (or src/, frontend/, app/)
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts (or webpack, etc.)
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── types/
│   └── dist/ (or build/)
├── Components/ (optional C# Razor components)
└── Services/ (optional C# services)
```

**Design Patterns:**
- Repository pattern, Service layer, Factory, etc.
- Frontend patterns: Component composition, Context API, Custom elements, etc.

---

## 2. Commands

**What to include:**

**-.NET Commands:**
```bash
# Build commands
dotnet build <project>.csproj
dotnet clean
dotnet restore

# Pack for distribution
dotnet pack

# Run (if executable)
dotnet run (or dotnet watch run)

# Test (if tests exist)
dotnet test
```

**Frontend Commands (from frontend directory):**
```bash
# Install dependencies
npm install (or yarn, pnpm)

# Build commands
npm run build              # Production build
npm run build:app          # Build application
npm run build:api          # Build/generate API clients (if applicable)

# Development
npm run dev                # Dev server with hot reload
npm run watch              # Watch mode (rebuild on changes)
npm run preview            # Preview production build

# Code quality
npm run lint               # Run linter
npm run lint:fix           # Fix linting issues
npm run format             # Format code

# Type checking
npm run type-check         # TypeScript type checking
tsc --noEmit               # Quick type check

# API client generation (if applicable)
npm run generate:api       # Generate API clients from OpenAPI/Swagger

# Testing (if applicable)
npm run test               # Run tests
npm run test:watch         # Test watch mode
npm run test:coverage      # Coverage report
```

**Integrated Build Workflow:**
```bash
# Full build from scratch
cd <frontend-dir> && npm install && npm run build && cd .. && dotnet build

# Development mode (run concurrently)
# Terminal 1: cd <frontend-dir> && npm run watch
# Terminal 2: dotnet watch run (if applicable)

# Package for distribution
cd <frontend-dir> && npm run build && cd .. && dotnet pack
```

**Environment Setup:**

**Prerequisites:**
- .NET SDK version (from global.json if present)
- Node.js version (from package.json engines)
- npm/yarn/pnpm version
- Any other tools (Docker, database, etc.)

**Initial Setup Steps:**
1. Clone repository
2. Install .NET SDK (correct version)
3. Install Node.js (correct version)
4. Navigate to frontend directory: `cd <frontend-dir>`
5. Install frontend dependencies: `npm install`
6. Build frontend assets: `npm run build`
7. Return to root: `cd ..`
8. Restore .NET packages: `dotnet restore`
9. Build .NET project: `dotnet build`
10. Run tests (if applicable): `dotnet test`

---

## 3. Style Guide

**KEEP IT SHORT** - Only include project-specific patterns, not generic .NET or TypeScript advice.

**What to include:**

**-.NET Specific (if non-standard):**
- Project-specific C# naming conventions
- Razor component patterns
- Static asset organization

**Frontend Specific (if non-standard):**
- TypeScript/JavaScript naming conventions
- Component naming (especially for web components)
- File/folder organization patterns
- Import path conventions

**Key Patterns from Actual Code:**
- 2-3 examples with file:line references showing unique patterns
- Component registration patterns
- API client usage patterns
- State management patterns

**What to SKIP:**
- Generic C# naming (everyone knows PascalCase)
- Generic TypeScript naming (everyone knows camelCase)
- Standard async/await patterns
- Generic component lifecycle advice

**Target length**: 40-60 lines, not 150+

---

## 4. Test Bench

**KEEP IT BRIEF** - Focus on what's unique about testing THIS project.

**What to include:**

**-.NET Tests (if present):**
- Test project location
- Testing framework (xUnit, NUnit, MSTest)
- How to run: `dotnet test`
- Project-specific test patterns

**Frontend Tests (if present):**
- Test directory structure
- Testing framework (Jest, Vitest, Mocha, Playwright, Cypress)
- How to run: `npm test`
- Component testing approach
- Mock strategies for APIs

**Integration Testing:**
- How to test .NET + frontend together
- Test data setup
- Critical paths to test

**What to SKIP:**
- Generic testing advice (AAA pattern, mocking basics)
- Standard test framework usage
- Generic test naming conventions
- Only include testing frameworks if project actually has tests

**Target length**: 30-50 lines, not 100+

---

## 5. Error Handling

**FOCUS ON PROJECT-SPECIFIC** - Not generic try-catch advice.

**What to include:**

**-.NET Side:**
- Custom exception classes
- Error middleware (if applicable)
- Logging patterns

**Frontend Side:**
- Error boundaries (if React) or error handling patterns
- API error handling
- User notification patterns
- Console logging strategy

**Integration:**
- How frontend handles .NET API errors
- Error response formats
- Validation error handling

**What to SKIP:**
- Generic exception handling advice
- Standard logging patterns
- Generic promise error handling
- Only include if project has custom error handling

**Target length**: 40-60 lines, not 100+

---

## 6. Clean Code

**SKIP GENERIC ADVICE** - Don't explain SOLID principles or basic patterns.

**What to include:**
- **Key design patterns actually used** (with file references)
- **Project-specific architectural decisions** (why certain patterns were chosen)
- **Code smells to watch for in THIS project** (based on actual codebase analysis)
- **Component composition patterns** (how components are structured and composed)
- **Dependency injection patterns** (both .NET and frontend if applicable)

**What to SKIP:**
- SOLID principles explanations
- Generic method/class design advice
- Standard DI patterns
- Generic code smells

**Target length**: 50-70 lines, not 200+

---

## 7. Security

**What to include:**

**-.NET Side:**
- Input validation (FluentValidation, Data Annotations)
- Authentication & authorization (if applicable)
- CORS configuration (if serving APIs)
- Security headers
- Secrets management (User Secrets, environment variables)

**Frontend Side:**
- Input validation and sanitization
- XSS prevention (escape output, Content Security Policy)
- CSRF protection (if applicable)
- Secure API communication (authentication tokens, headers)
- Dependency security (npm audit)
- Avoiding dangerous patterns (innerHTML, eval, etc.)

**API Security (if RCL serves APIs):**
- Authentication method (JWT, cookies, bearer tokens)
- Authorization patterns
- Rate limiting
- Request validation
- HTTPS enforcement

**Secrets Management:**
- User Secrets for development (.NET)
- Environment variables for production
- Never commit secrets (.env, appsettings.json with secrets)
- Never log secrets

**Dependencies:**
- Check vulnerable packages: `npm audit`, `dotnet list package --vulnerable`
- Update regularly
- Review security advisories

**Common Vulnerabilities:**
- SQL injection prevention (parameterized queries, EF Core)
- XSS prevention (escape output, CSP headers)
- CSRF protection
- Open redirect prevention
- Prototype pollution prevention (JavaScript)
- ReDoS prevention

---

## 8. Teamwork and Workflow

**⚠️ SKIP THIS SECTION if a directory parameter was provided (subdirectory project). Include only for root/standalone projects.**

**What to include:**

**Version Control:**
- Repository hosting: GitHub/Azure DevOps/GitLab from git config
- Branching strategy from CONTRIBUTING.md or inferred
- Branch naming convention
- Protected branches

**Commit Message Format:**
- From CONTRIBUTING.md if exists, otherwise Conventional Commits format
- Types: feat, fix, docs, style, refactor, test, chore, build
- Examples with scope

**Pull Request Process:**
- PR title format
- **PR description template - USE VERBATIM if found at .github/pull_request_template.md**
- Code review checklist
- Review guidelines
- Merge requirements (approvals, tests pass, builds succeed)

**Build & CI/CD:**
- Pipeline platform detected: GitHub Actions/Azure Pipelines/GitLab CI
- Pipeline stages:
  1. Install .NET dependencies
  2. Install frontend dependencies (npm install)
  3. Build frontend (npm run build)
  4. Build .NET project
  5. Run tests
  6. Pack/publish
- Quality gates:
  - Frontend linting passes
  - TypeScript compilation succeeds
  - All tests pass
  - .NET build succeeds
  - No security vulnerabilities
- Environments: development, staging, production

**Code Quality Gates:**
- ESLint/Prettier passing (frontend)
- TypeScript compilation with no errors
- .NET build with no warnings
- All tests passing
- Code coverage thresholds (if configured)

**Documentation:**
- When to update:
  - API changes
  - Architecture changes
  - Component API changes
  - New features
  - Configuration changes
  - Build process changes
- Documentation locations:
  - README.md
  - Component documentation (JSDoc/TSDoc)
  - API documentation (XML comments in C#)
  - CHANGELOG.md

**Release Process:**
1. Create release branch
2. Update version files (.NET and package.json)
3. Update CHANGELOG
4. Build frontend: `cd <frontend-dir> && npm run build`
5. Build .NET: `dotnet build`
6. Run tests
7. Create release tag
8. Trigger CI/CD pipeline
9. Merge back to main/dev

---

## 9. Edge Cases

**ONLY PROJECT-SPECIFIC EDGE CASES** - Not generic .NET or JavaScript edge cases.

**What to include:**
- **Domain-specific edge cases** (unique to this project's business logic)
- **Known gotchas** (from TODO comments, issues, or code comments)
- **Integration edge cases** (frontend-backend communication issues)
- **Build edge cases** (order dependencies, timing issues)
- **Asset loading edge cases** (paths, caching, versioning)

**What to SKIP:**
- Generic null handling (standard .NET/TypeScript)
- Generic collection/array edge cases
- Generic async patterns
- Standard DateTime/String edge cases
- Only include if project has documented edge cases

**Target length**: 40-60 lines, not 200+

---

## 10. Agentic Workflow

**HIGH-LEVEL GUIDANCE ONLY** - Not step-by-step code examples.

**What to include:**
- **Key decision points** (when to modify .NET vs frontend, when to consult team)
- **Project-specific workflow** (how to add features to THIS hybrid codebase)
- **Build workflow** (ensuring frontend builds before .NET pack)
- **Quality gates** (what must pass before PR: lint, types, tests, builds)
- **Common pitfalls** (mistakes to avoid in this hybrid project)
- **Development cycle** (typical workflow for adding a feature)

**Example workflow:**
1. Identify if change is .NET-side, frontend-side, or both
2. For frontend changes: modify TypeScript, run `npm run build`, test in .NET context
3. For .NET changes: modify C#, rebuild, test
4. For integrated changes: coordinate both sides, test integration
5. Run all quality checks before PR
6. Ensure CI/CD pipeline passes

**What to SKIP:**
- Generic implementation steps
- Detailed code examples
- Generic error recovery advice
- Verbose "think aloud" examples

**Target length**: 80-120 lines, not 250+

---

## 11. Project-Specific Notes ⭐ **MOST IMPORTANT SECTION**

**THIS IS THE HEART OF THE DOCUMENT** - Everything here should be unique to this RCL project.

**What to include:**

**Build Integration:**
- **Build order** (frontend must build before .NET pack? Concurrent builds?)
- **Asset pipeline** (how frontend output gets into wwwroot)
- **StaticWebAssetBasePath** configuration and purpose
- **Development workflow** (watch modes, hot reload, manual rebuilds)
- **CI/CD pipeline specifics** (build steps, artifacts, deployment)

**Key Design Decisions:**
- Why this specific frontend framework was chosen
- Why this specific build tool was chosen
- Component architecture decisions
- API design decisions
- State management approach
- Routing strategy (if applicable)

**External Integrations:**
- APIs consumed (with versions)
- Third-party libraries (critical ones with versions)
- CDN dependencies
- External services

**Known Limitations:**
- What doesn't work
- What's not supported
- Browser compatibility constraints
- .NET version constraints
- Breaking changes from previous versions

**Performance Considerations:**
- Bundle size optimization
- Tree shaking strategy
- Code splitting (if applicable)
- Lazy loading patterns
- Caching strategies
- Asset compression

**Deployment Specifics:**
- How to package for NuGet
- How assets are distributed
- Runtime asset loading
- Configuration for consuming applications

**Technical Debt:**
- TODO/HACK/FIXME with file:line references
- Top 5-10 only
- Prioritized by impact

**Gotchas and Non-obvious Behaviors:**
- Frontend-backend integration quirks
- Build system quirks
- Asset path resolution issues
- Development vs production differences

**What to emphasize:**
- Information that's NOT in the code
- Decisions and tradeoffs
- "Gotchas" and non-obvious behaviors
- Integration points between .NET and frontend

**Target length**: 150-250 lines (this section can be detailed for hybrid projects)

---

## Quick Reference (Always Include)

**What to include:**

**Essential Commands:**
```bash
# Full build
cd <frontend-dir> && npm install && npm run build && cd .. && dotnet build

# Development
# Terminal 1: cd <frontend-dir> && npm run watch
# Terminal 2: dotnet watch run (if applicable)

# Run tests
cd <frontend-dir> && npm test && cd .. && dotnet test

# Package
cd <frontend-dir> && npm run build && cd .. && dotnet pack
```

**Key Directories:**
- `<frontend-dir>/` - Frontend source code
- `<frontend-dir>/src/` - TypeScript source files
- `<frontend-dir>/dist/` or `<frontend-dir>/build/` - Compiled frontend output
- `wwwroot/` - Static assets served by .NET
- `Components/` - Razor components (if present)
- `Services/` - C# services (if present)

**Important Files:**
- `<project>.csproj` - .NET RCL project file
- `<frontend-dir>/package.json` - Frontend dependencies and scripts
- `<frontend-dir>/tsconfig.json` - TypeScript configuration
- `<frontend-dir>/vite.config.ts` (or webpack.config.js, etc.) - Build tool config
- `global.json` - .NET SDK version (if present)
- `.editorconfig` - Code style configuration

**Configuration:**
- Development: Local settings, environment variables
- Staging: Staging-specific configuration
- Production: Production configuration, optimized builds

**Getting Help:**
- Documentation: README.md, docs/ folder
- Team lead/maintainer: (from README if present)
- Issues: Repository issues link

---

## Usage

When generating CLAUDE.md for an RCL with TypeScript:

1. **Determine the target directory**:
   - If no directory parameter provided: Generate in current directory (include all sections)
   - If directory parameter provided: Generate in that subdirectory (skip section 8: Teamwork Protocol)

2. **Run discovery commands** to gather project information:
   - **.NET side:** Find .csproj, check properties, scan C# structure
   - **Frontend side:** Navigate to frontend dir, read package.json, check TypeScript config, scan source structure
   - **Integration:** Understand how frontend build integrates with .NET build

3. **Fill in each section** using the guidance above

4. **Only include sections** that are relevant:
   - Skip Testing if no tests exist
   - Skip Security for simple component libraries
   - **Skip Teamwork Protocol (section 8) if this is a subdirectory project**

5. **Use actual values** - no placeholders like [PROJECT_NAME]
   - Real npm script names from package.json
   - Real file paths from both .NET and frontend
   - Real dependency versions

6. **Emphasize hybrid nature** - document build integration thoroughly

7. **Keep it concise** - this is a guide, not every detail is required

8. **Verify completeness** - all relevant sections present, all placeholders replaced

---

## Suggested Length by Project Size

- **Small RCL (< 50 files):** 400-600 lines total
  - Focus on: Architecture (hybrid nature), Commands (both .NET and frontend), Key Integration Points, Project-Specific Notes, Quick Reference

- **Medium RCL (50-200 files):** 600-900 lines total
  - Add: Testing (both sides), Security, Agentic Workflow

- **Large RCL (200+ files):** 900-1,400 lines total
  - Add: More detailed sections, but still avoid generic advice
  - Deeper integration documentation

---

## Writing Philosophy

**Good CLAUDE.md characteristics for RCL:**
✅ Answers "Why?" not "What?" (the code shows what)
✅ Explains **hybrid project integration** clearly
✅ Documents **build order and dependencies** explicitly
✅ Points to actual files with line numbers (both .NET and TypeScript)
✅ Focuses on non-obvious information
✅ Highlights gotchas in frontend-backend integration
✅ References actual code patterns from both .NET and frontend
✅ Explains asset serving and static web assets clearly

**Bad CLAUDE.md characteristics:**
❌ Explains generic .NET concepts (SOLID, DI, async/await)
❌ Explains generic TypeScript/Node.js concepts
❌ Includes extensive code examples of basic patterns
❌ Repeats information from the root CLAUDE.md
❌ Contains advice that applies to all projects
❌ Exceeds 1,400 lines for any project
❌ Reads like a tutorial instead of a reference
❌ Ignores the hybrid nature of the project

---

**Remember: CONCISE and PROJECT-SPECIFIC is better than COMPREHENSIVE and GENERIC.**

**For RCLs: INTEGRATION DOCUMENTATION is critical - how .NET and frontend work together.**

## Final Step: Automatic Quality Review

**REQUIRED**: After generating CLAUDE.md, you MUST proactively use the `claude-md-optimizer` agent (without waiting for user to ask) to review for:
- Duplication and token waste
- Project-specific vs generic content
- Proper length targets
- Quality and accuracy
- Hybrid project integration clarity

Say to the user: "Documentation generated. Now running automatic quality review with the claude-md-optimizer agent..."

Then immediately invoke the claude-md-optimizer agent.
