#!/usr/bin/env python3
"""
Test different methods to check if prompt window has content.
"""

import sys
import os
import time
from pywinauto import Application
import win32gui
import win32con
import win32api

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from reliable_window_finder import TextTheSpireWindowFinder

def test_prompt_content_methods():
    """Test various methods to check prompt content."""
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
        
        print("\n=== METHOD 1: Check window_text() ===")
        print(f"window_text(): '{window.window_text()}'")
        print("[RESULT] Returns window title, not content")
        
        print("\n=== METHOD 2: Check children for edit controls ===")
        children = window.children()
        print(f"Number of children: {len(children)}")
        for i, child in enumerate(children):
            try:
                print(f"Child {i}: class='{child.class_name()}', text='{child.window_text()}'")
                # Try to get text from edit control
                if 'edit' in child.class_name().lower():
                    print(f"  Found edit control! Trying to get content...")
                    # Try different methods
                    try:
                        texts = child.texts()
                        print(f"  texts(): {texts}")
                    except:
                        print(f"  texts() failed")
            except Exception as e:
                print(f"Child {i}: Error - {e}")
        
        print("\n=== METHOD 3: Try to get selected text ===")
        window.set_focus()
        time.sleep(0.1)
        # Select all
        window.type_keys("^a")
        time.sleep(0.1)
        # Try to copy (this might not work)
        window.type_keys("^c")
        time.sleep(0.1)
        print("[INFO] Attempted to select all and copy")
        
        print("\n=== METHOD 4: Use Edit control methods ===")
        try:
            # Try to treat window as edit control
            edit_text = window.get_value()
            print(f"get_value(): '{edit_text}'")
        except Exception as e:
            print(f"get_value() failed: {e}")
        
        try:
            # Try text_block()
            text_block = window.text_block()
            print(f"text_block(): '{text_block}'")
        except Exception as e:
            print(f"text_block() failed: {e}")
        
        print("\n=== METHOD 5: Send test characters and check response ===")
        print("[INFO] Typing 'test' into prompt...")
        window.type_keys("test")
        time.sleep(0.1)
        
        # Now try to check if we can detect the content
        print("[INFO] Selecting all...")
        window.type_keys("^a")
        time.sleep(0.1)
        
        # Clear it
        print("[INFO] Deleting selected text...")
        window.type_keys("{DELETE}")
        time.sleep(0.1)
        
        print("\n=== METHOD 6: Use Windows API to get text ===")
        handle = prompt_data['hwnd']
        try:
            # Get text length
            text_length = win32gui.SendMessage(handle, win32con.WM_GETTEXTLENGTH, 0, 0)
            print(f"WM_GETTEXTLENGTH: {text_length}")
            
            # Get actual text
            buffer_size = text_length + 1
            buffer = win32gui.PyMakeBuffer(buffer_size)
            win32gui.SendMessage(handle, win32con.WM_GETTEXT, buffer_size, buffer)
            text = buffer[:text_length]
            print(f"WM_GETTEXT: '{text}'")
        except Exception as e:
            print(f"Windows API method failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Testing failed: {e}")
        return False

def test_smart_clearing():
    """Test a smart clearing approach."""
    finder = TextTheSpireWindowFinder()
    
    prompt_data = finder.get_prompt_window()
    if not prompt_data:
        print("[ERROR] Prompt window not found")
        return False
    
    try:
        app = Application().connect(handle=prompt_data['hwnd'])
        window = app.window(handle=prompt_data['hwnd'])
        
        print("\n=== SMART CLEARING APPROACH ===")
        window.set_focus()
        time.sleep(0.1)
        
        # Method 1: Try select all and type - if empty, first char gets selected
        print("[INFO] Attempting smart clear...")
        
        # Type a test character
        window.type_keys("X")
        time.sleep(0.05)
        
        # Select all (will select X plus any existing content)  
        window.type_keys("^a")
        time.sleep(0.05)
        
        # Delete everything
        window.type_keys("{DELETE}")
        time.sleep(0.1)
        
        print("[INFO] Smart clear complete - should work whether empty or not")
        
        # Now type the actual command
        print("[INFO] Typing 'info' command...")
        window.type_keys("info")
        time.sleep(0.1)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Smart clearing failed: {e}")
        return False

if __name__ == "__main__":
    print("TESTING PROMPT CONTENT DETECTION METHODS")
    print("=" * 60)
    
    # Test various methods
    test_prompt_content_methods()
    
    # Test smart clearing
    test_smart_clearing()
    
    print("\n[DONE] Testing complete")