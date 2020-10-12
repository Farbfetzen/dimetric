import pygame

from src import resources


class EventManager:
    # TODO: This class was once a bit more useful. Either make it more useful
    #  or handle the controls differently.
    def __init__(self):
        controls = resources.options["controls"]
        self.k_escape = pygame.K_ESCAPE
        self.k_scroll_left = pygame.key.key_code(controls["scroll left"])
        self.k_scroll_right = pygame.key.key_code(controls["scroll right"])
        self.k_scroll_up = pygame.key.key_code(controls["scroll up"])
        self.k_scroll_down = pygame.key.key_code(controls["scroll down"])
        self.mouse_map_scroll_button_index = controls["mouse scroll button index"]
        self.k_dev = pygame.key.key_code(controls["dev"])
