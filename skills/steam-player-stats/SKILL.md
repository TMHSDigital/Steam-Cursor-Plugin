---
name: steam-player-stats
description: Look up player and game statistics including player counts, achievement stats, leaderboards, and user game libraries for public profiles. Use when analyzing game performance, checking player engagement, or building features that consume player data.
---

# Steam Player Stats

## Trigger

Use this skill when the user:

- Asks how many players are currently playing a game
- Wants achievement unlock percentages or player achievement data
- Needs playtime or library data for a Steam user
- Is building analytics or dashboards around Steam player data
- Asks about leaderboard data or stat tracking

## Required Inputs

- **App ID** - for game-specific queries
- **Steam ID** (64-bit) - for player-specific queries (optional, depends on query type)
- **Steam API Key** - required for most player data endpoints (the user should have `STEAM_API_KEY` set)

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use `steam_getPlayerCount()`, `steam_getAchievementStats()`, and `steam_getOwnedGames()` instead of the `curl` commands below. See [MCP Usage](#mcp-usage).

### Current Player Count (no API key needed)

1. Fetch the current player count:
   ```bash
   curl.exe "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
   ```
2. Response: `response.player_count` - the number of players in-game right now.

### Global Achievement Percentages (no API key needed)

1. Fetch unlock percentages for all achievements:
   ```bash
   curl.exe "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid={appid}"
   ```
2. Response: `achievementpercentages.achievements[]` - each has `name` (API name) and `percent`.
3. Sort by percent descending and format as a table.

### Per-Player Achievements (API key required)

1. Fetch a specific player's achievements:
   ```bash
   curl.exe "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?appid={appid}&key={STEAM_API_KEY}&steamid={steamid}"
   ```
2. Response: `playerstats.achievements[]` - each has `apiname`, `achieved` (0/1), and `unlocktime`.
3. The player's profile must be public for this to work.

### User Stats for Game (API key required)

1. Fetch a player's stats (kills, deaths, playtime, custom stats):
   ```bash
   curl.exe "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid={appid}&key={STEAM_API_KEY}&steamid={steamid}"
   ```
2. Response: `playerstats.stats[]` - each has `name` and `value`.

### Owned Games / Playtime (API key required)

1. Fetch a player's game library with playtime:
   ```bash
   curl.exe "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steamid}&include_appinfo=1&include_played_free_games=1"
   ```
2. Response: `response.games[]` - each has `appid`, `name`, `playtime_forever` (minutes), `playtime_2weeks`.

### Steam ID Resolution

If the user provides a vanity URL or profile link instead of a 64-bit Steam ID:
```bash
curl.exe "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={STEAM_API_KEY}&vanityurl={vanity_name}"
```
Returns `response.steamid`.

## Output Format

Present data in tables or structured lists. Example for player count:

> **Counter-Strike 2** (App ID: 730)
> Current Players: 842,319

Example for achievement stats:

| Achievement | Unlock Rate |
|-------------|-------------|
| First Blood | 87.3% |
| Complete Tutorial | 72.1% |
| Beat Final Boss | 14.8% |

## Example Interaction

**User:** "How many people are playing Elden Ring right now? And what are the rarest achievements?"

**Agent:**
1. Resolves "Elden Ring" → App ID `1245620`
2. Fetches current player count → e.g., 45,231
3. Fetches global achievement percentages, sorts ascending
4. Presents current players + bottom-5 rarest achievements in a table

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured, use MCP tool calls instead of shell `curl` commands:

| Step | MCP Tool | Auth | Replaces |
|------|----------|------|----------|
| Current player count | `steam_getPlayerCount({ appid })` | None | `curl` to `GetNumberOfCurrentPlayers` |
| Global achievement stats | `steam_getAchievementStats({ appid })` | None | `curl` to `GetGlobalAchievementPercentagesForApp` |
| Owned games / playtime | `steam_getOwnedGames({ steamid })` | Key | `curl` to `GetOwnedGames` |
| Resolve vanity URL | `steam_resolveVanityURL({ vanityurl })` | Key | `curl` to `ResolveVanityURL` |
| Per-player achievements | `steam_getPlayerAchievements({ steamid, appid })` | Key | `curl` to `GetPlayerAchievements` |

User stats still require direct API calls (`GetUserStatsForGame`) as there is no dedicated MCP tool for that yet.

If the MCP server is not available, fall back to the `curl`-based workflow above.

## Common Pitfalls

1. **Confusing concurrent players with total owners** — `GetNumberOfCurrentPlayers` returns who's playing right now, not total sales. A game with 500 concurrent might have 500K owners.
2. **Querying player stats too frequently** — Steam rate-limits API calls. Cache responses for at least 5-10 minutes instead of polling every second.
3. **Not handling private profiles** — many players have private profiles. `GetPlayerAchievements` and `GetOwnedGames` return empty or error for private profiles. Always check the response status.
4. **Comparing achievement percentages across different-sized games** — a 50% unlock rate on a game with 1K owners is ~500 players. The same rate on a game with 1M owners is ~500K players. Context matters.

## See Also

- [Steam Leaderboards](../steam-leaderboards/SKILL.md) - create and query leaderboards
- [Steam Profile Lookup](../steam-profile-lookup/SKILL.md) - full profile data including owned games and playtime
- [Steam Game Comparison](../steam-game-comparison/SKILL.md) - compare player counts and stats across games
