#!/usr/bin/env python3
"""
Test Text the Spire window detection in different states.
Tests detection when game is running vs not running.
"""

import time
import sys
from find_text_spire_windows import find_text_spire_windows, print_categorized_windows


def test_detection_state():
    """Test and report current window detection state."""
    print("Testing Text the Spire window detection...")
    print("=" * 50)
    
    categorized = find_text_spire_windows()
    
    # Count windows by category
    counts = {
        'main_game': len(categorized['main_game_window']),
        'prompt': len(categorized['prompt_window']),
        'game_state': len(categorized['game_state_windows']),
        'mod_launcher': len(categorized['mod_launcher']),
        'other': len(categorized['other_spire_windows'])
    }
    
    total_windows = sum(counts.values())
    
    print(f"DETECTION RESULTS:")
    print(f"Total Text the Spire windows found: {total_windows}")
    for category, count in counts.items():
        print(f"  {category.replace('_', ' ').title()}: {count}")
    
    # Determine game state
    if counts['main_game'] > 0 and counts['game_state'] > 0:
        state = "GAME RUNNING WITH TEXT THE SPIRE MOD"
    elif counts['main_game'] > 0:
        state = "GAME RUNNING WITHOUT TEXT THE SPIRE MOD"
    elif counts['mod_launcher'] > 0:
        state = "MOD LAUNCHER ONLY"
    else:
        state = "GAME NOT RUNNING"
    
    print(f"\nDETECTED STATE: {state}")
    
    if total_windows > 0:
        print(f"\nDETAILED WINDOW INFO:")
        print_categorized_windows(categorized)
    
    return state, counts


def main():
    """Main function to test detection states."""
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        print("Continuous monitoring mode. Press Ctrl+C to stop.")
        print("Start/stop Text the Spire to see detection changes.")
        
        try:
            while True:
                state, counts = test_detection_state()
                print(f"\n[{time.strftime('%H:%M:%S')}] Current state: {state}")
                print("-" * 50)
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    else:
        print("Single detection test:")
        print("Usage: python test_detection_states.py [--continuous]")
        print()
        test_detection_state()
        print("\nTo monitor changes, run with --continuous flag")


if __name__ == "__main__":
    main()