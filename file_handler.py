# file_handler.py: Handles logic related to saving data and loading files.

import os
from pathlib import Path
import shelve
import shutil
from utility import *

def save_session(player_data, game_data):
    '''Saves the user's session data in a shelf file with its own directory.
    Args:
        player_data: A dictionary with the player's data.
        game_data: A dictionary with the game data.
    '''

    # Prompt user for a path to an existing directory.
    p = Path(input('Please enter an existing directory: ')).absolute()

    # An invalid directory will result in the current working directory being used.
    if not p.is_dir():
        print(f'{str(p)} is not a directory. Using "{Path.cwd()}".')
        p = Path.cwd()

    # Prompt user for a name for the directory where the save data will be stored.
    save_name = input('Please enter a name for the save data: ')
    p /= save_name

    # If the name is already taken, create a unique name based off the original.
    # Otherwise, use a default name.
    if p.exists():
        p = p.parent / get_unique_name(p.parent, save_name)
        print(f'"{save_name}" already exists. Using "{p.name}".')

    # Try creating the directory.
    try:
        os.makedirs(p)
        if p.is_dir():
            print(f'Successfully created "{str(p)}".')
    except FileExistsError: 
        print(f'Error creating "{str(p)}".')
        return
    p /= p.name

    # Try opening a shelf file, which has the same name as its parent, and writing to it.
    try:
        with shelve.open(p) as shelf_file:
            # Player-related data.
            shelf_file[PLAYER_DATA_LEVEL_KEY] = player_data[PLAYER_DATA_LEVEL_KEY]
            shelf_file[PLAYER_DATA_DIFFICULTIES_KEY] = player_data[PLAYER_DATA_DIFFICULTIES_KEY]
            shelf_file[PLAYER_DATA_CANDIES_KEY] = player_data[PLAYER_DATA_CANDIES_KEY]

            # Game data.
            shelf_file[GAME_DATA_BOARD_KEY] = game_data[GAME_DATA_BOARD_KEY]
            shelf_file[GAME_DATA_LEVEL_KEY] = game_data[GAME_DATA_LEVEL_KEY]
            shelf_file[GAME_DATA_DIFFICULTY_KEY] = game_data[GAME_DATA_DIFFICULTY_KEY]
            shelf_file[GAME_DATA_IN_PROGRESS_KEY] = game_data[GAME_DATA_IN_PROGRESS_KEY]
        print(f'Successfully saved session data to "{p.parent.name}".')
    except (KeyError, OSError): # Make sure variables exist and the file is able to be opened
        print(f'Could not save session data to "{p.parent.name}".')

def load_file(player_data, game_data):
    '''Loads a save file into the player's data and game data.
    Args:
        player_data: The player's previous player data.
        game_data: The player's previous game data.
    '''
    
    # Prompt user for a path to a directory containing their save data.
    p, valid_paths = get_paths_to_saves()
    if p == None:
        return
    
    # Get the user's choice of a directory.
    dir_idx = get_dir_idx(p, valid_paths)
    if dir_idx == -1:
        return
    p = valid_paths[dir_idx]

    # Load data from the shelf file in the directory.
    try:
        with shelve.open(p, 'r') as shelf_file:
            # Player-related data.
            player_data[PLAYER_DATA_LEVEL_KEY] = shelf_file[PLAYER_DATA_LEVEL_KEY]
            player_data[PLAYER_DATA_DIFFICULTIES_KEY] = shelf_file[PLAYER_DATA_DIFFICULTIES_KEY]
            player_data[PLAYER_DATA_CANDIES_KEY] = shelf_file[PLAYER_DATA_CANDIES_KEY]

            # Game data.
            game_data[GAME_DATA_BOARD_KEY] = shelf_file[GAME_DATA_BOARD_KEY]
            game_data[GAME_DATA_LEVEL_KEY] = shelf_file[GAME_DATA_LEVEL_KEY]
            game_data[GAME_DATA_DIFFICULTY_KEY] = shelf_file[GAME_DATA_DIFFICULTY_KEY]
            game_data[GAME_DATA_SCORE_KEY] = shelf_file[GAME_DATA_SCORE_KEY]
            game_data[GAME_DATA_IN_PROGRESS_KEY] = shelf_file[GAME_DATA_IN_PROGRESS_KEY]
        print(f'Successfully loaded save data from "{p.parent.name}".')
    except (KeyError, OSError):
        print(f'Could not load save data from "{p.parent.name}".')

