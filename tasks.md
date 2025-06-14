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
**Status: in progress**

#### 1.1 Install Required Tools
- [X] Install Python 3.8+ with virtual environment
- [X] Install Slay the Spire (Steam version)
- [X] Install development tools (VS Code, Git)
- [ ] Set up project directory structure

#### 1.2 Install Testing Libraries
- [ ] Install pywinauto for UI Automation
- [ ] Install win32api/pywin32 for Windows API
- [ ] Create requirements.txt with all dependencies


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

### 5. Command Input Testing
**Priority: High**
**Status: Pending**

#### 5.1 Prompt Window Interaction
- [ ] Test finding and focusing prompt window
- [ ] Test sending text to prompt using pywinauto
- [ ] Test sending text using Windows API
- [ ] Test command execution and response reading

#### 5.2 Input Reliability
- [ ] Test rapid command sequences
- [ ] Test command buffering/queuing
- [ ] Handle prompt window clearing/scrolling
- [ ] Measure input latency and success rate

### 6. Integration Testing
**Priority: Medium**
**Status: Pending**

#### 6.1 Combined Approach Testing
- [ ] Create proof-of-concept combining best methods
- [ ] Test full cycle: read state → decide → send command
- [ ] Measure end-to-end latency
- [ ] Test stability over extended periods

#### 6.2 Game State Parsing
- [ ] Create parser for main menu state
- [ ] Create parser for combat state
- [ ] Create parser for map/event states
- [ ] Test state detection accuracy


### 7. Documentation and Decision
**Priority: High**
**Status: Pending**

#### 7.1 Technical Documentation
- [ ] Document each approach with code examples
- [ ] Create comparison matrix of approaches
- [ ] List pros/cons for each method
- [ ] Include performance metrics and reliability data

#### 7.2 Recommendation Report
- [ ] Write executive summary of findings
- [ ] Recommend primary technical approach
- [ ] Outline hybrid approach if beneficial
- [ ] Create roadmap for Phase 2 based on findings

#### 7.3 Code Organization
- [ ] Refactor successful POC code into modules
- [ ] Create base classes for game interaction
- [ ] Set up proper project structure
- [ ] Create initial API design for agent

## Notes

### Testing Priority
1. Start with UI Automation as it's most likely to work
2. Test Windows API in parallel for comparison
3. Focus on reliability over performance initially

### Key Metrics to Track
- Success rate of reading game state
- Accuracy of parsed information
- Latency of read/write operations
- Stability over time
- Resource usage


## Next Steps After Phase 1
Based on the findings from this phase:
1. Select primary technical approach
2. Design agent architecture
3. Begin Phase 2: Core game state parsing
4. Develop command abstraction layer