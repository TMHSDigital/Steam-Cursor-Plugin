---
name: steam-input-controller
description: Integrate Steam Input for controller support. Covers ISteamInput for detecting controllers, configuring action sets, binding actions, and retrieving button glyphs. Use when adding controller support, configuring input for Steam Deck, or implementing action-based input systems.
standards-version: 1.6.3
---

# Steam Input / Controller Support

## Trigger

Use this skill when the user:

- Is adding controller support to their Steam game
- Needs to configure Steam Input action sets or bindings
- Wants button glyph images for prompt display
- Is targeting Steam Deck and needs input guidance
- Asks about `ISteamInput`, IGA files, or controller types

## Required Inputs

- **App ID** - the game's Steam App ID
- **Input actions** - the game actions to map (move, jump, fire, etc.)

## Workflow

### Understanding Steam Input

Steam Input provides a unified API across all controller types. Instead of polling raw buttons, you define **actions** and let players bind them to any controller.

Key concepts:
- **Action Set** - a group of actions active at a given time (e.g., "InGame", "Menu", "Vehicle")
- **Digital Action** - on/off (jump, fire, pause)
- **Analog Action** - continuous (move, camera, steering)

### In-Game Actions (IGA) File

Create a `game_actions_{appid}.vdf` file defining your input configuration:

```vdf
"In Game Actions"
{
    "actions"
    {
        "InGame"
        {
            "title" "#Set_InGame"
            "StickPadGyro"
            {
                "Move"
                {
                    "title" "#Action_Move"
                    "input_mode" "joystick_move"
                }
                "Camera"
                {
                    "title" "#Action_Camera"
                    "input_mode" "absolute_mouse"
                }
            }
            "Buttons"
            {
                "Jump"
                {
                    "title" "#Action_Jump"
                }
                "Fire"
                {
                    "title" "#Action_Fire"
                }
                "Pause"
                {
                    "title" "#Action_Pause"
                }
            }
        }
    }
    "localization"
    {
        "english"
        {
            "Set_InGame" "In-Game Controls"
            "Action_Move" "Move"
            "Action_Camera" "Camera"
            "Action_Jump" "Jump"
            "Action_Fire" "Fire"
            "Action_Pause" "Pause"
        }
    }
}
```

Upload this file in the Steamworks Partner site under Application > Steam Input.

### SDK Integration

**Initialize:**
```cpp
SteamInput()->Init(false);
SteamInput()->EnableDeviceCallbacks();
```

**Get connected controllers:**
```cpp
InputHandle_t handles[STEAM_INPUT_MAX_COUNT];
int count = SteamInput()->GetConnectedControllers(handles);
```

**Activate an action set:**
```cpp
InputActionSetHandle_t inGameSet = SteamInput()->GetActionSetHandle("InGame");
SteamInput()->ActivateActionSet(handles[0], inGameSet);
```

**Read digital action (button press):**
```cpp
InputDigitalActionHandle_t jumpAction = SteamInput()->GetDigitalActionHandle("Jump");
InputDigitalActionData_t data = SteamInput()->GetDigitalActionData(handles[0], jumpAction);
if (data.bState && data.bActive) {
    // Jump pressed
}
```

**Read analog action (stick/mouse):**
```cpp
InputAnalogActionHandle_t moveAction = SteamInput()->GetAnalogActionHandle("Move");
InputAnalogActionData_t data = SteamInput()->GetAnalogActionData(handles[0], moveAction);
float x = data.x; // -1.0 to 1.0
float y = data.y;
```

### Button Glyphs

Show the correct button icon for the player's controller type:

```cpp
InputDigitalActionHandle_t jumpAction = SteamInput()->GetDigitalActionHandle("Jump");
EInputActionOrigin origins[STEAM_INPUT_MAX_ORIGINS];
int count = SteamInput()->GetDigitalActionOrigins(handles[0], inGameSet, jumpAction, origins);
if (count > 0) {
    const char* glyphPath = SteamInput()->GetGlyphPNGForActionOrigin(origins[0],
        k_ESteamInputGlyphSize_Small, 0);
    // Load glyphPath as texture for UI prompt
}
```

This returns the correct icon (A button for Xbox, X button for PlayStation, etc.) automatically.

### Supported Controllers

| Controller | ESteamInputType |
|------------|-----------------|
| Xbox 360/One/Series | `k_ESteamInputType_XBox360Controller` / `XBoxOneController` |
| PlayStation 4/5 | `k_ESteamInputType_PS4Controller` / `PS5Controller` |
| Switch Pro | `k_ESteamInputType_SwitchProController` |
| Steam Controller | `k_ESteamInputType_SteamController` |
| Steam Deck | `k_ESteamInputType_SteamDeckController` |
| Generic | `k_ESteamInputType_GenericGamepad` |

## Key References

| Resource | URL |
|----------|-----|
| Steam Input overview | https://partner.steamgames.com/doc/features/steam_controller |
| ISteamInput API | https://partner.steamgames.com/doc/api/isteaminput |
| IGA file format | https://partner.steamgames.com/doc/features/steam_controller/iga_file |
| Getting Started guide | https://partner.steamgames.com/doc/features/steam_controller/getting_started_for_devs |

## Example Interaction

**User:** "My platformer has move, jump, dash, and pause. How do I set up Steam Input so it works on Xbox controllers and Steam Deck?"

**Agent:**
1. Creates the IGA VDF file with one "InGame" action set
2. Defines Move (analog), Jump/Dash/Pause (digital)
3. Shows SDK init + action reading code
4. Implements glyph retrieval for dynamic button prompts
5. Notes: "Steam Deck uses the same ISteamInput API. The built-in controls map to `k_ESteamInputType_SteamDeckController`. Test with the Steam Deck virtual controller in Desktop mode."

## MCP Usage

Steam Input is an in-process Steamworks SDK API (`ISteamInput`) with no Web API equivalent. This skill remains documentation-only regardless of whether the [Steam MCP server](https://github.com/TMHSDigital/steam-mcp) is available.

## Common Pitfalls

1. **Not calling `RunFrame()` every tick** — `ISteamInput` requires `RunFrame()` each frame to poll controller state. Without it, input data is stale.
2. **Hardcoding button mappings instead of using action sets** — Steam Input's power comes from action-based input (e.g. "Jump" not "Button A"). Hardcoding bypasses user rebinding and Steam Deck optimization.
3. **Forgetting to ship the IGA (In-Game Actions) file** — the controller configuration file must be uploaded to Steamworks Partner. Without it, Steam Input falls back to legacy mode.
4. **Not testing with Steam Deck controls** — the Deck's trackpads and gyro behave differently from standard controllers. Test with a Deck or use Desktop mode to simulate.
5. **Ignoring the `InputActionSetHandle` lifecycle** — action set handles must be obtained via `GetActionSetHandle()` after init. Using stale handles causes silent failures.

## See Also

- [Steam Deck Compatibility](../../rules/steam-deck-compat.mdc) - rule that flags input and compatibility issues for Steam Deck
