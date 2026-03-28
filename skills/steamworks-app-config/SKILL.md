---
name: steamworks-app-config
description: Manage Steamworks app configuration. Query and document depot configs, build configurations, launch options, and DLC setup. Use when working on Steamworks app admin tasks, setting up builds, or documenting deployment configs.
---

# Steamworks App Config

## Trigger

Use this skill when the user:

- Is setting up or modifying Steamworks depot configurations
- Needs help writing `app_build.vdf` or `depot_build.vdf` files
- Asks about launch options, OS-specific builds, or beta branches
- Is configuring DLC, packages, or bundles in Steamworks
- References Steamworks Partner site configuration
- Needs to document their build pipeline for Steam distribution

## Required Inputs

- **App ID** (for the game being configured)
- **Context**: what the user is trying to configure (depots, launch options, DLC, etc.)

## Workflow

### Depot Configuration

1. **Explain the depot model.** Steam distributes content via depots - each depot is a set of files for a specific platform or content type. Typical setup:
   - Depot `{appid+1}` - Windows content
   - Depot `{appid+2}` - macOS content
   - Depot `{appid+3}` - Linux content
   - Additional depots for DLC, soundtracks, dedicated servers

2. **Generate `app_build.vdf`** for the user's scenario:
   ```vdf
   "appbuild"
   {
     "appid" "{appid}"
     "desc" "{build_description}"
     "buildoutput" "..\output\"
     "contentroot" "..\content\"
     "setlive" ""
     "preview" "0"
     "local" ""
     "depots"
     {
       "{depotid}" "depot_build_{depotid}.vdf"
     }
   }
   ```

3. **Generate `depot_build_{depotid}.vdf`**:
   ```vdf
   "DepotBuildConfig"
   {
     "DepotID" "{depotid}"
     "contentroot" "..\content\"
     "FileMapping"
     {
       "LocalPath" "*"
       "DepotPath" "."
       "recursive" "1"
     }
     "FileExclusion" "*.pdb"
   }
   ```

### Launch Options

4. **Document launch option fields:**
   - `executable` - path relative to install directory
   - `type` - `default`, `server`, `editor`, `manual`, etc.
   - `oslist` - `windows`, `macos`, `linux`
   - `arguments` - command-line args
   - `description` - shown to user in launch dialog (if multiple options)

### DLC Setup

5. **DLC configuration steps:**
   - Create DLC App ID in Steamworks (under the base game)
   - Create a depot for DLC content
   - Add depot to DLC app's `app_build.vdf`
   - Configure DLC visibility, pricing, and store page separately
   - In-game, check DLC ownership via `ISteamApps::BIsDlcInstalled(dlcAppId)`

### Build Upload

6. **Instruct on using `steamcmd` for uploads:**
   ```bash
   steamcmd +login {username} +run_app_build ..\scripts\app_build.vdf +quit
   ```
   Remind the user to use Steam Guard and that first login requires interactive authentication.

## Key References

| Resource | URL |
|----------|-----|
| Steamworks Depot docs | https://partner.steamgames.com/doc/store/application/depots |
| SteamPipe build guide | https://partner.steamgames.com/doc/sdk/uploading |
| Launch option docs | https://partner.steamgames.com/doc/sdk/uploading#launch_options |
| DLC documentation | https://partner.steamgames.com/doc/store/application/dlc |

## Example Interaction

**User:** "I need to set up Steam build configs for my game. App ID is 2345678, Windows and Linux only."

**Agent:**
1. Generates `app_build.vdf` with depots `2345679` (Windows) and `2345680` (Linux)
2. Generates both `depot_build_*.vdf` files with platform-appropriate file mappings
3. Provides the `steamcmd` upload command
4. Notes: "Set `setlive` to a beta branch name for testing before pushing to default."

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured, you can fetch existing app metadata:

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Get app details | `steam.getAppDetails({ appid })` | None | Verify app name, type, platforms, and current config before generating VDF files |

This is useful for confirming the app exists and checking its current platform list before generating depot configs. Partner-level API access (depot config fetch, build management) is not available via MCP.

The VDF generation, depot configuration, launch options, DLC setup, and steamcmd documentation remain the same regardless of MCP availability.

## Common Pitfalls

1. **Using the wrong depot ID pattern** — depot IDs should follow `appid + N` convention (e.g. App 1234567 → depot 1234568 for Win, 1234569 for Mac). Random depot IDs cause confusion.
2. **Forgetting `FileMapping` exclusions in VDF** — without exclusion patterns, debug symbols (`.pdb`), editor files, and source code get uploaded to depots. Use `FileExclusion` directives.
3. **Not creating platform-specific depots** — shipping a single depot with Windows, Mac, and Linux binaries wastes bandwidth. Create separate depots and assign them by OS in the app config.
4. **Misconfiguring launch options** — each platform needs its own launch option entry with the correct `oslist`. A missing or wrong `oslist` makes the game unlaunhcable on that platform.
5. **Not testing the VDF with `steamcmd` before CI integration** — syntax errors in VDF files are hard to debug in CI logs. Validate locally first with `steamcmd +login ... +run_app_build`.

## See Also

- [Steam Achievement Designer](../steam-achievement-designer/SKILL.md) - design achievements and generate VDF configs
- [Steam Cloud Saves](../steam-cloud-saves/SKILL.md) - configure cloud save support alongside your build pipeline
