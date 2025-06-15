#!/usr/bin/env python3
"""
Improved command sending that handles both empty and non-empty prompts.
"""

import sys
import os
import time
from pywinauto import Application

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from reliable_window_finder import TextTheSpireWindowFinder

def send_command_smart(command="info"):
    """Send a command using smart clearing that works whether prompt is empty or not."""
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
        
        print(f"[INFO] Sending '{command}' command...")
        window.set_focus()
        time.sleep(0.1)
        
        # Smart clearing approach:
        # 1. Type a space (won't trigger error sound even if empty)
        # 2. Select all (selects space + any existing content)
        # 3. Type the command (replaces selection)
        
        print("[INFO] Smart clearing prompt...")
        window.type_keys(" ")      # Type space (no error sound)
        time.sleep(0.05)
        window.type_keys("^a")     # Select all
        time.sleep(0.05)
        window.type_keys(command)  # Type command (replaces selection)
        time.sleep(0.1)
        
        print("[INFO] Executing command...")
        window.type_keys("{ENTER}")
        
        print(f"[OK] Command '{command}' sent successfully")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send command: {e}")
        return False

def verify_command_in_log(command):
    """Check if command appears in the log window."""
    finder = TextTheSpireWindowFinder()
    
    # Wait a moment for log to update
    time.sleep(1.0)
    
    # Get Log window
    log_window = finder.get_window_by_title('Log')
    if not log_window:
        print("[ERROR] Log window not found")
        return False
    
    try:
        # Connect and read content
        app = Application().connect(handle=log_window['hwnd'])
        window = app.window(handle=log_window['hwnd'])
        
        # Extract text
        children = window.children()
        all_text = []
        for child in children:
            child_text = child.window_text()
            if child_text.strip():
                all_text.append(child_text)
        
        log_content = '\n'.join(all_text).strip()
        
        # Check if command is in log
        if command in log_content:
            print(f"[VERIFIED] Command '{command}' found in log")
            # Show first few lines of log
            lines = log_content.split('\n')
            print(f"[LOG] First 3 lines: {lines[:3]}")
            return True
        else:
            print(f"[WARNING] Command '{command}' not found in log")
            print(f"[LOG] Content: {log_content[:100]}...")
            return False
            
    except Exception as e:
        print(f"[ERROR] Failed to read log: {e}")
        return False

def test_window_title_change(command="info"):
    """Test if command changes the window title."""
    finder = TextTheSpireWindowFinder()
    
    # Get initial prompt window info
    prompt_before = finder.get_prompt_window(use_cache=False)
    if not prompt_before:
        print("[ERROR] Prompt window not found")
        return
    
    print(f"\n[BEFORE] Prompt window title: '{prompt_before['title']}'")
    
    # Send command
    success = send_command_smart(command)
    if not success:
        return
    
    # Verify command was received
    verified = verify_command_in_log(command)
    
    # Wait a bit for any potential title change
    print("\n[INFO] Waiting 2 seconds for potential title change...")
    time.sleep(2.0)
    
    # Check prompt window again
    prompt_after = finder.get_prompt_window(use_cache=False)
    if not prompt_after:
        print("[ERROR] Prompt window not found after command")
        return
    
    print(f"\n[AFTER] Prompt window title: '{prompt_after['title']}'")
    
    if prompt_before['title'] != prompt_after['title']:
        print(f"\n[DISCOVERY] Window title changed from '{prompt_before['title']}' to '{prompt_after['title']}'!")
    else:
        print(f"\n[RESULT] Window title unchanged (still '{prompt_after['title']}')")

if __name__ == "__main__":
    print("IMPROVED COMMAND SENDING TEST")
    print("=" * 60)
    
    # Test the improved command sending
    test_window_title_change("info")
    
    print("\n[DONE] Test complete")