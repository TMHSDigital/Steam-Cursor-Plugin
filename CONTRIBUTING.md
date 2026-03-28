# Contributing to Steam Developer Tools

Thanks for your interest in contributing to this Cursor plugin.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Steam-Cursor-Plugin.git
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Local Development

To test the plugin locally, symlink or copy the repo to your Cursor plugins directory:

```
~/.cursor/plugins/local/steam-cursor-plugin/
```

On Windows:
```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.cursor\plugins\local\steam-cursor-plugin" -Target (Resolve-Path .\Steam-Cursor-Plugin)
```

On macOS/Linux:
```bash
ln -s "$(pwd)/Steam-Cursor-Plugin" ~/.cursor/plugins/local/steam-cursor-plugin
```

Cursor will pick up changes to skills and rules without restarting.

## Plugin Structure

The plugin currently has **29 skills** and **9 rules**.

```
.cursor-plugin/
  plugin.json          # Plugin manifest (name, version, metadata)
skills/                # 29 skill directories
  <skill-name>/
    SKILL.md           # Skill definition with frontmatter + instructions
rules/                 # 9 rule files
  <rule-name>.mdc      # Rule definition with frontmatter + guidance
```

## Adding a Skill

1. Create a new directory under `skills/` with a kebab-case name
2. Add a `SKILL.md` file with YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: One-line description of what the skill does and when to use it.
   ---
   ```
3. Structure the body with these sections:
   - **Trigger** - when Cursor should load this skill
   - **Required Inputs** - what the user must provide
   - **Workflow** - step-by-step instructions for the agent
   - **Example Interaction** - sample prompt and response

## Adding a Rule

1. Create a `.mdc` file under `rules/`
2. Add YAML frontmatter:
   ```yaml
   ---
   description: What this rule enforces.
   alwaysApply: true   # or false with globs
   globs:               # only if alwaysApply is false
     - "**/*.vdf"
   ---
   ```
3. Write clear, actionable guidance in the body

## Pull Request Process

1. Keep changes focused - one skill or rule per PR when possible
2. Ensure all frontmatter is valid YAML
3. Test the skill/rule locally in Cursor before submitting
4. Write a clear PR description explaining what the change does and why

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, constructive, and collaborative.
