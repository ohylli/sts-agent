"""Stub implementations for Text the Spire integration."""

import time
from typing import List, Optional
from sts_types import WindowInfo, CommandResult, ExecuteAndReadResult, WindowContent, MultiWindowContent
from utils.constants import GAME_STATE_WINDOWS, AVERAGE_INPUT_LATENCY, AVERAGE_RESPONSE_TIME
from .window_finder import list_windows  # Use real implementation
from .text_extractor import read_window as _read_window, read_multiple_windows as _read_multiple_windows

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
    """Read content from a specific window using real text extractor."""
    return _read_window(window_title)

def read_multiple_windows(window_titles: List[str]) -> MultiWindowContent:
    """Read content from multiple windows using real text extractor."""
    return _read_multiple_windows(window_titles)

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