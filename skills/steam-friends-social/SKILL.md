---
name: steam-friends-social
description: Integrate Steam social features into your game. Covers friends list, rich presence, Steam Overlay, game invites, avatars, and persona names via ISteamFriends. Use when building social features, showing friends in-game, or setting up rich presence strings.
standards-version: 1.9.0
---

# Steam Friends & Social

## Trigger

Use this skill when the user:

- Wants to display friends list or online status in their game
- Needs to set up rich presence (status text shown in friends list)
- Is implementing game invites or join-game functionality
- Asks about the Steam Overlay or avatar retrieval
- Wants to show player names or profile pictures in-game

## Required Inputs

- **App ID** - the game's Steam App ID
- **Feature** - friends list, rich presence, invites, overlay, or avatars

## Workflow

### Rich Presence

Rich presence strings appear in the Steam friends list under "In-Game."

**Set rich presence:**

**C++ (Steamworks SDK):**
```cpp
SteamFriends()->SetRichPresence("status", "In Battle - Round 3");
SteamFriends()->SetRichPresence("steam_display", "#StatusInBattle");
SteamFriends()->SetRichPresence("round", "3");
```

**C# (Steamworks.NET):**
```csharp
SteamFriends.SetRichPresence("status", "Exploring the Dungeon - Floor 12");
```

The `steam_display` key references a localization token defined in your app's Rich Presence configuration on the Steamworks Partner site.

**Clear rich presence (on menu/exit):**
```cpp
SteamFriends()->ClearRichPresence();
```

### Friends List

**Get friend count and iterate:**
```cpp
int friendCount = SteamFriends()->GetFriendCount(k_EFriendFlagImmediate);
for (int i = 0; i < friendCount; i++) {
    CSteamID friendId = SteamFriends()->GetFriendByIndex(i, k_EFriendFlagImmediate);
    const char* name = SteamFriends()->GetFriendPersonaName(friendId);
    EPersonaState state = SteamFriends()->GetFriendPersonaState(friendId);
    // state: k_EPersonaStateOnline, k_EPersonaStateAway, etc.
}
```

**Check if a friend is playing your game:**
```cpp
FriendGameInfo_t gameInfo;
if (SteamFriends()->GetFriendGamePlayed(friendId, &gameInfo)) {
    if (gameInfo.m_gameID.AppID() == myAppId) {
        // friend is playing our game, can show "join" button
    }
}
```

### Game Invites

**Invite a friend to your lobby/game:**
```cpp
SteamFriends()->InviteUserToGame(friendSteamId, "+connect_lobby {lobbyId}");
```

**Handle incoming invites** - register for `GameRichPresenceJoinRequested_t` callback:
```cpp
void OnJoinRequested(GameRichPresenceJoinRequested_t* pCallback) {
    // pCallback->m_rgchConnect contains the connect string
    // Parse and join the lobby/server
}
```

### Avatars

**Get a friend's avatar (small 32x32, medium 64x64, large 184x184):**
```cpp
int avatarHandle = SteamFriends()->GetLargeFriendAvatar(steamId);
if (avatarHandle > 0) {
    uint32 width, height;
    SteamUtils()->GetImageSize(avatarHandle, &width, &height);
    uint8* rgbaBuf = new uint8[width * height * 4];
    SteamUtils()->GetImageRGBA(avatarHandle, rgbaBuf, width * height * 4);
    // Upload to GPU texture
}
```

Avatar loading may be asynchronous - listen for `AvatarImageLoaded_t` callback.

### Steam Overlay

**Activate the overlay to a specific page:**
```cpp
SteamFriends()->ActivateGameOverlay("friends");       // friends list
SteamFriends()->ActivateGameOverlay("achievements");   // achievements
SteamFriends()->ActivateGameOverlay("community");      // community hub

SteamFriends()->ActivateGameOverlayToWebPage("https://store.steampowered.com/app/{appid}");
SteamFriends()->ActivateGameOverlayToUser("steamid", friendSteamId);  // friend's profile
```

**Check if overlay is available:**
```cpp
bool overlayEnabled = SteamUtils()->IsOverlayEnabled();
```

### Persona Names

```cpp
const char* myName = SteamFriends()->GetPersonaName();
const char* friendName = SteamFriends()->GetFriendPersonaName(friendSteamId);
```

## Key References

| Resource | URL |
|----------|-----|
| ISteamFriends API | https://partner.steamgames.com/doc/api/ISteamFriends |
| Rich Presence | https://partner.steamgames.com/doc/features/enhancedrichpresence |
| Steam Overlay | https://partner.steamgames.com/doc/features/overlay |
| Game Invites | https://partner.steamgames.com/doc/features/multiplayer/matchmaking |

## Example Interaction

**User:** "I want to show 'Playing as [CharacterName] on [MapName]' in the Steam friends list for my RPG."

**Agent:**
1. Sets up rich presence with `steam_display` token and dynamic keys
2. Shows the localization config format for the Partner site
3. Provides `SetRichPresence` calls for character name and map name
4. Adds `ClearRichPresence` call on return to main menu
5. Notes: "Rich presence updates are rate-limited. Don't call `SetRichPresence` more than once per second."

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured, you can look up player profile data:

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Player summary | `steam_getPlayerSummary({ steamid })` | Key | Fetch display name, avatar, online status, profile visibility |

The SDK integration for rich presence, overlay, game invites, friends list iteration, and avatar retrieval remains documentation-only. These are in-process ISteamFriends APIs with no Web API equivalent for the write/interactive operations.

If the MCP server is not available, fall back to the `curl`-based approach using `ISteamUser/GetPlayerSummaries`.

## Common Pitfalls

1. **Not respecting privacy settings** — `GetFriendList` only works for profiles with public friends lists. Always handle empty results gracefully.
2. **Setting Rich Presence strings that are too long** — Rich Presence values are limited to 256 bytes each and 20 keys total. Exceeding this silently truncates.
3. **Forgetting to clear Rich Presence on disconnect** — stale Rich Presence shows players as "in-game" after they've quit. Call `ClearRichPresence()` on shutdown.
4. **Using Steam IDs as display names** — always resolve Steam IDs to persona names via `GetFriendPersonaName()` or `GetPlayerSummaries`. Raw 64-bit IDs mean nothing to users.

## See Also

- [Steam Multiplayer Networking](../steam-multiplayer-networking/SKILL.md) - lobbies and matchmaking that integrate with social features
- [Steam Profile Lookup](../steam-profile-lookup/SKILL.md) - look up player profiles, avatars, and friend lists via Web API
