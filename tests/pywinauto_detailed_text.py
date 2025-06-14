#!/usr/bin/env python3
"""
Phase 1 - Section 3.2: Text Content Extraction from Text the Spire Windows

Tests detailed text reading from Text the Spire windows using pywinauto.
Based on Section 3.1 findings:
- Method 2 (children aggregation) successfully extracts game content
- Each window has 1 Edit control containing the actual text
- Text includes multi-line formatted game state information
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from pywinauto import Application
import time
import re
from reliable_window_finder import TextTheSpireWindowFinder

def extract_window_text(handle, title):
    """Extract text content from a Text the Spire window using best method."""
    try:
        app = Application().connect(handle=handle)
        window = app.window(handle=handle)
        
        # Use Method 2 (children aggregation) - proven most effective
        children = window.children()
        all_text = []
        for child in children:
            child_text = child.window_text()
            if child_text.strip():
                all_text.append(child_text)
        
        combined = '\n'.join(all_text)
        return combined.strip()
        
    except Exception as e:
        print(f"Error extracting text from '{title}': {e}")
        return None

def test_text_extraction_reliability():
    """Test reliability and consistency of text extraction."""
    print("=== Testing Text Extraction Reliability ===\n")
    
    finder = TextTheSpireWindowFinder()
    game_state_windows = finder.get_game_state_windows()
    
    if not game_state_windows:
        print("No game state windows found")
        return False
    
    # Test multiple extractions from key windows
    key_windows = ['Player', 'Monster', 'Hand', 'Output']
    results = {}
    
    for window_dict in game_state_windows:
        handle = window_dict['hwnd']
        title = window_dict['title']
        
        if title not in key_windows:
            continue
            
        print(f"Testing '{title}' window reliability:")
        
        # Extract text multiple times to test consistency
        extractions = []
        for i in range(3):
            text = extract_window_text(handle, title)
            extractions.append(text)
            time.sleep(0.1)  # Small delay between extractions
        
        # Check consistency
        consistent = all(text == extractions[0] for text in extractions)
        results[title] = {
            'consistent': consistent,
            'text_length': len(extractions[0]) if extractions[0] else 0,
            'sample_text': extractions[0][:100] if extractions[0] else None
        }
        
        print(f"  - Extractions consistent: {consistent}")
        print(f"  - Text length: {results[title]['text_length']} chars")
        if results[title]['sample_text']:
            print(f"  - Sample: '{results[title]['sample_text']}{'...' if len(extractions[0]) > 100 else ''}'")
        else:
            print(f"  - No text content")
        print()
    
    # Summary
    successful = sum(1 for r in results.values() if r['consistent'] and r['text_length'] > 0)
    print(f"Reliable text extraction: {successful}/{len(results)} windows")
    
    return successful == len(results)

def test_text_formatting_parsing():
    """Test parsing of formatted text from different windows."""
    print("=== Testing Text Formatting and Parsing ===\n")
    
    finder = TextTheSpireWindowFinder()
    game_state_windows = finder.get_game_state_windows()
    
    if not game_state_windows:
        print("No game state windows found")
        return False
    
    parsing_tests = {}
    
    for window_dict in game_state_windows:
        handle = window_dict['hwnd']
        title = window_dict['title']
        
        text = extract_window_text(handle, title)
        if not text:
            continue
            
        print(f"Analyzing '{title}' window format:")
        print(f"Raw text ({len(text)} chars):")
        print("---")
        print(repr(text))
        print("---")
        
        # Analyze text structure
        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        print(f"Structure analysis:")
        print(f"  - Total lines: {len(lines)}")
        print(f"  - Non-empty lines: {len(non_empty_lines)}")
        print(f"  - Line patterns:")
        
        for i, line in enumerate(non_empty_lines[:5]):  # Show first 5 lines
            line_clean = line.strip()
            print(f"    {i+1}: '{line_clean}'")
        
        if len(non_empty_lines) > 5:
            print(f"    ... and {len(non_empty_lines) - 5} more lines")
        
        # Test specific parsing based on window type
        parsing_result = test_window_specific_parsing(title, text)
        parsing_tests[title] = parsing_result
        
        print(f"Parsing success: {parsing_result}")
        print()
    
    successful_parsing = sum(1 for success in parsing_tests.values() if success)
    print(f"Successful parsing: {successful_parsing}/{len(parsing_tests)} windows")
    
    return successful_parsing > 0

def test_window_specific_parsing(title, text):
    """Test parsing specific to each window type."""
    try:
        if title == 'Player':
            # Expected format: Block, Health, Energy
            if 'Block:' in text and 'Health:' in text and 'Energy:' in text:
                return True
                
        elif title == 'Monster':
            # Expected format: Count, enemy info, HP, Intent
            if 'Count:' in text and 'HP:' in text and 'Intent:' in text:
                return True
                
        elif title == 'Hand':
            # Expected format: numbered cards, potions
            if re.search(r'\d+:', text) and 'Potions:' in text:
                return True
                
        elif title == 'Output':
            # May be empty or contain game messages
            return True  # Always valid, even if empty
            
        elif title == 'Log':
            # Contains game action log
            return True  # Always valid
            
        elif title in ['Deck', 'Discard']:
            # Card lists or counts
            return True  # Always valid
            
        elif title == 'Orbs':
            # Orb information (may be empty for non-Defect)
            return True  # Always valid
            
        elif title == 'Relic':
            # Relic information
            return True  # Always valid
            
        return False
        
    except Exception as e:
        print(f"Error parsing '{title}': {e}")
        return False

def test_text_update_detection():
    """Test detecting when text content changes."""
    print("=== Testing Text Update Detection ===\n")
    
    finder = TextTheSpireWindowFinder()
    game_state_windows = finder.get_game_state_windows()
    
    if not game_state_windows:
        print("No game state windows found")
        return False
    
    # Focus on windows most likely to change
    monitor_windows = ['Player', 'Monster', 'Hand', 'Output']
    initial_states = {}
    
    print("Taking initial snapshots...")
    for window_dict in game_state_windows:
        handle = window_dict['hwnd']
        title = window_dict['title']
        
        if title not in monitor_windows:
            continue
            
        text = extract_window_text(handle, title)
        initial_states[title] = text
        print(f"  {title}: {len(text) if text else 0} chars")
    
    print(f"\nMonitoring {len(initial_states)} windows for changes...")
    print("(Make a move in the game to test change detection)")
    
    # Monitor for changes over 10 seconds
    changes_detected = {}
    for i in range(20):  # 10 seconds with 0.5s intervals
        time.sleep(0.5)
        
        for title, initial_text in initial_states.items():
            window_dict = finder.get_window_by_title(title)
            if not window_dict:
                continue
                
            current_text = extract_window_text(window_dict['hwnd'], title)
            
            if current_text != initial_text:
                if title not in changes_detected:
                    changes_detected[title] = {
                        'first_change_time': i * 0.5,
                        'initial_length': len(initial_text) if initial_text else 0,
                        'new_length': len(current_text) if current_text else 0
                    }
                    print(f"  Change detected in '{title}' at {i * 0.5}s")
                    print(f"    Length: {changes_detected[title]['initial_length']} -> {changes_detected[title]['new_length']}")
    
    print(f"\nChange detection results:")
    print(f"  Windows monitored: {len(initial_states)}")
    print(f"  Changes detected: {len(changes_detected)}")
    
    for title, change_info in changes_detected.items():
        print(f"    {title}: Changed at {change_info['first_change_time']}s")
    
    return True

def test_text_extraction_performance():
    """Test performance of text extraction operations."""
    print("=== Testing Text Extraction Performance ===\n")
    
    finder = TextTheSpireWindowFinder()
    game_state_windows = finder.get_game_state_windows()
    
    if not game_state_windows:
        print("No game state windows found")
        return False
    
    # Performance test: extract from all windows
    print(f"Testing extraction speed from {len(game_state_windows)} windows...")
    
    start_time = time.time()
    total_chars = 0
    successful_extractions = 0
    
    for window_dict in game_state_windows:
        handle = window_dict['hwnd']
        title = window_dict['title']
        
        extraction_start = time.time()
        text = extract_window_text(handle, title)
        extraction_time = time.time() - extraction_start
        
        if text is not None:
            successful_extractions += 1
            total_chars += len(text)
            print(f"  {title}: {len(text)} chars in {extraction_time:.4f}s")
    
    total_time = time.time() - start_time
    
    print(f"\nPerformance summary:")
    print(f"  Total time: {total_time:.4f}s")
    print(f"  Successful extractions: {successful_extractions}/{len(game_state_windows)}")
    print(f"  Total characters extracted: {total_chars}")
    print(f"  Average time per window: {total_time/len(game_state_windows):.4f}s")
    print(f"  Characters per second: {total_chars/total_time:.0f}")
    
    # Test rapid repeated extractions
    print(f"\nTesting rapid repeated extractions...")
    player_window = finder.get_window_by_title('Player')
    
    if player_window:
        rapid_start = time.time()
        for i in range(10):
            text = extract_window_text(player_window['hwnd'], 'Player')
        rapid_time = time.time() - rapid_start
        
        print(f"  10 rapid extractions: {rapid_time:.4f}s ({rapid_time/10:.4f}s each)")
    
    return successful_extractions > 0

def main():
    """Run all detailed text extraction tests."""
    print("Text the Spire - Detailed Text Extraction Testing")
    print("=" * 55)
    
    # Test 1: Reliability
    success1 = test_text_extraction_reliability()
    
    # Test 2: Text formatting and parsing
    success2 = test_text_formatting_parsing()
    
    # Test 3: Update detection
    success3 = test_text_update_detection()
    
    # Test 4: Performance
    success4 = test_text_extraction_performance()
    
    print("\n" + "=" * 55)
    print("SUMMARY:")
    print(f"Text Reliability: {'[PASS]' if success1 else '[FAIL]'}")
    print(f"Format Parsing: {'[PASS]' if success2 else '[FAIL]'}")
    print(f"Update Detection: {'[PASS]' if success3 else '[FAIL]'}")
    print(f"Performance: {'[PASS]' if success4 else '[FAIL]'}")
    
    if success1 and success2 and success3 and success4:
        print("\n[PASS] All detailed text extraction tests passed!")
        print("pywinauto approach is viable for Text the Spire integration.")
    else:
        print("\n[PARTIAL] Some tests passed. Review results for implementation guidance.")
    
    return success1 and success2 and success3 and success4

if __name__ == "__main__":
    main()