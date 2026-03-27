---
name: steam-api-reference
description: Search and retrieve Steam Web API and Steamworks SDK documentation. Returns endpoint signatures, parameter descriptions, and code examples. Use when the user needs to call a Steam API, wants to know available endpoints, or is integrating Steamworks SDK methods.
---

# Steam API Reference

## Trigger

Use this skill when the user:

- Asks how to call a specific Steam API endpoint
- Wants to know what Steam/Steamworks APIs are available
- Needs parameter details for a Steam Web API method
- Is integrating the Steamworks SDK (C++, C#, or other supported languages)
- Asks about authentication (API keys, session tickets, etc.)

## Required Inputs

- **Query**: the API, interface, or method the user is looking for (e.g., "get player achievements", "ISteamUserStats", "leaderboard upload")

## Workflow

1. **Identify the relevant API interface.** Steam Web APIs are organized into interfaces:

   | Interface | Purpose |
   |-----------|---------|
   | `ISteamApps` | App metadata, version checks |
   | `ISteamUser` | Player identity, friends, bans |
   | `ISteamUserStats` | Achievements, stats, leaderboards |
   | `IPlayerService` | Owned games, playtime, badges |
   | `ISteamNews` | Game news feeds |
   | `ISteamRemoteStorage` | Workshop / UGC file details |
   | `IPublishedFileService` | Workshop queries (newer API) |
   | `ISteamEconomy` | In-game economy, trade |
   | `ISteamMicroTxn` | Microtransaction support |
   | `ISteamWebAPIUtil` | API key validation, server info |

2. **Fetch documentation.** Use the WebFetch tool to retrieve the relevant doc page:
   ```
   https://partner.steamgames.com/doc/webapi/{InterfaceName}
   ```
   For SDK methods:
   ```
   https://partner.steamgames.com/doc/api/{InterfaceName}
   ```

3. **If the interface is unknown**, search for the method:
   - Use WebSearch: `"Steam Web API {user's query} site:partner.steamgames.com"`
   - Or fetch the supported API list:
     ```
     https://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v1/?key={apikey}
     ```
     This returns all available interfaces, methods, and parameters. No key needed for public methods.

4. **Present the endpoint information:**
   - **URL pattern**: `https://api.steampowered.com/{Interface}/{Method}/{Version}/`
   - **HTTP method**: GET or POST
   - **Parameters**: name, type, required/optional, description
   - **Authentication**: whether a Steam Web API key is required
   - **Response format**: key fields in the JSON response

5. **Provide a code example** in the language most relevant to the user's project. Default to `curl` if unclear:
   ```bash
   curl.exe "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?appid=440&key=YOUR_KEY&steamid=76561198000000000"
   ```

## Authentication Guide

- **Public endpoints** (store data, app list, current players): no key needed.
- **User data endpoints** (achievements, stats, owned games): require a Steam Web API key.
- **Publisher endpoints** (sales data, partner APIs): require publisher API key + IP allowlisting.
- **Get a key**: https://steamcommunity.com/dev/apikey

Users should store their API key in an environment variable (`STEAM_API_KEY`) and never commit it.

## Common Endpoints Quick Reference

| Method | URL | Key? |
|--------|-----|------|
| Get app list | `ISteamApps/GetAppList/v2/` | No |
| App details (store) | `store.steampowered.com/api/appdetails?appids=X` | No |
| Current players | `ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=X` | No |
| Player achievements | `ISteamUserStats/GetPlayerAchievements/v1/?appid=X&key=K&steamid=S` | Yes |
| Global achievement % | `ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid=X` | No |
| User stats | `ISteamUserStats/GetUserStatsForGame/v2/?appid=X&key=K&steamid=S` | Yes |
| Owned games | `IPlayerService/GetOwnedGames/v1/?key=K&steamid=S` | Yes |
| News for app | `ISteamNews/GetNewsForApp/v2/?appid=X` | No |

## Example Interaction

**User:** "How do I get a list of achievements for my game from the Steam API?"

**Agent:**
1. Identifies `ISteamUserStats/GetPlayerAchievements` and `GetGlobalAchievementPercentagesForApp`
2. Provides endpoint URLs, parameters, and auth requirements
3. Shows a `curl` example and explains the response structure
4. Notes: "For per-player achievements you need the player's Steam ID and an API key. For global unlock percentages, no key is needed."

## MCP Usage

The [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) provides 10 tools that call Steam APIs directly, eliminating the need for manual `curl` commands for common operations.

### Available MCP Tools

**No API key required:**

| Tool | Description |
|------|-------------|
| `steam.getAppDetails({ appid, cc?, l? })` | Store data: price, reviews, tags, platforms, system requirements |
| `steam.searchApps({ term, cc?, l? })` | Search the Steam store by name |
| `steam.getPlayerCount({ appid })` | Current concurrent player count |
| `steam.getAchievementStats({ appid })` | Global achievement unlock percentages |
| `steam.getWorkshopItem({ publishedfileid })` | Workshop item details (title, tags, subscribers) |

**Requires `STEAM_API_KEY` environment variable:**

| Tool | Description |
|------|-------------|
| `steam.getPlayerSummary({ steamid })` | Player profile: name, avatar, online status |
| `steam.getOwnedGames({ steamid, include_played_free_games?, include_appinfo? })` | Game library with playtime data |
| `steam.queryWorkshop({ appid, search_text?, cursor?, numperpage?, query_type?, requiredtags? })` | Search and browse Workshop items |
| `steam.getLeaderboardEntries({ appid, leaderboardid, rangestart?, rangeend?, datarequest?, steamid? })` | Leaderboard scores and rankings |
| `steam.resolveVanityURL({ vanityurl, url_type? })` | Convert vanity URL to 64-bit Steam ID |

When an MCP tool exists for a given endpoint, prefer it over raw `curl` calls. For endpoints not covered by MCP tools (per-player achievements, user stats, news, microtransactions), continue using the Web API directly.

The Steamworks SDK documentation and example generation logic remain the same regardless of MCP availability.

## See Also

- [Steam Store Lookup](../steam-store-lookup/SKILL.md) - look up game store data using the APIs documented here
- [Steam Player Stats](../steam-player-stats/SKILL.md) - query player data using ISteamUserStats and IPlayerService endpoints
