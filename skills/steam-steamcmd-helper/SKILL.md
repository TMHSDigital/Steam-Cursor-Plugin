---
name: steam-steamcmd-helper
description: Comprehensive steamcmd scripting reference. Common commands, batch/shell scripts, Docker containerized builds, Steam Guard handling, and troubleshooting. Use when writing steamcmd scripts, automating builds, or debugging steamcmd issues.
---

# Steam SteamCMD Helper

## Trigger

Use this skill when the user:

- Needs help with `steamcmd` commands or scripting
- Wants to automate Steam builds or dedicated server management
- Asks about `steamcmd` login, Steam Guard, or authentication
- Needs Docker-based steamcmd setups
- Is troubleshooting steamcmd errors
- Wants to download or update dedicated game servers

## Required Inputs

- **Task** - what the user wants steamcmd to do (build upload, server install, app info, etc.)
- **Platform** (optional) - Windows, Linux, macOS

## Workflow

### 1. Installation

**Linux:**
```bash
sudo apt-get update
sudo apt-get install -y lib32gcc-s1
mkdir -p ~/steamcmd
curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar xz -C ~/steamcmd
```

**Windows:**
```powershell
Invoke-WebRequest -Uri "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip" -OutFile steamcmd.zip
Expand-Archive steamcmd.zip -DestinationPath C:\steamcmd
```

**macOS:**
```bash
mkdir -p ~/steamcmd
curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_osx.tar.gz" | tar xz -C ~/steamcmd
```

**Docker:**
```bash
docker pull cm2network/steamcmd:latest
docker run -it cm2network/steamcmd:latest bash
```

### 2. Core Commands Reference

| Command | Description |
|---------|-------------|
| `login <user> [password]` | Authenticate (interactive Steam Guard on first use) |
| `login anonymous` | Anonymous login (for public dedicated servers) |
| `app_update <appid>` | Install or update an app |
| `app_update <appid> -beta <branch>` | Install a specific beta branch |
| `app_update <appid> validate` | Verify and repair installation |
| `run_app_build <vdf_path>` | Upload a build via SteamPipe |
| `app_info_print <appid>` | Print app metadata |
| `app_status <appid>` | Check install status |
| `workshop_build_item <vdf_path>` | Upload a Workshop item |
| `force_install_dir <path>` | Set install directory (must precede `app_update`) |
| `quit` | Exit steamcmd |

### 3. Common Scripting Patterns

**Upload a build:**
```bash
steamcmd +login "$STEAM_USER" \
         +run_app_build "$PWD/app_build.vdf" \
         +quit
```

**Install a dedicated server:**
```bash
steamcmd +login anonymous \
         +force_install_dir /home/steam/cs2 \
         +app_update 730 validate \
         +quit
```

**Update a dedicated server on a beta branch:**
```bash
steamcmd +login anonymous \
         +force_install_dir /home/steam/server \
         +app_update 232250 -beta prerelease validate \
         +quit
```

**Upload a Workshop item:**
```bash
steamcmd +login "$STEAM_USER" \
         +workshop_build_item "$PWD/workshop_item.vdf" \
         +quit
```

**Batch script (Windows `.bat`):**
```bat
@echo off
C:\steamcmd\steamcmd.exe ^
  +login %STEAM_USER% ^
  +run_app_build "%CD%\app_build.vdf" ^
  +quit
```

**PowerShell script:**
```powershell
& C:\steamcmd\steamcmd.exe `
  +login $env:STEAM_USER `
  +run_app_build "$PSScriptRoot\app_build.vdf" `
  +quit
```

### 4. Steam Guard / Authentication

**First-time login (interactive):**
```bash
steamcmd +login myaccount mypassword +quit
# Prompts for Steam Guard code via email or authenticator
```

After successful login, steamcmd caches credentials in:

| Platform | Location |
|----------|----------|
| Linux | `~/.steam/config/config.vdf` |
| Windows | `C:\Users\<user>\AppData\Local\Steam\config\config.vdf` |
| macOS | `~/Library/Application Support/Steam/config/config.vdf` |

**For CI/CD**, extract `config.vdf` after interactive login, base64-encode it, and store as a CI secret:

```bash
base64 ~/.steam/config/config.vdf > config_vdf_b64.txt
```

Restore in CI:
```bash
echo "$STEAM_CONFIG_VDF" | base64 -d > ~/Steam/config/config.vdf
```

### 5. Docker Containerized Builds

**Basic build upload container:**
```dockerfile
FROM cm2network/steamcmd:latest

