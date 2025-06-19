"""Command execution module for Text the Spire integration."""

import time
from typing import List, Optional
from pywinauto import Application

from sts_types import CommandResult
from utils.constants import (
    QUICK_COMMAND_WAIT, SLOW_COMMAND_WAIT, 
    SLOW_COMMANDS,
    AVERAGE_INPUT_LATENCY, PROMPT_WINDOW_TITLES
)
from .text_extractor import read_window, _get_window_handle

def get_command_wait_time(command: str) -> float:
    """Determine wait time based on command type."""
    # Extract first word from command for categorization
    first_word = command.strip().split()[0].lower() if command.strip() else ""
    
    if first_word in SLOW_COMMANDS:
        return SLOW_COMMAND_WAIT
    else:
        # Default to quick command wait time
        return QUICK_COMMAND_WAIT

def read_log_window() -> Optional[str]:
    """Read content from the Log window using text_extractor."""
    result = read_window("Log")
    if result["error"]:
        return None
    return result["content"]

def send_command_to_prompt(command: str) -> bool:
    """Send command to prompt window using smart clearing approach."""
    # Try to find prompt window by checking all known prompt window titles
    prompt_handle = None
    for title in PROMPT_WINDOW_TITLES:
        handle = _get_window_handle(title)
        if handle:
            prompt_handle = handle
            break
    
    if not prompt_handle:
        return False
    
    try:
        app = Application().connect(handle=prompt_handle)
        window = app.window(handle=prompt_handle)
        
        window.set_focus()
        time.sleep(0.1)
        
        # Smart clearing approach from existing implementation
        window.type_keys(" ")      # Type space (no error sound)
        time.sleep(0.05)
        window.type_keys("^a")     # Select all
        time.sleep(0.05)
        window.type_keys(command)  # Type command (replaces selection)
        time.sleep(0.1)
        window.type_keys("{ENTER}")
        
        return True
    except Exception:
        return False

def extract_log_difference(before_log: str, after_log: str) -> str:
    """Extract new content from log by comparing before and after."""
    if not before_log:
        return after_log or ""
    
    if not after_log:
        return ""
    
    # Simple approach: if after_log is longer, return the difference
    if len(after_log) > len(before_log):
        # Check if after_log contains before_log as prefix
        if after_log.endswith(before_log):
            return after_log[:-len(before_log)].strip()
        else:
            # Logs may have been truncated/rotated, return full after_log
            return after_log
    
    return ""

def command_appears_in_log(command: str, log_content: str) -> bool:
    """Check if command appears in the log content."""
    if not log_content:
        return False
    
    # Simple check: command appears in log
    return command.lower() in log_content.lower()

def execute_command(command: str, verify: bool = True, timeout: float = 5.0) -> CommandResult:
    """Execute a command in the Prompt window and capture response."""
    start_time = time.time()
    
    # Determine wait time based on command type
    wait_time = get_command_wait_time(command)
    
    # Capture log state before command
    before_log = read_log_window() if verify else None
    
    # Send command
    send_success = send_command_to_prompt(command)
    if not send_success:
        return {
            "success": False,
            "command": command,
            "response_time": time.time() - start_time,
            "wait_time_used": 0.0,
            "command_found_in_log": False,
            "log_response": None,
            "error": "Failed to send command to prompt window"
        }
    
    # Wait for command processing
    time.sleep(wait_time)
    
    # Capture log state after command
    after_log = read_log_window() if verify else None
    
    # Extract response and verify
    log_response = None
    command_found = False
    
    if verify and before_log is not None and after_log is not None:
        log_response = extract_log_difference(before_log, after_log)
        command_found = command_appears_in_log(command, after_log)
    
    response_time = time.time() - start_time
    
    return {
        "success": True,
        "command": command,
        "response_time": response_time,
        "wait_time_used": wait_time,
        "command_found_in_log": command_found,
        "log_response": log_response,
        "error": None
    }

def execute_command_sequence(commands: List[str], verify: bool = True, timeout: float = 5.0) -> List[CommandResult]:
    """Execute a sequence of commands, waiting for each to complete."""
    results = []
    
    for command in commands:
        result = execute_command(command, verify=verify, timeout=timeout)
        results.append(result)
        
        # If command failed, still continue with remaining commands
        # but could add logic here to stop on failure if needed
    
    return results