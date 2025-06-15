#!/usr/bin/env python3
"""
Test script for Text the Spire command execution and response detection.
Phase 1, Section 5.1.4: Test command execution and response detection

This script tests:
1. Different types of commands and their expected responses
2. Reliable response detection from game state windows
3. Command timing and response latency
4. Error handling for invalid commands

Based on learnings from previous sections:
- pywinauto is the most reliable approach for command sending
- Game state changes appear in Log window primarily
- Commands like 'help', 'status', 'info' are working
- Need to test actual game commands during combat/navigation
"""

import sys
import os
import time
from pywinauto import Application

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from reliable_window_finder import TextTheSpireWindowFinder

class CommandTester:
    """Test class for command execution and response detection."""
    
    def __init__(self):
        self.finder = TextTheSpireWindowFinder()
        self.prompt_window = None
        self.connected = False
        
    def connect(self):
        """Connect to the Text the Spire windows."""
        if not self.finder.is_game_running():
            print("[ERROR] Text the Spire is not running with the mod")
            return False
        
        prompt_data = self.finder.get_prompt_window()
        if not prompt_data:
            print("[ERROR] Prompt window not found")
            return False
        
        try:
            app = Application().connect(handle=prompt_data['hwnd'])
            self.prompt_window = app.window(handle=prompt_data['hwnd'])
            self.connected = True
            print(f"[OK] Connected to prompt window (handle: {prompt_data['hwnd']})")
            return True
        except Exception as e:
            print(f"[ERROR] Could not connect to prompt window: {e}")
            return False
    
    def send_command(self, command, wait_time=1.0):
        """Send a command and wait for response."""
        if not self.connected:
            print("[ERROR] Not connected to prompt window")
            return False
        
        try:
            # Focus and clear
            self.prompt_window.set_focus()
            time.sleep(0.05)
            self.prompt_window.type_keys("^a{DELETE}")
            time.sleep(0.05)
            
            # Send command
            self.prompt_window.type_keys(command)
            time.sleep(0.05)
            self.prompt_window.type_keys("{ENTER}")
            
            # Wait for response
            time.sleep(wait_time)
            
            print(f"[OK] Command '{command}' sent successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to send command '{command}': {e}")
            return False
    
    def capture_all_window_states(self):
        """Capture text from all game state windows."""
        states = {}
        game_state_windows = self.finder.get_game_state_windows()
        
        for window_data in game_state_windows:
            title = window_data['title']
            handle = window_data['hwnd']
            
            try:
                app = Application().connect(handle=handle)
                window = app.window(handle=handle)
                
                # Extract text using proven method
                children = window.children()
                all_text = []
                for child in children:
                    child_text = child.window_text()
                    if child_text.strip():
                        all_text.append(child_text)
                
                window_text = '\n'.join(all_text).strip()
                states[title] = {
                    'text': window_text,
                    'lines': len(window_text.split('\n')) if window_text else 0,
                    'chars': len(window_text)
                }
                
            except Exception as e:
                print(f"[WARN] Could not read {title} window: {e}")
                states[title] = {'text': None, 'lines': 0, 'chars': 0}
        
        return states
    
    def compare_states(self, before, after, show_details=False):
        """Compare two window states and return changes."""
        changes = {}
        
        for window_title in before.keys():
            before_state = before.get(window_title, {})
            after_state = after.get(window_title, {})
            
            before_text = before_state.get('text', '')
            after_text = after_state.get('text', '')
            
            if before_text != after_text:
                changes[window_title] = {
                    'changed': True,
                    'before_chars': before_state.get('chars', 0),
                    'after_chars': after_state.get('chars', 0),
                    'before_lines': before_state.get('lines', 0),
                    'after_lines': after_state.get('lines', 0),
                }
                
                if show_details and before_text and after_text:
                    # Show first few lines of difference
                    before_lines = before_text.split('\n')[:3]
                    after_lines = after_text.split('\n')[:3]
                    changes[window_title]['sample_before'] = before_lines
                    changes[window_title]['sample_after'] = after_lines
                    
            else:
                changes[window_title] = {'changed': False}
        
        return changes

def test_basic_commands():
    """Test basic information commands."""
    print("=== Testing Basic Commands ===")
    
    tester = CommandTester()
    if not tester.connect():
        return False
    
    # Test different basic commands
    basic_commands = [
        ("help", "Should show available commands"),
        ("status", "Should show current game status"),
        ("info", "Should show game information"), 
        ("state", "Should show current state"),
        ("player", "Should show player information"),
    ]
    
    results = {}
    
    for command, description in basic_commands:
        print(f"\n--- Testing '{command}' command ---")
        print(f"Expected: {description}")
        
        # Capture state before
        before = tester.capture_all_window_states()
        
        # Send command
        success = tester.send_command(command, wait_time=1.5)
        
        if success:
            # Capture state after
            after = tester.capture_all_window_states()
            
            # Compare states
            changes = tester.compare_states(before, after, show_details=True)
            
            # Analyze changes
            changed_windows = [w for w, c in changes.items() if c.get('changed', False)]
            
            if changed_windows:
                print(f"[SUCCESS] Command '{command}' caused changes in: {', '.join(changed_windows)}")
                
                for window in changed_windows:
                    change_info = changes[window]
                    print(f"  {window}: {change_info['before_chars']} -> {change_info['after_chars']} chars")
                    
                    if 'sample_before' in change_info and 'sample_after' in change_info:
                        print(f"    Sample change: {change_info['sample_before']} -> {change_info['sample_after']}")
                
                results[command] = 'SUCCESS'
            else:
                print(f"[INFO] Command '{command}' sent but no window changes detected")
                results[command] = 'NO_CHANGE'
        else:
            results[command] = 'FAILED'
    
    return results

