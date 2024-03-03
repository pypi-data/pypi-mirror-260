import os
from fumedev import env

from fumedev.utils.get_language_name import get_language_name

class FolderGraph:
    def __init__(self, root_folder):
        self.graph = {}
        self.root = root_folder
        self.excluded_dirs = set(env.EXCLUDE_FOLDERS)
        self.exluded_files = set(env.EXCLUDE_FILES.split(','))
        self._build_graph(root_folder)

    def _build_graph(self, current_folder):
        # Avoid infinite loops with symbolic links and exclude directories
        if os.path.islink(current_folder) or os.path.basename(current_folder) in self.excluded_dirs:
            return

        try:
            contents = os.listdir(current_folder)
        except PermissionError:
            contents = []

        self.graph[current_folder] = []

        for item in contents:
            path = os.path.join(current_folder, item)
            # Skip excluded directories
            if os.path.basename(path) in self.excluded_dirs:
                continue

            self.graph[current_folder].append(path)
            if os.path.isdir(path):
                self._build_graph(path)

    def get_leaf_files(self):
        leaf_files = []
        for folder, contents in self.graph.items():
            for item in contents:
                extension = item.split('.')[-1]
                extension = get_language_name(extension)
                if os.path.isfile(item) and extension != 'text' and item not in self.exluded_files:
                    leaf_files.append(item)
        return leaf_files
