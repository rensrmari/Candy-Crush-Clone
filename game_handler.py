# game_handler.py: Handles gameplay logic and board operations.

import random
import copy
import time
from utility import *

BOARD_SIZE = 10
DELAY = 1.5

MINIMUM_POSSIBLE_MOVES_START = 5
MINIMUM_POSSIBLE_MOVES_DURING = 2

CONSEC_NONE = 0
CONSEC_VERTICAL = 1
CONSEC_HORIZONTAL = 2
CONSEC_BOTH = 3

LINE_BOMB_VERTICAL = 'V'
LINE_BOMB_HORIZONTAL = 'H'

AREA_BOMB_RADIUS = 1

def reset_game(game_data, cont):
    '''Resets game-related data.
    Args:
        game_data: A dictionary with game-related data.
        cont: Whether or not certain data from the previous game will be used.
    '''
    # For when a game has truly been reset.
    # Otherwise, simply generate a new objective candy (previous difficulty and other data will be used).
    if not cont:
        game_data[GAME_DATA_EXISTS_KEY] = False
        game_data[GAME_DATA_LEVEL_KEY] = 1
        game_data[GAME_DATA_SCORE_KEY] = 0
        game_data[GAME_DATA_LIVES_KEY] = 3
    else:
        game_data[GAME_DATA_OBJECTIVE_CANDY_KEY] = get_objective(game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_STR_KEY])

    # Set game statuses.
    game_data[GAME_DATA_IN_PROGRESS_KEY] = cont
    game_data[GAME_DATA_GAME_OVER_KEY] = False

    # Always generate a board for a new game.
    game_data[GAME_DATA_BOARD_KEY] = get_empty_board()

def get_objective(difficulty):
    '''Randomly generates an objective candy according to a difficulty.
    Args:
        difficulty: A string representing the difficulty of the game.
    Returns:
        (string, string): A tuple representing a valid objective candy.
    '''
    candy = ('', '')
    while True:
        choices = (RED, BLUE, GREEN, YELLOW, PURPLE, COLOR_BOMB, LINE_BOMB, AREA_BOMB, BLOCKER)
        candy = random.choice(choices)

        # Check if this objective candy is allowed to be chosen.
        if DIFFICULTIES_EFFECTS[difficulty][DIFFICULTY_OBJECTIVE_COUNT_KEY][candy] != 0:
            break

    return candy

def change_difficulty(game_data):
    '''Prompts the user to change the current difficulty, which also sets the objective candy.
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

    # Copy a difficulty dictionary from DIFFICULTIES_EFFECTS and set an objective candy using it.
    game_data[GAME_DATA_DIFFICULTY_KEY] = DIFFICULTIES_EFFECTS[new_difficulty].copy()
    game_data[GAME_DATA_OBJECTIVE_CANDY_KEY] = get_objective(new_difficulty)

def exists(game_data):
    '''Checks if there exists game data, regardless of whether or not a game is in progress or has ended.
    Args:
        game_data: The game data to check.
    Returns:
        boolean: Whether or not game data exists.
    '''
    return game_data[GAME_DATA_EXISTS_KEY]

def in_progress(game_data):
    '''Checks if a game is in progress.
    Args:
        game_data: The game data to check.
    Returns:
        boolean: Whether or not a game is in progress.
    '''
    return game_data[GAME_DATA_IN_PROGRESS_KEY]

def game_over(game_data):
    '''Checks if the game does not have any more available lives.
    Args:
        game_data: The game data to check.
    Returns:
        boolean: Whether or not the game is over.
    '''
    return game_data[GAME_DATA_GAME_OVER_KEY]

def get_pos_info(board, position):
    '''Gets a tile's info based on a supplied position.
    Args:
        board: The board to check.
        position: The position to check.
    Returns:
        (string, string): A tuple containing the string and color of the tile.
    '''
    return get_tile_info(board[position[0]][position[1]])

def get_tile_info(str):
    '''Gets a tile's info based on a supplied string.
    Args:
        str: A string representing a tile on the board.
    Returns:
        (string, string): A tuple containing the string and color of the tile.
    '''
    if not str:
        return EMPTY

    for val in CANDIES_REP.values():
        if val[CANDIES_REP_STR_IDX] == str[0]: # Just get the first character of the supplied string
            return val

def display_board(board):
    '''Displays the game board in a formatted grid.
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
        
        # Update board if the fill is valid.
        if get_all_matches(temp_board, True) or get_possible_moves(temp_board) < minimum_moves:
            num_tries -= 1
        else:
            game_data[GAME_DATA_BOARD_KEY] = temp_board
            game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_BLOCKERS_KEY] = blockers_left
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
    cell = board[row][col]

    unchecked = (EMPTY, COLOR_BOMB, LINE_BOMB, AREA_BOMB, BLOCKER)

    # Do not consider non-regular candies or empty tiles.
    if get_tile_info(board[row][col]) in unchecked: return []

    # Iterate through valid directions, appending positions with identical candies.
    for position in valid_positions:
        if board[position[0]][position[1]] == cell:
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
    special_candies = (COLOR_BOMB, LINE_BOMB, AREA_BOMB)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if get_tile_info(board[row][col]) in special_candies:
                count += 1

    return count

