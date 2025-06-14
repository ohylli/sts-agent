# Slay the Spire Tool Suite Development Plan

## Executive Summary

This document outlines the development of a Python tool suite that enables Claude Code to play Slay the Spire through the Text the Spire mod. The focus is on creating clean, reliable tools that Claude can invoke to read game state from text windows and send commands to the game. Claude Code will handle all strategic decision-making using its reasoning capabilities.

## 1. Overview and Key Concepts

### 1.1 What This Project Provides
This project creates a Python toolkit that acts as Claude Code's "hands and eyes" for playing Slay the Spire. Instead of building an autonomous agent, we're building tools that Claude can call to:
- See what's happening in the game (read windows)
- Take actions (send commands)
- Understand game mechanics (analyze cards, simulate plays)

### 1.2 How Claude Will Use These Tools

**Example: Claude Playing a Combat Turn**
```python
# Claude calls tool to see the game state
state = read_game_state()
# Returns: {'mode': 'combat', 'player': {'hp': 45, 'energy': 3}, ...}

# Claude calls tool to understand the combat situation
combat = parse_combat_state(state['raw_windows']['combat'])
# Returns: {'enemies': [{'name': 'Cultist', 'hp': 48, 'intent': 'attack'}], ...}

# Claude decides to play a Strike card at enemy 0
result = play_card(card_index=0, target_index=0)
# Returns: {'success': True, 'damage_dealt': 6, ...}
```

Claude handles all the strategy and decision-making. The tools just provide the interface.

## 2. Core Principles and Architecture

### 2.1 Tool-Based Design Philosophy
- Each tool should have a single, clear purpose
- Tools return structured data that Claude can easily interpret
- Error handling should be robust but transparent to Claude
- Tools should be stateless where possible (Claude maintains context)
- Focus on reliability over optimization

### 2.2 Tool Categories
1. **Game State Reading Tools**: Extract information from Text the Spire windows
2. **Command Tools**: Send actions to the game
3. **Helper Tools**: Parse complex game elements and provide analysis
4. **State Management Tools**: Track game progression and history

## 3. Window Detection and Text Extraction Tools

### 3.1 Window Discovery Tool
**Purpose**: Find all Text the Spire windows currently open

**Tool Interface**:
```python
def find_game_windows() -> List[Dict[str, Any]]:
    """
    Discovers all Text the Spire related windows.
    
    Returns:
        List of window info dictionaries containing:
        - 'handle': Window handle for future operations
        - 'title': Full window title
        - 'type': Window type (e.g., 'player_info', 'combat', 'map', 'prompt')
        - 'visible': Whether window is currently visible
    """
```

**Implementation Considerations**:
- Use pywinauto or win32gui for Windows
- Cache window handles for performance
- Auto-detect window types based on title patterns
- Handle cases where windows are minimized or hidden

### 3.2 Window Text Reading Tool
**Purpose**: Extract text content from a specific game window

**Tool Interface**:
```python
def read_window_text(window_handle: int) -> Dict[str, Any]:
    """
    Reads the current text content from a game window.
    
    Args:
        window_handle: Handle from find_game_windows()
        
    Returns:
        Dictionary containing:
        - 'text': Raw text content
        - 'lines': Text split into lines
        - 'timestamp': When the text was read
        - 'error': Error message if reading failed
    """
```

**Implementation Considerations**:
- Try multiple methods (UI Automation, Windows API, OCR)
- Clean and normalize text (remove extra whitespace)
- Handle encoding issues
- Return empty result rather than crashing on errors

### 3.3 Game State Reading Tool
**Purpose**: Read all game windows and return structured game state

**Tool Interface**:
```python
def read_game_state() -> Dict[str, Any]:
    """
    Reads all available game windows and returns current game state.
    
    Returns:
        Dictionary containing:
        - 'mode': Current game mode ('combat', 'map', 'event', 'shop', etc.)
        - 'player': Player stats (hp, energy, gold, etc.)
        - 'combat': Combat-specific info (enemies, hand, etc.) if in combat
        - 'choices': Available choices/actions
        - 'raw_windows': Raw text from each window type
        - 'errors': List of any windows that couldn't be read
    """
```

**Implementation Considerations**:
- Automatically detect current game mode
- Parse different window types appropriately
- Provide both structured and raw data
- Handle missing or unreadable windows gracefully

### 3.4 Screenshot Capture Tool
**Purpose**: Capture screenshots of game windows for Claude to visually analyze

