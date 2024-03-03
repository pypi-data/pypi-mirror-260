"""This module holds all the GUI components of the application. Most of the GUI components just have one some additional
feature on top of the base tkinter component"""

def get_float_value(text):
    """
        Returns:
            float: the value of text as a float"""

    return float(text)


def get_int_value(text):
    """
        Returns:
            int: the value of text as an integer"""

    return int(text)


def get_csv_text(text: str, value_to_object=lambda x: x):
    """
        Returns:
            list[str]: each value of the text. The value in question is value_to_object(csv_value)"""

    values = text.split(", ")
    return [value_to_object(x) for x in values]
