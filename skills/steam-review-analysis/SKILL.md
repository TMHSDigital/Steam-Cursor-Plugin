---
name: steam-review-analysis
description: Fetch and analyze Steam game reviews. Sentiment breakdown, common complaints, comparison across updates, language distribution, and review volume trends. Use when evaluating player feedback, analyzing competitor reception, or investigating review bombing.
---

# Steam Review Analysis

## Trigger

Use this skill when the user:

- Wants to analyze reviews for a Steam game
- Asks about player sentiment, common complaints, or praise
- Needs a breakdown of positive vs negative reviews
- Wants to compare review sentiment before and after an update
- Asks about review bombing or sudden sentiment shifts
- Needs review data by language or purchase type

## Required Inputs

- **App ID** or **game name** - the game to analyze
- **Analysis scope** (optional) - recent reviews, all-time, specific date range, or language filter

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available and includes `steam_getReviews()`, use it instead of the `curl` commands below. See [MCP Usage](#mcp-usage).

### 1. Resolve the App ID

If the user provided a game name, resolve it first using the [Steam Store Lookup](../steam-store-lookup/SKILL.md) workflow.

### 2. Fetch Reviews

```bash
curl.exe "https://store.steampowered.com/appreviews/{appid}?json=1&filter=recent&language=english&num_per_page=100&review_type=all&purchase_type=all"
```

Key parameters:

| Parameter | Values | Default |
|-----------|--------|---------|
| `filter` | `recent`, `updated`, `all` | `recent` |
| `review_type` | `positive`, `negative`, `all` | `all` |
| `purchase_type` | `steam`, `non_steam_purchase`, `all` | `all` |
| `language` | ISO language code (`english`, `spanish`, `schinese`, etc.) | `all` |
| `num_per_page` | 1-100 | 20 |
| `day_range` | Number of days to look back (only with `filter=recent`) | 30 |
| `cursor` | Pagination cursor from previous response | `*` (first page) |

### 3. Parse the Response

The response contains:

```json
{
  "query_summary": {
    "num_reviews": 100,
    "review_score": 8,
    "review_score_desc": "Very Positive",
    "total_positive": 45231,
    "total_negative": 3892,
    "total_reviews": 49123
  },
  "reviews": [
    {
      "author": { "steamid": "...", "playtime_forever": 1234 },
      "language": "english",
      "review": "Great game, loved the combat...",
      "voted_up": true,
      "timestamp_created": 1700000000,
      "weighted_vote_score": 0.85,
      "steam_purchase": true,
      "received_for_free": false,
      "playtime_at_review": 980
    }
  ],
  "cursor": "next_page_cursor_string"
}
```

### 4. Perform Sentiment Analysis

Present a structured breakdown:

- **Overall score**: `review_score_desc` (e.g., "Very Positive")
- **Ratio**: `total_positive` / `total_reviews` as percentage
- **Recent trend**: compare recent review ratio to all-time ratio
- **Common themes**: scan review text for recurring keywords/phrases
- **Playtime correlation**: average playtime of positive vs negative reviewers
- **Language distribution**: if fetching `language=all`, group by language

### 5. Format Output

> **Hollow Knight** (App ID: 367520) - Review Analysis
> - **Overall:** Overwhelmingly Positive (95.2% of 142,000 reviews)
> - **Recent (30 days):** Very Positive (89.1% of 312 reviews)
> - **Avg playtime (positive):** 48.2 hours
> - **Avg playtime (negative):** 6.1 hours
> - **Common praise:** atmosphere, exploration, boss fights, value for price
> - **Common complaints:** difficulty spikes, map navigation, late-game backtracking

### 6. Advanced Analysis (if requested)

- **Review bombing detection**: flag periods where daily negative reviews spike 5x+ above baseline
- **Update impact**: compare sentiment before/after a specific date
- **Competitor comparison**: fetch reviews for multiple games and compare ratios
- **Language breakdown**: show review count and sentiment per language

## Key References

| Resource | URL |
|----------|-----|
| Steam Reviews API | https://partner.steamgames.com/doc/store/reviews |
| Store page review display | https://partner.steamgames.com/doc/store/application/platforms |
| Review score descriptions | https://www.steamcardexchange.net/index.php?inventorygames-hierarchyscoring |

## Example Interaction

**User:** "Analyze the recent reviews for Baldur's Gate 3. Are players happy with the latest patches?"

**Agent:**
1. Resolves "Baldur's Gate 3" to App ID `1086940`
2. Fetches recent reviews (last 30 days) and all-time summary
3. Compares recent positive % to all-time positive %
4. Scans recent reviews for mentions of patches, bugs, fixes
5. Presents sentiment breakdown with trend comparison
6. Notes: "Recent reviews are 94.3% positive vs 96.1% all-time, suggesting stable sentiment post-patch."

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured and includes the review tool:

| Step | MCP Tool | Auth | Replaces |
|------|----------|------|----------|
| Fetch reviews | `steam_getReviews({ appid, filter?, language?, count? })` | None | `curl` to `/appreviews/` |

The `steam_getReviews` tool is planned for v0.3.0 of the MCP server. Until available, use the `curl`-based workflow above.

Resolve game names with `steam_searchApps({ term })` and get store context with `steam_getAppDetails({ appid })` (both already available).

## Common Pitfalls

1. **Not filtering by language** — English reviews may represent only 30-40% of total reviews. Always check language distribution before drawing conclusions.
2. **Ignoring review bombs** — sudden spikes of negative reviews (often due to external controversies, not game quality) skew overall sentiment. Filter by date range to isolate genuine feedback.
3. **Treating "Mixed" as negative** — "Mixed" (40-69% positive) often means the game has a passionate niche audience alongside vocal critics. Read the actual reviews before judging.
4. **Not comparing pre- and post-update reviews** — reviews left before a major update may no longer reflect the current state. Steam's "Recent Reviews" metric is more actionable than "All Reviews" for evolving games.

## See Also

- [Steam Store Lookup](../steam-store-lookup/SKILL.md) - get store data and resolve game names
- [Steam Player Stats](../steam-player-stats/SKILL.md) - player counts and achievement data to complement review analysis
- [Steam Game Comparison](../steam-game-comparison/SKILL.md) - compare review scores across games
