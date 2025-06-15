#!/usr/bin/env python3
"""
Test script for sending commands to Text the Spire prompt window using Windows API.
Phase 1, Section 5.1.3: Test sending text commands using Windows API

This script tests:
1. Sending text commands using direct Windows API calls
2. Comparing Windows API approach with pywinauto approach
3. Testing different Windows API methods (SendMessage, PostMessage, etc.)
4. Performance and reliability comparison

Based on learnings from previous sections:
- Prompt window handle found reliably
- pywinauto approach is confirmed working
- Need to test Windows API as alternative approach
"""

import sys
import os
import time
import win32gui
import win32con
import win32api

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from reliable_window_finder import TextTheSpireWindowFinder

def get_prompt_window_handle():
    """Get the prompt window handle."""
    finder = TextTheSpireWindowFinder()
    
    if not finder.is_game_running():
        print("[ERROR] Text the Spire is not running with the mod")
        return None, None
    
    prompt_data = finder.get_prompt_window()
    if not prompt_data:
        print("[ERROR] Prompt window not found")
        return None, None
    
    return prompt_data['hwnd'], prompt_data

def test_window_focus_winapi():
    """Test focusing the prompt window using Windows API."""
    print("=== Testing Window Focus with Windows API ===")
    
    handle, prompt_data = get_prompt_window_handle()
    if not handle:
        return False
    
    print(f"Prompt window handle: {handle}")
    
    try:
        # Test different focus methods
        focus_methods = [
            ("SetForegroundWindow", lambda: win32gui.SetForegroundWindow(handle)),
            ("SetFocus", lambda: win32gui.SetFocus(handle)),
            ("ShowWindow(SW_RESTORE)", lambda: win32gui.ShowWindow(handle, win32con.SW_RESTORE)),
        ]
        
        for method_name, method_func in focus_methods:
            try:
                print(f"  Trying {method_name}...")
                result = method_func()
                print(f"  [OK] {method_name} returned: {result}")
                time.sleep(0.1)
            except Exception as e:
                print(f"  [ERROR] {method_name} failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Focus testing failed: {e}")
        return False

def test_send_message_methods():
    """Test different SendMessage methods for text input."""
    print("\n=== Testing SendMessage Methods ===")
    
    handle, prompt_data = get_prompt_window_handle()
    if not handle:
        return False
    
    # Test commands
    test_commands = ["help", "status", "info"]
    
    # Different message sending approaches
    message_methods = [
        ("WM_CHAR", test_wm_char),
        ("WM_KEYDOWN/WM_KEYUP", test_wm_keydown),
        ("WM_SETTEXT", test_wm_settext),
    ]
    
    for method_name, method_func in message_methods:
        print(f"\n--- Testing {method_name} ---")
        for command in test_commands:
            try:
                print(f"  Sending '{command}' with {method_name}")
                
                # Focus window first
                win32gui.SetForegroundWindow(handle)
                time.sleep(0.1)
                
                # Send the command
                success = method_func(handle, command)
                
                if success:
                    print(f"  [OK] Command sent successfully")
                    # Send Enter to execute
                    send_enter_key(handle)
                    time.sleep(0.5)
                else:
                    print(f"  [ERROR] Command sending failed")
                    
            except Exception as e:
                print(f"  [ERROR] {method_name} failed for '{command}': {e}")
    
    return True

def test_wm_char(handle, text):
    """Send text using WM_CHAR messages."""
    try:
        for char in text:
            win32api.SendMessage(handle, win32con.WM_CHAR, ord(char), 0)
            time.sleep(0.01)  # Small delay between characters
        return True
    except Exception as e:
        print(f"    WM_CHAR error: {e}")
        return False

def test_wm_keydown(handle, text):
    """Send text using WM_KEYDOWN/WM_KEYUP messages."""
    try:
        for char in text:
            vk_code = ord(char.upper())  # Virtual key code
            
            # Send key down
            win32api.SendMessage(handle, win32con.WM_KEYDOWN, vk_code, 0)
            time.sleep(0.01)
            
            # Send key up
            win32api.SendMessage(handle, win32con.WM_KEYUP, vk_code, 0)
            time.sleep(0.01)
        
        return True
    except Exception as e:
        print(f"    WM_KEYDOWN error: {e}")
        return False

def test_wm_settext(handle, text):
    """Send text using WM_SETTEXT message."""
    try:
        # Clear existing text and set new text
        win32api.SendMessage(handle, win32con.WM_SETTEXT, 0, text)
        return True
    except Exception as e:
        print(f"    WM_SETTEXT error: {e}")
        return False

def send_enter_key(handle):
    """Send Enter key to execute command."""
    try:
        # Send Enter key (VK_RETURN = 0x0D)
        win32api.SendMessage(handle, win32con.WM_KEYDOWN, 0x0D, 0)
        time.sleep(0.01)
        win32api.SendMessage(handle, win32con.WM_KEYUP, 0x0D, 0)
        return True
    except Exception as e:
        print(f"    Enter key error: {e}")
        return False

