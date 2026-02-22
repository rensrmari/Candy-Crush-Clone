# file_handler.py: Handles logic related to saving data and loading files.

import os
from pathlib import Path
import shelve
from utility import *

def save_session(player_data):
    '''Saves the user's session data in a shelf file with its own directory.
    Args:
        player_data: A dictionary with the player's data.
    Returns:
        boolean: Whether or not the data could be saved.
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
        return False

    # Try opening a shelf file, which has the same name as its parent, and writing to it.
    try:
        with shelve.open(p / save_name) as shelf_file:
            put_values_into(shelf_file, player_data)
        print(f'Successfully saved session data to "{p.name}".')
        return True
    except (KeyError, OSError): # Make sure variables exist and the file is able to be opened
        print(f'Could not save session data to "{p.name}".')
        return False

def load_file(player_data):
    '''Loads a save file into the player's data.
    Args:
        player_data: A dictionary whose values will be updated.
    Returns:
        boolean: Whether or not the load was successful.
    '''
    
    # Prompt user for a path to a directory containing their save data.
    p = Path(input('Please enter an existing directory: '))

    # Check if the directory is valid.
    if not p.is_dir():
        print(f'"{str(p)}" is not a directory.')
        return False

    # Check if the directory contains valid save data.
    items = list(p.glob('*'))
    valid_dirs = get_valid_dirs(p)

    if len(valid_dirs) == 0:
        print(f'No valid save data found in "{str(p)}".')
        return False
    
    # Display valid paths and prompt user to choose a directory.
    print('\nValid save data found in:')
    valid_numbers = []
    for dir in valid_dirs:
        num = len(valid_numbers) + 1
        print(f'\t{num}) {dir.parent.name} - {dir.parent}')
        valid_numbers.append(num)
    
    # Determine which directory is used.
    num_directories = len(valid_numbers)
    if num_directories == 0:
        print(f'"{str(p)}" is not a usable directory.')
        return False

    user_num = input(f'Please enter the number of the directory (1{' - ' + str(num_directories) if num_directories > 1 else ''}): ')
    if not user_num.isdecimal() or int(user_num) <= 0 or int(user_num) > num_directories:
        print('Number does not correspond to a directory.')

    # Load data from the shelf file in the directory.
    try:
        p = valid_dirs[num - 1]
        with shelve.open(p, 'r') as shelf_file:
            put_values_into(player_data, shelf_file)
        print(f'Successfully loaded save data from "{p.parent.name}".')
        return True
    except (KeyError, OSError):
        print(f'Could not load save data from "{p.parent.name}".')
        return False

def get_valid_dirs(path):
    '''Gets the paths of valid save data locations.
    Args:
        path: The path to look in.
    Returns:
        list: The paths that lead to valid save data.
    '''
    res = []

    for folder_name, subfolders, file_names in os.walk(path):
        # Try opening the file as a shelf file and check if all variables needed are present.
        try:
            for file_name in file_names:
                p = Path(folder_name).absolute() / file_name
                with shelve.open(p, 'r') as file: # Do not create new shelf files
                    data = [
                        file.get(DATA_BOARD_KEY, None),
                        file.get(PLAYER_DATA_LEVEL_KEY, None),
                        file.get(DATA_DIFFICULTIES_KEY, None),
                        file.get(DATA_CANDIES_KEY, None)
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
    path = Path(path).absolute()
    num = 0
    items = list(path.glob('*'))
    
    # Increase the number to be appended until the name is unique.
    while path / name in items:
        num += 1
        name = name[0:(-1 if num > 1 else len(name))] + str(num) # Slice name part of path and append a number
    
    return name

def put_values_into(dest, source):
    '''Sets keys of a destination dictionary to the source dictionary's values.
    Args:
        dest: A dictionary whose values will be updated.
        source: A dictionary whose values will be used.
    '''
    
    dest[DATA_BOARD_KEY] = source[DATA_BOARD_KEY]
    dest[PLAYER_DATA_LEVEL_KEY] = source[PLAYER_DATA_LEVEL_KEY]
    dest[DATA_DIFFICULTIES_KEY] = source[DATA_DIFFICULTIES_KEY]
    dest[DATA_CANDIES_KEY] = source[DATA_CANDIES_KEY]