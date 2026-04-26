---
name: steam-workshop-helper
description: Query and manage Steam Workshop items. Search workshop by game, get item details, and document workshop integration patterns. Use when building Workshop support into a game or querying UGC data.
standards-version: 1.9.0
---

# Steam Workshop Helper

## Trigger

Use this skill when the user:

- Wants to look up Steam Workshop items for a game
- Is integrating Steam Workshop (UGC) support into their game
- Needs details about a specific Workshop item (file ID)
- Asks about Workshop upload, update, or query APIs
- Wants to understand Workshop integration architecture
- Is a modder looking to publish or update a Workshop item
- Wants to find popular mods for a game
- Needs help with the Workshop upload/update SDK flow as a mod creator

## Required Inputs

- **App ID** - the game's Steam App ID (for browsing workshop items)
- **Published File ID** - for looking up a specific workshop item (optional)

## Workflow

> **Preferred:** If the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available, use `steam_getWorkshopItem()` and `steam_queryWorkshop()` instead of the `curl` commands below. See [MCP Usage](#mcp-usage).

### Look Up Workshop Item Details

1. Fetch details for a specific Workshop item (POST request):
   ```bash
   curl.exe -X POST "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/" -d "itemcount=1&publishedfileids[0]={file_id}"
   ```
2. Response fields in `publishedfiledetails[0]`:
   - `title`, `description`, `tags`
   - `file_size`, `file_url`
   - `creator` (Steam ID), `time_created`, `time_updated`
   - `subscriptions`, `favorited`, `views`
   - `preview_url` - thumbnail image

### Query Workshop Items for a Game

1. Use the newer `IPublishedFileService/QueryFiles` endpoint:
   ```bash
   curl.exe "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key={STEAM_API_KEY}&appid={appid}&query_type=1&numperpage=10&return_metadata=true"
   ```
   Query types: `0` = ranked by vote, `1` = ranked by date, `3` = ranked by trend, `12` = ranked by playtime.

2. Response: `response.publishedfiledetails[]` - same structure as above but in a list.

### Workshop Integration Patterns

When the user is building Workshop support into their game, provide guidance on the Steamworks SDK integration:

**Upload flow (SDK):**
1. `ISteamUGC::CreateItem(appId, k_EWorkshopFileTypeCommunity)` - creates a new item, returns `CreateItemResult_t` with `m_nPublishedFileId`
2. `ISteamUGC::StartItemUpdate(appId, publishedFileId)` - begins an update transaction
3. Set content: `SetItemTitle`, `SetItemDescription`, `SetItemContent` (folder path), `SetItemPreview` (image path), `SetItemTags`
4. `ISteamUGC::SubmitItemUpdate(handle, changeNote)` - submits asynchronously

**Download / subscribe flow (SDK):**
1. `ISteamUGC::SubscribeItem(publishedFileId)` - triggers download
2. `ISteamUGC::GetItemInstallInfo(publishedFileId, ...)` - returns local path, size, timestamp
3. Load content from the install path in your game

**Query flow (SDK):**
1. `ISteamUGC::CreateQueryAllUGCRequest(...)` - set up query with filters
2. `ISteamUGC::SendQueryUGCRequest(handle)` - execute
3. `ISteamUGC::GetQueryUGCResult(handle, index, &details)` - iterate results

## Key References

| Resource | URL |
|----------|-----|
| Workshop overview | https://partner.steamgames.com/doc/features/workshop |
| ISteamUGC API | https://partner.steamgames.com/doc/api/ISteamUGC |
| Workshop implementation guide | https://partner.steamgames.com/doc/features/workshop/implementation |
| Web API: GetPublishedFileDetails | https://partner.steamgames.com/doc/webapi/ISteamRemoteStorage#GetPublishedFileDetails |

## Example Interaction

**User:** "I want to add Workshop support to my Unity game (App ID 987654). How do I let players upload and download mods?"

**Agent:**
1. Outlines the ISteamUGC upload flow with C# Steamworks.NET equivalents
2. Provides the download/subscribe flow
3. Shows how to query installed items at game startup
4. Links to the Workshop implementation guide
5. Notes: "Use `SetItemContent` pointing to a folder - Steam will diff and upload only changed files."

**User:** "I made a custom map for Cities: Skylines. How do I upload it to the Workshop?"

**Agent:**
1. Uses `steam_searchApps({ query: "Cities: Skylines" })` to confirm the App ID
2. Walks through the ISteamUGC upload flow: CreateItem, StartItemUpdate, SetItemContent (pointing to the map folder), SetItemTitle, SetItemPreview, SetItemTags
3. Shows how to set visibility (Public/Friends/Private) and add a changelog
4. Notes: "After the first upload, use `SubmitItemUpdate` with a change note for updates. Steam tracks versions automatically."

## MCP Usage

When the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is configured, use MCP tool calls instead of shell `curl` commands:

| Step | MCP Tool | Auth | Replaces |
|------|----------|------|----------|
| Get item details | `steam_getWorkshopItem({ publishedfileid })` | None | `curl` POST to `GetPublishedFileDetails` |
| Search/browse items | `steam_queryWorkshop({ appid, search_text?, cursor?, numperpage?, query_type?, requiredtags? })` | Key | `curl` to `IPublishedFileService/QueryFiles` |

The `queryWorkshop` tool supports pagination via `cursor` (use `"*"` for the first page) and filtering by `requiredtags` (comma-separated).

The SDK integration guidance (upload, download, subscribe flows) remains documentation-only and doesn't change with MCP availability.

If the MCP server is not available, fall back to the `curl`-based workflow above.

## Common Pitfalls

1. **Not setting item visibility correctly** — newly created Workshop items default to the creator's settings. Items set to "Private" or "Friends Only" are invisible to other players.
2. **Exceeding the Workshop file size limit** — default per-item limit is 100MB (can be increased by Valve on request). Large items fail to upload silently if the limit is exceeded.
3. **Not subscribing to your own items during testing** — Workshop items must be subscribed to appear in-game. Uploading alone doesn't install the content locally.
4. **Ignoring the update changelog** — `SubmitItemUpdate` accepts a change note parameter. Leaving it empty means subscribers see "No change notes" in their update feed.
5. **Not handling `ISteamUGC` callbacks** — Workshop operations are async. Without registering and handling callbacks, you won't know if uploads succeed or fail.

## See Also

- [Steam Inventory & Economy](../steam-inventory-economy/SKILL.md) - item systems that can complement Workshop UGC
