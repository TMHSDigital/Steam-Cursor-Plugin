---
name: steam-anticheat-integration
description: Integrate anti-cheat solutions with Steam games. Covers EasyAntiCheat (EAC), BattlEye, and VAC setup, Proton/Linux compatibility, Steam Deck considerations, and custom anti-cheat patterns. Use when adding anti-cheat protection to a multiplayer Steam game.
standards-version: 1.7.0
---

# Steam Anti-Cheat Integration

## Trigger

Use this skill when the user:

- Wants to add anti-cheat to their Steam game
- Asks about EasyAntiCheat, BattlEye, or VAC
- Needs anti-cheat that works with Proton/Linux/Steam Deck
- Asks about the trade-offs between different anti-cheat solutions
- Needs to configure anti-cheat in Steamworks
- Is troubleshooting anti-cheat compatibility issues

## Required Inputs

- **Game type** - multiplayer mode (competitive, co-op, MMO, etc.)
- **Target platforms** - Windows, Linux, macOS, Steam Deck
- **Engine** (optional) - Unity, Unreal, Godot, custom

## Workflow

### 1. Anti-Cheat Options Overview

| Solution | Type | Proton/Linux | Steam Deck | Cost | Best for |
|----------|------|-------------|------------|------|----------|
| **EasyAntiCheat (EAC)** | Kernel + user mode | Supported (opt-in) | Supported (opt-in) | Free (via Epic) | Competitive MP, battle royale |
| **BattlEye** | Kernel + user mode | Supported (opt-in) | Supported (opt-in) | Paid license | Large-scale MP, MMOs |
| **VAC** | Server-side + client | Native support | Native support | Free (Valve) | Source/GoldSrc games, Steamworks titles |
| **Custom** | Varies | Developer-dependent | Developer-dependent | Development cost | Specific needs, lightweight protection |
| **None** | N/A | N/A | N/A | Free | Single-player, co-op, trust-based |

### 2. EasyAntiCheat (EAC)

**Setup:**

