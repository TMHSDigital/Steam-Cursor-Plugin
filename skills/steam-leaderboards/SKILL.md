---
name: steam-leaderboards
description: Implement and query Steam Leaderboards. Covers creating leaderboards, uploading scores, downloading entries (global, friends, around-user), and Web API queries. Use when adding leaderboards to a game or querying leaderboard data.
standards-version: 1.6.3
---

# Steam Leaderboards

## Trigger

Use this skill when the user:

- Wants to add leaderboards to their Steam game
- Needs to upload scores or download leaderboard entries
- Asks about leaderboard types (ascending, descending, friends-only)
- Wants to query leaderboard data via the Web API
- Is implementing a high-score or ranking system

## Required Inputs

- **App ID** - the game's Steam App ID
- **Leaderboard name** - the identifier for the leaderboard
- **Sort method** - ascending (speedruns, golf) or descending (high scores)

## Workflow

### Create Leaderboards

Leaderboards can be created in the Steamworks Partner site or via SDK at runtime.

**Partner site:** App Admin > Stats & Achievements > Leaderboards > New Leaderboard

**SDK (created on first use if it doesn't exist):**

**C++ (Steamworks SDK):**
```cpp
SteamUserStats()->FindOrCreateLeaderboard("BestTime_Level1",
    k_ELeaderboardSortMethodAscending,
    k_ELeaderboardDisplayTypeTimeMilliSeconds);
// Handle result in FindLeaderboardResult_t callback
```

Sort methods: `k_ELeaderboardSortMethodAscending`, `k_ELeaderboardSortMethodDescending`
Display types: `k_ELeaderboardDisplayTypeNumeric`, `k_ELeaderboardDisplayTypeTimeSeconds`, `k_ELeaderboardDisplayTypeTimeMilliSeconds`

### Upload Scores

```cpp
SteamUserStats()->UploadLeaderboardScore(leaderboardHandle,
    k_ELeaderboardUploadScoreMethodKeepBest,
    score,
    scoreDetails, // optional int32 array for extra data
    detailsCount);
```

**C# (Steamworks.NET):**
```csharp
SteamUserStats.UploadLeaderboardScore(handle,
    ELeaderboardUploadScoreMethod.k_ELeaderboardUploadScoreMethodKeepBest,
    score, null, 0);
```

Upload methods: `KeepBest` (only update if better) or `ForceUpdate` (always overwrite).

### Download Entries

**Global top scores:**
```cpp
SteamUserStats()->DownloadLeaderboardEntries(handle,
    k_ELeaderboardDataRequestGlobal, 1, 10);
```

**Around the current user:**
```cpp
SteamUserStats()->DownloadLeaderboardEntries(handle,
    k_ELeaderboardDataRequestGlobalAroundUser, -4, 5);
```

**Friends only:**
```cpp
SteamUserStats()->DownloadLeaderboardEntries(handle,
    k_ELeaderboardDataRequestFriends, 0, 0);
```

**Processing results (in callback):**
```cpp
void OnDownloadEntries(LeaderboardScoresDownloaded_t* result) {
    for (int i = 0; i < result->m_cEntryCount; i++) {
        LeaderboardEntry_t entry;
        SteamUserStats()->GetDownloadedLeaderboardEntry(
            result->m_hSteamLeaderboardEntries, i, &entry, nullptr, 0);
        // entry.m_steamIDUser, entry.m_nGlobalRank, entry.m_nScore
    }
}
```

### Web API Queries

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use `steam_getLeaderboardEntries()` instead of the `curl` command below. See [MCP Usage](#mcp-usage).

**Get leaderboard entries (API key required):**
```bash
curl.exe "https://api.steampowered.com/ISteamLeaderboards/GetLeaderboardEntries/v1/?appid={appid}&leaderboardid={id}&rangestart=0&rangeend=10&datarequest=0&key={STEAM_API_KEY}"
```

Data request types: `0` = global, `1` = global around user, `2` = friends.

### GDScript Example (GodotSteam)

```gdscript
func _ready():
    Steam.leaderboard_find_result.connect(_on_leaderboard_found)
    Steam.findLeaderboard("BestTime_Level1")

func _on_leaderboard_found(handle: int, found: int):
    if found:
        Steam.uploadLeaderboardScore(score, true, [], handle)
        Steam.downloadLeaderboardEntries(1, 10, Steam.LEADERBOARD_DATA_REQUEST_GLOBAL, handle)
```

## Key References

| Resource | URL |
|----------|-----|
| Leaderboards overview | https://partner.steamgames.com/doc/features/leaderboards |
| Step-by-step guide | https://partner.steamgames.com/doc/features/leaderboards/guide |
| ISteamUserStats API | https://partner.steamgames.com/doc/api/ISteamUserStats |
| Web API: ISteamLeaderboards | https://partner.steamgames.com/doc/webapi/ISteamLeaderboards |

## Example Interaction

**User:** "I have a speedrun game and want to add a leaderboard for each level. Times are in milliseconds, lower is better."

**Agent:**
1. Creates leaderboards with `Ascending` sort and `TimeMilliSeconds` display
2. Shows `FindOrCreateLeaderboard` for each level (`BestTime_Level1`, `BestTime_Level2`, etc.)
3. Implements score upload with `KeepBest` method
4. Downloads and displays global top 10 + around-user entries
5. Notes: "Create leaderboards in Partner site for production. SDK creation is useful for development but can't set all options."

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured, use MCP tool calls instead of shell `curl` commands:

| Step | MCP Tool | Auth | Replaces |
|------|----------|------|----------|
| Get leaderboard entries | `steam_getLeaderboardEntries({ appid, leaderboardid, rangestart?, rangeend?, datarequest?, steamid? })` | Key | `curl` to `ISteamLeaderboards/GetLeaderboardEntries` |
| List leaderboards | `steam_getLeaderboardsForGame({ appid })` | Key | Discover leaderboard numeric IDs by name |

The `datarequest` param controls the view: `0` = Global, `1` = Around user, `2` = Friends. When using `1` or `2`, provide the `steamid` param.

> **Note:** `steam_getLeaderboardEntries` calls the partner API (`partner.steam-api.com`), which requires a publisher API key with your server's IP allowlisted in the Steamworks partner site. A standard user API key from `steamcommunity.com/dev/apikey` will return HTTP 403. This is a Valve restriction, not an MCP server issue.

The SDK integration for creating leaderboards, uploading scores, and downloading entries in-game remains documentation-only.

If the MCP server is not available, fall back to the `curl`-based workflow above.

## Common Pitfalls

1. **Not calling `FindLeaderboard()` before uploading scores** — you must resolve the leaderboard name to a handle first. Uploading to an invalid handle silently fails.
2. **Using the wrong sort method** — setting a leaderboard to ascending when scores should be descending (or vice versa) reverses rankings. This can only be changed by creating a new leaderboard.
3. **Uploading scores with `ForceUpdate` in production** — `ForceUpdate` overwrites the player's best score. Use `KeepBest` unless you intentionally want to allow score resets.
4. **Not considering score spoofing** — leaderboard scores uploaded client-side can be manipulated. For competitive games, upload scores server-side via the partner API.
5. **Exceeding the leaderboard detail data limit** — detail data attached to leaderboard entries is limited to 64 int32 values (256 bytes). Don't try to store replays or complex data there.

## See Also

- [Steam Player Stats](../steam-player-stats/SKILL.md) - player counts, achievement stats, and playtime data
- [Steam Multiplayer Networking](../steam-multiplayer-networking/SKILL.md) - lobby and matchmaking setup for competitive games