**Tool Interface**:
```python
def capture_game_screenshot(window_type: str = 'all') -> Dict[str, Any]:
    """
    Captures screenshot(s) of game windows.
    
    Args:
        window_type: 'all', 'combat', 'map', or specific window name
        
    Returns:
        Dictionary containing:
        - 'images': Dict mapping window names to image file paths
        - 'success': Whether capture was successful
        - 'error': Error message if failed
    """
```

**Implementation Considerations**:
- Save images to temporary directory
- Include window borders for context
- Handle overlapping windows
- Return file paths Claude can read with its file reading capability

## 4. Command Execution Tools

### 4.1 Send Game Command Tool
**Purpose**: Send a command to the game's prompt window

**Tool Interface**:
```python
def send_game_command(command: str) -> Dict[str, Any]:
    """
    Sends a command to the Text the Spire prompt window.
    
    Args:
        command: The command to send (e.g., 'play 0', 'end', 'choose 1')
        
    Returns:
        Dictionary containing:
        - 'success': Whether command was sent successfully
        - 'method': Method used (direct, keyboard, clipboard)
        - 'confirmation': Any confirmation from the game
        - 'error': Error message if failed
    """
```

**Implementation Considerations**:
- Try multiple input methods in order of reliability
- Verify prompt window is active and ready
- Add small delay after sending for game to process
- Validate command format before sending

### 4.2 Play Card Tool
**Purpose**: Simplified tool for playing cards in combat

**Tool Interface**:
```python
def play_card(card_index: int, target_index: Optional[int] = None) -> Dict[str, Any]:
    """
    Plays a card from hand during combat.
    
    Args:
        card_index: Index of card in hand (0-based)
        target_index: Enemy index for targeted cards (0-based)
        
    Returns:
        Dictionary containing:
        - 'success': Whether card was played
        - 'energy_used': Energy cost of the card
        - 'new_state': Updated combat state after playing
        - 'error': Error message if failed
    """
```

**Implementation Considerations**:
- Build appropriate command based on targeting
- Verify we're in combat mode first
- Check energy availability
- Wait for animations and state update

## 5. Game State Analysis Tools

### 5.1 Parse Combat State Tool
**Purpose**: Parse combat window text into structured data

**Tool Interface**:
```python
def parse_combat_state(combat_text: str) -> Dict[str, Any]:
    """
    Parses combat window text into structured combat information.
    
    Args:
        combat_text: Raw text from combat window
        
    Returns:
        Dictionary containing:
        - 'enemies': List of enemy stats and intents
        - 'player': Player combat stats (hp, block, buffs/debuffs)
        - 'hand': List of playable cards with costs
        - 'energy': Current/max energy
        - 'draw_pile_count': Number of cards in draw pile
        - 'discard_pile_count': Number of cards in discard pile
        - 'turn': Current turn number
    """
```

**Implementation Considerations**:
- Use regex patterns for reliable parsing
- Handle variable enemy counts
- Parse buff/debuff stacks correctly
- Include intent interpretation

### 5.2 Parse Map State Tool
**Purpose**: Parse map window to understand navigation options

**Tool Interface**:
```python
def parse_map_state(map_text: str) -> Dict[str, Any]:
    """
    Parses map window text into structured map information.
    
    Args:
        map_text: Raw text from map window
        
    Returns:
        Dictionary containing:
        - 'current_floor': Current floor number
        - 'act': Current act (1, 2, or 3)
        - 'available_paths': List of available next nodes
        - 'node_types': Types of each available node (combat, elite, etc.)
        - 'boss_name': Name of act boss if visible
    """
```

### 5.3 Parse Event/Shop Tool
**Purpose**: Parse event and shop windows for available choices

**Tool Interface**:
```python
def parse_choices(window_text: str, window_type: str) -> Dict[str, Any]:
    """
    Parses event, shop, or choice windows.
    
    Args:
        window_text: Raw text from window
        window_type: Type of window ('event', 'shop', 'card_reward', etc.)
        
    Returns:
        Dictionary containing:
        - 'description': Event/shop description text
        - 'choices': List of available choices with costs/effects
        - 'can_skip': Whether skip/leave is available
        - 'gold_available': Player's current gold (for shops)
    """
```

## 6. Helper and Analysis Tools

### 6.1 Card Analysis Tool
**Purpose**: Provide detailed analysis of cards for Claude's decision making

