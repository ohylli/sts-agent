# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python toolkit for enabling Claude Code to play Slay the Spire through the Text the Spire accessibility mod. The project creates tools that Claude can invoke to:

- Read game state from Text the Spire's text windows
- Send commands through Text the Spire's prompt window
- Parse and understand game mechanics

**Key Architecture Principle**: Claude Code is the player making all strategic decisions. The Python tools only provide the interface to interact with the game - they do NOT make gameplay decisions.

## Development Environment

- **Python Environment**: Uses Windows Python (python.exe/pip.exe) in WSL environment
- **Virtual Environment**: `.venv` directory (Windows-based virtual environment)
- **Target Platform**: Windows (Text the Spire mod is Windows-only)

### Installation Commands
```bash
# Install dependencies (use .exe versions for Windows compatibility in WSL)
pip.exe install pywinauto
pip.exe install pywin32
```

## Project Architecture

### Text the Spire Integration Model
The project exclusively interacts with the Text the Spire mod, NOT the game's native UI:

- **Text Windows**: Multiple windows showing game state (player stats, cards, enemies, etc.)
- **Prompt Window**: Command input interface for sending actions
- **No UI Automation**: Does not click buttons or interact with game menus

### Tool Design Pattern
All tools follow this pattern:
- **Single Purpose**: Each tool does one specific thing
- **Structured Returns**: Return dictionaries/objects that Claude can easily parse
- **Stateless**: Tools don't maintain game state (Claude does)
- **Error Transparent**: Errors are returned as data, not exceptions where possible

## Development Phases

Currently in **Phase 1**: Feasibility Testing
- **Section 2 Complete**: Window Detection and Enumeration ✅
- **Key Finding**: Window handles are unstable across sessions, stable during gameplay
- **Main Output**: `scripts/reliable_window_finder.py` - production-ready window finder with caching
- **Next**: Section 3 - Text Window Reading (pywinauto approach)

See `docs/window_documentation.md` for detailed findings and implementation guidance.

## Directory Structure

- `src/` - Core toolkit modules (window detection, text extraction, command sending, parsers)
- `tests/` - Phase 1 testing scripts (pywinauto vs win32api, reliability tests, integration tests)
- `scripts/` - Standalone utilities (window enumeration, manual testing, performance tools)
- `docs/` - Technical findings, mod documentation, API design notes, metrics

## Key Files

- `docs/plan.md`: Complete technical design and implementation plan
- `docs/tasks.md`: Phase 1 task list with specific testing objectives
- `docs/textthespire.md`: Documentation about the Text the Spire mod

## Testing Approach

Phase 1 testing priorities:
1. Window detection and text extraction from Text the Spire windows
2. Command input through Text the Spire prompt window
3. Reliability comparison between pywinauto vs win32api approaches

## Important Constraints

- **Windows-only**: Text the Spire mod only works on Windows
- **No Game UI**: Never interact with Slay the Spire's native interface
- **Text-based Only**: All interaction through Text the Spire's accessibility windows
- **Tool Provider Role**: Code provides tools for Claude to use, not autonomous gameplay