---
name: steam-profile-lookup
description: Look up any Steam user's public profile. Fetch player summaries, owned games with playtime, recent activity, Steam level, badges, and friend lists. Use when someone wants to check a Steam profile, see their own stats, or look up another player.
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

- **Steam identifier** — any of: vanity URL name, full profile URL, or 64-bit Steam ID
- **Steam API Key** — required for all profile endpoints (`STEAM_API_KEY` environment variable)

## Workflow

### 1. Resolve the Steam ID

If the user provides a vanity URL or profile link instead of a 64-bit Steam ID:

**From vanity URL** (e.g., `steamcommunity.com/id/gaben`):
```bash
curl.exe "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={STEAM_API_KEY}&vanityurl=gaben"
```
Returns `response.steamid`.

**From profile URL** — extract the ID:
- `steamcommunity.com/id/{vanity}` — resolve via above
- `steamcommunity.com/profiles/{steamid64}` — use directly

### 2. Fetch Player Summary

```bash
curl.exe "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steamid}"
```

Key fields in `response.players[0]`:
- `personaname` — display name
- `avatarfull` — full-size avatar URL
- `personastate` — 0=Offline, 1=Online, 2=Busy, 3=Away, 4=Snooze, 5=LookingToTrade, 6=LookingToPlay
- `profileurl` — full profile URL
- `timecreated` — account creation timestamp
- `lastlogoff` — last seen timestamp
- `communityvisibilitystate` — 1=Private, 3=Public

### 3. Fetch Owned Games with Playtime

```bash
curl.exe "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steamid}&include_appinfo=1&include_played_free_games=1&format=json"
```

Response: `response.games[]` — each has `appid`, `name`, `playtime_forever` (minutes), `playtime_2weeks`, `img_icon_url`.

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

## MCP Integration (Future)

A Steam MCP server should expose `steam.getProfile({ steamid })`, `steam.getOwnedGames({ steamid })`, and `steam.getFriends({ steamid })`. The formatting logic remains the same.
