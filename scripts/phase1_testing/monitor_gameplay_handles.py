#!/usr/bin/env python3
"""
Monitor window handle stability during gameplay.
Tests if handles remain stable while playing (without restarting the game).
"""

import time
from datetime import datetime
from find_text_spire_windows import find_text_spire_windows


def capture_handle_snapshot():
    """Capture a quick snapshot of current handles."""
    categorized = find_text_spire_windows()
    
    snapshot = {}
    for category, windows in categorized.items():
        if windows:
            snapshot[category] = [(w['title'], w['hwnd']) for w in windows]
    
    return snapshot


def compare_snapshots(snap1, snap2):
    """Compare two handle snapshots."""
    changes = []
    
    for category in set(snap1.keys()) | set(snap2.keys()):
        if category not in snap1:
            changes.append(f"NEW: {category}")
            continue
        elif category not in snap2:
            changes.append(f"REMOVED: {category}")
            continue
        
        # Compare handles in this category
        handles1 = {title: handle for title, handle in snap1[category]}
        handles2 = {title: handle for title, handle in snap2[category]}
        
        for title in set(handles1.keys()) | set(handles2.keys()):
            if title not in handles1:
                changes.append(f"NEW WINDOW: {title}")
            elif title not in handles2:
                changes.append(f"REMOVED WINDOW: {title}")
            elif handles1[title] != handles2[title]:
                changes.append(f"CHANGED: {title} ({handles1[title]} -> {handles2[title]})")
    
    return changes


def monitor_gameplay_stability(duration_minutes=5, check_interval=30):
    """Monitor handle stability during gameplay."""
    print(f"MONITORING HANDLE STABILITY DURING GAMEPLAY")
    print(f"Duration: {duration_minutes} minutes")
    print(f"Check interval: {check_interval} seconds")
    print("=" * 50)
    
    # Initial snapshot
    print("Taking initial snapshot...")
    initial_snapshot = capture_handle_snapshot()
    
    if not initial_snapshot:
        print("ERROR: No Text the Spire windows found!")
        return False
    
    total_windows = sum(len(windows) for windows in initial_snapshot.values())
    print(f"Monitoring {total_windows} windows across {len(initial_snapshot)} categories")
    print()
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    check_count = 1
    all_stable = True
    
    print("Monitor started. Play the game normally...")
    print("(The script will check handles periodically)")
    print()
    
    try:
        while time.time() < end_time:
            time.sleep(check_interval)
            
            current_time = datetime.now().strftime("%H:%M:%S")
            current_snapshot = capture_handle_snapshot()
            
            if not current_snapshot:
                print(f"[{current_time}] WARNING: No windows found - game may have closed")
                continue
            
            changes = compare_snapshots(initial_snapshot, current_snapshot)
            
            if changes:
                print(f"[{current_time}] CHECK #{check_count}: CHANGES DETECTED")
                for change in changes:
                    print(f"  {change}")
                all_stable = False
            else:
                print(f"[{current_time}] CHECK #{check_count}: All handles STABLE")
            
            check_count += 1
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    
    print(f"\nMONITORING COMPLETE")
    print(f"Checks performed: {check_count - 1}")
    
    if all_stable:
        print("✓ RESULT: Handles remained STABLE during gameplay")
        print("  This means handles can be cached during active sessions")
    else:
        print("✗ RESULT: Handles CHANGED during gameplay")
        print("  This means handles need to be re-enumerated frequently")
    
    return all_stable


def quick_stability_test():
    """Quick test of handle stability over 2 minutes."""
    print("QUICK GAMEPLAY STABILITY TEST")
    print("Testing handle stability over 2 minutes...")
    print("Play the game normally (move between screens, play cards, etc.)")
    print()
    
    return monitor_gameplay_stability(duration_minutes=2, check_interval=20)


def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_stability_test()
    else:
        print("Gameplay Handle Stability Monitor")
        print("Usage:")
        print("  python monitor_gameplay_handles.py          # 5-minute monitoring")
        print("  python monitor_gameplay_handles.py --quick  # 2-minute quick test")
        print()
        
        choice = input("Run quick test (2 min) or full test (5 min)? [q/f]: ").lower()
        if choice == 'q':
            quick_stability_test()
        else:
            monitor_gameplay_stability()


if __name__ == "__main__":
    main()