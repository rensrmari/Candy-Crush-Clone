# Contributors: Caleb Le and Clarence Mariano
# Date: 2/19/2026
# Course: CISPROG-5
# Usage: This program simulates a game of Candy Crush. The user will be able to swap candies in a board
#        and clear candies from it to win. In addition to the game's basic behavior, the user will also
#        be able to save their current board for later during their session and save player-related
#        information to a file.

import sys

BOARD_SIZE = 10
TILE_SIZE = 2
RED = '\033[41m'
BLUE = '\033[44m'
GREEN = '\033[42m'
PURPLE = '\033[45m'
GREY = '\033[100m'
WHITE = '\033[107m'
CYAN = '\033[46m'
BLACK = '\033[40m'
RESET = '\033[0m'
CANDIES_REP_TYPE = 0
CANDIES_REP_COLOR = 1
CANDIES_REP = [
    ('Red', RED),
    ('Blue', BLUE),
    ('Green', GREEN),
    ('Purple', PURPLE),
    ('Color Bomb', GREY),
    ('Line Bomb', WHITE),
    ('Area Bomb', CYAN),
    ('Blocker', BLACK)
]
CANDIES_INFO = {
    'Red': 0,
    'Blue': 0,
    'Green': 0,
    'Purple': 0,
    'Color Bomb': 0,
    'Line Bomb': 0,
    'Area Bomb': 0,
    'Blocker': 0
}

def main():
    # Define an empty board.
    board = get_empty_board()

    # Define the player info.
    player_info = {
        'Highest Level': 0,
        'Total Crushed': 0,
        'Candies Crushed': CANDIES_INFO.copy()
    }

    # Define session-related info.
    session_info = {
        'Current Level': 0,
        'Total Crushed': 0,
        'Candies Crushed': CANDIES_INFO.copy()
    }

    while True:
        # Display the main menu.
        display_main_menu()
        user_input = prompt_user_input(('P', 'S', 'L', 'R', 'Q', 'V'), 'Please enter an menu option.')

        if user_input == 'P': # Play
            # TODO: If a user does not have an empty board, ask them if they would like to continue.


            # Enter the game.
            handle_play(session_info)
        elif user_input == 'S': # Save - TODO
            pass
        elif user_input == 'L': # Load - TODO
            pass
        elif user_input == 'V': # View Data - TODO
            pass
        elif user_input == 'R': # Read rules
            display_rules()
            print('Enter anything to return.')
            input(' > ')
        elif user_input == 'Q': # Quit
            print('\nThank you for playing our Candy Crush Clone.')
            sys.exit()

def display_main_menu():
    '''Displays the main menu.'''
    print('\nCANDY CRUSH CLONE')
    print('\t(P) Play Game')
    print('\t(S) Save Session Data')
    print('\t(L) Load Save File')
    print('\t(V) View Player Info')
    print('\t(R) Read Rules')
    print('\t(Q) Quit\n')

def display_player_info(player_info):
    '''Displays the player's information.
    Args:
        player_info: A dictionary representing the player's information.
    '''
    print(f'Highest level: {player_info['highest_level']}')
    print(f'Total Crushed: {player_info['total_crushed']}')
    print('All Candies Crushed:')
    
    for pair in CANDIES_REP:
        print(f'{CANDIES_REP[CANDIES_REP_TYPE]} {print_tile(CANDIES_REP[CANDIES_REP_COLOR])}: {player_info[CANDIES_REP_TYPE]}')

    print()

def display_rules():
    '''Displays the rules.'''
    print('''
    How to Play:
    \t1. Once you press "P", you will be either be able to choose a difficulty or leave where you left off.
    \t2. Then, you will be presented with a board of colored tiles, or "candies".
    \t3. Your objective is to clear candies by matching three of the same color through adjacent swaps.
    \t4. Objectives will determine the condition for clearing the level.
    \t\ta. If this objective is not met before a set number of moves has been used, you will lose the level.
    \t\tb. 3 losses will result in a game over, which will reset your level clear streak.
    \t5. Throughout levels, special candies with unique functions will appear and assist with clearing the level.
    \t6. Additionally, blockers will prevent nearby candies from being swapped to their position.
    ''')

    print('\nColors:')
    for pair in CANDIES_REP:
        print(f'{print_tile(CANDIES_REP[CANDIES_REP_COLOR])} - {CANDIES_REP[CANDIES_REP_TYPE]}')

    print()
#TODO: FIX COLOR PRINTING
def print_tile(color):
    '''Prints a tile of a specified color.
    Args:
        color: A string representing the color of the tile.
    '''
    print(f'{color}{' ' * TILE_SIZE}{RESET}')

def prompt_user_input(valid_args, prompt):
    '''Prompts the user for specific input.
    Args:
        valid_args: A tuple of valid arguments.
        prompt: A message to display.

    Returns:
        string: A valid piece of user input.
    '''
    while True:
        print(prompt)
        user_input = input('> ').strip().upper() # Standardize string with strip and uppercase

        if user_input in valid_args:
            return user_input
        else:
            print('\nInvalid input. ', end='')

def get_empty_board():
    '''Gets a board of all empty strings.
    Returns:
        list of lists: 2D array of empty strings.
    '''
    return [['' for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

def is_empty(board):
    '''Checks if a board only has empty strings.
    Args:
        board: A 2D array representing the board.
    
    Returns:
        boolean: Whether or not the board only has empty strings.
    '''
    
    for row in board:
        for col in row:
            if board[row][col] != '':
                return False
    
    return True

def handle_play(session_info):
    '''Handles the gameplay logic.
    Args:
        session_info: A dictionary representing the information for the current session.
    '''
    pass

# Run the program
main()