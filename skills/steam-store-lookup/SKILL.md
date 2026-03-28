---
name: steam-store-lookup
description: Look up any Steam game or app by name or App ID. Returns store page data including price, description, tags, reviews, release date, and system requirements. Use when the user asks about a Steam game, wants to check competitor pricing, or needs store metadata.
---

# Steam Store Lookup

## Trigger

Use this skill when the user:

- Asks about a specific Steam game or application
- Wants pricing, review scores, or store metadata for a game
- Needs system requirements for a title
- Wants to compare games or check competitor store pages
- Mentions a Steam App ID or game name in a store context

## Required Inputs

- **Game name** or **App ID** (numeric). At least one must be provided.

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use `steam_searchApps()` and `steam_getAppDetails()` instead of the `curl` commands below. See [MCP Usage](#mcp-usage).

1. **Resolve the App ID.** If the user provided a game name instead of an App ID:
   - Use the Shell tool to search the Steam store:
     ```
     curl.exe "https://store.steampowered.com/api/storesearch/?term={game_name}&l=english&cc=us"
     ```
   - The response contains `items[]` with `id` (App ID), `name`, and `price` fields.
   - If the top result matches the user's query, use that App ID. If multiple results look relevant, present the top candidates and ask the user to confirm.
   - **Fallback:** If the store search returns no results, use WebSearch to find the game's Steam page and extract the App ID from the URL (`store.steampowered.com/app/{appid}`).

2. **Fetch store details.** With the confirmed App ID:
   ```
   curl.exe "https://store.steampowered.com/api/appdetails?appids={appid}"
   ```
   The response JSON is keyed by the App ID string. Check `{appid}.success` is `true`, then read `{appid}.data`.

3. **Extract and present key fields:**
   - **Name**: `data.name`
   - **Type**: `data.type` (game, dlc, demo, etc.)
   - **Description**: `data.short_description`
   - **Price**: `data.price_overview.final_formatted` (or "Free to Play" if `data.is_free`)
   - **Release date**: `data.release_date.date`
   - **Developers / Publishers**: `data.developers[]`, `data.publishers[]`
   - **Genres**: `data.genres[].description`
   - **Categories**: `data.categories[].description` (multiplayer, controller support, etc.)
   - **Metacritic**: `data.metacritic.score` and `data.metacritic.url`
   - **Recommendations**: `data.recommendations.total`
   - **Platforms**: `data.platforms` (windows, mac, linux booleans)
   - **System requirements**: `data.pc_requirements`, `data.mac_requirements`, `data.linux_requirements`
   - **Steam page URL**: `https://store.steampowered.com/app/{appid}`

4. **Format output** as a structured summary. Use a table or bullet list depending on what the user asked for.

## API Reference

| Endpoint | Purpose | Auth Required |
|----------|---------|---------------|
| `https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=us` | Search store by game name | No |
| `https://api.steampowered.com/ISteamApps/GetAppList/v2/` | Full app list (large response, use sparingly) | No |
| `https://store.steampowered.com/api/appdetails?appids={appid}` | Store page details | No |
| `https://store.steampowered.com/api/appdetails?appids={appid}&cc={country}&l={language}` | Localized / regional pricing | No |

### Regional pricing

Append `&cc=us` (ISO country code) and `&l=english` (language) to get localized prices. Useful for comparing regional pricing.

## Example Interaction

**User:** "What's the current price and review score for Hades?"

**Agent:**
1. Searches store for "Hades", finds App ID `1145360`
2. Fetches `appdetails?appids=1145360`
3. Responds:

> **Hades** (App ID: 1145360)
> - **Price:** $24.99
> - **Reviews:** 216,000+ (Overwhelmingly Positive)
> - **Release:** September 17, 2020
> - **Developer:** Supergiant Games
> - **Genres:** Action, Indie, RPG
> - **Platforms:** Windows, macOS
> - **Store:** https://store.steampowered.com/app/1145360

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured, use MCP tool calls instead of shell `curl` commands:

| Step | MCP Tool | Replaces |
|------|----------|----------|
| Search by name | `steam_searchApps({ query })` | `curl` to `/api/storesearch/` |
| Fetch store data | `steam_getAppDetails({ appid, cc?, l? })` | `curl` to `/api/appdetails` |

Both tools require no API key. Optional `cc` (country code) and `l` (language) params support regional/localized results.

The data extraction and formatting logic remains the same. If the MCP server is not available, fall back to the `curl`-based workflow above.

## Common Pitfalls

1. **Assuming `appdetails` always returns data** — region-locked, delisted, or unreleased apps return `{ success: false }`. Always check the `success` field.
2. **Not specifying `&cc=` for regional data** — without a country code, the API returns data for the server's region, which may not match the user's intent.
3. **Confusing App IDs with Sub IDs or Package IDs** — the store API uses App IDs. Sub/Package IDs are different entities used for purchasing and licensing.
4. **Caching store data too aggressively** — prices, descriptions, and review scores change. Cache for minutes during active use, not hours or days.

## See Also

- [Steam Game Comparison](../steam-game-comparison/SKILL.md) - compare multiple games side by side
- [Steam Player Stats](../steam-player-stats/SKILL.md) - player counts and achievement data for a game
