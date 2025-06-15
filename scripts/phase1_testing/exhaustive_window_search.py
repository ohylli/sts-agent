#!/usr/bin/env python3
"""
Exhaustive search for any window that might be the 'info' prompt window.
"""

import win32gui
from typing import List, Dict

def enum_windows_callback(hwnd: int, windows: List[Dict]) -> bool:
    """Callback for window enumeration."""
    try:
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            _, process_id = win32gui.GetWindowThreadProcessId(hwnd)
            
            windows.append({
                'hwnd': hwnd,
                'title': title,
                'class_name': class_name,
                'width': width,
                'height': height,
                'process_id': process_id
            })
    except Exception as e:
        pass
    
    return True

def show_all_windows():
    """Show ALL visible windows to find the info window."""
    print("ALL VISIBLE WINDOWS (looking for 'info' title)")
    print("=" * 80)
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    
    # Sort by title for easier searching
    windows.sort(key=lambda w: w['title'].lower())
    
    info_windows = []
    small_windows = []
    sunawtframe_windows = []
    
    for i, window in enumerate(windows, 1):
        title = window['title']
        class_name = window['class_name']
        width = window['width']
        height = window['height']
        
        # Look for anything containing 'info' (case insensitive)
        if 'info' in title.lower():
            info_windows.append(window)
            print(f"*** INFO WINDOW FOUND ***")
        
        # Look for SunAwtFrame windows (original prompt class)
        if class_name == 'SunAwtFrame':
            sunawtframe_windows.append(window)
        
        # Look for small windows that could be prompts
        if 50 <= width <= 500 and 50 <= height <= 200 and title.strip():
            small_windows.append(window)
        
        # Show all windows with details
        print(f"{i:3}. '{title}' (Handle: {window['hwnd']})")
        print(f"     Class: {class_name}")
        print(f"     Size: {width}x{height}")
        print(f"     Process: {window['process_id']}")
        
        if 'info' in title.lower():
            print("     *** CONTAINS 'INFO' ***")
        if class_name == 'SunAwtFrame':
            print("     *** SunAwtFrame CLASS ***")
        if 50 <= width <= 500 and 50 <= height <= 200:
            print("     *** SMALL WINDOW (possible prompt) ***")
        
        print()
    
    print("=" * 80)
    print("SUMMARY OF INTERESTING WINDOWS:")
    print(f"Windows with 'info' in title: {len(info_windows)}")
    print(f"SunAwtFrame windows: {len(sunawtframe_windows)}")  
    print(f"Small windows (possible prompts): {len(small_windows)}")
    
    if info_windows:
        print("\nINFO WINDOWS DETAILS:")
        for w in info_windows:
            print(f"  '{w['title']}' - {w['class_name']} - {w['width']}x{w['height']}")
    
    if sunawtframe_windows:
        print("\nSUNAWTFRAME WINDOWS DETAILS:")
        for w in sunawtframe_windows:
            print(f"  '{w['title']}' - {w['class_name']} - {w['width']}x{w['height']}")
    
    return info_windows, sunawtframe_windows, small_windows

if __name__ == "__main__":
    info_windows, sunawtframe_windows, small_windows = show_all_windows()