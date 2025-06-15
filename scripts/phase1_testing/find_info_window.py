#!/usr/bin/env python3
"""
Specialized script to find the window that might be the renamed "Prompt" window,
now possibly called "info".

Searches for:
1. Windows with titles containing "info" (case insensitive)
2. SunAwtFrame windows with similar size to original prompt (300x100)
3. SWT_Window0 windows that might have changed from game state to prompt
4. Any other windows that could be the prompt window
"""

import win32gui
from typing import List, Dict, Optional
import sys


def enum_windows_callback(hwnd: int, windows: List[Dict]) -> bool:
    """Callback function for EnumWindows to collect ALL window information."""
    if win32gui.IsWindowVisible(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        
        try:
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0] 
            height = rect[3] - rect[1]
            x = rect[0]
            y = rect[1]
        except:
            width = height = x = y = 0
            
        try:
            _, process_id = win32gui.GetWindowThreadProcessId(hwnd)
        except:
            process_id = 0
            
        # Only include windows that have some title or are relevant classes
        if window_text or class_name in ['SunAwtFrame', 'SWT_Window0', 'LWJGL']:
            windows.append({
                'hwnd': hwnd,
                'title': window_text,
                'class_name': class_name,
                'width': width,
                'height': height,
                'x': x,
                'y': y,
                'process_id': process_id
            })
    
    return True


def find_potential_info_windows() -> Dict[str, List[Dict]]:
    """Find windows that might be the renamed prompt window."""
    all_windows = []
    win32gui.EnumWindows(enum_windows_callback, all_windows)
    
    candidates = {
        'info_titled_windows': [],
        'sunawtframe_windows': [],
        'small_swt_windows': [],
        'prompt_sized_windows': [],
        'all_spire_related': [],
        'other_candidates': []
    }
    
    # Known game state titles that should NOT be the prompt window
    game_state_titles = {
        'Player', 'Monster', 'Hand', 'Deck', 'Discard', 
        'Orbs', 'Relic', 'Output', 'Log'
    }
    
    for window in all_windows:
        title = window['title'].strip()
        class_name = window['class_name']
        width = window['width']
        height = window['height']
        
        # Windows with "info" in title (case insensitive)
        if 'info' in title.lower():
            candidates['info_titled_windows'].append(window)
        
        # All SunAwtFrame windows (original prompt was this class)
        if class_name == 'SunAwtFrame':
            candidates['sunawtframe_windows'].append(window)
        
        # SWT_Window0 windows that are small (might have changed from game state to prompt)
        if class_name == 'SWT_Window0' and width < 500 and height < 300:
            candidates['small_swt_windows'].append(window)
        
        # Windows with size similar to original prompt (300x100, allow some variance)
        if (250 <= width <= 400) and (80 <= height <= 150):
            candidates['prompt_sized_windows'].append(window)
        
        # Any spire-related windows
        if any(keyword in title.lower() for keyword in ['spire', 'text', 'mod']):
            candidates['all_spire_related'].append(window)
        
        # Other potential candidates (small windows with short titles)
        if (title and len(title) <= 10 and width < 500 and height < 300 and 
            title not in game_state_titles):
            candidates['other_candidates'].append(window)
    
    return candidates


def print_candidate_analysis(candidates: Dict[str, List[Dict]]) -> None:
    """Print detailed analysis of potential prompt window candidates."""
    print("ANALYSIS OF POTENTIAL PROMPT WINDOW CANDIDATES")
    print("=" * 50)
    
    for category, windows in candidates.items():
        if windows:
            print(f"\n{category.upper().replace('_', ' ')} ({len(windows)} found)")
            print("-" * 40)
            
            for i, window in enumerate(windows, 1):
                print(f"{i}. Title: '{window['title']}'")
                print(f"   Handle: {window['hwnd']}")
                print(f"   Class: {window['class_name']}")
                print(f"   Size: {window['width']}x{window['height']}")
                print(f"   Position: ({window['x']}, {window['y']})")
                print(f"   Process ID: {window['process_id']}")
                
                # Add analysis notes
                if window['class_name'] == 'SunAwtFrame':
                    print("   [ANALYSIS] Same class as original Prompt window!")
                if 'info' in window['title'].lower():
                    print("   [ANALYSIS] Contains 'info' - likely candidate!")
                if 250 <= window['width'] <= 400 and 80 <= window['height'] <= 150:
                    print("   [ANALYSIS] Size similar to original Prompt (300x100)")
                
                print()


