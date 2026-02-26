# game_handler.py: Handles gameplay logic and board operations.

import random
import copy
import time
from utility import *

BOARD_SIZE = 10
MINIMUM_POSSIBLE_MOVES_START = 5
MINIMUM_POSSIBLE_MOVES_DURING = 1
CONSEC_NONE = 0
CONSEC_VERTICAL = 1
CONSEC_HORIZONTAL = 2
CONSEC_BOTH = 3

def reset_game(game_data):
    '''Resets game-related data.
    Args:
        game_data: A dictionary with game-related data.
    '''

    game_data[GAME_DATA_BOARD_KEY] = get_empty_board()
    game_data[GAME_DATA_LEVEL_KEY] = 1
    game_data[GAME_DATA_SCORE_KEY] = 0
    game_data[GAME_DATA_IN_PROGRESS_KEY] = False
    game_data[GAME_DATA_DIFFICULTY_KEY] = DIFFICULTIES_EFFECTS['Medium'].copy()

def change_difficulty(game_data):
    '''Prompts the user to change the current difficulty.
    Args:
        game_data: The game data to update with the new difficulty.
    '''
    new_difficulty = ''
    user_difficulty = prompt_user_input(('E', 'M', 'H'), 'Please enter a difficulty.\n\t(E) Easy\n\t(M) Medium\n\t(H) Hard')

    if user_difficulty == 'E':
        new_difficulty = 'Easy'
    elif user_difficulty == 'M':
        new_difficulty = 'Medium'
    else:
        new_difficulty = 'Hard'

    # Copy a difficulty dictionary from DIFFICULTIES_EFFECTS.
    game_data[GAME_DATA_DIFFICULTY_KEY] = DIFFICULTIES_EFFECTS[new_difficulty].copy()

def in_progress(game_data):
    '''Checks if a game is in progress.
    Args:
        game_data: The game data to check.
    Returns:
        boolean: Whether or not a game is in progress.
    '''
    return game_data[GAME_DATA_IN_PROGRESS_KEY]

def get_tile_info(str):
    '''Gets a tile's info based on a supplied string.
    Args:
        str: A string representing a tile on the board.
    Returns:
        (string, string): A tuple containing the string and color of the tile.
    '''
    for val in CANDIES_REP.values():
        if val[CANDIES_REP_STR_IDX] == str[0]: # Just get the first character of the supplied string
            return val

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
        print(f"{col:{TILE_SIZE}}", end=" ")
    print()

    # Print board rows
    for row in range(size):
        print(f"{row:{TILE_SIZE}} ", end="")  # Row numbers
        
        for col in range(size):
            cell = board[row][col]

            if cell == '':
                print(". ", end=" ")
            else:
                print(f"{get_tile_display(get_tile_info(cell)[CANDIES_REP_COLOR_IDX])}", end=" ")

        print()  # New line after each row

    print()

