"""Stub implementations for Text the Spire integration."""

import time
from typing import List, Optional
from sts_types import WindowInfo, CommandResult, ExecuteAndReadResult, WindowContent, MultiWindowContent
from utils.constants import GAME_STATE_WINDOWS, AVERAGE_INPUT_LATENCY, AVERAGE_RESPONSE_TIME
from .window_finder import list_windows  # Use real implementation
from .text_extractor import read_window as _read_window, read_multiple_windows as _read_multiple_windows

def execute_command_sequence(commands: List[str], verify: bool = False, timeout: float = 5.0) -> List[CommandResult]:
    """Execute a sequence of commands using real implementation."""
    from .command_executor import execute_command_sequence as _execute_command_sequence
    return _execute_command_sequence(commands, verify=verify, timeout=timeout)

def read_window(window_title: str) -> WindowContent:
    """Read content from a specific window using real text extractor."""
    return _read_window(window_title)

def read_multiple_windows(window_titles: List[str]) -> MultiWindowContent:
    """Read content from multiple windows using real text extractor."""
    return _read_multiple_windows(window_titles)

