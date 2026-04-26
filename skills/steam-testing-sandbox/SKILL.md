---
name: steam-testing-sandbox
description: Guide for using Steam's development sandbox environment. Covers App ID 480 (SpaceWar) for testing, test account setup, Steam client console commands, Steamworks partner test environments, and testing achievements/leaderboards/inventory without affecting production. Use when setting up a Steamworks development or testing workflow.
standards-version: 1.9.0
---

# Steam Testing Sandbox

## Trigger

Use this skill when the user:

- Wants to test Steamworks features without a published game
- Asks about App ID 480 or SpaceWar for development
- Needs to set up test accounts for Steam multiplayer testing
- Wants to use the Steam client developer console
- Asks about testing achievements, leaderboards, or inventory in development
- Needs to test features before deploying to production

## Required Inputs

- **Feature to test** - what Steamworks feature the user wants to develop against (achievements, multiplayer, cloud saves, etc.)
- **App ID** (optional) - their game's App ID if they have one, otherwise they'll use 480

## Workflow

### 1. App ID 480 — SpaceWar Test App

SpaceWar (App ID 480) is Valve's official Steamworks SDK test application. Every Steam developer can use it for development without requesting their own App ID.

**What works with App ID 480:**
- `SteamAPI_Init()` and basic Steamworks SDK calls
- Achievements (SpaceWar has pre-configured achievements)
- Leaderboards (SpaceWar has pre-configured leaderboards)
- Steam Networking Sockets (P2P and relay)
- Lobby creation and matchmaking
- Cloud saves (ISteamRemoteStorage)
- Steam Input / controller support
- Steam Overlay
- Friends list and rich presence

