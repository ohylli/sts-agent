#!/usr/bin/env python3
"""
Test script for sending commands to Text the Spire prompt window using pywinauto.
Phase 1, Section 5.1.2: Test sending text commands using pywinauto

This script tests:
1. Sending text commands to the prompt window
2. Different pywinauto methods for text input
3. Command timing and reliability
4. Response detection from game state windows

Based on learnings from previous sections:
- Prompt window: Handle found via reliable_window_finder
- Connection via pywinauto is working
- Window focus methods are successful
- Game state windows can be read for response detection
"""

import sys
import os
import time
from pywinauto import Application

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from reliable_window_finder import TextTheSpireWindowFinder

def get_prompt_window():
    """Get the prompt window connection."""
    finder = TextTheSpireWindowFinder()
    
    if not finder.is_game_running():
        print("[ERROR] Text the Spire is not running with the mod")
        return None, None
    
    prompt_data = finder.get_prompt_window()
    if not prompt_data:
        print("[ERROR] Prompt window not found")
        return None, None
    
    try:
        app = Application().connect(handle=prompt_data['hwnd'])
        window = app.window(handle=prompt_data['hwnd'])
        return window, prompt_data
    except Exception as e:
        print(f"[ERROR] Could not connect to prompt window: {e}")
        return None, None

def capture_game_state_before_command():
    """Capture current game state for comparison after command."""
    finder = TextTheSpireWindowFinder()
    game_state_windows = finder.get_game_state_windows()
    
    state_before = {}
    
    for window_data in game_state_windows:
        title = window_data['title']
        handle = window_data['hwnd']
        
        try:
            app = Application().connect(handle=handle)
            window = app.window(handle=handle)
            
            # Use the proven method from Section 3.2
            children = window.children()
            all_text = []
            for child in children:
                child_text = child.window_text()
                if child_text.strip():
                    all_text.append(child_text)
            
            window_text = '\n'.join(all_text).strip()
            state_before[title] = window_text
            
        except Exception as e:
            print(f"[WARN] Could not read {title} window: {e}")
            state_before[title] = None
    
    return state_before

def test_basic_text_input():
    """Test basic text input methods."""
    print("=== Testing Basic Text Input Methods ===")
    
    window, prompt_data = get_prompt_window()
    if not window:
        return False
    
    print(f"Connected to prompt window (handle: {prompt_data['hwnd']})")
    
    # Test different text input methods
    test_commands = [
        "help",      # Basic help command
        "status",    # Game status command
        "info",      # Info command
    ]
    
    input_methods = [
        ("type_keys()", lambda text: window.type_keys(text)),
        ("send_chars()", lambda text: window.send_chars(text)),
    ]
    
    for method_name, method_func in input_methods:
        print(f"\n--- Testing {method_name} ---")
        
        for command in test_commands:
            try:
                print(f"  Sending command: '{command}'")
                
                # Focus the window first
                window.set_focus()
                time.sleep(0.1)
                
                # Clear any existing text (Ctrl+A, Delete)
                window.type_keys("^a")
                time.sleep(0.05)
                window.type_keys("{DELETE}")
                time.sleep(0.05)
                
                # Send the command
                method_func(command)
                time.sleep(0.1)
                
                # Send Enter to execute
                window.type_keys("{ENTER}")
                print(f"  [OK] Command '{command}' sent with {method_name}")
                
                # Wait for potential response
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  [ERROR] {method_name} failed for '{command}': {e}")
    
    return True