def get_adjacent_matches(board, position, checked):
    '''Gets all the adjacent candies identical to the one that is supplied.
    Args:
        board: The board to check.
        position: A tuple of the row and column of the candy to check.
        checked: A set of adjacent candies checked previously.
    Returns:
        list of tuples: The positions of adjacent, identical candies.
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
    return temp_matches

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

            adjacent_matches = tuple(get_adjacent_matches(board, (row, col), set()))
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

def attempt_swap(player_data, game_data, position1, position2):
    '''Checks if a swap between two positions results in matches.
    If so, updates the player's data and the game's state accordingly, displaying the changes.
    Args:
        player_data: The player data to update.
        game_data: The game data to update.
        position1: One of the positions involved in the swap.
        position2: Another position involved in the swap.
    Returns:
        boolean: Whether or not the swap resulted in matches.
    '''
    board = game_data[GAME_DATA_BOARD_KEY]
    swap(board, position1, position2)
    success = check_swap_match(board, position1, position2)
    display_board(board)
    time.sleep(DELAY)

    # Display the result of the swap.
    if not success:
        swap(board, position1, position2)
        display_board(board)
        print("Unsuccessful swap.")
        return False
    else:
        # Process the matches for each position.
        initial_points = 0
        initial_points += update_position(player_data, game_data, position1)[0]
        initial_points += update_position(player_data, game_data, position2)[0]
        display_board(game_data[GAME_DATA_BOARD_KEY])
        display_points(initial_points)
        return True

def clear_candies(player_data, game_data, positions):
    '''Updates the data of the player and the game based on the supplied candies, which are to be cleared.
    Also clears blockers if they are adjacent to the matched candies.
    Args:
        player_data: The player data to update.
        game_data: The game data to update.
        positions: The positions that will be cleared.
    Returns:
        int: The number of points earned from the clears.
    '''
    points = 0

    # Clear candies at the positions as well as nearby blockers.
    for position in positions:
        board = game_data[GAME_DATA_BOARD_KEY]
        pos_to_clear = [position]

        # Add adjacent blockers to the positions that will be removed, and update the board's maximum blockers for each blocker found.
        adjacent_pos = get_possible_directions(board, position)
        for pos in adjacent_pos:
            if get_pos_info(board, pos) == BLOCKER:
                game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_BLOCKERS_KEY] += 1
                pos_to_clear.append(pos)

        # Update the objective counter and player's crushed candies according to the list of cleared candies.
        # Then, clear the candy from the board.
        for pos in pos_to_clear:
            candy = get_pos_info(board, pos)
            if candy == game_data[GAME_DATA_OBJECTIVE_CANDY_KEY]:
                game_data[GAME_DATA_DIFFICULTY_KEY][DIFFICULTY_OBJECTIVE_COUNT_KEY][candy] -= 1

            # Find a candy that matches the one at the position.
            player_data[PLAYER_DATA_CANDIES_KEY][candy] += 1
            
            # Remove the string at this position from the board.
            board[pos[0]][pos[1]] = ''

        # Update the score.
        points += len(pos_to_clear)

    game_data[GAME_DATA_SCORE_KEY] += points
    return points

def display_points(points):
    '''Displays additional points.
    Args:
        points: The number of points that were added.
    '''
    print(f'+{points} points!\n')

def activate_special_candy(player_data, game_data, candy, position):
    '''Gets a list of candies to clear based on the special candy.
    Args:
        player_data: The player data to update.
        game_data: The game data to update.
        candy: The type of special candy.
        position: The position of the special candy.
    '''
    board = game_data[GAME_DATA_BOARD_KEY]
    positions = set()
    row = position[0]
    col = position[1]

    # Get the string of the special candy.
    candy_str = board[row][col]
    
    # Color bomb (clear all instances of a certain color).
    if candy == COLOR_BOMB:
        color = candy_str[1]

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == color:
                    positions.add((row, col))

    # Line bomb (clear the candies in a vertical or horizontal line).
    elif candy == LINE_BOMB:
        direction = candy_str[1]

        if direction == LINE_BOMB_VERTICAL:
            for r in range(BOARD_SIZE):
                positions.add((r, col))
        else:
            for c in range(BOARD_SIZE):
                positions.add((row, c))

    # Area bomb (clear candies in a given radius).
    else:
        for r in range(row - AREA_BOMB_RADIUS, row + AREA_BOMB_RADIUS + 1):
            for c in range(col - AREA_BOMB_RADIUS, col + AREA_BOMB_RADIUS + 1):
                positions.add((r, c))
        
        # Remove positions that are out of range.
        to_remove = []
        for (r, c) in positions:
            if not within_bounds(r, c):
                to_remove.append((r, c))
        
        for p in to_remove:
            positions.remove(p)

    positions.add(position)
    points = clear_candies(player_data, game_data, positions)
    display_board(board)
    display_points(points)

    
def update_position(player_data, game_data, position):
    ''' Updates a position on the board by matching it or changing it into a special candy, under certain conditions.
    Args:
        player_data: The player data that will be updated.
        game_data: The game data that will be updated.
        position: A tuple representing the position of the board to update.
    Returns:
        (int, list of lists): A tuple containing the points earned as well all the positions that were matched.
    '''
    board = game_data[GAME_DATA_BOARD_KEY]
    row, col = position
    cell = board[row][col]

    status, matches = check_consecutive(get_adjacent_matches(board, position, set()))
    matches_count = len(matches)
    points = clear_candies(player_data, game_data, matches)

    # Check for color bomb (5 consecutive candies).
    # Append the first character of the candy it is associated with.
    if (status == CONSEC_VERTICAL or status == CONSEC_HORIZONTAL) and matches_count >= 5:
        board[row][col] = COLOR_BOMB[CANDIES_REP_STR_IDX] + cell # Append candy's character to color bomb

    # Check for area bomb (3+ candies in both directions).
    elif status == CONSEC_BOTH and matches_count >= 3:
        board[row][col] = AREA_BOMB[CANDIES_REP_STR_IDX]
        
    # Check for line bomb (4 consecutive candies).
    # Append a character representing the direction of the line, based on the consecutive matches.
    elif status == CONSEC_VERTICAL and matches_count >= 4:
        board[row][col] = LINE_BOMB[CANDIES_REP_STR_IDX] + LINE_BOMB_VERTICAL
    elif status == CONSEC_HORIZONTAL and matches_count >= 4:
        board[row][col] = LINE_BOMB[CANDIES_REP_STR_IDX] + LINE_BOMB_HORIZONTAL

    return (points, matches)

def update_board(player_data, game_data):
    '''Clears any matches and converts certain candy sequences to special candies, displaying the board's status after.
    Args:
        player_data: The player data to update.
        game_data: The game data to update.
    Returns:
        boolean: Whether or not updates have occurred.
    '''
    updates = False
    points = 0
    checked = set()
    all_matches = get_all_matches(game_data[GAME_DATA_BOARD_KEY], False)
    
    for match in all_matches:
        if match in checked: continue
        pos_status = update_position(player_data, game_data, match)
        checked.update(pos_status[1])
        points += pos_status[0]
        updates = True

    # Display board and points after all the board updates.
    if updates:
        display_board(game_data[GAME_DATA_BOARD_KEY])
        display_points(points)

    return updates

def drop_candies(board):
    '''Drops candies to their lowest position.
    Args:
        board: The board to update.
    '''
    shifts = False

    # Get non-empty tiles in each column.
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - 2, -1, -1): # Go up from the second-to-last row of the column
            if board[row][col] == BLOCKER[CANDIES_REP_STR_IDX]: continue # Ignore blockers
            new_row = row

            # Calculate where the lowest empty space is below the candy.
            while True:
                if new_row + 1 >= BOARD_SIZE or board[new_row + 1][col] != '':
                    break
                new_row += 1
                shifts = True

            # Shift the candy to the empty position, if needed.
            if new_row != row:
                board[new_row][col] = board[row][col]
                board[row][col] = ''
    
    # Only display the board when there have been position changes.
    if shifts:
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

def within_bounds(row, col):
    '''Checks whether or not a supplied position is within the board's bounds.
    Args:
        row: The row of the position.
        col: The column of the position.
    Returns:
        boolean: Whether or not the position is within bounds.
    '''
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        return False

    return True

def get_user_coord(board, user_input):
    '''Tries to convert user input into a valid coordinate on the board, which must not contain a blocker.
    Also prints a message displaying the validity of the input.
    Args:
        board: The board to check.
        user_input: A string of the user's input.
    Returns:
        (boolean, tuple): A boolean representing the validity of the input's validity, and a tuple representing the coordinate.
    '''
    row = -1
    col = -1
    valid = False

    try:
        row, col = map(int, user_input.split())
        valid = True # If no error occurred when casting the input to integers
        
        # Check if the position is within the bounds.
        if not within_bounds(row, col):
            print("Out of range.")
            valid = False

        # Check if the position refers to a blocker.
        cell = board[row][col]
        if cell == BLOCKER[CANDIES_REP_STR_IDX]:
            print("Unable to perform actions on blocker.")
            valid = False
    except:
        print("Invalid input.")
        pass
    
    return (valid, (row, col))

def display_interface(game_data, difficulty_data, board, objective_candy, objective_count, max_objective):
    '''Displays the board and relevant game info.
    Args:
        game_data: The data related to the game.
        difficulty_data: A dictionary containing information related to the game's current difficulty.
        board: The board the player is using.
        objective_candy: The string representing the objective candy.
        objective_count: How much of the objective candy has been cleared.
        max_objective: The number of objective candies needed to beat the level.
    '''
    # Display level, difficulty, and score on top.
    level_str = f"{GAME_DATA_LEVEL_KEY}: {game_data[GAME_DATA_LEVEL_KEY]}".rjust(BOARD_SIZE * TILE_SIZE + BOARD_SIZE - 1)
    difficulty_str = str(difficulty_data[DIFFICULTY_STR_KEY])
    score_str = f"{GAME_DATA_SCORE_KEY}: {game_data[GAME_DATA_SCORE_KEY]}".rjust(BOARD_SIZE * TILE_SIZE + BOARD_SIZE - 1 - len(difficulty_str))
    print(f"\n   {level_str}")
    print(f"   {difficulty_str}{score_str}")
    display_board(board)

    # Display objective, lives, and moves left at the bottom.
    print(f"{GAME_DATA_OBJECTIVE_CANDY_KEY}: {objective_candy} ({max_objective - objective_count} / {max_objective})")
    print(f"{GAME_DATA_LIVES_KEY}: {game_data[GAME_DATA_LIVES_KEY]}")
    print(f"Moves left: {difficulty_data[DIFFICULTY_MOVES_KEY]}")
    print("Enter row and column (example: 1 2)")
    print("Or Q to quit")

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
    # Get game data, then update the game status and fill the board.
    difficulty_data = game_data[GAME_DATA_DIFFICULTY_KEY]
    objective_candy = game_data[GAME_DATA_OBJECTIVE_CANDY_KEY]
    max_objective = DIFFICULTIES_EFFECTS[difficulty_data[DIFFICULTY_STR_KEY]][DIFFICULTY_OBJECTIVE_COUNT_KEY][objective_candy]
    game_data[GAME_DATA_EXISTS_KEY] = True
    game_data[GAME_DATA_IN_PROGRESS_KEY] = True
    fill_board(game_data, MINIMUM_POSSIBLE_MOVES_START)

    # Allow user to make moves while available.
    while difficulty_data[DIFFICULTY_MOVES_KEY] > 0:
        objective_count = difficulty_data[DIFFICULTY_OBJECTIVE_COUNT_KEY][objective_candy]

        # Check if the objective has been met.
        # If so, update the player's difficulty and level counts.
        if objective_count <= 0:
            difficulty = difficulty_data[DIFFICULTY_STR_KEY]
            level = game_data[GAME_DATA_LEVEL_KEY]
            game_data[GAME_DATA_IN_PROGRESS_KEY] = False
            player_data[PLAYER_DATA_DIFFICULTIES_KEY][difficulty] += 1
            game_data[GAME_DATA_LEVEL_KEY] += 1
            
            time.sleep(DELAY)
            print(f"\nCleared Level {level} ({difficulty})!"
                  f"{' Personal Best!' if update_highest_level(player_data, level) else ''}")
            break

        # Show the user options.
        display_interface(game_data, difficulty_data, game_data[GAME_DATA_BOARD_KEY], objective_candy[CANDIES_REP_NAME_IDX], objective_count, max_objective)
        
        # Get user's input.
        user_input = input(" > ").upper()
        if user_input == 'Q':
            print("Exiting level...")
            return

        valid, (row, col) = get_user_coord(game_data[GAME_DATA_BOARD_KEY], user_input)
        if not valid:
            continue
        
        # After getting a valid position, check if the position refers to a normal or special candy.
        update = False
        candy = get_tile_info(game_data[GAME_DATA_BOARD_KEY][row][col])
        special_candies = (COLOR_BOMB, LINE_BOMB, AREA_BOMB)

        if candy in special_candies:
            activate_special_candy(player_data, game_data, candy, (row, col))
            update = True
        else:
            # Prompt user for an adjacent position to swap the regular candy.
            new_valid, (new_row, new_col) = get_user_coord(game_data[GAME_DATA_BOARD_KEY], input("Enter another row and column (example: 1 2)\n > "))
            if not new_valid:
                continue

            # Verify that the candy is adjacent (must be in same row/col and only one unit away).
            difference = abs(row - new_row) + abs(col - new_col)
            if difference != 1:
                print("Provided candy is not adjacent.")
                continue

            # Perform a swap with the two positions, reversing it if no matches can be done.
            update = attempt_swap(player_data, game_data, (row, col), (new_row, new_col))
            
        # If a move activated a special candy or resulted in matches, lower candies and update the board until no more matches.
        if update:
            while True:
                time.sleep(DELAY)
                drop_candies(game_data[GAME_DATA_BOARD_KEY])

                time.sleep(DELAY)
                updates = update_board(player_data, game_data)

                if not updates:
                    break
                
            # Replace empty tiles after all updates have been made.
            fill_board(game_data, MINIMUM_POSSIBLE_MOVES_DURING)
                
        # Reduce move count after the move.
        difficulty_data[DIFFICULTY_MOVES_KEY] -= 1
    else:
        # Loss logic (output lose message, decrease lives, and check number of lives left).
        game_data[GAME_DATA_LIVES_KEY] -= 1
        print(f"Out of moves! {game_data[GAME_DATA_LIVES_KEY]} lives left.")
        game_data[GAME_DATA_IN_PROGRESS_KEY] = False

        if game_data[GAME_DATA_LIVES_KEY] <= 0:
            print("Out of lives - Game Over!")
            game_data[GAME_DATA_GAME_OVER_KEY] = True
