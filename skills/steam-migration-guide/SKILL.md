---
name: steam-migration-guide
description: Guide for migrating games to Steam from other platforms (Epic, GOG, itch.io) or integrating Steamworks across engines (Unity, Unreal, Godot). Covers feature parity mapping, SDK integration steps, store page strategy, and technical migration checklists. Use when porting an existing game to Steam or adding Steamworks to a multi-platform title.
---

# Steam Migration Guide

## Trigger

Use this skill when the user:

- Wants to bring an existing game to Steam from another storefront
- Is porting from Epic Games Store, GOG, itch.io, or console to Steam
- Needs to integrate Steamworks SDK into an engine (Unity, Unreal, Godot)
- Asks about feature parity between platforms (achievements, cloud saves, etc.)
- Wants a checklist for launching an existing game on Steam

## Required Inputs

- **Source platform** - where the game currently lives (Epic, GOG, itch.io, console, self-published)
- **Game engine** - Unity, Unreal, Godot, custom, or native C++
- **Features to migrate** - achievements, cloud saves, multiplayer, leaderboards, etc.

## Workflow

### 1. Platform Feature Parity Mapping

Map existing platform features to their Steam equivalents:

| Feature | Epic Games Store | GOG Galaxy | itch.io | Steam |
|---------|-----------------|------------|---------|-------|
| Achievements | Epic Achievements | GOG Achievements | None | ISteamUserStats |
| Cloud Saves | Epic Cloud Saves | GOG Cloud Saves | None | ISteamRemoteStorage / Auto-Cloud |
| Multiplayer | Epic Online Services | GOG Galaxy Multiplayer | None | Steam Networking Sockets |
| Leaderboards | Epic Leaderboards | None | None | ISteamLeaderboards |
| Friends/Social | Epic Social Overlay | GOG Galaxy Friends | None | ISteamFriends |
| DRM | None (DRM-free option) | DRM-free | DRM-free | SteamDRM (optional) |
| Workshop/UGC | Epic Mods (limited) | GOG Workshop (limited) | None | ISteamUGC |
| In-App Purchases | Epic Commerce | None | Payments API | ISteamMicroTxn |
| Overlay | Epic Overlay | GOG Overlay | None | Steam Overlay |
| Input | None | None | None | ISteamInput |
| Rich Presence | Epic Presence | GOG Rich Presence | None | ISteamFriends Rich Presence |

### 2. Engine-Specific SDK Integration

**Unity (Steamworks.NET or Facepunch.Steamworks):**

```csharp
// Steamworks.NET - most common, C# wrapper
// Install via Unity Package Manager or download from GitHub
// https://github.com/rlabrecque/Steamworks.NET

using Steamworks;

void Awake() {
    if (!SteamAPI.Init()) {
        Debug.LogError("Steam failed to initialize");
        return;
    }
}

void OnDestroy() {
    SteamAPI.Shutdown();
}

void Update() {
    SteamAPI.RunCallbacks();
}
```

```csharp
// Facepunch.Steamworks - modern alternative, more idiomatic C#
// Install via NuGet or Unity Package Manager
// https://github.com/Facepunch/Facepunch.Steamworks

using Steamworks;

void Awake() {
    SteamClient.Init(YOUR_APP_ID);
}

void OnDestroy() {
    SteamClient.Shutdown();
}

void Update() {
    SteamClient.RunCallbacks();
}
```

**Unreal Engine (OnlineSubsystemSteam):**

```ini
; DefaultEngine.ini
[/Script/Engine.GameEngine]
+NetDriverDefinitions=(DefName="GameNetDriver",DriverClassName="OnlineSubsystemSteam.SteamNetDriver",DriverClassNameFallback="OnlineSubsystemUtils.IpNetDriver")

[OnlineSubsystem]
DefaultPlatformService=Steam

[OnlineSubsystemSteam]
bEnabled=true
SteamDevAppId=480
```

**Godot (GodotSteam):**

```gdscript
# Install GodotSteam plugin from Asset Library or compile from source
# https://godotsteam.com

func _ready() -> void:
    var init = Steam.steamInitEx(false, YOUR_APP_ID)
    if init.status != Steam.STEAM_API_INIT_RESULT_OK:
        print("Steam init failed: %s" % init.verbal)

func _process(_delta: float) -> void:
    Steam.run_callbacks()
```

### 3. Migration Checklist

**Steamworks Partner Setup:**
1. Create Steamworks partner account (if new to Steam)
2. Pay the Steam Direct fee ($100 per app, recoupable)
3. Set up App ID, depot configuration, and build pipelines
4. Configure store page: capsule images, screenshots, trailers, description

**SDK Integration:**
1. Download Steamworks SDK or engine-specific wrapper
2. Create `steam_appid.txt` with your App ID for development
3. Initialize `SteamAPI_Init()` at startup
4. Call `SteamAPI_RunCallbacks()` every frame
5. Implement `SteamAPI_Shutdown()` at exit

