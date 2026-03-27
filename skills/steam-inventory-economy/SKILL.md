---
name: steam-inventory-economy
description: Implement Steam Inventory and in-game economy. Covers ISteamInventory for item management, ISteamMicroTxn for in-game purchases, inventory schema definition, and Web API queries. Use when adding items, loot, microtransactions, or a player-facing item store to a game.
---

# Steam Inventory & Economy

## Trigger

Use this skill when the user:

- Wants to add an item/inventory system to their Steam game
- Needs to implement in-game purchases (microtransactions)
- Is defining an inventory schema (item types, bundles, recipes)
- Asks about `ISteamInventory`, `ISteamMicroTxn`, or the Steam Item Store
- Wants to set up item drops, crafting, or trading

## Required Inputs

- **App ID** - the game's Steam App ID
- **Feature** - inventory items, in-game purchases, item store, or trading

## Workflow

### Inventory Schema

Define items in the Steamworks Partner site under Community > Inventory Service > Item Definitions.

Item definition fields:
```json
{
    "appid": 480,
    "items": [
        {
            "itemdefid": 100,
            "type": "item",
            "name": "Iron Sword",
            "description": "A basic sword.",
            "icon_url": "https://example.com/iron_sword.png",
            "tradable": true,
            "marketable": false,
            "tags": { "class": "weapon", "rarity": "common" },
            "price": { "USD": 199 }
        }
    ]
}
```

Item types: `item`, `bundle`, `generator` (random drop), `playtimegenerator` (time-based drop), `tag_generator`.

### SDK: Grant and Query Items

**Get the player's inventory:**

**C++ (Steamworks SDK):**
```cpp
SteamInventory()->GetAllItems(&resultHandle);
// Poll with GetResultStatus(resultHandle) until k_EResultOK
// Then: GetResultItems(resultHandle, items, &count)
```

**Grant a promo item (defined as free in schema):**
```cpp
SteamInventoryItemDef_t itemDef = 100;
SteamInventory()->AddPromoItem(&resultHandle, itemDef);
```

**Consume an item:**
```cpp
SteamInventory()->ConsumeItem(&resultHandle, itemInstanceId, 1);
```

**Trigger a playtime-based item drop:**
```cpp
SteamInventory()->TriggerItemDrop(&resultHandle, playtimeGeneratorDefId);
```

### In-Game Purchases (ISteamMicroTxn)

For purchases processed through Steam's payment system (Steam Wallet):

1. **Initiate a transaction (server-side Web API call):**
```bash
curl.exe -X POST "https://partner.steam-api.com/ISteamMicroTxn/InitTxn/v3/" -d "key={PUBLISHER_KEY}&orderid={unique_order_id}&steamid={buyer_steamid}&appid={appid}&itemcount=1&language=en&currency=USD&itemid[0]=1001&qty[0]=1&amount[0]=199&description[0]=Iron+Sword"
```

2. **Steam shows the purchase dialog to the user.**

3. **Finalize the transaction (after user approves):**
```bash
curl.exe -X POST "https://partner.steam-api.com/ISteamMicroTxn/FinalizeTxn/v2/" -d "key={PUBLISHER_KEY}&orderid={unique_order_id}&appid={appid}"
```

4. **Verify in-game** - listen for `MicroTxnAuthorizationResponse_t` callback.

### Item Store

The Steam Item Store is a built-in storefront hosted on the Steam Community:
- Items with `price` in their schema appear automatically
- Users purchase with Steam Wallet
- No custom UI needed - Steam handles the store page

### Web API Queries

**Get a player's inventory:**
```bash
curl.exe "https://api.steampowered.com/IInventoryService/GetInventory/v1/?key={STEAM_API_KEY}&appid={appid}&steamid={steamid}"
```

**Get item definitions:**
```bash
curl.exe "https://api.steampowered.com/IInventoryService/GetItemDefs/v1/?key={STEAM_API_KEY}&appid={appid}"
```

## Key References

| Resource | URL |
|----------|-----|
| Steam Inventory Service | https://partner.steamgames.com/doc/features/inventory |
| Inventory schema | https://partner.steamgames.com/doc/features/inventory/schema |
| ISteamInventory API | https://partner.steamgames.com/doc/api/ISteamInventory |
| Microtransactions | https://partner.steamgames.com/doc/features/microtransactions |
| ISteamMicroTxn Web API | https://partner.steamgames.com/doc/webapi/ISteamMicroTxn |
| Item Store | https://partner.steamgames.com/doc/features/inventory/itemstore |

## Example Interaction

**User:** "I want to add cosmetic hat drops to my game. Players earn a random hat every 2 hours of playtime, and they can buy specific hats from a store."

**Agent:**
1. Defines hat items in the inventory schema with `type: item` and prices
2. Creates a `playtimegenerator` item with a 2-hour interval and a bundle of possible hats
3. Shows `TriggerItemDrop` SDK call
4. Explains the Steam Item Store setup (items with prices auto-appear)
5. Notes: "Playtime generators require the game to call `TriggerItemDrop` periodically. Steam tracks the cooldown server-side."

## MCP Integration (Future)

A Steam MCP server could expose `steam.getInventory({ appid, steamid })` and `steam.getItemDefs({ appid })` via the IInventoryService Web API. The SDK integration and microtransaction flows remain documentation-only.