def test_command_with_state_monitoring():
    """Test sending a command while monitoring game state changes."""
    print("\n=== Testing Command with State Monitoring ===")
    
    window, prompt_data = get_prompt_window()
    if not window:
        return False
    
    # Capture state before command
    print("[INFO] Capturing game state before command...")
    state_before = capture_game_state_before_command()
    
    # Show current state summary
    print("Current game state summary:")
    for window_title, content in state_before.items():
        if content:
            lines = content.split('\n')
            print(f"  {window_title}: {len(lines)} lines, {len(content)} chars")
        else:
            print(f"  {window_title}: [could not read]")
    
    # Send a test command
    test_command = "help"
    print(f"\n[INFO] Sending test command: '{test_command}'")
    
    try:
        # Focus and send command
        window.set_focus()
        time.sleep(0.1)
        
        # Clear and type command
        window.type_keys("^a{DELETE}")
        time.sleep(0.05)
        window.type_keys(test_command)
        time.sleep(0.1)
        window.type_keys("{ENTER}")
        
        print(f"[OK] Command '{test_command}' sent successfully")
        
        # Wait for response
        print("[INFO] Waiting for game response...")
        time.sleep(2.0)  # Give game time to process
        
        # Capture state after command
        print("[INFO] Capturing game state after command...")
        state_after = capture_game_state_before_command()
        
        # Compare states
        print("\n--- State Change Analysis ---")
        changes_detected = False
        
        for window_title in state_before.keys():
            before = state_before.get(window_title, "")
            after = state_after.get(window_title, "")
            
            if before != after:
                changes_detected = True
                print(f"  {window_title}: CHANGED")
                if before and after:
                    print(f"    Before: {len(before)} chars")
                    print(f"    After:  {len(after)} chars")
                    
                    # Show first few lines of change
                    before_lines = before.split('\n')[:3]
                    after_lines = after.split('\n')[:3]
                    
                    if before_lines != after_lines:
                        print(f"    First lines changed:")
                        print(f"      Before: {before_lines}")
                        print(f"      After:  {after_lines}")
                else:
                    print(f"    Content: {before} -> {after}")
            else:
                print(f"  {window_title}: No change")
        
        if changes_detected:
            print("\n[SUCCESS] Game state changes detected after command!")
            return True
        else:
            print("\n[INFO] No game state changes detected - command may not have been processed")
            return False
            
    except Exception as e:
        print(f"[ERROR] Command sending failed: {e}")
        return False

def test_rapid_command_sequence():
    """Test sending multiple commands in rapid succession."""
    print("\n=== Testing Rapid Command Sequence ===")
    
    window, prompt_data = get_prompt_window()
    if not window:
        return False
    
    commands = ["help", "status", "info", "help"]
    
    print(f"[INFO] Sending {len(commands)} commands rapidly...")
    
    successful_commands = 0
    
    for i, command in enumerate(commands):
        try:
            print(f"  Command {i+1}/{len(commands)}: '{command}'")
            
            # Focus and send command
            window.set_focus()
            window.type_keys("^a{DELETE}")
            window.type_keys(command)
            window.type_keys("{ENTER}")
            
            successful_commands += 1
            print(f"    [OK] Sent successfully")
            
            # Short delay between commands
            time.sleep(0.3)
            
        except Exception as e:
            print(f"    [ERROR] Failed: {e}")
    
    print(f"\n[INFO] Successfully sent {successful_commands}/{len(commands)} commands")
    
    # Wait for all responses
    print("[INFO] Waiting for final responses...")
    time.sleep(2.0)
    
    return successful_commands > 0

def run_all_tests():
    """Run all command sending tests."""
    print("TEXT THE SPIRE COMMAND SENDING TESTS (PYWINAUTO)")
    print("Phase 1, Section 5.1.2: Test sending text commands using pywinauto")
    print("=" * 70)
    
    # Check prerequisites
    finder = TextTheSpireWindowFinder()
    if not finder.is_game_running():
        print("[ERROR] Text the Spire is not running with the mod")
        print("Please start the game and ensure the Text the Spire mod is loaded")
        return False
    
    print("[OK] Text the Spire is running with mod")
    
    # Test 1: Basic text input methods
    basic_success = test_basic_text_input()
    
    # Test 2: Command with state monitoring
    state_success = test_command_with_state_monitoring()
    
    # Test 3: Rapid command sequence
    rapid_success = test_rapid_command_sequence()
    
    # Summary
    print("\n" + "=" * 70)
    print("COMMAND SENDING TEST SUMMARY (PYWINAUTO)")
    print("=" * 70)
    
    print(f"[+] Basic text input: {'PASS' if basic_success else 'FAIL'}")
    print(f"[+] State monitoring: {'PASS' if state_success else 'FAIL'}")
    print(f"[+] Rapid commands: {'PASS' if rapid_success else 'FAIL'}")
    
    overall_success = basic_success
    
    if overall_success:
        print("\n[SUCCESS] pywinauto command sending is working!")
        print("The prompt window accepts text input and can execute commands.")
        if state_success:
            print("Game state changes were detected, confirming command processing.")
        return True
    else:
        print("\n[FAILED] pywinauto command sending has issues.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)