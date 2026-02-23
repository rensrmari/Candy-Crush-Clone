# game_handler.py: Handles gameplay logic and board operations.

from utility import *

def reset_game(game_data):
    '''Resets game-related data.
    Args:
        game_data: A dictionary with game-related data.
    '''

    game_data[DATA_BOARD_KEY] = get_empty_board()
    # Color Constants
    RED = '\033[41m'
    BLUE = '\033[44m'
    GREEN = '\033[42m'
    YELLOW = '\033[103m'
    GREY = '\033[100m'
    WHITE = '\033[107m'
    CYAN = '\033[46m'
    BLACK = '\033[40m'
    RESET = '\033[0m'

    # Game Constant
    BOARD_SIZE = 10
    TILE_SIZE = 2

 def display_board(board):
    '''
    Displays the game board in a formatted grid.
    
    Args:
        board: A 2D list representing the game board.
    '''

    size = len(board)

    # Print column numbers
    print("\n   ", end="")
    for col in range(size):
        print(f"{col:2}", end=" ")
    print()

    # Print board rows
    for row in range(size):
        print(f"{row:2} ", end="")  # Row numbers
        
        for col in range(size):
            cell = board[row][col]

            if cell == '':
                print(". ", end=" ")
            else:
                print(f"{cell:2}", end=" ")

        print()  # New line after each row

    print() 
    game_data[GAME_DATA_LEVEL_KEY] = 0
    game_data[GAME_DATA_DIFFICULTY_KEY] = 'Medium'
    game_data[DATA_CANDIES_KEY] = CANDIES_DATA.copy()
    game_data[DATA_DIFFICULTIES_KEY] = DIFFICULTIES_DATA.copy()

def is_empty(board):
    '''Checks if a board only has empty strings.
    Args:
        board: A 2D array representing the board.
    
    Returns:
        boolean: Whether or not the board only has empty strings.
    '''
    
    for row in board:
        for cell in row:
            if cell != '':
                return False
    
    return True

def get_empty_board():
    '''Gets a board's with all empty strings.
    Returns:
        list of lists: A 2D array with all empty strings.
    '''
    return [['' for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

def play(player_data, game_data):
    '''Handles the gameplay logic.
    Args:
        player_data: A dictionary to update after the user has finished playing.
        game_data: A dictionary with game-related data.
    '''
    pass
