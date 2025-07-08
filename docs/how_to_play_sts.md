# How to Play Slay the Spire - AI Agent Guide

This guide provides comprehensive instructions for AI agents to play Slay the Spire using the Text the Spire accessibility mod through the CLI tool.

## 1. Quick Command Reference

### Essential CLI Commands
```bash
# Read game state
python.exe src/sts_tool.py --read-window "Player,Hand,Monster"

# Play cards (by position in hand)
python.exe src/sts_tool.py --execute "2"  # Play card at position 2
python.exe src/sts_tool.py --execute "1,3"  # Play multiple cards

# End turn
python.exe src/sts_tool.py --execute "end"

# Make choices
python.exe src/sts_tool.py --execute "1"

# Navigation
python.exe src/sts_tool.py --execute "proceed"

# Combined operations
python.exe src/sts_tool.py --execute "end" --read-window "Monster"
```

### Key Windows
- **Player**: Health, Block, Energy
- **Hand**: Cards in hand, Potions
- **Monster**: Enemy info, Intent
- **Map**: Floor navigation
- **Choices**: Available actions
- **Event**: Event text and outcomes
- **Deck/Discard**: Card locations
- **Relic**: Passive items

## 2. Game Overview

### Objective
Complete 3 acts, each containing:
- 15 floors
- 1 boss at the end
- Various room types (Monster, Elite, Shop, Campfire, Treasure, Unknown)

### Core Loop
1. Navigate map choosing paths
2. Enter rooms and resolve encounters
3. Gain cards, relics, and potions
4. Defeat act boss to progress
5. Win by defeating Act 3 boss

### Room Types
- **Monster**: Normal combat
- **Elite**: Harder combat, better rewards
- **Campfire**: Rest (heal) or upgrade cards
- **Shop**: Buy/remove cards, buy relics/potions
- **Treasure**: Free chest reward
- **Unknown**: Can be any type + events

## 3. CLI Tool Usage

### Reading Game State
```bash
# Single window
python.exe src/sts_tool.py --read-window "Player"

# Multiple windows (comma-separated)
python.exe src/sts_tool.py --read-window "Player,Hand,Monster"

# List available windows
python.exe src/sts_tool.py --list-windows
```

### Executing Actions
```bash
# Single command
python.exe src/sts_tool.py --execute "1"

# Multiple commands (executed in sequence)
python.exe src/sts_tool.py --execute "1,2,end"

# Skip verification for speed
python.exe src/sts_tool.py --execute "end" --dont-verify
```

### Efficient Patterns
```bash
# Execute then read
python.exe src/sts_tool.py --execute "end" --read-window "Monster,Player"

# JSON output for parsing
python.exe src/sts_tool.py --read-window "Hand" --json
```

## 4. Combat System

### Basic Mechanics
- **Energy**: Resource for playing cards (refreshes each turn)
- **Block**: Temporary defense (expires at turn start)
- **Draw**: New hand each turn
- **Intent**: Enemy's next action visible

### Playing Cards

#### Critical: Hand Reordering
When a card is played, remaining cards shift left. This affects multi-card plays:

**Example Hand**: [1:Strike, 2:Bash, 3:Defend, 4:Strike, 5:Defend]

