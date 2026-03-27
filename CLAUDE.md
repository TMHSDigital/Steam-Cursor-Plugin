# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Steam Developer Tools** is a Cursor IDE plugin (v0.2.0) that integrates Steam and Steamworks APIs for game developers and power users. It provides AI-assisted workflows for querying Steam store data, managing Steamworks configurations, building multiplayer networking, implementing cloud saves, leaderboards, input, inventory/economy, social features, looking up API docs, fetching player statistics, integrating Workshop UGC, designing achievements, looking up player profiles, and comparing games.

This plugin uses Markdown skill files and MDC rule files for AI guidance, paired with the companion [Steam MCP Server](https://github.com/TMHSDigital/steam-mcp) (separate repo) which provides 10 read-only API tools for live data access. No build system, no npm, no compiled code in this repo.

The project is on a themed release roadmap toward v1.0.0 (see `ROADMAP.md`). The next major milestone (v0.3.0 "Insights") adds analytics and market research skills. Subsequent releases add CI/CD automation (v0.4.0), community/monetization skills (v0.5.0), QA rules (v0.6.0), MCP write operations (v0.7.0), and polish (v0.8.0). Target at v1.0.0: 30 skills, 9 rules, 20 MCP tools.

## Plugin Architecture

```
.cursor-plugin/plugin.json   - Plugin manifest (name, version, skills/rules directory pointers)
skills/<skill-name>/SKILL.md - AI workflow definitions (one per skill)
rules/<rule-name>.mdc        - Code quality and security rules (applied by Cursor AI)
```

### Skills (14 total)

Each `SKILL.md` uses YAML frontmatter followed by markdown sections: **Trigger**, **Required Inputs**, **Workflow**, and **Example**.

| Skill | Purpose |
|-------|---------|
| `steam-store-lookup` | Look up games/apps by name or App ID via Steam Store API |
| `steamworks-app-config` | Generate depot VDF configs, build pipelines, DLC setup |
| `steam-api-reference` | Search and present Steam Web API / Steamworks SDK docs |
| `steam-player-stats` | Query player counts, achievement rates, leaderboards, libraries |
| `steam-workshop-helper` | Look up Workshop items and document UGC integration patterns |
| `steam-achievement-designer` | Design achievements, generate VDF/JSON configs, provide unlock code |
| `steam-multiplayer-networking` | Lobby creation, matchmaking, Steam Networking Sockets, dedicated servers |
| `steam-cloud-saves` | ISteamRemoteStorage manual cloud and Auto-Cloud configuration |
| `steam-leaderboards` | Create/query leaderboards, upload scores, download entries |
| `steam-friends-social` | Friends list, rich presence, game invites, overlay, avatars |
| `steam-input-controller` | ISteamInput action sets, bindings, controller glyph retrieval |
| `steam-inventory-economy` | Item schema, drops, crafting, microtransactions, Steam Item Store |
| `steam-profile-lookup` | Resolve vanity URLs, fetch player summaries, owned games, level/badges |
| `steam-game-comparison` | Side-by-side comparison of price, reviews, player counts, genres |

### Rules (4 total)

| Rule | Scope | Purpose |
|------|-------|---------|
| `steam-appid-validation.mdc` | `steam_appid.txt`, `*.vdf`, steamcmd configs | Enforces App ID consistency; warns if `480` (SpaceWar test) is used in production |
| `steamworks-secrets.mdc` | Global (all files) | Flags Steam API keys (32-char hex), ssfn files, publisher credentials, DRM keys |
| `steam-deck-compat.mdc` | `*.cpp`, `*.cs`, `*.gd`, `*.vdf`, `*.cfg`, `*.ini`, `*.json` | Flags Steam Deck compat issues: hardcoded resolutions, mouse-only input, anti-cheat, Windows paths |
| `steam-api-key-usage.mdc` | `*.sh`, `*.ps1`, `*.py`, `*.js`, `*.ts`, `*.yml`, `*.yaml` | Flags raw curl/fetch to Steam APIs when MCP tools are available; suggests equivalent MCP tool |

### Companion MCP Server

The [Steam MCP Server](https://github.com/TMHSDigital/steam-mcp) provides 10 read-only tools. Skills reference these tools in their `## MCP Usage` sections. When the MCP server is configured in Cursor, skills prefer MCP tool calls over shell `curl` commands.

| MCP Tool | Auth | Maps to |
|----------|------|---------|
| `steam.getAppDetails({ appid })` | None | Store API `appdetails` |
| `steam.searchApps({ term })` | None | Store API `storesearch` |
| `steam.getPlayerCount({ appid })` | None | `GetNumberOfCurrentPlayers` |
| `steam.getAchievementStats({ appid })` | None | `GetGlobalAchievementPercentagesForApp` |
| `steam.getWorkshopItem({ publishedfileid })` | None | `GetPublishedFileDetails` |
| `steam.getPlayerSummary({ steamid })` | Key | `GetPlayerSummaries` |
| `steam.getOwnedGames({ steamid })` | Key | `GetOwnedGames` |
| `steam.queryWorkshop({ appid })` | Key | `IPublishedFileService/QueryFiles` |
| `steam.getLeaderboardEntries({ appid, leaderboardid })` | Key | `ISteamLeaderboards/GetLeaderboardEntries` |
| `steam.resolveVanityURL({ vanityurl })` | Key | `ResolveVanityURL` |

## Development Workflow

No build step required. Changes to `skills/` and `rules/` are picked up by Cursor automatically.

**Local testing - symlink the plugin directory:**

Windows (PowerShell as Admin):
```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.cursor\plugins\local\steam-cursor-plugin" -Target (Get-Location)
```

Unix/macOS (bash):
```bash
ln -s "$(pwd)" ~/.cursor/plugins/local/steam-cursor-plugin
```

## Key Conventions

- **Skill API names:** `ACH_` prefix, uppercase with underscores (e.g. `ACH_BEAT_FINAL_BOSS`). Stable after release.
- **Depot ID pattern:** `appid + N` (e.g., App ID `2345678` → depots `2345679` (Win), `2345680` (macOS), `2345681` (Linux))
- **Steam API key:** Never hardcode. Use the `STEAM_API_KEY` environment variable or a `.env` file (already in `.gitignore`).
- **App ID `480`** (SpaceWar) is the Steam SDK test app - the `steam-appid-validation` rule warns if it appears in production contexts.
- **Secrets rule** flags: 32-char hex strings near "steam"/"api", `*.ssfn` files, `config.vdf`, steamcmd login lines, CEG/DRM keys.

## Steam API Quick Reference

| Endpoint | Auth |
|----------|------|
| `ISteamApps/GetAppList/v2/` | None |
| `store.steampowered.com/api/appdetails?appids={id}` | None |
| `ISteamUserStats/GetNumberOfCurrentPlayers/v1/` | None |
| `ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/` | None |
| `ISteamUserStats/GetPlayerAchievements/v1/` | API key |
| `IPlayerService/GetOwnedGames/v1/` | API key |
| `ISteamUser/ResolveVanityURL/v1/` | API key |
| `ISteamUser/GetPlayerSummaries/v2/` | API key |
| `IPlayerService/GetOwnedGames/v1/` | API key |
| `IPlayerService/GetRecentlyPlayedGames/v1/` | API key |
| `IPlayerService/GetSteamLevel/v1/` | API key |
| `ISteamUser/GetFriendList/v1/` | API key |
| `ISteamLeaderboards/GetLeaderboardEntries/v1/` | API key |
| `IInventoryService/GetInventory/v1/` | API key |
| Publisher/partner endpoints | API key + IP allowlist |

Regional pricing: append `&cc={country}&l={language}` to store API calls.
