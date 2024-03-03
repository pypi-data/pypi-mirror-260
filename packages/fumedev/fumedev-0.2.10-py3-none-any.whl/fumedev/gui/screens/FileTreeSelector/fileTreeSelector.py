from textual.app import App, ComposeResult
from textual.widgets import Static, Label, Button, DirectoryTree, Footer
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen

import fumedev.env as env

class FileCardRemoveButton(Static):
    """
    A static widget for a button that allows removing a selected file card.

    Attributes:
        removeAction (Callable): The action to perform when the button is clicked.
    """
    def __init__(self, removeAction):
        super().__init__()
        self.removeAction = removeAction

    def on_click(self):
        self.removeAction()

    def compose(self) -> ComposeResult:
        yield Container(Label('X'), id="fileCardRemove")

class FileCard(Static):
    """
    A static widget representing a selected file, displaying its name and providing a way to remove it.

    Attributes:
        file_path (str): The file path of the file represented by this card.
    """
    def __init__(self, file_path):
        super().__init__() 
        self.file_path = file_path

    def remove_file_card(self):
        """Remove the file card from the UI."""
        self.remove()

    def compose(self) -> ComposeResult:
        yield Container(Label(self.file_path, id="fileCardLabel"), FileCardRemoveButton(removeAction=self.remove_file_card), id="fileCard")

class SelectedFiles(Static):
    """
    A static widget displaying a list of selected files.
    """
    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Label("Selected Files", id="title"), id="selectedFilesScroll")

class FileTreeSelector(Screen[list]):
    """
    A screen for selecting files from a directory tree, allowing multiple files to be selected.

    Attributes:
        selected_files (List[str]): A list of file paths that have been selected.
    """

    CSS_PATH = "./fileTreeSelector.tcss"

    BINDINGS = [
        ("d", "done", "Done"),
        ("x", "exit", "Exit"),
    ]

    def action_done(self):
        """Dismiss the FileTreeSelector and return the list of selected files."""
        self.dismiss(self.selected_files)

    def action_exit(self):
        """Dismiss the FileTreeSelector without returning any files."""
    
    def action_exit(self):
        self.dismiss([])

    """
    Handle the file selection event from the directory tree.

    Args:
        node (Node): The directory tree node that was selected, representing a file.
    """
    def on_directory_tree_file_selected(self, node):
        file_path = str(node.path)
        file_name = node.path.name
        if not (file_path in self.selected_files):
            self.selected_files.append(file_path)
            new_file_card = FileCard(file_name)
            self.query_one("#selectedFilesScroll").mount(new_file_card)
            new_file_card.scroll_visible()

    def compose(self) -> ComposeResult:
        """Compose the UI for the FileTreeSelector screen."""
        self.selected_files = []
        yield Container(DirectoryTree(env.PROJECT_PATH), SelectedFiles(id="selectedFiles"), id="container")
        yield Footer()
