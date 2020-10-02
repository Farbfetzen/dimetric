# Copyright (C) 2020  Sebastian Henz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


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
                self.close
            )
        )

    def process_event(self, event, event_manager):
        super().process_event(event, event_manager)
        if event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_escape:
                self.close()

    def draw(self):
        self.target_surface.fill((100, 100, 100))  # DEBUG: red to check if rounded buttons work
        for b in self.buttons:
            self.target_surface.blit(b.image, b.rect)

    def new_game(self):
        self.persistent_scene_data["world name"] = "test"
        # Make sure the main game is a fresh instance:
        self.persistent_scene_data.pop("main game cache", None)
        self.close("main game")

    def goto_options(self):
        self.close("options menu")
