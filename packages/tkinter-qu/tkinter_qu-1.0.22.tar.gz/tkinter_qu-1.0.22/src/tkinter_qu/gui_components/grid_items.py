from tkinter_qu.base.important_variables import SCREEN_LENGTH, SCREEN_HEIGHT
from tkinter_qu.gui_components.dimensions import Dimensions
from tkinter_qu.gui_components.grid import Grid
from tkinter_qu.gui_components.component import Component


class GridType:
    """Holds all the types of grids that can be used"""

    # The order of the items follows this structure: [grid_rows, grid_columns]
    VERTICAL = [None, 1]
    HORIZONTAL = [1, None]


class GridItems(Component):
    """Holds all the items that should be in a grid"""

    items = []

    def __init__(self, items: list[Component], grid_type):
        """Initializes the object"""

        self.items = items
        self.grid = Grid(Dimensions.get_zero(), *grid_type)

    def number_set_dimensions(self, left_edge, top_edge, length, height, update_grid=True):
        """Places all the items at that location in a grid format"""

        Dimensions.number_set_dimensions(self, left_edge, top_edge, length, height)
        self.grid.number_set_dimensions(left_edge, top_edge, length, height)

        if update_grid:
            self.grid.turn_into_grid(self.items, None, None)

    def percentage_set_dimensions(self, percent_right, percent_down, percent_length, percent_height,
                                  horizontal_number=SCREEN_LENGTH, vertical_number=SCREEN_HEIGHT, update_grid=True):
        """ Sets the dimensions based on the values passed into this function

            Args:
                percent_right (int): the percent it is to right (percentage of horizontal_number)
                percent_down (int): the percent it is down (percentage of horizontal_number)
                percent_length (int): the length (percentage of vertical_number)
                percent_height (int): the height (percentage of vertical_number)
                horizontal_number (int): what percent_right and percent_length are percentages of
                vertical_number (int): what percent_down and percent_height are percentages of
                update_grid (bool): whether this class's items are turned into a grid

            Returns:
                None
        """

        left_edge = horizontal_number * percent_right / 100
        length = horizontal_number * percent_length / 100
        top_edge = vertical_number * percent_down / 100
        height = vertical_number * percent_height / 100

        self.number_set_dimensions(left_edge, top_edge, length, height, update_grid)

    def set_items(self, items):
        """Sets the items of the grid"""

        self.items = items
        self.number_set_dimensions(*self.get_values())
