import os
from fumedev import env
from collections import deque

def get_dir_structure(startpath, extensions=env.NONTRVIVIAL_FILES, exclude_dirs=env.EXCLUDE_FOLDERS):
    if extensions is None:
        extensions = []
    if exclude_dirs is None:
        exclude_dirs = []
    structure_str = ""
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]  # Exclude specified directories
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        structure_str += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not extensions or any(f.endswith(ext) for ext in extensions):
                structure_str += f"{subindent}{f}\n"
    return structure_str

def get_dir_structure_bfs(startpath=env.absolute_path('codebase'), n=500, extensions=env.NONTRVIVIAL_FILES, exclude_dirs=env.EXCLUDE_FOLDERS):
    if extensions is None:
        extensions = []
    if exclude_dirs is None:
        exclude_dirs = []
    structure_str = ""
    node_count = 0

    # Queue for BFS. Each element is a tuple (path, depth)
    queue = deque([(startpath, 0)])

    # Track the last depth processed to ensure we don't cut a level in half
    last_depth = 0

    while queue and node_count < n:
        current_path, depth = queue.popleft()
        # Check if we moved to a new depth level and have reached the limit
        if depth > last_depth and node_count >= n:
            break
        level = current_path.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        structure_str += f"{indent}{os.path.basename(current_path)}/\n"
        node_count += 1  # Increment for the current directory

        try:
            with os.scandir(current_path) as it:
                for entry in it:
                    if entry.is_dir() and entry.name not in exclude_dirs:
                        queue.append((entry.path, depth + 1))
                    elif entry.is_file() and (not extensions or any(entry.name.endswith(ext) for ext in extensions)):
                        if node_count < n:
                            subindent = ' ' * 4 * (level + 1)
                            structure_str += f"{subindent}{entry.name}\n"
                            node_count += 1
                        else:
                            # If adding this file would exceed the limit, check if we're on a new depth level
                            if depth > last_depth:
                                break  # Stop processing this level if we've moved to a new depth and reached the limit
        except PermissionError:
            pass  # Ignore directories that cannot be accessed

        last_depth = depth  # Update the last processed depth

    return structure_str