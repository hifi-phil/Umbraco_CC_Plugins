# Umbraco Claude Code Plugins 🚀

A curated marketplace of professional Claude Code plugins for Umbraco and .NET development workflows.

## Quick Start

Add the marketplace:
```bash
/plugin marketplace add hifi-phil/Umbraco_CC_Plugins
```

Install the memory-generator plugin:
```bash
/plugin install memory-generator@hifi-phil/Umbraco_CC_Plugins
```

Or install all plugins:
```bash
/plugin install @hifi-phil/Umbraco_CC_Plugins
```

## 📦 Available Plugins

### Memory Generator ✨
Generates and optimizes CLAUDE.md documentation files for Node.js, .NET projects, and multi-project repositories with intelligent project detection and automatic quality optimization.

_More plugins coming soon! This marketplace will expand with additional tools for Umbraco development, .NET workflows, and Claude Code productivity._

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
