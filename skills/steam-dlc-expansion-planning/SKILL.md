---
name: steam-dlc-expansion-planning
description: Plan and configure DLC, expansions, and post-launch content for Steam games. Covers DLC App ID creation, depot setup, season passes, content cadence, pricing tiers, and in-game ownership checks. Use when planning downloadable content or post-launch monetization.
standards-version: 1.9.0
---

# Steam DLC & Expansion Planning

## Trigger

Use this skill when the user:

- Wants to plan DLC or expansion content for their Steam game
- Needs to create and configure a DLC App ID
- Asks about season passes or content bundles
- Wants to plan post-launch content cadence
- Needs DLC pricing guidance
- Asks about in-game DLC ownership checks

## Required Inputs

- **Base game App ID** - the parent game
- **DLC concept** - what kind of DLC (cosmetic, expansion, soundtrack, etc.)

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use it to verify the base game. See [MCP Usage](#mcp-usage).

### 1. DLC Types

| Type | Description | Typical Price | Example |
|------|-------------|---------------|---------|
| **Cosmetic Pack** | Skins, outfits, visual themes | $1.99-$4.99 | Character skin pack |
| **Content Pack** | New levels, maps, items | $4.99-$9.99 | New dungeon pack |
| **Story Expansion** | New storyline, characters, areas | $9.99-$19.99 | Story chapter DLC |
| **Major Expansion** | Standalone-quality new content | $14.99-$29.99 | Full expansion pack |
| **Soundtrack** | Game OST (plays in Steam Music) | $4.99-$9.99 | Official soundtrack |
| **Art Book** | Digital art book (PDF/images) | $2.99-$4.99 | Digital artbook |
| **Season Pass** | Bundle of future DLCs | 10-20% off sum | Season 1 pass |

### 2. DLC App ID Setup

**In Steamworks Partner:**

1. Navigate to your base game > **All Associated Packages, DLC, Demos, and Tools**
2. Click **Add New DLC**
3. Steamworks creates a new App ID linked to your base game
4. Configure the DLC store page (separate from base game):
   - Name, description, capsule images
   - Pricing (independent from base game)
   - System requirements (can inherit from base game)

**Depot configuration for DLC:**

```vdf
"appbuild"
{
  "appid" "{dlc_appid}"
  "desc" "DLC content build"
  "buildoutput" "..\output\"
  "contentroot" "..\dlc_content\"
  "depots"
  {
    "{dlc_depotid}" "depot_build_{dlc_depotid}.vdf"
  }
}
```

DLC depot IDs follow the same `appid + N` convention. If base game is `1234567` with depots `1234568-1234570`, DLC app `1234580` might use depot `1234581`.

### 3. In-Game DLC Ownership Checks

**C++:**
```cpp
if (SteamApps()->BIsDlcInstalled(DLC_APP_ID)) {
    // DLC content is owned and installed
    EnableDLCContent();
}
```

**C#:**
```csharp
if (SteamApps.BIsDlcInstalled(new AppId_t(DLC_APP_ID))) {
    EnableDLCContent();
}
```

**GDScript (GodotSteam):**
```gdscript
if Steam.isDlcInstalled(DLC_APP_ID):
    enable_dlc_content()
```

**Best practices:**
- Check ownership at game start and cache the result
- Listen for `DlcInstalled_t` callback for mid-session DLC purchases
- Gracefully handle missing DLC (don't crash, hide/disable content)
- Don't gate critical gameplay behind DLC — keep the base game complete

### 4. Season Pass Structure

A season pass bundles multiple future DLCs at a discount.

**Implementation:**
1. Create all planned DLC App IDs (even if content isn't ready)
2. Create a **Package** containing all DLC App IDs
3. Price the package at 10-20% less than the sum of individual DLCs
4. Players who buy the season pass automatically receive each DLC as it releases

**Season pass tiers (example):**

| Pass | Contents | Price | Savings |
|------|----------|-------|---------|
| Season 1 Pass | DLC 1 + DLC 2 + DLC 3 | $19.99 | 20% off |
| Deluxe Pass | Season 1 + Soundtrack + Art Book | $24.99 | 25% off |

### 5. Content Cadence

**Post-launch content schedule (example for a 12-month plan):**

| Month | Content | Type |
|-------|---------|------|
| 1 | Patch 1.1 — bug fixes, QoL | Free update |
| 2 | Cosmetic Pack 1 | Paid DLC ($2.99) |
| 3 | Content Pack 1 — new area | Paid DLC ($4.99) |
| 5 | Patch 1.2 — major balance update | Free update |
| 6 | Story Expansion 1 | Paid DLC ($9.99) |
| 8 | Cosmetic Pack 2 | Paid DLC ($2.99) |
| 10 | Content Pack 2 — new area | Paid DLC ($4.99) |
| 12 | Major Expansion | Paid DLC ($14.99) |

**Cadence guidelines:**
- Alternate free updates and paid DLC — free updates maintain goodwill
- Space DLC releases 2-3 months apart minimum
- Announce DLC roadmap early to encourage season pass purchases
- Larger gaps for bigger content drops (story expansions, major expansions)
- Time DLC releases around Steam sales for visibility

### 6. DLC Store Page Tips

- DLC store page should clearly state what's included
- "Requires the base game" is added automatically by Steam
- DLC capsule images should be visually distinct from base game but share branding
- Show DLC content in screenshots on the DLC page
- Consider a trailer for major expansions

### 7. DLC vs Free Update Decision Framework

| Factor | Free Update | Paid DLC |
|--------|-------------|----------|
| Scope | Bug fixes, QoL, balance, small features | New content, substantial additions |
| Player expectation | Expected post-launch | Accepted when substantial |
| Revenue impact | Drives sales of base game | Direct revenue |
| Community goodwill | Very positive | Positive if value is clear |
| Development cost | Low-moderate | Moderate-high |

**Rule of thumb:** If it took significant development time and adds content players wouldn't expect in the base game, it can be paid DLC. If it fixes or improves what players already paid for, it should be free.

## Key References

| Resource | URL |
|----------|-----|
| DLC Documentation | https://partner.steamgames.com/doc/store/application/dlc |
| Packages & Bundles | https://partner.steamgames.com/doc/store/application/packages |
| ISteamApps::BIsDlcInstalled | https://partner.steamgames.com/doc/api/ISteamApps#BIsDlcInstalled |
| DLC Best Practices | https://partner.steamgames.com/doc/store/application/dlc#best_practices |

## Example Interaction

**User:** "I want to plan 3 DLC packs and a season pass for my roguelike. Base game App ID is 2345678."

**Agent:**
1. Verifies base game via MCP
2. Proposes DLC structure:
   - DLC 1: New character pack ($4.99) — month 2
   - DLC 2: New biome expansion ($7.99) — month 5
   - DLC 3: Boss rush mode + new items ($9.99) — month 8
   - Season Pass: All 3 DLCs ($17.99, 20% off $22.97)
3. Provides DLC App ID creation steps
4. Generates VDF depot configs for each DLC
5. Provides C++ ownership check code
6. Advises: "Announce the DLC roadmap at launch. Include a 'Season Pass' option on the store page from day one."

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Verify base game | `steam_getAppDetails({ appid })` | None | Confirm game exists and check current DLC listings |
| Competitor DLC research | `steam_searchApps({ query })` | None | Find competitor games to benchmark DLC pricing |

DLC creation and management require the Steamworks Partner site — not available via MCP.

## Common Pitfalls

1. **Creating DLC before the base game is stable** — DLC that depends on base game systems that are still changing creates maintenance nightmares. Stabilize the base first.
2. **Not setting up depot inheritance correctly** — DLC depots must reference the base app's depots properly. Misconfigured inheritance means DLC content is invisible to users who own it.
3. **Pricing DLC too high relative to the base game** — a $20 DLC for a $15 base game feels exploitative. Industry norm is 25-50% of base price for substantial content packs.
4. **Forgetting to check DLC ownership in code** — `SteamApps()->BIsDlcInstalled(dlcAppId)` must gate DLC content. Without this check, DLC content may be accessible to everyone or to nobody.
5. **Not creating a store page for each DLC** — every DLC needs its own store page with screenshots and description. Bundle pages alone are not sufficient for discoverability.

## See Also

- [Steamworks App Config](../steamworks-app-config/SKILL.md) - depot and build configuration for DLC
- [Steam Pricing Strategy](../steam-pricing-strategy/SKILL.md) - pricing guidance and discount planning
- [Steam Inventory & Economy](../steam-inventory-economy/SKILL.md) - in-game item systems for DLC content
- [Steam Community Management](../steam-community-management/SKILL.md) - announcing DLC to your community
