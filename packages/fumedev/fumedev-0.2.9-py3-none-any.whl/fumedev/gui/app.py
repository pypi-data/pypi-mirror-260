import time

import sentry_sdk
from fumedev.utils.search_snippet import search_snippet
from textual.app import App, ComposeResult
from textual.widgets import Label, Button
from fumedev.gui.screens.FileTreeSelector.fileTreeSelector import FileTreeSelector
from fumedev.gui.screens.Main.main import Main
from fumedev.gui.screens.SearchPhrase.searchPhrase import SearchPhrase
from fumedev.gui.screens.Login.login import Login
from textual.containers import Container
from fumedev.auth.auth import try_auto_login
from fumedev.models.ChatLog import ChatLog
from fumedev.utils.generate_id import generate_id
import fumedev.env as env

class FumeApp(App):
    def _handle_exception(self, error: Exception):
        sentry_sdk.capture_exception(error)
        super()._handle_exception(error)

    SCREENS = {"fileTreeSelector": FileTreeSelector(), "searchPhrase": SearchPhrase(), "login": Login()}

    def __init__(self):
        super().__init__()
        self.main_screen = Main()
        self.install_screen(screen=self.main_screen, name='main')
        self.contextFiles = []
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id

        if button_id == "navigateFileSelector":

            def updateContext(files: list):

                files = [env.absolute_path('codebase/' + file) for file in files]

                self.contextFiles = [snippet.get('file_path') for snippet in env.SNIPPETS]
                previous_files = set(self.contextFiles.copy())

                self.contextFiles += files
                self.contextFiles = list(set(self.contextFiles))

                context_files = self.query_one("ContextFiles")                
                context_files.update_file_list(self.contextFiles)

                # Calculate the difference between the current context files and the newly added ones
                new_files = list(set(files).difference(previous_files))
                if not new_files:  # If there are no new files, do nothing further
                    return

                # For each new file, perform a snippet search and append the results to globals()["SNIPPETS"]
                for file in new_files:
                    query = env.TASK  # Retrieve the TASK global variable as the query
                    snippets, _ = search_snippet(query=query, file_path=file)
                    env.SNIPPETS.extend(snippets)

            self.push_screen("fileTreeSelector", updateContext)

        elif button_id == "navigateSearchPhrase":
            self.push_screen("searchPhrase")

        elif button_id == "cancelBtn":
            self.pop_screen()

    def ask_multi_choice(self, options):
        self.main_screen.ask_multi_choice(options=options)

    def add_chat_log(self, log: ChatLog):
        self.main_screen.add_chat_log(log=log)

    def on_mount(self):
        login_success = try_auto_login()
        
        if login_success:
            self.push_screen('main')
        else:
            self.push_screen('login')
