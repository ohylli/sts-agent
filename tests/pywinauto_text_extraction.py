#!/usr/bin/env python3
"""
Phase 1 - Section 3.1: Text the Spire Window Connection with pywinauto

Tests connecting to Text the Spire windows using pywinauto approach.
Based on findings from window_documentation.md:
- Game state windows: class SWT_Window0 (9 windows)
- Command window: class SunAwtFrame, title "Prompt"
- Window handles are stable during gameplay but change between sessions
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from pywinauto import Application, Desktop
from pywinauto.findwindows import find_windows
import time
from reliable_window_finder import TextTheSpireWindowFinder

def test_pywinauto_connection():
    """Test connecting to Text the Spire windows using pywinauto"""
    print("=== Testing pywinauto Connection to Text the Spire Windows ===\n")
    
    # Use existing reliable window finder to get window handles
    finder = TextTheSpireWindowFinder()
    
    # Get all Text the Spire windows
    print("1. Finding Text the Spire windows...")
    game_state_windows = finder.get_game_state_windows()
    prompt_window = finder.get_prompt_window()
    
    if not game_state_windows:
        print("ERROR: No Text the Spire game state windows found!")
        print("Make sure Text the Spire is running with the mod loaded.")
        return False
    
    print(f"Found {len(game_state_windows)} game state windows")
    if prompt_window:
        print("Found prompt window")
    else:
        print("WARNING: Prompt window not found")
    
    print("\n2. Testing pywinauto connection to game state windows...")
    
    # Test connecting to each game state window
    connected_windows = []
    for i, window_dict in enumerate(game_state_windows):
        handle = window_dict['hwnd']
        title = window_dict['title']
        try:
            print(f"\nTesting window {i+1}: '{title}' (handle: {handle})")
            
            # Connect to window using pywinauto
            app = Application().connect(handle=handle)
            window = app.window(handle=handle)
            
            # Test basic properties
            print(f"  - Window exists: {window.exists()}")
            print(f"  - Window visible: {window.is_visible()}")
            print(f"  - Window enabled: {window.is_enabled()}")
            print(f"  - Window class: {window.class_name()}")
            print(f"  - Window text: '{window.window_text()}'")
            print(f"  - Rectangle: {window.rectangle()}")
            
            connected_windows.append((handle, title, window))
            print(f"  [OK] Successfully connected to '{title}'")
            
        except Exception as e:
            print(f"  [FAIL] Failed to connect to '{title}': {e}")
    
    print(f"\n3. Successfully connected to {len(connected_windows)}/{len(game_state_windows)} game state windows")
    
    # Test prompt window connection if available
    if prompt_window:
        handle = prompt_window['hwnd']
        title = prompt_window['title']
        try:
            print(f"\n4. Testing prompt window connection: '{title}'")
            app = Application().connect(handle=handle)
            window = app.window(handle=handle)
            
            print(f"  - Window exists: {window.exists()}")
            print(f"  - Window visible: {window.is_visible()}")
            print(f"  - Window enabled: {window.is_enabled()}")
            print(f"  - Window class: {window.class_name()}")
            print(f"  - Window text: '{window.window_text()}'")
            print(f"  [OK] Successfully connected to prompt window")
            
        except Exception as e:
            print(f"  [FAIL] Failed to connect to prompt window: {e}")
    
    return len(connected_windows) > 0

def test_window_controls():
    """Test accessing window controls and text content"""
    print("\n=== Testing Window Controls and Text Content ===\n")
    
    finder = TextTheSpireWindowFinder()
    game_state_windows = finder.get_game_state_windows()
    
    if not game_state_windows:
        print("No game state windows found for control testing")
        return False
    
    # Test the first few windows for control access
    for i, window_dict in enumerate(game_state_windows[:3]):
        handle = window_dict['hwnd']
        title = window_dict['title']
        try:
            print(f"\nTesting controls for '{title}':")
            
            app = Application().connect(handle=handle)
            window = app.window(handle=handle)
            
            # Try to get all child controls
            controls = window.children()
            print(f"  - Found {len(controls)} child controls")
            
            # Try different methods to get text content
            try:
                window_text = window.window_text()
                print(f"  - Window text: '{window_text[:100]}{'...' if len(window_text) > 100 else ''}'")
            except Exception as e:
                print(f"  - Window text failed: {e}")
            
            # Test control iteration
            for j, control in enumerate(controls[:5]):  # Limit to first 5 controls
                try:
                    control_text = control.window_text()
                    control_class = control.class_name()
                    print(f"    Control {j}: class='{control_class}' text='{control_text[:50]}{'...' if len(control_text) > 50 else ''}'")
                except Exception as e:
                    print(f"    Control {j}: Error reading - {e}")
            
            if len(controls) > 5:
                print(f"    ... and {len(controls) - 5} more controls")
                
        except Exception as e:
            print(f"  [FAIL] Failed to analyze controls for '{title}': {e}")
    
    return True

def test_text_extraction_methods():
    """Test different methods for extracting text from windows"""
    print("\n=== Testing Text Extraction Methods ===\n")
    
    finder = TextTheSpireWindowFinder()
    game_state_windows = finder.get_game_state_windows()
    
    if not game_state_windows:
        print("No game state windows found for text extraction testing")
        return False
    
    # Focus on a few key windows for detailed text extraction testing
    priority_windows = ['Player', 'Monster', 'Hand', 'Output']
    
    for window_dict in game_state_windows:
        handle = window_dict['hwnd']
        title = window_dict['title']
        if title not in priority_windows:
            continue
            
        print(f"\nTesting text extraction from '{title}':")
        
        try:
            app = Application().connect(handle=handle)
            window = app.window(handle=handle)
            
            # Method 1: Direct window text
            try:
                text = window.window_text()
                print(f"  Method 1 (window_text): {len(text)} chars")
                if text.strip():
                    print(f"    Preview: '{text[:100]}{'...' if len(text) > 100 else ''}'")
                else:
                    print("    No text content")
            except Exception as e:
                print(f"  Method 1 failed: {e}")
            
            # Method 2: Children text aggregation
            try:
                children = window.children()
                all_text = []
                for child in children:
                    child_text = child.window_text()
                    if child_text.strip():
                        all_text.append(child_text)
                
                combined = '\n'.join(all_text)
                print(f"  Method 2 (children): {len(combined)} chars from {len(all_text)} controls")
                if combined.strip():
                    print(f"    Preview: '{combined[:100]}{'...' if len(combined) > 100 else ''}'")
                else:
                    print("    No text content from children")
            except Exception as e:
                print(f"  Method 2 failed: {e}")
            
            # Method 3: Print control for specific classes
            try:
                # Look for text-specific control types
                text_controls = []
                for child in window.children():
                    class_name = child.class_name()
                    if any(keyword in class_name.lower() for keyword in ['text', 'label', 'static', 'edit']):
                        text_controls.append((class_name, child.window_text()))
                
                print(f"  Method 3 (text controls): Found {len(text_controls)} text-type controls")
                for class_name, text in text_controls[:3]:  # Show first 3
                    print(f"    {class_name}: '{text[:50]}{'...' if len(text) > 50 else ''}'")
                    
            except Exception as e:
                print(f"  Method 3 failed: {e}")
                
        except Exception as e:
            print(f"  [FAIL] Failed to test text extraction for '{title}': {e}")
    
    return True

def main():
    """Run all pywinauto connection tests"""
    print("Text the Spire - pywinauto Connection Testing")
    print("=" * 50)
    
    # Test 1: Basic connection
    success1 = test_pywinauto_connection()
    
    # Test 2: Window controls
    success2 = test_window_controls()
    
    # Test 3: Text extraction methods
    success3 = test_text_extraction_methods()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Basic Connection: {'[PASS]' if success1 else '[FAIL]'}")
    print(f"Window Controls: {'[PASS]' if success2 else '[FAIL]'}")
    print(f"Text Extraction: {'[PASS]' if success3 else '[FAIL]'}")
    
    if success1 and success2 and success3:
        print("\n[PASS] All pywinauto connection tests passed!")
        print("Ready to proceed with detailed text content extraction.")
    else:
        print("\n[FAIL] Some tests failed. Check Text the Spire mod setup.")
    
    return success1 and success2 and success3

if __name__ == "__main__":
    main()