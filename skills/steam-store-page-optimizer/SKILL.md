---
name: steam-store-page-optimizer
description: Optimize Steam store pages for maximum visibility and conversion. Covers capsule image specs, description structure, tag strategy, trailer guidance, demo setup, and screenshot optimization. Use when building or improving a Steam store page.
---

# Steam Store Page Optimizer

## Trigger

Use this skill when the user:

- Is building or improving a Steam store page
- Asks about capsule image sizes, specs, or guidelines
- Needs help writing store page descriptions
- Wants tag strategy advice for discoverability
- Asks about trailer requirements or best practices
- Wants to set up a demo on Steam
- Needs screenshot guidance

## Required Inputs

- **App ID** or **game name** - the game to optimize
- **Focus area** (optional) - images, description, tags, trailer, demo, or full audit

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use it to fetch the current store page state. See [MCP Usage](#mcp-usage).

### 1. Capsule Images

All images are required before the store page can go live.

| Asset | Size | Format | Usage |
|-------|------|--------|-------|
| **Header Capsule** | 460×215 | JPG/PNG | Library, search results, featured lists |
| **Small Capsule** | 231×87 | JPG/PNG | Wishlists, search, smaller displays |
| **Main Capsule** | 616×353 | JPG/PNG | Store page header, browse pages |
| **Hero Capsule** | 3840×1240 | JPG/PNG | Top of store page (with logo overlay) |
| **Page Background** | 1438×810 | JPG/PNG | Store page background (faded edges) |
| **Library Capsule** | 600×900 | JPG/PNG | Steam Library grid view |
| **Library Hero** | 3840×1240 | JPG/PNG | Steam Library detail view |
| **Library Logo** | 1280×720 | PNG (transparent) | Overlaid on Library Hero |
| **Community Icon** | 32×32 | JPG | Community Hub, activity feed |

**Image guidelines:**
- Game title/logo must be readable at small sizes
- No review quotes, awards, or "Game of the Year" text
- No "Coming Soon", "Available Now", or date text
- Consistent branding across all capsule sizes
- Hero capsule: place logo in lower-left third; leave upper area for background art
- High contrast — images are shown on both light and dark backgrounds

### 2. Store Description

**Short description** (< 300 characters):
- Lead with the core hook — what makes this game unique
- Include genre/type for context
- End with a call to action or key feature

**Long description structure:**

```
[Opening hook — 1-2 sentences that sell the fantasy]

[Key Features section with bullet points]
• Feature 1 — brief elaboration
• Feature 2 — brief elaboration
• Feature 3 — brief elaboration
• Feature 4 — brief elaboration

[Gameplay description — what does the player actually DO?]

[Unique selling points — what makes this different from competitors?]

[Social proof if available — "From the makers of..." or community milestones]
```

**Description tips:**
- Front-load the most compelling content (many players only read the first paragraph)
- Use Steam's formatting: `[h2]`, `[b]`, `[list]`, `[img]`
- Include 1-2 GIFs or images inline (use `[img]{url}[/img]`)
- Keep paragraphs short — 2-3 sentences max
- Avoid jargon unless your audience expects it
- Don't repeat information already visible on the page (tags, system requirements)

### 3. Tags

Tags are the primary discoverability mechanism on Steam.

**Strategy:**
- Apply 15-20 tags (the maximum Steam allows)
- First 5 tags carry the most weight — make them count
- Mix broad tags (Action, RPG) with specific ones (Roguelike Deckbuilder, Souls-like)
- Include mechanic tags (Turn-Based, Co-op, Open World)
- Include theme tags (Pixel Art, Dark Fantasy, Cozy)
- Check competitor games to see which tags drive traffic in your niche
- Monitor tag voting — players can upvote/downvote your tags

**Tag research workflow:**
1. Search for your genre on Steam
2. Note which tags the top-performing games use
3. Use `steam_searchApps({ term })` to find competitors
4. Use `steam_getAppDetails({ appid })` to inspect their tags
5. Cross-reference with your game's actual features

### 4. Trailer

**Specifications:**
- Format: MP4 (H.264 video, AAC audio)
- Resolution: 1920×1080 minimum, 3840×2160 recommended
- Framerate: 30 or 60 fps
- Length: 60-90 seconds ideal, 2 minutes maximum

**Content best practices:**
- Start with gameplay, not logos or intros (first 10 seconds are critical)
- Show actual gameplay, not just cinematics
- Demonstrate the core loop: what does the player DO?
- Include variety: different levels, abilities, environments
- End with the game title, release date, and call to action
- Consider a separate "Story Trailer" and "Gameplay Trailer"

**Upload:**
- Steamworks Partner > Store Page > Trailers
- Add multiple trailers (gameplay first, story second)
- Set the first trailer as the autoplay trailer on the store page

### 5. Screenshots

**Requirements:**
- Minimum 5, recommended 10-20
- Resolution: 1920×1080 minimum
- Must be actual in-game screenshots (no concept art in the screenshot section)
- No watermarks, logos, or marketing text overlaid

**Optimization:**
- Lead with the most visually impressive screenshot
- Show gameplay variety: different environments, mechanics, characters
- Include UI screenshots to set expectations
- Order by visual impact, then by game progression
- Consider adding captions via Steamworks (short text overlay on hover)

### 6. Demo Setup

**Creating a demo:**
1. Steamworks Partner > Your App > Demos
2. Create a separate Demo App ID (linked to the main game)
3. Configure demo-specific depots
4. Set demo build content (time-limited, level-limited, feature-limited)
5. Configure "Get the Full Game" link within demo

**Demo strategy:**
- Time-limited demos (30-60 minutes) create urgency
- Level/chapter-limited demos let players reach a hook point
- Next Fest demos run during Steam Next Fest events for maximum visibility
- Keep the demo available after launch — it continues to convert

### 7. Store Page Audit Checklist

For a full audit, verify:

- [ ] All capsule images uploaded and compliant
- [ ] Short description compelling and under 300 characters
- [ ] Long description structured with features, hooks, and formatting
- [ ] 15+ tags applied with strategic ordering
- [ ] At least one trailer (gameplay-first, 60-90 seconds)
- [ ] 10+ screenshots showing gameplay variety
- [ ] System requirements accurate for all platforms
- [ ] Supported languages listed
- [ ] Content descriptors and maturity ratings set
- [ ] "About This Game" section uses Steam BBCode formatting
- [ ] Demo available (if applicable)

## Key References

| Resource | URL |
|----------|-----|
| Store Page Assets | https://partner.steamgames.com/doc/store/assets |
| Capsule Image Rules | https://partner.steamgames.com/doc/store/assets/rules |
| Store Page Best Practices | https://partner.steamgames.com/doc/store/editing |
| Tags Documentation | https://partner.steamgames.com/doc/store/tags |
| Trailer Best Practices | https://partner.steamgames.com/doc/store/trailer |

## Example Interaction

**User:** "I need to set up my Steam store page. The game is a pixel art metroidvania. What do I need?"

**Agent:**
1. Provides the full capsule image size reference table
2. Generates a description template tailored to metroidvanias
3. Recommends tags: Metroidvania, Action, Pixel Graphics, Platformer, Exploration, Side Scroller, 2D, Indie, Singleplayer, Atmospheric, etc.
4. Trailer advice: "Open with a 5-second gameplay clip showing exploration and combat. Show at least 3 different biomes."
5. Screenshot guidance: "Lead with your most visually striking environment. Include one screenshot showing the map, one showing combat, one showing a boss."

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Current page state | `steam_getAppDetails({ appid })` | None | Check existing description, tags, screenshots, price |
| Competitor research | `steam_searchApps({ term })` | None | Find competing games in the genre |
| Competitor details | `steam_getAppDetails({ appid })` | None | Inspect competitor tags, descriptions, pricing |

## Common Pitfalls

1. **Using the wrong capsule image dimensions** — Steam has strict size requirements for each capsule type (header, small, main, hero, library). Wrong sizes get rejected or look blurry.
2. **Burying the game's hook in the description** — the first ~300 characters of your description show in search results. Lead with your unique selling point, not generic genre descriptions.
3. **Over-tagging your game** — applying too many tags (15+) dilutes each tag's weight. Focus on 5-8 highly relevant tags that accurately describe your game.
4. **Not having a trailer in the first media slot** — the first media item is auto-played on the store page. A screenshot in slot 1 means players miss your trailer unless they scroll.
5. **Forgetting to localize the store page** — Steam shows localized store pages when available. Even translating the short description and tags into top-5 languages significantly increases visibility.

## See Also

- [Steam Market Research](../steam-market-research/SKILL.md) - competitor analysis and tag research
- [Steam Release Checklist](../steam-release-checklist/SKILL.md) - full pre-launch checklist including store page
- [Steam Community Management](../steam-community-management/SKILL.md) - post-launch community engagement