1. Register at the [EAC Developer Portal](https://dev.easy.ac/)
2. Download the EAC SDK
3. Integrate the SDK into your game client:

```cpp
#include "eac_sdk.h"

// Initialize EAC
EOS_AntiCheatClient_BeginSession(AntiCheatClientHandle, &Options);

// On game tick
EOS_AntiCheatClient_Poll(AntiCheatClientHandle);

// On disconnect
EOS_AntiCheatClient_EndSession(AntiCheatClientHandle);
```

4. Configure in Steamworks Partner > Technical Tools > Anti-Cheat

**Proton/Linux support:**
- EAC supports Proton since June 2022
- Must be explicitly enabled in the EAC Developer Portal
- Go to EAC settings > Enable **Linux via Wine/Proton**
- Does NOT require a native Linux build — works through Proton translation
- Kernel-level features are limited under Proton; user-mode anti-cheat works

**Steam Deck:**
- Same as Proton support — enable Wine/Proton in EAC settings
- Test on actual Steam Deck hardware or Deck-like environment
- EAC + Proton is the standard path for Deck compatibility

### 3. BattlEye

**Setup:**

1. Contact BattlEye for a license agreement
2. Integrate the BattlEye SDK:

```cpp
#include "BattlEye.h"

// Initialize
BEClient_Init(version, &callbacks);

// Game loop
BEClient_Run();

// Shutdown
BEClient_Shutdown();
```

3. Ship BattlEye binaries with your game
4. Configure in Steamworks Partner

**Proton/Linux support:**
- BattlEye supports Proton since late 2021
- Must be enabled per-game by the developer
- Contact BattlEye support to enable Proton compatibility
- Once enabled, works automatically for Linux/Deck players

### 4. VAC (Valve Anti-Cheat)

VAC is Valve's built-in anti-cheat system. It's primarily used with Source engine games but can be enabled for any Steamworks title.

**Setup:**

1. Enable VAC in Steamworks Partner > Technical Tools > Anti-Cheat Configuration
2. Configure secure servers:

```cpp
// Mark server as VAC-secured
SteamGameServer()->SetSecure(true);

// Check if client is VAC-banned
bool banned = SteamGameServer()->BSecure();
```

3. VAC operates server-side — bans are applied by Valve after detection

**Characteristics:**
- No client-side SDK integration required (server-side detection)
- Bans are delayed (days to weeks) to mask detection methods
- VAC bans are permanent and tied to Steam account
- Works natively on all platforms including Linux and Steam Deck
- Less invasive than kernel-level solutions (no ring-0 driver)

### 5. Steam Deck Compatibility Matrix

| Anti-Cheat | Deck Status | Action Required |
|------------|-------------|-----------------|
| EAC | Works | Enable Wine/Proton in EAC portal |
| BattlEye | Works | Contact BattlEye to enable Proton |
| VAC | Works | No action needed (server-side) |
| Custom kernel-level | Blocked | Will NOT work under Proton |
| Custom user-mode | May work | Test under Proton; avoid kernel calls |

**Critical:** Kernel-level anti-cheat that has NOT been updated for Proton will prevent your game from running on Steam Deck. This is the #1 cause of Deck verification failure for multiplayer games.

### 6. Implementation Best Practices

**Do:**
- Enable Proton/Linux support from day one
- Test anti-cheat on Steam Deck before launch
- Provide clear error messages when anti-cheat blocks a launch
- Allow single-player/offline modes without anti-cheat
- Document anti-cheat on your store page (players expect transparency)

**Don't:**
- Don't use kernel-level anti-cheat for non-competitive games
- Don't block Linux/Deck players if your anti-cheat supports Proton
- Don't combine multiple anti-cheat solutions (conflicts, performance)
- Don't rely solely on client-side anti-cheat (always validate server-side)

### 7. Server-Side Validation

Regardless of anti-cheat solution, always validate on the server:

```cpp
// Validate Steam auth ticket
EBeginAuthSessionResult result = SteamGameServer()->BeginAuthSession(
    authTicket, ticketSize, steamID);

if (result != k_EBeginAuthSessionResultOK) {
    // Reject connection
}

// Validate gameplay data server-side
if (playerSpeed > MAX_ALLOWED_SPEED) {
    // Flag or kick player
}

// Never trust client-reported values for:
// - Position/velocity
// - Health/damage
// - Score/currency
// - Inventory changes
```

## Key References

| Resource | URL |
|----------|-----|
| EasyAntiCheat | https://dev.easy.ac/ |
| BattlEye | https://www.battleye.com/ |
| VAC | https://partner.steamgames.com/doc/features/anticheat |
| Proton Anti-Cheat | https://partner.steamgames.com/doc/steamdeck/proton |
| Deck Anti-Cheat Compat | https://areweanticheatyet.com/ |

## Example Interaction

**User:** "I'm making a competitive FPS. I need anti-cheat that works on Steam Deck. What should I use?"

**Agent:**
1. Recommends EAC as the primary choice (free, well-supported, Proton-compatible)
2. Explains setup steps: register at EAC portal, integrate SDK, enable Proton
3. Stresses: "Enable Wine/Proton support in the EAC Developer Portal immediately — this is opt-in, not automatic."
4. Adds: "Combine with server-side validation. EAC catches client-side cheats; your server should validate all gameplay-critical data independently."
5. Warns: "Test on Steam Deck hardware before launch. Anti-cheat issues are the most common Deck verification failure for multiplayer games."

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Verify app | `steam_getAppDetails({ appid })` | None | Confirm game exists and check platform list |

Anti-cheat configuration requires the Steamworks Partner site and anti-cheat vendor portals — not available via MCP.

## Common Pitfalls

1. **Not enabling Proton/Wine support for EAC or BattlEye** — Linux and Steam Deck players are blocked unless you explicitly opt in via the anti-cheat vendor portal. This is a separate checkbox from Steamworks Deck compatibility.
2. **Shipping EAC without the correct redistributable files** — the EAC service installer and `EasyAntiCheat` folder must be bundled with your build. Missing files cause immediate crashes.
3. **Trusting VAC alone for competitive games** — VAC is reactive (ban waves), not preventive. For real-time protection, pair it with EAC or BattlEye.
4. **Forgetting to test anti-cheat in dev builds** — anti-cheat services often behave differently in debug vs release. Always test with the release configuration before shipping.
5. **Breaking modding support unintentionally** — EAC and BattlEye block DLL injection, which some mods rely on. If your game supports mods, configure allowlists or provide a "modded" launch option without anti-cheat.

## See Also

- [Steam Multiplayer Networking](../steam-multiplayer-networking/SKILL.md) - networking setup that anti-cheat protects
- [Steam Deck Compatibility](../../rules/steam-deck-compat.mdc) - Deck compat rule (flags anti-cheat issues)
- [Steam Release Checklist](../steam-release-checklist/SKILL.md) - pre-launch anti-cheat verification
