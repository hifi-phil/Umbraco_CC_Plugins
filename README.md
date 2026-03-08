# Umbraco Claude Code Plugins 🚀

A curated marketplace of professional Claude Code plugins for Umbraco and .NET development workflows.

## Quick Start

Add the marketplace:
```bash
/plugin marketplace add hifi-phil/Umbraco_CC_Plugins
```

Install umb-flow for git workflow commands:
```bash
/plugin install umb-flow@hifi-phil/Umbraco_CC_Plugins
```

Install memory-generator for documentation:
```bash
/plugin install memory-generator@hifi-phil/Umbraco_CC_Plugins
```

Install umb-cms-reviews for PR testing:
```bash
/plugin install umb-cms-reviews@hifi-phil/Umbraco_CC_Plugins
```

Or install all plugins:
```bash
/plugin install @hifi-phil/Umbraco_CC_Plugins
```

## 📦 Available Plugins

### Umb-Flow 🔀
Git workflow commands for branching, committing, and pull requests. Follows your project's conventions automatically.

**Commands:**
- **`/branch <name>`** - Create a new branch
- **`/commit`** - Stage and commit changes
- **`/push`** - Push commits to remote
- **`/pr`** - Create a pull request

**Smart Branch Detection:**
- Identifies protected branches (main, master, dev, develop) via GitHub API
- Supports gitflow - automatically uses `dev`/`develop` as base when present
- Warns if you're branching from a feature branch instead of the base
- Uncommitted changes carry over to new branch (no forced stash)

**Convention Discovery:**
- Checks CLAUDE.md, CONTRIBUTING.md, .github/ templates for commit/PR formats
- Looks for commitlint config, .gitmessage templates
- Falls back to inferring style from recent commits/PRs
- Never forces conventional commits - uses whatever your project uses