def find_best_candidates(candidates: Dict[str, List[Dict]]) -> List[Dict]:
    """Analyze and rank the best candidates for the prompt window."""
    all_candidates = []
    
    # Collect all unique candidates
    seen_handles = set()
    for windows in candidates.values():
        for window in windows:
            if window['hwnd'] not in seen_handles:
                all_candidates.append(window)
                seen_handles.add(window['hwnd'])
    
    # Score each candidate
    scored_candidates = []
    for window in all_candidates:
        score = 0
        reasons = []
        
        # High score for "info" in title
        if 'info' in window['title'].lower():
            score += 10
            reasons.append("Contains 'info' in title")
        
        # High score for SunAwtFrame class (same as original)
        if window['class_name'] == 'SunAwtFrame':
            score += 8
            reasons.append("SunAwtFrame class (same as original Prompt)")
        
        # Medium score for size similarity to original prompt
        width, height = window['width'], window['height']
        if 250 <= width <= 400 and 80 <= height <= 150:
            score += 5
            reasons.append(f"Size {width}x{height} similar to original 300x100")
        
        # Small bonus for short titles (prompt windows typically have short names)
        if window['title'] and len(window['title']) <= 10:
            score += 2
            reasons.append("Short title")
        
        # Small bonus for being small window (prompts are typically small)
        if width < 500 and height < 300:
            score += 1
            reasons.append("Small window size")
        
        scored_candidates.append({
            'window': window,
            'score': score,
            'reasons': reasons
        })
    
    # Sort by score (highest first)
    scored_candidates.sort(key=lambda x: x['score'], reverse=True)
    
    return scored_candidates


def main():
    """Main function to find the potential info/prompt window."""
    print("SEARCHING FOR RENAMED PROMPT WINDOW (possibly 'info')")
    print("=" * 55)
    
    print("Enumerating all visible windows and analyzing candidates...")
    candidates = find_potential_info_windows()
    
    # Print detailed analysis
    print_candidate_analysis(candidates)
    
    # Find and rank best candidates
    print("\nBEST CANDIDATES RANKING")
    print("=" * 25)
    
    best_candidates = find_best_candidates(candidates)
    
    if not best_candidates:
        print("No potential candidates found.")
        return
    
    for i, candidate in enumerate(best_candidates[:5], 1):  # Show top 5
        window = candidate['window']
        score = candidate['score']
        reasons = candidate['reasons']
        
        print(f"\n{i}. CANDIDATE (Score: {score})")
        print(f"   Title: '{window['title']}'")
        print(f"   Handle: {window['hwnd']}")
        print(f"   Class: {window['class_name']}")
        print(f"   Size: {window['width']}x{window['height']}")
        print(f"   Reasons: {', '.join(reasons)}")
        
        if score >= 10:
            print("   [VERDICT] VERY LIKELY candidate!")
        elif score >= 5:
            print("   [VERDICT] POSSIBLE candidate")
        else:
            print("   [VERDICT] Less likely candidate")
    
    # Summary
    print(f"\nSUMMARY")
    print(f"Total candidates analyzed: {len(best_candidates)}")
    
    top_candidate = best_candidates[0] if best_candidates else None
    if top_candidate and top_candidate['score'] >= 8:
        window = top_candidate['window']
        print(f"RECOMMENDED: '{window['title']}' (Handle: {window['hwnd']}) - {window['class_name']}")
    else:
        print("No high-confidence candidates found. Manual verification needed.")


if __name__ == "__main__":
    main()