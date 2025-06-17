"""Text extractor for Text the Spire integration using pywinauto."""

import time
import win32gui
from typing import List, Optional
from pywinauto import Application

from sts_types import WindowContent, MultiWindowContent
from utils.constants import GAME_STATE_WINDOWS


def _get_window_handle(window_title: str) -> Optional[int]:
    """Find window handle by title for Text the Spire windows."""
    def enum_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            # Only Text the Spire windows
            if title == window_title and class_name in ['SWT_Window0', 'SunAwtFrame']:
                windows.append(hwnd)
        return True
    
    windows = []
    win32gui.EnumWindows(enum_callback, windows)
    return windows[0] if windows else None


def _extract_window_text(handle: int, title: str) -> Optional[str]:
    """Extract text content from a window using the proven children aggregation method."""
    try:
        app = Application().connect(handle=handle)
        window = app.window(handle=handle)
        
        # Verify window is accessible
        if not window.exists() or not window.is_visible():
            return None
        
        # Use Method 2 (children aggregation) - proven most effective
        children = window.children()
        all_text = []
        for child in children:
            child_text = child.window_text()
            if child_text.strip():
                all_text.append(child_text)
        
        combined = '\n'.join(all_text)
        return combined.strip() if combined.strip() else None
        
    except Exception:
        # Return None for any connection/extraction errors
        return None


def read_window(window_title: str) -> WindowContent:
    """Read content from a specific Text the Spire window.
    
    Args:
        window_title: Title of the window to read (e.g., 'Player', 'Hand', 'Monster')
        
    Returns:
        WindowContent with the extracted text or error information
    """
    # Find the window handle
    handle = _get_window_handle(window_title)
    if not handle:
        return {
            "window_title": window_title,
            "content": "",
            "error": f"Window '{window_title}' not found"
        }
    
    # Extract text content
    content = _extract_window_text(handle, window_title)
    if content is None:
        return {
            "window_title": window_title,
            "content": "",
            "error": f"Failed to extract text from '{window_title}' window"
        }
    
    return {
        "window_title": window_title,
        "content": content,
        "error": None
    }


def read_multiple_windows(window_titles: List[str]) -> MultiWindowContent:
    """Read content from multiple Text the Spire windows.
    
    Args:
        window_titles: List of window titles to read
        
    Returns:
        MultiWindowContent with results from all windows and timing information
    """
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


def check_window_availability(window_title: str) -> bool:
    """Check if a Text the Spire window is currently available.
    
    Args:
        window_title: Title of the window to check
        
    Returns:
        True if window exists and is accessible, False otherwise
    """
    handle = _get_window_handle(window_title)
    if not handle:
        return False
    
    try:
        app = Application().connect(handle=handle)
        window = app.window(handle=handle)
        return window.exists() and window.is_visible()
    except Exception:
        return False


def get_available_windows() -> List[str]:
    """Get list of currently available Text the Spire game state windows.
    
    Returns:
        List of available window titles
    """
    available = []
    for window_title in GAME_STATE_WINDOWS:
        if check_window_availability(window_title):
            available.append(window_title)
    return available