---
name: steam-wishlist-estimates
description: Estimate wishlist counts from follower data, review counts, and public signals. Provides conversion rate benchmarks (wishlist-to-sales, review-to-sales) and the Boxleiter method. Use when forecasting launch sales, evaluating pre-release traction, or setting marketing targets.
standards-version: 1.9.0
---

# Steam Wishlist Estimates

## Trigger

Use this skill when the user:

- Wants to estimate how many wishlists a game has
- Asks about wishlist-to-sales conversion rates
- Needs to forecast launch-week or first-month sales
- Asks about the Boxleiter method or review multipliers
- Wants to reverse-engineer sales from review counts
- Needs benchmarks for pre-release marketing targets

## Required Inputs

- **App ID** or **game name** - the game to analyze
- **Context** (optional) - whether the game is pre-release (wishlist estimation) or post-release (sales estimation)

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use MCP tools. See [MCP Usage](#mcp-usage).

### 1. Resolve the App ID

If the user provided a game name, resolve it first using the [Steam Store Lookup](../steam-store-lookup/SKILL.md) workflow.

### 2. Fetch Available Data

```bash
curl.exe "https://store.steampowered.com/api/appdetails?appids={appid}"
```

Key data points:

| Signal | Source | Notes |
|--------|--------|-------|
| Review count | `appdetails → recommendations.total` | Post-launch only |
| Follower count | Steam store page (not in API) | Pre-launch indicator |
| Current players | `GetNumberOfCurrentPlayers` | Activity proxy |
| Release date | `appdetails → release_date` | For time-based estimates |
| Price | `appdetails → price_overview` | Affects conversion rates |

### 3. Estimation Methods

#### The Boxleiter Method (Review Multiplier)

The most widely used estimation technique. Multiply total reviews by a factor:

| Scenario | Multiplier | Confidence |
|----------|------------|------------|
| Typical indie (2020+) | × 20-30 | Medium |
| Niche/enthusiast games | × 30-50 | Low-Medium |
| Broad-appeal/mainstream | × 15-20 | Medium |
| Free-to-play | × 50-80 | Low |
| Early Access | × 25-40 | Low |
| Very high price ($40+) | × 40-60 | Low |

**Example:** A game with 5,000 reviews → estimated 100,000-150,000 total units (at × 20-30).

The multiplier varies based on genre, price, platform, and visibility. The 2020+ range has shifted lower as Steam's review rate has increased.

#### Wishlist-to-Sales Conversion

Industry benchmarks for launch performance:

| Metric | Typical Range |
|--------|---------------|
| Wishlist → Day 1 purchase | 5-15% |
| Wishlist → Week 1 purchase | 10-20% |
| Wishlist → First month | 15-30% |
| Wishlist → Lifetime | 30-60% |

These vary significantly by:
- **Genre**: action/roguelike converts higher; narrative/VN converts lower
- **Price**: lower price → higher conversion
- **Marketing intensity**: active launch campaigns push week-1 higher
- **Season**: holiday releases convert differently

#### Follower-to-Wishlist Ratio

For pre-release games where follower count is visible:

| Source | Multiplier |
|--------|------------|
| Steam followers → wishlists | × 3-7 (typical × 5) |
| "Follow" button on store page captures a subset of interested users |

### 4. Revenue Estimation

| Factor | Value |
|--------|-------|
| Gross revenue | `units × price` |
| After Steam cut (30%) | `gross × 0.70` |
| After Steam cut (25%, >$10M) | `gross × 0.75` |
| After Steam cut (20%, >$50M) | `gross × 0.80` |
| After refunds (~5-15%) | `net × 0.90` |
| After regional pricing discount | `net × 0.85` (rough) |

### 5. Format Output

> **Hollow Knight** (App ID: 367520) - Sales Estimates
>
> **Observed data:**
> - Reviews: 142,000 (96% positive)
> - Current price: $14.99
> - Released: February 2017
>
> **Estimated total sales:** 2.8M - 4.3M units
> - Boxleiter (× 20): 2,840,000
> - Boxleiter (× 30): 4,260,000
> - Median estimate: ~3.5M units
>
> **Estimated gross revenue:** $42M - $64M
> **Estimated net (after Steam cut + refunds):** $26M - $40M
>
> *Note: These are rough estimates. Actual figures depend on discount sales mix, regional pricing, and bundle participation.*

### 6. Pre-Release Forecasting

For unreleased games, provide a target framework:

| Wishlist Target | Expected Week-1 Sales | Expected Month-1 Sales |
|-----------------|----------------------|------------------------|
| 5,000 | 500-1,000 | 750-1,500 |
| 10,000 | 1,000-2,000 | 1,500-3,000 |
| 50,000 | 5,000-10,000 | 7,500-15,000 |
| 100,000 | 10,000-20,000 | 15,000-30,000 |
| 500,000 | 50,000-100,000 | 75,000-150,000 |

Flag that 10,000+ wishlists at launch is often cited as the threshold for "likely profitability" for a solo/small-team indie.

## Key References

| Resource | URL |
|----------|-----|
| Valve on Wishlists | https://partner.steamgames.com/doc/marketing/wishlist |
| Chris Zukowski (How to Market a Game) | https://howtomarketagame.com/ |
| Simon Carless (GameDiscoverCo) | https://gamediscover.co/ |
| Jake Birkett (Grey Alien Games) | https://greyaliangames.com/ |
| VG Insights | https://vginsights.com/ |

## Example Interaction

**User:** "My game has 25,000 wishlists two weeks before launch. What should I expect?"

**Agent:**
1. Notes wishlist count: 25,000
2. Applies conversion benchmarks:
   - Week 1: 2,500-5,000 sales (10-20%)
   - Month 1: 3,750-7,500 sales (15-30%)
3. If price is $19.99 → Week 1 gross: $50K-$100K
4. After Steam cut + refunds: $31K-$63K net
5. Advises: "This is a solid position for an indie. Focus launch marketing on the first 48 hours — that's when Steam's algorithm weighs sales velocity most heavily."

## MCP Usage

| Step | MCP Tool | Auth | Replaces |
|------|----------|------|----------|
| Get store data | `steam_getAppDetails({ appid })` | None | `curl` to `appdetails` |
| Current players | `steam_getPlayerCount({ appid })` | None | `curl` to `GetNumberOfCurrentPlayers` |
| Resolve name | `steam_searchApps({ query })` | None | Manual search |

All required MCP tools are already available. No new MCP tools needed for this skill.

## Common Pitfalls

1. **Treating wishlist counts as guaranteed sales** — industry median conversion rate is ~15-20% at launch. A game with 10K wishlists typically sells 1.5K-2K copies in the first week.
2. **Comparing wishlist velocity across genres** — niche genres accumulate wishlists slower but convert at higher rates. A strategy game with 5K wishlists may outsell an action game with 20K.
3. **Ignoring wishlist decay** — wishlists degrade over time as players lose interest or buy competing games. Wishlists from 2+ years ago convert at much lower rates.
4. **Not accounting for follower-to-wishlist ratio** — Steam followers are public; wishlists are private. The typical ratio is ~1 follower per 5-10 wishlists, but this varies by visibility.

## See Also

- [Steam Market Research](../steam-market-research/SKILL.md) - genre and competitor analysis
- [Steam Player Stats](../steam-player-stats/SKILL.md) - player counts and achievement data
- [Steam Review Analysis](../steam-review-analysis/SKILL.md) - sentiment data to complement sales estimates
- [Steam Price History](../steam-price-history/SKILL.md) - pricing context for revenue calculations
