---
name: steam-build-automation
description: Automate Steam builds with SteamPipe CI/CD integration. Covers GitHub Actions, GitLab CI, and Jenkins pipelines for depot uploads, beta branch management, and Docker-containerized builds. Use when setting up automated Steam build pipelines or configuring CI/CD for Steamworks distribution.
standards-version: 1.7.0
---

# Steam Build Automation

## Trigger

Use this skill when the user:

- Wants to automate Steam builds in a CI/CD pipeline
- Needs GitHub Actions, GitLab CI, or Jenkins config for SteamPipe uploads
- Asks about automated depot uploads or build deployment
- Wants to manage beta vs default branches programmatically
- Needs to handle Steam Guard / `config.vdf` in CI
- Asks about Docker-based Steam build environments

## Required Inputs

- **App ID** - the game's Steam App ID
- **CI platform** - GitHub Actions, GitLab CI, Jenkins, or other
- **Target platforms** (optional) - Windows, macOS, Linux depot list

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use `steam_getAppDetails({ appid })` to verify the app exists and confirm its platform list before generating CI configs. See [MCP Usage](#mcp-usage).

### 1. Understand the SteamPipe Build Flow

```
Build artifacts → steamcmd login → run_app_build → depot upload → set branch live
```

The CI pipeline must:
1. Produce build artifacts (compile/package step)
2. Authenticate with `steamcmd` (cached credentials)
3. Run `app_build.vdf` to upload depots
4. Optionally set a branch live (`setlive` in VDF or via `steamcmd`)

### 2. Prerequisites

Before CI automation works, a one-time manual setup is required:

1. **Create a dedicated Steam build account** — do NOT use your main publisher account
2. **Grant the build account "Edit App Metadata" and "Publish App Changes to Steam"** permissions in Steamworks Partner site
3. **Run `steamcmd` interactively once** to complete Steam Guard and cache `config.vdf`:
   ```bash
   steamcmd +login build_account_name +quit
   ```
4. **Extract the cached `config.vdf`** from `~/.steam/config/` or `C:\Users\<user>\AppData\Local\Steam\config\`
5. **Store `config.vdf` as a CI secret** (base64-encoded)

### 3. GitHub Actions Pipeline

```yaml
name: Steam Build Upload
on:
  push:
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build game
        run: |
          # Your build step here — Unity, Unreal, Godot, custom, etc.
          echo "Build artifacts in ./build/"

      - name: Install steamcmd
        run: |
          sudo apt-get update
          sudo apt-get install -y lib32gcc-s1
          mkdir -p ~/steamcmd
          curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar xz -C ~/steamcmd

      - name: Restore Steam config
        env:
          STEAM_CONFIG_VDF: ${{ secrets.STEAM_CONFIG_VDF }}
        run: |
          mkdir -p ~/Steam/config
          echo "$STEAM_CONFIG_VDF" | base64 -d > ~/Steam/config/config.vdf

      - name: Upload to Steam
        env:
          STEAM_USERNAME: ${{ secrets.STEAM_USERNAME }}
        run: |
          ~/steamcmd/steamcmd.sh \
            +login "$STEAM_USERNAME" \
            +run_app_build "$GITHUB_WORKSPACE/steamworks/app_build.vdf" \
            +quit
```

**Required GitHub Secrets:**
| Secret | Value |
|--------|-------|
| `STEAM_USERNAME` | Dedicated build account username |
| `STEAM_CONFIG_VDF` | Base64-encoded `config.vdf` from one-time login |

### 4. GitLab CI Pipeline

```yaml
steam-upload:
  image: cm2network/steamcmd:latest
  stage: deploy
  only:
    - tags
  variables:
    STEAM_USERNAME: $STEAM_USERNAME
  before_script:
    - mkdir -p /root/Steam/config
    - echo "$STEAM_CONFIG_VDF" | base64 -d > /root/Steam/config/config.vdf
  script:
    - steamcmd +login "$STEAM_USERNAME"
               +run_app_build "$CI_PROJECT_DIR/steamworks/app_build.vdf"
               +quit
```

### 5. Docker-Based Builds

Use the `cm2network/steamcmd` Docker image for consistent environments:

```dockerfile
FROM cm2network/steamcmd:latest

COPY steamworks/ /app/steamworks/
COPY build/ /app/build/

ENTRYPOINT ["steamcmd", \
  "+login", "build_account", \
  "+run_app_build", "/app/steamworks/app_build.vdf", \
  "+quit"]
```

### 6. Branch Management

Control which Steam branch receives the build:

| Strategy | VDF `setlive` value | Use case |
|----------|-------------------|----------|
| Don't set live | `""` (empty) | Upload only, manually set live in Steamworks |
| Push to beta | `"beta"` | Automated testing branch |
| Push to default | `"default"` | Production release (use with caution) |

For staged releases:
1. CI pushes to `beta` branch on every tag
2. QA tests on `beta`
3. Manually promote `beta` → `default` in Steamworks Partner site

### 7. Secrets Management Best Practices

- **Never commit `config.vdf` or `ssfn` files** to the repository
- Use CI platform secret storage (GitHub Secrets, GitLab CI Variables, Jenkins Credentials)
- Base64-encode binary files before storing as secrets
- Rotate the build account password periodically
- The build account should have minimal permissions (no financial access)
- Consider IP allowlisting the CI runner if your Steamworks partnership supports it

## Key References

| Resource | URL |
|----------|-----|
| SteamPipe Build Guide | https://partner.steamgames.com/doc/sdk/uploading |
| Steamworks CI/CD | https://partner.steamgames.com/doc/sdk/uploading#automating_builds |
| steamcmd Documentation | https://developer.valvesoftware.com/wiki/SteamCMD |
| Docker steamcmd Image | https://hub.docker.com/r/cm2network/steamcmd |

## Example Interaction

**User:** "I want to set up GitHub Actions to automatically upload my Unity game to Steam when I push a version tag. App ID is 2345678, Windows and Linux."

**Agent:**
1. Verifies App ID `2345678` via MCP (if available)
2. Generates `app_build.vdf` with depots for Windows (`2345679`) and Linux (`2345680`)
3. Provides complete GitHub Actions workflow YAML
4. Explains one-time `steamcmd` login and `config.vdf` extraction
5. Lists required GitHub Secrets to configure
6. Recommends: "Push to `beta` branch first, test, then manually promote to `default`."

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Verify app | `steam_getAppDetails({ appid })` | None | Confirm app exists and check platform list before generating depot configs |

All other build automation steps (steamcmd, CI config, VDF generation) are offline operations not served by MCP.

## Common Pitfalls

1. **Hardcoding depot IDs in CI scripts** — depot IDs differ between platforms (Win/Mac/Linux). Use environment variables or template VDF files, not hardcoded values.
2. **Not using `+quit` in steamcmd scripts** — steamcmd hangs indefinitely without an explicit `+quit` at the end. Always terminate your command chain with it.
3. **Uploading to the default branch instead of a beta branch** — a misconfigured `setlive` in your VDF pushes directly to all users. Always upload to a staging branch first and promote manually.
4. **Forgetting to set the build as live** — uploading a build doesn't make it active. You must set the build live on a branch in Steamworks Partner or via `setlive` in the VDF.
5. **Leaking steamcmd credentials in CI logs** — use masked secrets/environment variables for `+login` credentials. Never echo them or store in plain text config files.

## See Also

- [Steamworks App Config](../steamworks-app-config/SKILL.md) - generate VDF depot and build configs
- [Steam SteamCMD Helper](../steam-steamcmd-helper/SKILL.md) - steamcmd command reference and scripting
- [Steam Release Checklist](../steam-release-checklist/SKILL.md) - pre-release validation before pushing to default
