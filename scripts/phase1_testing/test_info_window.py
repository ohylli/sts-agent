#!/usr/bin/env python3
"""
Test script to verify the 'info' window is the prompt window by attempting to read from it.
"""

import pywinauto
from pywinauto import Application, findwindows
import win32gui
import time


def test_info_window():
    """Test the 'info' window to confirm it's the prompt window."""
    print("TESTING 'info' WINDOW AS PROMPT WINDOW")
    print("=" * 40)
    
    # Find the info window
    info_handle = 148834590  # Handle found by find_info_window.py
    
    print(f"Target window handle: {info_handle}")
    
    # Verify the window still exists and get current info
    try:
        if win32gui.IsWindow(info_handle):
            title = win32gui.GetWindowText(info_handle)
            class_name = win32gui.GetClassName(info_handle)
            rect = win32gui.GetWindowRect(info_handle)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            
            print(f"Window exists: Yes")
            print(f"Title: '{title}'")
            print(f"Class: {class_name}")
            print(f"Size: {width}x{height}")
            print(f"Position: ({rect[0]}, {rect[1]})")
            print(f"Visible: {win32gui.IsWindowVisible(info_handle)}")
        else:
            print("ERROR: Window handle no longer valid")
            return False
    except Exception as e:
        print(f"ERROR: Could not get window info: {e}")
        return False
    
    # Try to connect using pywinauto
    print("\nTesting pywinauto connection...")
    try:
        # Connect using handle
        app = Application().connect(handle=info_handle)
        window = app.window(handle=info_handle)
        
        print(f"Connected successfully: {window.exists()}")
        print(f"Window is visible: {window.is_visible()}")
        print(f"Window is enabled: {window.is_enabled()}")
        
        # Try to get text content
        print("\nAttempting to read window text...")
        try:
            text_content = window.window_text()
            print(f"Window text: '{text_content}'")
        except Exception as e:
            print(f"Could not get window text: {e}")
        
        # Try to get all text from the window
        print("\nAttempting to read all text content...")
        try:
            # Get all control info
            controls = window.children()
            print(f"Number of child controls: {len(controls)}")
            
            for i, control in enumerate(controls):
                try:
                    control_text = control.window_text()
                    control_class = control.class_name()
                    print(f"  Control {i}: '{control_text}' (Class: {control_class})")
                except Exception as e:
                    print(f"  Control {i}: Error reading - {e}")
        
        except Exception as e:
            print(f"Could not enumerate controls: {e}")
        
        # Try getting the full window content
        print("\nAttempting to capture full window content...")
        try:
            full_text = window.get_line(0)  # Try to get first line
            print(f"First line: '{full_text}'")
        except Exception as e:
            print(f"Could not get line content: {e}")
        
        # Alternative approach - try to print properties
        print("\nWindow properties:")
        try:
            print(f"  Texts: {window.texts()}")
        except Exception as e:
            print(f"  Could not get texts: {e}")
            
        return True
        
    except Exception as e:
        print(f"ERROR: Could not connect with pywinauto: {e}")
        return False


def main():
    """Main test function."""
    success = test_info_window()
    
    if success:
        print("\n[SUCCESS] 'info' window appears to be accessible")
        print("This is likely the renamed prompt window!")
    else:
        print("\n[FAILED] Could not properly access 'info' window")
        print("May need different approach or window may not be the prompt")


if __name__ == "__main__":
    main()