# Slay the Spire Text-Based Agent Development Plan

## Executive Summary

This document outlines approaches for creating a Python program that can programmatically interact with Slay the Spire through the Text the Spire mod. The goal is to create an agent that can read game state from text windows, make intelligent decisions, and send commands to control gameplay.

## 1. Window Detection and Text Extraction Methods

### 1.1 Windows API Approach (Windows-specific)
**Description**: Use Windows API through Python libraries like `pywin32` or `ctypes` to find windows and extract text.

**Implementation**:
```python
# Using pywin32
import win32gui
import win32api
import win32con

# Find windows by title
def find_sts_windows():
    windows = []
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if "Text the Spire" in window_text or "Slay the Spire" in window_text:
                windows.append((hwnd, window_text))
    win32gui.EnumWindows(callback, windows)
    return windows

# Get window text content
def get_window_text(hwnd):
    # For standard windows with text controls
    text = win32gui.GetWindowText(hwnd)
    # May need to enumerate child controls
    return text
```

**Pros**:
- Direct access to window handles
- Fast and efficient
- Can send messages directly to windows
- No need for OCR

**Cons**:
- Windows-only solution
- May not work if text is rendered as graphics
- Requires understanding of Windows API

### 1.2 UI Automation API Approach
**Description**: Use UI Automation libraries that work across platforms to interact with application windows.

**Implementation Options**:
- **pywinauto** (Windows): Robust UI automation
- **pyautogui** (Cross-platform): Screen automation with OCR
- **uiautomation** (Windows): Python wrapper for Windows UI Automation

```python
from pywinauto import Desktop

# Find and connect to application
app = Desktop(backend="uia").window(title_re=".*Slay the Spire.*")
    
# Find text windows
text_windows = app.children(control_type="Window")
for window in text_windows:
    if "Text the Spire" in window.window_text():
        content = window.get_value() or window.window_text()
```

**Pros**:
- Higher-level API than raw Windows API
- Better support for complex UI elements
- Can handle various control types

**Cons**:
- Still mostly Windows-specific
- May have performance overhead
- Requires the application to expose UI elements properly

### 1.3 OCR-Based Approach
**Description**: Capture screenshots and use OCR to extract text from specific window regions.

**Implementation**:
```python
import pyautogui
import pytesseract
from PIL import Image
import cv2
import numpy as np

def capture_window_region(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    return screenshot

def extract_text_ocr(image):
    # Preprocess for better OCR
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    # Apply threshold or other preprocessing
    text = pytesseract.image_to_string(gray)
    return text

def find_window_coordinates():
    # Use template matching or manual configuration
    # to find window positions
    pass
```

**Pros**:
- Works regardless of how text is rendered
- Cross-platform solution
- Can handle any visual text

**Cons**:
- Slower than direct text extraction
- OCR accuracy issues possible
- Requires window positioning/detection
- CPU intensive

### 1.4 Memory Reading Approach
**Description**: Read game memory directly to extract game state (advanced approach).

**Pros**:
- Most reliable game state information
- Very fast
- Complete game state access

**Cons**:
- Complex implementation
- Game updates can break it
- May be detected as cheating
- Requires reverse engineering

### Recommended Approach: Hybrid Solution
Start with UI Automation (pywinauto) for Windows, with OCR as a fallback for text that can't be extracted directly.

## 2. Command Input Methods

### 2.1 Direct Window Messaging
**Description**: Send keyboard input directly to the prompt window.

```python
import win32gui
import win32con
import win32api

def send_command_to_window(hwnd, command):
    # Set focus to window
    win32gui.SetForegroundWindow(hwnd)
    
    # Send each character
    for char in command:
        win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(char), 0)
    
    # Send Enter key
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
```

### 2.2 Keyboard Automation
**Description**: Simulate keyboard input using automation libraries.

```python
import pyautogui
import time

def send_command_pyautogui(command):
    # Click on prompt window first
    pyautogui.click(prompt_x, prompt_y)
    time.sleep(0.1)
    
    # Type command
    pyautogui.typewrite(command)
    pyautogui.press('enter')
```

### 2.3 Clipboard-Based Input
**Description**: Copy command to clipboard and paste into prompt.

