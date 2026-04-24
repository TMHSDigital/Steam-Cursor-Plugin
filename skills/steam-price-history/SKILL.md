---
name: steam-price-history
description: Analyze pricing trends, sale history, regional pricing differences, and price-to-review value scoring for Steam games. Use when evaluating pricing strategy, comparing regional costs, or identifying sale patterns.
standards-version: 1.6.3
---

# Steam Price History

## Trigger

Use this skill when the user:

- Asks about a game's current or historical pricing
- Wants to compare prices across regions
- Needs sale frequency or discount pattern analysis
- Asks about price-to-value metrics (price per hour, price per review score)
- Wants to plan a pricing strategy for their own game
- Asks about regional pricing recommendations

## Required Inputs

- **App ID** or **game name** - the game to analyze
- **Region** (optional) - ISO country code for regional pricing (`us`, `eu`, `gb`, `br`, `ru`, `cn`, etc.)

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use MCP tools where possible. See [MCP Usage](#mcp-usage).

### 1. Resolve the App ID

If the user provided a game name, resolve it first using the [Steam Store Lookup](../steam-store-lookup/SKILL.md) workflow.

### 2. Fetch Current Pricing

```bash
# US pricing (default)
curl.exe "https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&filters=price_overview"

# Regional pricing (e.g., Brazil)
curl.exe "https://store.steampowered.com/api/appdetails?appids={appid}&cc=br&filters=price_overview"
```

Response contains:

```json
{
  "price_overview": {
    "currency": "USD",
    "initial": 2999,
    "final": 1499,
    "discount_percent": 50,
    "initial_formatted": "$29.99",
    "final_formatted": "$14.99"
  }
}
```

### 3. Multi-Region Comparison

Fetch pricing for key markets to identify regional differences:

| Region | Code | Currency |
|--------|------|----------|
| United States | `us` | USD |
| European Union | `de` | EUR |
| United Kingdom | `gb` | GBP |
| Brazil | `br` | BRL |
| Russia | `ru` | RUB |
| China | `cn` | CNY |
| Turkey | `tr` | TRY |
| Argentina | `ar` | ARS |
| Japan | `jp` | JPY |
| Australia | `au` | AUD |

### 4. Historical Pricing Context

Steam does not provide a public historical pricing API. For sale history:

- **SteamDB** (https://steamdb.info/app/{appid}/pricelist/) tracks historical prices and sales
- **IsThereAnyDeal** (https://isthereanydeal.com/) aggregates cross-platform deal history

Document these as external references — they are not accessible via MCP. The agent should:

1. Note the current price and any active discount
2. Mention when SteamDB/ITAD show historical data
3. Provide general guidance on typical sale cadence (Steam seasonal sales in February, June, October, December)

### 5. Value Scoring

Calculate price-to-value metrics when review and playtime data is available:

| Metric | Formula |
|--------|---------|
| Price per hour | `price / median_playtime_hours` |
| Reviews per dollar | `total_reviews / price` |
| Value score | `(positive_ratio × median_hours) / price` |
| Competitor ratio | `game_value_score / genre_avg_value_score` |

Combine with data from [Steam Player Stats](../steam-player-stats/SKILL.md) and [Steam Review Analysis](../steam-review-analysis/SKILL.md).

### 6. Format Output

> **Celeste** (App ID: 504230) - Price Analysis
> - **Current price:** $19.99 USD (no active sale)
> - **Lowest recorded:** $4.99 (75% off — Steam Summer Sale 2023)
> - **Sale frequency:** ~4 major sales/year, typical discount 40-75%
> - **Regional range:** $4.50 (Argentina) – $19.99 (US)
>
> **Value Metrics:**
> - Median playtime: 12.4 hours → **$1.61/hour**
> - Review score: 97% positive → **Value score: 6.01** (genre avg: 2.3)

### 7. Pricing Strategy Guidance (for developers)

If the user is pricing their own game, provide benchmarks:

- Comparable games in the genre by price tier
- Regional pricing recommendations using Valve's suggested regional multipliers
- Launch discount expectations (10-15% is standard)
- Sale cadence strategy (participate in all major Steam sales)
- Price point psychology ($9.99, $14.99, $19.99, $24.99 tiers)

## Key References

| Resource | URL |
|----------|-----|
| Steamworks Pricing | https://partner.steamgames.com/doc/store/pricing |
| Regional Pricing | https://partner.steamgames.com/doc/store/pricing/currencies |
| Discounting Best Practices | https://partner.steamgames.com/doc/marketing/discounts |
| SteamDB Price History | https://steamdb.info/app/{appid}/pricelist/ |

## Example Interaction

**User:** "What's the pricing history for Hades? Is it a good deal right now?"

**Agent:**
1. Resolves "Hades" to App ID `1145360`
2. Fetches current pricing for US and 3-4 other regions
3. Notes current price: $24.99, no active discount
4. References SteamDB for historical lows (~$9.99 at 60% off)
5. Calculates value: median playtime 45h, 97% positive → excellent value even at full price
6. Notes: "Next likely sale: Steam Summer Sale (late June). Historical low is $9.99 at 60% off."

## MCP Usage

| Step | MCP Tool | Auth | Replaces |
|------|----------|------|----------|
| Get current pricing | `steam_getAppDetails({ appid })` | None | `curl` to `appdetails` |
| Multi-region pricing | `steam_getPriceOverview({ appids, cc })` | None | Multiple `curl` calls |
| Resolve name | `steam_searchApps({ query })` | None | Manual search |

For regional pricing across multiple countries in a single call, use `steam_getRegionalPricing({ appid, countries })`.

If the MCP server is not available, fall back to the `curl`-based workflow above.

## Common Pitfalls

1. **Not accounting for regional pricing tiers** — Steam's suggested regional prices don't scale linearly with USD. Some regions have significantly lower purchasing power adjustments.
2. **Comparing prices without considering bundles** — a game's "effective price" drops significantly when included in popular bundles. Raw store price doesn't tell the full story.
3. **Ignoring historical lows from third-party key sellers** — Steam price history alone doesn't show prices on Humble, Fanatical, etc. Players track lowest-ever prices across all stores.
4. **Using cached price data for time-sensitive decisions** — Steam prices change during sales, regional adjustments, and publisher updates. Always fetch fresh data for pricing decisions.

## See Also

- [Steam Store Lookup](../steam-store-lookup/SKILL.md) - get store data and resolve game names
- [Steam Game Comparison](../steam-game-comparison/SKILL.md) - compare pricing across similar games
- [Steam Market Research](../steam-market-research/SKILL.md) - genre and competitor analysis including pricing tiers
