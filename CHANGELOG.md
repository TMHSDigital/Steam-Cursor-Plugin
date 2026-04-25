# Changelog

All notable changes to Steam Developer Tools will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.2] - 2026-04-25

See [release notes](https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v1.3.2) for details.

## [1.3.1] - 2026-04-25

See [release notes](https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v1.3.1) for details.

## [1.3.0] - 2026-04-25

See [release notes](https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v1.3.0) for details.

## [Versions 1.0.1 through 1.2.x] - prior to 2026-04-25

Multiple releases shipped between v1.0.0 and v1.3.0 without CHANGELOG
entries due to release-doc-sync automation not yet existing. See
[GitHub releases](https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases)
for the complete release history.

Going forward, release-doc-sync@v1.0 from
[TMHSDigital/Developer-Tools-Directory](https://github.com/TMHSDigital/Developer-Tools-Directory)
automatically maintains this file on each auto-release.

## [1.0.0] - 2026-03-29

### Added

- **5 new MCP tools** in companion Steam MCP server (v0.6.0), reaching 25 total tools:
  - `steam_getNewsForApp` — Fetch recent news and announcements for a game (no auth)
  - `steam_getSchemaForGame` — Achievement/stat schema with display names, descriptions, and icons (API key)
  - `steam_getPlayerAchievements` — Per-player achievement unlock status and timestamps (API key)
  - `steam_getLeaderboardsForGame` — List all leaderboards with numeric IDs (API key)
  - `steam_clearAchievement` — Re-lock/clear an achievement for QA testing (publisher key)
- Skills updated with new tool references: steam-api-reference, steam-achievement-designer, steam-player-stats, steam-leaderboards, steam-community-management, steam-testing-sandbox
- `steam-api-key-usage` rule updated with `GetNewsForApp`, `GetSchemaForGame`, `GetPlayerAchievements` equivalents

### Changed

- **Expanded target audience** to include modders alongside game developers and power users
- Widened skill triggers for steam-workshop-helper, steam-store-lookup, steam-api-reference, and steam-community-management to activate on modder use cases
- Added modder example interaction to steam-workshop-helper (Workshop upload flow)
- Added "For Modders" callout section in README with relevant tools
- Added "Who Is This For?" section to GitHub Pages site with game dev / modder / power user columns
- Added modder-related prompt cards to the site
- Updated OG card, meta descriptions, and plugin description to include modders
- Added `modding`, `steam-workshop`, `ugc` keywords to plugin.json
- Plugin version bumped to 1.0.0

### Fixed

- **MCP tool naming** — Renamed all 20 MCP tool references from dot notation (`steam.getAppDetails`) to underscore notation (`steam_getAppDetails`) across 34 files. Dots conflicted with Cursor's internal MCP bridge routing. Companion steam-mcp server v0.5.0 has the matching rename.
- **`steam_searchApps` parameter** — Renamed `term` to `query` across all skills, rules, and docs to match steam-mcp server v0.5.1 schema change
- **`steam_getLeaderboardsForGame` auth tier** — Corrected from publisher key to standard API key across all docs (companion steam-mcp server v0.6.1)
- **`steam_getPlayerAchievements` error message** — Corrected from publisher key boilerplate to free API key + public profile message (companion steam-mcp server v0.6.1)
- **Companion steam-mcp server v0.5.1** — `steam_getLeaderboardEntries` description clarified (numeric ID required), write tools (`steam_setAchievement`, `steam_uploadLeaderboardScore`, `steam_grantInventoryItem`) now return clear error messages when publisher key is missing
- **Companion steam-mcp server v0.6.0** — Fixed POST body encoding on publisher tools (params now sent as `application/x-www-form-urlencoded` body instead of URL query string), removed dead variable in `grantInventoryItem`

## [0.9.0] - 2026-03-28

### Added

- **4 new MCP read tools** in companion Steam MCP server (v0.4.0), reaching the target of 20 total tools:
  - `steam_getReviews` — Fetch user reviews with filters for language, sentiment, purchase type, and pagination (no auth)
  - `steam_getPriceOverview` — Batch price check for multiple apps in a specific region (no auth)
  - `steam_getAppReviewSummary` — Review score, total counts, and positive percentage without individual reviews (no auth)
  - `steam_getRegionalPricing` — Pricing breakdown across multiple countries/regions (no auth)

### Changed

- Plugin version bumped to 0.9.0
- Companion Steam MCP server bumped to 0.4.0 (20 tools: 14 read-only + 6 write/guidance)
- All documentation updated: README, CLAUDE.md, CONTRIBUTING.md, ROADMAP.md

## [0.8.0] - 2026-03-28

### Added

- **steam-migration-guide** skill: migrating games to Steam from Epic, GOG, itch.io — engine-specific SDK integration (Unity, Unreal, Godot), feature parity mapping, store page strategy, and technical migration checklist
- **Common Pitfalls sections** added to all 30 skills — each skill now includes 3-6 concise, actionable pitfalls specific to its domain

### Changed

- Plugin version bumped to 0.8.0
- Plugin description updated to reflect 30 skills
- All documentation updated: README, CLAUDE.md, CONTRIBUTING.md, ROADMAP.md

## [0.7.0] - 2026-03-28

### Added

- **steam-testing-sandbox** skill: development sandbox guide — App ID 480 (SpaceWar) usage, test account setup, Steam client console commands, partner test environments, and dev-to-production checklist
- **6 new MCP write tools** in companion Steam MCP server (v0.3.0):
  - `steam_createLobby` — SDK guidance for ISteamMatchmaking lobby creation (C++/C#/GDScript)
  - `steam_uploadWorkshopItem` — SDK guidance for ISteamUGC Workshop uploads (C++/GDScript)
  - `steam_updateWorkshopItem` — HTTP POST to update Workshop item metadata via partner API
  - `steam_setAchievement` — HTTP POST to set/unlock achievements via partner API (dev/test)
  - `steam_uploadLeaderboardScore` — HTTP POST to upload scores via partner API
  - `steam_grantInventoryItem` — HTTP POST to grant inventory items via partner API

### Changed

- `steam-appid-validation` rule enhanced with MCP live validation — suggests `steam_getAppDetails()` to verify App IDs exist
- Plugin version bumped to 0.7.0
- Plugin description updated to reflect 29 skills and 16 MCP tools
- All documentation updated: README, CLAUDE.md, CONTRIBUTING.md, ROADMAP.md

## [0.6.0] - 2026-03-28

### Added

- **steam-playtest-setup** skill: Steam Playtest feature configuration — open vs closed playtests, key distribution, signup pages, feedback collection, Next Fest integration, and transition to Early Access or launch
- **steam-bug-report-template** skill: structured bug report templates — Steam system info integration, crash dump collection (Windows/Unity/Unreal), known issues tracking, and Discussion forum integration
- **steam-anticheat-integration** skill: anti-cheat setup — EasyAntiCheat (EAC), BattlEye, and VAC integration with Proton/Linux compatibility matrix, Steam Deck considerations, and server-side validation patterns
- **steam-save-compat** rule: flags save file practices that break cross-platform Steam Cloud sync — binary endianness, OS-specific paths, hardcoded separators, non-portable serialization
- **steam-network-security** rule: flags insecure networking patterns — unvalidated auth tickets, missing session management, trusting client data, missing encryption
- **steam-api-error-handling** rule: flags missing error/callback handling for Steamworks SDK — unchecked `SteamAPI_Init()`, missing `StoreStats()`, ignored callbacks, missing `SteamAPI_RunCallbacks()`

### Changed

- Plugin version bumped to 0.6.0
- Plugin description updated to reflect 28 skills and 9 rules
- All documentation updated: README, CLAUDE.md, CONTRIBUTING.md, ROADMAP.md

## [0.5.0] - 2026-03-28

### Added

- **steam-community-management** skill: post-launch community tools — announcements, events, discussion forum setup, update post templates, Community Hub configuration, and communication cadence guidance
- **steam-store-page-optimizer** skill: store page best practices — capsule image specs (all 9 sizes), description structure, tag strategy, trailer guidance, demo setup, screenshot optimization, and full audit checklist
- **steam-pricing-strategy** skill: data-driven pricing — base price tiers, regional pricing with Valve multipliers, launch discounts, sale participation, bundles, free-to-play considerations, and price change cooldown rules
- **steam-dlc-expansion-planning** skill: DLC and post-launch content — App ID creation, depot config, season passes, content cadence templates, pricing tiers, and in-game ownership checks (C++/C#/GDScript)

### Changed

- Plugin version bumped to 0.5.0
- Plugin description updated to reflect 25 skills
- All documentation updated: README, CLAUDE.md, CONTRIBUTING.md, ROADMAP.md

### MCP Roadmap

- `steam_getAppReviewSummary({ appid })` - review histogram and summary (planned for MCP server)
- `steam_getRegionalPricing({ appid, countries })` - pricing by region (planned for MCP server)

## [0.4.0] - 2026-03-28

### Added

- **steam-build-automation** skill: SteamPipe CI/CD integration with GitHub Actions, GitLab CI, and Jenkins pipelines for automated depot uploads, beta branch management, Docker containerized builds, and secrets management
- **steam-release-checklist** skill: comprehensive pre-release validation checklist covering store page completeness, depot config, achievements, cloud saves, Steam Deck compatibility, pricing, multiplayer, leaderboards, social features, and launch readiness
- **steam-steamcmd-helper** skill: steamcmd scripting reference with common commands, batch/shell scripts, Docker containerized builds, Steam Guard handling, and troubleshooting guide
- **steam-build-config-validation** rule: validates VDF build configs for missing depots, mismatched App IDs, invalid file mappings, empty content roots, and `setlive` safety
- **steam-launch-options-check** rule: flags launch option issues including missing executables, wrong OS targeting, missing descriptions for multi-launch configs, and invalid type values

### Changed

- Plugin version bumped to 0.4.0
- Plugin description updated to reflect 21 skills and 6 rules
- All documentation updated: README, CLAUDE.md, CONTRIBUTING.md, ROADMAP.md

## [0.3.0] - 2026-03-27

### Added

- **steam-review-analysis** skill: fetch and analyze Steam game reviews - sentiment breakdown, common complaints, comparison across updates, language distribution, review bombing detection
- **steam-price-history** skill: pricing trends, sale history, regional pricing analysis, price-to-review value scoring, pricing strategy guidance for developers
- **steam-market-research** skill: genre trend analysis, tag popularity, competitor identification, market gap analysis, viability assessment using Steam store data
- **steam-wishlist-estimates** skill: estimate wishlists from follower counts and review data using the Boxleiter method, wishlist-to-sales conversion benchmarks, revenue estimation

### Changed

- Plugin version bumped to 0.3.0
- Plugin description updated to reflect 18 skills
- All documentation updated: README, CLAUDE.md, CONTRIBUTING.md, ROADMAP.md

### MCP Roadmap

- `steam_getReviews({ appid, filter, language, count })` - planned for MCP server v0.3.0 (review analysis skill uses curl fallback until available)
- `steam_getPriceOverview({ appids, cc })` - planned for MCP server v0.3.0 (price history skill uses getAppDetails with cc parameter until available)

## [0.2.0] - 2026-03-27

### Added

- **steam-api-key-usage** rule: when the Steam MCP server is available, flags raw `curl`/`fetch` calls to Steam API endpoints and suggests the equivalent MCP tool
- Companion [Steam MCP Server](https://github.com/TMHSDigital/steam-mcp) referenced across all skills (server lives in separate repo)

### Changed

- All 14 skills updated: replaced `## MCP Integration (Future)` placeholder sections with concrete `## MCP Usage` sections referencing the companion Steam MCP server's actual tool signatures
- 6 skills with direct MCP replacements now include "Preferred" callouts in their Workflow sections directing users to MCP tools over `curl` commands: steam-store-lookup, steam-player-stats, steam-profile-lookup, steam-game-comparison, steam-workshop-helper, steam-leaderboards
- **steam-api-reference** skill now includes a full catalog of all 10 available MCP tools with parameter signatures and auth requirements
- Plugin description updated to reflect MCP support and 4 rules
- Version bumped to 0.2.0

## [0.1.0] - 2026-03-26

### Added

- **steam-store-lookup** skill: look up any Steam game by name or App ID, returns store page data (price, reviews, tags, system requirements)
- **steamworks-app-config** skill: generate and document depot configs, build VDF files, launch options, and DLC setup
- **steam-api-reference** skill: search Steam Web API and Steamworks SDK documentation with endpoint signatures and code examples
- **steam-player-stats** skill: query current player counts, achievement stats, leaderboards, and user game libraries
- **steam-workshop-helper** skill: look up Workshop items and document UGC integration patterns for game developers
- **steam-achievement-designer** skill: design achievements, generate VDF/JSON config snippets, and get unlock code for C++, C#, and GDScript
- **steam-multiplayer-networking** skill: lobby creation, matchmaking, Steam Networking Sockets relay, dedicated game servers with C++/C#/GDScript examples
- **steam-cloud-saves** skill: ISteamRemoteStorage manual cloud and Auto-Cloud configuration, conflict resolution, quota management
- **steam-leaderboards** skill: create/find leaderboards, upload scores, download entries (global, friends, around-user), Web API queries
- **steam-friends-social** skill: friends list, rich presence strings, game invites, Steam Overlay control, avatar retrieval
- **steam-input-controller** skill: ISteamInput action sets, digital/analog bindings, controller glyph retrieval for Xbox/PlayStation/Switch/Steam Deck
- **steam-inventory-economy** skill: ISteamInventory item schema, drops, crafting, ISteamMicroTxn purchase flow, Steam Item Store, Web API queries
- **steam-profile-lookup** skill: resolve vanity URLs, fetch player summaries, owned games, recent activity, Steam level, badges, friend lists
- **steam-game-comparison** skill: side-by-side comparison of price, reviews, player counts, genres, and platforms for multiple Steam games
- **steam-appid-validation** rule: validates App ID consistency across project files and warns if steam_appid.txt is missing
- **steamworks-secrets** rule: prevents committing API keys, partner credentials, and auth tokens
- **steam-deck-compat** rule: flags common Steam Deck compatibility issues (hardcoded resolutions, mouse-only input, anti-cheat, Windows-only paths, missing controller support)
- Plugin manifest, README, CONTRIBUTING guide, and license

[1.0.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v1.0.0
[0.9.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.9.0
[0.8.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.8.0
[0.7.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.7.0
[0.6.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.6.0
[0.5.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.5.0
[0.4.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.4.0
[0.3.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.3.0
[0.2.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.2.0
[0.1.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.1.0
