# Text the Spire CLI Tool Development Documentation

## Overview

This document details the development of the Text the Spire CLI tool (`sts_tool.py`), which provides a command-line interface for Claude Code to interact with Slay the Spire through the Text the Spire accessibility mod.

## Major Design Decisions

### 1. CLI-First Development with Stubs

**Decision**: Implement the full CLI interface with stub functions before building the actual integration.

**Rationale**:
- Enables immediate testing of the CLI interface without requiring the game to be running
- Allows early validation of command structure and user experience
- Provides clear documentation of expected behavior through stub messages
- Facilitates incremental development - stubs can be replaced one by one

**Update**: This approach has proven highly successful. We've now replaced the window listing and text reading stubs with real implementations while keeping command execution as stubs for safety during development.

### 2. File Structure

**Decision**: Modular structure with clear separation of concerns.

```
src/
├── sts_tool.py          # Main CLI entry point
├── core/                # Core functionality modules
│   ├── stubs.py        # Stub implementations (partially replaced)
│   ├── window_finder.py # Real window enumeration (implemented)
│   └── text_extractor.py # Real text extraction (implemented)
├── utils/              # Utility functions
│   └── constants.py    # Constants and configuration
└── sts_types.py        # Type definitions
```

**Rationale**:
- `sts_tool.py` focuses solely on CLI parsing and output formatting
- Core logic separated into modules for maintainability
- Type definitions in a single file for easy reference
- Constants centralized for easy configuration

### 3. TypedDict for Data Structures

**Decision**: Use TypedDict instead of dataclasses or plain dictionaries.

**Rationale**:
- Provides type safety without runtime overhead
- Compatible with JSON serialization
- Follows the implementation guide's dictionary-based approach
- Better IDE support than plain dictionaries

### 4. Combined Command Executor Module

**Decision**: Merge command sending and verification into a single `command_executor.py` module (planned).

**Rationale**:
- These operations are tightly coupled (verification must happen immediately after sending)
- Critical timing relationship (<5ms response time)
- Both need access to prompt and log windows
- Reduces inter-module dependencies

### 5. Absolute Imports

**Decision**: Use absolute imports instead of relative imports.

**Rationale**:
- Simpler when running the tool from the src directory
- Avoids import errors when the tool is run directly
- More straightforward for a CLI tool

## Code Structure

### Main Entry Point (`sts_tool.py`)

```python
# Core structure:
- Argument parsing with argparse
- Handler functions for each command type
- JSON and text output formatting
- Error handling and exit codes
```

**Key features**:
- Comprehensive help text with examples
- Validation of argument combinations
- Consistent error handling
- Support for both human-readable and JSON output

### Type Definitions (`sts_types.py`)

```python
WindowInfo: {title, type, class_name}
CommandResult: {success, command, response_time, error}
ExecuteAndReadResult: {command_success, command, response_time, window_content, error}
WindowContent: {window_title, content, error}
MultiWindowContent: {windows, total_time}
```

### Constants (`utils/constants.py`)

Defines:
- Window class names (SWT_Window0, SunAwtFrame)
- Window titles (Player, Monster, Hand, etc.)
- Timing constants based on testing (0.249s latency, 0.002s response)
- Command execution limits (4 commands/second)

### Stub Implementations (`core/stubs.py`)

Current status:
- `list_windows()` - ✅ Using real implementation from window_finder.py
- `execute_command()` - ⏳ Still stub, simulates single command execution
- `execute_command_sequence()` - ⏳ Still stub, handles multiple commands (used for comma-separated commands)
- `read_window()` - ✅ Using real implementation from text_extractor.py (handles single window)
- `read_multiple_windows()` - ✅ Using real implementation from text_extractor.py (handles multiple windows from consolidated --read-window)
- `execute_and_read()` - ⏳ Still stub, uses real read but stub execute

## Implementation Plan

### Phase 1: CLI Shell (COMPLETED)
1. ✅ Create directory structure
2. ✅ Implement full CLI with argparse
3. ✅ Create all stub functions
4. ✅ Add type definitions
5. ✅ Test all CLI combinations

