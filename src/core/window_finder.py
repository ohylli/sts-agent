"""Window finder for Text the Spire integration."""

import win32gui
from typing import List, Dict, Tuple
from sts_types import WindowInfo
from utils.constants import GAME_STATE_WINDOWS


def _enum_windows_callback(hwnd: int, windows: List[Tuple[int, str, str]]) -> bool:
    """Callback function for EnumWindows to collect window information."""
    try:
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            if title:  # Only include windows with titles
                windows.append((hwnd, title, class_name))
    except Exception:
        # Skip windows that cause errors
        pass
    return True


def list_windows() -> List[WindowInfo]:
    """List all available Text the Spire windows."""
    # Collect all visible windows
    all_windows: List[Tuple[int, str, str]] = []
    win32gui.EnumWindows(_enum_windows_callback, all_windows)
    
    # Filter and categorize Text the Spire windows
    text_spire_windows: List[WindowInfo] = []
    
    for hwnd, title, class_name in all_windows:
        # Game state windows (SWT_Window0 class)
        if title in GAME_STATE_WINDOWS and class_name == 'SWT_Window0':
            text_spire_windows.append({
                'title': title,
                'type': 'game_state',
                'class_name': class_name
            })
        # Prompt window (SunAwtFrame class)
        elif title in ['Prompt', 'info'] and class_name == 'SunAwtFrame':
            text_spire_windows.append({
                'title': title,
                'type': 'command',
                'class_name': class_name
            })
    
    # Sort for consistent ordering: game state windows first, then command window
    text_spire_windows.sort(key=lambda w: (w['type'] != 'game_state', w['title']))
    
    return text_spire_windows