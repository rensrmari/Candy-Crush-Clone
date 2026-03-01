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
        PLAYER_DATA_DIFFICULTIES_KEY: PLAYER_DATA_DIFFICULTIES.copy(),
        PLAYER_DATA_CANDIES_KEY: PLAYER_DATA_CANDIES.copy()
    }
    game_data = {}
    game_handler.reset_game(game_data, False)

    # Allow user to choose options.
    while True:
        display_main_menu()
        user_input = prompt_user_input(('P', 'S', 'L', 'D', 'R', 'V', 'Q'), 'Please enter an menu option.')
        
        # Play
        if user_input == 'P':
            print('\n[PLAY]')
            user_continue = ''

            # If a user has game data and still has lives left, ask them if they would like to continue their previous game.
            can_continue = game_handler.exists(game_data)
            if can_continue:
                user_continue = prompt_user_input(('Y', 'N'), 'Unfinished game found, continue?\n\t(Y) Yes\n\t(N) No')
                print()
            
            # If user opts to continue and does not have a running game, perform a soft reset.
            if user_continue == 'Y' and not game_handler.in_progress(game_data):
                game_handler.reset_game(game_data, True)
                game_handler.change_difficulty(game_data)

            # If user begins a new game or they have lost all their lives, start with a new board and game data.
            if user_continue == 'N' or not can_continue or game_handler.game_over(game_data):
                game_handler.reset_game(game_data, False)
                game_handler.change_difficulty(game_data)

            # Enter the game.
            game_handler.play(player_data, game_data)

        # Save
        elif user_input == 'S':
            print('\n[SAVE SESSION DATA]')
            user_save = prompt_user_input(('Y', 'N'), 'Save session data?\n\t(Y) Yes\n\t(N) No')
            if user_save == 'Y':
                file_handler.save_session(player_data, game_data)
            else:
                print('Your current session has not been saved.')

        # Load
        elif user_input == 'L':
            print('\n[LOAD SAVE DATA]')
            file_handler.load_file(player_data, game_data)

        # Delete
        elif user_input == 'D':
            print('\n[DELETE SAVE DATA]')
            file_handler.delete_file()

        # View player data
        elif user_input == 'V':
            print('\n[PLAYER DATA]')
            display_player_data(player_data)
            print('Enter anything to return.')
            input(' > ')

        # Read rules
        elif user_input == 'R':
            print('\n[RULES]')
            display_rules()
            print('Enter anything to return.')
            input(' > ')

        # Quit
        elif user_input == 'Q':
            print('\nThank you for playing our Candy Crush Clone.')
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

def get_candy_data(candy, data, padding):
    '''Gets a string containing candy data.
    Args:
        candy: The candy whose data will be printed.
        data: The number associated with the candy.
        padding: How much padding the text should have.
    '''
    return f'{candy[CANDIES_REP_NAME_IDX].ljust(padding)} {get_tile_display(candy[CANDIES_REP_COLOR_IDX])} - {data}'

def display_player_data(player_data):
    DIFFICULTY_RIGHT_PADDING = 6
    CANDY_RIGHT_PADDING = 10

    '''Displays the player's data.
    Args:
        player_data: A dictionary with the player's data.
    '''
    # Display highest level.
    print(f'{PLAYER_DATA_LEVEL_KEY}: {player_data[PLAYER_DATA_LEVEL_KEY]}')

    # Display difficulties cleared.
    print(f'\n{PLAYER_DATA_DIFFICULTIES_KEY}:')
    for difficulty in PLAYER_DATA_DIFFICULTIES:
        print(f'\t{difficulty.ljust(DIFFICULTY_RIGHT_PADDING)} - {player_data[PLAYER_DATA_DIFFICULTIES_KEY][difficulty]}')

    # Display candies crushed and total.
    player_candies = player_data[PLAYER_DATA_CANDIES_KEY]
    total_candies = 0
    print(f'\n{PLAYER_DATA_CANDIES_KEY}:')
    for candy, num_candies in player_candies.items():
        total_candies += num_candies
        print(f'\t{get_candy_data(candy, num_candies, CANDY_RIGHT_PADDING)}')
    
    print(f"\t{'TOTAL'.ljust(CANDY_RIGHT_PADDING + TILE_SIZE + 1)} - {total_candies}\n")

def display_rules():
    '''Displays the rules.'''
    CANDY_RIGHT_PADDING = 10

    print('''How to Play:
\t1. After entering "P", you will be either be able to choose a difficulty or leave where you left off.
\t2. Then, you will be presented with a board of colored tiles, or "candies".
\t3. Your objective is to clear candies by matching three of the same color through adjacent swaps.
\t4. Objectives will determine the condition for clearing the level.
\t\ta. If this objective is not met before a set number of moves has been used, you will lose the level.
\t\tb. 3 losses will result in a game over, which will reset your level clear streak.
\t5. Matching candies in certain shapes will form useful special candies.
\t\ta. Color Bomb (5+ candies in a line): Clears all instances of the previously matched color.
\t\tb. Line Bomb (4+ candies in a line): Clears either the row or the column it is in.
\t\t\ti. The cleared section of the board will correspond to the shape that formed the Line Bomb.
\t\tc. Area Bomb (3+ candies in both directions): Clears all candies within its radius.
\t6. Additionally, blockers will prevent nearby candies from being swapped to their position.
\t\ta. They may be cleared by matching adjacent candies or through special candies.''')

    # Display difficulties and their effects.
    print('\nDifficulties:')
    for difficulty in DIFFICULTIES_EFFECTS:
        print(f'\t{difficulty}')
        print(f'\t   {DIFFICULTY_MOVES_KEY}: {DIFFICULTIES_EFFECTS[difficulty][DIFFICULTY_MOVES_KEY]}')
        print(f'\t   {DIFFICULTY_BLOCKERS_KEY}: {DIFFICULTIES_EFFECTS[difficulty][DIFFICULTY_BLOCKERS_KEY]}')
        print(f'\t   {DIFFICULTY_OBJECTIVE_COUNT_KEY}')

        for candy, objective_count in DIFFICULTIES_EFFECTS[difficulty][DIFFICULTY_OBJECTIVE_COUNT_KEY].items():
            print(f'\t      {get_candy_data(candy, objective_count, CANDY_RIGHT_PADDING)}')
            
    print()

# Run the program
if __name__ == "__main__":
    main()
