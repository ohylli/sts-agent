# Text the Spire Integration Tool Implementation Guide

This document provides a focused summary of best practices and implementation details for creating a CLI tool to interact with Text the Spire. Based on Phase 1 testing results.

## Tool Overview

A Python CLI tool that enables Claude Code to interact with Slay the Spire via the Text the Spire accessibility mod. The tool provides command execution, response verification, and game state reading capabilities.

### Core Features
1. Execute single commands in the prompt window with verification
2. Execute command sequences with individual verification
3. Read full content from any Text the Spire window
4. Combine command execution with window content reading
5. List all available Text the Spire windows
6. Capture multiple window states simultaneously
7. Configure response timeouts
8. Force cache refresh for window handles

## Implementation Requirements

### Dependencies
- **pywinauto** (preferred over win32api for better error handling)
- **pywin32** (for Windows-specific operations)
- **Python 3.x** running on Windows or WSL with Windows Python

### Key Classes and Methods

#### 1. Window Finder with Caching
```python
class TextTheSpireWindowFinder:
    def __init__(self, cache_duration=30):
        self.cache = {}
        self.cache_time = {}
        self.cache_duration = cache_duration
    
    def get_window(self, title):
        # Check cache validity (30 seconds)
        # Return cached handle or re-enumerate
        # Handle both "Prompt" and "info" titles for prompt window
```

#### 2. Command Sender with Smart Clearing
```python
def send_command(prompt_window, command):
    # Focus window
    prompt_window.set_focus()
    
    # Smart clearing sequence
    prompt_window.type_keys(' ')      # Type space
    prompt_window.type_keys('^a')     # Select all
    time.sleep(0.02)                  # Small delay
    
    # Type command and send
    prompt_window.type_keys(command)
    prompt_window.type_keys('{ENTER}')
    
    # Total latency: ~0.249s average
```

#### 3. Response Verification
```python
def verify_command(log_window, command, timeout=5.0):
    # Capture log content before sending
    before_text = extract_window_text(log_window)
    
    # Send command
    send_command(prompt_window, command)
    
    # Wait for response (typically <5ms)
    start_time = time.time()
    while time.time() - start_time < timeout:
        after_text = extract_window_text(log_window)
        if command in after_text and after_text != before_text:
            return True
        time.sleep(0.1)
    
    return False
```

#### 4. Text Extraction
```python
def extract_window_text(window):
    # Children aggregation method (25k chars/second)
    children = window.children()
    all_text = []
    for child in children:
        child_text = child.window_text()
        if child_text.strip():
            all_text.append(child_text)
    return '\n'.join(all_text).strip()
```

## CLI Interface Design

```bash
# Execute single command
python sts_tool.py --execute "choose 1" --verify

# Execute command sequence
python sts_tool.py --execute-list commands.txt --verify

# Read window content
python sts_tool.py --read-window "Map"

# Execute and read
python sts_tool.py --execute "end" --read-window "Event" --verify

# List all windows
python sts_tool.py --list-windows

# Read multiple windows
python sts_tool.py --read-windows "Map,Hand,Player"

# Force cache refresh
python sts_tool.py --refresh-cache --execute "choose 1"

# Custom timeout
python sts_tool.py --execute "wait" --timeout 10
```

## Critical Implementation Details

### Window Handle Management
- **Handles are stable during gameplay but invalidated on game restart**
- Cache handles for 30 seconds during active sessions
- Always handle window enumeration failures gracefully
- Prompt window may appear as "Prompt" or "info"

### Command Execution
- **Smart clearing eliminates Windows error sounds and input issues**
- Average input latency: 249ms (consistent across command types)
- Success rate: 91.7% average, 100% for sequences ≤10 commands
- Commands are queued by Text the Spire without dropping

### Response Detection
- **Primary verification via Log window monitoring**
- Response time: <5ms typically (2ms average)
- Valid commands: 100% generate log entries
- Invalid commands: 50% generate "Unknown command" responses
- Empty/whitespace commands handled gracefully

### Text Extraction
- **Use children aggregation for best performance**
- Each window typically has 1 Edit control with all content
- Text includes `\r\n` line separators
- Performance: ~25k characters/second

### Error Handling
- Window not found: Return None/empty, let caller decide
- Connection failures: Wrap in try/except, return status dict
- Invalid handles: Trigger re-enumeration
- Timeouts: Default 5 seconds, configurable per command

## Performance Expectations

| Operation | Typical Time | Notes |
|-----------|-------------|-------|
| Window enumeration | 0.0001s | Fresh scan |
| Cached window access | <0.00001s | 100x+ faster |
| Command input | 0.249s | Including verification |
| Response detection | 0.002s | After command processing |
| Text extraction | 0.0018s | Per window |
| Rapid commands | 4/second | Maximum reliable rate |

## Usage Example

```python
# Initialize tool
tool = TextTheSpireTool()

# Execute command with verification
result = tool.execute_command("choose 1", verify=True)
print(f"Success: {result['success']}")
print(f"Response time: {result['response_time']}s")

# Read game state
map_content = tool.read_window("Map")
hand_content = tool.read_window("Hand")

# Execute and read result
result = tool.execute_and_read("end", "Event")
print(f"Command executed: {result['command_success']}")
print(f"Event text: {result['window_content']}")
```

## Testing Recommendations

1. Test window enumeration after game restart
2. Verify command sequences of varying lengths
3. Test invalid/empty commands for graceful handling
4. Measure response times under different game states
5. Test rapid command sequences (up to 4/second)
6. Verify multi-window reading performance

This implementation guide provides all necessary details to build a reliable integration tool without consulting other documentation.