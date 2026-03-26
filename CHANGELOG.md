# Changelog

All notable changes to Steam Developer Tools will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Plugin manifest, README, CONTRIBUTING guide, and MIT license

[0.1.0]: https://github.com/TMHSDigital/Steam-Cursor-Plugin/releases/tag/v0.1.0
