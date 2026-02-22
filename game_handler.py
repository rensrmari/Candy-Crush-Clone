# game_handler.py: Handles gameplay logic and board operations.

from utility import *

def reset_game(game_data):
    '''Resets game-related data.
    Args:
        game_data: A dictionary with game-related data.
    '''

    game_data[DATA_BOARD_KEY] = get_empty_board()
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