#!/usr/bin/env python3
"""
Quick stability check - takes a few snapshots to test handle stability.
"""

import time
from find_text_spire_windows import find_text_spire_windows


def take_snapshot():
    """Take a snapshot of current handles."""
    categorized = find_text_spire_windows()
    
    handles = {}
    for category, windows in categorized.items():
        if windows:
            handles[category] = [(w['title'], w['hwnd']) for w in windows]
    
    return handles


def compare_snapshots(snap1, snap2, label1="Snapshot 1", label2="Snapshot 2"):
    """Compare two snapshots."""
    print(f"\nComparing {label1} vs {label2}:")
    
    all_same = True
    
    for category in set(snap1.keys()) | set(snap2.keys()):
        if category not in snap1 or category not in snap2:
            print(f"  {category}: Category missing in one snapshot")
            all_same = False
            continue
        
        handles1 = dict(snap1[category])
        handles2 = dict(snap2[category])
        
        for title in set(handles1.keys()) | set(handles2.keys()):
            if title not in handles1 or title not in handles2:
                print(f"  {title}: Window missing in one snapshot")
                all_same = False
            elif handles1[title] != handles2[title]:
                print(f"  {title}: Handle changed ({handles1[title]} -> {handles2[title]})")
                all_same = False
    
    if all_same:
        print(f"  All handles IDENTICAL")
    
    return all_same


def main():
    """Take several snapshots to test stability."""
    print("QUICK HANDLE STABILITY CHECK")
    print("Taking 3 snapshots 10 seconds apart...")
    print("=" * 40)
    
    # Take first snapshot
    print("Taking snapshot 1...")
    snap1 = take_snapshot()
    
    if not snap1:
        print("ERROR: No Text the Spire windows found!")
        return
    
    total_windows = sum(len(windows) for windows in snap1.values())
    print(f"Found {total_windows} windows")
    
    # Wait and take second snapshot
    print("\nWaiting 10 seconds...")
    time.sleep(10)
    
    print("Taking snapshot 2...")
    snap2 = take_snapshot()
    
    # Wait and take third snapshot
    print("\nWaiting 10 seconds...")
    time.sleep(10)
    
    print("Taking snapshot 3...")
    snap3 = take_snapshot()
    
    # Compare all snapshots
    print("\nCOMPARING SNAPSHOTS:")
    print("=" * 30)
    
    stable12 = compare_snapshots(snap1, snap2, "Snapshot 1", "Snapshot 2")
    stable23 = compare_snapshots(snap2, snap3, "Snapshot 2", "Snapshot 3")
    stable13 = compare_snapshots(snap1, snap3, "Snapshot 1", "Snapshot 3")
    
    print(f"\nRESULT:")
    if stable12 and stable23 and stable13:
        print("[OK] HANDLES STABLE during gameplay")
        print("  Handles can be cached during active game sessions")
    else:
        print("[!!] HANDLES CHANGED during gameplay")
        print("  Handles need frequent re-enumeration")


if __name__ == "__main__":
    main()