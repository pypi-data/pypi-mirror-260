from textual.screen import ModalScreen
from textual.widgets import Label, Input, Button
from textual.containers import Container
from textual.app import ComposeResult

class SearchPhrase(ModalScreen):

    CSS_PATH = "./searchPhrase.tcss"

    def compose(self) -> ComposeResult:
        yield Container(Label("Search Phrase", id="searchFileTitle"), Label('Search a file description or a phrase in your codebase. It might a description of a file or a piece in your code. Seperate by a comma for multiple.', id="searchFileSubtitle"), Input(placeholder="e.g. Controller that does XYZ, ExampleContainer component", id="searchInput"), Container(Button("Search & Add", variant="success", id="searchBtn"), Button("Cancel", id="cancelBtn"), id="searchButtonsContainer"), id="searchPhraseContainer")