### Phase 2: Core Implementation (IN PROGRESS)
Replace stubs with real implementations in this order:

1. **Window Finder Module** (`core/window_finder.py`) ✅ COMPLETED
   - Ported window enumeration from Phase 1 testing
   - Filters Text the Spire windows by class and title
   - Returns categorized window information

2. **Text Extractor Module** (`core/text_extractor.py`) ✅ COMPLETED
   - Uses pywinauto children aggregation method
   - Handles missing/inaccessible windows gracefully
   - Achieved performance: 0.006s for 3 windows (exceeds 25k chars/sec target)

3. **Command Executor Module** (`core/command_executor.py`) ⏳ PENDING
   - Implement smart clearing approach
   - Add response verification via Log window
   - Handle timing and reliability (target: >90% success rate)

### Phase 3: Enhancement (FUTURE)
- Add logging configuration
- Implement retry logic for failed commands
- Add performance metrics collection
- Create integration tests

## Current Status

### Completed ✅
- Full CLI interface with all commands working
- Window finder module with real window enumeration
- Text extractor module using pywinauto approach
- Type safety with TypedDict definitions
- Constants based on actual testing metrics
- Error handling for missing/inaccessible windows
- JSON output support
- Documentation and help text
- Successfully tested window listing and text reading with live game

### In Progress 🔄
- Replacing remaining stubs with real implementations
- Next step: Implement command_executor.py

### Pending ⏳
- Command execution with smart clearing
- Response verification via Log window
- Full integration testing with all features
- Performance optimization if needed

## Usage Examples

```bash
# List all available windows (REAL - shows actual Text the Spire windows)
python.exe sts_tool.py --list-windows

# List windows with debug info (REAL - includes window type and class)
python.exe sts_tool.py --list-windows --debug

# Execute a single command with verification (STUB - simulated execution)
python.exe sts_tool.py --execute "choose 1" --verify

# Execute multiple commands with verification (STUB - simulated execution)
python.exe sts_tool.py --execute "choose 1,play 0,end" --verify

# Read a specific window (REAL - shows actual game state)
python.exe sts_tool.py --read-window "Player"

# Read multiple windows (REAL - fast bulk reading)
python.exe sts_tool.py --read-window "Player,Hand,Monster"

# Execute command and read result (HYBRID - stub execute, real read)
python.exe sts_tool.py --execute "end" --read-window "Event" --verify

# JSON output for programmatic use (REAL data)
python.exe sts_tool.py --read-window "Player,Hand,Monster" --json
```

## Testing Strategy

1. **Manual Testing** ✅ (completed for implemented features)
   - Tested all CLI commands
   - Verified error handling for missing windows
   - Checked output formatting in both text and JSON modes

2. **Integration Testing** 🔄 (partially complete)
   - ✅ Tested window detection with live game
   - ✅ Verified text extraction from all window types
   - ✅ Measured performance (0.006s for 3 windows)
   - ⏳ Command execution reliability testing pending
   - ⏳ End-to-end workflow testing pending

3. **Automated Testing** (future)
   - Unit tests for each module
   - Integration tests with mock windows
   - Performance benchmarks

## Known Considerations

1. **Windows-specific**: Tool only works on Windows (Text the Spire limitation)
2. **Character encoding**: Avoided Unicode symbols for Windows compatibility
3. **Import structure**: Uses absolute imports, must run from src directory
4. **Performance targets**: Based on tested metrics (25k chars/sec extraction, 91.7% command success)

## Next Steps

1. ✅ ~~Create `core/window_finder.py` by porting code from `scripts/reliable_window_finder.py`~~
2. ✅ ~~Replace `list_windows()` stub with real implementation~~
3. ✅ ~~Test window enumeration with live game~~
4. ✅ ~~Create `core/text_extractor.py` using pywinauto approach~~
5. ✅ ~~Replace text reading stubs with real implementations~~
6. ⏳ Create `core/command_executor.py` with smart clearing approach
7. ⏳ Replace command execution stubs
8. ⏳ Add comprehensive logging
9. ⏳ Full integration testing with all features