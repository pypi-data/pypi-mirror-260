
from .syntax_checker import SyntaxChecker
import jedi

class PythonSyntaxChecker(SyntaxChecker):
    """
    A Python-specific syntax checker that inherits from the generic SyntaxChecker.
    Utilizes the jedi library to check for syntax errors in Python files.
    """
    def __init__(self, file_path):
        """Initialize the PythonSyntaxChecker with the specified file path."""
        super().__init__(file_path)

    def has_syntax_error(self):
        """
        Checks if the Python file at the specified path has any syntax errors
        using the jedi library.

        Returns:
            bool or list: False if no syntax errors are found, or a list of errors otherwise.
        """
        try:
            script = jedi.Script(path=self.file_path)
            all_errors = script.get_syntax_errors()
            if all_errors:
                # Formatting the errors to be more readable and informative
                return [f"Line {error.line}: {error.get_message()}" for error in all_errors]
            else:
                return False
        except Exception as e:
            # In case of an unexpected error, return the error message.
            # It's important to communicate the issue rather than silently failing.
            return [str(e)]
