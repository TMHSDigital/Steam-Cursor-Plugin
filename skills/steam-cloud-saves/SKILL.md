---
name: steam-cloud-saves
description: Implement Steam Cloud save functionality. Covers ISteamRemoteStorage for manual cloud saves, Auto-Cloud configuration, conflict resolution, and quota management. Use when adding cloud save support to a game or debugging cloud sync issues.
standards-version: 1.6.3
---

# Steam Cloud Saves

## Trigger

Use this skill when the user:

- Wants to add cloud saves to their Steam game
- Needs help configuring Auto-Cloud or manual cloud storage
- Is debugging cloud sync conflicts or quota issues
- Asks about `ISteamRemoteStorage` or `steam_autocloud.vdf`
- Wants to migrate from local saves to cloud saves

## Required Inputs

- **App ID** - the game's Steam App ID
- **Save approach** - Auto-Cloud (file-based, no code) or Manual (SDK API calls)

## Workflow

### Auto-Cloud (No Code Required)

The simplest approach - Steam automatically syncs files from specified paths.

1. **Configure in Steamworks Partner site:**
   - Go to App Admin > Steam Cloud > Settings
   - Set byte/file quotas
   - Add file path roots (relative to the game's save directory)

2. **Or configure via `steam_autocloud.vdf`:**
```vdf
"AutoCloud"
{
    "0"
    {
        "Root" "WinMyDocuments"
        "SubDirectory" "MyGame/Saves"
        "FileType" "*.sav"
        "Recursive" "1"
    }
    "1"
    {
        "Root" "LinuxHome"
        "SubDirectory" ".local/share/MyGame/Saves"
        "FileType" "*.sav"
        "Recursive" "1"
    }
}
```

Root values: `WinMyDocuments`, `WinAppDataLocal`, `WinAppDataLocalLow`, `WinAppDataRoaming`, `LinuxHome`, `MacHome`, `GameInstall`.

### Manual Cloud Storage (ISteamRemoteStorage)

For full control over what gets synced and when.

1. **Write a file to the cloud:**

**C++ (Steamworks SDK):**
```cpp
const char* data = saveBuf;
int dataLen = saveBufSize;
SteamRemoteStorage()->FileWrite("save_slot1.dat", data, dataLen);
```

**C# (Steamworks.NET):**
```csharp
byte[] data = SerializeSaveData();
SteamRemoteStorage.FileWrite("save_slot1.dat", data, data.Length);
```

**GDScript (GodotSteam):**
```gdscript
var data = save_to_bytes()
Steam.fileWrite("save_slot1.dat", data, data.size())
```

2. **Read a file from the cloud:**
```cpp
int fileSize = SteamRemoteStorage()->GetFileSize("save_slot1.dat");
char* buf = new char[fileSize];
SteamRemoteStorage()->FileRead("save_slot1.dat", buf, fileSize);
```

3. **List cloud files:**
```cpp
int fileCount = SteamRemoteStorage()->GetFileCount();
for (int i = 0; i < fileCount; i++) {
    int size;
    const char* name = SteamRemoteStorage()->GetFileNameAndSize(i, &size);
}
```

4. **Delete a cloud file:**
```cpp
SteamRemoteStorage()->FileDelete("save_slot1.dat");
```

5. **Check quota:**
```cpp
uint64 total, available;
SteamRemoteStorage()->GetQuota(&total, &available);
```

### Conflict Resolution

When a cloud conflict occurs (local and remote versions differ):

1. Steam shows a sync conflict dialog to the user before launch
2. For Auto-Cloud, the user picks local or remote
3. For manual cloud, implement your own conflict UI:
   - Compare `FileRead` content with local save
   - Show timestamps: `SteamRemoteStorage()->GetFileTimestamp("save_slot1.dat")`
   - Let the user choose which version to keep

### Best Practices

- Keep save files small (quota is typically 1GB / 1000 files per user)
- Use deterministic file names (not random GUIDs)
- Call `FileWrite` at natural save points, not every frame
- Test with Steam in offline mode to verify conflict handling
- Consider using `FileWriteAsync` for large saves to avoid blocking

## Key References

| Resource | URL |
|----------|-----|
| Steam Cloud overview | https://partner.steamgames.com/doc/features/cloud |
| ISteamRemoteStorage API | https://partner.steamgames.com/doc/api/ISteamRemoteStorage |
| Auto-Cloud technical info | https://partner.steamgames.com/doc/features/cloud#steam_auto-cloud |

## Example Interaction

**User:** "I want to add cloud saves to my roguelike. I have a single `run_data.json` file in AppData/Local. What's the easiest way?"

**Agent:**
1. Recommends Auto-Cloud since it's a single file pattern
2. Provides the `steam_autocloud.vdf` config targeting `WinAppDataLocal` with `*.json`
3. Adds Linux/Mac roots for cross-platform support
4. Sets quota recommendation (100MB / 100 files is plenty for a roguelike)
5. Notes: "Auto-Cloud works without any code changes. Steam syncs the files before launch and after exit."

## MCP Usage

Steam Cloud uses the in-process Steamworks SDK API (`ISteamRemoteStorage`) for reading and writing save files. Auto-Cloud is configured through the Steamworks Partner site or VDF files. Neither has a publicly available Web API equivalent for the core operations.

This skill remains documentation-only regardless of whether the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available.

## Common Pitfalls

1. **Binary save files with endianness issues** — a save written on little-endian Windows breaks on big-endian architectures. Use text-based formats (JSON, XML) or explicit byte-order markers.
2. **Exceeding the per-user cloud quota** — the default quota is typically 100MB-1GB depending on your app's configuration. Large save files silently fail to sync. Check quota with `GetQuota()`.
3. **Case-sensitive filenames on Linux** — `SaveGame.dat` and `savegame.dat` are different files on Linux but the same on Windows. Standardize to lowercase.
4. **Not handling cloud conflicts** — when a user plays on two machines, saves can conflict. Implement conflict resolution UI or auto-merge logic.
5. **Storing absolute paths in save files** — paths like `C:\Users\...` break on other machines and platforms. Use relative paths or platform-agnostic identifiers.

## See Also

- [Steamworks App Config](../steamworks-app-config/SKILL.md) - depot and build configuration that pairs with cloud save setup
