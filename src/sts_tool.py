#!/usr/bin/env python3
"""Text the Spire CLI Tool - Main entry point."""

import argparse
import json
import sys
from typing import List

from core import stubs
from core.speaker import Speaker
from utils.constants import DEFAULT_COMMAND_TIMEOUT

def handle_list_windows(args):
    """Handle --list-windows command."""
    windows = stubs.list_windows()
    
    if args.debug:
        print("\nAvailable Text the Spire Windows:")
        print("-" * 40)
        for window in windows:
            print(f"{window['title']:<15} Type: {window['type']:<12} Class: {window['class_name']}")
    else:
        for window in windows:
            print(window['title'])
    
    return 0

def handle_execute_command(args):
    """Handle --execute command (single or comma-separated multiple commands)."""
    # Parse commands - split by comma and strip whitespace
    commands = [cmd.strip() for cmd in args.execute.split(',') if cmd.strip()]
    
    # Always use sequence execution (single command is just a sequence of 1)
    results = stubs.execute_command_sequence(
        commands=commands,
        verify=not args.dont_verify,
        timeout=args.timeout
    )
    
    if args.json:
        # For JSON output, return single object if single command, array if multiple
        if len(commands) == 1:
            print(json.dumps(results[0], indent=2))
        else:
            print(json.dumps(results, indent=2))
    else:
        # Use detailed format for all commands
        if len(commands) == 1:
            print(f"\nExecuting 1 command:")
        else:
            print(f"\nExecuting {len(commands)} commands:")
        print("-" * 40)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Command: '{result['command']}'")
            print(f"   Success: {result['success']}")
            print(f"   Response Time: {result['response_time']:.3f}s")
            print(f"   Wait Time: {result['wait_time_used']:.1f}s")
            print(f"   Command Found in Log: {result['command_found_in_log']}")
            if result['log_response']:
                print(f"   Response: {result['log_response']}")
            if result['error']:
                print(f"   Error: {result['error']}")
    
    failed = sum(1 for r in results if not r['success'])
    return failed


def handle_read_window(args):
    """Handle --read-window command (single or comma-separated multiple windows)."""
    # Parse window titles - split by comma and strip whitespace
    window_titles = [title.strip() for title in args.read_window.split(',') if title.strip()]
    
    if len(window_titles) == 1:
        # Single window
        window_content = stubs.read_window(window_titles[0])
        
        if args.json:
            print(json.dumps(window_content, indent=2))
        else:
            print(f"\n=== {window_content['window_title']} Window ===")
            if window_content['error']:
                print(f"Error: {window_content['error']}")
            else:
                print(window_content['content'])
        
        return 0 if not window_content['error'] else 1
    else:
        # Multiple windows
        result = stubs.read_multiple_windows(window_titles)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\nReading {len(window_titles)} windows (took {result['total_time']:.3f}s):")
            print("=" * 50)
            for window in result['windows']:
                print(f"\n=== {window['window_title']} ===")
                if window['error']:
                    print(f"Error: {window['error']}")
                else:
                    print(window['content'])
        
        return 0


def handle_speak(args, speaker):
    """Handle --speak command."""
    success = speaker.speak(args.speak)
    
    if args.json:
        result = {
            "text": args.speak,
            "success": success,
            "error": None if success else "Speech failed - check API key"
        }
        print(json.dumps(result, indent=2))
    else:
        if not success:
            print("Speech failed - check ELEVENLABS_API_KEY in .env file")
    
    return 0 if success else 1


def handle_routes(args):
    """Handle --routes command."""
    from core.route_evaluator import evaluate_all_routes
    
    print(f"\nEvaluating routes to floor 15 rest sites...")
    print("-" * 60)
    
    routes = evaluate_all_routes(top_n=args.routes)
    
    # Check for errors
    if routes and 'error' in routes[0]:
        print(f"Error: {routes[0]['error']}")
        return 1
    
    if not routes:
        print("No routes found.")
        return 1
    
    # Display routes
    print(f"Evaluated {len(routes)} unique routes\n")
    for i, route in enumerate(routes, 1):
        print(f"Route {i} (Score: {route['score']}):")
        counts = route['encounter_counts']
        print(f"  Emerald {counts['Emerald']}, Elite {counts['Elite']}, Rest {counts['Rest']}, "
              f"Shop {counts['Shop']}, Unknown {counts['Unknown']}, Monster {counts['Monster']}, "
              f"Treasure {counts['Treasure']}")
        print(f"  Path: {route['detail']}")
        print(f"  Destination: Rest Floor:{route['destination']}")
        print()
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Text the Spire Integration Tool - Control Slay the Spire via Text the Spire mod",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list-windows
  %(prog)s --execute "choose 1" --dont-verify
  %(prog)s --execute "choose 1,play 0,end"
  %(prog)s --read-window "Map"
  %(prog)s --execute "end" --read-window "Event"
  %(prog)s --read-window "Map,Hand,Player"
  %(prog)s --speak "I'm going to play a strike card" --execute "play 0"
        """
    )
    
    # Command options
    parser.add_argument('--list-windows', action='store_true',
                        help='List all available Text the Spire windows')
    parser.add_argument('--execute', metavar='COMMAND',
                        help='Execute one or more commands (comma-separated for multiple)')
    parser.add_argument('--read-window', metavar='WINDOW[,WINDOW2,...]',
                        help='Read content from one or more windows (comma-separated for multiple)')
    parser.add_argument('--speak', metavar='TEXT',
                        help='Speak the given text using text-to-speech')
    parser.add_argument('--routes', nargs='?', type=int, const=10, metavar='N',
                        help='Evaluate routes to floor 15 rest sites (default: top 10)')
    
    # Options
    parser.add_argument('--dont-verify', action='store_true',
                        help='Do not verify command execution via Log window')
    parser.add_argument('--timeout', type=float, default=DEFAULT_COMMAND_TIMEOUT,
                        help=f'Command timeout in seconds (default: {DEFAULT_COMMAND_TIMEOUT})')
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')
    parser.add_argument('--debug', action='store_true',
                        help='Show detailed debug information')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.list_windows, args.execute, args.read_window, args.speak, args.routes]):
        parser.error('No action specified. Use --help for usage information.')
    
    # Initialize speaker if needed
    speaker = None
    if args.speak:
        speaker = Speaker()
    
    # Handle commands
    try:
        # Handle speak first if provided
        if args.speak:
            handle_speak(args, speaker)
        
        # Then handle other commands
        if args.execute:
            handle_execute_command(args)
        if args.read_window:
            handle_read_window(args)
        if args.list_windows:
            handle_list_windows(args)
        if args.routes:
            handle_routes(args)
            
        # Wait for speech to complete if it was started
        if speaker:
            speaker.wait_for_completion()
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())