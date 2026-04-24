---
name: steam-release-checklist
description: Pre-release validation checklist for Steam games. Covers store page completeness, depot configuration, achievements, cloud saves, Steam Deck compatibility, pricing, and launch readiness. Use when preparing to launch or update a game on Steam.
standards-version: 1.6.3
---

# Steam Release Checklist

## Trigger

Use this skill when the user:

- Is preparing to launch a game on Steam
- Asks what they need to do before releasing
- Wants a pre-release validation checklist
- Is about to push a build to the `default` branch
- Asks about store page requirements or launch readiness
- Needs to verify their Steamworks configuration is complete

## Required Inputs

- **App ID** - the game's Steam App ID
- **Release type** (optional) - initial launch, major update, Early Access, or DLC

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use it to verify store page data and current configuration. See [MCP Usage](#mcp-usage).

### Pre-Release Checklist

Walk through each section with the user. Mark items as done, flagged, or not applicable.

---

### 1. Store Page

- [ ] **App name** finalized and matches marketing materials
- [ ] **Short description** (< 300 characters) written and compelling
- [ ] **Detailed description** with formatting, features list, and call to action
- [ ] **Header capsule** (460×215) uploaded
- [ ] **Small capsule** (231×87) uploaded
- [ ] **Main capsule** (616×353) uploaded
- [ ] **Hero capsule** (3840×1240) uploaded
- [ ] **Logo** (1280×720, transparent background) uploaded
- [ ] **Screenshots** - minimum 5, recommended 10+, showing actual gameplay
- [ ] **Trailer** uploaded (MP4, recommended 1080p/4K)
- [ ] **Tags** configured (at least 5-10 relevant tags)
- [ ] **Genre** selected correctly
- [ ] **System requirements** (minimum and recommended) filled out for each OS
- [ ] **Supported languages** listed with audio/subtitles/interface breakdown
- [ ] **Legal lines** (copyright, EULA) if required
- [ ] **Content descriptors** and **maturity ratings** set appropriately
- [ ] **Coming Soon** page has been live for wishlist collection

### 2. Build & Depots

- [ ] **Depots configured** for all target platforms (Windows, macOS, Linux)
- [ ] **app_build.vdf** and **depot_build_*.vdf** files valid
- [ ] **Launch options** set for each platform with correct executables
- [ ] **Build uploaded** to a beta branch and tested
- [ ] **Install size** reasonable and listed accurately
- [ ] **Redistributables** included (Visual C++ runtime, .NET, DirectX, etc.)
- [ ] **steam_appid.txt** present in game root with correct App ID
- [ ] **Steamworks SDK initialized** correctly in game code

### 3. Achievements

- [ ] Achievements **defined** in Steamworks Partner site (name, description, icon, locked icon)
- [ ] Achievement **API names** match code (`ACH_` prefix convention)
- [ ] Achievements **tested** — unlock and clear work correctly
- [ ] **Hidden achievements** marked appropriately (story spoilers)
- [ ] Achievement **icons** uploaded (64×64 JPG/PNG, both locked and unlocked)

### 4. Cloud Saves

- [ ] **Auto-Cloud** or **ISteamRemoteStorage** configured
- [ ] Save files **tested** — create on one machine, verify on another
- [ ] **Conflict resolution** tested (modify save on two machines, sync)
- [ ] **Quota** sufficient for save file sizes
- [ ] Save path uses Steam-recommended location (not hardcoded OS paths)

### 5. Steam Deck Compatibility

- [ ] Game **tested on Steam Deck** or in Deck-like environment (1280×800, gamepad only)
- [ ] **Controller support** implemented (Steam Input or native gamepad)
- [ ] No **hardcoded resolutions** — supports 1280×800 at 16:10
- [ ] No **mouse-only interactions** without controller alternatives
- [ ] **UI text** readable at Deck's 7" screen size
- [ ] **Anti-cheat** compatible with Proton (if applicable)
- [ ] No **external launchers** that break under Proton
- [ ] **Deck compatibility review** submitted via Steamworks

### 6. Multiplayer (if applicable)

- [ ] **Lobbies** create and join correctly
- [ ] **Matchmaking** tested with multiple accounts
- [ ] **Dedicated servers** deployed and accessible
- [ ] **Steam Networking Sockets** relay tested (if using relay)
- [ ] **NAT traversal** verified — players behind restrictive NATs can connect

### 7. Leaderboards (if applicable)

- [ ] Leaderboards **created** in Steamworks
- [ ] Score **upload** and **download** tested
- [ ] **Display name** and **sort method** configured correctly
- [ ] **Friend** and **global** views working

### 8. Social Features

- [ ] **Rich Presence** strings configured and tested
- [ ] **Game invites** working (if multiplayer)
- [ ] **Steam Overlay** accessible in-game

### 9. Pricing & Business

- [ ] **Base price** set in Steamworks
- [ ] **Regional pricing** reviewed (use Valve's suggested regional prices as starting point)
- [ ] **Launch discount** configured (10-15% is standard, max 40%, min 7 days before first discount)
- [ ] **Bundles/packages** created (if applicable — game + soundtrack, deluxe edition)
- [ ] **DLC** listed and configured (if launching with DLC)

### 10. Marketing & Launch Prep

- [ ] **Release date** set (or "Coming Soon" configured)
- [ ] **Curator keys** generated and distributed
- [ ] **Community Hub** enabled
- [ ] **Announcements** drafted for launch day
- [ ] **Social media** posts prepared
- [ ] **Wishlist notification** will fire on release (automatic if wishlists exist)

### 11. Final Validation

- [ ] **Store page reviewed** by a second person
- [ ] **Build playtest** on a clean machine (fresh install, no dev tools)
- [ ] **Steamworks review** submitted (Valve review for new apps)
- [ ] **`setlive` to default`** — only after ALL above are confirmed

## Key References

| Resource | URL |
|----------|-----|
| Store Page Best Practices | https://partner.steamgames.com/doc/store/assets |
| Pre-Release Checklist (Valve) | https://partner.steamgames.com/doc/store/releasing |
| Steam Direct Process | https://partner.steamgames.com/doc/gettingstarted |
| Deck Compatibility Review | https://partner.steamgames.com/doc/steamdeck/compat |
| Pricing Overview | https://partner.steamgames.com/doc/store/pricing |

## Example Interaction

**User:** "I'm about to launch my game on Steam. App ID 2345678. What do I need to check?"

**Agent:**
1. Fetches store page data via MCP to check current state
2. Walks through each checklist section
3. Flags: "Your store page has 3 screenshots — Valve recommends at least 5. No trailer detected."
4. Flags: "No achievements found. If your game has achievements, upload them before launch."
5. Confirms: "Cloud saves configured via Auto-Cloud. Depot configs look valid for Windows and Linux."
6. Provides remaining action items as a prioritized list

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Check store page | `steam_getAppDetails({ appid })` | None | Verify description, screenshots, tags, price, platforms |
| Check achievements | `steam_getAchievementStats({ appid })` | None | Verify achievements are uploaded and visible |
| Check player stats | `steam_getPlayerCount({ appid })` | None | Confirm game is accessible (returns data = app is public) |

## Common Pitfalls

1. **Not submitting the store page for review early enough** — Valve's review process can take 2-5 business days. Submit at least 2 weeks before your planned launch date.
2. **Forgetting to set the release date to "coming soon" first** — jumping straight to a specific date without a "coming soon" period misses weeks of wishlist accumulation.
3. **Not testing the "Download" flow end-to-end** — install your game via Steam on a clean machine. Missing redistributables (VC++, .NET, DirectX) are the #1 cause of day-one crashes.
4. **Skipping the default branch build check** — ensure the build on your default (public) branch is the one you want to ship. Beta branch builds are not visible to the public.
5. **Launching without a community hub** — the community hub (discussions, guides, screenshots) should be enabled and seeded with a welcome post and a known issues thread.

## See Also

- [Steamworks App Config](../steamworks-app-config/SKILL.md) - depot and build configuration
- [Steam Build Automation](../steam-build-automation/SKILL.md) - CI/CD pipeline for automated uploads
- [Steam Achievement Designer](../steam-achievement-designer/SKILL.md) - design and configure achievements
- [Steam Cloud Saves](../steam-cloud-saves/SKILL.md) - cloud save setup and testing
- [Steam Input / Controllers](../steam-input-controller/SKILL.md) - controller support for Deck compatibility
- [Steam Price History](../steam-price-history/SKILL.md) - pricing strategy and benchmarks
