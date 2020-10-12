import pygame

from src.scenes.scene import Scene
from src import button


class OptionsMenu(Scene):
    def __init__(self, game):
        super().__init__(game)

        # TODO: Create text fields and input fields which allow users to
        #  modify keybindings.

    def process_event(self, event, event_manager):
        block = super().process_event(event, event_manager)
        if block:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_escape:
                self.close()
                return True

    def draw(self):
        self.target_surface.fill((0, 0, 0))
        for b in self.buttons:
            self.target_surface.blit(b.image, b.rect)
