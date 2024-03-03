import jedi

class PythonLanguageServer:

    def __init__(self,file_path):
        self.script = None
        self.file_path = file_path
        self.initialize()

    def initialize(self):
        # Initialize the Jedi Script object with the file content
        with open(self.file_path, 'r') as f:
            file_content = f.read()
        self.script = jedi.Script(file_content)

    def get_completions(self, line, column):
        # Get completions for a given line and column
        completions = self.script.complete(line, column)
        return [completion.name for completion in completions]

    def get_definitions(self, line, column):
        # Get definitions for a given line and column
        definitions = self.script.goto(line, column)
        return [(definition.name, definition.type) for definition in definitions]

    def update_script(self, file_path):
        self.file_path = file_path
        self.initialize()

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