# Phase 1: Feasibility Testing - Task Plan

## Overview
Phase 1 focuses on proving the basic technical feasibility of interacting with Slay the Spire through the "Text the Spire" mod. This mod provides text windows showing game state and a prompt window for entering commands. We will ONLY interact with these Text the Spire windows - NOT the game's native UI. The goal is to identify the most reliable approach for reading text windows and sending commands.

## Success Criteria
- Successfully read game state from Text the Spire's text windows
- Successfully send commands through Text the Spire's prompt window
- Identify the most reliable technical approach for text window interaction
- Document pros/cons of each method tested
- Confirm we can interact WITHOUT touching the game's native UI

## Task List

### 1. Environment Setup
**Priority: High**
**Status: in progress**

#### 1.1 Install Required Tools
- [X] Install Python 3.8+ with virtual environment
- [X] Install Slay the Spire (Steam version)
- [ ] Install Text the Spire mod (provides text windows for accessibility)
- [X] Install development tools (VS Code, Git)
- [ ] Set up project directory structure

#### 1.2 Install Testing Libraries
- [ ] Install pywinauto for text window reading
- [ ] Install win32api/pywin32 for Windows API text reading
- [ ] Create requirements.txt with all dependencies


### 2. Window Detection and Enumeration
**Priority: High**
**Status: Pending**

#### 2.1 Basic Window Finding
- [ ] Write script to enumerate all windows using win32api
- [ ] Write script to find Text the Spire text windows (game state windows)
- [ ] Write script to find Text the Spire prompt window (command input)
- [ ] Test window detection with game running/not running
- [ ] Document Text the Spire window class names and titles
- [ ] Count and identify all Text the Spire windows

#### 2.2 Window Handle Persistence
- [ ] Test if window handles remain stable across game sessions
- [ ] Test handle stability during gameplay
- [ ] Create reliable window finder function
- [ ] Add error handling for missing windows

### 3. Text Window Reading - Pywinauto Approach
**Priority: High**
**Status: Pending**

#### 3.1 Text the Spire Window Connection
- [ ] Create script to connect to Text the Spire windows using pywinauto
- [ ] Identify all Text the Spire text windows
- [ ] Test reading window titles and properties
- [ ] Verify we can access text content, NOT game UI

#### 3.2 Text Content Extraction
- [ ] Test reading text from Text the Spire game state windows
- [ ] Test different methods to extract window text content
- [ ] Handle multi-line text and formatting
- [ ] Document text extraction success rates

#### 3.3 Text Window Monitoring
- [ ] Test detecting when text windows update
- [ ] Test reading from multiple Text the Spire windows
- [ ] Measure text reading latency and reliability
- [ ] Handle window scrolling if applicable

### 4. Text Window Reading - Windows API Approach
**Priority: High**
**Status: Pending**

#### 4.1 Direct API Text Reading
- [ ] Create script using win32api to find Text the Spire windows
- [ ] Test GetWindowText on Text the Spire windows
- [ ] Test alternative text reading methods (WM_GETTEXT, etc.)
- [ ] Compare text extraction quality with pywinauto

### 5. Text the Spire Command Input Testing
**Priority: High**
**Status: Pending**

#### 5.1 Prompt Window Interaction
- [ ] Test finding and focusing Text the Spire prompt window
- [ ] Test sending text commands using pywinauto
- [ ] Test sending text commands using Windows API
- [ ] Test command execution and response detection
- [ ] Verify commands affect game state (via text window updates)

#### 5.2 Input Reliability
- [ ] Test rapid command sequences to Text the Spire
- [ ] Test command buffering/queuing
- [ ] Handle prompt window clearing/scrolling
- [ ] Measure input latency and success rate
- [ ] Test error handling for invalid commands

### 6. Integration Testing
**Priority: Medium**
**Status: Pending**

#### 6.1 Combined Approach Testing
- [ ] Create proof-of-concept combining best methods
- [ ] Test full cycle: read state → decide → send command
- [ ] Measure end-to-end latency
- [ ] Test stability over extended periods

#### 6.2 Text the Spire Output Parsing
- [ ] Create parser for Text the Spire main menu text
- [ ] Create parser for Text the Spire combat state text
- [ ] Create parser for Text the Spire map/event text
- [ ] Test state detection accuracy from text windows


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

### Important: Text the Spire Interaction Model
**We are NOT automating the game's native UI.** The Text the Spire mod provides:
- Multiple text windows displaying game state information
- A prompt window for entering text commands

Our agent will ONLY:
1. Read text from Text the Spire's game state windows
2. Send commands to Text the Spire's prompt window

We will NOT:
- Click on game buttons or UI elements
- Interact with game menus directly
- Automate any part of the game's native interface

### Testing Priority
1. Start by identifying all Text the Spire windows
2. Test both pywinauto and Windows API for text reading
3. Focus on reliable text extraction from Text the Spire windows
4. Ensure command input works through Text the Spire prompt
5. Never attempt to automate the game's native UI

### Key Metrics to Track
- Success rate of reading text from Text the Spire windows
- Accuracy of parsed Text the Spire output
- Latency of text reading operations
- Command input success rate via Text the Spire prompt
- Stability of Text the Spire window handles over time
- Resource usage


## Next Steps After Phase 1
Based on the findings from this phase:
1. Select primary technical approach for Text the Spire interaction
2. Design agent architecture around text-based communication
3. Begin Phase 2: Core Text the Spire output parsing
4. Develop command abstraction layer for Text the Spire prompt