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

- **App ID** — for game-specific queries
- **Steam ID** (64-bit) — for player-specific queries (optional, depends on query type)
- **Steam API Key** — required for most player data endpoints (the user should have `STEAM_API_KEY` set)

## Workflow

### Current Player Count (no API key needed)

1. Fetch the current player count:
   ```bash
   curl.exe "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
   ```
2. Response: `response.player_count` — the number of players in-game right now.

### Global Achievement Percentages (no API key needed)

1. Fetch unlock percentages for all achievements:
   ```bash
   curl.exe "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid={appid}"
   ```
2. Response: `achievementpercentages.achievements[]` — each has `name` (API name) and `percent`.
3. Sort by percent descending and format as a table.

### Per-Player Achievements (API key required)

1. Fetch a specific player's achievements:
   ```bash
   curl.exe "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?appid={appid}&key={STEAM_API_KEY}&steamid={steamid}"
   ```
2. Response: `playerstats.achievements[]` — each has `apiname`, `achieved` (0/1), and `unlocktime`.
3. The player's profile must be public for this to work.

### User Stats for Game (API key required)

1. Fetch a player's stats (kills, deaths, playtime, custom stats):
   ```bash
   curl.exe "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid={appid}&key={STEAM_API_KEY}&steamid={steamid}"
   ```
2. Response: `playerstats.stats[]` — each has `name` and `value`.

### Owned Games / Playtime (API key required)

1. Fetch a player's game library with playtime:
   ```bash
   curl.exe "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steamid}&include_appinfo=1&include_played_free_games=1"
   ```
2. Response: `response.games[]` — each has `appid`, `name`, `playtime_forever` (minutes), `playtime_2weeks`.

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

## MCP Integration (Future)

A Steam MCP server should expose `steam.getPlayerCount({ appid })`, `steam.getAchievementStats({ appid })`, and `steam.getUserStats({ appid, steamid })`. The formatting and analysis logic remains the same.
