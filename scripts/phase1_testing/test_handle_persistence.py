#!/usr/bin/env python3
"""
Test window handle persistence across Text the Spire game sessions.
This script helps determine if window handles remain stable when the game restarts.
"""

import time
import json
import os
from datetime import datetime
from find_text_spire_windows import find_text_spire_windows


def capture_window_handles():
    """Capture current window handles and metadata."""
    categorized = find_text_spire_windows()
    
    # Extract handle information
    handles_info = {}
    
    for category, windows in categorized.items():
        if windows:
            handles_info[category] = []
            for window in windows:
                handles_info[category].append({
                    'title': window['title'],
                    'handle': window['hwnd'],
                    'class_name': window['class_name'],
                    'size': f"{window['width']}x{window['height']}",
                    'process_id': window['process_id']
                })
    
    return handles_info


def save_handles_snapshot(handles_info, session_name):
    """Save handles to a JSON file for comparison."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"handles_{session_name}_{timestamp}.json"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    snapshot = {
        'timestamp': timestamp,
        'session_name': session_name,
        'handles': handles_info
    }
    
    with open(filepath, 'w') as f:
        json.dump(snapshot, f, indent=2)
    
    print(f"Saved handles snapshot: {filename}")
    return filepath


def compare_handle_snapshots(snapshot1_path, snapshot2_path):
    """Compare two handle snapshots to check for stability."""
    
    def load_snapshot(path):
        with open(path, 'r') as f:
            return json.load(f)
    
    snap1 = load_snapshot(snapshot1_path)
    snap2 = load_snapshot(snapshot2_path)
    
    print(f"\nCOMPARING SNAPSHOTS:")
    print(f"Session 1: {snap1['session_name']} at {snap1['timestamp']}")
    print(f"Session 2: {snap2['session_name']} at {snap2['timestamp']}")
    print("=" * 60)
    
    handles1 = snap1['handles']
    handles2 = snap2['handles']
    
    # Check each category
    all_stable = True
    
    for category in set(handles1.keys()) | set(handles2.keys()):
        print(f"\n{category.upper().replace('_', ' ')}:")
        
        if category not in handles1:
            print(f"  NEW CATEGORY in session 2")
            all_stable = False
            continue
        elif category not in handles2:
            print(f"  MISSING CATEGORY in session 2")
            all_stable = False
            continue
        
        windows1 = handles1[category]
        windows2 = handles2[category]
        
        if len(windows1) != len(windows2):
            print(f"  WINDOW COUNT CHANGED: {len(windows1)} -> {len(windows2)}")
            all_stable = False
        
        # Match windows by title
        for w1 in windows1:
            matching_w2 = next((w for w in windows2 if w['title'] == w1['title']), None)
            
            if not matching_w2:
                print(f"  MISSING WINDOW: '{w1['title']}'")
                all_stable = False
                continue
            
            # Compare handles
            if w1['handle'] == matching_w2['handle']:
                print(f"  ✓ '{w1['title']}': Handle STABLE ({w1['handle']})")
            else:
                print(f"  ✗ '{w1['title']}': Handle CHANGED ({w1['handle']} -> {matching_w2['handle']})")
                all_stable = False
            
            # Check other properties
            if w1['process_id'] != matching_w2['process_id']:
                print(f"    Process ID changed: {w1['process_id']} -> {matching_w2['process_id']}")
    
    print(f"\nOVERALL RESULT: {'HANDLES STABLE' if all_stable else 'HANDLES CHANGED'}")
    return all_stable


def interactive_test():
    """Interactive test for handle persistence."""
    print("TEXT THE SPIRE HANDLE PERSISTENCE TEST")
    print("=" * 40)
    print()
    print("This test will help determine if window handles remain stable")
    print("when Text the Spire is restarted.")
    print()
    
    # First snapshot
    print("STEP 1: Capture initial handles")
    print("Make sure Text the Spire with Text the Spire mod is running.")
    input("Press Enter when ready...")
    
    handles1 = capture_window_handles()
    
    if not any(handles1.values()):
        print("ERROR: No Text the Spire windows found!")
        print("Make sure the game and mod are running properly.")
        return
    
    snapshot1_path = save_handles_snapshot(handles1, "session1")
    
    print(f"\nFound {sum(len(windows) for windows in handles1.values())} windows:")
    for category, windows in handles1.items():
        if windows:
            print(f"  {category}: {len(windows)} windows")
    
    # Wait for restart
    print(f"\nSTEP 2: Restart the game")
    print("1. Close Text the Spire completely")
    print("2. Restart Text the Spire with the Text the Spire mod")
    print("3. Load the same save or start a new run")
    input("Press Enter when the game is running again...")
    
    # Second snapshot
    handles2 = capture_window_handles()
    
    if not any(handles2.values()):
        print("ERROR: No Text the Spire windows found after restart!")
        return
    
    snapshot2_path = save_handles_snapshot(handles2, "session2")
    
    # Compare
    handles_stable = compare_handle_snapshots(snapshot1_path, snapshot2_path)
    
    print(f"\nTEST CONCLUSION:")
    if handles_stable:
        print("✓ Window handles appear to be STABLE across sessions")
        print("  The same handles can be reused after game restart")
    else:
        print("✗ Window handles CHANGE across sessions")
        print("  Need to re-enumerate windows after each game restart")
    
    return handles_stable


def main():
    """Main function."""
    print("Window Handle Persistence Test")
    print("Usage: python test_handle_persistence.py")
    print()
    
    try:
        result = interactive_test()
        
        print(f"\nNEXT STEPS:")
        if result:
            print("- Handles are stable: Can cache handles during gameplay")
            print("- Test handle stability during gameplay next")
        else:
            print("- Handles change: Must re-enumerate after game restarts")
            print("- Create reliable window finder function")
            print("- Test handle stability during gameplay")
            
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
    except Exception as e:
        print(f"Test failed with error: {e}")


if __name__ == "__main__":
    main()