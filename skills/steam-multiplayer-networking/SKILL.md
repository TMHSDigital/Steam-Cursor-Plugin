---
name: steam-multiplayer-networking
description: Integrate Steam multiplayer networking into your game. Covers lobby creation, matchmaking, Steam Networking Sockets (relay), dedicated game servers, and auth tickets. Use when building multiplayer features, setting up lobbies, or implementing peer-to-peer or server-based networking with Steamworks.
---

# Steam Multiplayer Networking

## Trigger

Use this skill when the user:

- Is adding multiplayer support to a Steam game
- Needs help with lobby creation, joining, or matchmaking
- Wants to use Steam Networking Sockets (relay network)
- Is setting up dedicated game servers with Steam
- Asks about auth tickets, P2P networking, or skill-based matchmaking

## Required Inputs

- **App ID** - the game's Steam App ID
- **Multiplayer type** - lobbies, P2P, dedicated servers, or a combination

## Workflow

### Lobby-Based Matchmaking (ISteamMatchmaking)

1. **Create a lobby:**

**C++ (Steamworks SDK):**
```cpp
SteamMatchmaking()->CreateLobby(k_ELobbyTypePublic, maxPlayers);
// Handle result in OnLobbyCreated callback
```

**C# (Steamworks.NET):**
```csharp
SteamMatchmaking.CreateLobby(ELobbyType.k_ELobbyTypePublic, maxPlayers);
```

Lobby types: `Private`, `FriendsOnly`, `Public`, `Invisible`.

2. **Set lobby metadata** (game mode, map, version - used for filtering):
```cpp
SteamMatchmaking()->SetLobbyData(lobbyId, "gamemode", "deathmatch");
SteamMatchmaking()->SetLobbyData(lobbyId, "map", "arena_01");
```

3. **Search for lobbies:**
```cpp
SteamMatchmaking()->AddRequestLobbyListStringFilter("gamemode", "deathmatch", k_ELobbyComparisonEqual);
SteamMatchmaking()->AddRequestLobbyListDistanceFilter(k_ELobbyDistanceFilterDefault);
SteamMatchmaking()->RequestLobbyList();
```

4. **Join a lobby:**
```cpp
SteamMatchmaking()->JoinLobby(lobbyId);
```

5. **Lobby chat and data exchange** - use `SetLobbyMemberData` and `SendLobbyChatMsg` for pre-game coordination.

### Steam Networking Sockets (Relay Network)

The modern networking API that relays traffic through Valve's network, protecting player IPs.

1. **Initialize and create a listen socket (host):**
```cpp
SteamNetworkingSockets()->CreateListenSocketP2P(0, 0, nullptr);
```

2. **Connect to a host (client):**
```cpp
SteamNetworkingIdentity identity;
identity.SetSteamID(hostSteamId);
SteamNetworkingSockets()->ConnectP2P(identity, 0, 0, nullptr);
```

3. **Send messages:**
```cpp
SteamNetworkingSockets()->SendMessageToConnection(conn, data, dataSize, k_nSteamNetworkingSend_Reliable, nullptr);
```

4. **Receive messages:**
```cpp
SteamNetworkingMessage_t* msgs[16];
int numMsgs = SteamNetworkingSockets()->ReceiveMessagesOnConnection(conn, msgs, 16);
for (int i = 0; i < numMsgs; i++) {
    // process msgs[i]->m_pData (size: msgs[i]->m_cbSize)
    msgs[i]->Release();
}
```

### Dedicated Game Servers (ISteamGameServer)

1. **Initialize the game server:**
```cpp
SteamGameServer_Init(0, gamePort, queryPort, eServerModeAuthenticationAndSecure, "1.0.0");
SteamGameServer()->SetProduct("mygame");
SteamGameServer()->SetGameDescription("My Game Server");
SteamGameServer()->LogOnAnonymous();
```

2. **Auth tickets** - validate connecting players:
```cpp
SteamGameServer()->BeginAuthSession(ticket, ticketLen, clientSteamId);
// Check EAuthSessionResponse in callback
```

3. **Server browser registration** - servers appear in Steam's server browser automatically after `LogOnAnonymous()`.

### Skill-Based Matchmaking

Steam does not provide built-in Elo/MMR. Recommended pattern:
- Store skill ratings in Steam Stats (`ISteamUserStats`)
- Use lobby metadata filters to match similar skill ranges
- Or run a backend matchmaking service that creates lobbies for matched players

## Key References

| Resource | URL |
|----------|-----|
| Multiplayer overview | https://partner.steamgames.com/doc/features/multiplayer |
| Matchmaking & Lobbies | https://partner.steamgames.com/doc/features/multiplayer/matchmaking |
| ISteamMatchmaking API | https://partner.steamgames.com/doc/api/ISteamMatchmaking |
| ISteamNetworkingSockets | https://partner.steamgames.com/doc/api/ISteamNetworkingSockets |
| ISteamGameServer | https://partner.steamgames.com/doc/api/ISteamGameServer |

## Example Interaction

**User:** "I'm building a 4-player co-op game (App ID 567890). How do I set up lobbies where the host can pick a map and others can join?"

**Agent:**
1. Shows `CreateLobby` with `k_ELobbyTypePublic` and `maxPlayers=4`
2. Sets lobby metadata: map name, game version
3. Implements lobby search with map filter
4. Shows how to transition from lobby to gameplay using Steam Networking Sockets
5. Notes: "Use `SetLobbyData` for host-controlled settings and `SetLobbyMemberData` for per-player info like character selection."

## MCP Usage

Multiplayer networking uses in-process Steamworks SDK APIs (`ISteamMatchmaking`, `ISteamNetworkingSockets`, `ISteamGameServer`) with no Web API equivalents for P2P connections or dedicated server management.

| Step | MCP Tool | Auth | Purpose |
|------|----------|------|---------|
| Lobby code examples | `steam_createLobby({ type, max_members, metadata })` | SDK guide | Get C++/C#/GDScript code for lobby creation |

The `steam_createLobby` tool returns SDK code examples and documentation, not an HTTP API call. The actual lobby creation happens in-process via the Steamworks SDK.

If the MCP server is not available, use the SDK code examples in the Workflow section above.

## Common Pitfalls

1. **Not calling `SteamAPI_RunCallbacks()` frequently enough** — networking callbacks (connection state changes, messages) are only dispatched during `RunCallbacks()`. Missing or infrequent calls cause lag and missed events.
2. **Trusting client-reported game state** — never trust client-sent positions, damage values, scores, or inventory. Validate everything server-side or with an authoritative host.
3. **Forgetting relay fallback** — Steam Networking Sockets uses Valve's relay network for NAT traversal. If you implement direct P2P only, players behind strict NATs can't connect.
4. **Not handling `k_ESteamNetworkingConnectionState_ClosedByPeer`** — players disconnect without warning. Always handle this state to clean up sessions and notify other players.
5. **Sending too much data per tick** — Steam Networking has per-connection bandwidth limits. Sending full game state every frame instead of deltas causes packet loss and disconnects.

## See Also

- [Steam Friends & Social](../steam-friends-social/SKILL.md) - game invites, rich presence, and overlay for multiplayer games
- [Steam Leaderboards](../steam-leaderboards/SKILL.md) - competitive ranking systems for multiplayer games
