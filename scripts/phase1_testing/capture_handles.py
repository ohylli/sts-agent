#!/usr/bin/env python3
"""
Capture current window handles for persistence testing.
Run this script before and after restarting Text the Spire to compare handles.
"""

import json
import os
from datetime import datetime
from find_text_spire_windows import find_text_spire_windows


def capture_and_save_handles(session_name="session"):
    """Capture current handles and save to file."""
    print(f"Capturing handles for {session_name}...")
    
    categorized = find_text_spire_windows()
    
    # Extract handle information
    handles_info = {}
    total_windows = 0
    
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
            total_windows += len(windows)
    
    if total_windows == 0:
        print("ERROR: No Text the Spire windows found!")
        print("Make sure Text the Spire with Text the Spire mod is running.")
        return None
    
    # Save to file
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
    
    print(f"[OK] Captured {total_windows} windows:")
    for category, windows in handles_info.items():
        print(f"  {category.replace('_', ' ').title()}: {len(windows)}")
    
    print(f"[OK] Saved to: {filename}")
    return filepath


def compare_two_files(file1, file2):
    """Compare two handle files."""
    def load_snapshot(path):
        with open(path, 'r') as f:
            return json.load(f)
    
    try:
        snap1 = load_snapshot(file1)
        snap2 = load_snapshot(file2)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return
    
    print(f"\nCOMPARING HANDLES:")
    print(f"File 1: {snap1['session_name']} ({snap1['timestamp']})")
    print(f"File 2: {snap2['session_name']} ({snap2['timestamp']})")
    print("=" * 50)
    
    handles1 = snap1['handles']
    handles2 = snap2['handles']
    
    all_stable = True
    
    for category in set(handles1.keys()) | set(handles2.keys()):
        print(f"\n{category.upper().replace('_', ' ')}:")
        
        if category not in handles1 or category not in handles2:
            print(f"  Category missing in one session")
            all_stable = False
            continue
        
        windows1 = handles1[category]
        windows2 = handles2[category]
        
        # Match by title and compare handles
        for w1 in windows1:
            matching = next((w for w in windows2 if w['title'] == w1['title']), None)
            if matching:
                if w1['handle'] == matching['handle']:
                    print(f"  [OK] {w1['title']}: STABLE ({w1['handle']})")
                else:
                    print(f"  [!!] {w1['title']}: CHANGED ({w1['handle']} -> {matching['handle']})")
                    all_stable = False
            else:
                print(f"  ? {w1['title']}: Not found in second session")
                all_stable = False
    
    print(f"\nRESULT: Handles are {'STABLE' if all_stable else 'UNSTABLE'}")
    return all_stable


def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Handle Persistence Testing Tool")
        print("Usage:")
        print("  python capture_handles.py capture <session_name>")
        print("  python capture_handles.py compare <file1> <file2>")
        print("\nExample workflow:")
        print("  1. python capture_handles.py capture before_restart")
        print("  2. [Restart Text the Spire]")
        print("  3. python capture_handles.py capture after_restart")
        print("  4. python capture_handles.py compare handles_before_restart_*.json handles_after_restart_*.json")
        return
    
    command = sys.argv[1]
    
    if command == "capture":
        session_name = sys.argv[2] if len(sys.argv) > 2 else "session"
        capture_and_save_handles(session_name)
    
    elif command == "compare":
        if len(sys.argv) < 4:
            print("Usage: python capture_handles.py compare <file1> <file2>")
            return
        compare_two_files(sys.argv[2], sys.argv[3])
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()