# Phase 1: Feasibility Testing - Task Plan

## Overview
Phase 1 focuses on proving the basic technical feasibility of interacting with Slay the Spire through window reading and command input. The goal is to identify the most reliable approach for building the agent.

## Success Criteria
- Successfully read game state from Slay the Spire windows
- Successfully send commands through the prompt window
- Identify the most reliable technical approach
- Document pros/cons of each method tested

## Task List

### 1. Environment Setup
**Priority: High**
**Status: Pending**

#### 1.1 Install Required Tools
- [ ] Install Python 3.8+ with virtual environment
- [ ] Install Slay the Spire (Steam version)
- [ ] Install development tools (VS Code, Git)
- [ ] Set up project directory structure

#### 1.2 Install Testing Libraries
- [ ] Install pywinauto for UI Automation
- [ ] Install win32api/pywin32 for Windows API
- [ ] Install Pillow for screenshot capture
- [ ] Install pytesseract and Tesseract-OCR for OCR testing
- [ ] Install opencv-python for image processing
- [ ] Create requirements.txt with all dependencies

#### 1.3 Configure Test Environment
- [ ] Create test script templates for each approach
- [ ] Set up logging infrastructure
- [ ] Create screenshot/output directories
- [ ] Configure Slay the Spire for windowed mode

### 2. Window Detection and Enumeration
**Priority: High**
**Status: Pending**

#### 2.1 Basic Window Finding
- [ ] Write script to enumerate all windows using win32api
- [ ] Write script to find Slay the Spire main window
- [ ] Write script to find prompt/console window
- [ ] Test window detection with game running/not running
- [ ] Document window class names and titles

#### 2.2 Window Handle Persistence
- [ ] Test if window handles remain stable across game sessions
- [ ] Test handle stability during gameplay
- [ ] Create reliable window finder function
- [ ] Add error handling for missing windows

### 3. UI Automation Approach Testing
**Priority: High**
**Status: Pending**

#### 3.1 Pywinauto Integration
- [ ] Create script to connect to Slay the Spire using pywinauto
- [ ] Test reading window titles and basic properties
- [ ] Attempt to read UI element tree
- [ ] Test if game UI elements are accessible

#### 3.2 Control Identification
- [ ] Map out accessible UI controls in main menu
- [ ] Map out accessible UI controls during gameplay
- [ ] Test reading text from UI elements
- [ ] Document which elements are/aren't accessible

#### 3.3 Interaction Testing
- [ ] Test clicking UI elements programmatically
- [ ] Test keyboard input to game window
- [ ] Test focus management between windows
- [ ] Measure response time and reliability

### 4. Windows API Approach Testing
**Priority: High**
**Status: Pending**

#### 4.1 Direct API Integration
- [ ] Create script using win32api for window manipulation
- [ ] Test GetWindowText and related functions
- [ ] Test SendMessage/PostMessage for input
- [ ] Test window positioning and sizing

#### 4.2 Memory Reading Investigation
- [ ] Research if game state is readable from memory
- [ ] Test ReadProcessMemory (if applicable)
- [ ] Document any anti-cheat or protection mechanisms
- [ ] Evaluate feasibility and ethics of memory reading

### 5. OCR Approach Testing
**Priority: High**
**Status: Pending**

#### 5.1 Screenshot Capture
- [ ] Create reliable screenshot function for game window
- [ ] Test screenshot performance (FPS achievable)
- [ ] Handle multi-monitor setups
- [ ] Test partial window capture for specific regions

#### 5.2 OCR Implementation
- [ ] Test Tesseract OCR on game screenshots
- [ ] Test different OCR preprocessing techniques
- [ ] Identify optimal regions for OCR (cards, energy, HP)
- [ ] Measure OCR accuracy on game text

#### 5.3 Template Matching
- [ ] Create template images for common game elements
- [ ] Test OpenCV template matching for icons/cards
- [ ] Combine OCR with template matching
- [ ] Evaluate accuracy and performance

### 6. Command Input Testing
**Priority: High**
**Status: Pending**

#### 6.1 Prompt Window Interaction
- [ ] Test finding and focusing prompt window
- [ ] Test sending text to prompt using pywinauto
- [ ] Test sending text using Windows API
- [ ] Test command execution and response reading

#### 6.2 Input Reliability
- [ ] Test rapid command sequences
- [ ] Test command buffering/queuing
- [ ] Handle prompt window clearing/scrolling
- [ ] Measure input latency and success rate

### 7. Integration Testing
**Priority: Medium**
**Status: Pending**

#### 7.1 Combined Approach Testing
- [ ] Create proof-of-concept combining best methods
- [ ] Test full cycle: read state → decide → send command
- [ ] Measure end-to-end latency
- [ ] Test stability over extended periods

#### 7.2 Game State Parsing
- [ ] Create parser for main menu state
- [ ] Create parser for combat state
- [ ] Create parser for map/event states
- [ ] Test state detection accuracy

### 8. Performance Evaluation
**Priority: Medium**
**Status: Pending**

#### 8.1 Benchmarking
- [ ] Measure CPU usage for each approach
- [ ] Measure memory usage for each approach
- [ ] Test impact on game performance
- [ ] Identify bottlenecks and optimization opportunities

#### 8.2 Reliability Testing
- [ ] Run extended tests (1+ hour sessions)
- [ ] Test recovery from errors/crashes
- [ ] Test handling of game updates/patches
- [ ] Document failure modes and rates

### 9. Documentation and Decision
**Priority: High**
**Status: Pending**

#### 9.1 Technical Documentation
- [ ] Document each approach with code examples
- [ ] Create comparison matrix of approaches
- [ ] List pros/cons for each method
- [ ] Include performance metrics and reliability data

#### 9.2 Recommendation Report
- [ ] Write executive summary of findings
- [ ] Recommend primary technical approach
- [ ] Outline hybrid approach if beneficial
- [ ] Create roadmap for Phase 2 based on findings

#### 9.3 Code Organization
- [ ] Refactor successful POC code into modules
- [ ] Create base classes for game interaction
- [ ] Set up proper project structure
- [ ] Create initial API design for agent

## Notes

### Testing Priority
1. Start with UI Automation as it's most likely to work
2. Test Windows API in parallel for comparison
3. Use OCR as fallback or complement to other methods
4. Focus on reliability over performance initially

### Key Metrics to Track
- Success rate of reading game state
- Accuracy of parsed information
- Latency of read/write operations
- Stability over time
- Resource usage

### Risk Mitigation
- Test with different game resolutions
- Test with different Windows versions
- Consider Steam overlay interference
- Plan for game updates breaking compatibility

## Next Steps After Phase 1
Based on the findings from this phase:
1. Select primary technical approach
2. Design agent architecture
3. Begin Phase 2: Core game state parsing
4. Develop command abstraction layer