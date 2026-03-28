---
name: steam-market-research
description: Genre trend analysis, tag popularity, competitor identification, and market gap analysis using Steam store data. Use when evaluating a game concept's market fit, scouting competitors, or analyzing genre saturation.
---

# Steam Market Research

## Trigger

Use this skill when the user:

- Wants to analyze a genre or tag's popularity on Steam
- Needs to identify competitors for a game concept
- Asks about market gaps or underserved niches
- Wants to evaluate a game idea's viability
- Needs data on release volume, review benchmarks, or pricing tiers within a genre
- Asks "what's selling well" in a category

## Required Inputs

- **Genre, tag, or game concept** - the market segment to research
- **Comparison scope** (optional) - number of competitors, time period, price range

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use MCP tools. See [MCP Usage](#mcp-usage).

### 1. Define the Market Segment

Clarify the scope with the user:

- **Genre tags**: roguelike, metroidvania, city-builder, souls-like, etc.
- **Theme tags**: pixel-art, cozy, horror, sci-fi
- **Mechanics tags**: deck-building, turn-based, co-op, open-world
- **Intersection**: e.g., "roguelike deck-builder" or "cozy farming sim"

### 2. Search for Competitors

```bash
# Search by genre/tag keywords
curl.exe "https://store.steampowered.com/api/storesearch/?term={genre_keyword}&l=english&cc=us"
```

For broader market data, use the Steam search page with tag filtering:
- `https://store.steampowered.com/search/?tags={tag_id}&sort_by=Reviews_DESC`
- Common tag IDs: Roguelike (1716), Metroidvania (9551), City Builder (1643), Souls-like (29482)

### 3. Gather Competitor Data

For each top competitor (aim for 8-15 games), fetch details:

```bash
curl.exe "https://store.steampowered.com/api/appdetails?appids={appid}"
```

Collect per game:

| Field | Source |
|-------|--------|
| Name, release date | `appdetails` |
| Price | `appdetails → price_overview` |
| Review count & score | `appdetails → recommendations` |
| Tags/genres | `appdetails → genres`, `categories` |
| Current players | `GetNumberOfCurrentPlayers` |
| Developer/publisher | `appdetails → developers` |

### 4. Analyze the Market

Present findings in these categories:

**Market Size & Health**
- Total games in segment (estimate from search results)
- Distribution of review scores (what % are Positive or better?)
- Median review count (proxy for visibility/sales)

**Pricing Landscape**
- Price distribution: Free, <$10, $10-20, $20-30, $30+
- Median price for the genre
- Correlation between price and review score

**Competitive Density**
- Release frequency: how many new games in this segment per month?
- Market leaders: top 5 by review count
- Recent successes: top 5 from last 12 months

**Market Gaps**
- Tag combinations with few entries but strong performers
- Underserved platforms (Linux, Steam Deck)
- Missing features common in adjacent genres

### 5. Format Output

> **Market Research: Roguelike Deck-Builders**
>
> **Segment size:** ~85 games tagged roguelike + deck-building
> **Market leaders:**
>
> | Game | Reviews | Score | Price | Players |
> |------|---------|-------|-------|---------|
> | Slay the Spire | 142K | 97% | $24.99 | 8,200 |
> | Monster Train | 18K | 92% | $24.99 | 1,100 |
> | Inscryption | 65K | 96% | $19.99 | 2,400 |
> | Balatro | 98K | 97% | $14.99 | 12,000 |
>
> **Pricing:** Median $14.99, range $4.99-$24.99
> **Gap opportunities:** roguelike deck-builder with co-op (only 3 exist), horror-themed deck-builder (1 exists)
> **Risk:** High competitive density, strong incumbents. Differentiation is critical.

### 6. Viability Assessment

Score the market opportunity:

| Factor | Weight | Score (1-5) |
|--------|--------|-------------|
| Market demand (search volume, wishlist signals) | 25% | — |
| Competitive density | 25% | — |
| Differentiation potential | 20% | — |
| Price ceiling | 15% | — |
| Audience crossover potential | 15% | — |

Provide an overall recommendation: **Strong**, **Moderate**, **Cautious**, or **Avoid**.

## Key References

| Resource | URL |
|----------|-----|
| Steamworks Tags | https://partner.steamgames.com/doc/store/tags |
| Steam Search API | https://store.steampowered.com/search/ |
| Steam Spy (estimates) | https://steamspy.com/ |
| Game Discover Co | https://gamediscover.co/ |
| VG Insights | https://vginsights.com/ |

## Example Interaction

**User:** "I'm thinking about making a cozy farming sim. Is the market too saturated?"

**Agent:**
1. Identifies key tags: farming simulation, cozy, life sim
2. Searches Steam for games with those tags
3. Fetches details for top 15 results
4. Analyzes: 120+ farming sims, but only ~15 with >5K reviews
5. Notes Stardew Valley dominance (500K+ reviews) but also recent successes (Sun Haven, Coral Island)
6. Identifies gaps: farming + crafting automation, farming + mystery/detective
7. Verdict: "Moderate opportunity. Market is large but well-served. Strong differentiation or unique hook required. Price ceiling $24.99."

## MCP Usage

| Step | MCP Tool | Auth | Replaces |
|------|----------|------|----------|
| Search for games | `steam.searchApps({ term })` | None | `curl` to `storesearch` |
| Get game details | `steam.getAppDetails({ appid })` | None | `curl` to `appdetails` |
| Player counts | `steam.getPlayerCount({ appid })` | None | `curl` to `GetNumberOfCurrentPlayers` |

All required MCP tools are already available. No new MCP tools needed for this skill.

## See Also

- [Steam Store Lookup](../steam-store-lookup/SKILL.md) - resolve names and get store data
- [Steam Price History](../steam-price-history/SKILL.md) - pricing analysis for competitors
- [Steam Game Comparison](../steam-game-comparison/SKILL.md) - detailed side-by-side competitor comparison
- [Steam Wishlist Estimates](../steam-wishlist-estimates/SKILL.md) - estimate demand from public signals
