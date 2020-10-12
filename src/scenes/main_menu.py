import pygame

from src import constants
from src.scenes.scene import Scene
from src.button import Button


class MainMenu(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.buttons = (
            Button(
                "New Game",
                (100, 50),
                (constants.SMALL_DISPLAY_WIDTH // 2, 50),
                self.new_game
            ),
            Button(
                "Options",
                (100, 50),
                (constants.SMALL_DISPLAY_WIDTH // 2, constants.SMALL_DISPLAY_HEIGHT // 2),
                self.goto_options
            ),
            Button(
                "Quit",
                (100, 50),
                (constants.SMALL_DISPLAY_WIDTH // 2, 200),
                self.game.quit
            )
        )

    def process_event(self, event, event_manager):
        block = super().process_event(event, event_manager)
        if block:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_escape:
                self.close()
                return True

    def draw(self):
        self.target_surface.fill((100, 100, 100))  # DEBUG: red to check if rounded buttons work
        for b in self.buttons:
            self.target_surface.blit(b.image, b.rect)

    def new_game(self):
        self.game.persistent_scene_data["world name"] = "test"
        self.close("main game")

    def goto_options(self):
        self.close("options menu", remove_self=False)
