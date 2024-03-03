from textual.screen import Screen
from textual.widgets import Label, Input, Button
from textual.containers import Container, ScrollableContainer
from textual.app import ComposeResult
from fumedev.auth.auth import try_login
from fumedev.gui.screens.Main.main import Main

class Login(Screen):

    CSS_PATH = "./login.tcss"

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == 'loginBtn':
            email = self.query_one('#emailInput').value
            password = self.query_one('#passwordInput').value

            success = try_login(email=email, password=password)

            if success:
                self.app.push_screen(Main())
            else:
                self.notify("Wrong username and password", severity='error')

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Label("Login", id="loginTitle"), Label('FumeLX vALPHA', id="loginSubtitle"), Input(placeholder="Your email address", id="emailInput"), Input(placeholder="Your password", id="passwordInput", password=True), Container(Button("Login", variant="success", id="loginBtn"), Button("Register", id="registerBtn"), id="loginButtonsContainer"), id="loginContainer")