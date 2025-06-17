#!/usr/bin/env python3
"""Text the Spire CLI Tool - Main entry point."""

import argparse
import json
import sys
from typing import List

from core import stubs
from utils.constants import DEFAULT_COMMAND_TIMEOUT

def handle_list_windows(args):
    """Handle --list-windows command."""
    windows = stubs.list_windows()
    
    print("\nAvailable Text the Spire Windows:")
    print("-" * 40)
    for window in windows:
        print(f"{window['title']:<15} Type: {window['type']:<12} Class: {window['class_name']}")
    
    return 0

def handle_execute_command(args):
    """Handle --execute command."""
    result = stubs.execute_command(
        command=args.execute,
        verify=args.verify,
        timeout=args.timeout
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\nCommand: '{result['command']}'")
        print(f"Success: {result['success']}")
        print(f"Response Time: {result['response_time']:.3f}s")
        if result['error']:
            print(f"Error: {result['error']}")
    
    return 0 if result['success'] else 1

def handle_execute_list(args):
    """Handle --execute-list command."""
    try:
        with open(args.execute_list, 'r') as f:
            commands = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Command file '{args.execute_list}' not found")
        return 1
    
    results = stubs.execute_command_sequence(
        commands=commands,
        verify=args.verify,
        timeout=args.timeout
    )
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\nExecuting {len(commands)} commands:")
        print("-" * 40)
        for i, result in enumerate(results, 1):
            status = "OK" if result['success'] else "FAIL"
            print(f"{i}. [{status}] '{result['command']}' - {result['response_time']:.3f}s")
            if result['error']:
                print(f"   Error: {result['error']}")
    
    failed = sum(1 for r in results if not r['success'])
    return failed

def handle_read_window(args):
    """Handle --read-window command."""
    window_content = stubs.read_window(args.read_window)
    
    if args.json:
        print(json.dumps(window_content, indent=2))
    else:
        print(f"\n=== {window_content['window_title']} Window ===")
        if window_content['error']:
            print(f"Error: {window_content['error']}")
        else:
            print(window_content['content'])
    
    return 0 if not window_content['error'] else 1

def handle_read_windows(args):
    """Handle --read-windows command."""
    window_titles = [title.strip() for title in args.read_windows.split(',')]
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

def handle_execute_and_read(args):
    """Handle combined --execute and --read-window."""
    result = stubs.execute_and_read(
        command=args.execute,
        window_title=args.read_window,
        verify=args.verify,
        timeout=args.timeout
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\nExecuted: '{result['command']}'")
        print(f"Success: {result['command_success']}")
        print(f"Response Time: {result['response_time']:.3f}s")
        
        if result['error']:
            print(f"Error: {result['error']}")
        else:
            print(f"\n=== {args.read_window} Window ===")
            print(result['window_content'])
    
    return 0 if result['command_success'] and not result['error'] else 1

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Text the Spire Integration Tool - Control Slay the Spire via Text the Spire mod",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list-windows
  %(prog)s --execute "choose 1" --verify
  %(prog)s --execute-list commands.txt --verify
  %(prog)s --read-window "Map"
  %(prog)s --execute "end" --read-window "Event" --verify
  %(prog)s --read-windows "Map,Hand,Player"
        """
    )
    
    # Command options
    parser.add_argument('--list-windows', action='store_true',
                        help='List all available Text the Spire windows')
    parser.add_argument('--execute', metavar='COMMAND',
                        help='Execute a single command')
    parser.add_argument('--execute-list', metavar='FILE',
                        help='Execute commands from a file (one per line)')
    parser.add_argument('--read-window', metavar='WINDOW',
                        help='Read content from a specific window')
    parser.add_argument('--read-windows', metavar='WINDOWS',
                        help='Read content from multiple windows (comma-separated)')
    
    # Options
    parser.add_argument('--verify', action='store_true',
                        help='Verify command execution via Log window')
    parser.add_argument('--timeout', type=float, default=DEFAULT_COMMAND_TIMEOUT,
                        help=f'Command timeout in seconds (default: {DEFAULT_COMMAND_TIMEOUT})')
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.list_windows, args.execute, args.execute_list, 
                args.read_window, args.read_windows]):
        parser.error('No action specified. Use --help for usage information.')
    
    # Handle commands
    try:
        if args.list_windows:
            return handle_list_windows(args)
        elif args.execute and args.read_window:
            return handle_execute_and_read(args)
        elif args.execute:
            return handle_execute_command(args)
        elif args.execute_list:
            return handle_execute_list(args)
        elif args.read_windows:
            return handle_read_windows(args)
        elif args.read_window:
            return handle_read_window(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())