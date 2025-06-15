#!/usr/bin/env python3
"""
Send a single command to verify title change behavior.
"""

import sys
import os
import time
from pywinauto import Application

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from reliable_window_finder import TextTheSpireWindowFinder

def send_info_command():
    """Send the 'info' command to the prompt window."""
    finder = TextTheSpireWindowFinder()
    
    # Get prompt window
    prompt_data = finder.get_prompt_window()
    if not prompt_data:
        print("[ERROR] Prompt window not found")
        return False
    
    print(f"[OK] Found prompt window: '{prompt_data['title']}' (Handle: {prompt_data['hwnd']})")
    
    try:
        # Connect with pywinauto
        app = Application().connect(handle=prompt_data['hwnd'])
        window = app.window(handle=prompt_data['hwnd'])
        
        # Send the info command
        print("[INFO] Sending 'info' command...")
        window.set_focus()
        time.sleep(0.1)
        
        # Smart clearing approach that works whether prompt is empty or not:
        # 1. Type a space (won't trigger error sound even if empty)
        # 2. Select all (selects space + any existing content)
        # 3. Type the command (replaces selection)
        print("[INFO] Using smart clearing approach...")
        window.type_keys(" ")      # Type space (no error sound)
        time.sleep(0.05)
        window.type_keys("^a")     # Select all
        time.sleep(0.05)
        window.type_keys("info")   # Type command (replaces selection)
        time.sleep(0.1)
        
        print("[INFO] Executing command...")
        window.type_keys("{ENTER}")     # Execute
        
        print("[OK] Command 'info' sent successfully")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send command: {e}")
        return False

if __name__ == "__main__":
    success = send_info_command()
    if success:
        print("\n[SUCCESS] Info command sent. Check log and window title now.")
    else:
        print("\n[FAILED] Could not send info command.")