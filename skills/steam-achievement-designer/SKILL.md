---
name: steam-achievement-designer
description: Design and document Steam achievements. Helps structure achievement definitions (API name, display name, description, icon requirements, hidden flag) and generates the VDF/JSON config snippets for Steamworks upload. Use when planning or implementing achievements.
standards-version: 1.7.0
---

# Steam Achievement Designer

## Trigger

Use this skill when the user:

- Is planning achievements for a Steam game
- Needs to generate achievement configuration files (VDF or JSON)
- Asks about achievement icon requirements or naming conventions
- Wants to structure achievement data for Steamworks upload
- Is implementing achievement unlocking in their game code

## Required Inputs

- **Achievement list** - at minimum, names and descriptions for each achievement
- **App ID** - the game's Steam App ID (for code examples)

## Workflow

### 1. Structure Achievement Definitions

For each achievement, define these fields:

| Field | Description | Example |
|-------|-------------|---------|
| `apiname` | Unique identifier (uppercase, underscores, no spaces) | `ACH_WIN_FIRST_GAME` |
| `displayName` | Player-facing name | `First Victory` |
| `description` | Player-facing description | `Win your first multiplayer match` |
| `hidden` | `0` = visible, `1` = hidden until unlocked | `0` |
| `icon` | Path to unlocked icon (JPG/PNG, 64x64) | `achievements/ach_win_first_game.jpg` |
| `icon_gray` | Path to locked icon (64x64, grayscale recommended) | `achievements/ach_win_first_game_gray.jpg` |

### 2. Naming Conventions

- API names: `ACH_` prefix, uppercase, underscores. E.g., `ACH_COLLECT_ALL_ITEMS`
- Keep API names stable - changing them after release breaks existing unlock data
- Display names: title case, concise (under 64 characters)
- Descriptions: one sentence, under 128 characters, describe the unlock condition

### 3. Icon Requirements

- Format: JPG or PNG
- Size: exactly **64x64 pixels**
- Two versions per achievement: color (unlocked) and gray (locked)
- Consistent art style across all achievement icons
- Avoid text in icons (doesn't scale well in Steam UI)

### 4. Generate VDF Config

For Steamworks bulk upload, generate a VDF file:

```vdf
"achievements"
{
  "0"
  {
    "name" "ACH_WIN_FIRST_GAME"
    "displayName"
    {
      "english" "First Victory"
    }
    "description"
    {
      "english" "Win your first multiplayer match"
    }
    "hidden" "0"
    "icon" "achievements/ach_win_first_game.jpg"
    "icon_gray" "achievements/ach_win_first_game_gray.jpg"
  }
  "1"
  {
    "name" "ACH_COLLECT_100"
    "displayName"
    {
      "english" "Collector"
    }
    "description"
    {
      "english" "Collect 100 items"
    }
    "hidden" "0"
    "icon" "achievements/ach_collect_100.jpg"
    "icon_gray" "achievements/ach_collect_100_gray.jpg"
  }
}
```

### 5. Generate JSON Config (alternative)

For tools or pipelines that prefer JSON:

```json
{
  "achievements": [
    {
      "apiname": "ACH_WIN_FIRST_GAME",
      "displayName": "First Victory",
      "description": "Win your first multiplayer match",
      "hidden": false,
      "icon": "achievements/ach_win_first_game.jpg",
      "icon_gray": "achievements/ach_win_first_game_gray.jpg"
    }
  ]
}
```

### 6. In-Game Unlock Code Examples

**C++ (Steamworks SDK):**
```cpp
SteamUserStats()->SetAchievement("ACH_WIN_FIRST_GAME");
SteamUserStats()->StoreStats();
```

**C# (Steamworks.NET):**
```csharp
SteamUserStats.SetAchievement("ACH_WIN_FIRST_GAME");
SteamUserStats.StoreStats();
```

**GDScript (GodotSteam):**
```gdscript
Steam.setAchievement("ACH_WIN_FIRST_GAME")
Steam.storeStats()
```

Always call `StoreStats()` after setting achievements to persist them to Steam servers.

### 7. Validation Checklist

- [ ] All API names are unique and follow `ACH_` prefix convention
- [ ] No API name exceeds 128 characters
- [ ] Display names are under 64 characters
- [ ] Descriptions are under 128 characters
- [ ] Each achievement has both color and gray icon at 64x64
- [ ] Hidden achievements have non-spoiler descriptions (or empty description)
- [ ] Total achievement count is reasonable (Steam has no hard limit, but 100-300 is typical)

## Key References

| Resource | URL |
|----------|-----|
| Achievements overview | https://partner.steamgames.com/doc/features/achievements |
| ISteamUserStats API | https://partner.steamgames.com/doc/api/ISteamUserStats |
| Achievement icon specs | https://partner.steamgames.com/doc/features/achievements#4 |

## Example Interaction

**User:** "I need achievements for my platformer. Here are the milestones: complete tutorial, beat world 1, beat world 2, beat world 3, beat the final boss, collect all coins, speedrun under 2 hours, die 100 times."

**Agent:**
1. Structures each achievement with API name, display name, description, hidden flag
2. Marks "beat the final boss" as hidden (spoiler)
3. Generates the complete VDF config file
4. Provides C++ unlock code snippets for each
5. Notes icon requirements and suggests consistent naming for icon files

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured, you can fetch existing achievement data to inform new designs:

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Get existing achievements | `steam_getAchievementStats({ appid })` | None | Fetch global unlock percentages to see what players actually unlock |
| Get achievement names/descriptions | `steam_getSchemaForGame({ appid })` | Key | Fetch display names, descriptions, and icons for all achievements |

This is useful for reviewing an existing game's achievement distribution before designing new ones, or for auditing unlock rates on your own game.

The design guidance, VDF/JSON generation, naming conventions, icon requirements, and SDK unlock code remain the same regardless of MCP availability.

## Common Pitfalls

1. **Forgetting `StoreStats()` after `SetAchievement()`** — achievements are only saved locally until you call `SteamUserStats()->StoreStats()`. Without it, progress is lost on restart.
2. **Using spaces or special characters in API names** — achievement API names must be alphanumeric with underscores (e.g. `ACH_BEAT_BOSS_1`). Spaces cause silent failures.
3. **Exceeding the 1000 achievement limit** — Steam enforces a hard cap of ~5000 stat/achievement entries per app. Plan achievement lists before implementation.
4. **Not calling `RequestCurrentStats()` at startup** — the stats system won't work until you request the current user's stats. Must be called once before any `Get`/`Set` operations.
5. **Unlocking achievements in offline mode without testing** — achievements queued offline are sent when the user reconnects, but only if `StoreStats()` was called. Test this flow.

## See Also

- [Steam Player Stats](../steam-player-stats/SKILL.md) - query achievement unlock rates to inform achievement design
