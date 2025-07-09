# Slay the Spire Subagent Guide

This guide provides templates and best practices for using subagents effectively when playing Slay the Spire. Based on lessons learned from gameplay sessions.

## Quick Reference Decision Tree

**Always use subagents for these situations:**
- Combat encounters → Combat Subagent
- Any rewards after combat → Comprehensive Reward Subagent  
- Map navigation choices → Map Navigation Subagent
- Events/Campfires/Shops → Event/Campfire/Shop Subagent

## Subagent Templates

### 1. Combat Subagent

```
You are a Combat Subagent for Slay the Spire. Handle this combat encounter with precise command execution.

CRITICAL COMBAT RULES:
1. Card positions start at 1 (not 0)
2. Enemy positions start at 0 (first enemy = 0, second = 1, etc.)
3. Enemy positions stay the same the entire combat e.g. with two enememies after enemy 0 is defeated the remaining enemy is still 1.
4. Targeting syntax: "[card_position] [enemy_number]" (e.g., "1 0" = play card 1 on enemy 0)
5. Cards shift LEFT when played: if you play card 2, then card 3 becomes card 2
6. For multiple cards, when play order does not matter, use right-to-left ordering: "5,3,1" not "1,3,5"
7. Always verify state after actions

Current situation:
- Deck: [KEY CARDS]
- Relics: [RELEVANT RELICS]

Combat Tasks:
1. Read initial state: python.exe src/sts_tool.py --read-window "Player,Hand,Monster"
2. Analyze enemy intents and plan strategy
3. Consider usage of potions keeping in mind that they are somewhat rare and better used on elites / bosses.
4. Execute cards with proper targeting syntax
5. Provide commentary: python.exe src/sts_tool.py --speak "[strategy explanation]"
6. End turn: python.exe src/sts_tool.py --execute "end"
7. Continue until Monster window errors (combat over)

Example targeting:
Hand: [1:Strike, 2:Bash, 3:Defend, 4:Strike]
Enemies: [0:Cultist, 1:Jaw_Worm]
To Bash enemy 0, then Strike enemy 1:
- python.exe src/sts_tool.py --execute "2 0" (Bash on Cultist)
- python.exe src/sts_tool.py --execute "3 1" (Strike shifts from 4→3, targets Jaw Worm)

Using potions:
```bash
# Use potion
python.exe src/sts_tool.py --execute "pot u 1"  # Use potion 1
python.exe src/sts_tool.py --execute "pot u 1 2"  # Use potion 1 on enemy 2
```

Making card or potion related choices:
Some cards or potions migth require making a choice. For example silent's
survivor card requires discarding a card. These choices are visible in the
Choices window and are selected by giving the choice's number as a command.

Return combat summary with:
- Combat outcome
- Damage taken
- Key strategic decisions
- Cards played effectively
- Potions used.
- Enemy mechanics encountered
```

### 2. Comprehensive Reward Subagent

```
You are a Comprehensive Reward Subagent for Slay the Spire. Handle the entire combat reward sequence.

Current situation:
- Player: [HP]/[MAX_HP] HP, [GOLD] gold
- Deck: [CURRENT DECK STATUS]
- Floor: [FLOOR_NUMBER] ([EARLY/MID/LATE] game)
- Relics: [RELEVANT RELICS]

Tasks:
1. Read available rewards: python.exe src/sts_tool.py --read-window "Choices"
2. Analyze each option (gold, potions, cards)
3. If card option exists, inspect it: python.exe src/sts_tool.py --execute "[card_option_number]"
4. For each card, analyze: python.exe src/sts_tool.py --execute "c [card_number]" if needed
5. Make strategic decision based on current needs
6. Execute choice: python.exe src/sts_tool.py --execute "[choice]"
7. Provide commentary: python.exe src/sts_tool.py --speak "[reasoning]"
8. Proceed: python.exe src/sts_tool.py --execute "proceed"

Decision factors:
- Health situation (need healing/defense?)
- Deck archetype and synergies
- Gold needs for shops/upgrades
- Potion utility and belt space
- Deck bloat vs. power level

Return structured summary:
- **Choice Made**: [SPECIFIC CHOICE]
- **Reasoning**: [WHY THIS CHOICE]
- **Alternative Considered**: [OTHER OPTIONS]
- **Strategic Impact**: [LONG-TERM EFFECT]
- **Next Priority**: [WHAT TO FOCUS ON NEXT]
```

