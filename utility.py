# utility.py: Contains shared constants relating to colors, difficulties, candies, player data, and game data.
#             Also contains functions used among modules.

BOARD_SIZE = 10
TILE_SIZE = 2

# Dictionary of dictionaries for game modifiers affected by difficulty, and keys for access.
DIFFICULTY_MOVES_KEY = 'Max Moves'
DIFFICULTY_BLOCKERS_KEY = 'Max Blockers'
DIFFICULTY_OBJECTIVES_KEY = 'Objective Candies'
DIFFICULTIES_EFFECTS = {
    'Easy': {
        DIFFICULTY_MOVES_KEY: 10,
        DIFFICULTY_BLOCKERS_KEY: 0,
        DIFFICULTY_OBJECTIVES_KEY: 15
    },

    'Medium': {
        DIFFICULTY_MOVES_KEY: 13,
        DIFFICULTY_BLOCKERS_KEY: 3,
        DIFFICULTY_OBJECTIVES_KEY: 25
    },

    'Hard': {
        DIFFICULTY_MOVES_KEY: 15,
        DIFFICULTY_BLOCKERS_KEY: 5,
        DIFFICULTY_OBJECTIVES_KEY: 35
    }
}

# Constants for candy representation.
RED = 'R'
BLUE = 'B'
GREEN = 'G'
YELLOW = 'Y'
COLOR_BOMB = 'C'
LINE_BOMB = 'L'
AREA_BOMB = 'A'
BLOCKER = 'X'
CANDIES_REP_STR_IDX = 0
CANDIES_REP_COLOR_IDX = 1
CANDIES_REP = {
    'Red': (RED, '\033[41m'),                # Red
    'Blue': (BLUE, '\033[44m'),              # Blue
    'Green': (GREEN, '\033[42m'),            # Green
    'Yellow': (YELLOW, '\033[103m'),         # Yellow
    'Color Bomb': (COLOR_BOMB, '\033[107m'), # White
    'Line Bomb': (LINE_BOMB, '\033[100m'),   # Grey
    'Area Bomb': (AREA_BOMB, '\033[46m'),    # Cyan
    'Blocker': (BLOCKER, '\033[40m')         # Black
}

# Keys and dictionaries for player/game data.
PLAYER_DATA_LEVEL_KEY = 'Highest Level'
PLAYER_DATA_DIFFICULTIES_KEY = 'Difficulties Cleared'
PLAYER_DATA_CANDIES_KEY = 'Candies Crushed'
GAME_DATA_BOARD_KEY = 'Board'
GAME_DATA_DIFFICULTY_KEY = 'Current Difficulty'
GAME_DATA_LEVEL_KEY = 'Current Level'
GAME_DATA_SCORE_KEY = 'Score'
DATA_IN_PROGRESS_KEY = 'In Progress'
DATA_DIFFICULTIES = {
    'Easy': 0,
    'Medium': 0,
    'Hard': 0
}
DATA_CANDIES = {
    'Red': 0,
    'Blue': 0,
    'Green': 0,
    'Yellow': 0,
    'Color Bomb': 0,
    'Line Bomb': 0,
    'Area Bomb': 0,
    'Blocker': 0
}

# General-use functions.
def get_tile_string(color):
    '''Gets the string representation of a tile with a certain color.
    Args:
        color: A string representing the color of the tile.
    Returns:
        string: A string that displays the tile's color.
    '''
       return f"{color}{' ' * TILE_SIZE}\033[0m"

def prompt_user_input(valid_inputs, prompt):
    '''Continually prompts the user for a valid piece of input.
    Args:
        valid_inputs: A tuple of valid inputs.
        prompt: A message to display.

    Returns:
        string: A valid piece of user input.
    '''
    while True:
        print(prompt)
        user_input = input('> ').strip().upper() # Standardize string with strip and uppercase

        if user_input in valid_inputs:
            print()
            return user_input
        else:
            print('\nInvalid input. ', end='')