**Tool Interface**:
```python
def analyze_card(card_name: str, upgraded: bool = False) -> Dict[str, Any]:
    """
    Provides detailed information about a specific card.
    
    Args:
        card_name: Name of the card
        upgraded: Whether the card is upgraded
        
    Returns:
        Dictionary containing:
        - 'cost': Energy cost
        - 'type': Attack, Skill, or Power
        - 'damage': Damage dealt (if applicable)
        - 'block': Block gained (if applicable)
        - 'effects': List of special effects
        - 'exhausts': Whether card exhausts
        - 'targets': Whether card needs a target
    """
```

### 6.2 Combat Simulation Tool
**Purpose**: Simulate outcomes of card plays for Claude's planning

**Tool Interface**:
```python
def simulate_card_play(card_index: int, target_index: Optional[int], 
                      current_state: Dict) -> Dict[str, Any]:
    """
    Simulates the outcome of playing a specific card.
    
    Args:
        card_index: Index of card to play
        target_index: Target enemy index (if applicable)
        current_state: Current combat state from parse_combat_state()
        
    Returns:
        Dictionary containing:
        - 'damage_dealt': Damage to each enemy
        - 'block_gained': Block gained by player
        - 'energy_remaining': Energy after playing
        - 'card_draws': Number of cards drawn
        - 'buffs_applied': New buffs/debuffs
        - 'valid_play': Whether the play is legal
    """
```

## 7. Tool Coordination and State Management

### 7.1 Session Manager Tool
**Purpose**: Initialize and manage a game session

**Tool Interface**:
```python
def initialize_session() -> Dict[str, Any]:
    """
    Initializes a new game session and discovers windows.
    
    Returns:
        Dictionary containing:
        - 'session_id': Unique session identifier
        - 'windows_found': List of discovered windows
        - 'game_running': Whether game is detected
        - 'initial_state': Initial game state
    """

def get_current_mode() -> str:
    """
    Quickly checks the current game mode.
    
    Returns:
        String indicating mode: 'combat', 'map', 'event', 'shop', 
        'card_reward', 'rest', 'game_over', or 'unknown'
    """
```

### 7.2 History Tracking Tool
**Purpose**: Track game progression for Claude's context

**Tool Interface**:
```python
def add_to_history(action: str, result: Dict[str, Any]) -> None:
    """
    Records an action and its result for future reference.
    
    Args:
        action: The command or action taken
        result: The outcome of the action
    """

def get_recent_history(num_entries: int = 10) -> List[Dict[str, Any]]:
    """
    Retrieves recent game history.
    
    Args:
        num_entries: Number of recent entries to return
        
    Returns:
        List of history entries with actions and results
    """
```

### 7.3 Wait for State Change Tool
**Purpose**: Wait for game animations and state updates

**Tool Interface**:
```python
def wait_for_update(expected_change: str = 'any', timeout: float = 5.0) -> Dict[str, Any]:
    """
    Waits for game state to change after an action.
    
    Args:
        expected_change: Type of change to wait for ('combat_end', 'new_turn', etc.)
        timeout: Maximum time to wait in seconds
        
    Returns:
        Dictionary containing:
        - 'changed': Whether a change was detected
        - 'new_mode': New game mode if changed
        - 'time_waited': Actual time waited
    """
```

## 8. Tool Implementation Architecture

### 8.1 Tool Registry and Interface

```python
class STSToolkit:
    """
    Main interface for Claude Code to interact with Slay the Spire.
    All tools are accessible through this single class.
    """
    
    def __init__(self):
        self.window_manager = WindowManager()
        self.command_sender = CommandSender()
        self.parser = StateParser()
        self.session_active = False
    
    # Window and State Reading Tools
    def find_game_windows(self) -> List[Dict[str, Any]]:
        """Find all Text the Spire windows"""
        return self.window_manager.discover_windows()
    
    def read_game_state(self) -> Dict[str, Any]:
        """Read current game state from all windows"""
        return self.window_manager.read_all_windows()
    
    # Command Tools
    def send_command(self, command: str) -> Dict[str, Any]:
        """Send a command to the game"""
        return self.command_sender.send(command)
    
    def play_card(self, card_index: int, target: Optional[int] = None) -> Dict[str, Any]:
        """Play a card from hand"""
        cmd = f"play {card_index}"
        if target is not None:
            cmd += f" {target}"
        return self.send_command(cmd)
    
    # Analysis Tools
    def parse_combat_state(self, combat_text: str) -> Dict[str, Any]:
        """Parse combat window text"""
        return self.parser.parse_combat(combat_text)
    
    def analyze_card(self, card_name: str, upgraded: bool = False) -> Dict[str, Any]:
        """Get detailed card information"""
        return self.parser.get_card_info(card_name, upgraded)
```

