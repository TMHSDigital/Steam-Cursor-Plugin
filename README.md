<p align="center">
  <img src="assets/logo.png" alt="Steam Developer Tools" width="128" height="128">
</p>

<h1 align="center">Steam Developer Tools</h1>

<p align="center">
  <em>Steam &amp; Steamworks integration for Cursor IDE &mdash; built for game developers.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.1.0-green.svg" alt="Version"></a>
  <a href="https://github.com/TMHSDigital/Steam-Cursor-Plugin/stargazers"><img src="https://img.shields.io/github/stars/TMHSDigital/Steam-Cursor-Plugin?style=flat" alt="GitHub Stars"></a>
  <a href="https://github.com/TMHSDigital/Steam-Cursor-Plugin/commits/main"><img src="https://img.shields.io/github/last-commit/TMHSDigital/Steam-Cursor-Plugin" alt="Last Commit"></a>
  <a href="https://github.com/TMHSDigital/Steam-Cursor-Plugin"><img src="https://img.shields.io/badge/Cursor-Plugin-8B5CF6.svg" alt="Cursor Plugin"></a>
  <a href="https://partner.steamgames.com/doc/webapi"><img src="https://img.shields.io/badge/Steam_Web_API-1b2838.svg?logo=steam&logoColor=white" alt="Steam Web API"></a>
</p>

---

Query Steam store data, manage Steamworks app configurations, look up player stats, design achievements, and reference Steam API documentation &mdash; all from within Cursor's AI chat.

> **No API key required** for most features. Store lookups, player counts, global achievement stats, and app searches all work out of the box.

## Features

### Skills

| Skill | What it does |
|:------|:-------------|
| **Steam Store Lookup** | Look up any Steam game by name or App ID. Returns price, description, tags, reviews, release date, system requirements, and store links. |
| **Steamworks App Config** | Generate and document depot configs, build VDF files, launch options, and DLC setup for Steamworks. |
| **Steam API Reference** | Search Steam Web API and Steamworks SDK documentation. Get endpoint signatures, parameters, auth requirements, and code examples. |
| **Steam Player Stats** | Check current player counts, achievement unlock percentages, leaderboards, playtime data, and user game libraries. |
| **Steam Workshop Helper** | Query Workshop items, get UGC details, and follow integration patterns for adding Workshop support to your game. |
| **Steam Achievement Designer** | Design achievements with proper naming conventions, generate VDF/JSON config files, and get unlock code snippets for C++, C#, and GDScript. |

### Rules

| Rule | What it does |
|:-----|:-------------|
| **App ID Validation** | Checks that Steam App IDs are consistent across your project (`steam_appid.txt`, VDF files, source code) and warns if `steam_appid.txt` is missing. |
| **Steamworks Secrets** | Prevents committing API keys, partner credentials, and auth tokens. Flags sensitive patterns and suggests secure alternatives. |

## Quick Start

1. **Install** the plugin from the Cursor marketplace (or [manually](#manual-installation))
2. **Ask** Cursor anything about Steam &mdash; try: `What's the current price for Hades?`
3. **Get results** &mdash; the plugin fetches live data from Steam's public APIs and formats it for you

That's it. No configuration needed for basic usage.

## Installation

### From the Cursor Marketplace

1. Open Cursor
2. Go to **Settings** > **Plugins**
3. Search for **"Steam Developer Tools"**
4. Click **Install**

### Manual Installation

Clone the repo and symlink it to your local plugins directory:

```bash
git clone https://github.com/TMHSDigital/Steam-Cursor-Plugin.git
```

**Windows (PowerShell as Admin):**
```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.cursor\plugins\local\steam-cursor-plugin" -Target (Resolve-Path .\Steam-Cursor-Plugin)
```

**macOS / Linux:**
```bash
ln -s "$(pwd)/Steam-Cursor-Plugin" ~/.cursor/plugins/local/steam-cursor-plugin
```

## Usage Examples

Once installed, the plugin's skills are available in Cursor's AI chat. Just ask naturally.

---

### Store Lookup

```
What's the current price and review score for Hollow Knight?
```

```
Look up Steam App ID 1245620
```

---

### Steamworks Configuration

```
Set up Steam build configs for my game. App ID is 2345678, Windows and Linux only.
```

```
How do I configure DLC depots in Steamworks?
```

---

### API Reference

```
How do I get a list of achievements from the Steam API?
```

```
What parameters does ISteamUserStats/GetUserStatsForGame accept?
```

---

### Player Stats

```
How many people are playing Elden Ring right now?
```

```
What are the rarest achievements in Celeste?
```

---

### Workshop

```
I want to add Workshop support to my Unity game. How do I handle uploads and downloads?
```

```
Get details for Workshop item 1234567890
```

---

### Achievement Design

```
I need achievements for my platformer. Milestones: complete tutorial, beat each world, collect all coins, speedrun under 2 hours.
```

```
Generate a VDF achievement config for my game with these achievements: [list]
```

## Configuration

### Steam API Key

Some features (player stats, user data, workshop queries) require a Steam Web API key.

1. Get a free key at [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey)
2. Set it as an environment variable:

<details>
<summary><strong>Platform-specific setup</strong></summary>

**Windows (PowerShell):**
```powershell
$env:STEAM_API_KEY = "your_key_here"
```

**macOS / Linux:**
```bash
export STEAM_API_KEY="your_key_here"
```

**Persistent (`.env` file in your project):**
```
STEAM_API_KEY=your_key_here
```

</details>

The plugin's **Steamworks Secrets** rule will warn you if it detects an API key hardcoded in your source files.

### No-Key Features

These work immediately without any API key:

- Store lookups (price, description, reviews, system requirements)
- Current player counts
- Global achievement unlock percentages
- App and game searches

## Roadmap

- [ ] Steam MCP server for live, structured API calls
- [ ] Steam Deck compatibility checker skill
- [ ] Steamworks SDK code generation (boilerplate for common integrations)
- [ ] Steam review sentiment analysis skill

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute skills, rules, and improvements.

## License

MIT &mdash; see [LICENSE](LICENSE) for details.

<details>
<summary><strong>Steam API Reference Links</strong></summary>

- [Steam Web API Overview](https://partner.steamgames.com/doc/webapi)
- [Steamworks SDK Reference](https://partner.steamgames.com/doc/api)
- [Store API (appdetails)](https://wiki.teamfortress.com/wiki/User:RJackson/StorefrontAPI)
- [Steamworks Partner Documentation](https://partner.steamgames.com/doc/home)
- [Steam Workshop Implementation](https://partner.steamgames.com/doc/features/workshop)

</details>

---

<p align="center">
  Built by <a href="https://github.com/TMHSDigital">TMHSDigital</a>
</p>
