# game_handler.py: Handles gameplay logic and board operations.

import random
import copy
import time
from utility import *

BOARD_SIZE = 10
DELAY = 0.5

MINIMUM_POSSIBLE_MOVES_START = 5
MINIMUM_POSSIBLE_MOVES_DURING = 2

CONSEC_NONE = 0
CONSEC_VERTICAL = 1
CONSEC_HORIZONTAL = 2
CONSEC_BOTH = 3

def reset_game(game_data, cont):
    '''Resets game-related data.
    Args:
        game_data: A dictionary with game-related data.
        cont: Whether or not certain data from the previous game will be saved.
    '''

    game_data[GAME_DATA_IN_PROGRESS_KEY] = cont

    if not cont: # Fresh start variables
        game_data[GAME_DATA_LEVEL_KEY] = 1
        game_data[GAME_DATA_SCORE_KEY] = 0

    # Always generate these variables for a new game, regardless of whether it is a complete reset.
    game_data[GAME_DATA_BOARD_KEY] = get_empty_board()
    game_data[GAME_DATA_LIVES_KEY] = 3
    game_data[GAME_DATA_DIFFICULTY_KEY] = DIFFICULTIES_EFFECTS['Medium'].copy()
    game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_OBJECTIVES_KEY][OBJECTIVES_STR_IDX] = get_objective()

def get_objective():
    '''Randomly generates an objective candy.'''
    choices = (RED, BLUE, GREEN, YELLOW, PURPLE)
    return random.choice(choices)[CANDIES_REP_STR_IDX]

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

def is_empty(board):
    '''Checks if a board has all empty strings.
    Args:
        board: The board to check.
    Returns:
        boolean: Whether or not the board has all empty strings.
    '''
    for row in board:
        for cell in row:
            if cell != '':
                return False
            
    return True

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

                    if check_consecutive(matches)[0] != CONSEC_NONE:
                        num_choices -= 1
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
            match_type = check_consecutive(adjacent_matches)[0]

            if match_type == CONSEC_VERTICAL or match_type == CONSEC_HORIZONTAL or match_type == CONSEC_BOTH:
                matches_above_2.update(adjacent_matches)

                # Prematurely stop if any matches were found.
                if stop_at_one:
                    return list(matches_above_2)

    return list(matches_above_2)

