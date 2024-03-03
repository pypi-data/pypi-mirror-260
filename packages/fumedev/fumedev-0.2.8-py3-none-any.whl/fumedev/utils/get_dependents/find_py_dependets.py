import ast
import os

def module_path_to_name(module_path, project_root):
    """
    Converts a module's file path to its dotted module name based on the project root.
    """
    relative_path = os.path.relpath(module_path, start=project_root)
    without_extension = os.path.splitext(relative_path)[0]
    module_name = without_extension.replace(os.path.sep, '.')
    return module_name

def find_imports_in_file(filepath):
    """
    Parses a Python file and returns a set of imported module names and relative imports.
    """
    with open(filepath, 'r') as file:
        tree = ast.parse(file.read(), filename=filepath)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
            for alias in node.names:
                # Include the import name for from-import statements, handling relative imports
                if node.level > 0:  # Relative import
                    prefix = '.' * node.level
                    imports.add(f"{prefix}{node.module}" if node.module else prefix)
                else:
                    imports.add(node.module)
    
    return imports

def find_dependent_files(target_filepath, project_root):
    """
    Finds all files in the project that depend on the given file by analyzing imports.
    
    :param target_filepath: Path to the file to check dependencies for.
    :param project_root: Root directory of the project to search through.
    :return: A list of files that import the given file.
    """
    target_module_name = module_path_to_name(target_filepath, project_root)
    dependent_files = []

    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                imports = find_imports_in_file(filepath)
                file_module_name = module_path_to_name(filepath, project_root)
                
    
                match_found = any(
                    target_module_name == imp or target_module_name.startswith(imp + '.')
                    for imp in imports
                )
                if match_found:
                    dependent_files.append(filepath)
    
    return dependent_files


def get_py_dependents(file_path):

    project_root = './codebase'
    res = find_dependent_files(file_path, project_root)
    return list(res)
