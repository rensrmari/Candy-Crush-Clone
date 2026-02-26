# Contributors: Caleb Le and Clarence Mariano
# Date: 2/19/2026
# Course: CISPROG-5
# Usage: This program simulates a game of Candy Crush. The user will be able to swap candies in a board
#        and clear candies from it to win. In addition to the game's basic behavior, the user will also
#        be able to save their current board for later during their session and save player-related
#        information to a file.

import sys
import game_handler
import file_handler
from utility import *

def main():
    # Define the player and game data.
    player_data = {
        PLAYER_DATA_LEVEL_KEY: 0,
        PLAYER_DATA_DIFFICULTIES_KEY: DATA_DIFFICULTIES.copy(),
        PLAYER_DATA_CANDIES_KEY: DATA_CANDIES.copy()
    }
    game_data = {}
    game_handler.reset_game(game_data)

    # Allow user to choose options.
    while True:
        display_main_menu()
        user_input = prompt_user_input(('P', 'S', 'L', 'D', 'R', 'V', 'Q'), 'Please enter an menu option.')

        if user_input == 'P': # Play
            print('[PLAY]')

            # If a user does not have an empty board, ask them if they would like to continue their previous game.
            if game_handler.in_progress(game_data):
                user_continue = prompt_user_input(('Y', 'N'), 'Previous game data found, continue?\n\t(Y) Yes\n\t(N) No')
                    
            # If user begins new game or the previous game is quit, start with a new board and game data.
            # Additionally, prompt user for difficulty.
            if not game_handler.in_progress(game_data) or user_continue == 'N':
                game_handler.reset_game(game_data)
                game_handler.change_difficulty(game_data)

            # Enter the game.
            game_handler.play(player_data, game_data)
        elif user_input == 'S': # Save
            print('[SAVE SESSION DATA]')
            user_save = prompt_user_input(('Y', 'N'), 'Save session data?\n\t(Y) Yes\n\t(N) No')
            if user_save == 'Y':
                file_handler.save_session(player_data, game_data)
            else:
                print('Your current session has not been saved.')
        elif user_input == 'L': # Load
            print('[LOAD SAVE DATA]')
            file_handler.load_file(player_data, game_data)
        elif user_input == 'D': # Delete
            print('[DELETE SAVE DATA]')
            file_handler.delete_file()
        elif user_input == 'V': # View
            print('[PLAYER DATA]')
            display_player_data(player_data)
            print('Enter anything to return.')
            input(' > ')
        elif user_input == 'R': # Read rules
            print('[RULES]')
            display_rules()
            print('Enter anything to return.')
            input(' > ')
        elif user_input == 'Q': # Quit
            print('Thank you for playing our Candy Crush Clone.')
            sys.exit()

def display_main_menu():
    '''Displays the main menu.'''
    print('\nCANDY CRUSH CLONE')
    print('\t(P) Play Game')
    print('\t(S) Save Session Data')
    print('\t(L) Load Save Data')
    print('\t(D) Delete Save Data')
    print('\t(V) View Player Data')
    print('\t(R) Read Rules')
    print('\t(Q) Quit\n')

def display_player_data(player_data):
    DIFFICULTY_RIGHT_PADDING = 7
    CANDY_RIGHT_PADDING = 10

    '''Displays the player's data.
    Args:
        player_data: A dictionary with the player's data.
    '''
    # Display highest level.
    print(f'{PLAYER_DATA_LEVEL_KEY}: {player_data[PLAYER_DATA_LEVEL_KEY]}')

    # Display difficulties cleared.
    print(PLAYER_DATA_DIFFICULTIES_KEY + ':')
    for difficulty in DATA_DIFFICULTIES:
        print(f'\t{difficulty.ljust(DIFFICULTY_RIGHT_PADDING)}: {player_data[PLAYER_DATA_DIFFICULTIES_KEY][difficulty]}')

    # Display candies crushed and total.
    total_candies = 0
    print(PLAYER_DATA_CANDIES_KEY + ':')
    for key, val in CANDIES_REP.items():
        candy_color = val[CANDIES_REP_COLOR_IDX]
        num_candies = player_data[PLAYER_DATA_CANDIES_KEY][key]
        total_candies += num_candies
        print(f'\t{key.ljust(CANDY_RIGHT_PADDING)} {get_tile_string(candy_color)}: {num_candies}')
    
    print(f'\t{'TOTAL'.ljust(CANDY_RIGHT_PADDING + TILE_SIZE + 1)}: {total_candies}\n')

def display_rules():
    '''Displays the rules.'''
    DIFFICULTY_EFFECT_PADDING = 18

    print('''How to Play:
\t1. Once you press "P", you will be either be able to choose a difficulty or leave where you left off.
\t2. Then, you will be presented with a board of colored tiles, or "candies".
\t3. Your objective is to clear candies by matching three of the same color through adjacent swaps.
\t4. Objectives will determine the condition for clearing the level.
\t\ta. If this objective is not met before a set number of moves has been used, you will lose the level.
\t\tb. 3 losses will result in a game over, which will reset your level clear streak.
\t5. Throughout levels, special candies with unique functions will appear and assist with clearing the level.
\t6. Additionally, blockers will prevent nearby candies from being swapped to their position.''')

    # Display difficulties and their effects.
    print('\nDifficulties:')
    for difficulty in DIFFICULTIES_EFFECTS:
        print(f'\t{difficulty}')
        print(f'\t   {DIFFICULTY_MOVES_KEY.ljust(DIFFICULTY_EFFECT_PADDING)}: {DIFFICULTIES_EFFECTS[difficulty][DIFFICULTY_MOVES_KEY]}')
        print(f'\t   {DIFFICULTY_BLOCKERS_KEY.ljust(DIFFICULTY_EFFECT_PADDING)}: {DIFFICULTIES_EFFECTS[difficulty][DIFFICULTY_BLOCKERS_KEY]}')
        print(f'\t   {DIFFICULTY_OBJECTIVES_KEY.ljust(DIFFICULTY_EFFECT_PADDING)}: {DIFFICULTIES_EFFECTS[difficulty][DIFFICULTY_OBJECTIVES_KEY]}')

    # Display candies and their colors.
    print('\nColors:')
    for key, val in CANDIES_REP.items():
        print(f'\t{get_tile_string(val[CANDIES_REP_COLOR_IDX])} - {key}')

    print()

# Run the program
if __name__ == "__main__"
main()
