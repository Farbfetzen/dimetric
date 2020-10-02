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
from src.scenes import SCENES
from src.event_manager import EventManager


class Game:
    def __init__(self, initial_scene_name):
        pygame.init()
        self.main_display = pygame.display.set_mode(constants.MAIN_DISPLAY_SIZE)
        self.small_display = pygame.Surface(constants.SMALL_DISPLAY_SIZE)
        resources.load_all()
        self.running = True
        self.active_scenes = []
        self.active_scenes.append(SCENES[initial_scene_name](self))
        self.active_scenes_reversed = list(reversed(self.active_scenes))
        # Only the dev overlay of the front scene may be active and visible.
        self.active_dev_overlay = self.active_scenes[-1].dev_overlay
        self.dev_overlay_visible = True
        self.persistent_scene_data = {}
        self.active_scenes[-1].start()

    def change_scenes(self, remove, new_scene_name=""):
        for r in remove:
            self.active_scenes.remove(r)
        if not new_scene_name:
            if not self.active_scenes:
                print(new_scene_name)
                self.quit()
        else:
            if new_scene_name == "main game":
                world_name = self.persistent_scene_data["world name"]
                new_scene = SCENES[new_scene_name](self, world_name)
                self.active_scenes.append(new_scene)
            else:
                new_scene = SCENES[new_scene_name](self)
                self.active_scenes.append(new_scene)
            new_scene.start()
        if self.active_scenes:
            self.active_scenes_reversed = list(reversed(self.active_scenes))
            self.active_dev_overlay = self.active_scenes[-1].dev_overlay
        # print(self.active_scenes)

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

            for event in pygame.event.get():
                # process events front to back
                for scene in self.active_scenes_reversed:
                    if scene.process_event(event, event_manager) is not None:
                        break

            # update front to back
            for scene in self.active_scenes_reversed:
                if scene.update(dt) is not None:
                    break

            # draw back to front
            for scene in self.active_scenes:
                scene.draw()

            pygame.transform.scale(
                self.small_display,
                constants.MAIN_DISPLAY_SIZE,
                self.main_display
            )
            if self.dev_overlay_visible:
                self.active_dev_overlay.update(clock)
                self.active_dev_overlay.draw()
            pygame.display.flip()


if __name__ == "__main__":
    game = Game("main menu")
    game.run()
