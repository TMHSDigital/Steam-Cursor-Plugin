---
name: steam-profile-lookup
description: Look up any Steam user's public profile. Fetch player summaries, owned games with playtime, recent activity, Steam level, badges, and friend lists. Use when someone wants to check a Steam profile, see their own stats, or look up another player.
standards-version: 1.7.0
---

# Steam Profile Lookup

## Trigger

Use this skill when the user:

- Wants to look up a Steam profile (their own or someone else's)
- Asks about a player's game library, playtime, or recent activity
- Needs to resolve a Steam vanity URL or profile link to a Steam ID
- Wants to check someone's Steam level, badges, or friend list
- Is curious about their own Steam stats

## Required Inputs

- **Steam identifier** - any of: vanity URL name, full profile URL, or 64-bit Steam ID
- **Steam API Key** - required for all profile endpoints (`STEAM_API_KEY` environment variable)

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use `steam_resolveVanityURL()`, `steam_getPlayerSummary()`, and `steam_getOwnedGames()` instead of the `curl` commands below. See [MCP Usage](#mcp-usage).

### 1. Resolve the Steam ID

If the user provides a vanity URL or profile link instead of a 64-bit Steam ID:

**From vanity URL** (e.g., `steamcommunity.com/id/gaben`):
```bash
curl.exe "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={STEAM_API_KEY}&vanityurl=gaben"
```
Returns `response.steamid`.

**From profile URL** - extract the ID:
- `steamcommunity.com/id/{vanity}` - resolve via above
- `steamcommunity.com/profiles/{steamid64}` - use directly

### 2. Fetch Player Summary

```bash
curl.exe "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steamid}"
```

Key fields in `response.players[0]`:
- `personaname` - display name
- `avatarfull` - full-size avatar URL
- `personastate` - 0=Offline, 1=Online, 2=Busy, 3=Away, 4=Snooze, 5=LookingToTrade, 6=LookingToPlay
- `profileurl` - full profile URL
- `timecreated` - account creation timestamp
- `lastlogoff` - last seen timestamp
- `communityvisibilitystate` - 1=Private, 3=Public

### 3. Fetch Owned Games with Playtime

```bash
curl.exe "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steamid}&include_appinfo=1&include_played_free_games=1&format=json"
```

Response: `response.games[]` - each has `appid`, `name`, `playtime_forever` (minutes), `playtime_2weeks`, `img_icon_url`.

Sort by `playtime_forever` descending for "most played" view.

### 4. Fetch Recent Activity

```bash
curl.exe "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={STEAM_API_KEY}&steamid={steamid}&count=5"
```

Returns the 5 most recently played games with `playtime_2weeks`.

### 5. Fetch Steam Level and Badges

```bash
curl.exe "https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={STEAM_API_KEY}&steamid={steamid}"
```

```bash
curl.exe "https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={STEAM_API_KEY}&steamid={steamid}"
```

### 6. Fetch Friend List

```bash
curl.exe "https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={STEAM_API_KEY}&steamid={steamid}&relationship=friend"
```

Returns `friendslist.friends[]` with `steamid` and `friend_since` timestamp. Only works for public profiles.

## Key References

| Resource | URL |
|----------|-----|
| ISteamUser API | https://partner.steamgames.com/doc/webapi/ISteamUser |
| IPlayerService API | https://partner.steamgames.com/doc/webapi/IPlayerService |
| Steam Community profiles | https://partner.steamgames.com/doc/features/community |

## Output Format

Present as a structured profile card:

> **Gabe Newell** (Steam ID: 76561197960287930)
> - **Status:** Online
> - **Steam Level:** 76
> - **Account Created:** September 2003
> - **Games Owned:** 614
> - **Most Played:** Counter-Strike 2 (4,231 hrs), Dota 2 (2,891 hrs), Half-Life 2 (312 hrs)
> - **Recently Played:** Counter-Strike 2 (23 hrs last 2 weeks)
> - **Profile:** https://steamcommunity.com/id/gaben

## Example Interaction

**User:** "Look up the Steam profile for vanity URL 'gaben'"

**Agent:**
1. Resolves `gaben` → Steam ID `76561197960287930`
2. Fetches player summary, owned games, recent activity, and level
3. Formats as a profile card with top games by playtime
4. Notes: "This profile is public. Private profiles will return limited data."

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured, use MCP tool calls instead of shell `curl` commands:

| Step | MCP Tool | Replaces |
|------|----------|----------|
| Resolve vanity URL | `steam_resolveVanityURL({ vanityurl })` | `curl` to `ResolveVanityURL` |
| Player summary | `steam_getPlayerSummary({ steamid })` | `curl` to `GetPlayerSummaries` |
| Owned games | `steam_getOwnedGames({ steamid, include_appinfo?, include_played_free_games? })` | `curl` to `GetOwnedGames` |

All three require `STEAM_API_KEY`. Recent activity, Steam level, badges, and friend list still require direct API calls as there are no dedicated MCP tools for those yet.

If the MCP server is not available, fall back to the `curl`-based workflow above.

## Common Pitfalls

1. **Confusing Steam ID formats** — Steam has Steam64 (76561198...), Steam32 (STEAM_0:...), and Steam3 ([U:1:...]) formats. The Web API requires Steam64. Use `ResolveVanityURL` for custom URLs.
2. **Not handling private profiles** — most profile data returns empty for private profiles. Always check `communityvisibilitystate` in the response before assuming data is available.
3. **Caching avatar URLs too long** — avatar URLs can change when users update their profile picture. Cache for minutes, not days.
4. **Assuming vanity URLs are permanent** — users can change their custom URL at any time. Always store and reference the immutable Steam64 ID, not the vanity URL.

## See Also

- [Steam Player Stats](../steam-player-stats/SKILL.md) - achievement stats and player counts for specific games
- [Steam Friends & Social](../steam-friends-social/SKILL.md) - in-game friends list, rich presence, and social features
