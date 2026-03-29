# Roadmap

Themed release plan toward v1.0.0.

**Current:** v1.0.0 - 30 skills, 9 rules, companion [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) with 25 tools (18 read-only + 7 write/guidance).

**Status:** v1.0.0 "Stable" released. 30 skills, 9 rules, 25 MCP tools.

| Version | Theme | New Skills | New Rules | MCP Tools | Total Skills | Total Rules |
|---------|-------|-----------|-----------|-----------|-------------|-------------|
| v0.1.0 | - | - | - | 0 | 14 | 3 |
| v0.2.0 | Live Data | 0 (updates) | 1 | 10 | 14 | 4 |
| v0.3.0 | Insights | 4 | 0 | 2 | 18 | 4 |
| v0.4.0 | Ship It | 3 | 2 | 0 | 21 | 6 |
| v0.5.0 | Grow | 4 | 0 | 2 | 25 | 6 |
| v0.6.0 | Quality | 3 | 3 | 0 | 28 | 9 |
| v0.7.0 | Full Power | 1 | 0 | 6 | 29 | 9 |
| v0.8.0 | Polish | 1 | 0 | 0 | 30 | 9 |
| v0.9.0 | Complete | 0 | 0 | 4 | 30 | 9 |
| v1.0.0 (current) | Stable | 0 | 0 | 5 | 30 | 9 |

---

## v0.2.0 - "Live Data" (MCP Server Foundation)

**Theme:** Replace static guidance with live, structured API calls.

### MCP Server

