#!/usr/bin/env python3
"""
Reliable window finder for Text the Spire windows.
Based on handle persistence testing findings.
"""

import win32gui
from typing import Dict, List, Optional, Tuple
import time


class TextTheSpireWindowFinder:
    """Reliable finder for Text the Spire mod windows."""
    
    def __init__(self):
        self._cached_handles = {}
        self._cache_timestamp = 0
        self._cache_duration = 30  # Cache valid for 30 seconds during gameplay
    
    def _enum_windows_callback(self, hwnd: int, windows: List[Dict]) -> bool:
        """Callback for window enumeration."""
        try:
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                _, process_id = win32gui.GetWindowThreadProcessId(hwnd)
                
                windows.append({
                    'hwnd': hwnd,
                    'title': title,
                    'class_name': class_name,
                    'width': width,
                    'height': height,
                    'process_id': process_id
                })
        except Exception as e:
            print(f"   Debug: Error processing window {hwnd}: {e}")
        
        return True
    
    def _enumerate_all_windows(self) -> List[Dict]:
        """Enumerate all visible windows."""
        # Use the working implementation from find_text_spire_windows
        from find_text_spire_windows import find_text_spire_windows
        
        # Get all windows using the working function
        categorized = find_text_spire_windows()
        
        # Flatten back to a list
        windows = []
        for window_list in categorized.values():
            windows.extend(window_list)
        
        return windows
    
    def _categorize_windows(self, windows: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize Text the Spire windows."""
        categorized = {
            'game_state_windows': [],
            'prompt_window': [],
            'main_game_window': [],
            'mod_launcher': [],
            'other_spire_windows': []
        }
        
        game_state_titles = {
            'Player', 'Monster', 'Hand', 'Deck', 'Discard',
            'Orbs', 'Relic', 'Output', 'Log'
        }
        
        for window in windows:
            title = window['title']
            class_name = window['class_name']
            
            if 'Slay the Spire' in title and class_name == 'LWJGL':
                categorized['main_game_window'].append(window)
            elif title == 'Prompt' and class_name == 'SunAwtFrame':
                categorized['prompt_window'].append(window)
            elif 'ModTheSpire' in title:
                categorized['mod_launcher'].append(window)
            elif title in game_state_titles and class_name == 'SWT_Window0':
                categorized['game_state_windows'].append(window)
            elif any(keyword in title.lower() for keyword in ['spire', 'text']):
                categorized['other_spire_windows'].append(window)
        
        return categorized
    
    def find_windows(self, use_cache: bool = True) -> Dict[str, List[Dict]]:
        """
        Find Text the Spire windows with optional caching.
        
        Args:
            use_cache: Use cached results if available and recent
            
        Returns:
            Dictionary of categorized windows
        """
        current_time = time.time()
        
        # Use cache if available and recent (handles stable during gameplay)
        if (use_cache and 
            self._cached_handles and 
            current_time - self._cache_timestamp < self._cache_duration):
            return self._cached_handles
        
        # Use the working implementation
        from find_text_spire_windows import find_text_spire_windows
        categorized = find_text_spire_windows()
        
        # Cache the results
        self._cached_handles = categorized
        self._cache_timestamp = current_time
        
        return categorized
    
    def get_game_state_windows(self, use_cache: bool = True) -> List[Dict]:
        """Get all game state windows."""
        windows = self.find_windows(use_cache)
        return windows.get('game_state_windows', [])
    
    def get_prompt_window(self, use_cache: bool = True) -> Optional[Dict]:
        """Get the prompt window for command input."""
        windows = self.find_windows(use_cache)
        prompt_windows = windows.get('prompt_window', [])
        return prompt_windows[0] if prompt_windows else None
    
    def get_main_game_window(self, use_cache: bool = True) -> Optional[Dict]:
        """Get the main game window."""
        windows = self.find_windows(use_cache)
        main_windows = windows.get('main_game_window', [])
        return main_windows[0] if main_windows else None
    
    def get_window_by_title(self, title: str, use_cache: bool = True) -> Optional[Dict]:
        """Find a specific window by title."""
        windows = self.find_windows(use_cache)
        
        for category_windows in windows.values():
            for window in category_windows:
                if window['title'] == title:
                    return window
        
        return None
    
    def is_game_running(self) -> bool:
        """Check if Text the Spire is running with the mod."""
        windows = self.find_windows(use_cache=False)  # Always check fresh
        
        has_main_game = len(windows.get('main_game_window', [])) > 0
        has_game_state = len(windows.get('game_state_windows', [])) > 0
        
        
        return has_main_game and has_game_state
    
    def get_game_state_summary(self) -> Dict:
        """Get a summary of the current game state."""
        windows = self.find_windows()
        
        summary = {
            'game_running': self.is_game_running(),
            'window_counts': {
                category: len(window_list)
                for category, window_list in windows.items()
            },
            'total_windows': sum(len(w) for w in windows.values()),
            'available_game_states': [
                w['title'] for w in windows.get('game_state_windows', [])
            ]
        }
        
        return summary
    
    def invalidate_cache(self):
        """Force cache invalidation (call after game restart)."""
        self._cached_handles = {}
        self._cache_timestamp = 0
    
    def get_handles_for_category(self, category: str, use_cache: bool = True) -> List[int]:
        """Get just the window handles for a specific category."""
        windows = self.find_windows(use_cache)
        return [w['hwnd'] for w in windows.get(category, [])]


def main():
    """Demonstration of the reliable window finder."""
    print("RELIABLE TEXT THE SPIRE WINDOW FINDER")
    print("=" * 40)
    
    finder = TextTheSpireWindowFinder()
    
    # Test game detection
    print("1. Testing game detection...")
    if finder.is_game_running():
        print("[OK] Text the Spire is running with mod")
    else:
        print("[!!] Text the Spire not detected")
        return
    
    # Show summary
    print("\n2. Game state summary:")
    summary = finder.get_game_state_summary()
    print(f"   Total windows: {summary['total_windows']}")
    print(f"   Available game states: {', '.join(summary['available_game_states'])}")
    
    # Test specific window finding
    print("\n3. Testing specific window access...")
    
    prompt = finder.get_prompt_window()
    if prompt:
        print(f"   Prompt window: Found (handle {prompt['hwnd']})")
    else:
        print("   Prompt window: Not found")
    
    player_window = finder.get_window_by_title('Player')
    if player_window:
        print(f"   Player window: Found (handle {player_window['hwnd']})")
    else:
        print("   Player window: Not found")
    
    # Test caching
    print("\n4. Testing cache performance...")
    start_time = time.time()
    finder.find_windows(use_cache=False)  # Fresh enumeration
    fresh_time = time.time() - start_time
    
    start_time = time.time()
    finder.find_windows(use_cache=True)   # Cached access
    cached_time = time.time() - start_time
    
    print(f"   Fresh enumeration: {fresh_time:.4f}s")
    print(f"   Cached access: {cached_time:.4f}s")
    if cached_time > 0:
        print(f"   Speedup: {fresh_time/cached_time:.1f}x")
    else:
        print(f"   Cached access too fast to measure")
    
    print("\n[OK] Reliable window finder is working correctly")


if __name__ == "__main__":
    main()