```python
import pyperclip
import pyautogui

def send_command_clipboard(command):
    pyperclip.copy(command)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
```

**Recommended**: Direct window messaging for reliability, with keyboard automation as fallback.

## 3. Game State Parsing and Representation

### 3.1 Text Parser Architecture

```python
class GameStateParser:
    def __init__(self):
        self.parsers = {
            'player': self.parse_player_info,
            'map': self.parse_map,
            'combat': self.parse_combat,
            'cards': self.parse_cards,
            'relics': self.parse_relics,
            'potions': self.parse_potions,
            'shop': self.parse_shop,
            'event': self.parse_event
        }
    
    def parse_window_text(self, window_name, text):
        parser = self.parsers.get(window_name)
        if parser:
            return parser(text)
        return None
    
    def parse_player_info(self, text):
        # Extract HP, energy, gold, etc.
        player_state = {}
        lines = text.split('\n')
        for line in lines:
            if 'HP:' in line:
                player_state['hp'] = self.extract_numbers(line)
            elif 'Energy:' in line:
                player_state['energy'] = self.extract_numbers(line)
            # ... more parsing
        return player_state
```

### 3.2 Game State Representation

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class CardType(Enum):
    ATTACK = "Attack"
    SKILL = "Skill"
    POWER = "Power"
    STATUS = "Status"
    CURSE = "Curse"

@dataclass
class Card:
    name: str
    cost: int
    card_type: CardType
    description: str
    upgraded: bool = False
    
@dataclass
class Enemy:
    name: str
    hp: int
    max_hp: int
    intent: str
    buffs: List[str]
    debuffs: List[str]

@dataclass
class Player:
    hp: int
    max_hp: int
    energy: int
    max_energy: int
    block: int
    gold: int
    buffs: List[str]
    debuffs: List[str]

@dataclass
class GameState:
    player: Player
    enemies: List[Enemy]
    hand: List[Card]
    draw_pile: List[Card]
    discard_pile: List[Card]
    exhaust_pile: List[Card]
    relics: List[str]
    potions: List[str]
    current_floor: int
    current_act: int
    game_mode: str  # "combat", "map", "shop", "event", etc.
```

### 3.3 State Update System

```python
class GameStateManager:
    def __init__(self):
        self.current_state = GameState()
        self.previous_states = []
        self.state_parser = GameStateParser()
    
    def update_from_windows(self, window_texts: Dict[str, str]):
        new_state = self.build_state(window_texts)
        self.previous_states.append(self.current_state)
        self.current_state = new_state
        return new_state
    
    def build_state(self, window_texts):
        # Parse each window and construct complete game state
        state = GameState()
        for window_name, text in window_texts.items():
            parsed = self.state_parser.parse_window_text(window_name, text)
            self.update_state_component(state, window_name, parsed)
        return state
```

## 4. Decision-Making Architecture

### 4.1 Rule-Based System
Simple but effective for basic gameplay:

```python
class RuleBasedAgent:
    def __init__(self):
        self.rules = [
            self.check_lethal,
            self.check_block_needed,
            self.check_power_cards,
            self.check_card_draw,
            self.check_energy_efficiency
        ]
    
    def decide_action(self, game_state: GameState):
        for rule in self.rules:
            action = rule(game_state)
            if action:
                return action
        return "end"  # End turn if no actions
    
    def check_lethal(self, game_state):
        # Check if we can kill all enemies
        total_damage = self.calculate_potential_damage(game_state)
        total_enemy_hp = sum(e.hp for e in game_state.enemies)
        if total_damage >= total_enemy_hp:
            return self.get_lethal_sequence(game_state)
```

### 4.2 Evaluation Function Approach
Score each possible action:

```python
class EvaluationAgent:
    def __init__(self):
        self.weights = {
            'damage_per_energy': 2.0,
            'block_per_energy': 1.5,
            'card_draw': 1.0,
            'energy_gain': 2.5,
            'debuff_value': 1.5,
            'buff_value': 2.0
        }
    
    def evaluate_action(self, game_state, action):
        score = 0
        # Calculate various metrics
        if action.is_attack():
            damage = action.calculate_damage(game_state)
            score += damage / action.cost * self.weights['damage_per_energy']
        # ... more evaluation logic
        return score
    
    def decide_action(self, game_state):
        possible_actions = self.get_possible_actions(game_state)
        best_action = max(possible_actions, key=lambda a: self.evaluate_action(game_state, a))
        return best_action