**What does NOT work with App ID 480:**
- Workshop uploads (you need your own App ID)
- Steam Inventory / item economy (needs your own item definitions)
- DLC ownership checks (no DLC configured for SpaceWar)
- Store page features (you can't edit SpaceWar's store page)
- Custom achievements (you get SpaceWar's, not your own)
- Anti-cheat configuration

**Setup:**

Create `steam_appid.txt` in your project's working directory:

```
480
```

Then initialize Steamworks in your code:

```cpp
// Skip the restart check during development
if (SteamAPI_RestartAppIfNecessary(480)) {
    // In production, this exits and relaunches via Steam
    // During dev with steam_appid.txt, this is bypassed
}
if (!SteamAPI_Init()) {
    // Steam client not running or steam_appid.txt missing
}
```

### 2. Using Your Own App ID

Once you have a Steamworks partner account and your own App ID:

1. Replace `480` in `steam_appid.txt` with your App ID
2. Configure your features in Steamworks Partner (achievements, leaderboards, etc.)
3. Publish the configuration to the Steam backend
4. Your game must be installed in your Steam library (even if not released)

**The `steam-appid-validation` rule** will warn if App ID 480 appears in production-looking files. This is intentional — switch to your real App ID before release.

### 3. Test Account Setup

For multiplayer testing, you need multiple Steam accounts:

**Requirements per test account:**
- Separate Steam account (free to create)
- Must own the game (use dev comp keys from Steamworks Partner)
- Can run on the same machine with separate Steam instances, or on different machines

**Generating developer comp keys:**
1. Steamworks Partner > Your App > Request Keys
2. Generate keys (dev comp, not retail)
3. Activate on each test account

**Running multiple Steam instances (same machine):**
- Use Steam's `-login` command-line argument
- Or use separate user profiles at the OS level
- Third-party tools like Sandboxie can isolate instances

### 4. Steam Client Developer Console

Access the developer console for debugging:

**Open the console:**
- Launch Steam with `-console` flag: `steam.exe -console`
- Or navigate to `steam://open/console` in your browser
- The Console tab appears in the Steam client

**Useful console commands:**

| Command | Purpose |
|---------|---------|
| `app_info_print <appid>` | Dump app configuration data |
| `app_status <appid>` | Check install state and update status |
| `log_ipc *` | Log all IPC calls (very verbose) |
| `@AllowSkipGameUpdate 1` | Skip pending game updates |
| `testappcloudpaths <appid>` | Show Auto-Cloud file paths |
| `set_spew_level 4 4` | Maximum debug spew |

### 5. Steamworks Partner Test Environments

**Store page preview:**
- Use "Preview" mode in Steamworks Partner to test store page changes
- Changes are not visible to the public until "Publish"

**Beta branches:**
- Create beta branches for testing builds: Steamworks > Your App > SteamPipe > Builds
- Set a branch password for restricted access
- Use `set_beta <branch>` in the game's properties to switch branches

**Achievement testing:**
- Reset achievements via `SteamUserStats()->ResetAllStats(true)` in code
- Or use the Steamworks Partner site > Your App > Stats & Achievements > Reset Test Data
- The `steam_setAchievement` MCP tool can set achievements via the partner API (requires publisher key)

**Leaderboard testing:**
- Create test leaderboards in Steamworks Partner
- Delete test entries via the partner site or partner API
- The `steam_uploadLeaderboardScore` MCP tool can upload scores via the partner API

### 6. Development vs Production Checklist

Before moving from testing to production:

| Item | Dev/Test | Production |
|------|----------|------------|
| `steam_appid.txt` | Present in working directory | Remove from shipping build (or keep for debug) |
| App ID | 480 or your real ID | Your real App ID only |
| `SteamAPI_RestartAppIfNecessary` | Skipped via `steam_appid.txt` | Enabled — launches via Steam |
| Achievement names | Test names / SpaceWar defaults | Your configured names |
| API key | Dev key (okay to test with) | Publisher key (IP allowlisted) |
| Build branch | Beta / testing branch | Default branch |
| Cloud saves | Test files in dev path | Production paths configured in Auto-Cloud |

## Key References

| Resource | URL |
|----------|-----|
| SpaceWar SDK Example | https://partner.steamgames.com/doc/sdk/api/example |
| Steamworks SDK Getting Started | https://partner.steamgames.com/doc/sdk |
| Steam Console Commands | https://developer.valvesoftware.com/wiki/Command_line_options |
| SteamPipe Beta Branches | https://partner.steamgames.com/doc/store/application/builds |

## Example Interaction

**User:** "I want to test Steam achievements in my game but I don't have an App ID yet. How do I get started?"

**Agent:**
1. Explains App ID 480 (SpaceWar) as the sandbox
2. Shows `steam_appid.txt` setup with `480`
3. Provides the `SteamAPI_Init` boilerplate
4. Lists SpaceWar's available test achievements
5. Shows how to set and reset achievements in code
6. Notes: "Once you have your own App ID from Steamworks Partner, swap 480 for your real ID and configure your custom achievements there."

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Verify app | `steam_getAppDetails({ appid: 480 })` | None | Confirm SpaceWar is accessible |
| Set achievement | `steam_setAchievement({ steamid, appid, achievement })` | Publisher key | Unlock a test achievement via partner API |
| Clear achievement | `steam_clearAchievement({ steamid, appid, achievement })` | Publisher key | Re-lock a test achievement via partner API |
| Upload score | `steam_uploadLeaderboardScore({ appid, leaderboardid, steamid, score })` | Publisher key | Upload a test leaderboard score |
| Check stats | `steam_getAchievementStats({ appid })` | None | View global achievement unlock percentages |

## Common Pitfalls

1. **Shipping with App ID 480 in production** — `steam_appid.txt` containing `480` bypasses ownership checks. The `steam-appid-validation` rule catches this, but always double-check release builds.
2. **Assuming SpaceWar achievements match your game's** — App ID 480 has its own pre-configured achievements. You can test the SDK flow, but the achievement names won't match your real ones.
3. **Testing multiplayer with only one Steam account** — you need separate Steam accounts (each owning the game) for multiplayer testing. One account can't join its own lobby.
4. **Forgetting to reset test data before launch** — test achievements, leaderboard scores, and inventory items persist. Reset via Steamworks Partner or the partner API before going live.

## See Also

- [Steam App ID Validation](../../rules/steam-appid-validation.mdc) - warns about App ID 480 in production
- [Steam Release Checklist](../steam-release-checklist/SKILL.md) - pre-launch validation
- [Steam Achievement Designer](../steam-achievement-designer/SKILL.md) - designing achievements
- [Steam Leaderboards](../steam-leaderboards/SKILL.md) - leaderboard setup
