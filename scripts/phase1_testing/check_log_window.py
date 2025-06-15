#!/usr/bin/env python3
"""
Check the Log window content to verify command was received.
"""

import sys
import os
from pywinauto import Application

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from reliable_window_finder import TextTheSpireWindowFinder

def check_log_window():
    """Check Log window content."""
    finder = TextTheSpireWindowFinder()
    
    # Get Log window
    log_window = finder.get_window_by_title('Log')
    if not log_window:
        print("[ERROR] Log window not found")
        return False
    
    print(f"[OK] Found Log window (Handle: {log_window['hwnd']})")
    
    try:
        # Connect and read content
        app = Application().connect(handle=log_window['hwnd'])
        window = app.window(handle=log_window['hwnd'])
        
        # Extract text using proven method
        children = window.children()
        all_text = []
        for child in children:
            child_text = child.window_text()
            if child_text.strip():
                all_text.append(child_text)
        
        log_content = '\n'.join(all_text).strip()
        
        print("\n=== LOG WINDOW CONTENT ===")
        print(log_content)
        print("=========================")
        
        # Check for 'info' in recent entries
        if 'info' in log_content.lower():
            print("\n[CONFIRMED] 'info' command found in log!")
            return True
        else:
            print("\n[INFO] 'info' command not visible in current log content")
            return False
        
    except Exception as e:
        print(f"[ERROR] Failed to read log: {e}")
        return False

if __name__ == "__main__":
    check_log_window()