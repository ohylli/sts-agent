#!/usr/bin/env python3
"""
Window enumeration script using win32api.
Part of Phase 1 feasibility testing for Text the Spire interaction.
"""

import win32gui
import win32con
import win32api
from typing import List, Dict, Tuple
import sys


def enum_windows_callback(hwnd: int, windows: List[Dict]) -> bool:
    """Callback function for EnumWindows to collect window information."""
    if win32gui.IsWindowVisible(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        
        # Get window rect for size info
        try:
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
        except:
            width = height = 0
            
        # Get process ID
        try:
            _, process_id = win32gui.GetWindowThreadProcessId(hwnd)
        except:
            process_id = 0
            
        windows.append({
            'hwnd': hwnd,
            'title': window_text,
            'class_name': class_name,
            'width': width,
            'height': height,
            'process_id': process_id
        })
    
    return True


def enumerate_all_windows() -> List[Dict]:
    """Enumerate all visible windows on the system."""
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows


def filter_text_spire_windows(windows: List[Dict]) -> List[Dict]:
    """Filter windows that might be related to Text the Spire mod."""
    text_spire_windows = []
    
    for window in windows:
        title_lower = window['title'].lower()
        class_lower = window['class_name'].lower()
        
        # Look for Text the Spire related keywords
        spire_keywords = ['text', 'spire', 'slay', 'prompt', 'accessibility']
        
        if any(keyword in title_lower for keyword in spire_keywords) or \
           any(keyword in class_lower for keyword in spire_keywords):
            text_spire_windows.append(window)
    
    return text_spire_windows


def print_window_info(windows: List[Dict], title: str = "") -> None:
    """Print formatted window information."""
    if title:
        print(f"\n{title}")
        print("=" * len(title))
    
    if not windows:
        print("No windows found.")
        return
        
    for i, window in enumerate(windows, 1):
        print(f"\n{i}. Handle: {window['hwnd']}")
        print(f"   Title: '{window['title']}'")
        print(f"   Class: '{window['class_name']}'")
        print(f"   Size: {window['width']}x{window['height']}")
        print(f"   PID: {window['process_id']}")


def main():
    """Main function to enumerate and display windows."""
    print("Enumerating all visible windows...")
    
    try:
        all_windows = enumerate_all_windows()
        print(f"Found {len(all_windows)} visible windows total.")
        
        # Filter for potential Text the Spire windows
        text_spire_windows = filter_text_spire_windows(all_windows)
        
        if text_spire_windows:
            print_window_info(text_spire_windows, "Potential Text the Spire Windows")
        else:
            print("\nNo Text the Spire windows detected.")
            print("Make sure the Text the Spire mod is running.")
            
        # Also show all windows with non-empty titles for reference
        non_empty_windows = [w for w in all_windows if w['title'].strip()]
        print_window_info(non_empty_windows[:20], "Sample of All Windows (first 20)")
        
        if len(non_empty_windows) > 20:
            print(f"\n... and {len(non_empty_windows) - 20} more windows")
            
    except Exception as e:
        print(f"Error enumerating windows: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()