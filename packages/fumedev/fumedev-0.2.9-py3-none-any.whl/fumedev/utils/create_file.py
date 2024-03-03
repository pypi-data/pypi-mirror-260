import os

import os


def create_file(file_path):

    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(file_path, 'a') as file:
        pass

    print(f"File '{file_path}' created or already exists.")