from src.constants import MAGNIFICATION


def main_to_small_display(x, y):
    """ Convert a position to small_display coordinates. """
    return x / MAGNIFICATION, y / MAGNIFICATION


def main_to_small_display_int(x, y):
    """ Convert position and to integer small_display coordinates. """
    return x // MAGNIFICATION, y // MAGNIFICATION