```

### 4.3 Monte Carlo Tree Search (Advanced)
For more sophisticated decision making:

```python
class MCTSAgent:
    def __init__(self):
        self.simulations_per_move = 100
        
    def decide_action(self, game_state):
        root = MCTSNode(game_state)
        
        for _ in range(self.simulations_per_move):
            node = root
            # Selection
            while node.is_fully_expanded() and not node.is_terminal():
                node = node.best_child()
            
            # Expansion
            if not node.is_terminal():
                node = node.expand()
            
            # Simulation
            reward = self.simulate(node.state)
            
            # Backpropagation
            while node is not None:
                node.update(reward)
                node = node.parent
        
        return root.best_action()
```

### 4.4 Machine Learning Approach (Future Enhancement)
Train a neural network on game states and optimal actions:

```python
class NeuralAgent:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.state_encoder = StateEncoder()
    
    def decide_action(self, game_state):
        encoded_state = self.state_encoder.encode(game_state)
        action_probs = self.model.predict(encoded_state)
        return self.decode_action(action_probs, game_state)
```

## 5. System Architecture

### 5.1 Main Control Loop

```python
class STSAgent:
    def __init__(self):
        self.window_manager = WindowManager()
        self.state_manager = GameStateManager()
        self.decision_engine = EvaluationAgent()
        self.command_sender = CommandSender()
        self.running = False
    
    def run(self):
        self.running = True
        self.initialize_windows()
        
        while self.running:
            try:
                # Read all windows
                window_texts = self.window_manager.read_all_windows()
                
                # Update game state
                game_state = self.state_manager.update_from_windows(window_texts)
                
                # Make decision
                action = self.decision_engine.decide_action(game_state)
                
                # Execute action
                if action:
                    self.command_sender.send_command(action)
                
                # Wait for game to process
                time.sleep(0.5)
                
            except Exception as e:
                self.handle_error(e)
```

### 5.2 Error Handling and Recovery

```python
class ErrorHandler:
    def __init__(self):
        self.error_count = {}
        self.recovery_strategies = {
            'window_not_found': self.recover_window,
            'parse_error': self.recover_parse,
            'command_failed': self.retry_command
        }
    
    def handle_error(self, error_type, error, context):
        self.error_count[error_type] = self.error_count.get(error_type, 0) + 1
        
        if self.error_count[error_type] > 5:
            raise Exception(f"Too many {error_type} errors")
        
        recovery = self.recovery_strategies.get(error_type)
        if recovery:
            return recovery(error, context)
```

## 6. Challenges and Solutions

### 6.1 Window Management Challenges

**Challenge**: Windows may move, resize, or be obscured.

**Solutions**:
- Store window handles, not positions
- Implement window tracking and re-discovery
- Use window bring-to-front before reading
- Implement position validation

```python
class WindowTracker:
    def __init__(self):
        self.windows = {}
        self.last_positions = {}
    
    def validate_windows(self):
        for name, hwnd in self.windows.items():
            if not win32gui.IsWindow(hwnd):
                self.rediscover_window(name)
            elif self.has_moved(hwnd):
                self.update_position(hwnd)
```

### 6.2 Text Parsing Challenges

**Challenge**: Text format may vary, special characters, incomplete updates.

**Solutions**:
- Robust regex patterns with fallbacks
- Fuzzy string matching for card/relic names
- State validation and sanity checks
- Incremental parsing with error recovery

```python
class RobustParser:
    def parse_with_fallback(self, text, patterns):
        for pattern in patterns:
            try:
                match = re.search(pattern, text)
                if match:
                    return match.groups()
            except:
                continue
        return None
    
    def fuzzy_match_card(self, card_text, known_cards):
        from difflib import get_close_matches
        matches = get_close_matches(card_text, known_cards, n=1, cutoff=0.8)
        return matches[0] if matches else None
