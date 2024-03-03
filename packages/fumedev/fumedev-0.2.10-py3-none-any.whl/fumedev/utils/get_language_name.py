

def get_language_name(file_extension):

    extension_dict = {
        "py": "python",
        "js": "javascript",
        'jsx': 'javascript',
        "ts": "typescript",
        "tsx": "typescript",
        "c": "c",
        "cpp": "cpp",
        "cs": "csharp",
        "css": "css",
        "go": "go",
        "html": "html",
        "java": "java",
        "php": "php",
        "rb": "ruby",
        "rs": "rust",
        "swift": "swift",
        "pug": "pug",
        'tcss': 'tcss'
    }
    return extension_dict.get(file_extension, "text")