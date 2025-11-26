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
- **`/init-nodejs-project`** - Generate CLAUDE.md for Node.js/TypeScript projects
- **`/init-dotnet-project`** - Generate CLAUDE.md for .NET projects
- **`/init-multi-project-repo`** - Generate root CLAUDE.md for monorepos
- **`/init-split`** - Split large CLAUDE.md into organized docs/ structure

**Agent:**
- **`claude-md-optimizer`** - Automatically runs after doc generation to eliminate duplication and optimize token usage

## 🌟 Features

- ✅ **Framework Support** - Node.js, TypeScript, .NET, and multi-project repositories
- ✅ **Intelligent Detection** - Automatically detects project type, dependencies, and structure
- ✅ **Monorepo Aware** - Smart handling of standalone vs sub-projects
- ✅ **Auto-Optimization** - Built-in QA agent eliminates duplication and maximizes efficiency
- ✅ **Project-Specific** - Generates docs based on actual code analysis, not templates

## 💡 How It Works

The plugins analyze your codebase and generate focused CLAUDE.md documentation that:
- Answers "Why?" not "What?" (code already shows what)
- Includes project-specific decisions and tradeoffs
- Points to actual files with line numbers
- Highlights gotchas and common mistakes
- Avoids generic advice found in tutorials

Target lengths:
- Small library (< 50 files): 300-500 lines
- Medium project (50-200 files): 500-800 lines
- Large application (200+ files): 800-1,200 lines

## 🎯 Usage Examples

Generate documentation for a Node.js project:
```bash
/init-nodejs-project
# Analyzes package.json, detects TypeScript/testing frameworks, generates CLAUDE.md
```

Generate for a .NET project:
```bash
/init-dotnet-project ./src/MyProject
# Analyzes .csproj files, detects EF Core/testing, generates CLAUDE.md
```

Split large documentation:
```bash
/init-split
# Converts to navigation index + organized topic files in docs/
```

## 📚 Documentation Philosophy

**Good Documentation:**
- ✅ Project-specific decisions and tradeoffs
- ✅ Non-obvious information and gotchas
- ✅ References to actual code with line numbers
- ✅ Focus on "why" rather than "what"

**Avoid:**
- ❌ Generic framework/language advice
- ❌ Tutorial-style explanations
- ❌ Redundant code examples
- ❌ Information applicable to all projects

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
