import os

from fumedev import env

def get_unique_extensions(directory):
    exclude_folders = env.EXCLUDE_FOLDERS
    exclude_files = env.EXCLUDE_FILES.split(',')
    allowed_extensions = env.NONTRVIVIAL_FILES
    unique_extensions = set()
    
    for root, dirs, files in os.walk(directory):
        # Modify the list of directories to exclude specified folders by name
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        for file in files:
            # Check if the file name (not the full path) is not in the exclude list
            if file not in exclude_files:
                extension = os.path.splitext(file)[1].lstrip('.').lower() # Remove dot and convert to lowercase
                unique_extensions.add(extension)
    # Filter the collected extensions to include only those in allowed_extensions
    filtered_extensions = {ext for ext in unique_extensions if ext in allowed_extensions}
    return filtered_extensions