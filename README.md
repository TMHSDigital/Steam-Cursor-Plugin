<p align="center">
  <img src="assets/logo.png" alt="Steam Developer Tools" width="128" height="128">
</p>

<h1 align="center">Steam Developer Tools</h1>

<p align="center">
  <em>Steam &amp; Steamworks integration for Cursor IDE - built for game developers and power users.</em>
</p>

<p align="center">
  <a href="https://github.com/TMHSDigital/Steam-Cursor-Plugin/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/TMHSDigital/Steam-Cursor-Plugin/validate.yml?label=CI" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC--BY--NC--ND--4.0-blue.svg" alt="License: CC BY-NC-ND 4.0"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.3.0-green.svg" alt="Version"></a>
  <a href="https://github.com/TMHSDigital/Steam-Cursor-Plugin/stargazers"><img src="https://img.shields.io/github/stars/TMHSDigital/Steam-Cursor-Plugin?style=flat" alt="GitHub Stars"></a>
  <a href="https://github.com/TMHSDigital/Steam-Cursor-Plugin/commits/main"><img src="https://img.shields.io/github/last-commit/TMHSDigital/Steam-Cursor-Plugin" alt="Last Commit"></a>
  <a href="https://github.com/TMHSDigital/Steam-Cursor-Plugin"><img src="https://img.shields.io/badge/Cursor-Plugin-8B5CF6.svg" alt="Cursor Plugin"></a>
  <a href="https://partner.steamgames.com/doc/webapi"><img src="https://img.shields.io/badge/Steam_Web_API-1b2838.svg?logo=steam&logoColor=white" alt="Steam Web API"></a>
  <a href="https://github.com/sponsors/TMHSDigital"><img src="https://img.shields.io/badge/Sponsor-ea4aaa.svg?logo=githubsponsors&logoColor=white" alt="Sponsor"></a>
</p>

---

<p align="center">
  <strong>18 skills</strong> &nbsp;&bull;&nbsp; <strong>4 rules</strong> &nbsp;&bull;&nbsp; <strong>10 MCP tools</strong>
</p>

Query Steam store data, manage Steamworks app configurations, build multiplayer networking, implement cloud saves, design achievements, compare games, and look up player profiles - all from within Cursor's AI chat. Covers the full Steam &amp; Steamworks ecosystem with live data via the companion [Steam MCP Server](https://github.com/TMHSDigital/steam-mcp).

> **No API key required** for most features. Store lookups, player counts, global achievement stats, and app searches all work out of the box.

## How It Works

```mermaid
flowchart LR
    A["You ask Cursor\na Steam question"] --> B["Cursor loads\na Skill"]
    B --> C{"MCP server\navailable?"}
    C -- Yes --> D["Steam MCP Server\n(10 tools)"]
    C -- No --> E["curl to\nSteam Web API"]
    D --> F["Steam API"]
    E --> F
    F --> G["Formatted answer\nin Cursor chat"]
```

**Skills** teach Cursor how to handle Steam-related prompts. **Rules** enforce best practices in your game project files. The **MCP server** provides live, structured API access so skills can fetch real data instead of relying on shell commands.

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
| **Steam Multiplayer Networking** | Implement lobbies, matchmaking, Steam Networking Sockets (relay), and dedicated game servers with code examples for C++, C#, and GDScript. |
| **Steam Cloud Saves** | Add cloud save support via Auto-Cloud config or ISteamRemoteStorage SDK calls. Covers conflict resolution and quota management. |
| **Steam Leaderboards** | Create leaderboards, upload scores, and download entries (global, friends, around-user) via SDK and Web API. |
| **Steam Friends & Social** | Integrate friends list, rich presence, game invites, Steam Overlay, and avatar/persona retrieval into your game. |
| **Steam Input / Controllers** | Set up Steam Input with action sets, digital/analog bindings, and controller glyph retrieval for Xbox, PlayStation, Switch, and Steam Deck. |
| **Steam Inventory & Economy** | Implement item systems, drops, crafting, the Steam Item Store, and in-game purchases via ISteamInventory and ISteamMicroTxn. |
| **Steam Profile Lookup** | Look up any Steam user's public profile - games, playtime, level, badges, friends, and recent activity. |
| **Steam Game Comparison** | Compare two or more Steam games side by side - price, reviews, player counts, genres, and platforms in a formatted table. |
| **Steam Review Analysis** | Fetch and analyze game reviews - sentiment breakdown, common complaints, comparison across updates, and review bombing detection. |
| **Steam Price History** | Pricing trends, sale history, regional pricing analysis, and price-to-value scoring for any Steam game. |
| **Steam Market Research** | Genre trend analysis, tag popularity, competitor identification, and market gap analysis using Steam store data. |
| **Steam Wishlist Estimates** | Estimate wishlists from public signals using the Boxleiter method, with conversion rate benchmarks and revenue projections. |

### Rules

| Rule | What it does |
|:-----|:-------------|
| **App ID Validation** | Checks that Steam App IDs are consistent across your project (`steam_appid.txt`, VDF files, source code) and warns if `steam_appid.txt` is missing. |
| **Steamworks Secrets** | Prevents committing API keys, partner credentials, and auth tokens. Flags sensitive patterns and suggests secure alternatives. |
| **Steam Deck Compatibility** | Flags common Deck compat issues in game code: hardcoded resolutions, mouse-only input, anti-cheat blockers, Windows-only paths, and missing controller support. |
| **MCP Tool Preference** | When the Steam MCP server is configured, flags raw `curl`/`fetch` calls to Steam APIs and suggests the equivalent MCP tool. |

