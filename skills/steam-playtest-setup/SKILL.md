---
name: steam-playtest-setup
description: Configure Steam Playtest for pre-release testing. Covers playtest App ID creation, open vs NDA playtests, key distribution, signup page setup, feedback collection, and transition to Early Access or launch. Use when setting up player testing before or during Early Access.
standards-version: 1.9.0
---

# Steam Playtest Setup

## Trigger

Use this skill when the user:

- Wants to set up a Steam Playtest for their game
- Asks about open vs closed/NDA playtests
- Needs to generate and distribute playtest keys
- Wants to configure a playtest signup page
- Asks about collecting feedback during a playtest
- Is transitioning from playtest to Early Access or full launch

## Required Inputs

- **Base game App ID** - the parent game
- **Playtest type** - open playtest, closed/NDA playtest, or Next Fest demo

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use it to verify the base game. See [MCP Usage](#mcp-usage).

### 1. Understanding Steam Playtest

Steam Playtest is a free, separate app linked to your base game that lets players request access and try your game before launch. It is distinct from demos:

| Feature | Steam Playtest | Demo |
|---------|---------------|------|
| Separate App ID | Yes | Yes |
| Free | Always | Always |
| Access control | Developer-controlled (approve/deny) | Open to all |
| Time-limited | Typically yes | Optional |
| Shows on base game page | Yes (signup button) | Yes (download button) |
| Player data | Playtest-specific stats | Demo-specific stats |
| Ideal for | Pre-release testing, feedback | Permanent store presence |

### 2. Creating a Playtest

**In Steamworks Partner:**

1. Navigate to your base game > **All Associated Packages, DLC, Demos, and Tools**
2. Click **Create Playtest**
3. Steamworks generates a linked Playtest App ID
4. Configure the playtest:
   - **Name**: "[Game Name] Playtest"
   - **Description**: What players should expect and how to give feedback
   - **Build**: Upload a playtest-specific build (can be a subset of the full game)

### 3. Open vs Closed Playtest

| Type | Access | Use case |
|------|--------|----------|
| **Open** | Anyone can join immediately | Maximum reach, stress testing, Next Fest |
| **Closed (manual)** | Developer approves each request | Controlled testing, NDA enforcement |
| **Closed (auto-approve)** | Approve up to N players automatically | Scalable closed testing |
| **Closed (keys)** | Key-based access | Influencer/press access, targeted testing |

**Configuration in Steamworks:**
- Set access mode under Playtest > Settings
- For closed playtests, set maximum participant count
- Enable/disable the "Request Access" button on the store page

### 4. Key Distribution

For closed playtests with key-based access:

1. Go to Steamworks Partner > Your Playtest App > Request Keys
2. Generate a batch of keys (up to 5,000 per request)
3. Distribute via:
   - Direct email to testers
   - Discord bot / community management tool
   - Influencer outreach
   - Curator Connect

**Key management best practices:**
- Track which keys go to whom
- Generate keys in small batches to control distribution
- Revoke unused keys after the playtest ends
- Never post keys publicly — use Steam's key request system

### 5. Playtest Build Configuration

**What to include in a playtest build:**
- Core gameplay loop (enough to evaluate the experience)
- Feedback mechanism (in-game survey, link to form, Discord link)
- Telemetry/analytics if permitted
- Time or content limits to create urgency
- Watermarking or NDA notice for closed tests

**What to exclude:**
- Unfinished content that misrepresents quality
- Spoiler content (late-game, endings)
- Systems not ready for testing

**Build setup:**
- Upload to a separate branch on the playtest App ID
- Use `setlive` to control when players get the build
- Can update the build during the playtest without disrupting players

### 6. Feedback Collection

| Method | Best for | Setup |
|--------|----------|-------|
| **Steam Discussion forums** | Public feedback, bug reports | Enable on playtest Community Hub |
| **In-game survey** | Structured feedback at session end | Custom UI linking to Google Forms / Typeform |
| **Discord** | Real-time discussion, screenshots | Link in playtest description |
| **Telemetry** | Quantitative data (playtime, deaths, progression) | Steam Analytics or custom telemetry |
| **Bug report form** | Structured bug submissions | See [Steam Bug Report Template](../steam-bug-report-template/SKILL.md) |

**Feedback prompt template (in-game or store page):**

```
Thanks for playing the [Game Name] Playtest!

We'd love your feedback:
- What did you enjoy most?
- What frustrated you?
- Did you encounter any bugs? (describe steps to reproduce)
- How likely are you to wishlist the full game? (1-5)

Submit feedback: [link to form]
Report bugs: [link to forum or form]
Join the community: [Discord link]
```

### 7. Steam Next Fest Integration

Steam Next Fest is a week-long event where developers can showcase upcoming games with playable demos or playtests.

**Next Fest requirements:**
- Game must have a "Coming Soon" page live
- Playtest or demo must be available during the event
- Registration deadline is typically 6 weeks before the event
- Developer livestreams are available during Next Fest

**Next Fest schedule (approximate):**
- February Next Fest
- June Next Fest
- October Next Fest

### 8. Transitioning from Playtest

**Playtest → Early Access:**
1. End the playtest (revoke access or leave open)
2. Launch the base game as Early Access
3. Playtest players receive a notification about the base game
4. Consider offering a launch discount to playtest participants

**Playtest → Full Launch:**
1. End the playtest
2. Launch the base game
3. Playtest reviews/data do NOT transfer to the base game
4. Wishlist conversions from playtest are tracked separately

**Best practice:** Keep the playtest open during Early Access if you want continuous external testing of new builds.

## Key References

| Resource | URL |
|----------|-----|
| Steam Playtest | https://partner.steamgames.com/doc/features/playtest |
| Steam Next Fest | https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest |
| Key Management | https://partner.steamgames.com/doc/features/keys |

## Example Interaction

**User:** "I want to run a closed playtest for my game before Early Access. How do I set it up?"

**Agent:**
1. Explains the Steam Playtest feature and how it differs from demos
2. Walks through Playtest App ID creation in Steamworks Partner
3. Recommends closed playtest with auto-approve (cap at 1,000 players)
4. Advises on build content: "Include your first 2 hours of gameplay. Add an end-of-session feedback prompt."
5. Suggests feedback channels: Steam forums + in-game survey + Discord
6. Notes: "Register for the next Steam Next Fest for maximum visibility."

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Verify base game | `steam_getAppDetails({ appid })` | None | Confirm game exists and check current state |

Playtest creation and management require the Steamworks Partner site — not available via MCP.

## Common Pitfalls

1. **Not setting a player cap** — open playtests without limits can overwhelm servers and support capacity. Start with a small cap and increase gradually.
2. **Using the playtest App ID for production features** — playtest App IDs are separate from the main game. Achievements, leaderboards, and cloud saves configured on the playtest don't transfer to the main app.
3. **Forgetting to close signups** — leaving playtest signups open indefinitely dilutes the urgency. Set clear windows aligned with your testing schedule.
4. **Not collecting feedback through Steam** — Steam Discussions has built-in playtest forums. Using only external feedback tools (Discord, Google Forms) misses players who prefer staying in Steam.
5. **Skipping Next Fest integration** — Steam Next Fest is the highest-visibility opportunity for playtests. Plan your playtest timing around it.

## See Also

- [Steam Release Checklist](../steam-release-checklist/SKILL.md) - full pre-launch checklist
- [Steam Community Management](../steam-community-management/SKILL.md) - managing playtest community
- [Steam Bug Report Template](../steam-bug-report-template/SKILL.md) - structured bug reporting for playtests
