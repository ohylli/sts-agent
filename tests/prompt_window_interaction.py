#!/usr/bin/env python3
"""
Test script for Text the Spire prompt window interaction.
Phase 1, Section 5.1: Prompt Window Interaction Testing

This script tests:
1. Finding the Text the Spire prompt window
2. Focusing the prompt window
3. Basic window properties and state
4. Preparation for command sending tests

Based on learnings from Sections 2-3:
- Use reliable_window_finder for consistent window detection
- Prompt window: Title="Prompt", Class="SunAwtFrame"
- pywinauto approach proven successful for window interaction
"""

import sys
import os
import time
from pywinauto import Application

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from reliable_window_finder import TextTheSpireWindowFinder

def test_prompt_window_finding():
    """Test finding the Text the Spire prompt window."""
    print("=== Testing Prompt Window Finding ===")
    
    finder = TextTheSpireWindowFinder()
    
    # Check if game is running
    if not finder.is_game_running():
        print("[ERROR] Text the Spire is not running with the mod")
        print("Please start the game with Text the Spire mod before running this test")
        return False
    
    # Find the prompt window
    prompt_window = finder.get_prompt_window()
    
    if not prompt_window:
        print("[ERROR] Prompt window not found")
        print("Available windows:")
        summary = finder.get_game_state_summary()
        for category, count in summary['window_counts'].items():
            print(f"  {category}: {count}")
        return False
    
    print(f"[OK] Prompt window found:")
    print(f"  Handle: {prompt_window['hwnd']}")
    print(f"  Title: '{prompt_window['title']}'")
    print(f"  Class: '{prompt_window['class_name']}'")
    print(f"  Size: {prompt_window['width']}x{prompt_window['height']}")
    print(f"  Process ID: {prompt_window['process_id']}")
    
    return prompt_window

def test_prompt_window_connection():
    """Test connecting to the prompt window with pywinauto."""
    print("\n=== Testing Prompt Window Connection ===")
    
    finder = TextTheSpireWindowFinder()
    prompt_window = finder.get_prompt_window()
    
    if not prompt_window:
        print("[ERROR] Cannot test connection - prompt window not found")
        return None
    
    handle = prompt_window['hwnd']
    
    try:
        # Connect using pywinauto (proven method from Section 3)
        app = Application().connect(handle=handle)
        window = app.window(handle=handle)
        
        print(f"[OK] Successfully connected to prompt window")
        print(f"  pywinauto window object: {window}")
        
        # Test window properties
        print(f"  Exists: {window.exists()}")
        print(f"  Visible: {window.is_visible()}")
        print(f"  Enabled: {window.is_enabled()}")
        print(f"  Window text: '{window.window_text()}'")
        print(f"  Class name: '{window.class_name()}'")
        
        # Get window rectangle
        rect = window.rectangle()
        print(f"  Rectangle: {rect}")
        
        return window
        
    except Exception as e:
        print(f"[ERROR] Failed to connect to prompt window: {e}")
        return None

def test_prompt_window_focus():
    """Test focusing the prompt window."""
    print("\n=== Testing Prompt Window Focus ===")
    
    finder = TextTheSpireWindowFinder()
    prompt_window = finder.get_prompt_window()
    
    if not prompt_window:
        print("[ERROR] Cannot test focus - prompt window not found")
        return False
    
    handle = prompt_window['hwnd']
    
    try:
        # Connect to window
        app = Application().connect(handle=handle)
        window = app.window(handle=handle)
        
        # Test if window can be focused
        print(f"[INFO] Attempting to focus prompt window...")
        
        # Try different focus methods
        focus_methods = [
            ("set_focus()", lambda: window.set_focus()),
            ("click_input()", lambda: window.click_input()),
            ("restore()", lambda: window.restore()),
        ]
        
        for method_name, method_func in focus_methods:
            try:
                print(f"  Trying {method_name}...")
                method_func()
                print(f"  [OK] {method_name} executed successfully")
                
                # Small delay to let focus take effect
                time.sleep(0.1)
                
                # Check if window is focused (has focus)
                # Note: pywinauto doesn't have a direct "has_focus" method
                # so we'll check if the window is still accessible
                if window.is_visible() and window.is_enabled():
                    print(f"  [OK] Window appears to be accessible after {method_name}")
                else:
                    print(f"  [WARN] Window accessibility unclear after {method_name}")
                
            except Exception as e:
                print(f"  [ERROR] {method_name} failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Focus testing failed: {e}")
        return False

def test_prompt_window_children():
    """Test examining prompt window children (for input controls)."""
    print("\n=== Testing Prompt Window Children ===")
    
    finder = TextTheSpireWindowFinder()
    prompt_window = finder.get_prompt_window()
    
    if not prompt_window:
        print("[ERROR] Cannot test children - prompt window not found")
        return None
    
    handle = prompt_window['hwnd']
    
    try:
        # Connect to window
        app = Application().connect(handle=handle)
        window = app.window(handle=handle)
        
        # Get children (using method from Section 3.2)
        children = window.children()
        print(f"[OK] Found {len(children)} child controls")
        
        for i, child in enumerate(children):
            try:
                child_text = child.window_text()
                child_class = child.class_name()
                child_rect = child.rectangle()
                
                print(f"  Child {i}:")
                print(f"    Text: '{child_text}'")
                print(f"    Class: '{child_class}'")
                print(f"    Rectangle: {child_rect}")
                print(f"    Visible: {child.is_visible()}")
                print(f"    Enabled: {child.is_enabled()}")
                
                # Check if this looks like an input control
                if child_class.lower() in ['edit', 'textbox', 'input']:
                    print(f"    [INFO] This appears to be an input control!")
                
            except Exception as e:
                print(f"    [ERROR] Could not examine child {i}: {e}")
        
        return children
        
    except Exception as e:
        print(f"[ERROR] Children examination failed: {e}")
        return None

def run_all_tests():
    """Run all prompt window interaction tests."""
    print("TEXT THE SPIRE PROMPT WINDOW INTERACTION TESTING")
    print("Phase 1, Section 5.1: Prompt Window Interaction")
    print("=" * 60)
    
    # Test 1: Finding the prompt window
    prompt_window = test_prompt_window_finding()
    if not prompt_window:
        print("\n[FAILED] Cannot proceed - prompt window not found")
        return False
    
    # Test 2: Connecting with pywinauto
    window_object = test_prompt_window_connection()
    if not window_object:
        print("\n[FAILED] Cannot proceed - pywinauto connection failed")
        return False
    
    # Test 3: Focusing the prompt window
    focus_success = test_prompt_window_focus()
    if not focus_success:
        print("\n[WARN] Focus testing had issues, but continuing...")
    
    # Test 4: Examining window children
    children = test_prompt_window_children()
    if children is None:
        print("\n[WARN] Children examination failed, but continuing...")
    
    print("\n" + "=" * 60)
    print("PROMPT WINDOW INTERACTION TEST SUMMARY")
    print("=" * 60)
    
    print(f"[+] Prompt window finding: {'PASS' if prompt_window else 'FAIL'}")
    print(f"[+] pywinauto connection: {'PASS' if window_object else 'FAIL'}")
    print(f"[+] Window focus: {'PASS' if focus_success else 'WARN'}")
    print(f"[+] Children examination: {'PASS' if children is not None else 'WARN'}")
    
    if prompt_window and window_object:
        print("\n[SUCCESS] Prompt window interaction basics are working!")
        print("Ready to proceed with command sending tests.")
        return True
    else:
        print("\n[FAILED] Prompt window interaction has critical issues.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)