# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Steam Developer Tools** is a Cursor IDE plugin (v0.1.0) that integrates Steam and Steamworks APIs for game developers. It provides AI-assisted workflows for querying Steam store data, managing Steamworks configurations, looking up API docs, fetching player statistics, integrating Workshop UGC, and designing achievements.

This is a **static, documentation-only plugin** — no build system, no npm, no compiled code. All plugin logic is expressed in Markdown skill files and MDC rule files.

## Plugin Architecture

```
.cursor-plugin/plugin.json   — Plugin manifest (name, version, skills/rules directory pointers)
skills/<skill-name>/SKILL.md — AI workflow definitions (one per skill)
rules/<rule-name>.mdc        — Code quality and security rules (applied by Cursor AI)
```

### Skills (6 total)

Each `SKILL.md` uses YAML frontmatter followed by markdown sections: **Trigger**, **Required Inputs**, **Workflow**, and **Example**.

| Skill | Purpose |
|-------|---------|
| `steam-store-lookup` | Look up games/apps by name or App ID via Steam Store API |
| `steamworks-app-config` | Generate depot VDF configs, build pipelines, DLC setup |
| `steam-api-reference` | Search and present Steam Web API / Steamworks SDK docs |
| `steam-player-stats` | Query player counts, achievement rates, leaderboards, libraries |
| `steam-workshop-helper` | Look up Workshop items and document UGC integration patterns |
| `steam-achievement-designer` | Design achievements, generate VDF/JSON configs, provide unlock code |

### Rules (2 total)

| Rule | Scope | Purpose |
|------|-------|---------|
| `steam-appid-validation.mdc` | `steam_appid.txt`, `*.vdf`, steamcmd configs | Enforces App ID consistency; warns if `480` (SpaceWar test) is used in production |
| `steamworks-secrets.mdc` | Global (all files) | Flags Steam API keys (32-char hex), ssfn files, publisher credentials, DRM keys |

## Development Workflow

No build step required. Changes to `skills/` and `rules/` are picked up by Cursor automatically.

**Local testing — symlink the plugin directory:**

Windows (PowerShell as Admin):
```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.cursor\plugins\local\steam-cursor-plugin" -Target (Get-Location)
```

Unix/macOS (bash):
```bash
ln -s "$(pwd)" ~/.cursor/plugins/local/steam-cursor-plugin
```

## Key Conventions

- **Skill API names:** `ACH_` prefix, uppercase with underscores (e.g. `ACH_BEAT_FINAL_BOSS`). Stable after release.
- **Depot ID pattern:** `appid + N` (e.g., App ID `2345678` → depots `2345679` (Win), `2345680` (macOS), `2345681` (Linux))
- **Steam API key:** Never hardcode. Use the `STEAM_API_KEY` environment variable or a `.env` file (already in `.gitignore`).
- **App ID `480`** (SpaceWar) is the Steam SDK test app — the `steam-appid-validation` rule warns if it appears in production contexts.
- **Secrets rule** flags: 32-char hex strings near "steam"/"api", `*.ssfn` files, `config.vdf`, steamcmd login lines, CEG/DRM keys.

## Steam API Quick Reference

| Endpoint | Auth |
|----------|------|
| `ISteamApps/GetAppList/v2/` | None |
| `store.steampowered.com/api/appdetails?appids={id}` | None |
| `ISteamUserStats/GetNumberOfCurrentPlayers/v1/` | None |
| `ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/` | None |
| `ISteamUserStats/GetPlayerAchievements/v1/` | API key |
| `IPlayerService/GetOwnedGames/v1/` | API key |
| `ISteamUser/ResolveVanityURL/v1/` | API key |
| Publisher/partner endpoints | API key + IP allowlist |

Regional pricing: append `&cc={country}&l={language}` to store API calls.
