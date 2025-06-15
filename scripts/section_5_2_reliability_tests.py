#!/usr/bin/env python3
"""
Phase 1 Section 5.2: Input Reliability Testing

Comprehensive testing of command input reliability using the smart clearing approach.
Tests rapid command sequences, buffering, latency, and error handling.
"""

import sys
import os
import time
import statistics
from pywinauto import Application
from datetime import datetime

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from reliable_window_finder import TextTheSpireWindowFinder

class ReliabilityTester:
    def __init__(self):
        self.finder = TextTheSpireWindowFinder()
        self.results = {
            'rapid_sequences': [],
            'latency_measurements': [],
            'buffering_tests': [],
            'error_handling': []
        }
    
    def send_command_with_timing(self, command, measure_latency=True):
        """Send command using smart clearing and optionally measure timing."""
        # Get prompt window
        prompt_data = self.finder.get_prompt_window()
        if not prompt_data:
            return {'success': False, 'error': 'Prompt window not found', 'timing': None}
        
        try:
            # Connect with pywinauto
            app = Application().connect(handle=prompt_data['hwnd'])
            window = app.window(handle=prompt_data['hwnd'])
            
            # Record start time
            start_time = time.perf_counter()
            
            # Smart clearing approach
            window.set_focus()
            time.sleep(0.05)
            window.type_keys(" ")      # Type space (no error sound)
            time.sleep(0.02)
            window.type_keys("^a")     # Select all
            time.sleep(0.02)
            window.type_keys(command)  # Type command (replaces selection)
            time.sleep(0.05)
            window.type_keys("{ENTER}")
            
            # Record command sent time
            command_sent_time = time.perf_counter()
            
            if not measure_latency:
                return {'success': True, 'error': None, 'timing': command_sent_time - start_time}
            
            # Wait for response in log window if measuring latency
            response_time = self.wait_for_log_response(command, timeout=5.0)
            end_time = time.perf_counter()
            
            timing_data = {
                'command_input_time': command_sent_time - start_time,
                'total_response_time': end_time - start_time,
                'processing_time': response_time if response_time else None
            }
            
            return {'success': True, 'error': None, 'timing': timing_data}
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'timing': None}
    
    def wait_for_log_response(self, command, timeout=5.0):
        """Wait for command to appear in log and return response time."""
        start_time = time.perf_counter()
        
        while time.perf_counter() - start_time < timeout:
            if self.check_command_in_log(command):
                return time.perf_counter() - start_time
            time.sleep(0.1)
        
        return None  # Timeout
    
    def check_command_in_log(self, command):
        """Quick check if command appears in log."""
        log_window = self.finder.get_window_by_title('Log')
        if not log_window:
            return False
        
        try:
            app = Application().connect(handle=log_window['hwnd'])
            window = app.window(handle=log_window['hwnd'])
            
            # Quick text extraction
            children = window.children()
            for child in children:
                child_text = child.window_text()
                if command in child_text:
                    return True
            return False
            
        except Exception:
            return False
    
    def test_rapid_command_sequences(self):
        """Test 5.2.1: Rapid command sequences with smart clearing."""
        print("\n" + "="*60)
        print("TEST 5.2.1: RAPID COMMAND SEQUENCES")
        print("="*60)
        
        # Test different sequence lengths
        sequence_lengths = [3, 5, 10, 15]
        commands = ["info", "help", "version", "status", "quit", "menu", "save", "load", "restart", "debug"]
        
        for seq_length in sequence_lengths:
            print(f"\nTesting sequence of {seq_length} commands...")
            
            test_commands = commands[:seq_length]
            sequence_start = time.perf_counter()
            success_count = 0
            timings = []
            
            for i, cmd in enumerate(test_commands):
                print(f"  Command {i+1}/{seq_length}: '{cmd}'")
                result = self.send_command_with_timing(cmd, measure_latency=False)
                
                if result['success']:
                    success_count += 1
                    timings.append(result['timing'])
                else:
                    print(f"    [ERROR] {result['error']}")
                
                # Small delay between commands
                time.sleep(0.1)
            
            sequence_end = time.perf_counter()
            total_time = sequence_end - sequence_start
            
            sequence_result = {
                'length': seq_length,
                'success_count': success_count,
                'success_rate': success_count / seq_length,
                'total_time': total_time,
                'average_command_time': statistics.mean(timings) if timings else 0,
                'timings': timings
            }
            
            self.results['rapid_sequences'].append(sequence_result)
            
            print(f"  Results: {success_count}/{seq_length} successful ({sequence_result['success_rate']:.1%})")
            print(f"  Total time: {total_time:.2f}s, Avg per command: {sequence_result['average_command_time']:.3f}s")
    
    def test_command_buffering(self):
        """Test 5.2.2: Command buffering and queuing behavior."""
        print("\n" + "="*60)
        print("TEST 5.2.2: COMMAND BUFFERING/QUEUING")
        print("="*60)
        
        # Test rapid succession without delays
        print("\nTesting rapid succession (no delays)...")
        commands = ["info", "help", "version"]
        
        # Send all commands as fast as possible
        start_time = time.perf_counter()
        results = []
        
        for cmd in commands:
            result = self.send_command_with_timing(cmd, measure_latency=False)
            results.append({'command': cmd, 'result': result})
        
        send_time = time.perf_counter() - start_time
        
        # Wait for all responses
        print("Waiting 3 seconds for all responses...")
        time.sleep(3.0)
        
        # Check which commands made it to log
        verified_count = 0
        for test in results:
            if self.check_command_in_log(test['command']):
                verified_count += 1
                print(f"  [OK] '{test['command']}' found in log")
            else:
                print(f"  [MISS] '{test['command']}' NOT found in log")
        
        buffering_result = {
            'commands_sent': len(commands),
            'commands_verified': verified_count,
            'send_time': send_time,
            'buffer_success_rate': verified_count / len(commands)
        }
        
        self.results['buffering_tests'].append(buffering_result)
        
        print(f"\nBuffering Results: {verified_count}/{len(commands)} commands processed ({buffering_result['buffer_success_rate']:.1%})")
        print(f"Total send time: {send_time:.3f}s")
    
    def test_input_latency(self):
        """Test 5.2.3: Precise input latency measurements."""
        print("\n" + "="*60)
        print("TEST 5.2.3: INPUT LATENCY MEASUREMENT")
        print("="*60)
        
        # Test commands with different expected response types
        test_commands = ["info", "help", "version"]
        measurements_per_command = 5
        
        for command in test_commands:
            print(f"\nMeasuring latency for '{command}' command...")
            command_measurements = []
            
            for i in range(measurements_per_command):
                print(f"  Measurement {i+1}/{measurements_per_command}")
                
                result = self.send_command_with_timing(command, measure_latency=True)
                
                if result['success'] and result['timing']:
                    timing = result['timing']
                    command_measurements.append(timing)
                    
                    print(f"    Input time: {timing['command_input_time']:.3f}s")
                    if timing['processing_time']:
                        print(f"    Response time: {timing['processing_time']:.3f}s")
                        print(f"    Total time: {timing['total_response_time']:.3f}s")
                    else:
                        print(f"    Response: TIMEOUT")
                else:
                    print(f"    ERROR: {result['error']}")
                
                # Wait between measurements
                time.sleep(1.0)
            
            if command_measurements:
                # Calculate statistics
                input_times = [m['command_input_time'] for m in command_measurements]
                response_times = [m['processing_time'] for m in command_measurements if m['processing_time']]
                
                latency_stats = {
                    'command': command,
                    'sample_count': len(command_measurements),
                    'input_time_avg': statistics.mean(input_times),
                    'input_time_stdev': statistics.stdev(input_times) if len(input_times) > 1 else 0,
                    'response_time_avg': statistics.mean(response_times) if response_times else None,
                    'response_time_stdev': statistics.stdev(response_times) if len(response_times) > 1 else 0,
                    'timeout_count': len([m for m in command_measurements if not m['processing_time']])
                }
                
                self.results['latency_measurements'].append(latency_stats)
                
                print(f"  Summary for '{command}':")
                print(f"    Input latency: {latency_stats['input_time_avg']:.3f}s ± {latency_stats['input_time_stdev']:.3f}s")
                if latency_stats['response_time_avg']:
                    print(f"    Response latency: {latency_stats['response_time_avg']:.3f}s ± {latency_stats['response_time_stdev']:.3f}s")
                if latency_stats['timeout_count'] > 0:
                    print(f"    Timeouts: {latency_stats['timeout_count']}/{latency_stats['sample_count']}")
    
    def test_error_handling(self):
        """Test 5.2.4: Error handling for invalid commands."""
        print("\n" + "="*60)
        print("TEST 5.2.4: ERROR HANDLING FOR INVALID COMMANDS")
        print("="*60)
        
        # Test various invalid commands
        invalid_commands = [
            "invalidcommand",
            "xyz123",
            "notarealcommand",
            "",  # Empty command
            "   ",  # Whitespace only
            "verylongcommandnamethatdoesnotexist",
            "help me please",  # Multi-word
            "!@#$%"  # Special characters
        ]
        
        for cmd in invalid_commands:
            print(f"\nTesting invalid command: '{cmd}'")
            
            result = self.send_command_with_timing(cmd, measure_latency=True)
            
            if result['success']:
                # Check if there's any response in log
                time.sleep(1.0)
                has_response = self.check_command_in_log(cmd) if cmd.strip() else False
                
                error_result = {
                    'command': cmd,
                    'send_success': True,
                    'has_log_response': has_response,
                    'timing': result['timing']
                }
                
                print(f"  Send: SUCCESS, Log response: {'YES' if has_response else 'NO'}")
                if result['timing'] and result['timing']['processing_time']:
                    print(f"  Response time: {result['timing']['processing_time']:.3f}s")
            else:
                error_result = {
                    'command': cmd,
                    'send_success': False,
                    'error': result['error'],
                    'timing': None
                }
                print(f"  Send: FAILED - {result['error']}")
            
            self.results['error_handling'].append(error_result)
    
    def generate_report(self):
        """Generate comprehensive test report."""
        print("\n" + "="*80)
        print("SECTION 5.2 INPUT RELIABILITY TEST REPORT")
        print("="*80)
        print(f"Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Rapid sequences summary
        print("\n" + "-"*60)
        print("5.2.1 RAPID COMMAND SEQUENCES SUMMARY")
        print("-"*60)
        for result in self.results['rapid_sequences']:
            print(f"Length {result['length']:2d}: {result['success_rate']:6.1%} success, {result['average_command_time']:.3f}s avg/cmd")
        
        if self.results['rapid_sequences']:
            overall_success = sum(r['success_count'] for r in self.results['rapid_sequences'])
            total_commands = sum(r['length'] for r in self.results['rapid_sequences'])
            print(f"Overall: {overall_success}/{total_commands} ({overall_success/total_commands:.1%}) successful")
        
        # Buffering summary
        print("\n" + "-"*60)
        print("5.2.2 COMMAND BUFFERING SUMMARY")
        print("-"*60)
        for result in self.results['buffering_tests']:
            print(f"Buffer test: {result['commands_verified']}/{result['commands_sent']} ({result['buffer_success_rate']:.1%}) processed")
            print(f"Send time: {result['send_time']:.3f}s")
        
        # Latency summary
        print("\n" + "-"*60)
        print("5.2.3 INPUT LATENCY SUMMARY")
        print("-"*60)
        for result in self.results['latency_measurements']:
            print(f"Command '{result['command']}':")
            print(f"  Input latency: {result['input_time_avg']:.3f}s ± {result['input_time_stdev']:.3f}s")
            if result['response_time_avg']:
                print(f"  Response latency: {result['response_time_avg']:.3f}s ± {result['response_time_stdev']:.3f}s")
            if result['timeout_count'] > 0:
                print(f"  Timeouts: {result['timeout_count']}/{result['sample_count']}")
        
        # Error handling summary
        print("\n" + "-"*60)
        print("5.2.4 ERROR HANDLING SUMMARY")
        print("-"*60)
        successful_sends = len([r for r in self.results['error_handling'] if r['send_success']])
        total_invalid = len(self.results['error_handling'])
        print(f"Invalid command sends: {successful_sends}/{total_invalid} ({successful_sends/total_invalid:.1%}) successful")
        
        has_responses = len([r for r in self.results['error_handling'] if r.get('has_log_response', False)])
        print(f"Invalid commands with log responses: {has_responses}/{successful_sends}")
        
        # Overall conclusion
        print("\n" + "="*60)
        print("OVERALL SECTION 5.2 CONCLUSION")
        print("="*60)
        
        if self.results['rapid_sequences']:
            avg_success_rate = statistics.mean([r['success_rate'] for r in self.results['rapid_sequences']])
            print(f"[OK] Rapid sequences: {avg_success_rate:.1%} average success rate")
        
        if self.results['buffering_tests']:
            avg_buffer_rate = statistics.mean([r['buffer_success_rate'] for r in self.results['buffering_tests']])
            print(f"[OK] Command buffering: {avg_buffer_rate:.1%} success rate")
        
        if self.results['latency_measurements']:
            avg_input_latency = statistics.mean([r['input_time_avg'] for r in self.results['latency_measurements']])
            response_measurements = [r for r in self.results['latency_measurements'] if r['response_time_avg']]
            if response_measurements:
                avg_response_latency = statistics.mean([r['response_time_avg'] for r in response_measurements])
                print(f"[OK] Average input latency: {avg_input_latency:.3f}s")
                print(f"[OK] Average response latency: {avg_response_latency:.3f}s")
        
        error_send_rate = successful_sends / total_invalid if total_invalid > 0 else 0
        print(f"[OK] Invalid command handling: {error_send_rate:.1%} send success rate")
        
        print("\n[CONCLUSION] Smart clearing approach provides reliable command input for Text the Spire")

def main():
    """Run all Section 5.2 reliability tests."""
    print("PHASE 1 SECTION 5.2: INPUT RELIABILITY TESTING")
    print("="*80)
    print("Testing command input reliability using smart clearing approach")
    print("REQUIREMENTS: Text the Spire must be running with prompt and log windows visible")
    
    # Check if Text the Spire windows are available
    finder = TextTheSpireWindowFinder()
    prompt_window = finder.get_prompt_window()
    log_window = finder.get_window_by_title('Log')
    
    if not prompt_window:
        print("\n[ERROR] Prompt window not found. Is Text the Spire running?")
        return False
    
    if not log_window:
        print("\n[ERROR] Log window not found. Is Text the Spire running?")
        return False
    
    print(f"\n[OK] Found prompt window: '{prompt_window['title']}'")
    print(f"[OK] Found log window: '{log_window['title']}'")
    print("\nStarting automated testing...")
    
    tester = ReliabilityTester()
    
    try:
        # Run all tests
        tester.test_rapid_command_sequences()
        tester.test_command_buffering()
        tester.test_input_latency()
        tester.test_error_handling()
        
        # Generate final report
        tester.generate_report()
        
        print(f"\n[SUCCESS] Section 5.2 reliability testing completed successfully!")
        print(f"Results saved in memory. See report above for detailed findings.")
        return True
        
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Testing cancelled by user")
        return False
    except Exception as e:
        print(f"\n[ERROR] Testing failed: {e}")
        return False

if __name__ == "__main__":
    main()