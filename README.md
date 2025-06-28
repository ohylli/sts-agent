# STS Agent - Slay the Spire AI Agent Interface

A Python toolkit that enables Claude Code to play Slay the Spire through the Text the Spire accessibility mod. This project provides a command-line interface for reading game state and sending commands, allowing AI agents to interact with the game programmatically. See [this demo video](https://www.youtube.com/watch?v=W46J357-c44) of Claude Code fighting an early game enemy.

## Overview

STS Agent acts as a bridge between AI models (like Claude) and Slay the Spire, using the Text the Spire mod's text windows for game state reading and command execution. The AI makes all strategic decisions while the toolkit handles the technical interface.

## How It Works

The toolkit interacts exclusively with Text the Spire's accessibility features:

- **Text Windows**: Reads game state from multiple text windows (player stats, cards, enemies, etc.)
- **Prompt Window**: Sends commands through the mod's command interface
- **CLI Tool**: Provides a command-line interface for all operations
- **Audio Feedback**: Optional text-to-speech integration via ElevenLabs API

## Installation

1. **Prerequisites**:
   - Windows (UI automation is windows specific)
   - Python 3.x (used from WSL since claude code works only there)
   - If using a Windows virtual env you probably have to modify Scripts/activate manually so it points to the windows virtual env correctly.
   - Slay the Spire with [Text the Spire mod](https://github.com/Wensber/TextTheSpire) installed

2. **Install dependencies**:
   ```bash
   pip.exe install -r requirements.txt
   ```

3. **For audio feedback (optional)**:
   - Create a `.env` file in the project root
   - Add your ElevenLabs API key: `ELEVENLABS_API_KEY=your_key_here`
   - Add the id of the voice you want to use `VOICE_ID=your_voice_id`

## Usage

**Note**: Use with python.exe when in WSL to ensure you use the Windows python.

### Basic Commands

```bash
# List all Text the Spire windows
python.exe src/sts_tool.py --list-windows

# Read specific window
python.exe src/sts_tool.py --read-window "Player"

# Read specific windows
python.exe src/sts_tool.py --read-window "Player,Hand,Monster"

# Execute a game command. Plays first card in hand when in combat.
python.exe src/sts_tool.py --execute "1"

# Execute multiple game commands. Plays second and first cards in hand and ends turn when in combat.
python.exe src/sts_tool.py --execute "2,1,end"

# Speak text aloud with ElevenLabs.
python.exe src/sts_tool.py --speak "this is a test"

# You can combine multiple commands: speak, execute commands, and read windows (commands are always executed first)
python.exe src/sts_tool.py --speak "this is a test" --execute "2,1,end" --read-window "Player,Hand,Monster"
```

See `docs/cli_tool_api.md` for more details.

### Example Workflow

1. Start Slay the Spire with Text the Spire mod
2. Use the CLI to read game state and send commands
3. The AI agent processes the state and decides on actions

### Example Prompts

The `prompts/` directory contains example prompts for Claude Code:

- **`play_prompt.md`**: Simple early game combat with commentary
- **`video_prompt.md`**: YouTube-style demonstration with detailed explanations. Used to make [this video demo](https://www.youtube.com/watch?v=W46J357-c44)

These prompts demonstrate how to instruct Claude to play the game effectively.  It is recommended to tell claude code to read them for instructions when in plan mode. Both these assume that game is in the start of early game combat against a single enemy.

## Current Status and Limitations

This is currently a proof-of-concept. It has been tested only in simple early game combats against a single enemy.

## TODOs

- Refactor the CLI code removing the stubs module.
- Give Claude more info about how to play the game. Currently just basic info in the example prompts.

## Technical Details

For more technical documentation, see the `docs/` directory. Note not all docs are uptodate or have been human verified.