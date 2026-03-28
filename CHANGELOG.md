# Changelog

All notable changes to Steam Developer Tools will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

- `steam.getReviews({ appid, filter, language, count })` - planned for MCP server v0.3.0 (review analysis skill uses curl fallback until available)
- `steam.getPriceOverview({ appids, cc })` - planned for MCP server v0.3.0 (price history skill uses getAppDetails with cc parameter until available)

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

[0.4.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.4.0
[0.3.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.3.0
[0.2.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.2.0
[0.1.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.1.0