**Safety Checks:**
- Warns before committing to protected branches
- Validates that changes match the branch purpose (e.g., warns if you're on `feature/auth` but committing payment code)
- Offers to create a new branch if you're on the wrong one
- Never force pushes or amends without explicit request

**Workflow Example:**
```bash
# Start new work
/branch feature/user-settings

# Make changes, then commit
/commit
# → Finds your commit conventions
# → Stages files, creates commit
# → Asks if you want to push

# Ready for review
/pr
# → Detects target branch (dev or main)
# → Uses your PR template
# → Creates PR and returns URL
```

### Memory Generator 📝
Generates and optimizes CLAUDE.md documentation files for Node.js, .NET projects, and multi-project repositories with intelligent project detection and automatic quality optimization.

**Commands:**
- **`/memory-generator:init-nodejs-project`** - Generate CLAUDE.md for Node.js/TypeScript projects
- **`/memory-generator:init-dotnet-project`** - Generate CLAUDE.md for .NET projects
- **`/memory-generator:init-multi-project-repo`** - Generate root CLAUDE.md for monorepos
- **`/memory-generator:init-split`** - Split large CLAUDE.md into organized docs/ structure

**Agent:**
- **`claude-md-optimizer`** - Automatically runs after doc generation to eliminate duplication and optimize token usage

**Features:**
- Intelligent detection of project type, dependencies, and structure
- Monorepo aware — smart handling of standalone vs sub-projects
- Auto-optimization agent eliminates duplication and maximizes token efficiency
- Generates docs based on actual code analysis, not templates

**How It Works:**
The commands analyze your codebase and generate focused CLAUDE.md documentation that:
- Answers "Why?" not "What?" (code already shows what)
- Includes project-specific decisions and tradeoffs
- Points to actual files with line numbers
- Highlights gotchas and common mistakes
- Avoids generic advice found in tutorials

Target lengths:
- Small library (< 50 files): 300-500 lines
- Medium project (50-200 files): 500-800 lines
- Large application (200+ files): 800-1,200 lines

**Usage Examples:**
```bash
# Node.js project
/memory-generator:init-nodejs-project
# Analyzes package.json, detects TypeScript/testing frameworks, generates CLAUDE.md

# .NET project
/memory-generator:init-dotnet-project ./src/MyProject
# Analyzes .csproj files, detects EF Core/testing, generates CLAUDE.md

# Split large documentation
/memory-generator:init-split
# Converts to navigation index + organized topic files in docs/
```

### Umb-CMS-Reviews 🧪
A complete workflow for reviewing Umbraco CMS pull requests using browser automation. Classifies PRs by testability, spins up isolated instances, runs automated UI tests with Playwright, captures evidence (screenshots, video, traces), and posts results back to the PR.

**Prerequisites:**
- [GitHub CLI](https://cli.github.com/) (`gh auth login`) — used to fetch PR details and post test results
- .NET SDK installed (for building Umbraco)
- A local clone of [Umbraco-CMS](https://github.com/umbraco/Umbraco-CMS)
- Playwright MCP server configured in `.mcp.json` (pr-test will check and guide you)

**Skills:**
- **`/pr-classify`** - Classify open PRs by testability and help pick which to test
- **`/pr-setup <number>`** - Check out a PR, build, and start a running Umbraco instance
- **`/pr-test <number>`** - Test a PR instance via browser automation with evidence capture
- **`/pr-cleanup <number>`** - Stop the instance and remove the worktree

**PR Classification:**
Each PR is classified into one of three categories:
- **BROWSER_TESTABLE** - Has UI changes with test steps that can be verified in the backoffice
- **API_TESTABLE** - Backend changes verifiable through API calls but no UI test plan
- **NOT_TESTABLE** - Dependency bumps, drafts, pure refactoring, or no behavioral change

**Isolated PR Instances:**
- Each PR is checked out into its own git worktree (`.claude/worktrees/pr-{number}`)
- Umbraco runs with SQLite and unattended install — no wizard needed
- Optional starter kit installation (e.g., Clean Starter Kit) for realistic test content
- Each instance gets a unique port (`10000 + PR number % 10000`)

**Evidence Capture:**
- Automatic video recording of the entire test session
- Screenshots at each test step (before/after)
- Playwright traces for debugging
- All evidence saved to `.playwright-mcp/` directory
- Results can be posted as a comment on the PR

**Workflow Example:**
```bash
# See what's open and testable
/pr-classify
# → Fetches open PRs, classifies by testability
# → Shows summary table with complexity ratings
# → Suggests which PR to test first

# Set up a PR for testing
/pr-setup 21887
# → Creates isolated worktree
# → Offers starter kit selection (Clean, UmBootstrap, etc.)
# → Configures unattended install with SQLite
# → Builds and starts Umbraco on a unique port
# → Reports URL, login credentials, and worktree path

# Run automated browser tests
/pr-test 21887
# → Extracts test steps from PR description
# → Logs into backoffice via Playwright
# → Executes each test step with retry logic
# → Captures screenshots and checks console for errors
# → Reports pass/fail per step with evidence
# → Optionally posts results to the PR

# Clean up when done
/pr-cleanup 21887
# → Stops the Umbraco process
# → Removes the git worktree
# → Cleans up the branch reference
```

## 🔄 Managing Plugins

List installed plugins:
```bash
/plugin list
```

Update plugins:
```bash
/plugin update memory-generator
```

Remove plugins:
```bash
/plugin remove memory-generator
```

## 🤝 Contributing

Want to add a plugin to this marketplace?

1. Fork this repository
2. Create a new plugin directory under `plugins/`
3. Add your plugin manifest and content
4. Update `marketplace.json`
5. Submit a pull request

## 📄 License

MIT License - see individual plugins for specific licensing.

## 🙏 Credits

Built with ❤️ by Phil W ([@hifi-phil](https://github.com/hifi-phil))

For [Claude Code](https://claude.com/claude-code) by Anthropic.
