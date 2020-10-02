"""Run this file to run the game."""

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


import os
# Must be done before importing Pygame:
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEO_CENTERED"] = "1"

import pygame
import pygame.freetype

from src import constants
from src import resources
from src import scenes
from src.event_manager import EventManager


class Game:
    def __init__(self, initial_scene_name):
        pygame.init()
        self.main_display = pygame.display.set_mode(constants.MAIN_DISPLAY_SIZE)
        self.small_display = pygame.Surface(constants.SMALL_DISPLAY_SIZE)
        resources.load_all()
        self.running = True
        self.scenes = {
            "main menu": scenes.MainMenu,
            "options menu": scenes.OptionsMenu,
            "main game": scenes.MainGame,
            "pause menu": scenes.PauseMenu
        }
        self.scene = self.scenes[initial_scene_name](self)

    def change_scenes(self, next_scene_name):
        persistent_scene_data = self.scene.persistent_scene_data
        if next_scene_name == "main game":
            if "main game cache" in persistent_scene_data:
                self.scene = persistent_scene_data["main game cache"]
            else:
                world_name = persistent_scene_data["world name"]
                self.scene = self.scenes[next_scene_name](self, world_name)
        else:
            self.scene = self.scenes[next_scene_name](self)
        self.scene.start(persistent_scene_data)

    def quit(self):
        # TODO: If there are unsaved changes, ask if they should be
        #  saved, discarded or if the exit should be canceled. That
        #  popup will be its own scene. And that one may then exit the game.
        self.running = False

    def run(self):
        event_manager = EventManager()
        clock = pygame.time.Clock()

        while self.running:
            # delta time of previous tick in seconds.
            # Protect against hiccups (e.g. from moving the pygame window)
            # by limiting to 100 milliseconds.
            dt = min(clock.tick(constants.FPS), 100) / 1000

            event_manager.process_events(self.scene)
            self.scene.update(dt)

            self.scene.draw(self.small_display)
            pygame.transform.scale(
                self.small_display,
                constants.MAIN_DISPLAY_SIZE,
                self.main_display
            )
            if self.scene.dev_overlay.is_visible:
                self.scene.dev_overlay.update(clock)
                self.scene.dev_overlay.draw(self.main_display)
            pygame.display.flip()


if __name__ == "__main__":
    game = Game("main menu")
    game.run()
