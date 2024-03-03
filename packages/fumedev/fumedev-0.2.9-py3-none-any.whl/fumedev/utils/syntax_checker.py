

from abc import ABC, abstractmethod


class SyntaxChecker(ABC):
    def __init__(self, file_path):
        """
        
        Parameters:
            file_path (str): The path to the file to be checked for syntax errors.
        """
        self.file_path = file_path

    @abstractmethod
    def has_syntax_error(self):
        """
        Checks if the file at the specified path has any syntax errors.

        
        Returns:
            bool or list: False if no syntax errors are found, or a list of errors otherwise.
        """
        pass
