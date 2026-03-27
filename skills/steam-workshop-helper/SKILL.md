---
name: steam-workshop-helper
description: Query and manage Steam Workshop items. Search workshop by game, get item details, and document workshop integration patterns. Use when building Workshop support into a game or querying UGC data.
---

# Steam Workshop Helper

## Trigger

Use this skill when the user:

- Wants to look up Steam Workshop items for a game
- Is integrating Steam Workshop (UGC) support into their game
- Needs details about a specific Workshop item (file ID)
- Asks about Workshop upload, update, or query APIs
- Wants to understand Workshop integration architecture

## Required Inputs

- **App ID** - the game's Steam App ID (for browsing workshop items)
- **Published File ID** - for looking up a specific workshop item (optional)

## Workflow

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

## MCP Integration (Future)

A Steam MCP server should expose `steam.getWorkshopItem({ fileId })` and `steam.queryWorkshop({ appid, queryType, count })`. The SDK integration guidance remains documentation-only and doesn't change with MCP availability.
