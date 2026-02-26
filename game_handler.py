# game_handler.py: Handles gameplay logic and board operations.

from utility import *

def reset_game(game_data):
    '''Resets game-related data.
    Args:
        game_data: A dictionary with game-related data.
    '''

    game_data[GAME_DATA_BOARD_KEY] = get_empty_board()
    game_data[GAME_DATA_DIFFICULTY_KEY] = 'Medium'
    game_data[GAME_DATA_LEVEL_KEY] = 0
    game_data[GAME_DATA_SCORE_KEY] = 0
    game_data[DATA_IN_PROGRESS_KEY] = True

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

def in_progress(game_data):
    '''Checks if a game is in progress.
    Args:
        game_data: The game data to check.
    Returns:
        boolean: Whether or not a game is in progress.
    '''
    return game_data[DATA_IN_PROGRESS_KEY]

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

def change_difficulty(game_data):
    '''Prompts the user to change the current difficulty.
    Args:
        game_data: The game data to update with the new difficulty.
    '''
    new_difficulty = ''
    user_difficulty = prompt_user_input(('E', 'M', 'H'), 'Please enter a difficulty.\n\t(E) Easy\n\t(M) Medium\n\t(H) Hard')

    if user_difficulty == 'E':
        new_difficulty = 'Easy'
    if user_difficulty == 'M':
        new_difficulty = 'Medium'
    else:
        new_difficulty = 'Hard'

    game_data[GAME_DATA_DIFFICULTY_KEY] = new_difficulty

def play(player_data, game_data):
    board = game_data[GAME_DATA_BOARD_KEY]

    if GAME_DATA_MOVE_KEY not in game_data:
        game_data[GAME_DATA_MOVE_KEY] = 10

    while game_data[GAME_DATA_MOVE_KEY] > 0:

        display_board(board)

        print(f"Moves left: {game_data[GAME_DATA_MOVE_KEY]}")
        print("Enter row and column to clear (example: 1 2)")
        print("Or Q to quit")

        user_input = input(" > ").upper()

        if user_input == 'Q':
            print("Exiting level...")
            return

        try:
            row, col = map(int, user_input.split())
        except:
            print("Invalid input.")
            continue

        if row < 0 or row >= len(board) or col < 0 or col >= len(board):
            print("Out of range.")
            continue

        board[row][col] = random.choice(list(CANDIES_REP.keys()))

        game_data[GAME_DATA_MOVE_KEY] -= 1

    print("Out of moves! Game Over.")