COPY steamworks/ /app/steamworks/
COPY build/ /app/build/

CMD ["bash", "-c", \
  "steamcmd +login $STEAM_USER \
            +run_app_build /app/steamworks/app_build.vdf \
            +quit"]
```

**Dedicated server container:**
```dockerfile
FROM cm2network/steamcmd:latest

RUN steamcmd +login anonymous \
             +force_install_dir /home/steam/server \
             +app_update 232250 validate \
             +quit

EXPOSE 27015/udp 27015/tcp 27020/udp

CMD ["/home/steam/server/srcds_run", "-game", "csgo", "-console"]
```

**Docker Compose for dedicated server:**
```yaml
services:
  gameserver:
    image: cm2network/steamcmd:latest
    volumes:
      - server-data:/home/steam/server
    ports:
      - "27015:27015/udp"
      - "27015:27015/tcp"
    command: >
      bash -c "steamcmd +login anonymous
                        +force_install_dir /home/steam/server
                        +app_update 232250 validate
                        +quit
               && /home/steam/server/srcds_run -game csgo -console"
volumes:
  server-data:
```

### 6. Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Login Failure: Invalid Password` | Wrong password or expired Steam Guard | Re-run interactive login, enter new Steam Guard code |
| `Login Failure: Rate Limit Exceeded` | Too many failed attempts | Wait 30-60 minutes, then retry |
| `ERROR! Failed to install (No subscription)` | Account doesn't own the app | Use `anonymous` for free servers, or verify app ownership |
| `ERROR! Not enough disk space` | Insufficient disk | Free space or change `force_install_dir` |
| `Update state (0x3)` stuck | Download stuck or corrupt | Delete `downloading/` folder, run with `validate` |
| `config.vdf` not found in CI | Credentials not restored | Check base64 decode step, verify file path |
| `ContentServerUnreachable` | Network/firewall issue | Check outbound ports 27015-27050 (UDP/TCP) |

### 7. Useful `app_info_print` Queries

To inspect app metadata without the store API:

```bash
steamcmd +login anonymous +app_info_print 730 +quit
```

This outputs depot IDs, branch info, launch configs, and install scripts — useful for verifying build configuration.

## Key References

| Resource | URL |
|----------|-----|
| SteamCMD Documentation | https://developer.valvesoftware.com/wiki/SteamCMD |
| SteamPipe Build Guide | https://partner.steamgames.com/doc/sdk/uploading |
| Dedicated Servers List | https://developer.valvesoftware.com/wiki/Dedicated_Servers_List |
| Docker steamcmd Image | https://hub.docker.com/r/cm2network/steamcmd |

## Example Interaction

**User:** "I need a script to download and update a CS2 dedicated server on Linux."

**Agent:**
1. Provides installation commands for steamcmd on Linux
2. Generates a shell script:
   ```bash
   #!/bin/bash
   ~/steamcmd/steamcmd.sh \
     +login anonymous \
     +force_install_dir /home/steam/cs2-server \
     +app_update 730 validate \
     +quit
   ```
3. Notes: "CS2 dedicated server uses App ID 730 and supports anonymous login. Add `validate` to verify file integrity after updates."
4. Optionally provides a systemd service file for auto-start

## MCP Usage

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Verify app | `steam.getAppDetails({ appid })` | None | Confirm app exists before building scripts |
| Check Workshop item | `steam.getWorkshopItem({ publishedfileid })` | None | Verify Workshop item details before upload scripts |

Steamcmd operations are local/CLI — MCP is only used for pre-validation.

## Common Pitfalls

1. **Running steamcmd without `+quit`** — the process hangs indefinitely waiting for input. Always end command chains with `+quit`.
2. **Using `+login anonymous` for apps that require ownership** — anonymous login only works for dedicated server downloads and free apps. Game depots require an authenticated account.
3. **Not escaping paths with spaces on Windows** — steamcmd requires double quotes around paths containing spaces. Unquoted paths silently fail.
4. **Forgetting `+force_install_dir` before `+app_update`** — without setting the install directory, steamcmd uses its default location, which may not be where you expect.
5. **Running steamcmd from a directory without write permissions** — steamcmd needs to create cache files. Running from `Program Files` or other protected directories fails silently on Windows.

## See Also

- [Steamworks App Config](../steamworks-app-config/SKILL.md) - generate VDF build and depot configs
- [Steam Build Automation](../steam-build-automation/SKILL.md) - CI/CD pipelines using steamcmd
- [Steam Workshop Helper](../steam-workshop-helper/SKILL.md) - Workshop item management
