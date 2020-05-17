"""Main loop."""

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

import src.constants as const
from src.states.main_game import MainGame


def run(display):
    states = {"MainGame": MainGame("test")}
    state = states["MainGame"]

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(const.FPS)

        if pygame.event.get(pygame.QUIT):
            break
        else:
            state.process_events()

        if state.done:
            persistent_state_data = state.close()
            next_state_name = persistent_state_data["next_state_name"]
            if next_state_name == "quit":
                break
            state = states[next_state_name]
            state.start(persistent_state_data)

        state.update(dt)

        state.draw(display)
        pygame.display.flip()
