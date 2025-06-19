"""Constants for Text the Spire integration."""

# Window class names
GAME_STATE_WINDOW_CLASS = "SWT_Window0"
PROMPT_WINDOW_CLASS = "SunAwtFrame"

# Window titles
PROMPT_WINDOW_TITLES = ["Prompt", "info"]
GAME_STATE_WINDOWS = ["Player", "Monster", "Hand", "Deck", "Discard", "Orbs", "Relic", "Output", "Log", "Map", "Event"]

# Timing constants (in seconds)
DEFAULT_COMMAND_TIMEOUT = 5.0
COMMAND_INPUT_DELAY = 0.02  # Delay after select all
RESPONSE_CHECK_INTERVAL = 0.1
AVERAGE_INPUT_LATENCY = 0.249  # From testing
AVERAGE_RESPONSE_TIME = 0.002  # From testing

# Command execution
MAX_RELIABLE_COMMANDS_PER_SECOND = 4

# Command wait times (in seconds)
QUICK_COMMAND_WAIT = 1.0  # For info commands like help, tutorial, info, version
SLOW_COMMAND_WAIT = 5.0   # For game state commands like end, choose, play


# Slow commands (change game state, may have animations)
SLOW_COMMANDS = {"end", "choose", "play", "quit", "continue"}