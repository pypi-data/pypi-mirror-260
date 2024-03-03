import json
from tree_sitter import Language, Parser
import os
from fumedev import env

from fumedev.env import absolute_path

def load_jsconfig_aliases(directory):
    """
    Search for jsconfig.json starting from the given directory and load path aliases.
    If jsconfig.json is found, parse it to extract path aliases.
    """
    def find_jsconfig(directory):
        """Recursively search for jsconfig.json starting from the given directory."""
        for root, dirs, files in os.walk(directory):
            if 'jsconfig.json' in files:
                return os.path.join(root, 'jsconfig.json')
        return None

    jsconfig_path = find_jsconfig(directory)
    if jsconfig_path is None:
        return {}

    with open(jsconfig_path, 'r') as file:
        jsconfig = json.load(file)

    paths = jsconfig.get('compilerOptions', {}).get('paths', {})
    # Correctly handle the path transformation to retain all characters
    aliases = {}
    for key, value in paths.items():
        # Strip the trailing '/*' from the key and the '/*.js' from the value if present
        alias_key = key.rstrip("/*")
        # Ensure we don't remove the essential parts of the path
        alias_value = value[0].rstrip("*.js")
        alias_value = alias_value if alias_value.endswith('/') else alias_value + '/'
        aliases[alias_key] = alias_value

    return aliases


def resolve_alias(import_path, aliases, base_directory):
    """
    Resolves the given import path using the specified aliases, prepends the base directory,
    tries to infer the extension, and normalizes the path.

    :param import_path: The import path to resolve.
    :param aliases: A dictionary of alias mappings with possible extensions.
    :param base_directory: The base directory of the project to prepend to resolved paths.
    :return: The normalized filesystem path with inferred extension.
    """
    # Default extension
    default_extension = '.js'
    
    for alias, actual_path in aliases.items():
        if import_path.startswith(alias):
            # Check if actual_path hints at a specific extension
            _, ext = os.path.splitext(actual_path)
            if not ext:
                # If no extension in actual_path, use default
                ext = default_extension
            else:
                # If actual_path includes '*', replace it with nothing as we're handling the file directly
                actual_path = actual_path.replace('*', '')

            # Replace the alias in import_path with the actual path, append extension if missing
            resolved_path = import_path.replace(alias, actual_path, 1)
            if not os.path.splitext(resolved_path)[1]:
                resolved_path += ext

            # Prepend the base directory and normalize
            full_path = os.path.join(base_directory, resolved_path)
            normalized_path = os.path.normpath(full_path)
            return normalized_path
    
    # If no alias is found, normalize the path and ensure it has a default extension
    normalized_path = os.path.normpath(os.path.join(base_directory, import_path))
    if not os.path.splitext(normalized_path)[1]:
        normalized_path += default_extension
    return normalized_path

JS_LANGUAGE = Language(env.FILE_FOLDER + '/my-languages.so', 'javascript')

parser = Parser()
parser.set_language(JS_LANGUAGE)

def parse_js_file(file_path,aliases,base_directory):
    """Parse a JavaScript file and return a list of its dependencies."""
    with open(file_path, 'rb') as file:
        js_code = file.read()
    """
    Extracts all import statements from the given JavaScript code.
    
    :param js_code: A string containing JavaScript code.
    :return: A list of import statements found in the code.
    """
    tree = parser.parse(js_code)
    imports = []

    def collect_imports_and_requires(node):
        # Check for ES6 import statements
        if node.type == 'import_statement' or node.type == 'import_declaration':
            imported_path = bfs_search_ast(node, 'string_fragment')
            if imported_path:
                resolved_path = resolve_alias(imported_path.text.decode(), aliases,base_directory)
                imports.append(resolved_path)
        # Check for CommonJS require statements
        elif node.type == 'variable_declarator':
            for child in node.children:
                if child.type == 'call_expression' and js_code[child.start_byte:child.end_byte].decode('utf8').startswith('require('):
                    imported_path = bfs_search_ast(child, 'string_fragment')
                    if imported_path:
                        resolved_path = resolve_alias(imported_path.text.decode(), aliases,base_directory)
                        imports.append(resolved_path)
                    
        # Recursively search in child nodes
        for child in node.children:
            collect_imports_and_requires(child)

    collect_imports_and_requires(tree.root_node)
    return imports

def build_dependency_graph(base_directory,aliases):
    """Build a dependency graph for all JavaScript files in a directory."""
    graph = {}
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                dependencies = parse_js_file(file_path,aliases,base_directory)
                graph[file_path] = dependencies
    return graph

def find_dependents(target_file, dependency_graph):
    """Find all files that are dependent on the target file."""
    dependents = set()
    for file, dependencies in dependency_graph.items():
        if target_file in dependencies:
            dependents.add(file)
    return dependents

def bfs_search_ast(root, target_node_type):
    """
    Perform a breadth-first search on an AST for the first occurrence of a node of a specific type.

    :param root: The root node of the AST.
    :param target_node_type: The type of node to search for.
    :return: The first node of the specified type, or None if no such node is found.
    """
    queue = [root]  # Initialize the queue with the root node

    while queue:
        current_node = queue.pop(0)  # Dequeue the first node in the queue

        # Check if the current node matches the target node type
        if current_node.type == target_node_type:
            return current_node

        # Add child nodes of the current node to the queue
        if hasattr(current_node, 'children'):
            queue.extend(current_node.children)


def get_js_dependents(file_path):

    base_directory = 'codebase'

    aliases = load_jsconfig_aliases(base_directory)

    dependency_graph = build_dependency_graph(base_directory,aliases)
    dependents = find_dependents(file_path, dependency_graph)

    return list(dependents)