def delete_file():
    '''Deletes a save file.'''
    # Prompt user for a path to a directory containing their save data.
    p, valid_paths = get_paths_to_saves()
    if p == None:
        return
    
    # Get the user's choice of a directory.
    dir_idx = get_dir_idx(p, valid_paths)
    if dir_idx == -1:
        return
    p = valid_paths[dir_idx]
    
    # Get final confirmation.
    user_confirm = prompt_user_input(('Y', 'N'), f'Are you sure you want to delete "{p.parent.name}"?\n\t(Y) Yes\n\t(N) No')
    
    # Try deleting data.
    if user_confirm == "Y":
        try:
            shutil.rmtree(p.parent)
            print(f'Successfully deleted save data from "{p.parent.name}".')
        except OSError:
            print(f'An error occurred when deleting "{p.parent.name}".')
    else:
        print(f'"{p.parent.name}" has not been deleted.')

def get_dir_idx(path, valid_paths):
    '''Gets a user's choice of a directory among a list of directories.
    Args:
        path: The path to check.
        valid_paths: Valid paths to save files from the initial path.
    Returns:
        int: A number between 0 and len(paths) - 1 if a valid number was chosen, -1 otherwise.
    '''
    
    # Display valid paths and prompt user to choose a directory.
    print('\nValid save data found in:')
    valid_numbers = []
    for valid_path in valid_paths:
        num = len(valid_numbers) + 1
        print(f'\t{num}) {valid_path.parent.name} - {valid_path.parent}')
        valid_numbers.append(num)
    
    # Determine which directory is used.
    num_directories = len(valid_numbers)
    if num_directories == 0:
        print(f'"{str(path)}" is not a usable directory.')
        return -1

    user_num = input(f'Please enter the number of the directory (1{' - ' + str(num_directories) if num_directories > 1 else ''}): ')
    if not user_num.isdecimal() or int(user_num) <= 0 or int(user_num) > num_directories:
        print('Number does not correspond to a directory.')
        return -1

    return int(user_num) - 1

def get_paths_to_saves():
    '''Prompts user for a path to valid save data.
    Returns:
        (path, list of paths): A path and a list of valid paths to save files if the directory was valid, otherwise None.
    '''
    
    # Prompt user for a path to a directory containing their save data.
    p = Path(input('Please enter an existing directory: ')).absolute()

    # Check if the directory is valid.
    if not p.is_dir():
        print(f'"{str(p)}" is not a directory.')
        return (None, None)

    # Check if the directory contains valid save data.
    items = list(p.glob('*'))
    valid_dirs = get_valid_dirs(p)

    if len(valid_dirs) == 0:
        print(f'No valid save data found in "{str(p)}".')
        return (None, None)
    
    return (p, valid_dirs)

def get_valid_dirs(path):
    '''Gets the paths of valid save data locations.
    Args:
        path: The path to look in.
    Returns:
        list: The paths to valid save data.
    '''
    res = []

    for folder_name, subfolders, file_names in os.walk(path):
        # Try opening the file as a shelf file and check if all variables needed are present.
        try:
            for file_name in file_names:
                p = Path(folder_name).absolute() / file_name
                with shelve.open(p, 'r') as file: # Do not create new shelf files
                    data = [
                        file.get(PLAYER_DATA_LEVEL_KEY, None),
                        file.get(PLAYER_DATA_DIFFICULTIES_KEY, None),
                        file.get(PLAYER_DATA_CANDIES_KEY, None),
                        file.get(GAME_DATA_BOARD_KEY, None),
                        file.get(GAME_DATA_LEVEL_KEY, None),
                        file.get(GAME_DATA_DIFFICULTY_KEY, None),
                        file.get(GAME_DATA_SCORE_KEY, None),
                        file.get(GAME_DATA_IN_PROGRESS_KEY, None)
                    ]

                if None not in data:
                    res.append(p)
        except:
            pass

    return res

def get_unique_name(path, name):
    '''Checks for duplicate directory or directory names and returns a unique name.
    Args:
        path: A path to look in.
        name: A string to check.
    Return:
        string: A unique name.
    '''
    path = path.absolute()
    num = 0
    items = list(path.glob('*'))
    
    # Increase the number to be appended until the name is unique.
    while path / name in items:
        num += 1
        name = name[0:(-1 if num > 1 else len(name))] + str(num) # Slice name part of path and append a number
    
    return name