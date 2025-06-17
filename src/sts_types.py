"""Type definitions for Text the Spire integration."""

from typing import TypedDict, Optional, Any, List

class WindowInfo(TypedDict):
    """Information about a Text the Spire window."""
    title: str
    type: str  # 'game_state' or 'command'
    class_name: str

class CommandResult(TypedDict):
    """Result of executing a command."""
    success: bool
    command: str
    response_time: float
    error: Optional[str]

class ExecuteAndReadResult(TypedDict):
    """Result of executing a command and reading a window."""
    command_success: bool
    command: str
    response_time: float
    window_content: Optional[str]
    error: Optional[str]

class WindowContent(TypedDict):
    """Content from a Text the Spire window."""
    window_title: str
    content: str
    error: Optional[str]

class MultiWindowContent(TypedDict):
    """Content from multiple windows."""
    windows: List[WindowContent]
    total_time: float