def check_consecutive(matches):
    '''Checks if a given list of matches has candies that are 3+ in a row or column.
    Args:
        matches: A list of matching candies' positions.
    Returns:
        (int, list): An integer representing the status of the matches as well as a list of positions that contain a certain sequence.
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

    # Check for row and/or column counts over 2, as well as the maximum row/column with the maximum consecutive matches.
    max_row = 0
    max_row_val = 0
    max_col = 0
    max_col_val = 0
    for row, row_count in counts['Row'].items():
        if row_count > max_row_val:
            max_row = row
            max_row_val = row_count
        if max_row_val > 2:
            horiz = True
        
    for col, col_count in counts['Col'].items():
        if col_count > max_col_val:
            max_col = col
            max_col_val = col_count
        if max_col_val > 2:
            vert = True

    # Get the positions of the row/col with the maximum consecutive matches.
    max_row_positions = []
    max_col_positions = []
    for match in matches:            
        if match[0] == max_row:
            max_row_positions.append(match)
        if match[1] == max_col:
            max_col_positions.append(match)

    if vert and horiz:
        to_add = set()
        to_add.update(max_row_positions)
        to_add.update(max_col_positions)
        return (CONSEC_BOTH, list(to_add))
    elif vert:
        return (CONSEC_VERTICAL, max_col_positions)
    elif horiz:
        return (CONSEC_HORIZONTAL, max_row_positions)
    else:
        return (CONSEC_NONE, [])

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
    if check_consecutive(get_adjacent_matches(board, position1, set()))[0] != CONSEC_NONE or check_consecutive(get_adjacent_matches(board, position2, set()))[0] != CONSEC_NONE:
        return True
    else:
        return False
# TODO: implement activation for 3 candies
def activate_special_candy(game_data, candy):
    '''Gets a list of candies to clear based on the special candy.
    Args:
        game_data: The game data to update.
        candy: The string representing the candy.
    Returns:
        list of tuples: A list of positions that represent the special candy's future clears.
    '''

    # Call clear_candies() somewhere

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
    
def clear_candies(player_data, game_data, positions):
    '''Updates the data of the player and the game based on the supplied candies, which are to be cleared.
    Also clears blockers if they are adjacent to the matched candies.
    Args:
        player_data: The player data to update.
        game_data: The game data to update.
        positions: The positions that will be cleared.
    '''

    # Iterate through positions.
    for position in positions:
        cell = game_data[GAME_DATA_BOARD_KEY][position[0]][position[1]]
        cleared = [position]

        # Player and game: Update the candies crushed for blockers, and increase the blocker limit due to removal.
        adjacent_pos = get_possible_directions(game_data[GAME_DATA_BOARD_KEY], position)
        for pos in adjacent_pos:
            if get_tile_info(game_data[GAME_DATA_BOARD_KEY][pos[0]][pos[1]]) == BLOCKER:
                if game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_BLOCKERS_KEY] < DIFFICULTIES_EFFECTS[game_data[GAME_DATA_DIFFICULTY_KEY]][DIFFICULTY_BLOCKERS_KEY]:
                    game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_BLOCKERS_KEY] += 1
                    cleared.append(pos)

        # Game: Update the objective counter.

        # TODO: FIX OBJECTIVES UPDATE, DROP_CANDIES() 
        if cell == game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_OBJECTIVES_KEY][OBJECTIVES_STR_IDX]:
            game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_MOVES_KEY] -= 1


        # Player: Update the candies crushed.
        candy = get_tile_info(cell)
        for key, val in CANDIES_REP.items():
            if val == candy:
                player_data[PLAYER_DATA_CANDIES_KEY][key] += 1
                break

        # Remove strings of removed tiles from the board.
        for pos in cleared:
            game_data[GAME_DATA_BOARD_KEY][pos[0]][pos[1]] = ''

        # Update the score.
        game_data[GAME_DATA_SCORE_KEY] += len(cleared)

def get_clearable_positions(board, positions):
    '''Returns a list of positions that contains as many supplied positions as possible before going out of range/blocker.
    Args:
        positions: The positions to potentially modify.
    Returns:
        list: The positions that are allowable given the board.
    '''
    pass

# used initially, and maybe by update_board in iteration
def update_position(player_data, game_data, position):
    ''' Updates a position on the board by changing it into a special candy or matching it.
    Args:
        player_data: The player data that will be updated.
        game_data: The game data that will be updated.
        position: A tuple representing the position of the board to update.
    Returns:
        list of lists: A list containing all the positions that were matched.
    '''
        
    status, matches = check_consecutive(get_adjacent_matches(game_data[GAME_DATA_BOARD_KEY], position, set()))
    matches_count = len(matches)
    row, col = position

    # Check for color bomb (5 consecutive candies).
    # Append the first character of the candy it is associated with.
    if (status == CONSEC_VERTICAL or status == CONSEC_HORIZONTAL) and matches_count >= 5:
        candy = game_data[GAME_DATA_BOARD_KEY][row][col]
        game_data[GAME_DATA_BOARD_KEY][row][col] = COLOR_BOMB[CANDIES_REP_STR_IDX] + candy

    # Check for area bomb (3+ candies in both directions).
    elif status == CONSEC_BOTH and matches_count >= 3:
        game_data[GAME_DATA_BOARD_KEY][row][col] = AREA_BOMB[CANDIES_REP_STR_IDX]

    # Check for line bomb (4 consecutive candies).
    # Append a character representing the direction of the line, based on the consecutive matches.
    elif (status == CONSEC_VERTICAL or status == CONSEC_HORIZONTAL) and matches_count >= 4:
        game_data[GAME_DATA_BOARD_KEY][row][col] = LINE_BOMB[CANDIES_REP_STR_IDX] + 'V'

    clear_candies(player_data, game_data, matches)
    return matches

def update_board(player_data, game_data):
    '''Clears any matches and converts certain candy sequences to special candies.CLEAR AND REPLACE. (SAME TIME)
    Args:
        player_data: The player data to update.
        game_data: The game data to update.
    Returns:
        boolean: Whether or not updates have occurred.
    '''
    checked = set()
    all_matches = get_all_matches(game_data[GAME_DATA_BOARD_KEY], False)
    
    for match in all_matches:
        if match in checked: continue
        matches = tuple(update_position(player_data, game_data, match))
        checked.update(matches)

    # Display board after all the board updates.
    display_board(game_data[GAME_DATA_BOARD_KEY])

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
    
    display_board(board)

def update_highest_level(player_data, level):
    '''Updates the player's highest level with a new level if it is surpassed.
    Args:
        player_data: The player data whose highest level is to be updated.
        level: The level to check.
    Returns:
        boolean: Whether or not the new level beats the previous highest level.
    '''
    if level > player_data[PLAYER_DATA_LEVEL_KEY]:
        player_data[PLAYER_DATA_LEVEL_KEY] = level
        return True
    
    return False

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
            - Lives
            - Progress
    '''
    # Get the game data, update the game status, and fill the board.
    game_data[GAME_DATA_IN_PROGRESS_KEY] = True
    difficulty_data = game_data[GAME_DATA_DIFFICULTY_KEY]
    fill_board(game_data, MINIMUM_POSSIBLE_MOVES_START)

    # Allow user to make moves while available.
    while difficulty_data[DIFFICULTY_MOVES_KEY] > 0:
        # Display game info.
        level_str = f"{GAME_DATA_LEVEL_KEY}: {game_data[GAME_DATA_LEVEL_KEY]}".rjust(BOARD_SIZE * TILE_SIZE + BOARD_SIZE - 1)
        difficulty_str = str(game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_STR_KEY])
        score_str = f"{GAME_DATA_SCORE_KEY}: {game_data[GAME_DATA_SCORE_KEY]}".rjust(BOARD_SIZE * TILE_SIZE + BOARD_SIZE - 1 - len(difficulty_str))

        print(f"   {level_str}")
        print(f"   {difficulty_str}{score_str}")
        display_board(game_data[GAME_DATA_BOARD_KEY])
        print(f"{GAME_DATA_LIVES_KEY}: {game_data[GAME_DATA_LIVES_KEY]}")
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
        update = False
        special_candies = (COLOR_BOMB[CANDIES_REP_STR_IDX], LINE_BOMB[CANDIES_REP_STR_IDX], AREA_BOMB[CANDIES_REP_STR_IDX])
        if candy in special_candies:
            activate_special_candy(candy)
            update = True
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
                time.sleep(DELAY)
                print("Unsuccessful swap.")
            else:
                update = True
            
            # Update the board if a move activated a special candy or resulted in matches.
            if update:
                # Lower the candies, then check for any possible matches to update the board.
                # Stop when no updates can occur when candies are at their lowest.
                update_position(player_data, game_data, (row, col))
                update_position(player_data, game_data, (new_row, new_col))
                time.sleep(DELAY)
                display_board(game_data[GAME_DATA_BOARD_KEY])

                while True:
                    drop_candies(game_data[GAME_DATA_BOARD_KEY])
                    time.sleep(DELAY)
                    updates = update_board(player_data, game_data)
                    time.sleep(DELAY)

                    if not updates:
                        break

                fill_board(game_data, MINIMUM_POSSIBLE_MOVES_DURING)
                
        # Reduce move count after the move.
        difficulty_data[DIFFICULTY_MOVES_KEY] -= 1

        # Check if the objective has been met.
        if game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_OBJECTIVES_KEY] == 0:
            level = game_data[GAME_DATA_LEVEL_KEY]
            print(f"Cleared Level {level} - {"Personal Best!" if update_highest_level(player_data, level) else ""}")
            break
    else:
        # Loss logic (output lose message, decrease lives, and check number of lives left).
        game_data[GAME_DATA_LIVES_KEY] -= 1
        print(f"Out of moves! Live count: {game_data[GAME_DATA_LIVES_KEY]}.")

        if game_data[GAME_DATA_LIVES_KEY] <= 0:
            print("Out of lives - Game Over!")
            game_data[GAME_DATA_IN_PROGRESS_KEY] = False
