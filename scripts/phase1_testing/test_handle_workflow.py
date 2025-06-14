#!/usr/bin/env python3
"""
Demonstration of handle persistence testing workflow.
"""

import os
import glob
from capture_handles import capture_and_save_handles, compare_two_files


def demonstrate_workflow():
    """Show the handle persistence testing workflow."""
    print("HANDLE PERSISTENCE TESTING WORKFLOW")
    print("=" * 40)
    print()
    
    # Step 1: Capture current state
    print("STEP 1: Capturing current window handles...")
    first_capture = capture_and_save_handles("demo_session1")
    
    if not first_capture:
        print("Cannot proceed - Text the Spire not running")
        return
    
    print()
    print("STEP 2: Instructions for testing")
    print("To complete the handle persistence test:")
    print("1. Close Text the Spire completely")
    print("2. Restart Text the Spire with the Text the Spire mod")
    print("3. Load the same save or start a new run")
    print("4. Run: python capture_handles.py capture after_restart")
    print("5. Run: python capture_handles.py compare handles_demo_session1_*.json handles_after_restart_*.json")
    print()
    
    # Check if we have previous captures to compare
    before_files = glob.glob("handles_before_restart_*.json")
    after_files = glob.glob("handles_after_restart_*.json")
    
    if before_files and after_files:
        print("FOUND PREVIOUS CAPTURES - COMPARING:")
        print("=" * 40)
        compare_two_files(before_files[-1], after_files[-1])
    else:
        print("Previous captures not found. Follow the workflow above to test handle persistence.")


if __name__ == "__main__":
    demonstrate_workflow()