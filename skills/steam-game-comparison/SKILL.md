---
name: steam-game-comparison
description: Compare two or more Steam games side by side. Fetches store data and player counts for multiple titles and formats a comparison table. Use when comparing game prices, reviews, player counts, or features for competitive analysis, purchase decisions, or market research.
---

# Steam Game Comparison

## Trigger

Use this skill when the user:

- Wants to compare two or more Steam games
- Is doing competitive analysis or market research
- Asks "which game has more players / better reviews / lower price"
- Needs a side-by-side feature comparison of Steam titles
- Is deciding between multiple games to buy or study

## Required Inputs

- **Game names or App IDs** - at least two games to compare

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use `steam.searchApps()`, `steam.getAppDetails()`, and `steam.getPlayerCount()` instead of the `curl` commands below. See [MCP Usage](#mcp-usage).

### 1. Resolve App IDs

For each game name, resolve to an App ID using the store search:
```bash
curl.exe "https://store.steampowered.com/api/storesearch/?term={game_name}&l=english&cc=us"
```

If the user provided App IDs directly, skip this step.

### 2. Fetch Store Data for Each Game

For each App ID:
```bash
curl.exe "https://store.steampowered.com/api/appdetails?appids={appid}"
```

Extract from `data`:
- `name`
- `price_overview.final_formatted` (or "Free" if `is_free`)
- `metacritic.score`
- `recommendations.total`
- `release_date.date`
- `genres[].description`
- `developers[]`
- `platforms` (windows, mac, linux)
- `categories[].description`

### 3. Fetch Current Player Counts

For each App ID (no API key needed):
```bash
curl.exe "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
```

### 4. Format as Comparison Table

Present the results side by side:

| | **Hades** | **Dead Cells** | **Hollow Knight** |
|---|---|---|---|
| **App ID** | 1145360 | 588650 | 367520 |
| **Price** | $24.99 | $24.99 | $14.99 |
| **Reviews** | 216K (Overwhelmingly Positive) | 98K (Overwhelmingly Positive) | 142K (Overwhelmingly Positive) |
| **Metacritic** | 93 | 89 | 87 |
| **Current Players** | 12,431 | 3,218 | 5,892 |
| **Release** | Sep 17, 2020 | Aug 7, 2018 | Feb 24, 2017 |
| **Developer** | Supergiant Games | Motion Twin | Team Cherry |
| **Genres** | Action, Indie, RPG | Action, Indie, RPG | Action, Adventure, Indie |
| **Platforms** | Win, Mac | Win, Mac, Linux | Win, Mac, Linux |

### 5. Optional Analysis

If the user asks for insights, add:
- **Price-to-review ratio** - which game offers the best perceived value
- **Player count trends** - note if a game has unusually high/low concurrent players for its age
- **Platform coverage** - flag if a game is missing Mac/Linux
- **Genre overlap** - highlight shared and unique genres

## Key References

| Resource | URL |
|----------|-----|
| Store API (appdetails) | https://wiki.teamfortress.com/wiki/User:RJackson/StorefrontAPI |
| ISteamUserStats (player counts) | https://partner.steamgames.com/doc/webapi/ISteamUserStats |

## Example Interaction

**User:** "Compare Hades, Dead Cells, and Hollow Knight - price, reviews, and current players."

**Agent:**
1. Resolves all three names to App IDs
2. Fetches store data and player counts for each
3. Formats a comparison table
4. Notes: "All three are Overwhelmingly Positive. Hollow Knight is the cheapest at $14.99 and also the oldest (2017). Hades has the highest current player count."

**User:** "Compare App IDs 570 and 730"

**Agent:**
1. Fetches data for Dota 2 (570) and Counter-Strike 2 (730)
2. Formats comparison table
3. Notes both are free-to-play with massive player counts

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured, use MCP tool calls instead of shell `curl` commands:

| Step | MCP Tool | Auth | Replaces |
|------|----------|------|----------|
| Resolve game names | `steam.searchApps({ term })` | None | `curl` to `/api/storesearch/` |
| Fetch store data (per game) | `steam.getAppDetails({ appid })` | None | `curl` to `/api/appdetails` |
| Current players (per game) | `steam.getPlayerCount({ appid })` | None | `curl` to `GetNumberOfCurrentPlayers` |

Call `steam.getAppDetails` and `steam.getPlayerCount` once per game being compared. The comparison formatting logic remains the same.

If the MCP server is not available, fall back to the `curl`-based workflow above.

## See Also

- [Steam Store Lookup](../steam-store-lookup/SKILL.md) - detailed store data for a single game
- [Steam Player Stats](../steam-player-stats/SKILL.md) - deeper stats and achievement data per game
