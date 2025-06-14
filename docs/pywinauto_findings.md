# Text the Spire - pywinauto Approach Findings

## Overview
Testing results for using pywinauto to read text content from Text the Spire mod windows (Phase 1, Section 3.1-3.2).

## Test Scripts Created
- `tests/pywinauto_text_extraction.py` - Basic connection and text extraction testing
- `tests/pywinauto_detailed_text.py` - Detailed text content analysis and performance testing

## Connection Testing Results (Section 3.1)

### Window Connection Success
- **✅ 100% Success Rate**: Connected to all 9 game state windows + prompt window
- **Window Types Tested**: Output, Log, Orbs, Player, Relic, Discard, Deck, Monster, Hand, Prompt
- **Connection Method**: `Application().connect(handle=handle)` + `app.window(handle=handle)`
- **Properties Accessible**: exists(), is_visible(), is_enabled(), class_name(), window_text(), rectangle()

### Window Properties Confirmed
All windows show consistent properties:
- **Game State Windows**: Class `SWT_Window0`, all visible and enabled
- **Prompt Window**: Class `SunAwtFrame`, visible and enabled
- **Rectangle Data**: Accurate positioning information available

## Text Extraction Results (Section 3.2)

### Text Extraction Methods Tested

#### Method 1: Direct Window Text
- **Function**: `window.window_text()`
- **Result**: Returns window title only (e.g., "Player", "Monster")
- **Effectiveness**: Poor for content extraction

#### Method 2: Children Aggregation ⭐ BEST METHOD
- **Function**: Iterate `window.children()` and collect `child.window_text()`
- **Result**: Successfully extracts actual game content
- **Effectiveness**: Excellent - this is the recommended approach

#### Method 3: Text Control Filtering
- **Function**: Filter children by class names containing 'text', 'label', 'static', 'edit'
- **Result**: Identifies Edit controls containing the content
- **Effectiveness**: Good for understanding structure

### Content Quality Analysis

#### Player Window
```
Raw text: 'Block: 0\r\nHealth: 88/88\r\nEnergy: 3'
Structure: 3 lines with key stats
Parsing: ✅ Contains Block, Health, Energy as expected
```

#### Monster Window  
```
Raw text: 'Count: 1\r\nIncoming: 11\r\n0: Jaw Worm\r\nBlock: 0\r\nHP: 41/41\r\nIntent: Attack 11'
Structure: 6 lines with combat info
Parsing: ✅ Contains Count, HP, Intent as expected
```

#### Hand Window
```
Raw text: '1:Strike 1\r\n2:Strike 1\r\n3:Strike 1\r\n4:Strike 1\r\n5:Bash 2\r\nPotions:\r\n0:Potion Slot\r\n1:Potion Slot\r\n2:Potion Slot'
Structure: 9 lines with numbered cards and potions
Parsing: ✅ Contains numbered cards and potion slots as expected
```

#### Other Windows
- **Log**: Game action history (Draw commands, HP changes)
- **Deck**: Card list with size count
- **Discard**: Size information
- **Orbs**: Front/Back orb positions (for Defect)
- **Relic**: Active relic list
- **Output**: Currently empty (game messages)

### Text Parsing Success Rates
- **8/8 Windows**: Successfully parsed with expected format
- **Text Structure**: Clean `\r\n` line separators
- **Content Quality**: Rich, structured game state information
- **Format Consistency**: Predictable patterns for each window type

## Performance Results

### Extraction Speed
- **Total Characters**: 407 chars from 9 windows
- **Total Time**: 0.016 seconds
- **Speed**: 25,449 characters/second
- **Per Window**: 0.0018s average
- **Rapid Extraction**: 0.0004s per extraction (10 rapid tests)

### Reliability
- **Connection Success**: 100% (10/10 attempts)
- **Text Consistency**: 100% (multiple extractions identical)
- **Error Rate**: 0% during testing

## Technical Implementation Notes

### Window Control Structure
Each Text the Spire window contains:
- **1 Child Control**: Single Edit control with all content
- **Control Class**: "Edit"
- **Content Format**: Multi-line text with `\r\n` separators

### Recommended Extraction Function
```python
def extract_window_text(handle, title):
    try:
        app = Application().connect(handle=handle)
        window = app.window(handle=handle)
        
        # Use children aggregation method
        children = window.children()
        all_text = []
        for child in children:
            child_text = child.window_text()
            if child_text.strip():
                all_text.append(child_text)
        
        return '\n'.join(all_text).strip()
    except Exception as e:
        return None
```

## Limitations Identified

### Minor Issues
- **Output Window**: Currently empty during testing (not critical)
- **Text Encoding**: Windows line endings (`\r\n`) need handling
- **Handle Dependency**: Requires valid window handles from finder

### Not Tested (Section 3.3 - Skipped)
- **Change Detection**: Monitoring for text updates during gameplay
- **Multi-Window Coordination**: Reading all windows simultaneously  
- **Extended Reliability**: Long-term stability testing
- **Window Scrolling**: Handling if windows have scrollable content

## Comparison with Windows API (Pending)
Section 4 will compare this approach with direct Windows API calls for:
- Performance differences
- Text extraction quality
- Implementation complexity
- Error handling

## Conclusion

### pywinauto Approach Assessment: ✅ VIABLE
- **Connection**: Excellent (100% success)
- **Text Quality**: Excellent (rich, structured game state)
- **Performance**: Excellent (25k chars/sec, sub-millisecond)
- **Parsing**: Excellent (8/8 windows parsed successfully)
- **Implementation**: Straightforward with reliable patterns

### Recommendation
pywinauto is a solid approach for Text the Spire integration. The children aggregation method provides reliable access to well-formatted game state information with excellent performance characteristics.

### Next Steps
1. Complete Section 4 (Windows API comparison)
2. Make final technical recommendation
3. Begin Phase 2 development with chosen approach