**Feature Migration:**
1. Map existing achievements to Steam achievements (configure in Steamworks Partner)
2. Migrate cloud save paths to ISteamRemoteStorage or configure Auto-Cloud
3. Replace platform-specific multiplayer with Steam Networking Sockets
4. Create Steam leaderboards for any existing leaderboards
5. Set up Steam Input action sets if you have controller support
6. Configure Rich Presence strings

**Testing:**
1. Test with App ID 480 (SpaceWar) first for SDK basics
2. Switch to your real App ID and test all features
3. Verify Steam Overlay works
4. Test on Steam Deck if applicable
5. Run through the release checklist

### 4. Store Page Strategy for Migrated Games

**Key considerations:**
- Reviews do NOT transfer from other platforms
- Wishlists must be built from scratch on Steam
- "Coming to Steam" announcements can drive early wishlists
- Consider a launch discount to incentivize purchases from existing fans
- Cross-platform save migration is a strong selling point if feasible

**Timeline recommendation:**
1. **3-6 months before launch**: Set up store page, start wishlist collection
2. **1-3 months before**: Submit store page for review, prepare marketing materials
3. **2 weeks before**: Upload release candidate build, configure launch settings
4. **Launch day**: Publish, announce on all platforms, engage community

### 5. Cross-Platform Considerations

**Save file compatibility:**
- Use platform-agnostic serialization (JSON, Protocol Buffers)
- Avoid endianness-dependent binary formats
- Test save file loading across platforms

**Achievement mapping:**
- Document a mapping table between platform achievement IDs
- Consider unlocking Steam achievements retroactively if you can verify progress

**Multiplayer cross-play:**
- Steam Networking Sockets supports non-Steam platforms via `ISteamNetworkingMessages`
- Epic Online Services and Steam can coexist for cross-play
- GOG Galaxy SDK can interop with Steam for some features

## Common Pitfalls

1. **Forgetting `SteamAPI_RunCallbacks()`** — callbacks never fire, achievements don't save, overlay breaks. Must be called every frame.
2. **Shipping with `steam_appid.txt` in the release build** — bypasses Steam's DRM and ownership checks. Remove before release or use `SteamAPI_RestartAppIfNecessary()`.
3. **Assuming reviews transfer** — Steam reviews are platform-specific. Plan for zero reviews at Steam launch regardless of your game's reputation elsewhere.
4. **Using the wrong Steamworks wrapper version** — Steamworks.NET and Facepunch.Steamworks have different APIs. Pick one and stick with it; don't mix.
5. **Not testing the Steam Overlay** — overlay requires the game to be launched through Steam (or via `steam_appid.txt`). Test early — some rendering setups (Vulkan, certain OpenGL contexts) need explicit overlay support.
6. **Skipping Steam Deck testing** — Deck verification is free marketing. Use the `steam-deck-compat` rule to catch common issues before submission.

## Key References

| Resource | URL |
|----------|-----|
| Steamworks Getting Started | https://partner.steamgames.com/doc/sdk |
| Steamworks.NET (Unity) | https://github.com/rlabrecque/Steamworks.NET |
| Facepunch.Steamworks (Unity) | https://github.com/Facepunch/Facepunch.Steamworks |
| OnlineSubsystemSteam (Unreal) | https://docs.unrealengine.com/en-US/ProgrammingAndScripting/Online/Steam/ |
| GodotSteam | https://godotsteam.com |
| Steam Direct | https://partner.steamgames.com/steamdirect |

## Example Interaction

**User:** "I have a game on itch.io built with Godot. I want to bring it to Steam with achievements and cloud saves. Where do I start?"

**Agent:**
1. Outlines the migration path: Steamworks Partner account, App ID, GodotSteam plugin
2. Provides GodotSteam initialization code
3. Maps itch.io features (none for achievements/cloud) to Steam equivalents
4. Walks through achievement configuration in Steamworks Partner
5. Shows Auto-Cloud setup for save files
6. Provides the migration checklist with itch.io-specific notes
7. Recommends store page setup timeline

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Verify App ID | `steam_getAppDetails({ appid })` | None | Check if your App ID is live and configured |
| Search competitors | `steam_searchApps({ term })` | None | Find similar games already on Steam |
| Check player counts | `steam_getPlayerCount({ appid })` | None | Benchmark against comparable titles |
| Test achievements | `steam_setAchievement({ steamid, appid, achievement })` | Publisher key | Verify achievements work via partner API |
| Test leaderboards | `steam_uploadLeaderboardScore({ appid, leaderboardid, steamid, score })` | Publisher key | Verify leaderboard uploads |

## See Also

- [Steamworks App Config](../steamworks-app-config/SKILL.md) - depot and build configuration
- [Steam Release Checklist](../steam-release-checklist/SKILL.md) - pre-launch validation
- [Steam Store Page Optimizer](../steam-store-page-optimizer/SKILL.md) - store page best practices
- [Steam Testing Sandbox](../steam-testing-sandbox/SKILL.md) - development testing with App ID 480
- [Steam Cloud Saves](../steam-cloud-saves/SKILL.md) - ISteamRemoteStorage and Auto-Cloud
- [Steam Achievement Designer](../steam-achievement-designer/SKILL.md) - achievement design and configuration
