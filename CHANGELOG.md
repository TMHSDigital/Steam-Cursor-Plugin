# Changelog

All notable changes to Steam Developer Tools will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-26

### Added

- **steam-multiplayer-networking** skill: lobby creation, matchmaking, Steam Networking Sockets relay, dedicated game servers with C++/C#/GDScript examples
- **steam-cloud-saves** skill: ISteamRemoteStorage manual cloud and Auto-Cloud configuration, conflict resolution, quota management
- **steam-leaderboards** skill: create/find leaderboards, upload scores, download entries (global, friends, around-user), Web API queries
- **steam-friends-social** skill: friends list, rich presence strings, game invites, Steam Overlay control, avatar retrieval
- **steam-input-controller** skill: ISteamInput action sets, digital/analog bindings, controller glyph retrieval for Xbox/PlayStation/Switch/Steam Deck
- **steam-inventory-economy** skill: ISteamInventory item schema, drops, crafting, ISteamMicroTxn purchase flow, Steam Item Store, Web API queries
- **steam-profile-lookup** skill: resolve vanity URLs, fetch player summaries, owned games, recent activity, Steam level, badges, friend lists
- **steam-game-comparison** skill: side-by-side comparison of price, reviews, player counts, genres, and platforms for multiple Steam games
- **steam-deck-compat** rule: flags common Steam Deck compatibility issues (hardcoded resolutions, mouse-only input, anti-cheat, Windows-only paths, missing controller support)

## [0.1.0] - 2026-03-26

### Added

- **steam-store-lookup** skill: look up any Steam game by name or App ID, returns store page data (price, reviews, tags, system requirements)
- **steamworks-app-config** skill: generate and document depot configs, build VDF files, launch options, and DLC setup
- **steam-api-reference** skill: search Steam Web API and Steamworks SDK documentation with endpoint signatures and code examples
- **steam-player-stats** skill: query current player counts, achievement stats, leaderboards, and user game libraries
- **steam-workshop-helper** skill: look up Workshop items and document UGC integration patterns for game developers
- **steam-achievement-designer** skill: design achievements, generate VDF/JSON config snippets, and get unlock code for C++, C#, and GDScript
- **steam-appid-validation** rule: validates App ID consistency across project files and warns if steam_appid.txt is missing
- **steamworks-secrets** rule: prevents committing API keys, partner credentials, and auth tokens
- Plugin manifest, README, CONTRIBUTING guide, and license

[0.2.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.2.0
[0.1.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.1.0
