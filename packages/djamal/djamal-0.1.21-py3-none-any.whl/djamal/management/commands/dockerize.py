from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Static, Button

QUESTION = "Do you want to learn about Textual CSS?"


class Dockerize(App):
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]
    #CSS_PATH = "question.css"

    def compose(self) -> ComposeResult:
        """Place all widgets."""
        yield Header()
        yield Footer()
        yield Container(
            Static(QUESTION, classes="question"),
            Horizontal(
                Button("Yes", variant="success"),
                Button("No", variant="error"),
                classes="buttons",
            ),
            id="dialog",
        )

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Exit app with id of the button pressed."""
        self.exit(event.button.label)
