# Text the Spire CLI Tool API Reference

## Overview

The `sts_tool.py` provides a command-line interface for interacting with Slay the Spire through the Text the Spire accessibility mod.

## Installation

```bash
# Install dependencies
pip.exe install pywinauto pywin32

# Run from src directory
cd src
python.exe sts_tool.py --help
```

## Requirements

- Windows OS (Text the Spire is Windows-only)
- Python 3.8+
- Slay the Spire with Text the Spire mod installed and running
- pywinauto and pywin32 packages

## Commands

### Window Operations

#### `--list-windows`
List all available Text the Spire windows.

**Output**: 
- Default: Simple list of window titles (one per line)
- With `--debug`: Detailed table showing window title, type (game_state/command), and class name

```bash
# Simple output - just window names
python.exe sts_tool.py --list-windows

# Detailed output with debug info
python.exe sts_tool.py --list-windows --debug
```

#### `--read-window WINDOW[,WINDOW2,...]`
Read content from one or more windows.

**Parameters**:
- `WINDOW`: Single window title (e.g., "Player", "Map", "Hand")
- `WINDOW[,WINDOW2,...]`: Multiple window titles separated by commas

```bash
# Single window
python.exe sts_tool.py --read-window "Map"

# Multiple windows
python.exe sts_tool.py --read-window "Player,Hand,Monster"
```

### Command Execution

#### `--execute COMMAND[,COMMAND2,...]`
Execute one or more commands in the game.

**Parameters**:
- `COMMAND`: Single game command (e.g., "choose 1", "play 0", "end")
- `COMMAND[,COMMAND2,...]`: Multiple commands separated by commas

```bash
# Single command
python.exe sts_tool.py --execute "choose 1"

# Multiple commands
python.exe sts_tool.py --execute "choose 1,play 0,end"
```

### Combined Operations

#### `--execute COMMAND[,COMMAND2,...] --read-window WINDOW[,WINDOW2,...]`
Execute one or more commands and immediately read one or more windows.

```bash
# Single command with single window read
python.exe sts_tool.py --execute "end" --read-window "Event"

# Multiple commands with single window read
python.exe sts_tool.py --execute "1,2,end" --read-window "Monster"

# Single command with multiple window read
python.exe sts_tool.py --execute "end" --read-window "Player,Monster"
```

## Options

### `--verify`
Verify command execution by checking the Log window for response.

```bash
python.exe sts_tool.py --execute "choose 1" --verify
```

### `--timeout SECONDS`
Set command timeout (default: 5.0 seconds).

```bash
python.exe sts_tool.py --execute "choose 1" --verify --timeout 10
```

### `--json`
Output results in JSON format for programmatic use.

```bash
python.exe sts_tool.py --read-window "Player" --json
```

### `--debug`
Show detailed debug information (currently only affects `--list-windows`).

```bash
python.exe sts_tool.py --list-windows --debug
```

## Return Codes

- `0`: Success
- `1`: Error (command failed, window not found, etc.)

## JSON Output Schemas

### Window List
```json
[
  {
    "title": "Player",
    "type": "game_state",
    "class_name": "SWT_Window0"
  },
  {
    "title": "Hand",
    "type": "game_state",
    "class_name": "SWT_Window0"
  },
  {
    "title": "Prompt",
    "type": "command",
    "class_name": "SunAwtFrame"
  }
]
```

### Command Result
```json
{
  "success": true,
  "command": "choose 1",
  "response_time": 5.436,
  "wait_time_used": 5.0,
  "command_found_in_log": true,
  "log_response": "choose 1",
  "error": null
}
```

### Window Content
```json
{
  "window_title": "Player",
  "content": "Block: 0\nHealth: 88/88\nEnergy: 3",
  "error": null
}
```

### Multiple Windows Content
```json
{
  "windows": [
    {
      "window_title": "Player",
      "content": "Block: 0\nHealth: 88/88\nEnergy: 3",
      "error": null
    },
    {
      "window_title": "Hand",
      "content": "1:Strike 1\n2:Strike 1\n3:Defend 1\nPotions:\n0:Potion Slot",
      "error": null
    }
  ],
  "total_time": 0.006
}
```

### Execute and Read Result
```json
{
  "command_success": true,
  "command": "end",
  "response_time": 0.249,
  "window_content": "Event text here...",
  "error": null
}
```

## Example Workflows

### Basic Combat Turn
```bash
# View current game state
python.exe sts_tool.py --read-window "Player,Hand,Monster"

# Play a card
python.exe sts_tool.py --execute "1" --verify

# End turn
python.exe sts_tool.py --execute "end" --verify
```

### Navigation
```bash
# Check map
python.exe sts_tool.py --read-window "Map"

# Make choice
python.exe sts_tool.py --execute "choose 2" --verify

# Proceed
python.exe sts_tool.py --execute "proceed" --verify
```

### Batch Processing
```bash
# Execute sequence of commands
python.exe sts_tool.py --execute "choose 1,play 0,play 1,end" --verify
```

## Performance Characteristics

### Measured (Real Implementation)
- **Window enumeration**: <100ms for all windows
- **Text extraction**: 0.006s for 3 windows (exceeds 25,000 chars/second)
- **Multi-window reading**: Scales linearly, very efficient

### Measured (Real Implementation)
- **Command execution**: ~250ms input latency
- **Quick commands**: 1.0s total time (help, info, tutorial, version)
- **Slow commands**: 5.0s total time (end, choose, play, quit, continue)
- **Response verification**: <5ms via Log window
- **Reliability**: >90% command success rate with smart clearing

## Error Handling

The tool provides clear error messages for common issues:
- Window not found
- Command execution timeout
- Invalid command syntax

## Current Implementation Status

### Fully Implemented (Real) ✅
- `--list-windows`: Enumerates actual Text the Spire windows
- `--read-window`: Reads real game state from single or multiple windows (comma-separated)
- `--execute`: Sends commands to Prompt window with smart clearing
- `--verify`: Verifies command execution via Log window
- Window detection and filtering by class/title
- Text extraction using pywinauto (children aggregation method)
- Command categorization (quick vs slow commands)
- Log-based response detection
- Error handling for missing/inaccessible windows


### Current Limitations

1. **Windows Only**: Text the Spire mod is Windows-specific
2. **Single Instance**: Assumes one game instance running
3. **Sequential Commands**: No parallel command execution
4. **Log Parsing**: Basic response extraction (may need enhancement for complex responses)