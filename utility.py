# utility.py: Contains shared constants relating to colors, difficulties, candies, player data, and game data.
#             Also contains functions used among modules.

RED = '\033[41m'
BLUE = '\033[44m'
GREEN = '\033[42m'
YELLOW = '\033[103m'
GREY = '\033[100m'
WHITE = '\033[107m'
CYAN = '\033[46m'
BLACK = '\033[40m'
RESET = '\033[0m'

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

# A list of candy types and colors, with index constants.
CANDIES_REP_TYPE_IDX = 0
CANDIES_REP_COLOR_IDX = 1
CANDIES_REP = [
    ('Red', RED),
    ('Blue', BLUE),
    ('Green', GREEN),
    ('Yellow', YELLOW),
    ('Color Bomb', GREY),
    ('Line Bomb', WHITE),
    ('Area Bomb', CYAN),
    ('Blocker', BLACK)
]

# Keys and dictionaries for player/game data.
PLAYER_DATA_LEVEL_KEY = 'Highest Level'
GAME_DATA_LEVEL_KEY = 'Current Level'
GAME_DATA_DIFFICULTY_KEY = 'Current Difficulty'
DATA_BOARD_KEY = 'Board'
DATA_DIFFICULTIES_KEY = 'Difficulties Cleared'
DATA_CANDIES_KEY = 'Candies Crushed'
DIFFICULTIES_DATA = {
    'Easy': 0,
    'Medium': 0,
    'Hard': 0
}
CANDIES_DATA = {
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
    return f'{color}{' ' * TILE_SIZE}{RESET}'

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