def test_invalid_commands():
    """Test invalid commands and error handling."""
    print("\n=== Testing Invalid Commands ===")
    
    tester = CommandTester()
    if not tester.connect():
        return False
    
    # Test invalid commands
    invalid_commands = [
        "invalidcommandxyz",
        "asdfasdf",
        "quit",
        "exit",
    ]
    
    results = {}
    
    for command in invalid_commands:
        print(f"\n--- Testing invalid command '{command}' ---")
        
        # Capture state before
        before = tester.capture_all_window_states()
        
        # Send command
        success = tester.send_command(command, wait_time=1.0)
        
        if success:
            # Capture state after
            after = tester.capture_all_window_states()
            
            # Compare states
            changes = tester.compare_states(before, after)
            changed_windows = [w for w, c in changes.items() if c.get('changed', False)]
            
            if changed_windows:
                print(f"[INFO] Invalid command '{command}' still caused changes in: {', '.join(changed_windows)}")
                results[command] = 'RESPONSE'
            else:
                print(f"[INFO] Invalid command '{command}' was ignored (no changes)")
                results[command] = 'IGNORED'
        else:
            results[command] = 'FAILED'
    
    return results

def test_response_timing():
    """Test response timing for different commands."""
    print("\n=== Testing Response Timing ===")
    
    tester = CommandTester()
    if not tester.connect():
        return False
    
    # Test with different wait times
    test_command = "help"
    wait_times = [0.1, 0.5, 1.0, 2.0]
    
    results = {}
    
    for wait_time in wait_times:
        print(f"\n--- Testing with {wait_time}s wait time ---")
        
        # Capture state before
        before = tester.capture_all_window_states()
        
        # Send command with specific wait time
        success = tester.send_command(test_command, wait_time=wait_time)
        
        if success:
            # Capture state after
            after = tester.capture_all_window_states()
            
            # Compare states
            changes = tester.compare_states(before, after)
            changed_windows = [w for w, c in changes.items() if c.get('changed', False)]
            
            if changed_windows:
                print(f"[OK] Response detected after {wait_time}s wait")
                results[wait_time] = 'DETECTED'
            else:
                print(f"[INFO] No response detected after {wait_time}s wait")
                results[wait_time] = 'NOT_DETECTED'
        else:
            results[wait_time] = 'FAILED'
    
    # Determine minimum response time
    detected_times = [t for t, r in results.items() if r == 'DETECTED']
    if detected_times:
        min_time = min(detected_times)
        print(f"\n[INFO] Minimum response time: {min_time}s")
    
    return results

def test_game_context_commands():
    """Test commands that might be context-dependent."""
    print("\n=== Testing Game Context Commands ===")
    
    tester = CommandTester()
    if not tester.connect():
        return False
    
    # Commands that might work differently based on game state
    context_commands = [
        ("play", "Might work in combat"),
        ("end", "Might end turn in combat"),
        ("card", "Might show card information"),
        ("hand", "Might show hand information"),
        ("deck", "Might show deck information"),
        ("map", "Might show map in navigation"),
    ]
    
    results = {}
    
    for command, description in context_commands:
        print(f"\n--- Testing context command '{command}' ---")
        print(f"Note: {description}")
        
        # Capture state before
        before = tester.capture_all_window_states()
        
        # Send command
        success = tester.send_command(command, wait_time=1.5)
        
        if success:
            # Capture state after
            after = tester.capture_all_window_states()
            
            # Compare states
            changes = tester.compare_states(before, after)
            changed_windows = [w for w, c in changes.items() if c.get('changed', False)]
            
            if changed_windows:
                print(f"[SUCCESS] Context command '{command}' worked: {', '.join(changed_windows)}")
                results[command] = 'SUCCESS'
            else:
                print(f"[INFO] Context command '{command}' sent but no response")
                results[command] = 'NO_RESPONSE'
        else:
            results[command] = 'FAILED'
    
    return results

def run_all_tests():
    """Run all command execution and response tests."""
    print("TEXT THE SPIRE COMMAND EXECUTION AND RESPONSE TESTING")
    print("Phase 1, Section 5.1.4: Test command execution and response detection")
    print("=" * 80)
    
    # Test 1: Basic commands
    basic_results = test_basic_commands()
    
    # Test 2: Invalid commands
    invalid_results = test_invalid_commands()
    
    # Test 3: Response timing
    timing_results = test_response_timing()
    
    # Test 4: Game context commands
    context_results = test_game_context_commands()
    
    # Summary
    print("\n" + "=" * 80)
    print("COMMAND EXECUTION TEST SUMMARY")
    print("=" * 80)
    
    print("\nBasic Commands:")
    for cmd, result in basic_results.items():
        print(f"  {cmd}: {result}")
    
    print("\nInvalid Commands:")
    for cmd, result in invalid_results.items():
        print(f"  {cmd}: {result}")
    
    print("\nTiming Tests:")
    for wait_time, result in timing_results.items():
        print(f"  {wait_time}s: {result}")
    
    print("\nContext Commands:")
    for cmd, result in context_results.items():
        print(f"  {cmd}: {result}")
    
    # Overall assessment
    successful_basic = sum(1 for r in basic_results.values() if r == 'SUCCESS')
    total_basic = len(basic_results)
    
    print(f"\n[INFO] Basic command success rate: {successful_basic}/{total_basic}")
    
    if successful_basic > 0:
        print("\n[SUCCESS] Command execution and response detection is working!")
        print("The Text the Spire mod accepts commands and provides feedback through window updates.")
        return True
    else:
        print("\n[FAILED] Command execution has issues.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)