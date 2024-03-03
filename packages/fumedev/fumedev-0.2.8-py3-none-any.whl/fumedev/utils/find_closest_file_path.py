import os
from fumedev import env
from difflib import SequenceMatcher

def list_all_file_paths(directory=env.absolute_path('codebase'), extensions=env.NONTRVIVIAL_FILES, exclude_dirs=env.EXCLUDE_FOLDERS):
    """
    Generates a list of all file paths in the given directory, including paths in subdirectories, filtered by extensions and excluding specified directories.
    
    :param directory: The directory to list file paths from.
    :param extensions: A list of file extensions to include. If None, all files are included.
    :param exclude_dirs: A list of directories to exclude. If None, no directories are excluded.
    :return: A list of file paths.
    """
    file_paths = []  # List to store file paths
    for root, directories, files in os.walk(directory, topdown=True):
        directories[:] = [d for d in directories if d not in exclude_dirs] if exclude_dirs else directories
        for filename in files:
            if extensions is None or any(filename.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, directory)
                file_paths.append(relative_path)
    return file_paths

def levenshtein_distance(s1, s2):
    # If one of the strings is empty, return the length of the other (all insertions/deletions)
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    
    # Initialize a matrix to hold the distances
    distance_matrix = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
    
    # Initialize the first row and column of the matrix
    for i in range(len(s1) + 1):
        distance_matrix[i][0] = i
    for j in range(len(s2) + 1):
        distance_matrix[0][j] = j
        
    # Populate the matrix
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            # Check if the characters are the same
            cost = 0 if s1[i-1] == s2[j-1] else 1
            
            # Calculate distances for the three operations
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1] + cost
            
            # Determine the minimum distance
            distance_matrix[i][j] = min(deletion, insertion, substitution)
    
    # The distance between the two strings is in the bottom-right corner of the matrix
    return distance_matrix[-1][-1]


def calculate_layer_similarity(filepath1, filepath2):
    # Split the filepaths into layers
    layers1 = filepath1.split('/')
    layers2 = filepath2.split('/')
    
    # Initialize a list to store the minimum distances for each layer in filepath1
    min_distances = []
    
    # For each layer in filepath1, find the layer in filepath2 it is most similar to
    for layer1 in layers1:
        layer_distances = [levenshtein_distance(layer1, layer2) for layer2 in layers2]
        min_distance = min(layer_distances)  # Find the minimum distance for this layer
        min_distances.append(min_distance)
    
    # Calculate the total difference index as the sum of minimum distances
    difference_index = sum(min_distances)
    
    return difference_index / len(layers2)

def find_closest_file_path(target_filepath, directory=env.absolute_path('codebase'), extensions=env.NONTRVIVIAL_FILES, exclude_dirs=env.EXCLUDE_FOLDERS):
    """
    Finds the closest file path in the directory to the given target filepath using Levenshtein distance.
    
    :param target_filepath: The target filepath to find the closest match for.
    :param directory: The directory to search in.
    :param extensions: A list of file extensions to include. If None, all files are included.
    :param exclude_dirs: A list of directories to exclude. If None, no directories are excluded.
    :return: The closest file path as a string.
    """
    #check if target_filepath exists 
    if os.path.exists(target_filepath):
        return target_filepath
    target_filepath = target_filepath.replace(directory+'/','')
    all_file_paths = list_all_file_paths(directory, extensions, exclude_dirs)
    closest_path = None
    infinity = float('inf')
    min_distance = infinity
    for path in all_file_paths:
        distance = calculate_layer_similarity(target_filepath, path)
        if distance < min_distance:
            min_distance = distance
            closest_path = path
    return f'{directory}/{closest_path}'