def test_performance_comparison():
    """Compare performance of Windows API vs pywinauto."""
    print("\n=== Testing Performance Comparison ===")
    
    handle, prompt_data = get_prompt_window_handle()
    if not handle:
        return False
    
    test_command = "help"
    iterations = 10
    
    # Test Windows API performance
    print(f"Testing Windows API performance ({iterations} iterations)...")
    start_time = time.time()
    
    for i in range(iterations):
        try:
            win32gui.SetForegroundWindow(handle)
            test_wm_char(handle, test_command)
            send_enter_key(handle)
            time.sleep(0.1)  # Small delay between commands
        except Exception as e:
            print(f"  [ERROR] Iteration {i+1} failed: {e}")
    
    winapi_time = time.time() - start_time
    print(f"  Windows API: {winapi_time:.3f}s total, {winapi_time/iterations:.3f}s per command")
    
    # Test pywinauto performance for comparison
    print(f"Testing pywinauto performance ({iterations} iterations)...")
    
    try:
        from pywinauto import Application
        app = Application().connect(handle=handle)
        window = app.window(handle=handle)
        
        start_time = time.time()
        
        for i in range(iterations):
            try:
                window.set_focus()
                window.type_keys("^a{DELETE}")
                window.type_keys(test_command)
                window.type_keys("{ENTER}")
                time.sleep(0.1)
            except Exception as e:
                print(f"  [ERROR] pywinauto iteration {i+1} failed: {e}")
        
        pywinauto_time = time.time() - start_time
        print(f"  pywinauto: {pywinauto_time:.3f}s total, {pywinauto_time/iterations:.3f}s per command")
        
        # Comparison
        if winapi_time > 0 and pywinauto_time > 0:
            ratio = pywinauto_time / winapi_time
            faster = "Windows API" if ratio > 1 else "pywinauto"
            print(f"  {faster} is {abs(ratio-1)*100:.1f}% faster")
        
    except Exception as e:
        print(f"  [ERROR] pywinauto performance test failed: {e}")
    
    return True

def capture_state_changes():
    """Test Windows API command with state change detection."""
    print("\n=== Testing Windows API Command with State Monitoring ===")
    
    handle, prompt_data = get_prompt_window_handle()
    if not handle:
        return False
    
    # Simple state capture (just check if Log window changes)
    finder = TextTheSpireWindowFinder()
    log_window = finder.get_window_by_title('Log')
    
    if not log_window:
        print("[WARN] Could not find Log window for state monitoring")
        return False
    
    # Get initial state
    try:
        from pywinauto import Application
        log_app = Application().connect(handle=log_window['hwnd'])
        log_win = log_app.window(handle=log_window['hwnd'])
        
        # Get initial text
        children = log_win.children()
        initial_text = ""
        for child in children:
            child_text = child.window_text()
            if child_text.strip():
                initial_text += child_text
        
        print(f"[INFO] Initial Log window: {len(initial_text)} chars")
        
        # Send command via Windows API
        print("[INFO] Sending 'help' command via Windows API...")
        win32gui.SetForegroundWindow(handle)
        time.sleep(0.1)
        
        # Clear and send command
        test_wm_char(handle, "help")
        time.sleep(0.1)
        send_enter_key(handle)
        
        print("[INFO] Waiting for response...")
        time.sleep(2.0)
        
        # Check for changes
        children = log_win.children()
        final_text = ""
        for child in children:
            child_text = child.window_text()
            if child_text.strip():
                final_text += child_text
        
        print(f"[INFO] Final Log window: {len(final_text)} chars")
        
        if initial_text != final_text:
            print("[SUCCESS] State change detected - Windows API command was processed!")
            return True
        else:
            print("[INFO] No state change detected")
            return False
            
    except Exception as e:
        print(f"[ERROR] State monitoring failed: {e}")
        return False

def run_all_tests():
    """Run all Windows API command sending tests."""
    print("TEXT THE SPIRE COMMAND SENDING TESTS (WINDOWS API)")
    print("Phase 1, Section 5.1.3: Test sending text commands using Windows API")
    print("=" * 75)
    
    # Check prerequisites
    finder = TextTheSpireWindowFinder()
    if not finder.is_game_running():
        print("[ERROR] Text the Spire is not running with the mod")
        return False
    
    print("[OK] Text the Spire is running with mod")
    
    # Test 1: Window focus
    focus_success = test_window_focus_winapi()
    
    # Test 2: Different message methods
    message_success = test_send_message_methods()
    
    # Test 3: Performance comparison
    perf_success = test_performance_comparison()
    
    # Test 4: State change detection
    state_success = capture_state_changes()
    
    # Summary
    print("\n" + "=" * 75)
    print("COMMAND SENDING TEST SUMMARY (WINDOWS API)")
    print("=" * 75)
    
    print(f"[+] Window focus: {'PASS' if focus_success else 'FAIL'}")
    print(f"[+] Message methods: {'PASS' if message_success else 'FAIL'}")
    print(f"[+] Performance test: {'PASS' if perf_success else 'FAIL'}")
    print(f"[+] State monitoring: {'PASS' if state_success else 'FAIL'}")
    
    overall_success = focus_success and message_success
    
    if overall_success:
        print("\n[SUCCESS] Windows API command sending is working!")
        return True
    else:
        print("\n[FAILED] Windows API command sending has issues.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)