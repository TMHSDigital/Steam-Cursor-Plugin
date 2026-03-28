---
name: steam-pricing-strategy
description: Data-driven pricing strategy for Steam games. Covers regional pricing, launch discounts, sale participation, bundles, free-to-play conversion, and price change rules. Use when setting or adjusting game pricing on Steam.
---

# Steam Pricing Strategy

## Trigger

Use this skill when the user:

- Needs to set a price for their Steam game
- Asks about regional pricing or Valve's suggested multipliers
- Wants to plan launch discounts or sale participation
- Asks about bundles, packages, or pricing tiers
- Is considering free-to-play or free-to-play conversion
- Wants to change their game's price and needs to understand cooldown rules

## Required Inputs

- **App ID** or **game name** - the game to price
- **Context** - new game pricing, price change, sale planning, or regional pricing review

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use it to fetch competitor pricing. See [MCP Usage](#mcp-usage).

### 1. Base Price Selection

Common indie price tiers and what they signal:

| Tier | Price (USD) | Typical game scope | Expected content hours |
|------|-------------|-------------------|----------------------|
| Micro | $0.99-$4.99 | Short experiences, jam games, prototypes | < 2 hours |
| Budget | $4.99-$9.99 | Small indie games, focused experiences | 2-8 hours |
| Standard Indie | $9.99-$14.99 | Full indie games, moderate scope | 5-20 hours |
| Premium Indie | $14.99-$24.99 | Large indie games, deep systems | 15-50+ hours |
| AA | $24.99-$39.99 | High-production indie or AA titles | 20-60+ hours |
| AAA | $49.99-$69.99 | Major studio releases | 30-100+ hours |

**Pricing factors:**
- Genre expectations (roguelikes tolerate higher prices; puzzle games are price-sensitive)
- Content volume (hours of gameplay, replayability)
- Production quality (art, music, voice acting, polish)
- Competitor pricing (use [Steam Market Research](../steam-market-research/SKILL.md) to benchmark)
- Target audience spending habits

### 2. Regional Pricing

Valve provides suggested regional pricing multipliers. Developers can customize.

**Key markets and typical multipliers (relative to USD):**

| Region | Currency | Valve Suggested Multiplier |
|--------|----------|---------------------------|
| United States | USD | 1.00× (base) |
| European Union | EUR | ~0.85-0.95× |
| United Kingdom | GBP | ~0.80-0.90× |
| Brazil | BRL | ~0.40-0.55× |
| Russia | RUB | ~0.30-0.50× |
| Turkey | TRY | ~0.25-0.40× |
| Argentina | ARS | ~0.20-0.35× |
| China | CNY | ~0.50-0.65× |
| Japan | JPY | ~0.90-1.00× |
| Australia | AUD | ~0.95-1.05× |

**Best practices:**
- Start with Valve's suggested prices (they're based on purchasing power parity)
- Adjust for your genre — some genres have different regional demand curves
- Don't set emerging market prices too low (signals low value; invites key resale abuse)
- Review regional pricing at least annually as exchange rates shift
- Use `steam.getAppDetails({ appid })` with `&cc=` param to check competitor regional prices

### 3. Launch Discounts

Steam's launch discount rules:

| Rule | Detail |
|------|--------|
| Maximum discount | 40% at launch |
| Minimum duration | 7 days |
| Cooldown before first sale | 28 days after launch |
| Recommended | 10-15% for established brands, 15-20% for new developers |

**Strategy:**
- A 10% launch discount is the standard expectation — going with no discount is acceptable but converts fewer wishlists
- Higher launch discounts (20-40%) generate more first-week volume but may devalue perception
- Launch discounts stack with wishlist notifications — the discount appears in the notification email

### 4. Sale Participation

**Major Steam sales:**

| Sale | Typical Timing | Registration Deadline |
|------|---------------|----------------------|
| Spring Sale | ~March | ~6 weeks before |
| Summer Sale | ~Late June | ~6 weeks before |
| Autumn Sale | ~Late November | ~6 weeks before |
| Winter Sale | ~Late December | ~6 weeks before |

**Discount progression strategy:**

| Time since launch | Suggested max discount |
|-------------------|----------------------|
| 0-3 months | 10-20% |
| 3-6 months | 20-30% |
| 6-12 months | 30-50% |
| 1-2 years | 50-75% |
| 2+ years | 75-90% |

