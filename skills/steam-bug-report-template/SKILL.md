---
name: steam-bug-report-template
description: Generate structured bug report templates for Steam games. Covers report structure, Steam system info integration, crash dump guidance, known issues tracking, and forum integration. Use when setting up bug reporting workflows or helping players submit useful reports.
---

# Steam Bug Report Template

## Trigger

Use this skill when the user:

- Needs a bug report template for their Steam game
- Wants to set up a bug reporting workflow
- Asks about crash dump collection or analysis
- Needs to organize known issues tracking
- Wants to integrate bug reporting with Steam Discussion forums
- Asks about Steam system info for debugging

## Required Inputs

- **Game name** or **App ID** - the game to create templates for
- **Platform** (optional) - which platforms the game supports

## Workflow

### 1. Bug Report Template

Provide a structured template players can use:

```markdown
## Bug Report

**Game Version:** [e.g., 1.2.3]
**Platform:** [Windows / macOS / Linux / Steam Deck]
**Bug Severity:** [Critical / Major / Minor / Cosmetic]

### Description
[Clear, concise description of the bug]

### Steps to Reproduce
1. [First step]
2. [Second step]
3. [Third step]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Frequency
[Always / Sometimes / Rarely / Once]

### Screenshots / Video
[Attach screenshots or video if applicable]

### System Information
[Paste output from Steam > Help > System Information, or use steam://sysinfo]

### Additional Context
[Save file attached? Mods installed? Controller or keyboard?]
```

### 2. Steam System Info

Players can access detailed system information through Steam:

**How to get system info:**
1. Open Steam client
2. Go to **Help > System Information**
3. Copy all text
4. Paste into bug report

**Or use the protocol link:**
```
steam://sysinfo
```

System info includes:
- OS version and architecture
- CPU model and speed
- RAM amount
- GPU model, driver version, VRAM
- Display resolution and refresh rate
- Steam client version
- Installed Steam games and sizes

**Developer-side system info collection:**

```cpp
// Get user's OS via Steamworks
const char* os = SteamUtils()->GetSteamUILanguage();
uint32 ram = SteamUtils()->GetSystemRAM(); // in MB
```

### 3. Crash Dump Collection

**Windows minidumps:**

Configure your game to write minidumps on crash:

```cpp
#include <DbgHelp.h>

LONG WINAPI CrashHandler(EXCEPTION_POINTERS* pExceptionInfo) {
    HANDLE hFile = CreateFileA("crash.dmp", GENERIC_WRITE, 0,
        nullptr, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);

    MINIDUMP_EXCEPTION_INFORMATION mei;
    mei.ThreadId = GetCurrentThreadId();
    mei.ExceptionPointers = pExceptionInfo;
    mei.ClientPointers = FALSE;

    MiniDumpWriteDump(GetCurrentProcess(), GetCurrentProcessId(),
        hFile, MiniDumpWithDataSegs, &mei, nullptr, nullptr);

    CloseHandle(hFile);
    return EXCEPTION_EXECUTE_HANDLER;
}

// Register at startup
SetUnhandledExceptionFilter(CrashHandler);
```

**Unity crash logs:**
- Windows: `%USERPROFILE%\AppData\LocalLow\{Company}\{Product}\Player.log`
- macOS: `~/Library/Logs/Unity/Player.log`
- Linux: `~/.config/unity3d/{Company}/{Product}/Player.log`

**Unreal Engine crash reports:**
- `{Project}/Saved/Crashes/` directory
- UE4/5 Crash Reporter sends reports automatically if configured

**Steam Error Reporting:**
- Steamworks provides crash reporting via `ISteamUtils`
- Steam client can show crash dialogs with upload option
- Configure in Steamworks Partner > Technical Tools

### 4. Known Issues Tracking

**Steam Discussion forum pinned thread template:**

```markdown
# Known Issues — [Game Name] v[X.Y.Z]

Last updated: [date]

## Critical
- [ ] [Issue description] — workaround: [if any]

## Major
- [ ] [Issue description] — fix in progress
- [ ] [Issue description] — investigating

## Minor
- [x] [Issue description] — fixed in v[X.Y.Z+1] (pending release)

## Workarounds
- **[Issue]**: [step-by-step workaround]

---
Please report new bugs using the Bug Reports forum with the template pinned there.
Do NOT report bugs in this thread — use it as a reference only.
```

### 5. Forum Integration

**Setting up a Bug Reports sub-forum:**

1. Steamworks Partner > Community > Discussion Forums
2. Create a sub-forum named "Bug Reports"
3. Pin the bug report template as the first post
4. Pin the known issues thread
5. Set moderation: developer-monitored

**Pinned template post:**

```markdown
# How to Report a Bug

Please use this template when reporting bugs. Well-structured reports help us fix issues faster.

[Paste the bug report template from Section 1]

**Before posting:**
- Check the Known Issues thread (pinned above)
- Search existing reports — your bug may already be reported
- Include your system info (Steam > Help > System Information)
- One bug per post, please
```

### 6. Severity Classification

| Severity | Definition | Response time |
|----------|------------|---------------|
| **Critical** | Game crashes, data loss, save corruption, cannot progress | Hotfix ASAP |
| **Major** | Significant gameplay impact, broken features, frequent occurrence | Next patch |
| **Minor** | Cosmetic issues, rare edge cases, minor inconvenience | Planned fix |
| **Cosmetic** | Visual glitches, typos, UI polish | Low priority |

### 7. Internal Bug Tracking Integration

For developers using external trackers:

| Tracker | Integration approach |
|---------|---------------------|
| GitHub Issues | Link Steam forum posts, use labels for severity/platform |
| Jira | Create tickets from Steam reports, link back in forum reply |
| Trello | Board per release, cards from bug reports |
| Linear | Import from Steam, tag with App ID |

**Workflow:** Steam forum report → Developer acknowledges → Creates internal ticket → Fixes → Updates forum thread → Closes internal ticket.

## Key References

| Resource | URL |
|----------|-----|
| Steam Discussions | https://partner.steamgames.com/doc/features/community#discussions |
| Steam Error Reporting | https://partner.steamgames.com/doc/features/error_reporting |
| ISteamUtils | https://partner.steamgames.com/doc/api/ISteamUtils |

## Example Interaction

**User:** "I need to set up bug reporting for my game. Players keep submitting vague reports."

**Agent:**
1. Provides the structured bug report template
2. Explains how to create a Bug Reports sub-forum with the template pinned
3. Shows how to direct players to `steam://sysinfo` for system info
4. Creates a known issues thread template
5. Recommends severity classification for internal triage
6. Advises: "Reply to every bug report with acknowledgment. Even 'Thanks, logged.' shows players you're reading."

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Verify app | `steam.getAppDetails({ appid })` | None | Confirm game name and platforms for template customization |

Bug reporting setup requires the Steamworks Partner site — not available via MCP.

## See Also

- [Steam Community Management](../steam-community-management/SKILL.md) - forum setup and community engagement
- [Steam Playtest Setup](../steam-playtest-setup/SKILL.md) - feedback collection during playtests
- [Steam Release Checklist](../steam-release-checklist/SKILL.md) - pre-launch QA validation