The MCP server lives in a separate repo: [steam-mcp](https://github.com/TMHSDigital/steam-mcp).

Read-only tools:

| Tool | Description |
|------|-------------|
| `steam_getAppDetails({ appid })` | Store data (price, reviews, tags, platforms) |
| `steam_searchApps({ query })` | App search by name |
| `steam_getPlayerCount({ appid })` | Current concurrent players |
| `steam_getAchievementStats({ appid })` | Global achievement unlock percentages |
| `steam_getPlayerSummary({ steamid })` | Profile data (name, avatar, status) |
| `steam_getOwnedGames({ steamid })` | Game library with playtime |
| `steam_getWorkshopItem({ publishedfileid })` | Workshop item details |
| `steam_queryWorkshop({ appid, query_type, count })` | Workshop search/browse |
| `steam_getLeaderboardEntries({ appid, leaderboardid, rangestart?, rangeend? })` | Leaderboard data |
| `steam_resolveVanityURL({ vanity })` | Vanity URL to 64-bit Steam ID |

### Skill Updates

Update all 14 existing skills to reference MCP tools where applicable. Replace "MCP Integration (Future)" placeholder sections with concrete "MCP Usage" sections.

### New Rule

- `steam-api-key-usage.mdc` - when MCP tools are available, guide users to prefer MCP calls over raw curl commands

---

## v0.3.0 - "Insights" (Analytics and Market Research)

**Theme:** Data-driven decision-making for game developers and analysts.

### New Skills

| Skill | Description |
|-------|-------------|
| `steam-review-analysis` | Fetch and analyze game reviews: sentiment breakdown, common complaints, comparison across updates, language distribution |
| `steam-price-history` | Pricing trends, sale history, regional pricing analysis, price-to-review value scoring |
| `steam-market-research` | Genre trend analysis, tag popularity, competitor identification, market gap analysis using store data |
| `steam-wishlist-estimates` | Estimate wishlists from follower counts and public signals, conversion rate benchmarks |

### New MCP Tools

| Tool | Description |
|------|-------------|
| `steam_getReviews({ appid, filter, language, count })` | Fetch user reviews |
| `steam_getPriceOverview({ appids, cc })` | Batch price check across regions |

---

## v0.4.0 - "Ship It" (CI/CD and Build Pipeline)

**Theme:** Automate the Steam build and release process.

### New Skills

| Skill | Description |
|-------|-------------|
| `steam-build-automation` | SteamPipe CI/CD integration (GitHub Actions, GitLab CI, Jenkins), automated depot uploads, branch management (beta/default) |
| `steam-release-checklist` | Pre-release validation: store page completeness, depot config, achievements uploaded, cloud save tested, Deck compat reviewed |
| `steam-steamcmd-helper` | steamcmd scripting reference, common commands, batch scripts, Docker containerized builds |

### New Rules

| Rule | Description |
|------|-------------|
| `steam-build-config-validation.mdc` | Validate VDF build configs: missing depots, mismatched app IDs, invalid file mappings |
| `steam-launch-options-check.mdc` | Flag launch option issues: missing executables, wrong OS targeting, missing descriptions for multi-launch |

---

## v0.5.0 - "Grow" (Community and Monetization)

**Theme:** Post-launch growth, community management, and revenue.

### New Skills

| Skill | Description |
|-------|-------------|
| `steam-community-management` | Announcements, event creation, discussion forum moderation patterns, update post templates |
| `steam-store-page-optimizer` | Store page best practices: capsule image specs, description structure, tag strategy, trailer guidance, demo setup |
| `steam-pricing-strategy` | Regional pricing recommendations, launch discount planning, sale participation, bundle strategy, free-to-play conversion |
| `steam-dlc-expansion-planning` | DLC roadmap templates, season pass structure, content cadence planning, pricing tiers |

### New MCP Tools

| Tool | Description |
|------|-------------|
| `steam_getAppReviewSummary({ appid })` | Review histogram and summary |
| `steam_getRegionalPricing({ appid, countries })` | Pricing by region |

---

## v0.6.0 - "Quality" (Testing, QA, and Rules)

**Theme:** Catch issues before players do.

### New Skills

| Skill | Description |
|-------|-------------|
| `steam-playtest-setup` | Steam Playtest feature configuration, feedback collection, NDA playtest vs open playtest, key distribution |
| `steam-bug-report-template` | Structured bug report templates with Steam system info integration, crash dump guidance |
| `steam-anticheat-integration` | EAC and BattlEye setup, Proton/Linux compatibility, VAC integration, custom anti-cheat considerations |

### New Rules

| Rule | Description |
|------|-------------|
| `steam-save-compat.mdc` | Flag save file practices that break cross-platform cloud sync: binary endianness, OS-specific paths, hardcoded separators |
| `steam-network-security.mdc` | Flag insecure networking patterns: unvalidated auth tickets, missing encryption, trusting client data |
| `steam-api-error-handling.mdc` | Flag missing error/callback handling for Steamworks SDK calls: unchecked results, missing `StoreStats()`, ignored callbacks |

---

## v0.7.0 - "Full Power" (Advanced MCP - Write Operations)

**Theme:** Expand MCP server with write/mutation capabilities.

### New MCP Tools (Write Operations)

| Tool | Description |
|------|-------------|
| `steam_createLobby({ type, maxPlayers, metadata })` | Create multiplayer lobbies |
| `steam_uploadWorkshopItem({ appid, title, content_path })` | Upload new Workshop items |
| `steam_updateWorkshopItem({ fileid, changes })` | Update existing Workshop items |
| `steam_setAchievement({ steamid, achievement })` | Unlock achievements (dev/test) |
| `steam_uploadLeaderboardScore({ appid, leaderboard, score })` | Upload leaderboard scores |
| `steam_grantInventoryItem({ steamid, itemdef })` | Grant inventory items (dev/test) |

### New Skill

| Skill | Description |
|-------|-------------|
| `steam-testing-sandbox` | Guide for using App ID 480 (SpaceWar) as a development sandbox, test account setup, Steam client developer console commands |

### Rule Updates

- Update `steam-appid-validation.mdc` to integrate with MCP for live validation (check if App ID exists via API)

---

## v0.8.0 - "Polish" (Refinement and Gaps)

**Theme:** Fill gaps, improve consistency, harden everything.

### Improvements

- Audit and improve all skill workflows for clarity and completeness
- Add troubleshooting/error reference sections to every skill
- Add cross-references between related skills (e.g., multiplayer links to friends/social, leaderboards links to player stats)
- Ensure every MCP tool has proper error handling documented
- Add "Common Pitfalls" sections to skills that deal with tricky APIs

### New Skill

| Skill | Description |
|-------|-------------|
| `steam-migration-guide` | Migrating from other platforms (Epic, GOG, itch.io) to Steam, or porting between engines with Steamworks |

### Documentation

- Comprehensive MCP server README with setup instructions
- API rate limiting and best practices guide
- Full skill/rule cross-reference matrix

---

## v0.9.0 - "Complete" (Final MCP Tools)

**Theme:** Reach the target of 25 MCP tools by adding the 4 remaining read-only tools.

### New MCP Tools (Read-Only, No Auth)

| Tool | Description |
|------|-------------|
| `steam_getReviews({ appid, filter, language, review_type, purchase_type })` | Fetch user reviews with pagination and filters |
| `steam_getPriceOverview({ appids, cc })` | Batch price check for multiple apps in a region |
| `steam_getAppReviewSummary({ appid })` | Review score, totals, and positive percentage (no individual reviews) |
| `steam_getRegionalPricing({ appid, countries })` | Pricing breakdown across multiple countries |

---

## v1.0.0 - "Stable" (Production Release)

**Theme:** Stable, complete, production-ready plugin.

### Release Checklist

- [x] All 30 skills reviewed and tested
- [x] All 25 MCP tools documented and stable
- [x] All 9 rules validated against real projects
- [x] CHANGELOG fully up to date
- [x] README reflects final feature set
- [x] Version locked at 1.0.0, semver from here on out
- [x] Target audience expanded to include modders alongside game developers and power users

---

## Completed

- [x] ~~Steam Deck compatibility checker~~ - added in v0.1.0 as a rule
- [x] ~~Steamworks SDK code generation~~ - covered by multiplayer, cloud, leaderboard, input, and inventory skills
- [x] ~~Steam MCP server with 10 read-only tools~~ - companion repo [steam-mcp](https://github.com/TMHSDigital/steam-mcp), skills updated in v0.2.0
- [x] ~~MCP tool preference rule~~ - `steam-api-key-usage.mdc` added in v0.2.0
- [x] ~~Review analysis skill~~ - `steam-review-analysis` added in v0.3.0
- [x] ~~Price history skill~~ - `steam-price-history` added in v0.3.0
- [x] ~~Market research skill~~ - `steam-market-research` added in v0.3.0
- [x] ~~Wishlist estimates skill~~ - `steam-wishlist-estimates` added in v0.3.0
- [x] ~~Build automation skill~~ - `steam-build-automation` added in v0.4.0
- [x] ~~Release checklist skill~~ - `steam-release-checklist` added in v0.4.0
- [x] ~~SteamCMD helper skill~~ - `steam-steamcmd-helper` added in v0.4.0
- [x] ~~Build config validation rule~~ - `steam-build-config-validation.mdc` added in v0.4.0
- [x] ~~Launch options check rule~~ - `steam-launch-options-check.mdc` added in v0.4.0
- [x] ~~Community management skill~~ - `steam-community-management` added in v0.5.0
- [x] ~~Store page optimizer skill~~ - `steam-store-page-optimizer` added in v0.5.0
- [x] ~~Pricing strategy skill~~ - `steam-pricing-strategy` added in v0.5.0
- [x] ~~DLC expansion planning skill~~ - `steam-dlc-expansion-planning` added in v0.5.0
- [x] ~~Playtest setup skill~~ - `steam-playtest-setup` added in v0.6.0
- [x] ~~Bug report template skill~~ - `steam-bug-report-template` added in v0.6.0
- [x] ~~Anti-cheat integration skill~~ - `steam-anticheat-integration` added in v0.6.0
- [x] ~~Save compatibility rule~~ - `steam-save-compat.mdc` added in v0.6.0
- [x] ~~Network security rule~~ - `steam-network-security.mdc` added in v0.6.0
- [x] ~~API error handling rule~~ - `steam-api-error-handling.mdc` added in v0.6.0
- [x] ~~Testing sandbox skill~~ - `steam-testing-sandbox` added in v0.7.0
- [x] ~~MCP write tools~~ - 6 write/guidance tools added to steam-mcp in v0.7.0 (createLobby, uploadWorkshopItem, updateWorkshopItem, setAchievement, uploadLeaderboardScore, grantInventoryItem)
- [x] ~~App ID validation MCP enhancement~~ - `steam-appid-validation.mdc` updated with live validation via MCP in v0.7.0
- [x] ~~Migration guide skill~~ - `steam-migration-guide` added in v0.8.0
- [x] ~~Common Pitfalls sections~~ - added to all 30 skills in v0.8.0
- [x] ~~getReviews MCP tool~~ - `steam_getReviews` added in v0.9.0
- [x] ~~getPriceOverview MCP tool~~ - `steam_getPriceOverview` added in v0.9.0
- [x] ~~getAppReviewSummary MCP tool~~ - `steam_getAppReviewSummary` added in v0.9.0
- [x] ~~getRegionalPricing MCP tool~~ - `steam_getRegionalPricing` added in v0.9.0
- [x] ~~getSchemaForGame MCP tool~~ - `steam_getSchemaForGame` added in steam-mcp v0.6.0
- [x] ~~getNewsForApp MCP tool~~ - `steam_getNewsForApp` added in steam-mcp v0.6.0
- [x] ~~getLeaderboardsForGame MCP tool~~ - `steam_getLeaderboardsForGame` added in steam-mcp v0.6.0
- [x] ~~getPlayerAchievements MCP tool~~ - `steam_getPlayerAchievements` added in steam-mcp v0.6.0
- [x] ~~clearAchievement MCP tool~~ - `steam_clearAchievement` added in steam-mcp v0.6.0
