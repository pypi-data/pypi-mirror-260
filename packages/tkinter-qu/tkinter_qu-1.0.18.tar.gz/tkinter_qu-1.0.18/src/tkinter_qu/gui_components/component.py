import tkinter

from tkinter_qu.gui_components.dimensions import Dimensions


class Component(tkinter.Widget, Dimensions):
    """A component of any application (has some additional features on top of tkinter.Widget)"""

    saved_place_info = None
    is_currently_hidden = False

    def hide(self):
        """Hides the component, so it is no longer rendered"""

        if not self.is_currently_hidden:
            self.saved_place_info = self.place_info()
            self.place_forget()
            self.is_currently_hidden = True

    def show(self):
        """Shows the component, so it is rendered again"""

        if self.saved_place_info is not None:
            super().place(**self.saved_place_info)
            self.is_currently_hidden = False

    def number_set_dimensions(self, left_edge, top_edge, length, height):
        """Sets the dimensions of the component with the numbers provided"""

        super().number_set_dimensions(left_edge, top_edge, length, height)
        super().place(x=int(left_edge), y=int(top_edge), width=int(length), height=int(height))

    def place(self, **kwargs):
        """Calls the tkinter.Widget place function"""

        self.number_set_dimensions(kwargs.get("x"), kwargs.get("y"), kwargs.get("width"), kwargs.get("height"))

        # Do not want to call the place function with the x, y, width, and height values
        removed_keys = ["x", "y", "width", "height"]
        new_kwargs = {}

        for key in kwargs.keys():
            if not removed_keys.__contains__(key):
                new_kwargs[key] = kwargs.get(key)



