# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Steam Developer Tools** is a Cursor IDE plugin (v0.9.0) that integrates Steam and Steamworks APIs for game developers and power users. It provides AI-assisted workflows for querying Steam store data, managing Steamworks configurations, building multiplayer networking, implementing cloud saves, leaderboards, input, inventory/economy, social features, looking up API docs, fetching player statistics, integrating Workshop UGC, designing achievements, looking up player profiles, comparing games, analyzing reviews, researching pricing, evaluating market fit, estimating wishlists, automating builds, validating release readiness, scripting steamcmd, managing communities, optimizing store pages, planning pricing strategy, configuring DLC, setting up playtests, creating bug report workflows, integrating anti-cheat, providing a testing sandbox, and guiding platform migration.

This plugin uses Markdown skill files and MDC rule files for AI guidance, paired with the companion [Steam MCP Server](https://github.com/TMHSDigital/steam-mcp) (separate repo) which provides 20 API tools (14 read-only + 6 write/guidance) for live data access. No build system, no npm, no compiled code in this repo.

The project is on a themed release roadmap toward v1.0.0 (see `ROADMAP.md`). The next milestone is v1.0.0 "Stable" — the production release. Target at v1.0.0: 30 skills, 9 rules, 20 MCP tools.

## Plugin Architecture

```
.cursor-plugin/plugin.json   - Plugin manifest (name, version, skills/rules directory pointers)
skills/<skill-name>/SKILL.md - AI workflow definitions (one per skill)
rules/<rule-name>.mdc        - Code quality and security rules (applied by Cursor AI)
```

### Skills (30 total)

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
| `steam-review-analysis` | Fetch and analyze game reviews: sentiment, complaints, review bombing |
| `steam-price-history` | Pricing trends, sale history, regional pricing, value scoring |
| `steam-market-research` | Genre trends, tag popularity, competitor ID, market gap analysis |
| `steam-wishlist-estimates` | Estimate wishlists from public signals, conversion benchmarks |
| `steam-build-automation` | SteamPipe CI/CD: GitHub Actions, GitLab CI, Jenkins, Docker builds |
| `steam-release-checklist` | Pre-release validation: store page, depots, achievements, pricing, Deck |
| `steam-steamcmd-helper` | steamcmd scripting reference, commands, Docker, troubleshooting |
| `steam-community-management` | Announcements, events, forums, update templates, Community Hub |
| `steam-store-page-optimizer` | Capsule images, descriptions, tags, trailers, demos, screenshots |
| `steam-pricing-strategy` | Base pricing, regional pricing, discounts, sales, bundles, F2P |
| `steam-dlc-expansion-planning` | DLC setup, season passes, content cadence, pricing tiers |
| `steam-playtest-setup` | Steam Playtest config, open/closed playtests, key distribution |
| `steam-bug-report-template` | Bug report templates, crash dumps, system info, known issues |
| `steam-anticheat-integration` | EAC, BattlEye, VAC setup, Proton/Deck compatibility |
| `steam-testing-sandbox` | App ID 480 sandbox, test accounts, console commands, dev workflow |
| `steam-migration-guide` | Platform migration (Epic/GOG/itch.io to Steam), engine SDK integration |

### Rules (9 total)

| Rule | Scope | Purpose |
|------|-------|---------|
| `steam-appid-validation.mdc` | `steam_appid.txt`, `*.vdf`, steamcmd configs | Enforces App ID consistency; warns if `480` (SpaceWar test) is used in production |
| `steamworks-secrets.mdc` | Global (all files) | Flags Steam API keys (32-char hex), ssfn files, publisher credentials, DRM keys |
| `steam-deck-compat.mdc` | `*.cpp`, `*.h`, `*.hpp`, `*.cs`, `*.gd`, `*.vdf`, `*.cfg`, `*.ini`, `*.json` | Flags Steam Deck compat issues: hardcoded resolutions, mouse-only input, anti-cheat, Windows paths |
| `steam-api-key-usage.mdc` | `*.sh`, `*.ps1`, `*.py`, `*.js`, `*.ts`, `*.yml`, `*.yaml` | Flags raw curl/fetch to Steam APIs when MCP tools are available; suggests equivalent MCP tool |
| `steam-build-config-validation.mdc` | `*.vdf`, `*build*`, `*depot*` | Validates VDF build configs: missing depots, mismatched App IDs, invalid file mappings |
| `steam-launch-options-check.mdc` | `*.vdf`, `*launch*`, `*config*.json`, `*config*.cfg` | Flags launch option issues: missing executables, wrong OS targeting, missing descriptions |
| `steam-save-compat.mdc` | `*.cpp`, `*.h`, `*.hpp`, `*.cs`, `*.gd`, `*.json`, `*.cfg` | Flags save practices breaking cross-platform cloud sync: endianness, paths, serialization |
| `steam-network-security.mdc` | `*.cpp`, `*.h`, `*.hpp`, `*.cs`, `*.gd` | Flags insecure networking: unvalidated auth tickets, trusting client data, missing encryption |
| `steam-api-error-handling.mdc` | `*.cpp`, `*.h`, `*.hpp`, `*.cs`, `*.gd` | Flags missing Steamworks error handling: unchecked init, missing StoreStats, ignored callbacks |

### Companion MCP Server

The [Steam MCP Server](https://github.com/TMHSDigital/steam-mcp) provides 20 tools (14 read-only + 6 write/guidance). Skills reference these tools in their `## MCP Usage` sections. When the MCP server is configured in Cursor, skills prefer MCP tool calls over shell `curl` commands.

| MCP Tool | Auth | Maps to |
|----------|------|---------|
| `steam.getAppDetails({ appid })` | None | Store API `appdetails` |
| `steam.searchApps({ term })` | None | Store API `storesearch` |
| `steam.getPlayerCount({ appid })` | None | `GetNumberOfCurrentPlayers` |
| `steam.getAchievementStats({ appid })` | None | `GetGlobalAchievementPercentagesForApp` |
| `steam.getWorkshopItem({ publishedfileid })` | None | `GetPublishedFileDetails` |
| `steam.getReviews({ appid, filter, language })` | None | Store API `appreviews` |
| `steam.getPriceOverview({ appids, cc })` | None | Store API `appdetails` (price filter) |
| `steam.getAppReviewSummary({ appid })` | None | Store API `appreviews` (summary only) |
| `steam.getRegionalPricing({ appid, countries })` | None | Store API `appdetails` (multi-region) |
| `steam.getPlayerSummary({ steamid })` | Key | `GetPlayerSummaries` |
| `steam.getOwnedGames({ steamid })` | Key | `GetOwnedGames` |
| `steam.queryWorkshop({ appid })` | Key | `IPublishedFileService/QueryFiles` |
| `steam.getLeaderboardEntries({ appid, leaderboardid })` | Key | `ISteamLeaderboards/GetLeaderboardEntries` |
| `steam.resolveVanityURL({ vanityurl })` | Key | `ResolveVanityURL` |
| `steam.createLobby({ type, max_members, metadata })` | SDK guide | ISteamMatchmaking code examples |
| `steam.uploadWorkshopItem({ appid, title, ... })` | SDK guide | ISteamUGC upload code examples |
| `steam.updateWorkshopItem({ publishedfileid, ... })` | Publisher key | `IPublishedFileService/UpdateDetails` |
| `steam.setAchievement({ steamid, appid, achievement })` | Publisher key | `ISteamUserStats/SetUserStatsForGame` |
| `steam.uploadLeaderboardScore({ appid, leaderboardid, ... })` | Publisher key | `ISteamLeaderboards/SetLeaderboardScore` |
| `steam.grantInventoryItem({ appid, steamid, itemdefid })` | Publisher key | `IInventoryService/AddItem` |

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
| `IPlayerService/GetBadges/v1/` | API key |
| `IPlayerService/GetRecentlyPlayedGames/v1/` | API key |
| `IPlayerService/GetSteamLevel/v1/` | API key |
| `ISteamUser/GetFriendList/v1/` | API key |
| `ISteamLeaderboards/GetLeaderboardEntries/v1/` | API key |
| `IInventoryService/GetInventory/v1/` | API key |
| Publisher/partner endpoints | API key + IP allowlist |

Regional pricing: append `&cc={country}&l={language}` to store API calls.
