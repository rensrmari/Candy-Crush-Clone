# game_handler.py: Handles gameplay logic and board operations.

from utility import *

def reset_game(board, game_data):
    '''Resets the provided board and game-related data.
    Args:
        board: A 2D array to update.
        game_data: A dictionary with game-related data.
    '''

    set_empty_board(board)
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

def set_empty_board(board):
    '''Sets a board's cells to all empty strings.
    Args:
        board: A 2D array to update.
    '''
    for row in board:
        for cell in row:
            cell = ''

def play(board, player_data, game_data):
    '''Handles the gameplay logic.
    Args:
        board: A 2D array to update.
        player_data: A dictionary to update after the user has finished playing.
        game_data: A dictionary with game-related data.
    '''
    pass