from tkinter import Button as TkButton
from tkinter_qu.gui_components.component import Component
from tkinter_qu.base.colors import *


class Button(TkButton, Component):
    """A button for any application (adds some helper methods from Component to an existing TkButton)"""

    selected_color = None
    is_selected = False
    background_color = None
    current_color = None

    def __init__(self, window_type, text, font, background_color=pleasing_green, text_color=black, hover_color=dark_green):
        """Initializes a button"""

        super().__init__(window_type, text=text, font=font, bg=background_color, fg=text_color)

        self.selected_color = background_color
        self.background_color = background_color
        self.set_current_color(background_color)

        self.set_hover_color(hover_color)

    def set_command(self, command):
        """Sets the command that is called when the button is clicked (uses the one parameter tkinter config method)"""

        self.configure(command=command)

    def set_background_color(self, background_color):
        """Sets the color of the button"""

        self.configure(bg=background_color)
        self.background_color = background_color

    def set_current_color(self, current_color):
        """Sets the color of the button when it is not selected"""

        self.current_color = current_color
        self.configure(bg=current_color)

    def set_text_color(self, text_color):
        """Sets the color of the text of the button"""

        self.configure(fg=text_color)

    def unselect(self):
        """Makes the button unselected"""

        self.is_selected = False
        self.set_current_color(self.background_color)

    def get_is_selected(self):
        """Returns whether the button is selected"""

        return self.is_selected

    def select(self):
        """Makes the button selected"""

        self.is_selected = True
        self.set_current_color(self.selected_color)

    def set_selected_color(self, selected_color):
        """Sets the color of the button when it is selected"""

        self.selected_color = selected_color

    def set_hover_color(self, hover_color):
        """Sets the color of the button when it is hovered over"""

        self.bind("<Enter>", lambda e: self.configure(bg=hover_color))
        self.bind("<Leave>", lambda e: self.configure(bg=self.current_color))
