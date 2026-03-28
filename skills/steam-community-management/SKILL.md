---
name: steam-community-management
description: Post-launch community management for Steam games. Covers announcements, events, discussion forum moderation, update post templates, and Community Hub configuration. Use when managing player communication, creating events, or setting up community channels.
---

# Steam Community Management

## Trigger

Use this skill when the user:

- Wants to post an announcement or patch notes on Steam
- Needs templates for update posts, sale announcements, or roadmap updates
- Asks about Steam Events (livestreams, free weekends, seasonal events)
- Wants to set up or moderate Steam Discussion forums
- Asks about Community Hub configuration (screenshots, artwork, guides)
- Needs help with community engagement strategy post-launch

## Required Inputs

- **App ID** - the game's Steam App ID
- **Task** - what the user wants to do (post announcement, create event, set up forums, etc.)

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use it to verify app details. See [MCP Usage](#mcp-usage).

### 1. Steam Announcements

Announcements appear in the game's Community Hub, the Activity Feed, and as notifications to followers/owners.

**Announcement types:**

| Type | Use case | Visibility |
|------|----------|------------|
| Regular update | Patch notes, minor updates | Owners + followers |
| Major update | Large content drops, expansions | Broader reach, Steam algorithm boost |
| Event | Time-limited events, sales, livestreams | Calendar integration |

**Patch notes template:**

```markdown
## [Game Name] Update v1.2.0 - [Title]

### New Features
- Feature 1: brief description
- Feature 2: brief description

### Improvements
- Improvement 1
- Improvement 2

### Bug Fixes
- Fixed issue where [description]
- Fixed crash when [description]

### Known Issues
- Issue 1 (fix in progress)

---
Thanks for playing! Join the discussion below or report bugs in the Bug Reports forum.
```

**Major update template:**

```markdown
# [Update Name] is Live!

[Hero image or GIF]

We're excited to announce [update name], the biggest update to [game] yet!

## What's New

### [Feature Category 1]
[Description with screenshots]

### [Feature Category 2]
[Description with screenshots]

## How to Access
[Instructions — update automatically, opt into beta, etc.]

## What's Next
[Teaser for upcoming content]

## Thank You
[Community acknowledgment]
```

**Sale announcement template:**

```markdown
# [Game Name] is [X]% Off!

[Game] is on sale during the [Sale Name]!

🎮 **[X]% off** — now just $[price]
⏰ Sale ends [date]

[Brief game description for new players]

[Link to store page]
```

### 2. Steam Events

Events show on the Steam calendar and can include:

| Event type | Description | Setup |
|------------|-------------|-------|
| **Game Update** | Patch notes linked to a build | Steamworks Partner > Posts |
| **Livestream** | Stream with embedded player | Link YouTube/Twitch URL |
| **Free Weekend** | Temporary free access | Steamworks Partner > Marketing |
| **Sale Event** | Discount period | Steamworks Partner > Pricing |
| **Seasonal Event** | Time-limited in-game content | Custom event + in-game integration |
| **Tournament** | Competitive event | Custom event type |

**Event creation flow:**
1. Go to Steamworks Partner > Your App > Community > Posts & Events
2. Choose event type
3. Set title, description, start/end times
4. Add cover image (800×450 recommended)
5. Optionally link to a game build/branch
6. Save as draft → preview → publish

### 3. Discussion Forums

**Recommended forum structure:**

| Forum | Description | Moderation |
|-------|-------------|------------|
| General Discussion | Open chat about the game | Light moderation |
| Bug Reports | Structured bug submissions | Developer-monitored |
| Suggestions & Feedback | Feature requests | Developer-monitored |
| Guides & Tutorials | Player-created guides | Community-driven |
| Announcements | Dev posts only | Locked to developers |
| Modding (if applicable) | Mod discussion & support | Community-driven |

**Moderation best practices:**
- Pin important threads (FAQ, known issues, rules)
- Respond to bug reports with acknowledgment, even if no fix yet
- Create megathreads for common topics to reduce noise
- Use Steam's built-in moderation tools (delete, lock, move, ban)
- Set up sub-forum permissions for announcement-only forums

### 4. Community Hub Configuration

The Community Hub includes:

- **Screenshots** — enable/disable player screenshots
- **Artwork** — player-submitted artwork and fan art
- **Videos** — player gameplay videos
- **Guides** — player-written guides and walkthroughs
- **Reviews** — player reviews (always enabled)
- **Workshop** — if Workshop is configured

**Configuration in Steamworks Partner:**
1. Community > General Settings
2. Enable/disable each section
3. Set content moderation level
4. Configure Community Hub visibility

### 5. Communication Cadence

Recommended post-launch communication schedule:

| Frequency | Content |
|-----------|---------|
| Weekly | Community engagement (respond to forums, social media) |
| Bi-weekly | Minor update posts or devlog entries |
| Monthly | Roadmap progress update or major patch notes |
| Quarterly | Major content update announcements |
| As needed | Critical bug fix notices, sale announcements |

## Key References

| Resource | URL |
|----------|-----|
| Steam Announcements | https://partner.steamgames.com/doc/marketing/event_tools |
| Community Hub | https://partner.steamgames.com/doc/features/community |
| Discussion Forums | https://partner.steamgames.com/doc/features/community#discussions |
| Steam Events | https://partner.steamgames.com/doc/marketing/event_tools/events |

## Example Interaction

**User:** "I just released a big content update. Help me write patch notes and set up an announcement."

**Agent:**
1. Asks for update highlights, new features, and bug fixes
2. Generates a structured patch notes post using the major update template
3. Recommends posting as a "Major Update" event type for maximum visibility
4. Suggests adding a cover image (800x450) and linking to the update build
5. Advises: "Post during peak hours (10am-2pm PST weekdays) for maximum initial visibility."

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Verify app | `steam.getAppDetails({ appid })` | None | Confirm app name and current state |
| Check reviews | `steam.getAchievementStats({ appid })` | None | Reference achievement data in update posts |

Community management actions (posting, moderating) require the Steamworks Partner site — they are not available via API or MCP.

## See Also

- [Steam Store Page Optimizer](../steam-store-page-optimizer/SKILL.md) - optimize store page for conversions
- [Steam Review Analysis](../steam-review-analysis/SKILL.md) - analyze player feedback to inform community posts
- [Steam Release Checklist](../steam-release-checklist/SKILL.md) - pre-launch community setup