def get_empty_board():
    '''Gets a board's with all empty strings.
    Returns:
        list of lists: A 2D array with all empty strings.
    '''
    return [['' for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

def fill_board(game_data, minimum_moves):
    '''Tries to fill a board's empty spaces based on the number of current blockers and possible moves on the board.
    The board must allow at least a set number of possible moves, and must not contain matches.
    Args:
        game_data: The dictionary containing the board info.
        minimum_moves: The lower limit of permitted moves for a valid board.
    Returns:
        boolean: Whether or not a fill could be made.
    '''
    num_tries = 100
    blockers_to_add = game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_BLOCKERS_KEY]

    while num_tries >= 0:
        temp_board = copy.deepcopy(game_data[GAME_DATA_BOARD_KEY]) # Prevent actual board from being modified
        blockers_left = blockers_to_add

        # Get a random candy's string (not including those of color, line, or area bombs).
        # Blockers are included when more blockers can be added.
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if temp_board[row][col] != '': continue # Ignore filled tiles
                
                choices = [RED, BLUE, GREEN, YELLOW, PURPLE]
                if (blockers_left > 0):
                    choices.append(BLOCKER)
                num_choices = len(choices)

                while num_choices > 0:
                    new_candy = random.choice(choices)
                    temp_board[row][col] = new_candy[CANDIES_REP_STR_IDX]
                    matches = get_adjacent_matches(temp_board, (row, col), set())

                    if check_consecutive(matches):
                        num_tries += 1
                        choices.remove(new_candy)
                        temp_board[row][col] = ''
                    else:
                        # Check if the new candy is a blocker and reduce the running limit.
                        if new_candy == BLOCKER:
                            blockers_left -= 1
                        break
        
        if get_all_matches(temp_board, True) or get_possible_moves(temp_board) < minimum_moves:
            num_tries -= 1
        else:
            game_data[GAME_DATA_BOARD_KEY] = temp_board
            return True
    else:
        return False

def get_possible_directions(board, position):
    '''Gets a list of directions that are allowed from the specified position.
    Args:
        board: The board to check.
        position: The position to check.
    Returns:
        list of tuples: A list of positions.
    '''

    positions = []
    row = position[0]
    col = position[1]
    candy = board[row][col]

    left = col - 1
    right = col + 1
    up = row - 1
    down = row + 1

    if left >= 0:
        positions.append((row, left))
    
    if right < BOARD_SIZE:
        positions.append((row, right))

    if up >= 0:
        positions.append((up, col))

    if down < BOARD_SIZE:
        positions.append((down, col))

    return positions

def get_adjacent_directions(board, position):
    '''Checks left, right, above and below the position, and returns a list of positions within the range of the board
    that contain candies identical to the supplied one.
    Args:
        board: The board to check.
        position: A tuple containing the row and column to check.
    Returns:
        list of tuples: A list of positions.
    '''
    
    valid_positions = get_possible_directions(board, position)
    adj_positions = []
    row = position[0]
    col = position[1]
    candy = board[row][col]

    left = col - 1
    right = col + 1
    up = row - 1
    down = row + 1

    unchecked = ('', COLOR_BOMB[CANDIES_REP_STR_IDX], LINE_BOMB[CANDIES_REP_STR_IDX], AREA_BOMB[CANDIES_REP_STR_IDX], BLOCKER[CANDIES_REP_STR_IDX])

    # Do not consider non-regular candies or empty tiles.
    if board[row][col] in unchecked: return []

    # Iterate through valid directions, appending positions with identical candies.
    for position in valid_positions:
        if board[position[0]][position[1]] == candy:
            adj_positions.append(position)

    return adj_positions

def get_possible_moves(board):
    '''Gets the number of possible moves a player can make, which counts potential successful swaps and unactivated special candies.
    Args:
        board: The board to check.
    Returns:
        int: The number of possible moves a player can make on the board.
    '''
    count = 0

    # Check how many tile swaps can result in adjacent matches exceeding 2.
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            initial_position = (row, col)
            dirs = get_possible_directions(board, (row, col))

            for dir in dirs:
                # Make a temporary swap.
                swap(board, initial_position, dir)

                # Check both initial position and new position for adjacent matches after the potential swap.
                if check_swap_match(board, initial_position, dir):
                    count += 1

                # Return tile to original position.    
                swap(board, dir, initial_position)

    # Count the number of special candies on the board.
    special_candies = (COLOR_BOMB[CANDIES_REP_STR_IDX], LINE_BOMB[CANDIES_REP_STR_IDX], AREA_BOMB[CANDIES_REP_STR_IDX])
    for row in board:
        for cell in row:
            if cell in special_candies:
                count += 1

    return count

def get_adjacent_matches(board, position, checked):
    '''Gets all the adjacent candies identical to the one that is supplied.
    Args:
        board: The board to check.
        position: A tuple of the row and column of the candy to check.
        checked: A set of adjacent candies checked previously.
    Returns:
        list of tuples: A list of positions of adjacent, identical candies.
    '''
    # Create a set with starting position.
    # Needed for when different coordinates have the same adjacent match.
    temp_matches = {position}

    # Get all adjacent directions.
    to_check = set(get_adjacent_directions(board, position))
    checked.add(position)
    
    # Ensure checked positions are not re-checked, then check subsequent matches for the new adjacent positions.
    for prev_position in checked:
        to_check.discard(prev_position)

    for new_position in to_check:
        # Stop recursing when there are no more adjacent matches.
        if len(to_check) < 1:
            return []
        
        temp_matches.update(get_adjacent_matches(board, new_position, checked))

    # Add the first position to complete the list of matches.
    return list(temp_matches)

def get_all_matches(board, stop_at_one=False):
    '''Gets all matches (3+ consecutive candies) on the board.
    Args:
        board: The board to check.
        stop_at_one: Whether or not the function should proceed after finding a match.
    Returns:
        list of lists: A collection of the positions for candies that are identical and adjacent.
    '''
    matches_above_2 = set()
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Check if the position is already in a list of matches (do not have to check).
            for matches in matches_above_2:
                if (row, col) in matches:
                    continue

            adjacent_matches = tuple(get_adjacent_matches(board, (row, col), set())) # Make returned list compatible with set
            match_type = check_consecutive(adjacent_matches)

            if match_type == CONSEC_VERTICAL or match_type == CONSEC_HORIZONTAL or match_type == CONSEC_BOTH:
                matches_above_2.add(adjacent_matches)

                # Prematurely stop if any matches were found.
                if stop_at_one:
                    return list(matches_above_2)

    return list(matches_above_2)

def check_consecutive(matches):
    '''Checks if a given list of matches has candies that are 3+ in a row or column.
    Args:
        matches: A list of matching candies' positions.
    Returns:
        int: An integer representing the status of the matches.
    '''
    # Dictionary that counts same row and column values.
    counts = {
        'Row': {},
        'Col': {}
    }
    horiz = False
    vert = False

    # Add the position's row and column to the count.
    for match in matches:
        row = match[0]
        counts['Row'].setdefault(row, 0)
        counts['Row'][row] += 1

        col = match[1]
        counts['Col'].setdefault(col, 0)
        counts['Col'][col] += 1

    # Check for row and/or column counts over 2.
    for row_count in counts['Row'].values():
        if row_count > 2:
            vert = True
        
    for col_count in counts['Col'].values():
        if col_count > 2:
            horiz = True

    if vert and horiz:
        return CONSEC_BOTH
    elif vert:
        return CONSEC_VERTICAL
    elif horiz:
        return CONSEC_HORIZONTAL
    else:
        return CONSEC_NONE

def swap(board, position1, position2):
    '''Swaps two candies on the board.
    Args:
        board: The board to update.
        position1: A tuple of a row and column.
        position2: Another tuple of a row and column.
    '''
    temp_str = board[position1[0]][position1[1]]
    board[position1[0]][position1[1]] = board[position2[0]][position2[1]]
    board[position2[0]][position2[1]] = temp_str


def check_swap_match(board, position1, position2):
    '''Checks if a swap results in matches.
    Args:
        board: The board to check.
        position1: A tuple of a row and column.
        position2: Another tuple of a row and column.
    Returns:
        boolean: Whether or not the swap results in matches.
    '''
    if check_consecutive(get_adjacent_matches(board, position1, set())) != CONSEC_NONE or check_consecutive(get_adjacent_matches(board, position2, set())) != CONSEC_NONE:
        return True
    else:
        return False
# TODO: implement activation for 3 candies
def activate_special_candy(game_data, candy):
    '''Executes the behavior of the special candy.
    Args:
        game_data: The game data to update.
        candy: The string representing the candy.
    '''

    pass

def get_user_coord(user_input):
    '''Tries to convert user input into a valid coordinate on the board.
    Args:
        user_input: A string of the user's input.
    Returns:
        (boolean, tuple): A boolean representing the validity of the input, and a tuple representing a coordinate.
    '''

    try:
        row, col = map(int, user_input.split())
        return (True, (row, col))
    except:
        return (False, (-1, -1))
# TODO: implement matching + converting here
def update_board(game_data, start_pos=(-1,-1)):
    '''Clears any matches and converts certain candy sequences to special candies, one at a time.
    Also updates game data associated with any cleared candies.
    Args:
        start_pos: An optional position specifying where the updates should start.
    Returns:
        boolean: Whether or not updates have occurred.
    '''
    pass

def drop_candies(board):
    '''Drops candies to their lowest position.
    Args:
        board: The board to update.
    '''
    # Get non-empty tiles in each column.
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - 2, 0, -1): # Go up from the second-to-last row of the column
            if board[row][col] == BLOCKER[CANDIES_REP_STR_IDX]: continue # Ignore blockers
            new_row = row

            # Calculate where the lowest empty space is below the candy.
            while True:
                if new_row + 1 >= BOARD_SIZE or board[new_row + 1][col] != '':
                    break
                new_row += 1

            # Shift the candy to the empty position.
            board[new_row][col] = board[row][col]
            board[row][col] = ''

