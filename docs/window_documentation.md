# Text the Spire Window Documentation

## Overview
This document details the window structure and properties of the Text the Spire mod based on testing with win32api enumeration.

## Text the Spire Window Categories

### 1. Game State Windows
**Class Name**: `SWT_Window0`  
**Purpose**: Display real-time game state information  
**Count**: 9 windows  

| Window Title | Size | Purpose |
|-------------|------|---------|
| Player | 300x300 | Player stats, health, energy, block |
| Monster | 400x600 | Enemy information, intent, health |
| Hand | 300x300 | Cards currently in hand |
| Deck | 300x300 | Cards in draw pile |
| Discard | 300x300 | Cards in discard pile |
| Orbs | 300x300 | Orb information (for Defect) |
| Relic | 300x300 | Active relics |
| Output | 450x525 | Game output messages |
| Log | 450x525 | Detailed game log |

### 2. Command Input Window
**Window Title**: `Prompt`  
**Class Name**: `SunAwtFrame`  
**Size**: 300x100  
**Purpose**: Text input for sending commands to the game  

### 3. Main Game Window
**Window Title**: `Modded Slay the Spire`  
**Class Name**: `LWJGL`  
**Size**: 1920x1080  
**Purpose**: Main game display (not used for text interaction)  

### 4. Mod Launcher
**Window Title**: `ModTheSpire 3.30.3`  
**Class Name**: `SunAwtFrame`  
**Size**: 160x28  
**Purpose**: Mod loading interface  

## Technical Notes

### Window Detection Reliability
- All Text the Spire mod windows use consistent class names
- Game state windows: `SWT_Window0`
- Command interface: `SunAwtFrame`
- Window titles are stable and predictable

### Window Handle Stability
**Testing Results (Section 2.2)**:
- **UNSTABLE across sessions**: All window handles change when game restarts
- **STABLE during gameplay**: Handles remain constant while game is running
- **Caching Strategy**: Safe to cache handles for 30+ seconds during active gameplay
- **Re-enumeration Required**: Must re-find windows after each game restart

**Practical Implications**:
- Cache handles during gameplay for performance
- Invalidate cache when game is restarted
- Handle enumeration is fast enough for real-time use

### Interaction Model
**Text-Only Interaction**: Only interact with Text the Spire mod windows:
- **READ**: Extract text from game state windows (SWT_Window0)
- **WRITE**: Send commands to Prompt window (SunAwtFrame)
- **NEVER**: Interact with main game window (LWJGL) or native UI

## Implementation Recommendations

### Window Finding Strategy
1. Enumerate all visible windows
2. Filter by class name and title patterns
3. Categorize into game state vs command windows
4. Re-enumerate after game restarts

**Reliable Window Finder** (scripts/reliable_window_finder.py):
- Provides caching with automatic invalidation
- Built-in error handling for missing windows
- Methods for specific window access (prompt, game state, etc.)
- Game state detection and summary functions

### Text Extraction Priority
Focus on these windows for game state:
1. **Player** - Essential for health/energy decisions
2. **Monster** - Critical for combat strategy
3. **Hand** - Required for card selection
4. **Output** - Game messages and feedback
5. **Deck/Discard** - Card tracking
6. **Orbs/Relic** - Secondary game state

### Command Input
- Use Prompt window (handle varies by session)
- Text-based command interface
- Commands sent as strings to window

## Next Phase Requirements
- Test text extraction from each window type
- Verify command sending to Prompt window
- Measure text reading reliability and latency