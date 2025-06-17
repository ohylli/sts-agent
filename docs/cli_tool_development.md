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

### 2. File Structure

**Decision**: Modular structure with clear separation of concerns.

```
src/
├── sts_tool.py          # Main CLI entry point
├── core/                # Core functionality modules
│   └── stubs.py        # Stub implementations (to be replaced)
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

Current stubs:
- `list_windows()` - Returns mock window list
- `execute_command()` - Simulates command execution
- `execute_command_sequence()` - Handles multiple commands
- `read_window()` - Returns mock window content
- `read_multiple_windows()` - Reads multiple windows
- `execute_and_read()` - Combined operation

## Implementation Plan

### Phase 1: CLI Shell (COMPLETED)
1. ✅ Create directory structure
2. ✅ Implement full CLI with argparse
3. ✅ Create all stub functions
4. ✅ Add type definitions
5. ✅ Test all CLI combinations

### Phase 2: Core Implementation (PENDING)
Replace stubs with real implementations in this order:

1. **Window Finder Module** (`core/window_finder.py`)
   - Port window enumeration from `scripts/reliable_window_finder.py`
   - Implement window caching for performance
   - Add robust error handling

2. **Text Extractor Module** (`core/text_extractor.py`)
   - Use pywinauto for text extraction
   - Handle empty windows and errors
   - Optimize for performance (target: 25k chars/sec)

3. **Command Executor Module** (`core/command_executor.py`)
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
- Stub implementations providing realistic mock data
- Type safety with TypedDict definitions
- Constants based on actual testing metrics
- Error handling for common cases
- JSON output support
- Documentation and help text

### In Progress 🔄
- Ready to begin replacing stubs with real implementations
- Next step: Implement window_finder.py

### Pending ⏳
- Real window detection and enumeration
- Actual text extraction from game windows
- Command execution with smart clearing
- Response verification
- Integration testing with live game

## Usage Examples

```bash
# List all available windows
python.exe sts_tool.py --list-windows

# Execute a command with verification
python.exe sts_tool.py --execute "choose 1" --verify

# Read a specific window
python.exe sts_tool.py --read-window "Map"

# Execute command and read result
python.exe sts_tool.py --execute "end" --read-window "Event" --verify

# Batch execution from file
python.exe sts_tool.py --execute-list commands.txt --verify

# JSON output for programmatic use
python.exe sts_tool.py --read-windows "Player,Hand,Monster" --json
```

## Testing Strategy

1. **Manual Testing** (current phase)
   - Test all CLI commands with stubs
   - Verify error handling
   - Check output formatting

2. **Integration Testing** (next phase)
   - Test with Text the Spire running
   - Verify window detection
   - Test command execution reliability
   - Measure performance metrics

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

1. Create `core/window_finder.py` by porting code from `scripts/reliable_window_finder.py`
2. Replace `list_windows()` stub with real implementation
3. Test window enumeration with live game
4. Continue replacing stubs incrementally
5. Add comprehensive error handling and logging