### 8.2 Error Handling Strategy

```python
def safe_tool_wrapper(func):
    """
    Decorator to ensure tools always return valid responses, even on error.
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {
                'success': True,
                'data': result,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e),
                'error_type': type(e).__name__
            }
    return wrapper
```

## 9. Implementation Challenges and Solutions

### 9.1 Window Detection Reliability

**Challenge**: Text the Spire windows may not be consistently detectable.

**Solutions**:
- Try multiple detection methods (window title, class name, process)
- Cache window handles once found
- Provide manual window selection as fallback
- Include diagnostic tool to list all windows

```python
def diagnose_windows() -> Dict[str, Any]:
    """
    Diagnostic tool to help Claude understand window detection issues.
    
    Returns:
        Dictionary containing:
        - 'all_windows': List of all visible windows
        - 'game_process': Whether Slay the Spire process is running
        - 'potential_matches': Windows that might be game windows
        - 'recommendations': Suggested fixes
    """
```

### 9.2 Text Extraction Accuracy

**Challenge**: Window text may not be readable through standard APIs.

**Solutions**:
- Implement multiple extraction methods:
  1. UI Automation API
  2. Windows Messages
  3. OCR as last resort
- Return confidence scores with extracted text
- Provide raw and cleaned versions of text
- Include screenshot tool for Claude to verify

### 9.3 Command Timing and Confirmation

**Challenge**: Commands may fail or take variable time to process.

**Solutions**:
- Implement intelligent wait times based on command type
- Check for state changes to confirm command execution
- Provide retry mechanism with backoff
- Return detailed status for each command

```python
def send_command_with_confirmation(command: str, 
                                  expected_change: str = None,
                                  max_retries: int = 3) -> Dict[str, Any]:
    """
    Sends command and waits for confirmation.
    
    Returns:
        Dictionary containing:
        - 'sent': Whether command was sent
        - 'confirmed': Whether expected change occurred
        - 'retries': Number of retries needed
        - 'final_state': State after command execution
    """
```

### 9.4 State Parsing Robustness

**Challenge**: Game text format may vary or contain unexpected content.

**Solutions**:
- Use flexible regex patterns with named groups
- Implement fuzzy matching for card and relic names
- Return partial results when full parsing fails
- Include raw text in all responses for Claude to analyze

```python
def parse_with_fallback(text: str, parser_type: str) -> Dict[str, Any]:
    """
    Attempts to parse text with multiple strategies.
    
    Returns:
        Dictionary containing:
        - 'parsed': Structured data (may be partial)
        - 'confidence': Confidence score (0-1)
        - 'raw_text': Original text for Claude's analysis
        - 'warnings': List of parsing issues encountered
    """
```

## 10. Implementation Roadmap

### Phase 1: Core Tool Infrastructure (Priority 1)
1. **Window Detection Tools**
   - `find_game_windows()` - Locate all Text the Spire windows
   - `read_window_text()` - Extract text from specific windows
   - `capture_game_screenshot()` - Capture window images

2. **Basic Command Tools**
   - `send_game_command()` - Send commands to prompt window
   - `wait_for_update()` - Wait for game state changes

### Phase 2: Game State Tools (Priority 2)
1. **State Reading Tools**
   - `read_game_state()` - Comprehensive state reading
   - `get_current_mode()` - Detect current game mode

2. **Parsing Tools**
   - `parse_combat_state()` - Parse combat information
   - `parse_map_state()` - Parse map navigation options
   - `parse_choices()` - Parse events, shops, and choices

### Phase 3: Specialized Tools (Priority 3)
1. **Combat Tools**
   - `play_card()` - Simplified card playing
   - `use_potion()` - Potion usage
   - `end_turn()` - End turn command

2. **Analysis Tools**
   - `analyze_card()` - Card information lookup
   - `simulate_card_play()` - Basic outcome prediction
   - `get_available_actions()` - List valid actions

### Phase 4: Enhancement Tools (Priority 4)
1. **Session Management**
   - `initialize_session()` - Setup game connection
   - `save_game_state()` - Save state for analysis
   - `load_game_state()` - Load previous state

2. **Diagnostic Tools**
   - `diagnose_windows()` - Debug window issues
   - `test_commands()` - Verify command sending
   - `validate_parsing()` - Check parser accuracy

## 11. Tool Design Best Practices

### 11.1 Tool Interface Guidelines
- **Single Responsibility**: Each tool does one thing well
- **Clear Return Values**: Always return structured dictionaries
- **Error Transparency**: Include error details for Claude to understand
- **Stateless Design**: Tools shouldn't maintain state between calls
- **Consistent Naming**: Use clear, descriptive function names