def play(player_data, game_data):
    '''Handles the gameplay logic.
    Args:
        player_data: The player data to update, containing information about:
            - Highest level
            - Difficulties cleared
            - Candies crushed
        game_data: Data relating to the game itself, containing information about:
            - Board
            - Level
            - Difficulty info (moves left, blocker limit, objective count)
            - Score
    '''
    # Get the game data, update the game status, and fill the board.
    game_data[GAME_DATA_IN_PROGRESS_KEY] = True
    difficulty_data = game_data[GAME_DATA_DIFFICULTY_KEY]
    fill_board(game_data, MINIMUM_POSSIBLE_MOVES_START)

    # Allow user to make moves while available.
    while difficulty_data[DIFFICULTY_MOVES_KEY] > 0:
        # Display game info.
        level_str = f"\n   {GAME_DATA_LEVEL_KEY}: {game_data[GAME_DATA_LEVEL_KEY]}"
        difficulty_str = str(game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_STR_KEY]).rjust(BOARD_SIZE * TILE_SIZE + BOARD_SIZE - 1 - len(level_str))

        print(f"   {level_str}{difficulty_str}")
        display_board(game_data[GAME_DATA_BOARD_KEY])
        print(f"Moves left: {difficulty_data[DIFFICULTY_MOVES_KEY]}")
        print("Enter row and column (example: 1 2)")
        print("Or Q to quit")

        # Get user's input.
        user_input = input(" > ").upper()

        if user_input == 'Q':
            print("Exiting level...")
            return

        valid, (row, col) = get_user_coord(user_input)
        if not valid:
            print("Invalid input.")
            continue

        # Check if the position is within the bounds.
        if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
            print("Out of range.")
            continue

        # Check if the position refers to a blocker.
        candy = game_data[GAME_DATA_BOARD_KEY][row][col]
        if candy == BLOCKER[CANDIES_REP_STR_IDX]:
            print("Unable to perform actions on blocker.")
            continue
        
        # After getting a valid position, check if the position refers to a normal or special candy.
        special_candies = (COLOR_BOMB[CANDIES_REP_STR_IDX], LINE_BOMB[CANDIES_REP_STR_IDX], AREA_BOMB[CANDIES_REP_STR_IDX])
        if candy in special_candies:
            activate_special_candy(candy)
        else:
            # Prompt user for an adjacent position to swap the regular candy.
            new_valid, (new_row, new_col) = get_user_coord(input("Enter another row and column (example: 1 2)\n > ").upper())
            if not new_valid:
                print("Invalid input.")
                continue

            # Check if the position is within the bounds.
            if new_row < 0 or new_row >= BOARD_SIZE or new_col < 0 or new_col >= BOARD_SIZE:
                print("Out of range.")
                continue

            # Verify that the candy is adjacent (must be in same row/col and only one unit away).
            difference = abs(row - new_row) + abs(col - new_col)
            if difference != 1:
                print("Provided candy is not adjacent.")
                continue

            # Check if the position refers to a blocker.
            new_candy = game_data[GAME_DATA_BOARD_KEY][new_row][new_col]
            if new_candy == BLOCKER[CANDIES_REP_STR_IDX]:
                print("Unable to perform actions on blocker.")
                continue

            # Perform a swap with the two positions, reversing it if no matches can be done.
            swap(game_data[GAME_DATA_BOARD_KEY], (row, col), (new_row, new_col))
            success = check_swap_match(game_data[GAME_DATA_BOARD_KEY], (row, col), (new_row, new_col))
            display_board(game_data[GAME_DATA_BOARD_KEY])

            if not success:
                swap(game_data[GAME_DATA_BOARD_KEY], (row, col), (new_row, new_col))
                display_board(game_data[GAME_DATA_BOARD_KEY])
                print("Unsuccessful swap.")
            else:
                # TODO: Update score, objectives, current level, level clear condition, player candies crushed, difficulties cleared
                # Lower the candies, then check for any possible matches to update the board.
                # Stop when no updates can occur when candies are at their lowest.
                while True:
                    drop_candies(game_data[GAME_DATA_BOARD_KEY])
                    updates = update_board()

                    if not updates:
                        break

                fill_board()
                
        # Reduce move count after the move.
        difficulty_data[DIFFICULTY_MOVES_KEY] -= 1

        # TODO: Check if the objective has been met.


    print("Out of moves! Game Over.")
    game_data[GAME_DATA_IN_PROGRESS_KEY] = False
