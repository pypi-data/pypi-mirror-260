from fumedev.utils.get_dependents.find_js_dependents import get_js_dependents
from fumedev.utils.get_dependents.find_py_dependets import get_py_dependents
from fumedev.utils.get_language_name import get_language_name


def get_dependents(file_path):
    file_extension = file_path.split('.')[-1]

    file_language = get_language_name(file_extension)

    if file_language == 'javascript':
        return get_js_dependents(file_path)
    elif file_language == 'python':
        return get_py_dependents(file_path)
    else:
        return [] 