### 11.2 Return Value Standards
```python
# Standard return format for all tools
{
    'success': bool,          # Whether the operation succeeded
    'data': Any,             # The actual result data
    'error': str,            # Error message if failed
    'warnings': List[str],   # Non-fatal issues
    'raw_data': Any,         # Original/unprocessed data
    'metadata': Dict         # Additional context
}
```

### 11.3 Tool Documentation
Each tool should include:
- Clear purpose statement
- Parameter descriptions with types
- Return value structure
- Example usage
- Common error scenarios

### 11.4 Testing Approach
- Mock game windows for unit tests
- Record real game states for integration tests
- Test error conditions explicitly
- Verify tool isolation (no side effects)

## 12. Example Implementation Structure

```
sts-tools/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── toolkit.py          # Main STSToolkit class
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── constants.py        # Game constants
│   ├── window_tools/
│   │   ├── __init__.py
│   │   ├── window_finder.py    # Window discovery
│   │   ├── text_reader.py      # Text extraction
│   │   ├── screenshot.py       # Screenshot capture
│   │   └── ocr_fallback.py     # OCR backup method
│   ├── command_tools/
│   │   ├── __init__.py
│   │   ├── command_sender.py   # Send commands
│   │   ├── action_helpers.py   # High-level actions
│   │   └── timing.py           # Wait and sync tools
│   ├── parsing_tools/
│   │   ├── __init__.py
│   │   ├── combat_parser.py    # Combat state parsing
│   │   ├── map_parser.py       # Map parsing
│   │   ├── event_parser.py     # Event/shop parsing
│   │   └── card_database.py    # Card information
│   ├── analysis_tools/
│   │   ├── __init__.py
│   │   ├── card_analyzer.py    # Card analysis
│   │   ├── combat_simulator.py # Simple simulation
│   │   └── state_validator.py  # State validation
│   └── utils/
│       ├── __init__.py
│       ├── logging.py          # Logging utilities
│       ├── config.py           # Configuration
│       └── helpers.py          # Common utilities
├── tests/
│   ├── test_window_tools.py
│   ├── test_parsers.py
│   ├── test_commands.py
│   └── fixtures/               # Test data
├── examples/
│   ├── basic_usage.py          # Simple examples
│   └── claude_integration.py   # How Claude uses tools
├── docs/
│   ├── tool_reference.md       # Complete tool docs
│   └── troubleshooting.md      # Common issues
└── README.md
```

## 13. Example Tool Usage by Claude Code

### 13.1 Basic Combat Turn
```python
# Claude would use tools like this:
toolkit = STSToolkit()

# Read current state
state = toolkit.read_game_state()
if state['mode'] == 'combat':
    combat = toolkit.parse_combat_state(state['raw_windows']['combat'])
    
    # Analyze options
    for i, card in enumerate(combat['hand']):
        card_info = toolkit.analyze_card(card['name'])
        # Claude reasons about the card...
    
    # Play a card
    result = toolkit.play_card(0, target=1)
    
    # Wait for animation
    toolkit.wait_for_update('animation_complete')
```

### 13.2 Map Navigation
```python
# Read map state
map_state = toolkit.parse_map_state(state['raw_windows']['map'])

# Claude analyzes paths and chooses
choice = 2  # Claude's decision
result = toolkit.send_command(f'choose {choice}')
```

### 13.3 Event Handling
```python
# Parse event choices
event = toolkit.parse_choices(state['raw_windows']['event'], 'event')

# Claude reads options and decides
for i, choice in enumerate(event['choices']):
    print(f"Option {i}: {choice['text']} - Cost: {choice['cost']}")
    
# Make choice
toolkit.send_command('choose 0')
```

## 14. Conclusion

This plan outlines a tool-based approach that enables Claude Code to play Slay the Spire effectively. By focusing on reliable tools with clean interfaces, we allow Claude to leverage its reasoning capabilities while handling the technical complexity of game interaction.

Key principles:
1. **Tool Simplicity**: Each tool has a single, clear purpose
2. **Reliable Interaction**: Robust window detection and command sending
3. **Transparent Errors**: Claude can understand and work around issues
4. **Structured Data**: Parse game state into Claude-friendly formats
5. **No Hidden Logic**: All decisions are made by Claude, not the tools

The implementation should prioritize reliability and clarity over optimization, creating a toolkit that Claude can use naturally to play the game at a high level.