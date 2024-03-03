def file_path_formatter(file_path):
    if not file_path.startswith('./codebase'):
    # Check if it starts with 'codebase' (without './')
        if file_path.startswith('codebase'):
        # Append './' in front of 'codebase'
            file_path = './' + file_path
        else:
        # If it doesn't start with 'codebase', append './codebase/'
            file_path = './codebase/' + file_path

    return file_path