**Method 1 - Right to Left** (when order doesn't matter):
```bash
# To play all three Strikes at positions 1, 2, 5
python.exe src/sts_tool.py --execute "5,2,1"
```

**Method 2 - Recalculate Positions** (when order matters):
```bash
# To play Bash (pos 2) then Strike (pos 4)
# After Bash is played, Strike shifts from 4 to 3
python.exe src/sts_tool.py --execute "2,3"
```

#### Card Targeting
```bash
# No target needed (single enemy or non-targeted)
python.exe src/sts_tool.py --execute "1"

# With target (card position, enemy number)
python.exe src/sts_tool.py --execute "1 2"  # Play card 1 on enemy 2

# Multiple targeted cards
python.exe src/sts_tool.py --execute "1 1,3 2"  # Card 1 on enemy 1, card 3 on enemy 2
```

### Combat Flow
1. Read initial state: `--read-window "Player,Hand,Monster"`
2. Analyze enemy intent and your options
3. Play cards considering energy and effects
4. End turn: `--execute "end"`
5. Repeat until combat ends (Monster window returns error)

### Potions
```bash
# Use potion
python.exe src/sts_tool.py --execute "pot u 1"  # Use potion 1
python.exe src/sts_tool.py --execute "pot u 1 2"  # Use potion 1 on enemy 2

# Discard potion
python.exe src/sts_tool.py --execute "pot d 1"

# Inspect potion
python.exe src/sts_tool.py --execute "pot i 1"
```

## 5. Navigation & Exploration

### Map Commands
```bash
# View current map
python.exe src/sts_tool.py --read-window "Map"

# Inspect specific path
python.exe src/sts_tool.py --execute "map 6 4"  # Check path to floor 6, position 4

# Path analysis
python.exe src/sts_tool.py --execute "path 6 4"  # Analyze all paths to destination
```

### Movement
```bash
# Check available choices
python.exe src/sts_tool.py --read-window "Choices"

# Select path (numbered choices)
python.exe src/sts_tool.py --execute "2"

# Proceed after events
python.exe src/sts_tool.py --execute "proceed"
```

## 6. Resource Management

### Cards
- **Adding**: Choose rewards carefully - deck size matters
- **Removing**: Shops and events offer removal
- **Upgrading**: Campfires allow upgrades

### Relics
```bash
# View relics
python.exe src/sts_tool.py --read-window "Relic"

# Inspect specific relic
python.exe src/sts_tool.py --execute "relic 1"
```

### Deck Management
```bash
# View full deck (out of combat)
python.exe src/sts_tool.py --read-window "Deck"

# During combat shows draw pile
python.exe src/sts_tool.py --read-window "Deck,Discard,exhaust"
```

## 7. Decision Making Patterns

### State Verification
```bash
# Check if combat ended
python.exe src/sts_tool.py --read-window "Monster"
# Error = combat over

# Verify action success
python.exe src/sts_tool.py --read-window "Log"
```

### Choice Inspection
```bash
# Before selecting rewards/events
python.exe src/sts_tool.py --execute "c 1"  # Inspect choice 1
python.exe src/sts_tool.py --execute "c 2"  # Inspect choice 2
```

### Error Handling
- Window not found: Game state changed
- Command timeout: Use `--timeout 10` for slow commands
- Invalid command: Check syntax and game state

### Efficiency Tips
1. Batch commands when possible: `--execute "1,2,3,end"`
2. Combine operations: `--execute "end" --read-window "Monster"`
3. Use `--dont-verify` for non-critical fast actions
4. Read multiple windows at once for full state

## 8. Audio Commentary (Optional)

### Using --speak Feature
```bash
# Basic commentary
python.exe src/sts_tool.py --speak "Starting combat against two Cultists"

# Combined with actions
python.exe src/sts_tool.py --speak "Playing Strike for damage" --execute "1"

# Strategy narration
python.exe src/sts_tool.py --speak "Defending this turn to block 15 damage" --execute "3,4,end"
```

### Commentary Guidelines
- **Default Style**: Twitch streamer/YouTube Let's Player
- **Focus**: High-level strategy and decision reasoning
- **Avoid**: Technical command descriptions ("Now I'm reading the Monster window")
- **Include**: Game state analysis, strategy explanations, predictions

### Customization
Commentary style can be adjusted based on user preferences:
- Educational (explaining game mechanics)
- Entertainment (personality-driven)
- Strategic (deep analysis)
- Minimal (key decisions only)

### Efficient Usage
```bash
# Combine speak with other operations
python.exe src/sts_tool.py --speak "Checking enemy patterns" --read-window "Monster,Player"
python.exe src/sts_tool.py --speak "Time to go all-in with attacks" --execute "1,2,5,end"
```

## Key Reminders

1. **Hand positions change** when cards are played
2. **Combat ends** when Monster window returns error
3. **Batch commands** for efficiency
4. **Energy refreshes** each turn
5. **Block expires** at turn start
6. **Choices** can be inspected before selecting