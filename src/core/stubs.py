"""Stub implementations for Text the Spire integration."""

import time
from typing import List, Optional
from sts_types import WindowInfo, CommandResult, ExecuteAndReadResult, WindowContent, MultiWindowContent
from utils.constants import GAME_STATE_WINDOWS, AVERAGE_INPUT_LATENCY, AVERAGE_RESPONSE_TIME

def list_windows() -> List[WindowInfo]:
    """Stub: List all available Text the Spire windows."""
    print("[STUB] Would enumerate Text the Spire windows")
    print("[STUB] Found windows: Player, Monster, Hand, Deck, Discard, Orbs, Relic, Output, Log, Map, Prompt")
    
    # Return mock window list
    windows = []
    for window_name in GAME_STATE_WINDOWS:
        windows.append({
            "title": window_name,
            "type": "game_state",
            "class_name": "SWT_Window0"
        })
    windows.append({
        "title": "Prompt",
        "type": "command", 
        "class_name": "SunAwtFrame"
    })
    return windows

def execute_command(command: str, verify: bool = False, timeout: float = 5.0) -> CommandResult:
    """Stub: Execute a command in the Prompt window."""
    print(f"[STUB] Would send command to Prompt window: '{command}'")
    
    if verify:
        print(f"[STUB] Would verify command execution via Log window (timeout: {timeout}s)")
        print(f"[STUB] Expected response time: ~{AVERAGE_RESPONSE_TIME}s")
    
    # Simulate execution time
    time.sleep(0.1)
    
    return {
        "success": True,
        "command": command,
        "response_time": AVERAGE_INPUT_LATENCY,
        "error": None
    }

def execute_command_sequence(commands: List[str], verify: bool = False, timeout: float = 5.0) -> List[CommandResult]:
    """Stub: Execute a sequence of commands."""
    print(f"[STUB] Would execute {len(commands)} commands in sequence")
    if verify:
        print("[STUB] Each command would be verified before proceeding to next")
    
    results = []
    for i, cmd in enumerate(commands, 1):
        print(f"[STUB] Command {i}/{len(commands)}: '{cmd}'")
        result = execute_command(cmd, verify=verify, timeout=timeout)
        results.append(result)
    
    return results

def read_window(window_title: str) -> WindowContent:
    """Stub: Read content from a specific window."""
    print(f"[STUB] Would read content from '{window_title}' window")
    
    # Mock some example content
    mock_content = {
        "Player": "HP: 70/70\nEnergy: 3/3\nBlock: 0\nGold: 99",
        "Hand": "1. Strike - Deal 6 damage. Cost: 1\n2. Defend - Gain 5 Block. Cost: 1",
        "Monster": "Cultist - HP: 48/48\nIntent: Attack for 6 damage",
        "Map": "Floor 1 - Enemy\nFloor 2 - Unknown\nFloor 3 - Elite",
        "Log": "Turn 1\nDrew 5 cards\nPlayer's turn begins"
    }
    
    content = mock_content.get(window_title, f"[Mock content from {window_title} window]")
    print(f"[STUB] Window contains {len(content)} characters")
    
    return {
        "window_title": window_title,
        "content": content,
        "error": None
    }

def read_multiple_windows(window_titles: List[str]) -> MultiWindowContent:
    """Stub: Read content from multiple windows."""
    print(f"[STUB] Would read content from {len(window_titles)} windows: {', '.join(window_titles)}")
    
    start_time = time.time()
    windows = []
    
    for title in window_titles:
        window_content = read_window(title)
        windows.append(window_content)
    
    total_time = time.time() - start_time
    
    return {
        "windows": windows,
        "total_time": total_time
    }

def execute_and_read(command: str, window_title: str, verify: bool = True, timeout: float = 5.0) -> ExecuteAndReadResult:
    """Stub: Execute a command and then read a window."""
    print(f"[STUB] Would execute command '{command}' and then read '{window_title}' window")
    
    # Execute command
    cmd_result = execute_command(command, verify=verify, timeout=timeout)
    
    # Read window
    window_content = read_window(window_title)
    
    return {
        "command_success": cmd_result["success"],
        "command": command,
        "response_time": cmd_result["response_time"],
        "window_content": window_content["content"],
        "error": cmd_result["error"] or window_content["error"]
    }