**Rules:**
- Minimum 28 days between discounts
- Discount must be lower than or equal to any discount in the last 30 days for sale featuring
- Price cannot be raised within 28 days before a discount
- Custom discounts (midweek, weekend deals) can be requested via Steamworks

### 5. Bundles and Packages

| Type | Description | Strategy |
|------|-------------|----------|
| **Complete Your Collection** | Main game + all DLC | Discount 10-15% beyond individual sum |
| **Developer Bundle** | Multiple games from same dev | Cross-promote your catalog |
| **Franchise Bundle** | Series/franchise collection | Drive back-catalog sales |
| **Game + Soundtrack** | Main game + OST | Small premium for music fans |
| **Deluxe Edition** | Game + extras (art book, OST, cosmetics) | 20-40% premium over base |

Bundles dynamically adjust price — players who already own some items pay less.

### 6. Free-to-Play Considerations

**Transitioning to F2P:**
- Revenue shifts from unit sales to microtransactions
- Existing paid owners should receive compensation (exclusive items, premium currency)
- F2P games typically need 10-50× larger player base to match paid revenue
- Steamworks supports F2P with ISteamInventory and ISteamMicroTxn

**Hybrid models:**
- Free demo → paid full game
- Free base game → paid DLC/expansions
- Paid game → free with microtransactions (conversion)

### 7. Price Change Rules

| Action | Cooldown |
|--------|----------|
| Price increase | No cooldown, but cannot discount within 28 days after |
| Price decrease | Treated as a "sale" — 28-day cooldown before next discount |
| Currency-only adjustment | No cooldown for exchange rate corrections |
| Going free | Permanent — cannot return to paid |

## Key References

| Resource | URL |
|----------|-----|
| Steamworks Pricing | https://partner.steamgames.com/doc/store/pricing |
| Regional Pricing | https://partner.steamgames.com/doc/store/pricing/currencies |
| Discounting Rules | https://partner.steamgames.com/doc/marketing/discounts |
| Bundles & Packages | https://partner.steamgames.com/doc/store/application/packages |

## Example Interaction

**User:** "I'm launching a roguelike deckbuilder. 15-20 hours of content. How should I price it?"

**Agent:**
1. Benchmarks competitors: Slay the Spire ($24.99), Balatro ($14.99), Monster Train ($24.99)
2. Analyzes content depth vs competitors
3. Recommends: "$14.99-$19.99 depending on production quality. $14.99 is safer for a new IP; $19.99 is justifiable if polish is high."
4. Regional pricing: "Use Valve's suggested prices as baseline."
5. Launch discount: "10% for 7 days. This converts wishlists without devaluing."
6. Sale plan: "First major sale at 20% off. Reach 50% off by month 8-12."

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Competitor pricing | `steam.getAppDetails({ appid })` | None | Check competitor prices and regional variants |
| Search competitors | `steam.searchApps({ term })` | None | Find competing games for price benchmarking |
| Regional pricing | `steam.getPriceOverview({ appids, cc })` | None | Batch price check (planned MCP tool) |

The `steam.getPriceOverview` tool is planned for the MCP server. Until available, use `steam.getAppDetails` with `&cc=` parameter per region.

## Common Pitfalls

1. **Launching at too high a price then discounting immediately** — early buyers feel cheated, and it trains your audience to wait for sales. Launch at the price you're comfortable with long-term.
2. **Not opting into Steam's regional pricing suggestions** — Valve provides recommended regional prices. Ignoring them means your game is overpriced in lower-income regions, losing sales.
3. **Running discounts too frequently** — constant sales (every 2-3 weeks) devalue your game and train customers to never buy at full price. Major sales 3-4 times per year is typical.
4. **Setting the launch discount above 40%** — Steam limits launch discounts to 40%. Going too close to this cap leaves little room for future sale depth perception.
5. **Forgetting the 30-day cooldown between discounts** — Steam enforces a cooldown period. Plan your discount calendar to avoid conflicts with seasonal sales.

## See Also

- [Steam Price History](../steam-price-history/SKILL.md) - historical pricing data and sale patterns
- [Steam Market Research](../steam-market-research/SKILL.md) - competitor analysis and market positioning
- [Steam Wishlist Estimates](../steam-wishlist-estimates/SKILL.md) - revenue projections at different price points
- [Steam DLC & Expansion Planning](../steam-dlc-expansion-planning/SKILL.md) - DLC pricing tiers
