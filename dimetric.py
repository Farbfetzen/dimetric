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
from src.states import game_states
from src.event_manager import EventManager


def run():
    pygame.init()
    assert pygame.font.get_init(), "Font module not initialized!"
    main_display = pygame.display.set_mode(constants.MAIN_DISPLAY_SIZE)
    small_display = pygame.Surface(constants.SMALL_DISPLAY_SIZE)
    resources.load_options()
    resources.load_images()
    resources.load_worlds()
    event_manager = EventManager()
    state = game_states["MainMenu"]()
    clock = pygame.time.Clock()

    while True:
        # delta time of previous tick in seconds. Protect against hiccups
        # (e.g. from moving the pygame window) by limiting to 0.1 s.
        dt = min(clock.tick(constants.FPS) / 1000, 0.1)

        event_manager.process_events(state)

        if state.is_done:
            # TODO: Make it possible to resume a state instance from a stack
            #  instead of starting a new instance. At the moment states are
            #  always new instances.
            persistent_state_data = state.persistent_state_data
            next_state_name = persistent_state_data["next_state_name"]
            if next_state_name == "quit":
                # TODO: If there are unsaved changes, ask if they should be
                #  saved, discarded or if the exit should be canceled.
                break
            elif next_state_name == "MainGame":
                world_name = persistent_state_data["world_name"]
                state = game_states[next_state_name](world_name)
            else:
                state = game_states[next_state_name]()
            state.resume(persistent_state_data)

        state.update(dt)

        state.draw(small_display)
        pygame.transform.scale(
            small_display,
            constants.MAIN_DISPLAY_SIZE,
            main_display
        )
        if state.dev_overlay_visible:
            state.draw_dev_overlay(main_display, clock)
        pygame.display.flip()


if __name__ == "__main__":
    run()