```

### 6.3 Timing and Synchronization

**Challenge**: Game animations, state transitions, command processing delays.

**Solutions**:
- Implement state change detection
- Adaptive waiting based on action type
- Command confirmation through state changes
- Animation skip commands when available

```python
class TimingManager:
    def __init__(self):
        self.action_delays = {
            'play_card': 1.0,
            'end_turn': 2.0,
            'potion': 0.5,
            'choice': 0.3
        }
    
    def wait_for_state_change(self, old_state, timeout=5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            new_state = self.read_current_state()
            if self.has_changed(old_state, new_state):
                return True
            time.sleep(0.1)
        return False
```

### 6.4 Complex Game States

**Challenge**: Events with multiple choices, complex card interactions, deck building.

**Solutions**:
- State machine for different game modes
- Context-aware parsing
- History tracking for multi-step decisions
- Specialized handlers for each game mode

```python
class GameModeHandler:
    def __init__(self):
        self.handlers = {
            'combat': CombatHandler(),
            'map': MapHandler(),
            'shop': ShopHandler(),
            'event': EventHandler(),
            'card_reward': CardRewardHandler(),
            'rest': RestHandler()
        }
    
    def handle_current_mode(self, game_state):
        mode = self.detect_game_mode(game_state)
        handler = self.handlers.get(mode)
        if handler:
            return handler.handle(game_state)
```

## 7. Implementation Roadmap

### Phase 1: Basic Infrastructure (Week 1-2)
1. Window detection and text extraction
2. Basic game state parsing
3. Simple command sending
4. Logging and debugging framework

### Phase 2: Core Gameplay (Week 3-4)
1. Complete combat state parsing
2. Basic combat decision making
3. Card play execution
4. Turn management

### Phase 3: Advanced Features (Week 5-6)
1. Map navigation
2. Shop interactions
3. Event handling
4. Deck building decisions

### Phase 4: Optimization (Week 7-8)
1. Decision algorithm improvements
2. Performance optimization
3. Error recovery enhancement
4. Configuration system

### Phase 5: Machine Learning (Optional, Week 9+)
1. Data collection system
2. State encoding
3. Model training pipeline
4. Neural network integration

## 8. Development Best Practices

### 8.1 Modular Design
- Separate window management from game logic
- Abstract decision making from state parsing
- Plugin architecture for different agents

### 8.2 Testing Strategy
- Unit tests for parsers
- Integration tests with mock windows
- Record and replay game states
- Performance benchmarking

### 8.3 Configuration Management
```python
# config.yaml
window_detection:
  method: "ui_automation"  # or "ocr", "windows_api"
  retry_attempts: 3
  
parsing:
  fuzzy_match_threshold: 0.8
  validation_enabled: true
  
agent:
  type: "evaluation"  # or "rules", "mcts", "neural"
  thinking_time: 1.0
  
logging:
  level: "debug"
  file: "sts_agent.log"
```

### 8.4 Debugging Tools
- Screenshot capture on errors
- State history replay
- Decision explanation system
- Performance profiling

## 9. Example Implementation Structure

```
sts-agent/
├── src/
│   ├── window_management/
│   │   ├── __init__.py
│   │   ├── window_detector.py
│   │   ├── text_extractor.py
│   │   └── ocr_fallback.py
│   ├── parsing/
│   │   ├── __init__.py
│   │   ├── state_parser.py
│   │   ├── combat_parser.py
│   │   ├── map_parser.py
│   │   └── card_database.py
│   ├── game_state/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── state_manager.py
│   │   └── validators.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── rule_agent.py
│   │   ├── evaluation_agent.py
│   │   └── mcts_agent.py
│   ├── command_execution/
│   │   ├── __init__.py
│   │   ├── command_sender.py
│   │   └── action_translator.py
│   └── main.py
├── tests/
├── config/
├── logs/
└── README.md
```

## 10. Conclusion

This plan provides a comprehensive approach to building a Slay the Spire agent using the Text the Spire mod. The modular architecture allows for iterative development and easy swapping of different components. Starting with basic window reading and rule-based decisions, the system can evolve to use more sophisticated algorithms and even machine learning approaches.

Key success factors:
1. Robust window and text handling
2. Accurate game state parsing
3. Flexible decision-making architecture
4. Good error handling and recovery
5. Iterative development approach

The proposed solution balances complexity with practicality, providing a clear path from a basic working agent to a sophisticated AI player.