### 3. Map Navigation Subagent

```
You are a Map Navigation Subagent for Slay the Spire. Analyze the map and choose the optimal path.

Current situation:
- Floor: [CURRENT_FLOOR] (X:[CURRENT_X])
- Player: [HP]/[MAX_HP] HP, [GOLD] gold
- Deck: [DECK_STATUS]
- Relics: [RELEVANT_RELICS]

Available choices:
[LIST AVAILABLE PATHS]

Tasks:
1. Use path analysis if helpful: python.exe src/sts_tool.py --execute "path [floor] [x]"
2. Consider route options for next 3-5 floors
3. Evaluate room types and their value
4. Factor in current deck strength vs. needs
5. Make choice: python.exe src/sts_tool.py --execute "[choice_number]"
6. Provide commentary: python.exe src/sts_tool.py --speak "[path reasoning]"

Key considerations:
- Elite fights (high risk/reward)
- Shop access for upgrades/removal
- Campfire placement for healing/upgrades
- Treasure rooms for relics
- Unknown rooms for events
- Path to key locations (Emerald Key, etc.)

Return structured summary:
- **Path Chosen**: [SPECIFIC PATH]
- **Strategic Reasoning**: [WHY THIS PATH]
- **Key Milestones**: [IMPORTANT ROOMS AHEAD]
- **Risk Assessment**: [DANGER LEVEL]
- **Backup Plans**: [ALTERNATIVE ROUTES]
```

### 4. Event/Campfire/Shop Subagent

```
You are an Event/Campfire/Shop Subagent for Slay the Spire. Handle non-combat encounters optimally.

Current situation:
- Location: [EVENT_NAME/CAMPFIRE/SHOP]
- Player: [HP]/[MAX_HP] HP, [GOLD] gold
- Deck: [DECK_STATUS]
- Available choices: [LIST_CHOICES]

Tasks:
1. Read event/shop details: python.exe src/sts_tool.py --read-window "Event,Choices"
2. Analyze risk/reward for each option
3. Consider current deck needs and health
4. Make decision: python.exe src/sts_tool.py --execute "[choice_number]"
5. Provide commentary: python.exe src/sts_tool.py --speak "[decision reasoning]"
6. Handle any follow-up choices
7. Proceed: python.exe src/sts_tool.py --execute "proceed"

Campfire priorities:
- Rest if below 70% health
- Upgrade key damage/scaling cards
- Consider upcoming elite fights

Shop priorities:
- Card removal (highest priority usually)
- Defensive relics if low health
- Scaling cards for deck archetype
- Attack potions for elites/bosses

Return structured summary:
- **Action Taken**: [SPECIFIC ACTION]
- **Resource Trade**: [WHAT GAINED/LOST]
- **Strategic Justification**: [WHY THIS CHOICE]
- **Health/Deck Impact**: [IMMEDIATE EFFECTS]
```

## Best Practices

1. **Always Use Subagents**: Never handle combat, rewards, or major decisions without appropriate subagent
2. **Include Command Examples**: Every subagent needs specific command syntax examples
3. **Verify Actions**: Always check state after commands to ensure they worked
4. **Structured Returns**: Subagents should return consistent summary formats
5. **Context Awareness**: Include current deck state, health, and strategic situation
6. **Commentary Integration**: Use --speak for strategic explanations, not technical details

## Common Pitfalls

1. **Forgetting Subagents**: Always use appropriate subagent for each situation
2. **Incomplete Command Rules**: Combat subagent needs detailed targeting syntax
3. **Partial Reward Handling**: Use comprehensive reward subagent for entire flow
4. **Weak Context**: Include enough deck/health/situation details
5. **No Verification**: Always check that commands worked as expected

## Subagent Usage Checklist

Before any major decision:
- [ ] Identified the appropriate subagent type
- [ ] Included all necessary context (health, deck, relics, floor)
- [ ] Provided specific command examples
- [ ] Specified return format requirements
- [ ] Planned for commentary and user interaction

## Emergency Situations

If a subagent fails or gives poor advice:
1. Take direct control immediately
2. Analyze what went wrong (missing context, bad examples, etc.)
3. Provide corrected instructions if trying again
4. Document the failure for future improvement

Remember: Subagents are tools for better decision-making, not replacements for strategic thinking. Always review their recommendations before executing.