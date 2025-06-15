#!/usr/bin/env python3
"""
Specific Text the Spire window finder script.
Identifies and categorizes Text the Spire mod windows.
"""

import win32gui
from typing import List, Dict, Optional
import sys


def enum_windows_callback(hwnd: int, windows: List[Dict]) -> bool:
    """Callback function for EnumWindows to collect window information."""
    if win32gui.IsWindowVisible(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        
        try:
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0] 
            height = rect[3] - rect[1]
        except:
            width = height = 0
            
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


def find_text_spire_windows() -> Dict[str, List[Dict]]:
    """Find and categorize Text the Spire mod windows."""
    all_windows = []
    win32gui.EnumWindows(enum_windows_callback, all_windows)
    
    categorized = {
        'game_state_windows': [],
        'prompt_window': [],
        'main_game_window': [],
        'mod_launcher': [],
        'other_spire_windows': []
    }
    
    # Known Text the Spire game state window titles
    game_state_titles = {
        'Player', 'Monster', 'Hand', 'Deck', 'Discard', 
        'Orbs', 'Relic', 'Output', 'Log'
    }
    
    for window in all_windows:
        title = window['title']
        class_name = window['class_name']
        
        # Main game window
        if 'Slay the Spire' in title and class_name == 'LWJGL':
            categorized['main_game_window'].append(window)
        
        # Prompt window for commands (can be titled 'Prompt' or 'info')
        elif (title in ['Prompt', 'info']) and class_name == 'SunAwtFrame':
            categorized['prompt_window'].append(window)
        
        # Mod launcher
        elif 'ModTheSpire' in title:
            categorized['mod_launcher'].append(window)
        
        # Game state windows (Text the Spire mod windows)
        elif title in game_state_titles and class_name == 'SWT_Window0':
            categorized['game_state_windows'].append(window)
        
        # Other potential spire-related windows
        elif any(keyword in title.lower() for keyword in ['spire', 'text']):
            categorized['other_spire_windows'].append(window)
    
    return categorized


def print_categorized_windows(categorized: Dict[str, List[Dict]]) -> None:
    """Print categorized window information."""
    for category, windows in categorized.items():
        if windows:
            print(f"\n{category.upper().replace('_', ' ')}")
            print("=" * len(category))
            
            for i, window in enumerate(windows, 1):
                print(f"{i}. '{window['title']}' (Handle: {window['hwnd']})")
                print(f"   Class: {window['class_name']}")
                print(f"   Size: {window['width']}x{window['height']}")


def get_window_by_title(title: str) -> Optional[Dict]:
    """Find a specific window by title."""
    all_windows = []
    win32gui.EnumWindows(enum_windows_callback, all_windows)
    
    for window in all_windows:
        if window['title'] == title:
            return window
    
    return None


def main():
    """Main function to find and display Text the Spire windows."""
    print("Searching for Text the Spire windows...")
    
    categorized = find_text_spire_windows()
    
    # Check if Text the Spire is running
    if not any(categorized.values()):
        print("No Text the Spire windows found.")
        print("Make sure Slay the Spire with Text the Spire mod is running.")
        return
    
    print_categorized_windows(categorized)
    
    # Summary
    print(f"\nSUMMARY:")
    print(f"Main game window: {len(categorized['main_game_window'])}")
    print(f"Prompt window: {len(categorized['prompt_window'])}")
    print(f"Game state windows: {len(categorized['game_state_windows'])}")
    print(f"Mod launcher: {len(categorized['mod_launcher'])}")
    print(f"Other spire windows: {len(categorized['other_spire_windows'])}")


if __name__ == "__main__":
    main()