## Companion: Steam MCP Server

The [Steam MCP Server](https://github.com/TMHSDigital/steam-mcp) is the companion project that provides live, structured API tools for this plugin. It exposes Steam store data, player stats, achievements, workshop items, and more as MCP tools that Cursor can call directly.

### Setup

**Requires [Node.js](https://nodejs.org/) (v18+)** for `npx`. Add the Steam MCP server to your Cursor MCP configuration (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "steam": {
      "command": "npx",
      "args": ["-y", "@tmhs/steam-mcp"],
      "env": {
        "STEAM_API_KEY": "your_key_here"
      }
    }
  }
}
```

The `STEAM_API_KEY` is only required for tools that access user-specific data (player summaries, owned games, workshop queries, leaderboards, vanity URL resolution). Store lookups, player counts, achievement stats, and workshop item details work without a key.

### Available Tools

| Tool | Auth | Description |
|------|------|-------------|
| `steam.getAppDetails` | None | Store data (price, reviews, tags, platforms) |
| `steam.searchApps` | None | Search the Steam store by name |
| `steam.getPlayerCount` | None | Current concurrent players |
| `steam.getAchievementStats` | None | Global achievement unlock percentages |
| `steam.getWorkshopItem` | None | Workshop item details |
| `steam.getPlayerSummary` | Key | Player profile (name, avatar, status) |
| `steam.getOwnedGames` | Key | Game library with playtime |
| `steam.queryWorkshop` | Key | Search/browse Workshop items |
| `steam.getLeaderboardEntries` | Key | Leaderboard scores and rankings |
| `steam.resolveVanityURL` | Key | Convert vanity URL to Steam ID |

## Quick Start

1. **Install** the plugin [manually](#installation) (marketplace listing coming soon)
2. **Ask** Cursor anything about Steam - try: `What's the current price for Hades?`
3. **Get results** - the plugin fetches live data from Steam's public APIs and formats it for you

That's it. No configuration needed for basic usage.

## Installation

> **Marketplace listing pending review.** In the meantime, use manual installation.

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

```
What's the current price and review score for Hollow Knight?
```

```
How many people are playing Elden Ring right now?
```

```
Compare Hades, Dead Cells, and Hollow Knight - price, reviews, and current players.
```

<details>
<summary><strong>More examples (all 18 skills)</strong></summary>

**Store Lookup**
```
Look up Steam App ID 1245620
```

**Steamworks Configuration**
```
Set up Steam build configs for my game. App ID is 2345678, Windows and Linux only.
```

**API Reference**
```
What parameters does ISteamUserStats/GetUserStatsForGame accept?
```

**Player Stats**
```
What are the rarest achievements in Celeste?
```

**Workshop**
```
I want to add Workshop support to my Unity game. How do I handle uploads and downloads?
```

**Achievement Design**
```
I need achievements for my platformer. Milestones: complete tutorial, beat each world, collect all coins, speedrun under 2 hours.
```

**Multiplayer Networking**
```
How do I set up Steam lobbies for a 4-player co-op game?
```

**Cloud Saves**
```
I want to add cloud saves to my roguelike. I have a single save file in AppData/Local.
```

**Leaderboards**
```
My speedrun game needs a leaderboard for each level. Times in ms, lower is better.
```

**Friends & Social**
```
I want to show "Playing as [Character] on [Map]" in the Steam friends list.
```

**Controllers & Steam Deck Input**
```
My platformer has move, jump, dash, and pause. Set up Steam Input for Xbox and Steam Deck.
```

**Inventory & Economy**
```
I want cosmetic hat drops every 2 hours of playtime, plus a Steam Item Store for direct purchases.
```

**Profile Lookup**
```
Look up the Steam profile for vanity URL "gaben"
```

**Game Comparison**
```
Compare App IDs 570 and 730 side by side.
```

**Review Analysis**
```
Analyze recent reviews for Baldur's Gate 3. Are players happy with the latest patches?
```

**Price History**
```
What's the pricing history for Hades? Is it a good deal right now?
```

**Market Research**
```
I'm thinking about making a cozy farming sim. Is the market too saturated?
```

**Wishlist Estimates**
```
My game has 25,000 wishlists two weeks before launch. What should I expect for sales?
```

</details>

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
- Game comparisons (side-by-side analysis)
- Current player counts
- Global achievement unlock percentages
- App and game searches

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full themed release plan (v0.2.0 through v1.0.0).

| Version | Theme | Highlights |
|---------|-------|------------|
| **v0.2.0** | Live Data | Steam MCP server with 10 read-only tools, skill updates |
| **v0.3.0 (current)** | Insights | Review analysis, price history, market research, wishlist estimates |
| **v0.4.0** | Ship It | CI/CD automation, release checklist, steamcmd helper, build validation rules |
| **v0.5.0** | Grow | Community management, store page optimization, pricing strategy, DLC planning |
| **v0.6.0** | Quality | Playtest setup, anti-cheat integration, save compat / network security / error handling rules |
| **v0.7.0** | Full Power | MCP write operations (lobbies, workshop uploads, achievements, inventory) |
| **v0.8.0** | Polish | Cross-references, troubleshooting sections, migration guide |
| **v1.0.0** | Stable | Production release: 30 skills, 9 rules, 20 MCP tools |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute skills, rules, and improvements.

## Support

If this plugin is useful to you, consider [sponsoring the project](https://github.com/sponsors/TMHSDigital).

## License

CC BY-NC-ND 4.0 - see [LICENSE](LICENSE) for details.

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
