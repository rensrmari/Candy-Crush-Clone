# utility.py: Contains shared constants relating to colors, difficulties, candies, player data, and game data.
#             Also contains functions used among modules.

TILE_SIZE = 2

# Constants for candy representation.
RED = ('Red', 'R', '\033[41m')                 # Red
BLUE = ('Blue', 'B', '\033[44m')               # Blue
GREEN = ('Green', 'G', '\033[42m')             # Green
YELLOW = ('Yellow', 'Y', '\033[103m')          # Yellow
PURPLE = ('Purple', 'P', '\033[105m')          # Purple
COLOR_BOMB = ('Color Bomb', 'C', '\033[107m')  # White
LINE_BOMB = ('Line Bomb', 'L', '\033[100m')    # Grey
AREA_BOMB = ('Area Bomb', 'A', '\033[106m')    # Cyan
BLOCKER = ('Blocker', 'X', '\033[40m')         # Black
EMPTY = ('Empty', '', '')                      # Empty tile
CANDIES_REP_NAME_IDX = 0
CANDIES_REP_STR_IDX = 1
CANDIES_REP_COLOR_IDX = 2
CANDIES_REP = {
    'Red': RED,
    'Blue': BLUE,
    'Green': GREEN,
    'Yellow': YELLOW,
    'Purple': PURPLE,
    'Color Bomb': COLOR_BOMB,
    'Line Bomb': LINE_BOMB,
    'Area Bomb': AREA_BOMB,
    'Blocker': BLOCKER     
}

# Dictionary of dictionaries for game modifiers affected by difficulty, and keys for access.
DIFFICULTY_STR_KEY = 'Difficulty'
DIFFICULTY_MOVES_KEY = 'Max Moves'
DIFFICULTY_BLOCKERS_KEY = 'Max Blockers'
DIFFICULTY_OBJECTIVE_COUNT_KEY = 'Objective Counts'
DIFFICULTIES_EFFECTS = {
    'Easy': {
        DIFFICULTY_STR_KEY: 'Easy',
        DIFFICULTY_MOVES_KEY: 30,
        DIFFICULTY_BLOCKERS_KEY: 0,
        DIFFICULTY_OBJECTIVE_COUNT_KEY: {
            RED: 15,
            BLUE: 15,
            GREEN: 15,
            YELLOW: 15,
            PURPLE: 15,
            COLOR_BOMB: 0,
            LINE_BOMB: 2,
            AREA_BOMB: 0,
            BLOCKER: 0
        }
    },

    'Medium': {
        DIFFICULTY_STR_KEY: 'Medium',
        DIFFICULTY_MOVES_KEY: 25,
        DIFFICULTY_BLOCKERS_KEY: 3,
        DIFFICULTY_OBJECTIVE_COUNT_KEY: {
            RED: 25,
            BLUE: 25,
            GREEN: 25,
            YELLOW: 25,
            PURPLE: 25,
            COLOR_BOMB: 2,
            LINE_BOMB: 3,
            AREA_BOMB: 1,
            BLOCKER: 5
        }
    },

    'Hard': {
        DIFFICULTY_STR_KEY: 'Hard',
        DIFFICULTY_MOVES_KEY: 20,
        DIFFICULTY_BLOCKERS_KEY: 5,
        DIFFICULTY_OBJECTIVE_COUNT_KEY: {
            RED: 35,
            BLUE: 35,
            GREEN: 35,
            YELLOW: 35,
            PURPLE: 35,
            COLOR_BOMB: 3,
            LINE_BOMB: 5,
            AREA_BOMB: 3,
            BLOCKER: 10
        }
    }
}

# Keys and dictionaries for player/game data.
PLAYER_DATA_LEVEL_KEY = 'Highest Level'
PLAYER_DATA_DIFFICULTIES_KEY = 'Difficulties Cleared'
PLAYER_DATA_CANDIES_KEY = 'Candies Crushed'
PLAYER_DATA_DIFFICULTIES = {
    'Easy': 0,
    'Medium': 0,
    'Hard': 0
}
PLAYER_DATA_CANDIES = {
    RED: 0,
    BLUE: 0,
    GREEN: 0,
    YELLOW: 0,
    PURPLE: 0,
    COLOR_BOMB: 0,
    LINE_BOMB: 0,
    AREA_BOMB: 0,
    BLOCKER: 0
}
GAME_DATA_BOARD_KEY = 'Board'
GAME_DATA_LEVEL_KEY = 'Level'
GAME_DATA_DIFFICULTY_KEY = 'Current Difficulty'
GAME_DATA_SCORE_KEY = 'Score'
GAME_DATA_OBJECTIVE_CANDY_KEY = 'Objective Candy'
GAME_DATA_LIVES_KEY = 'Lives'
GAME_DATA_EXISTS_KEY = 'Existing Data'
GAME_DATA_IN_PROGRESS_KEY = 'In Progress'
GAME_DATA_GAME_OVER_KEY = 'Game Over'

# General-use functions.
def get_tile_display(color):
    '''Gets a string that displays a tile with a certain color.
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
            return user_input
        else:
            print('\nInvalid input. ', end='')
